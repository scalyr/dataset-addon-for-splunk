# -*- coding: utf-8 -*-
import json
import logging
import os.path as op
import time
from logging import Logger
from typing import Optional  # noqa: F401

# adjust paths to make the Splunk app working
import import_declare_test  # noqa: F401
from solnlib import conf_manager, log

APP_NAME = __file__.split(op.sep)[-3]
CONF_NAME = "ta_dataset"

LOGGER = None  # type: Optional[Logger]


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


def logger() -> Logger:
    if LOGGER:
        return LOGGER
    return logging.getLogger()


# returns logger that logs data into file
# /opt/splunk/var/log/splunk/${APP_NAME}/${suffix}
# you should call this function as soon as possible, to set up proper logging
def get_logger(session_key, suffix: str) -> Logger:
    logger = log.Logs().get_logger("{}_{}".format(APP_NAME, suffix))
    log_level = get_log_level(session_key, logging)
    logger.setLevel(log_level)

    global LOGGER
    LOGGER = logger
    return logger


# one conf manager to rule them all
def get_conf_manager(session_key, logger):
    realm = "__REST_CREDENTIAL__#{}#configs/conf-{}_settings".format(
        APP_NAME, CONF_NAME
    )
    try:
        logger.debug("Get conf manager - App: {}; Realm: {}".format(APP_NAME, realm))
        cfm = conf_manager.ConfManager(
            session_key,
            APP_NAME,
            realm=realm,
        )

        return cfm

    except Exception as e:
        msg = (
            "Failed to fetch configuration for realm {}. Check permissions. error={}"
            .format(realm, e)
        )
        logger.error(msg + " - %s", e, exc_info=True)
        raise Exception(msg) from e


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

    except Exception as e:
        logger.error(
            "Failed to fetch the log details from the configuration taking INFO as"
            " default level - %s",
            e,
            exc_info=True,
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
            # MM: it does not have key `proxy_enabled, it has key - disabled
            #  {'disabled': '0', 'eai:appName': 'TA_dataset' ...
            proxy_details = cfm.get_conf(CONF_NAME + "_settings").get("proxy")
            proxy_enabled = proxy_details.get("proxy_enabled", 0)
        except Exception as e:
            logger.debug("No proxy information defined: {}".format(e), exc_info=True)
            return None

        if int(proxy_enabled) == 0:
            return None
        else:
            proxy_type = proxy_details.get("proxy_type")
            proxy_host = proxy_details.get("proxy_url")
            proxy_port = proxy_details.get("proxy_port")
            proxy_username = proxy_details.get("proxy_username")
            proxy_password = proxy_details.get("proxy_password")
            proxies = {}
            proxy_url = ""
            if proxy_type:
                proxy_url += proxy_type
            else:
                proxy_url += "http"
            proxy_url += "://"
            if proxy_username:
                proxy_url += proxy_username
            if proxy_password:
                proxy_url += ":" + proxy_password
            if proxy_username:
                proxy_url += "@"
            proxy_url += proxy_host
            proxy_url += ":" + proxy_port

            proxies["http"] = proxy_url
            proxies["https"] = proxies["http"]

            return proxies

    except Exception as e:
        logger.info("Failed to fetch proxy information: {}".format(e), exc_info=True)
        return None


def get_acct_info(self, logger, account=None):
    logger.debug(
        "DataSetFunction={}, startTime={}".format("get_acct_info", time.time())
    )
    acct_dict = {}
    conf_name = "ta_dataset_account"

    if account is not None:
        # wildcard to use all accounts
        if account == "*":
            try:
                confs = self.service.confs[conf_name]
                for conf in confs:
                    acct_dict[conf.name] = {}
                    acct_dict[conf.name]["base_url"] = conf.url
                    acct_dict[conf.name]["ds_api_key"] = get_token_from_config(
                        self, conf, conf.name, logger
                    )
                    acct_dict = update_tenant_conf(
                        conf, conf.name, acct_dict, logger
                    )
            except Exception as e:
                msg = "Error retrieving add-on settings, error = {}".format(e)
                logger.error(msg + " - %s", e, exc_info=True)
                raise Exception(msg) from e
        else:
            try:
                # remove spaces and split by commas
                account = account.replace(" ", "").split(",")
                for entry in account:
                    conf = self.service.confs[conf_name][entry]
                    acct_dict[entry] = {}
                    acct_dict[entry]["base_url"] = conf.url
                    acct_dict[entry]["ds_api_key"] = get_token_from_config(
                        self, conf, entry, logger
                    )
                    acct_dict = update_tenant_conf(conf, entry, acct_dict, logger)
            except Exception as e:
                msg = "Error retrieving account settings, error = {}".format(e)
                logger.error(msg + " - %s", e, exc_info=True)
                raise Exception(msg) from e
    # if account is not defined, try to get the first entry
    # (Splunk sorts alphabetically)
    else:
        try:
            confs = self.service.confs[conf_name]
            for conf in confs:
                acct_dict[conf.name] = {}
                acct_dict[conf.name]["base_url"] = conf.url
                acct_dict[conf.name]["ds_api_key"] = get_token_from_config(
                    self, conf, conf.name, logger
                )
                acct_dict = update_tenant_conf(conf, conf.name, acct_dict, logger)
                break
        except Exception as e:
            msg = (
                "Error retrieving settings. Do you have at least one account in"
                " Configuration?, error = {}".format(e)
            )
            logger.error(msg + " - %s", e, exc_info=True)
            raise Exception(msg) from e
    logger.debug("DataSetFunction={}, endTime={}".format("get_acct_info", time.time()))
    return acct_dict


def update_tenant_conf(conf, conf_name, acct_dict, logger):
    if hasattr(conf, "tenant") and conf.tenant in ["all_scopes", "specified_scopes"]:
        tenant_value = True if conf.tenant == "all_scopes" else False
        acct_dict[conf_name]["tenant"] = tenant_value
        if not tenant_value:
            acct_dict[conf_name]["account_ids"] = get_account_ids(conf, logger)
    return acct_dict


def get_account_ids(conf, logger):
    account_ids_array = []
    if hasattr(conf, "account_ids"):
        account_ids_conf = conf.account_ids
        account_ids_conf = account_ids_conf.strip()
        if account_ids_conf:
            account_ids_array = account_ids_conf.split(",")
        logger.debug(f"the provided account ids in config: {account_ids_array}")
    if not account_ids_array:
        raise Exception(
            "Tenant is false, so please provide the valid comma-separated account IDs"
            " in the account configuration page."
        )
    return account_ids_array


def get_token_from_config(self, conf, name, logger):
    authn_token = ""
    if hasattr(conf, "authn_token_part_one"):
        logger.debug("The AuthN api token first part was available")
        first_half = get_token(self, name, "authn", logger, "authn_token_part_one")
        if not first_half:
            raise Exception(
                "Configuration error: AuthN API Token First Part is not specified"
            )
        authn_token += first_half
    if hasattr(conf, "authn_token_part_two"):
        logger.debug("The AuthN api token second part was available")
        second_part = conf.authn_token_part_two
        if not second_part:
            raise Exception(
                "Configuration error: AuthN API Token Second Part is not specified"
            )
        authn_token += second_part
    if not hasattr(conf, "authn_token_part_one") and not hasattr(
        conf, "authn_token_part_two"
    ):
        logger.debug("The AuthN api token was not available")
        return get_token(self, name, "read", logger)

    return authn_token


def get_tenant_related_payload(ds_acct):
    if ds_acct.get("tenant") is not None:
        tenant_value = ds_acct.get("tenant")
        if tenant_value:
            return {"tenant": True}
        return {
            "tenant": False,
            "accountIds": ds_acct["account_ids"],
        }
    return {}


def get_token(self, account, token_type, logger, config_key=None):
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
                if token_type == "authn":
                    if config_key in cred:
                        cred_json = json.loads(cred)
                        token = cred_json[config_key]
                if token_type == "read":
                    if "dataset_log_read_access_key" in cred:
                        cred_json = json.loads(cred)
                        token = cred_json["dataset_log_read_access_key"]
                elif token_type == "write":
                    if "dataset_log_write_access_key" in cred:
                        cred_json = json.loads(cred)
                        token = cred_json["dataset_log_write_access_key"]
                return token
            else:
                logger.debug("the credentials were not retireived")
    except Exception as e:
        logger.error(
            self,
            "Unable to retrieve API token, check configuration. error={} - %s".format(
                e
            ),
            e,
            exc_info=True,
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
