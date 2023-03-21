# encoding = utf-8

import os
import sys
import time
import json
import math
import requests
import logging
import re
import copy
from dataset_common import get_url, normalize_time, relative_to_epoch, get_read_token
from dataset_api import *
#From Splunk UCC
import import_declare_test
#Splunk Enterprise SDK
from splunklib.searchcommands import dispatch, GeneratingCommand, Configuration, Option, validators
from splunklib import setup_logging


def get_acct_info(self, account=None):
    logging.debug("DataSetFunction={}, startTime={}".format("get_acct_info", time.time()))
    acct_dict = {}
    if account is not None:
        #wildcard to use all accounts
        if account == "*":
            try:
                confs = self.service.confs['ta_dataset_account']
                for conf in confs:
                    acct_dict[conf.name] = {}
                    acct_dict[conf.name]['base_url'] = conf.url
                    acct_dict[conf.name]['ds_api_key'] = get_read_token(self, conf.name, logging)
            except:
                search_error_exit(self, "Unable to retrieve add-on settings, check configuration")
        else:
            try:
                #remove spaces and split by commas
                account = account.replace(' ', '').split(",")
                for entry in account:
                    conf = self.service.confs['ta_dataset_account'][entry]
                    acct_dict[entry] = {}
                    acct_dict[entry]['base_url'] = conf.url
                    acct_dict[entry]['ds_api_key'] = get_read_token(self, entry, logging)
            except:
                search_error_exit(self, "Account not found in settings")
    #if account is not defined, try to get the first entry (Splunk sorts alphabetically)
    else:
        try:
            confs = self.service.confs['ta_dataset_account']
            for conf in confs:
                acct_dict[conf.name] = {}
                acct_dict[conf.name]['base_url'] = conf.url
                acct_dict[conf.name]['ds_api_key'] = get_read_token(self, conf.name, logging)
                break
        except:
            search_error_exit(self, "Unable to retrieve add-on settings, check configuration")
    end = time.time()
    logging.debug("DataSetFunction={}, endTime={}".format("get_acct_info", time.time()))
    return(acct_dict)


def get_search_times(self):
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
    
    return (start_time, end_time)


def get_search_arguments(self):
        #optional arguments
        ds_account = ds_search = ds_columns = ds_maxcount = f_field = None

        if self.account:
            ds_account = self.account
        if self.search:
            ds_search = self.search
        if self.columns:
            ds_columns = self.columns
        if self.maxcount:
            ds_maxcount = self.maxcount
        else:
            ds_maxcount = get_maxcount(0)
        if self.field:
            f_field = self.field

        #the following have defaults defined and will always have a value
        ds_method = self.method.lower()
        ts_function = self.function
        ts_buckets = self.buckets
        ts_create_summ = self.createsummaries
        ts_use_summ = self.onlyusesummaries
        return (ds_account, ds_method, ds_search, ds_columns, ds_maxcount, f_field, ts_function, ts_buckets, ts_create_summ, ts_use_summ)


def get_proxy_settings(self):
        conf = self.service.confs['ta_dataset_settings']['proxy'].content
        conf_j = json.dumps(conf)
        conf_json = json.loads(conf_j)

        if 'proxy_enabled' in conf_json:
            proxy_enabled = int(conf_json['disabled'])

            if proxy_enabled == 0:
                return None
            else:
                proxies = {}
                if 'proxy_username' in conf_json and 'proxy_password' in conf_json:
                    proxies['http'] = conf_json['proxy_username'] + ":" + conf_json['proxy_password'] + "@" + conf_json['proxy_url'] + ":" + conf_json['proxy_port']
                elif 'proxy_username' in conf_json:
                    proxies['http'] =  conf_json['proxy_username'] + "@" + conf_json['proxy_url'] + ":" + conf_json['proxy_port']
                elif 'proxy_url' in conf_json and 'proxy_port' in conf_json:
                    proxies['http'] =  conf_json['proxy_url'] + ":" + conf_json['proxy_port']

                if 'http' in proxies:
                    #prepend http and https, respectively
                    proxies['http'] = f"{'http://'}{proxies['http']}"
                    proxies['https'] = f"{'https://'}{proxies['http']}"
                    return proxies
                else:
                    return None
        else:
            return None


