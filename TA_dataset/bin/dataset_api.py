import requests
import json
import time
from dataset_common import normalize_time

import logging

# Dataset V2 API client (generated)
from dataset_query_api_client import AuthenticatedClient
from dataset_query_api_client.models import PostQueriesLaunchQueryRequestBody, PostQueriesLaunchQueryRequestBodyQueryType, PostQueriesLaunchQueryRequestBodyQueryPriority, LogAttributes, PQAttributes, FacetValuesAttributes, QueryResult
from dataset_query_api_client.api.default import post_queries, get_queries, delete_queries
from dataset_query_api_client.types import Response

# Executes Dataset LongRunningQuery for log events
def ds_lrq_log_query(base_url, api_key, start_time, end_time, filter_expr, limit):
    client = AuthenticatedClient(base_url=base_url, token=api_key)
    body = PostQueriesLaunchQueryRequestBody(
        query_type = PostQueriesLaunchQueryRequestBodyQueryType.LOG,
        start_time = start_time,
        end_time = end_time,
        log = LogAttributes(filter_ = filter_expr, limit = limit)
    )
    return ds_lrq_run_loop(client = client, body= body)

# Executes Dataset LongRunningQuery using PowerQuery language
def ds_lrq_power_query(base_url, api_key, start_time, end_time, query):
    client = AuthenticatedClient(base_url=base_url, token=api_key)
    body = PostQueriesLaunchQueryRequestBody(
        query_type = PostQueriesLaunchQueryRequestBodyQueryType.PQ,
        start_time = start_time,
        end_time = end_time,
        pq = PQAttributes(query = query)
    )
    return ds_lrq_run_loop(client = client, body = body)

# Executes Dataset LongRunningQuery to fetch facet values
def ds_lrq_facet_values(base_url, api_key, start_time, end_time, filter, name, max_values):
    client = AuthenticatedClient(base_url=base_url, token=api_key)
    body = PostQueriesLaunchQueryRequestBody(
        query_type = PostQueriesLaunchQueryRequestBodyQueryType.FACET_VALUES,
        start_time = start_time,
        end_time = end_time,
        facet_values = FacetValuesAttributes(filter_ = filter, name = name, max_values = max_values)
    )
    return ds_lrq_run_loop(client = client, body = body)

# Executes LRQ run loop of launch-ping-remove API requests until the query completes with a result
def ds_lrq_run_loop(client, body: PostQueriesLaunchQueryRequestBody):
    body.query_priority = PostQueriesLaunchQueryRequestBodyQueryPriority.HIGH
    response = post_queries.sync_detailed(client = client, json_body = body)
    result = response.parsed
    forward_tag = response.headers["x-dataset-query-forward-tag"]
    steps_done = result.steps_completed
    steps_total = result.steps_total
    query_id = result.id
    while (steps_done < steps_total):
        response = get_queries.sync_detailed(id = query_id, query_type=body.query_type, client = client, last_step_seen = steps_done, forward_tag = forward_tag)
        result = response.parsed
        steps_done = result.steps_completed
    delete_queries.sync_detailed(id = query_id, client = client, forward_tag = forward_tag)

    return result

# Returns a valid PowerQuery incorporating provided filter, columns and limit
def ds_build_pq(filter, columns, limit):
    result =  filter if (filter is not None) else '*'
    if columns is not None:
        result += " | columns " + str(columns)
    if (limit is not None):
        result += " | limit " + str(limit)
    return result

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
        ds_payload['query'] = ds_build_pq(ds_search, ds_columns, maxcount)
    
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

    splunk_dt = parse_splunk_dt(ds_event)

    return (ds_event, splunk_dt)


# Extracts event timestamp from the Dataset event dictionary and converts it to seconds
def parse_splunk_dt(ds_event):
    #if timestamp exists, convert epoch nanoseconds to seconds for Splunk
    if '_time' in ds_event:
        splunk_dt = normalize_time(int(ds_event['_time']))
    elif 'timestamp' in ds_event:
        splunk_dt = normalize_time(int(ds_event['timestamp']))
    else:
        #Splunk does not parse events well without a timestamp, use current time to fix this
        splunk_dt = int(time.time())
    return splunk_dt


def parse_powerquery(value_list, columns):
    ds_event_dict = {}

    for counter in range(len(value_list)):
        ds_event_dict[columns[counter]['name']] = value_list[counter]

    #PowerQuery results are returned by default in chronological order
    ds_event = json.loads(json.dumps(ds_event_dict))

    #if timestamp exists, convert epoch nanoseconds to seconds for Splunk
    splunk_dt = parse_splunk_dt(ds_event)
    
    return (ds_event, splunk_dt)


def get_bucket_increments(ds_start, ds_end, ts_buckets):
    #determine timestamp by adding bucket_time to start_time x number of iterations (+1 since indices start at 0)
    bucket_time = (ds_end - ds_start) / ts_buckets
    return bucket_time