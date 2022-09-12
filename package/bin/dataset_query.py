import os
import os.path as op
import sys
import time
import datetime
import json
import requests
import traceback
import math

from dataset_common import *

import import_declare_test
from splunklib import modularinput as smi
from solnlib import conf_manager, log

APP_NAME = __file__.split(op.sep)[-3]


class DATASET_QUERY_INPUT(smi.Script):

    def __init__(self):
        super(DATASET_QUERY_INPUT, self).__init__()

    def get_scheme(self):
        scheme = smi.Scheme("DataSet Alerts")
        scheme.description = ("Go to the add-on\'s configuration UI and configure modular inputs under the Inputs menu.")
        scheme.use_external_validation = True
        scheme.streaming_mode_xml = True
        scheme.use_single_instance = False

        scheme.add_argument(smi.Argument("name", title="Name",
                                         description="",
                                         required_on_create=True))

        scheme.add_argument(smi.Argument("start_time", title="Start Time",
                                         description="Relative start time to query back. Use short form relative time, e.g.: 24h or 30d. Reference https://app.scalyr.com/help/time-reference",
                                         required_on_create=True,
                                         required_on_edit=True))

        scheme.add_argument(smi.Argument("end_time", title="End Time",
                                         description="Relative end time to query back. Use short form relative time.",
                                         required_on_create=False,
                                         required_on_edit=False))

        scheme.add_argument(smi.Argument("dataset_query_string", title="Query String",
                                         description="The DataSet query exectued to return matching results.",
                                         required_on_create=False,
                                         required_on_edit=False))
        
        scheme.add_argument(smi.Argument("dataset_query_columns", title="Columns",
                                         description="Specified columns to return.",
                                         required_on_create=False,
                                         required_on_edit=False))

        scheme.add_argument(smi.Argument("max_count", title="Max Count",
                                         description="The maximum number of records to return.",
                                         required_on_create=False,
                                         required_on_edit=False))
        return scheme


    def validate_input(self, definition):
        pass

    def stream_events(self, inputs, ew):
        meta_configs = self._input_definition.metadata
        session_key = meta_configs['session_key']
        input_name = list(inputs.inputs.keys())[0]

        input_items = {}
        input_items = inputs.inputs[input_name]

        # Generate logger with input name
        _, input_name = (input_name.split('//', 2))
        logger = log.Logs().get_logger('{}_input'.format(APP_NAME))

        # Log level configuration
        log_level = get_log_level(session_key, logger)
        logger.setLevel(log_level)

        logger.debug("Modular input invoked.")

        # Input logic here
        try:
            #Create checkpointer
            checkpoint = checkpointer.KVStoreCheckpointer(
                input_name,
                session_key,
                APP_NAME
            )
            ds_start_time = input_items.get('start_time')
            #convert start time to epoch, necessary for recursive calls with continuation token
            ds_st = relative_to_epoch(ds_start_time)

            ds_environment = get_environment(session_key, logger)
            ds_url_endpoint = 'query'
            ds_url = get_url(ds_environment) + ds_url_endpoint
            ds_api_key = get_token(session_key, logger, 'read')
            ds_headers = { "Authorization": "Bearer " + ds_api_key }
            ds_proxy = get_proxy(session_key, logger)

            ds_payload = { "queryType": "log", "startTime": ds_st }

            ds_end_time = input_items.get('end_time')
            ds_query = input_items.get('dataset_query_string')
            ds_columns = input_items.get('dataset_query_columns')
            ds_max_count = int(input_items.get('max_count'))

            api_maxcount = 100

            if ds_end_time:
                ds_et = relative_to_epoch(ds_end_time)
                ds_payload['endTime'] = ds_et
            if ds_query:
                ds_payload['filter'] = ds_query
            if ds_columns:
                ds_payload['columns'] = ds_columns
            if ds_max_count:
                api_maxcount = get_maxcount(ds_max_count)
                ds_payload['maxCount'] = api_maxcount
            else:
                ds_max_count = 100

            ds_iterations = math.ceil(ds_max_count / 5000)
            for count in range(ds_iterations):
                logger.info("query api {} of {}".format(count+1, ds_iterations))
                r = requests.post(url=ds_url, headers=ds_headers, json=ds_payload, proxies=ds_proxy)
                r_json = r.json() #parse results json

                #first, validate success
                if r.ok:
                    if 'warnings' in r_json :
                        logger.warning(r_json["warnings"])
                    
                    #response includes good information for debug logging
                    if 'executionTime' in r_json:
                        logger.debug("executionTime %s" % (str(r_json['executionTime'])))

                    if 'cpuUsage' in r_json:
                        logger.debug("cpuUsage is %s" % (str(r_json['cpuUsage'])))

                    if 'matches' in r_json and 'sessions' in r_json:
                        #parse results, match returned matches with corresponding sessions
                        matches = r_json['matches']
                        sessions = r_json['sessions']
                        
                        for match_list in matches:
                            ds_event_dict = {}
                            ds_event_dict = match_list

                            #if columns were given, simply return matches and skip merging session data
                            #if columns were not given, merge sessions and matches to return all fields
                            if not ds_columns:
                                session_key = match_list['session']

                                for session_entry, session_dict in sessions.items():
                                    if session_entry == session_key:
                                        for key in session_dict:
                                            ds_event_dict[key] = session_dict[key]

                            if 'timestamp' in ds_event_dict:
                                event_time = int(ds_event_dict['timestamp'])
                            else:
                                #if no timestamp, use current time in nanoseconds
                                event_time = int(time.time()) * 1000000000

                            get_checkpoint = checkpoint.get(input_name)

                            #if checkpoint doesn't exist, set to 0
                            if get_checkpoint == None:
                                checkpoint.update(input_name, {"timestamp": 0})
                                checkpoint_time = 0
                            else:
                                checkpoint_time = get_checkpoint["timestamp"]

                            if event_time > checkpoint_time:
                                #if greater than current checkpoint, write event and update checkpoint
                                splunk_dt = normalize_time(int(event_time))
                                ds_event = json.dumps(ds_event_dict)
                                #create and write event
                                event = smi.Event(
                                    stanza=input_name,
                                    data=ds_event,
                                    source=input_name,
                                    sourcetype='dataset:query',
                                    time=splunk_dt
                                )
                                logger.debug("writing event with event_time=%s and checkpoint=%s" % (str(event_time), str(checkpoint_time)))
                                ew.write_event(event)

                                logger.debug("saving checkpoint %s" % (str(event_time)))
                                checkpoint.update(input_name, {"timestamp": event_time})
                            else:
                                logger.debug("skipping due to event_time=%s is less than checkpoint=%s" % (str(event_time), str(checkpoint_time)))

                    else:
                        logger.info("no matching events")

                    #after first call, set continuationToken
                    if 'continuationToken' in r_json:
                        ds_payload['continuationToken'] = r_json['continuationToken']
                        #reduce maxcount for each call, then for last call set payload to only return remaining # of desired results
                        ds_max_count = ds_max_count - api_maxcount
                        if ds_max_count > 0 and ds_max_count < 5000:
                            ds_payload['maxCount'] = ds_max_count
                    else:
                        break
                else:
                    if 'message' in r_json:
                        logger.error(r_json['message'])
                    else:
                        logger.error("response = {}".format(r_json))
                    break

        except Exception as e:
            logger.exception(e)
            sys.exit(1)


if __name__ == "__main__":
    exitcode = DATASET_QUERY_INPUT().run(sys.argv)
    sys.exit(exitcode)