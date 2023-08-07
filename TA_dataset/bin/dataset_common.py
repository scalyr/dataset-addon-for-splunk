# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
import os.path as op
import sys
import time

from solnlib import conf_manager

APP_NAME = __file__.split(op.sep)[-3]
CONF_NAME = "ta_dataset"


# define DataSet API URL for all environments
def get_url(base_url, ds_method):
    if ds_method == "query":
        ds_api_endpoint = "query"
    elif ds_method == "powerquery":
        ds_api_endpoint = "powerQuery"
    elif ds_method == "facet":
        ds_api_endpoint = "facetQuery"
    elif ds_method == "timeseries":
        ds_api_endpoint = "timeseriesQuery"
    elif ds_method == "addevents":
        ds_api_endpoint = "addEvents"

    return base_url + "/api/" + ds_api_endpoint


# one conf manager to rule them all
def get_conf_manager(session_key, logger):
    try:
        cfm = conf_manager.ConfManager(
            session_key,
            APP_NAME,
            realm="__REST_CREDENTIAL__#{}#configs/conf-{}_settings".format(
                APP_NAME, CONF_NAME
            ),
        )

        return cfm

    except Exception as e:
        logger.error(
            "Failed to fetch configuration. Check permissions. error={}".format(e)
        )
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
            logging_details.get("loglevel")
            if (logging_details.get("loglevel"))
            else "INFO"
        )
        return log_level

    except Exception:
        logger.error(
            "Failed to fetch the log details from the configuration taking INFO as default level."
        )
        return "INFO"


def get_proxy(session_key, logger):
    """
    This function returns the proxy settings for the addon from configuration file.
    :param session_key: session key for particular modular input.
    :return : proxy dictionary.
    """
    try:
        cfm = get_conf_manager(session_key, logger)
        try:
            proxy_details = cfm.get_conf(CONF_NAME + "_settings").get("proxy")
            proxy_enabled = proxy_details.get("proxy_enabled")
        except Exception:
            logger.debug("No proxy information defined.")
            return None

        if int(proxy_enabled) == 0:
            return None
        else:
            proxy_url = proxy_details.get("proxy_url")
            proxy_port = proxy_details.get("proxy_port")
            proxy_username = proxy_details.get("proxy_username")
            proxy_password = proxy_details.get("proxy_password")
            proxy_type = proxy_details.get("proxy_type")
            proxies = {}
            if proxy_username and proxy_password:
                proxies["http"] = (
                    proxy_username
                    + ":"
                    + proxy_password
                    + "@"
                    + proxy_url
                    + ":"
                    + proxy_port
                )
            elif proxy_username:
                proxies["http"] = proxy_username + "@" + proxy_url + ":" + proxy_port
            else:
                proxies["http"] = proxy_url + ":" + proxy_port
            if proxy_type and proxy_type != "http":
                proxies["http"] = proxy_type + "://" + proxies["http"]

            proxies["https"] = proxies["http"]
            return proxies

    except Exception:
        logger.info("Failed to fetch proxy information.")
        return None


def get_acct_info(self, logger, account=None):
    logger.debug(
        "DataSetFunction={}, startTime={}".format("get_acct_info", time.time())
    )
    acct_dict = {}
    if account is not None:
        # wildcard to use all accounts
        if account == "*":
            try:
                confs = self.service.confs["ta_dataset_account"]
                for conf in confs:
                    acct_dict[conf.name] = {}
                    acct_dict[conf.name]["base_url"] = conf.url
                    acct_dict[conf.name]["ds_api_key"] = get_token(
                        self, conf.name, "read", logger
                    )
            except Exception as e:
                logger.error("Error retrieving add-on settings, error = {}".format(e))
                return None
        else:
            try:
                # remove spaces and split by commas
                account = account.replace(" ", "").split(",")
                for entry in account:
                    conf = self.service.confs["ta_dataset_account"][entry]
                    acct_dict[entry] = {}
                    acct_dict[entry]["base_url"] = conf.url
                    acct_dict[entry]["ds_api_key"] = get_token(
                        self, entry, "read", logger
                    )
            except Exception as e:
                logger.error("Error retrieving account settings, error = {}".format(e))
                return None
    # if account is not defined, try to get the first entry (Splunk sorts alphabetically)
    else:
        try:
            confs = self.service.confs["ta_dataset_account"]
            for conf in confs:
                acct_dict[conf.name] = {}
                acct_dict[conf.name]["base_url"] = conf.url
                acct_dict[conf.name]["ds_api_key"] = get_token(
                    self, conf.name, "read", logger
                )
                break
        except Exception as e:
            logger.error("Error retrieving settings, error = {}".format(e))
    logger.debug("DataSetFunction={}, endTime={}".format("get_acct_info", time.time()))
    return acct_dict


def get_token(self, account, rw, logger):
    try:
        # use Python SDK secrets retrieval
        for credential in self.service.storage_passwords:
            if (
                credential.realm
                == "__REST_CREDENTIAL__#{}#configs/conf-{}_account".format(
                    APP_NAME, CONF_NAME
                )
                and credential.username.startswith(account)
            ):
                cred = credential.content.get("clear_password")
                if rw == "read":
                    if "dataset_log_read_access_key" in cred:
                        cred_json = json.loads(cred)
                        token = cred_json["dataset_log_read_access_key"]
                elif rw == "write":
                    if "dataset_log_write_access_key" in cred:
                        cred_json = json.loads(cred)
                        token = cred_json["dataset_log_write_access_key"]
                return token
    except Exception as e:
        logger.error(
            self,
            "Unable to retrieve API token, check configuration. error={}".format(e),
        )


def normalize_time(ds_time):
    """
    This function converts nanoseconds (used by DataSet API) to seconds (used by Splunk)
    :param ds_time: timestamps nanoseconds
    :return : timestamp in seconds
    """
    splunk_dt = ds_time / 1000000000
    return splunk_dt


def relative_to_epoch(relative):
    """
    This function returns epoch time from a relative time
    :param relative: shorthand relative time stamp (e.g. "24h" for 24 hours ago)
    :return : time_relative in epoch as an integer
    """
    relative_num = int(relative[0:-1])
    relative_unit = relative[-1:]
    # get current epoch time in milliseconds
    time_current = int(time.time())
    num_seconds = 1
    if relative_unit == "m":
        num_seconds = num_seconds * 60
    elif relative_unit == "h":
        num_seconds = num_seconds * 60 * 60
    elif relative_unit == "d":
        num_seconds = num_seconds * 60 * 60 * 24

    time_relative = time_current - (relative_num * num_seconds)
    return time_relative
