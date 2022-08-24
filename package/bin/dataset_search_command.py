# encoding = utf-8

import os
import sys
import time
import datetime
import json
import requests
import ast
from dataset_common import get_url, normalize_time
import logging

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
        **Syntax: method=(query|powerQuery|timeseriesQuery)
        **Description:** DataSet endpoint to use: simple query, timeseriesQuery or powerQuery''', 
        require=False, validate=validators.Match('query', '(?i)query|timeseriesQuery|powerQuery'))
    
    search = Option(doc='''
        **Syntax: search=<string>
        **Description:** DataSet search to filter events''', 
        require=False)

    maxcount = Option(doc='''
        **Syntax: maxcount=<integer>
        **Description:** the number of events to return from DataSet. Default is 100.''', 
        require=False, validate=validators.Integer())

    starttime = Option(doc='''
        **Syntax: starttime=<string>
        **Description:** alternative to time picker for start time to send to DataSet. Use relative (e.g. 1d) or epoch time.''', 
        require=False, validate=validators.Match('time', '\d*(d|h|m|s)|\d{10,16}'))

    endtime = Option(doc='''
        **Syntax: endtime=<string>
        **Description:** alternative to time picker for end time to send to DataSet. Use relative (e.g. 5m) or epoch time.''', 
        require=False, validate=validators.Match('time', '\d*(d|h|m|s)|\d{10,16}'))

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

        #use startTime and endTime if provided in search
        if self.starttime:
            start_time = self.starttime
        #or use Splunk time picker
        else:
            try:
                start_time = int(self.search_results_info.search_et)
            except:
                #default to 0 (e.g.: "all time" is used, which doesn't provide a time)
                start_time = '24h'

        #same logic for end
        if self.endtime:
            end_time = self.endtime
        else:
            try:
                end_time = int(self.search_results_info.search_lt)
            except:
                end_time = "1s"

        ds_payload = { 
            "startTime": start_time,
            "endTime": end_time
        }

        #set default values
        ds_url_endpoint = 'query'
        ds_search = "'*'"
        if self.search:
            ds_search = self.search

        ##### Parse user-provided options
        if self.method:
            ds_method = self.method.lower() #added

            if ds_method == 'query':
                ds_url_endpoint = 'query'
                ds_payload["queryType"] = "log"
                ds_payload['filter'] = ds_search
                if self.maxcount:
                    ds_payload['maxCount'] = self.maxcount

            elif ds_method == 'powerquery':
                ds_url_endpoint = 'powerQuery'
                ds_payload['query'] = ds_search
                if self.maxcount:
                    ds_payload['query'] += "| limit " + str(self.maxcount)
                    logging.info('powerQuery uses | limit instead of maxCount, adding this to powerQuery filter')
        else:
            #set maxcount if user provided no other arguments
            if self.maxcount:
                ds_payload['maxCount'] = self.maxcount

        ds_url += ds_url_endpoint
        #make request
        r = requests.post(url=ds_url, headers=ds_headers, json=ds_payload)
        r_json = r.json()

        try:
            #first, validate success
            if r.ok:
                #log any warnings
                if 'warnings' in r_json :
                    logging.warning(r_json["warnings"])

                #handle query payload
                if ds_url_endpoint == 'query':
                    if 'matches' in r_json and 'sessions' in r_json:
                        matches = r_json['matches']
                        sessions = r_json['sessions']
                        
                        for match_list in matches:
                            ds_event_dict = {}
                            ds_event_dict = match_list
                            session_key = match_list['session']

                            for session_entry, session_dict in sessions.items():
                                if session_entry == session_key:
                                    for key in session_dict:
                                        ds_event_dict[key] = session_dict[key]


                            #parse as proper json
                            ds_event = json.loads(json.dumps(ds_event_dict))
                            #convert epoch nanoseconds to seconds for Splunk timestamping
                            splunk_dt = normalize_time(int(ds_event['timestamp']))

                            yield {
                                '_raw': ds_event,
                                '_time': splunk_dt,
                                'source': 'dataset_command',
                                'sourcetype': 'dataset:query'
                            }
                    else: #if no resulting ['matches'] and ['sessions']:
                        yield { '_raw': 'No matching results' }

                if ds_url_endpoint == 'powerQuery':
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

                            #if timestamp exists, use it
                            if 'timestamp' in ds_event:
                                #convert epoch nanoseconds to seconds for Splunk
                                splunk_dt = normalize_time(int(ds_event['timestamp']))
                                yield {
                                    '_raw': ds_event,
                                    '_time': splunk_dt,
                                    'source': 'dataset_command',
                                    'sourcetype': 'dataset:powerQuery'
                                }
                            #otherwise, if no 'timestamp' field just return payload
                            else:
                                yield {
                                    '_raw': ds_event,
                                    'source': 'dataset_command',
                                    'sourcetype': 'dataset:powerQuery'
                                }                  
                                             
                    else: #if no resulting ['values']
                        yield { '_raw': 'No matching results' }

            else:
                if 'message' in r_json:
                    yield { '_raw': 'response: %s' % r_json['message']}

        except:
            #yield { '_raw': 'error returned: %s' % r_json }
            logging.error(r_json)

dispatch(DataSetSearch, sys.argv, sys.stdin, sys.stdout, __name__)