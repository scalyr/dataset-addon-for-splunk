# encoding = utf-8
import uuid
import datetime
import json
import requests
from dataset_common import get_url

def process_event(helper, *args, **kwargs):
    """
    # IMPORTANT
    # Do not remove the anchor macro:start and macro:end lines.
    # These lines are used to generate sample code. If they are
    # removed, the sample code will not be updated when configurations
    # are updated.

    [sample_code_macro:start]

    # The following example gets the alert action parameters and prints them to the log
    dataset_serverhost = helper.get_param("dataset_serverhost")
    helper.log_info("dataset_serverhost={}".format(dataset_serverhost))

    dataset_message = helper.get_param("dataset_message")
    helper.log_info("dataset_message={}".format(dataset_message))

    dataset_severity = helper.get_param("dataset_severity")
    helper.log_info("dataset_severity={}".format(dataset_severity))


    # The following example adds two sample events ("hello", "world")
    # and writes them to Splunk
    # NOTE: Call helper.writeevents() only once after all events
    # have been added
    helper.addevent("hello", sourcetype="sample_sourcetype")
    helper.addevent("world", sourcetype="sample_sourcetype")
    helper.writeevents(index="summary", host="localhost", source="localhost")

    # The following example gets the events that trigger the alert
    events = helper.get_events()
    for event in events:
        helper.log_info("event={}".format(event))

    # helper.settings is a dict that includes environment configuration
    # Example usage: helper.settings["server_uri"]
    helper.log_info("server_uri={}".format(helper.settings["server_uri"]))
    [sample_code_macro:end]
    """

    helper.set_log_level(helper.log_level)
    helper.log_debug("Alert action dataset_event started.")

    # TODO: Implement your alert action logic here
    try:
        #ModularAlertBase includes helpers to get settings, alleviating need to use generic SDK or dataset_common methods
        ds_environment = helper.get_global_setting("dataset_environment")
        ds_url = get_url(ds_environment) + 'addEvents'
        ds_api_key = helper.get_global_setting("dataset_log_write_access_key")

        dataset_serverhost = helper.get_param("dataset_serverhost")
        dataset_severity = int(helper.get_param('dataset_severity'))
        dataset_message = helper.get_param('dataset_message')

        ds_uuid = str(uuid.uuid4())
        ds_headers = { "Authorization": "Bearer " + ds_api_key }

        events = helper.get_events()
        counter = 1

        ds_event_dict = {}
        ds_event_dict["events"] = []
        ds_event_dict["threads"] = []

        for event in events:

            if counter == 1:
                #on first event, format payload for DataSet addEvents API
                ds_event_dict["session"] = ds_uuid
                ds_event_dict["sessionInfo"] = {
                    "serverHost": dataset_serverhost
                }

            #for all events, append details
            #convert Splunk _time to nanoseconds, string representation of float requires double conversion of string -> float -> int
            ds_time = int(float(event["_time"])) * 1000000000
            ds_event_dict["events"].append(
                {
                    "thread": str(counter),
                    "ts": str(ds_time),
                    "sev": dataset_severity,
                    "tag": "splunk",
                    "attrs": {
                        "message": dataset_message,
                        "Application": "splunk"
                    }
                }
            )
            ds_event_dict["threads"].append(
                {
                    "id": counter,
                    "name": "splunk alert " + str(counter)
                }
            )

            counter +=1

        ds_payload = json.loads(json.dumps(ds_event_dict))
        #ModularAlertBase includes send_http_request method which includes helpers to handle proxy configuration
        r = helper.send_http_request(ds_url, 'POST', parameters=None, payload=ds_payload, headers=ds_headers)
        helper.log_debug("response = %s" % r.text)
        
    except Exception as e:
        helper.log_error(e)
        return 1

    return 0