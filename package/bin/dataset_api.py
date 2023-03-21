import requests
import json
import time
from dataset_common import normalize_time

import logging


def build_payload(ds_start, ds_end, ds_method, ds_search=None, ds_columns=None, maxcount=None, f_field=None, ts_function="rate", ts_buckets=1, ts_create_summ=True, ts_use_summ=False):
    ds_payload = { 
        "startTime": ds_start,
        "endTime": ds_end
    }

    #handle different API endpoints
    if ds_method == 'query':
        ds_payload['queryType'] = "log"
        if ds_search is not None:
            ds_payload['filter'] = ds_search
        if ds_columns is not None:
            ds_payload['columns'] = ds_columns
        if maxcount is None:
            ds_payload['maxCount'] = 100
        else:
            ds_payload['maxCount'] = get_maxcount(maxcount)

    elif ds_method == 'powerquery':
        if ds_search is None:
            #powerquery requires query, set default if not given
            ds_payload['query'] = "'*'"
        else:
            ds_payload['query'] = ds_search
        if ds_columns is not None:
            ds_payload['query'] += "| columns " + str(ds_columns)
        if maxcount is not None:
            #powerQuery uses <| limit>
            ds_payload['query'] += "| limit " + str(maxcount)
    
    elif ds_method == 'facet':
        if ds_search is not None:
            ds_payload['filter'] = ds_search
        if maxcount is not None:
            ds_payload['maxCount'] = maxcount
        if f_field is None:
            #facetquery requires field, set default if not given
            ds_payload['field'] = "logfile"
        else:
            ds_payload['field'] = f_field

    elif ds_method == 'timeseries':
        if ds_search is not None:
            ds_payload['filter'] = ds_search
        ds_payload['function'] = ts_function
        ds_payload['buckets'] = ts_buckets
        ds_payload['createSummaries'] = ts_create_summ
        ds_payload['onlyUseSummaries'] = ts_use_summ
        ds_payload = { "queries": [ds_payload] }

    return ds_payload


def get_maxcount(max):
    #query API returns max 5,000 results per call
    if max > 5000:
        return 5000
    elif max == 0:
        return 100
    else:
        return max

def query_api_max():
    return 5000


def parse_query(ds_columns, match_list, sessions):
    ds_event_dict = {}
    ds_event_dict = match_list

    #if columns were given, simply return matches and skip merging session data
    #if columns were not given, merge sessions and matches to return all fields
    if ds_columns is None:
        session_key = match_list['session']

        for session_entry, session_dict in sessions.items():
            if session_entry == session_key:
                for key in session_dict:
                    ds_event_dict[key] = session_dict[key]

    ds_event = json.loads(json.dumps(ds_event_dict))

    #if timestamp exists, convert epoch nanoseconds to seconds for Splunk
    if 'timestamp' in ds_event:
        splunk_dt = normalize_time(int(ds_event['timestamp']))
    else:
        #Splunk does not parse events well without a timestamp, use current time to fix this
        splunk_dt = int(time.time())

    return (ds_event, splunk_dt)


def parse_powerquery(value_list, columns):
    ds_event_dict = {}

    for counter in range(len(value_list)):
        ds_event_dict[columns[counter]['name']] = value_list[counter]

    #PowerQuery results are returned by default in chronological order
    ds_event = json.loads(json.dumps(ds_event_dict))

    #if timestamp exists, convert epoch nanoseconds to seconds for Splunk
    if 'timestamp' in ds_event:
        splunk_dt = normalize_time(int(ds_event['timestamp']))
    else:                                
        splunk_dt = int(time.time())
    
    return (ds_event, splunk_dt)


def get_bucket_increments(ds_start, ds_end, ts_buckets):
    #determine timestamp by adding bucket_time to start_time x number of iterations (+1 since indices start at 0)
    bucket_time = (ds_end - ds_start) / ts_buckets
    return bucket_time