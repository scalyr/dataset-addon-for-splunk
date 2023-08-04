#! /usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import math

import requests
from dataset_api import (
    build_payload,
    get_maxcount,
    json,
    parse_query,
    query_api_max,
    time,
)
from dataset_common import (
    get_acct_info,
    get_log_level,
    get_proxy,
    get_url,
    op,
    relative_to_epoch,
    sys,
)
from dataset_query_api_client.client import get_user_agent
from solnlib import log
from solnlib.modular_input import checkpointer
from splunklib import modularinput as smi

APP_NAME = __file__.split(op.sep)[-3]


class DATASET_QUERY_INPUT(smi.Script):
    def __init__(self):
        super(DATASET_QUERY_INPUT, self).__init__()

    def get_scheme(self):
        scheme = smi.Scheme("DataSet Alerts")
        scheme.description = "Go to the add-on's configuration UI and configure modular inputs under the Inputs menu."
        scheme.use_external_validation = True
        scheme.streaming_mode_xml = True
        scheme.use_single_instance = False

        scheme.add_argument(
            smi.Argument("name", title="Name", description="", required_on_create=True)
        )

        scheme.add_argument(
            smi.Argument(
                "start_time",
                title="Start Time",
                description="Relative start time to query back. Use short form relative time, e.g.: 24h or 30d. Reference https://app.scalyr.com/help/time-reference",
                required_on_create=True,
                required_on_edit=True,
            )
        )

        scheme.add_argument(
            smi.Argument(
                "end_time",
                title="End Time",
                description="Relative end time to query back. Use short form relative time.",
                required_on_create=False,
                required_on_edit=False,
            )
        )

        scheme.add_argument(
            smi.Argument(
                "dataset_query_string",
                title="Query String",
                description="The DataSet query exectued to return matching results.",
                required_on_create=False,
                required_on_edit=False,
            )
        )

        scheme.add_argument(
            smi.Argument(
                "dataset_query_columns",
                title="Columns",
                description="Specified columns to return.",
                required_on_create=False,
                required_on_edit=False,
            )
        )

        scheme.add_argument(
            smi.Argument(
                "max_count",
                title="Max Count",
                description="The maximum number of records to return.",
                required_on_create=False,
                required_on_edit=False,
            )
        )
        return scheme

    def validate_input(self, definition):
        pass

    def stream_events(self, inputs, ew):
        meta_configs = self._input_definition.metadata
        session_key = meta_configs["session_key"]
        input_name = list(inputs.inputs.keys())[0]

        input_items = {}
        input_items = inputs.inputs[input_name]

        # Generate logger with input name
        _, input_name = input_name.split("//", 2)
        logger = log.Logs().get_logger("{}_input".format(APP_NAME))

        # Log level configuration
        log_level = get_log_level(session_key, logger)
        logger.setLevel(log_level)

        logger.debug("Modular input invoked.")

        # Input logic here
        try:
            ds_account = input_items.get("account")
            ds_start = input_items.get("start_time")
            ds_end = input_items.get("end_time")
            ds_search = input_items.get("dataset_query_string")
            ds_columns = input_items.get("dataset_query_columns")
            maxcount = input_items.get("max_count")

            ds_st = relative_to_epoch(ds_start)
            if ds_end:
                ds_et = relative_to_epoch(ds_end)
            else:
                ds_et = relative_to_epoch("1s")
            if maxcount:
                ds_maxcount = int(maxcount)
            else:
                ds_maxcount = get_maxcount(0)

            ds_payload = build_payload(
                ds_st, ds_et, "query", ds_search, ds_columns, ds_maxcount
            )
            logger.debug("ds_payload = {}".format(ds_payload))
            proxy = get_proxy(session_key, logger)
            acct_dict = get_acct_info(self, logger, ds_account)
            for ds_acct in acct_dict.keys():
                curr_payload = copy.deepcopy(ds_payload)
                curr_maxcount = copy.copy(ds_maxcount)
                ds_url = get_url(acct_dict[ds_acct]["base_url"], "query")
                ds_headers = {
                    "Authorization": "Bearer " + acct_dict[ds_acct]["ds_api_key"],
                    "User-Agent": get_user_agent(),
                }

                # Create checkpointer
                checkpoint = checkpointer.KVStoreCheckpointer(
                    input_name, session_key, APP_NAME
                )

                ds_api_max = query_api_max()
                ds_iterations = math.ceil(ds_maxcount / ds_api_max)

                for count in range(ds_iterations):
                    logger.info("query api {} of {}".format(count + 1, ds_iterations))
                    logger.debug(
                        "DataSetFunction=sendRequest, destination={}, startTime={}".format(
                            ds_url, time.time()
                        )
                    )
                    r = requests.post(
                        url=ds_url, headers=ds_headers, json=curr_payload, proxies=proxy
                    )
                    logger.debug(
                        "DataSetFunction=getResponse, elapsed={}".format(r.elapsed)
                    )
                    r_json = r.json()

                    if r.ok:
                        # log any warnings
                        if "warnings" in r_json:
                            logger.warning(r_json["warnings"])

                        if "matches" in r_json and "sessions" in r_json:
                            matches = r_json["matches"]
                            sessions = r_json["sessions"]

                            if len(matches) == 0 and len(sessions) == 0:
                                logger.warning(
                                    "DataSet response success, no matches returned"
                                )
                                logger.warning(r_json)

                            for match_list in matches:
                                ds_event, splunk_dt = parse_query(
                                    ds_columns, match_list, sessions
                                )
                                get_checkpoint = checkpoint.get(input_name)

                                # if checkpoint doesn't exist, set to 0
                                if get_checkpoint is None:
                                    checkpoint.update(input_name, {"timestamp": 0})
                                    checkpoint_time = 0
                                else:
                                    checkpoint_time = get_checkpoint["timestamp"]

                                if splunk_dt > checkpoint_time:
                                    # if greater than current checkpoint, write event and update checkpoint
                                    event = smi.Event(
                                        stanza=input_name,
                                        data=json.dumps(ds_event),
                                        sourcetype="dataset:query",
                                        time=splunk_dt,
                                    )
                                    logger.debug(
                                        "writing event with splunk_dt={}, checkpoint={}".format(
                                            splunk_dt, checkpoint_time
                                        )
                                    )
                                    ew.write_event(event)

                                    logger.debug(
                                        "saving checkpoint {}".format(splunk_dt)
                                    )
                                    checkpoint.update(
                                        input_name, {"timestamp": splunk_dt}
                                    )
                                else:
                                    logger.debug(
                                        "skipping due to splunk_dt={} is less than checkpoint={}".format(
                                            splunk_dt, checkpoint_time
                                        )
                                    )

                        else:
                            logger.warning(
                                "DataSet response success, no matches returned"
                            )

                        # after first call, set continuationToken
                        if "continuationToken" in r_json:
                            curr_payload["continuationToken"] = r_json[
                                "continuationToken"
                            ]
                            # reduce maxcount for each call, then for last call set payload to only return remaining # of desired results
                            curr_maxcount = curr_maxcount - ds_api_max
                            if curr_maxcount > 0 and curr_maxcount < ds_api_max:
                                curr_payload["maxCount"] = curr_maxcount

                    else:
                        logger.warning(r_json)
                        break

        except Exception as e:
            logger.exception(e)
            sys.exit(1)


if __name__ == "__main__":
    exitcode = DATASET_QUERY_INPUT().run(sys.argv)
    sys.exit(exitcode)
