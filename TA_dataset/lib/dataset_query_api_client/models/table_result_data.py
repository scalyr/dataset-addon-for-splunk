from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.column import Column
    from ..models.table_result_data_values_item_item import (
        TableResultDataValuesItemItem,
    )


T = TypeVar("T", bound="TableResultData")


@attr.s(auto_attribs=True)
class TableResultData:
    """Results of a `PQ` query with result type `TABLE`.

    Attributes:
        match_count (Union[Unset, float]): Count of events matched in this query. May be exact, but for many queries it
            will be approximate.
        values (Union[Unset, List[List['TableResultDataValuesItemItem']]]): List of values in a row column format where
            values[0][0], returns the value from first column in the first row.
        columns (Union[Unset, List['Column']]): List of column definitions for the returned table.
        key_columns (Union[Unset, int]): The number of columns which are grouping keys.
        omitted_events (Union[Unset, float]): If we exceeded our memory or cardinality limits for a `PQ` query, this
            will hold the number of events which (as a result) are not reflected in the output. Otherwise 0. Always in the
            range [0, matchCount].
        partial_results_due_to_time_limit (Union[Unset, bool]): Whether the query returned partial results due to
            reaching time limit.
        warnings (Union[Unset, List[str]]): A list of messages which can be shown to the user regarding this query.
    """

    match_count: Union[Unset, float] = UNSET
    values: Union[Unset, List[List[Any]]] = UNSET
    columns: Union[Unset, List["Column"]] = UNSET
    key_columns: Union[Unset, int] = UNSET
    omitted_events: Union[Unset, float] = UNSET
    partial_results_due_to_time_limit: Union[Unset, bool] = UNSET
    warnings: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        match_count = self.match_count
        values: Union[Unset, List[List[Dict[str, Any]]]] = UNSET
        if not isinstance(self.values, Unset):
            values = []
            for values_item_data in self.values:
                values_item = []
                for values_item_item_data in values_item_data:
                    values_item_item = values_item_item_data.to_dict()

                    values_item.append(values_item_item)

                values.append(values_item)

        columns: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.columns, Unset):
            columns = []
            for columns_item_data in self.columns:
                columns_item = columns_item_data.to_dict()

                columns.append(columns_item)

        key_columns = self.key_columns
        omitted_events = self.omitted_events
        partial_results_due_to_time_limit = self.partial_results_due_to_time_limit
        warnings: Union[Unset, List[str]] = UNSET
        if not isinstance(self.warnings, Unset):
            warnings = self.warnings

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if match_count is not UNSET:
            field_dict["matchCount"] = match_count
        if values is not UNSET:
            field_dict["values"] = values
        if columns is not UNSET:
            field_dict["columns"] = columns
        if key_columns is not UNSET:
            field_dict["keyColumns"] = key_columns
        if omitted_events is not UNSET:
            field_dict["omittedEvents"] = omitted_events
        if partial_results_due_to_time_limit is not UNSET:
            field_dict[
                "partialResultsDueToTimeLimit"
            ] = partial_results_due_to_time_limit
        if warnings is not UNSET:
            field_dict["warnings"] = warnings

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.column import Column
        from ..models.table_result_data_values_item_item import (
            TableResultDataValuesItemItem,
        )

        d = src_dict.copy()
        match_count = d.pop("matchCount", UNSET)

        values = []
        values = d.pop("values", UNSET)
        # for values_item_data in _values or []:
        #     values_item = []
        #     _values_item = values_item_data
        #     for values_item_item_data in _values_item:
        #         values_item_item = TableResultDataValuesItemItem.from_dict(values_item_item_data)

        #         values_item.append(values_item_item)

        #     values.append(values_item)

        columns = []
        _columns = d.pop("columns", UNSET)
        for columns_item_data in _columns or []:
            columns_item = Column.from_dict(columns_item_data)

            columns.append(columns_item)

        key_columns = d.pop("keyColumns", UNSET)

        omitted_events = d.pop("omittedEvents", UNSET)

        partial_results_due_to_time_limit = d.pop("partialResultsDueToTimeLimit", UNSET)

        warnings = cast(List[str], d.pop("warnings", UNSET))

        table_result_data = cls(
            match_count=match_count,
            values=values,
            columns=columns,
            key_columns=key_columns,
            omitted_events=omitted_events,
            partial_results_due_to_time_limit=partial_results_due_to_time_limit,
            warnings=warnings,
        )

        table_result_data.additional_properties = d
        return table_result_data

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
