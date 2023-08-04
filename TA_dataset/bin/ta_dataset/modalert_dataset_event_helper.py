# -*- coding: utf-8 -*-
import json
import uuid

from dataset_api import *
from dataset_common import *


def process_event(helper, *args, **kwargs):
    """
    # IMPORTANT
    # Do not remove the anchor macro:start and macro:end lines.
    # These lines are used to generate sample code. If they are
    # removed, the sample code will not be updated when configurations
    # are updated.

    [sample_code_macro:start]

    # The following example gets the alert action parameters and prints them to the log
    account = helper.get_param("account")
    helper.log_info("account={}".format(account))

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

    # TODO: Implement your alert action logic here
    account = helper.get_param("account")

    try:
        ds_user_cred = helper.get_user_credential_by_account_id(account)
        acct_dict = {}
        acct_dict[account] = {}
        acct_dict[account]["base_url"] = ds_user_cred["url"]
        acct_dict[account]["ds_api_key"] = ds_user_cred["dataset_log_write_access_key"]

        ds_url = get_url(acct_dict[account]["base_url"], "addevents")
        ds_headers = {"Authorization": "Bearer " + acct_dict[account]["ds_api_key"]}

        dataset_serverhost = helper.get_param("dataset_serverhost")
        dataset_severity = int(helper.get_param("dataset_severity"))
        dataset_message = helper.get_param("dataset_message")
        dataset_parser = helper.get_param("dataset_parser")
        ds_uuid = str(uuid.uuid4())

        events = helper.get_events()
        counter = 1

        ds_event_dict = {}
        ds_event_dict["events"] = []
        ds_event_dict["threads"] = []

        for event in events:
            if counter == 1:
                # on first event, format payload for DataSet addEvents API
                ds_event_dict["session"] = ds_uuid
                ds_event_dict["sessionInfo"] = {"serverHost": dataset_serverhost}

            # for all events, append details
            # convert Splunk _time to nanoseconds, string representation of float requires double conversion of string -> float -> int
            ds_time = int(float(event["_time"])) * 1000000000
            ds_event_dict["events"].append(
                {
                    "thread": str(counter),
                    "ts": str(ds_time),
                    "sev": dataset_severity,
                    "tag": "splunk",
                    "attrs": {
                        "message": dataset_message,
                        "Application": "splunk",
                        "parser": dataset_parser,
                    },
                }
            )
            ds_event_dict["threads"].append(
                {"id": counter, "name": "splunk alert " + str(counter)}
            )

            counter += 1

        ds_payload = json.loads(json.dumps(ds_event_dict))
        helper.log_debug("payload = {}".format(ds_payload))
        # ModularAlertBase includes send_http_request method which includes helpers to handle proxy configuration
        r = helper.send_http_request(
            ds_url, "POST", parameters=None, payload=ds_payload, headers=ds_headers
        )
        helper.log_debug("response={}".format(r.text))
        helper.log_debug("elapsed={}".format(r.elapsed))

    except Exception as e:
        helper.log_error(e)
        return 1

    return 0
