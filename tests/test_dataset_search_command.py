# -*- coding: utf-8 -*-
import pytest
from dataset_search_command import DataSetSearch, search_error_exit


@pytest.mark.parametrize(
    "payload,expected",
    [
        ({"message": "foo - A"}, "foo - A"),
        ({"message": "foo - B", "code": "bar"}, "foo - B (bar)"),
        (
            {"message": "Couldn't decode API token"},
            "API token rejected, check add-on configuration",
        ),
        ("foo - C", "foo - C"),
    ],
)
def test_search_error_exit(mocker, payload, expected):
    s = DataSetSearch()
    m = mocker.patch.object(s, "error_exit", return_value=True, autospec=True)
    search_error_exit(s, payload)
    m.assert_called_with(error="ERROR", message=expected)
