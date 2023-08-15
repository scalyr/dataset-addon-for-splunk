# -*- coding: utf-8 -*-

from dataset_api import ds_build_pq


def test_ds_build_pq():
    query_filter = "source=ABC"
    columns = "source, host"
    limit = 30
    expected_power_query = "{} | columns {} | limit {}".format(
        query_filter, columns, limit
    )
    power_query = ds_build_pq(query_filter, columns, str(limit))
    assert power_query == expected_power_query


def test_ds_build_pq_no_filter_is_replaced_by_asterisk():
    columns = "source, host"
    limit = 30
    expected_power_query = "* | columns {} | limit {}".format(columns, limit)
    power_query = ds_build_pq(None, columns, str(limit))
    assert power_query == expected_power_query


def test_ds_build_pq_empty_columns_are_omitted():
    query_filter = "source=ABC"
    limit = 30
    expected_power_query = "{} | limit {}".format(query_filter, limit)
    power_query = ds_build_pq(query_filter, None, str(limit))
    assert power_query == expected_power_query


def test_ds_build_pq_empty_columns_are_omitted():
    query_filter = "source=ABC"
    columns = "source, host"
    expected_power_query = "{} | columns {}".format(query_filter, columns)
    power_query = ds_build_pq(query_filter, columns, None)
    assert power_query == expected_power_query
