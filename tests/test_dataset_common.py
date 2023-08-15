# -*- coding: utf-8 -*-
from dataset_common import normalize_time


def test_normalize_time():
    dataset_time_nanos = int(1692099758000000000)
    splunk_time_seconds = normalize_time(dataset_time_nanos)
    assert splunk_time_seconds == int(1692099758)


def test_should_fail():
    assert 3 == 5