def search_error_exit(self, r_json):
    if 'message' in r_json:
        logging.error(r_json['message'])
        if r_json['message'].startswith("Couldn\'t decode API token"):
            error_message = "API token rejected, check add-on configuration" #make API error more user-friendly
        else:
            error_message = r_json['message']
    else:
        logging.error(r_json)
        try:
            error_message = str(r_json)
        except:
           error_message = "Request failed, confirm connectivity and check search log"
    self.error_exit(error='ERROR', message = error_message)


@Configuration()
class DataSetSearch(GeneratingCommand):
    account = Option(doc='''
        **Syntax: account=<string>
        **Description:** DataSet account to use''', 
        require=False)

    method = Option(doc='''
        **Syntax: method=(query|powerQuery|facet|timeseries)
        **Description:** DataSet endpoint to use: query, powerquery, facet or timeseries''', 
        default='query', require=False, validate=validators.Match('query', '(?i)query|powerquery|facet|timeseries'))
    
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

    field = Option(doc='''
        **Syntax: field=<string>
        **Description:** For facetQuery, the fielt to get most frequent values of''', 
        require=False)
    
    function = Option(doc='''
        **Syntax: endtime=<string>
        **Description:** For timeseriesQuery, define value to compute from matching events. Default is rate.''', 
        default='rate', require=False, validate=validators.Match('function', '(?i)(rate|count|mean|min|max|sum|sumPerSecond|median|p10|p50|p90|p95|p9{2,3})(\(\w+\))?'))

    buckets = Option(doc='''
        **Syntax: endtime=<string>
        **Description:** For timeseriesQuery, the number of numeric values to return by dividing time range into equal slices. Default is 1.''', 
        default=1, require=False, validate=validators.Integer(minimum=1, maximum=5000))
    
    createsummaries = Option(doc='''
        **Syntax: endtime=<string>
        **Description:** For timeseriesQuery, specify whether to create summaries to automatically update on ingestion pipeline. Default is true, set to false while testing.''', 
        default=True, require=False, validate=validators.Boolean())
    
    onlyusesummaries = Option(doc='''
        **Syntax: endtime=<string>
        **Description:** For timeseriesQuery, specify whether to only use preexisting timeseries for fastest speed.''', 
        default=False, require=False, validate=validators.Boolean())


    def generate(self):
        ds_start, ds_end = get_search_times(self)
        ds_account, ds_method, ds_search, ds_columns, ds_maxcount, f_field, ts_function, ts_buckets, ts_create_summ, ts_use_summ = get_search_arguments(self)
        ds_payload = build_payload(ds_start, ds_end, ds_method, ds_search, ds_columns, ds_maxcount, f_field, ts_function, ts_buckets, ts_create_summ, ts_use_summ)
        acct_dict = get_acct_info(self, ds_account)
        proxy = get_proxy_settings(self)

        for ds_acct in acct_dict.keys():
            ds_url = get_url(acct_dict[ds_acct]['base_url'], ds_method)
            ds_headers = { "Authorization": "Bearer " + acct_dict[ds_acct]['ds_api_key'] }

            try:
                if ds_method == 'query':
                    #Determine how many recursive calls to accomodate desired number of results
                    ds_api_max = query_api_max()
                    ds_iterations = math.ceil(ds_maxcount / ds_api_max)
                    for count in range(ds_iterations):
                        curr_payload = ds_payload.copy()
                        curr_maxcount = copy.copy(ds_maxcount)

                        logging.debug("DataSetFunction=sendRequest, destination={}, startTime={}".format(ds_url, time.time()))
                        r = requests.post(url=ds_url, headers=ds_headers, json=ds_payload, proxies=proxy)
                        logging.debug("DataSetFunction=getResponse, elapsed={}".format(r.elapsed))
                        r_json = r.json()

                        if r.ok:
                            #log any warnings
                            if 'warnings' in r_json :
                                logging.warning(r_json["warnings"])

                            if 'matches' in r_json and 'sessions' in r_json:
                                matches = r_json['matches']
                                sessions = r_json['sessions']

                                if len(matches) == 0 and len(sessions) == 0:
                                    logging.warning("DataSet response success, no matches returned")
                                    logging.warning(r_json)
                                
                                for match_list in matches:
                                    ds_event, splunk_dt = parse_query(ds_columns, match_list, sessions)
                                    yield self.gen_record(_time=splunk_dt, source='dataset:command', sourcetype='_json', account=ds_account, _raw=ds_event)

                            else:
                                logging.warning('DataSet response success, no matches returned')
                                logging.warning(r_json)

                            #after first call, set continuationToken
                            if 'continuationToken' in r_json:
                                curr_payload['continuationToken'] = r_json['continuationToken']
                                #reduce curr_maxcount for each call, then for last call set payload to only return remaining # of desired results
                                curr_maxcount = curr_maxcount - ds_api_max
                                if curr_maxcount > 0 and curr_maxcount < 5000:
                                    curr_payload['maxCount'] = curr_maxcount

                        else:
                            search_error_exit(self, r_json)

                        logging.debug("DataSetFunction=completeEvents, startTime={}".format(time.time()))
                        GeneratingCommand.flush

                else:
                    logging.debug("DataSetFunction=makeRequest, destination={}, startTime={}".format(ds_url, time.time()))
                    r = requests.post(url=ds_url, headers=ds_headers, json=ds_payload, proxies=proxy)
                    logging.debug("DataSetFunction=getResponse, elapsed={}".format(r.elapsed))
                    r_json = r.json()

                    if r.ok:
                        if ds_method == 'powerquery':
                            #parse results, match returned columns with corresponding values
                            if 'values' in r_json and 'columns' in r_json:
                                for value_list in r_json['values']:
                                    ds_event, splunk_dt = parse_powerquery(value_list, r_json['columns'])
                                    yield self.gen_record(_time=splunk_dt, source='dataset_command', sourcetype='dataset:powerQuery', account=ds_account, _raw=ds_event)
                                    
                            else: #if no resulting ['values'] and ['columns']
                                logging.warning('DataSet response success, no matches returned')

                        elif ds_method == 'timeseries':
                            if 'results' in r_json:
                                bucket_time = get_bucket_increments(ds_start, ds_end, ts_buckets)
                                values = r_json['results'][0]['values']
                                for counter in range(len(values)):
                                    ds_event = values[counter]
                                    splunk_function = re.split("\(", self.function)[0]
                                    #determine timestamp by adding bucket_time to start_time x number of iterations (+1 since indices start at 0)
                                    splunk_dt = ds_start + (bucket_time * (counter + 1))
                                    #splunk needs a string in _raw to render correctly; = is sufficient so write to _raw and again to splunk_function field
                                    yield self.gen_record(_time=splunk_dt, source='dataset:command', sourcetype='dataset:timeseriesQuery', account=ds_account, _raw='{}={}'.format(splunk_function, ds_event), splunk_function=ds_event)

                            else:
                                logging.warning('DataSet response success, no matches returned')
                        
                        elif ds_method == 'facet':
                            if 'matchCount' in r_json:
                                logging.info('matchCount: %s ' % r_json['matchCount'] )

                            #parse results
                            if 'values' in r_json:
                                values = r_json['values']
                                for counter in range(len(values)):
                                    ds_event = values[counter]
                                    #Splunk does not parse events well without a timestamp, use current time to fix this
                                    splunk_dt = int(time.time())
                                    yield self.gen_record(_time=splunk_dt, source='dataset_command', sourcetype='dataset:facetQuery', account=ds_account, _raw=ds_event)

                            else: #if no resulting ['values']
                                logging.warning('DataSet response success, no matches returned')

                    else:
                        search_error_exit(self, r_json)
                    
                    logging.debug("DataSetFunction=completeEvents, startTime={}".format(time.time()))
                    GeneratingCommand.flush
            except Exception as e:
                search_error_exit(self, str(e))
      

dispatch(DataSetSearch, sys.argv, sys.stdin, sys.stdout, __name__)