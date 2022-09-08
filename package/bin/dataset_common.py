import os
import os.path as op
import sys
import json
from collections import OrderedDict

import import_declare_test
from solnlib import conf_manager, log
from solnlib.modular_input import checkpointer

APP_NAME = __file__.split(op.sep)[-3]
CONF_NAME = "ta_dataset"


#define DataSet API URL for all environments
def get_url(dataset_environment):
    if dataset_environment == 'eu':
        return 'https://app.eu.scalyr.com/api/'
    else:
        return 'https://app.scalyr.com/api/'


#one conf manager to rule them all
def get_conf_manager(session_key, logger):
    try:
        cfm = conf_manager.ConfManager(
                session_key,
                APP_NAME,
                realm="__REST_CREDENTIAL__#{}#configs/conf-{}_settings".format(APP_NAME, CONF_NAME)
            )

        return cfm
    
    except Exception:
        logger.error("Failed to fetch configuration. Check permissions.")
        sys.exit(1)


def get_log_level(session_key, logger):
    """
    This function returns the log level for the addon from configuration file.
    :param session_key: session key for particular modular input.
    :return : log level configured in addon.
    """
    try:
        cfm = get_conf_manager(session_key, logger)
        logging_details = cfm.get_conf(CONF_NAME + "_settings").get("logging")
        log_level = (
            logging_details.get('loglevel')
            if (logging_details.get('loglevel'))
            else 'INFO'
        )
        return log_level

    except Exception:
        logger.error("Failed to fetch the log details from the configuration taking INFO as default level.")
        return 'INFO'


def get_environment(session_key, logger):
    """
    This function returns the environmentfrom configuration file.
    :param session_key: session key for particular modular input.
    :return : environment as string, e.g. 'us'
    """
    try:
        cfm = get_conf_manager(session_key, logger)
        environment_details = cfm.get_conf(CONF_NAME + "_settings").get("dataset_parameters")
        environment = environment_details.get('dataset_environment')
        return environment

    except Exception:
        logger.error("Failed to fetch environment. Check configuration.")
        sys.exit(1)


def get_token(session_key, logger, rw):
    """
    This function retrieves API key details from addon configuration file.
    :param rw: 'read' or 'write'.
    :return : API key as a string.    
    """
    try:
        cfm = get_conf_manager(session_key, logger)
        token_details = cfm.get_conf(CONF_NAME + "_settings").get("dataset_parameters")
        token = token_details.get('dataset_log_' + rw + '_access_key')
        return token

    except Exception as e:
        logger.error("Failed to fetch API key. Check configuration.")
        sys.exit(1)

def get_proxy(session_key, logger):
    try:
        cfm = get_conf_manager(session_key, logger)
        try:
            proxy_details = cfm.get_conf(CONF_NAME + "_settings").get("proxy")
            proxy_enabled = proxy_details.get('proxy_enabled')
        except Exception:
            logger.debug("No proxy information defined.")
            return None

        if int(proxy_enabled) == 0:
            return None
        else:
            proxy_url = proxy_details.get('proxy_url')
            proxy_port = proxy_details.get('proxy_port')
            proxy_username = proxy_details.get('proxy_username')
            proxy_password = proxy_details.get('proxy_password')
            proxy_type = proxy_details.get('proxy_type')
            proxies = {}
            if proxy_username and proxy_password:
                proxies['http'] = proxy_username + ":" + proxy_password + "@" + proxy_url + ":" + proxy_port
            elif proxy_username:
                proxies['http'] = proxy_username + "@" + proxy_url + ":" + proxy_port
            else:
                proxies['http'] = proxy_url + ":" + proxy_port
            if proxy_type and proxy_type != 'http':
                proxies['http'] = proxy_type + "://" + proxies['http']
            
            proxies['https'] = proxies['http']
            return proxies

    except Exception:
        logger.info("Failed to fetch proxy information.")
        return(None)


def normalize_time(ds_time):
    splunk_dt = ds_time / 1000000000
    return splunk_dt


def relative_to_epoch(relative):
    """
    This function uses return epoch time from a relative time
    :param relative: shorthand relative time stamp (e.g. "24h" for 24 hours ago)
    :return : time_relative in epoch as an integer
    """
    relative_num = int(relative[0:-1])
    relative_unit = relative[-1:]
    #get current epoch time in milliseconds
    time_current = int(time.time())
    num_seconds = 1
    if relative_unit == 'm':
        num_seconds = num_seconds * 60
    elif relative_unit == 'h':
        num_seconds = num_seconds * 60 * 60
    elif relative_unit == 'd':
        num_seconds = num_seconds * 60 * 60 * 24

    time_relative = time_current - (relative_num * num_seconds)
    return time_relative


def get_maxcount(max):
    #query API returns max 5,000 results per call
    if max > 5000:
        return 5000
    else:
        return max