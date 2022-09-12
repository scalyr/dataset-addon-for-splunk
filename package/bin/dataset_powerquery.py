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


class DATASET_POWERQUERY_INPUT(smi.Script):

    def __init__(self):
        super(DATASET_POWERQUERY_INPUT, self).__init__()

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

            ds_environment = get_environment(session_key, logger)
            ds_url_endpoint = 'powerQuery'
            ds_url = get_url(ds_environment) + ds_url_endpoint
            ds_api_key = get_token(session_key, logger, 'read')
            ds_headers = { "Authorization": "Bearer " + ds_api_key }
            ds_proxy = get_proxy(session_key, logger)

            ds_payload = { "startTime": ds_start_time }

            ds_query = input_items.get('dataset_query_string')
            ds_payload['query'] = ds_query

            ds_end_time = input_items.get('end_time')
            if ds_end_time:
                ds_payload['endTime'] = ds_end_time        

            r = requests.post(url=ds_url, headers=ds_headers, json=ds_payload, proxies=ds_proxy)
            r_json = r.json() #parse results json

            #first, validate success
            if r.ok:
                #log information from results
                if 'status' in r_json:
                    logger.info("response status=%s" % str(r_json['status']))
                
                if 'warnings' in r_json:
                    for warning in r_json['warnings']:
                        logger.warning("response warning=%s" % str(warning))
                    
                if 'matchingEvents' in r_json:
                    logger.info("response matches=%s" % str(r_json['matchingEvents']))
                    
                if 'cpuUsage' in r_json:
                    logger.info('cpuUsage: %s ' % r_json['cpuUsage'] )

                #parse results, match returned columns with corresponding values
                if 'columns' in r_json and 'values' in r_json:
                    for value_list in r_json['values']:
                        ds_event_dict = {}

                        for counter in range(len(value_list)):
                            ds_event_dict[r_json['columns'][counter]['name']] = value_list[counter]
                    
                        #check event time against checkpoint
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
                            checkpoint_time = int(get_checkpoint["timestamp"])

                        if event_time > checkpoint_time:
                            #if greater than current checkpoint, write event and update checkpoint
                            splunk_dt = normalize_time(int(event_time))
                            ds_event = json.dumps(ds_event_dict)
                            #create and write event
                            event = smi.Event(
                                stanza=input_name,
                                data=ds_event,
                                source=input_name,
                                sourcetype='dataset:powerquery',
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

            else:
                if 'message' in r_json:
                    logger.error(r_json['message'])
                else:
                    logger.error("response = {}".format(r_json))

        except Exception as e:
            logger.exception(e)
            sys.exit(1)


if __name__ == "__main__":
    exitcode = DATASET_POWERQUERY_INPUT().run(sys.argv)
    sys.exit(exitcode)