# -*- coding: utf-8 -*-
import time

from dataset_common import normalize_time, relative_to_epoch


def test_normalize_time():
    dataset_time_nanos = int(1692099758000000000)
    splunk_time_seconds = normalize_time(dataset_time_nanos)
    assert splunk_time_seconds == int(1692099758)


def test_relative_to_epoch_produces_timestamp_with_3s_prior_now():
    now = time.time()
    epoch_start = relative_to_epoch("3s")
    now_rounded = int(now)
    assert epoch_start + 3 == now_rounded


def test_relative_to_epoch_produces_timestamp_with_4h_prior_now():
    now = time.time()
    epoch_start = relative_to_epoch("4h")
    now_rounded = int(now)
    assert epoch_start + 4 * 60 * 60 == now_rounded


def test_relative_to_epoch_does_not_support_combination():
    try:
        relative_to_epoch("4h30m")
        raise AssertionError
    except ValueError:
        print("Caught the correct exception")
    except Exception:
        print("Caught the wrong exception")
        raise AssertionError
