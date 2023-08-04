# -*- coding: utf-8 -*-
import requests
from dataset_api import *
from dataset_common import *
from solnlib import log
from solnlib.modular_input import checkpointer
from splunklib import modularinput as smi

APP_NAME = __file__.split(op.sep)[-3]


class DATASET_POWERQUERY_INPUT(smi.Script):
    def __init__(self):
        super(DATASET_POWERQUERY_INPUT, self).__init__()

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
                "account",
                title="Account",
                description="DataSet account",
                required_on_create=True,
                required_on_edit=True,
            )
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
                required_on_create=True,
                required_on_edit=True,
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
            ds_payload = build_payload(ds_start, ds_end, "powerquery", ds_search)
            proxy = get_proxy(session_key, logger)
            acct_dict = get_acct_info(self, logger, ds_account)
            for ds_acct in acct_dict.keys():
                ds_url = get_url(acct_dict[ds_acct]["base_url"], "powerquery")
                ds_headers = {
                    "Authorization": "Bearer " + acct_dict[ds_acct]["ds_api_key"]
                }

                # Create checkpointer
                checkpoint = checkpointer.KVStoreCheckpointer(
                    input_name, session_key, APP_NAME
                )

                logger.debug(
                    "DataSetFunction=sendRequest, destination={}, startTime={}".format(
                        ds_url, time.time()
                    )
                )
                r = requests.post(
                    url=ds_url, headers=ds_headers, json=ds_payload, proxies=proxy
                )
                r_json = r.json()  # parse results json

                # first, validate success
                if r.ok:
                    # log information from results
                    if "status" in r_json:
                        logger.info("response status={}".format(r_json["status"]))

                    if "warnings" in r_json:
                        for warning in r_json["warnings"]:
                            logger.warning("response warning={}".format(warning))

                    if "matchingEvents" in r_json:
                        logger.info(
                            "response matches={}".format(r_json["matchingEvents"])
                        )

                    if "cpuUsage" in r_json:
                        logger.info("cpuUsage={}".format(r_json["cpuUsage"]))

                    # parse results, match returned columns with corresponding values
                    if "columns" in r_json and "values" in r_json:
                        for value_list in r_json["values"]:
                            ds_event, splunk_dt = parse_powerquery(
                                value_list, r_json["columns"]
                            )
                            get_checkpoint = checkpoint.get(input_name)

                            # if checkpoint doesn't exist, set to 0
                            if get_checkpoint is None:
                                checkpoint.update(input_name, {"timestamp": 0})
                                checkpoint_time = 0
                            else:
                                checkpoint_time = float(get_checkpoint["timestamp"])

                            if splunk_dt > checkpoint_time:
                                # if greater than current checkpoint, write event and update checkpoint
                                event = smi.Event(
                                    stanza=input_name,
                                    data=json.dumps(ds_event),
                                    sourcetype="dataset:powerquery",
                                    time=splunk_dt,
                                )
                                logger.debug(
                                    "writing event with splunk_dt={}, checkpoint={}".format(
                                        splunk_dt, checkpoint_time
                                    )
                                )
                                ew.write_event(event)

                                logger.debug("saving checkpoint {}".format(splunk_dt))
                                checkpoint.update(input_name, {"timestamp": splunk_dt})
                            else:
                                logger.debug(
                                    "skipping due to splunk_dt={} is less than checkpoint={}".format(
                                        splunk_dt, checkpoint_time
                                    )
                                )

                    else:  # if no resulting ['values'] and ['columns']
                        logger.warning("DataSet response success, no matches returned")

        except Exception as e:
            logger.exception(e)
            sys.exit(1)


if __name__ == "__main__":
    exitcode = DATASET_POWERQUERY_INPUT().run(sys.argv)
    sys.exit(exitcode)
