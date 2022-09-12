# encoding = utf-8

import os
import sys
import time
import datetime
import json
from tracemalloc import start
import requests
import ast
from dataset_common import get_url, normalize_time, relative_to_epoch, get_maxcount
import logging
import math
import re

#From Splunk UCC
import import_declare_test
#Splunk Enterprise SDK
from splunklib.searchcommands import dispatch, GeneratingCommand, Configuration, Option, validators


def get_read_token(self):
    #use Python SDK secrets retrieval
    for credential in self.service.storage_passwords:
        cred = credential.content.get('clear_password')

        #Python SDK uses custom names, so filter resulting string to known key instead of by name
        if 'dataset_log_read_access_key' in cred:
            #convert string to json and get corresponding value
            cred_json = json.loads(cred)
            token = cred_json['dataset_log_read_access_key']
            return token


@Configuration()
class DataSetSearch(GeneratingCommand):
    method = Option(doc='''
        **Syntax: method=(query|powerQuery|timeseries)
        **Description:** DataSet endpoint to use: simple query, powerQuery or timeseries''', 
        require=False, validate=validators.Match('query', '(?i)query|powerQuery|timeseries'))
    
    search = Option(doc='''
        **Syntax: search=<string>
        **Description:** DataSet search to filter events''', 
        require=False)
    
    columns = Option(doc='''
        **Syntax: columns=<string>
        **Description:** Specified columns to return''', 
        require=False)

    maxcount = Option(doc='''
        **Syntax: maxcount=<integer>
        **Description:** the number of events to return from DataSet. Default is 100.''', 
        require=False, validate=validators.Integer())

    starttime = Option(doc='''
        **Syntax: starttime=<string>
        **Description:** alternative to time picker for start time to send to DataSet. Use relative (e.g. 1d) or epoch time.''', 
        require=False, validate=validators.Match('time', '\d*(d|h|m|s)|\d{10,19}'))

    endtime = Option(doc='''
        **Syntax: endtime=<string>
        **Description:** alternative to time picker for end time to send to DataSet. Use relative (e.g. 5m) or epoch time.''', 
        require=False, validate=validators.Match('time', '\d*(d|h|m|s)|\d{10,19}'))
    
    function = Option(doc='''
        **Syntax: endtime=<string>
        **Description:** alternative to time picker for end time to send to DataSet. Use relative (e.g. 5m) or epoch time.''', 
        default='rate', require=False, validate=validators.Match('function', '(?i)(rate|count|mean|min|max|sum|sumPerSecond|median|p10|p50|p90|p95|p9{2,3})(\(\w+\))?'))

    buckets = Option(doc='''
        **Syntax: endtime=<string>
        **Description:** alternative to time picker for end time to send to DataSet. Use relative (e.g. 5m) or epoch time.''', 
        default=1, require=False, validate=validators.Integer(minimum=1, maximum=5000))
    
    createsummaries = Option(doc='''
        **Syntax: endtime=<string>
        **Description:** alternative to time picker for end time to send to DataSet. Use relative (e.g. 5m) or epoch time.''', 
        default=True, require=False, validate=validators.Boolean())
    
    onlyusesummaries = Option(doc='''
        **Syntax: endtime=<string>
        **Description:** alternative to time picker for end time to send to DataSet. Use relative (e.g. 5m) or epoch time.''', 
        default=False, require=False, validate=validators.Boolean())


    def generate(self):
        #get datasest environment from conf settings
        conf = self.service.confs['ta_dataset_settings']['dataset_parameters'].content
        #convert single quote key: value to proper json "key": "value"
        conf_j = json.dumps(conf)
        conf_json = json.loads(conf_j)
        ds_environment = conf_json['dataset_environment']

        #set DataSet url and get API key
        ds_url = get_url(ds_environment)
        ds_api_key = get_read_token(self)

        #error if no api key provided in settings
        if not ds_api_key:
            yield { '_raw': 'read api key error, check add-on settings' }
            sys.exit(0)

        ds_headers = { "Authorization": "Bearer " + ds_api_key }

        ##### Parse user-provided options
        #if starttime was given in search, use it
        if self.starttime:
            st_match = re.match("\d+(d|h|m|s)", self.starttime)
            if st_match: 
            #if relative time was given, convert to epoch time which is required for recursive calls to API with consistent time bounds
                start_time = relative_to_epoch(self.starttime)
            else:
                #if epoch time was given, use it
                start_time = self.starttime
        else:
            try:
                #if Splunk time picker was used, convert provided epoch string to integer and use it
                start_time = int(self.search_results_info.search_et)
            except:
                #if "all time" is used no search_et is defined, or if nothing was provided, default to 24h to follow DataSet default
                start_time = relative_to_epoch("24h")

        #follow same startime logic for endtime
        if self.endtime:
            et_match = re.match("\d+(d|h|m|s)", self.endtime)
            if et_match:
                end_time = relative_to_epoch(self.endtime)
            else:
                end_time = self.endtime
        else:
            try:
                end_time = int(self.search_results_info.search_lt)
            except:
                end_time = relative_to_epoch("1s")

        ds_payload = { 
            "startTime": start_time,
            "endTime": end_time
        }

        #set default values for payload
        api_maxcount = 100 #used for queries needing recursing calls
        ds_url_endpoint = "query"

        #set payload for different API endpoints
        if self.method:
            ds_method = self.method.lower()

            if ds_method == 'query':
                ds_url_endpoint = "query"
                ds_payload['queryType'] = "log"
                if self.search:
                    ds_payload['filter'] = self.search
                if self.maxcount:
                    api_maxcount = get_maxcount(self.maxcount)
                    ds_payload['maxCount'] = api_maxcount
                if self.columns:
                    ds_payload['columns'] = self.columns

            elif ds_method == 'powerquery':
                ds_url_endpoint = "powerQuery"
                if self.search:
                    ds_payload['query'] = self.search
                else:
                    #powerquery reequires query, set default if not given
                    ds_payload['query'] = "'*'"
                if self.maxcount:
                    ds_payload['query'] += "| limit " + str(self.maxcount)
                    logging.info('powerQuery uses | limit instead of maxCount, adding this to powerQuery filter')
                if self.columns:
                    ds_payload['query'] += "| columns " + str(self.columns)

            elif ds_method == 'timeseries':
                ds_url_endpoint = "timeseriesQuery"
                if self.search:
                    ds_payload['filter'] = self.search
                if self.function:
                    ds_payload['function'] = self.function
                ds_payload['buckets'] = self.buckets
                ds_payload['createSummaries'] = self.createsummaries
                ds_payload['onlyUseSummaries'] = self.onlyusesummaries
                
        else:
            #handle options if no API endpoint was defined
            if self.maxcount:
                api_maxcount = get_maxcount(self.maxcount)
                ds_payload['maxCount'] = api_maxcount
            if self.columns:
                ds_payload['columns'] = self.columns
            
            ds_payload['queryType'] = "log"   
            
        ds_url += ds_url_endpoint

        try:
            ##### Handle simple query
            if ds_url_endpoint == 'query':
                #set maxcount if user-provided, else set to dataset default of 100 results
                if self.maxcount:
                    ds_max_count = self.maxcount
                else:
                    ds_max_count = 100

                #Determine how many recursive calls to accomodate desired number of results
                ds_iterations = math.ceil(ds_max_count / 5000)
                for count in range(ds_iterations):
                    logging.info("query api {} of {}".format(count+1, ds_iterations))
                    r = requests.post(url=ds_url, headers=ds_headers, json=ds_payload)
                    r_json = r.json()

                    #first, validate success
                    if r.ok:
                        #log any warnings
                        if 'warnings' in r_json :
                            logging.warning(r_json["warnings"])

                        if 'matches' in r_json and 'sessions' in r_json:
                            matches = r_json['matches']
                            sessions = r_json['sessions']
                            
                            for match_list in matches:
                                ds_event_dict = {}
                                ds_event_dict = match_list

                                #if columns were given, simply return matches and skip merging session data
                                #if columns were not given, merge sessions and matches to return all fields
                                if not self.columns:
                                    session_key = match_list['session']

                                    for session_entry, session_dict in sessions.items():
                                        if session_entry == session_key:
                                            for key in session_dict:
                                                ds_event_dict[key] = session_dict[key]

                                #parse as proper json
                                ds_event = json.loads(json.dumps(ds_event_dict))

                                #if timestamp exists, convert epoch nanoseconds to seconds for Splunk
                                if 'timestamp' in ds_event:
                                    splunk_dt = normalize_time(int(ds_event['timestamp']))
                                else:
                                    #Splunk does not parse events well without a timestamp, use current time to fix this
                                    splunk_dt = int(time.time())

                                yield {
                                    '_raw': ds_event,
                                    '_time': splunk_dt,
                                    'source': 'dataset_command',
                                    'sourcetype': 'dataset:query'
                                }

                        else:
                            logging.error('No matches and sessions in response')
                            logging.error(r_json)

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
                            logging.error(r_json['message'])
                        else:
                            logging.error("response = {}".format(r_json))
                        break

            ##### Handle PowerQuery
            if ds_url_endpoint == 'powerQuery':
                r = requests.post(url=ds_url, headers=ds_headers, json=ds_payload)
                r_json = r.json()

                #first, validate success
                if r.ok:                
                    if 'cpuUsage' in r_json:
                        logging.info('cpuUsage: %s ' % r_json['cpuUsage'] )

                    #parse results, match returned columns with corresponding values
                    if 'values' in r_json and 'columns' in r_json:
                        values = r_json['values']

                        for value_list in values:
                            ds_event_dict = {}

                            for counter in range(len(value_list)):
                                ds_event_dict[r_json['columns'][counter]['name']] = value_list[counter]

                            #PowerQuery results are returned by default in chronological order
                            ds_event = json.loads(json.dumps(ds_event_dict))

                            #if timestamp exists, convert epoch nanoseconds to seconds for Splunk
                            if 'timestamp' in ds_event:
                                splunk_dt = normalize_time(int(ds_event['timestamp']))
                            else:                                
                                #Splunk does not parse events well without a timestamp, use current time to fix this
                                splunk_dt = int(time.time())

                            yield {
                                '_raw': ds_event,
                                '_time': splunk_dt,
                                'source': 'dataset_command',
                                'sourcetype': 'dataset:powerQuery'
                            }              
                                                
                    else: #if no resulting ['values'] and ['columns']
                        logging.error('No matches in response')
                        logging.error(r_json)
                else:
                    if 'message' in r_json:
                        logging.error(r_json['message'])
                    else:
                        logging.error("response = {}".format(r_json))
            
            #### Handle timeseriesQuery
            if ds_url_endpoint == 'timeseriesQuery':
                #get function used, split before parenthesees
                splunk_function = re.split("\(", self.function)[0]
                ts_payload = { "queries": [ds_payload] }

                #with varying lengths of time (10 - 19 digits), take first 10 digits
                start_str = str(start_time)[0:10]
                end_str = str(end_time)[0:10]
                splunk_start = int(start_str)
                splunk_end = int(end_str)
                #calculate time differental for start and end, then divide by number of buckets
                bucket_time = (splunk_end - splunk_start) / int(self.buckets)

                r = requests.post(url=ds_url, headers=ds_headers, json=ts_payload)
                r_json = r.json()

                 #first, validate success
                if r.ok:   
                    if 'cpuUsage' in r_json:
                        logging.info('cpuUsage: %s ' % r_json['cpuUsage'] )

                    #parse resulting values
                    if 'results' in r_json:
                        values = r_json['results'][0]['values']

                        for counter in range(len(values)):
                            ds_event = values[counter]
                            #determine timestamp by adding bucket_time to start_time x number of iterations (+1 since indices start at 0)
                            splunk_dt = splunk_start + bucket_time * (counter + 1)

                            #splunk needs a string in _raw to render correctly; = is sufficient so write to _raw and again to splunk_function field
                            yield {
                                '_raw': '{}={}'.format(splunk_function, ds_event),
                                splunk_function: ds_event,
                                '_time': splunk_dt,
                                'source': 'dataset_command',
                                'sourcetype': 'dataset:timeseriesQuery'
                            }
                                                
                    else:
                        logging.error('No matches in response')
                        logging.error(r_json)
                else:
                    if 'message' in r_json:
                        logging.error(r_json['message'])
                    else:
                        logging.error("response = {}".format(r_json))

        except Exception as e:
            logging.error(e)


dispatch(DataSetSearch, sys.argv, sys.stdin, sys.stdout, __name__)