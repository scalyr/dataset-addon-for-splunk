from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.post_queries_launch_query_request_body_query_type import (
    PostQueriesLaunchQueryRequestBodyQueryType,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.facet_values_result_data import FacetValuesResultData
    from ..models.histogram_result_data import HistogramResultData
    from ..models.log_result_data import LogResultData
    from ..models.plot_result_data import PlotResultData
    from ..models.query_result_error import QueryResultError
    from ..models.table_result_data import TableResultData
    from ..models.time_range_result_data import TimeRangeResultData
    from ..models.top_facets_result_data import TopFacetsResultData


T = TypeVar("T", bound="QueryResult")


@attr.s(auto_attribs=True)
class QueryResult:
    """Provides information about current query status and results.

    Attributes:
        id (Union[Unset, str]): The unique query identifier. Can be used in Ping requests to fetch latest query status
            and results. Example:
            eyJ0eXBlIjoiTE9HIiwidG9rZW4iOiJxYXRlc3RpbmctbG9nLTF6XzE3OjM5OjMxLjIyMV8yMzgzY19mZjAzMjEwYyJ9.
        steps_completed (Union[Unset, int]): Number of steps completed in this long running query.
        steps_total (Union[Unset, int]): Total number of steps to execute.
        resolved_time_range (Union[Unset, TimeRangeResultData]): Start time and end time for the query in nanoseconds.
        error (Union[Unset, QueryResultError]): Error if the query was not executed. If not null, will always have
            `message` key which will provide the basic error message and an optional `details` field providing further
            information. If the query execution was successful, the error field will be null.
        data (Union['FacetValuesResultData', 'HistogramResultData', 'LogResultData', 'PlotResultData',
            'TableResultData', 'TopFacetsResultData', Unset]): Data object containing results of the query.

            Note that `PQ` queries may return either `PlotResultData` or `TableResultData` depending on the `resultType`
            specified in the request.
    """

    id: Union[Unset, str] = UNSET
    steps_completed: Union[Unset, int] = UNSET
    steps_total: Union[Unset, int] = UNSET
    resolved_time_range: Union[Unset, "TimeRangeResultData"] = UNSET
    error: Union[Unset, "QueryResultError"] = UNSET
    data: Union[
        "FacetValuesResultData",
        "HistogramResultData",
        "LogResultData",
        "PlotResultData",
        "TableResultData",
        "TopFacetsResultData",
        Unset,
    ] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.facet_values_result_data import FacetValuesResultData
        from ..models.log_result_data import LogResultData
        from ..models.plot_result_data import PlotResultData
        from ..models.table_result_data import TableResultData
        from ..models.top_facets_result_data import TopFacetsResultData

        id = self.id
        steps_completed = self.steps_completed
        steps_total = self.steps_total
        resolved_time_range: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.resolved_time_range, Unset):
            resolved_time_range = self.resolved_time_range.to_dict()

        error: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        data: Union[Dict[str, Any], Unset]
        if isinstance(self.data, Unset):
            data = UNSET

        elif isinstance(self.data, LogResultData):
            data = UNSET
            if not isinstance(self.data, Unset):
                data = self.data.to_dict()

        elif isinstance(self.data, TopFacetsResultData):
            data = UNSET
            if not isinstance(self.data, Unset):
                data = self.data.to_dict()

        elif isinstance(self.data, FacetValuesResultData):
            data = UNSET
            if not isinstance(self.data, Unset):
                data = self.data.to_dict()

        elif isinstance(self.data, PlotResultData):
            data = UNSET
            if not isinstance(self.data, Unset):
                data = self.data.to_dict()

        elif isinstance(self.data, TableResultData):
            data = UNSET
            if not isinstance(self.data, Unset):
                data = self.data.to_dict()

        else:
            data = UNSET
            if not isinstance(self.data, Unset):
                data = self.data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if steps_completed is not UNSET:
            field_dict["stepsCompleted"] = steps_completed
        if steps_total is not UNSET:
            field_dict["stepsTotal"] = steps_total
        if resolved_time_range is not UNSET:
            field_dict["resolvedTimeRange"] = resolved_time_range
        if error is not UNSET:
            field_dict["error"] = error
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(
        cls: Type[T],
        src_dict: Dict[str, Any],
        query_type: PostQueriesLaunchQueryRequestBodyQueryType,
    ) -> T:
        from ..models.facet_values_result_data import FacetValuesResultData
        from ..models.histogram_result_data import HistogramResultData
        from ..models.log_result_data import LogResultData
        from ..models.plot_result_data import PlotResultData
        from ..models.query_result_error import QueryResultError
        from ..models.table_result_data import TableResultData
        from ..models.time_range_result_data import TimeRangeResultData
        from ..models.top_facets_result_data import TopFacetsResultData

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        steps_completed = d.pop("stepsCompleted", UNSET)

        steps_total = d.pop("totalSteps", UNSET)  # FIX: inconsitency with schema

        _resolved_time_range = d.pop("resolvedTimeRange", UNSET)
        resolved_time_range: Union[Unset, TimeRangeResultData]
        if isinstance(_resolved_time_range, Unset):
            resolved_time_range = UNSET
        else:
            resolved_time_range = TimeRangeResultData.from_dict(_resolved_time_range)

        _error = d.pop("error", UNSET)
        error: Union[Unset, QueryResultError]
        if isinstance(_error, Unset):
            error = UNSET
        else:
            error = QueryResultError.from_dict(_error)

        def _parse_data(
            data: object,
        ) -> Union[
            "FacetValuesResultData",
            "HistogramResultData",
            "LogResultData",
            "PlotResultData",
            "TableResultData",
            "TopFacetsResultData",
            Unset,
        ]:
            if isinstance(data, Unset):
                return data
            if (
                data is None
            ):  # FIX: the API always returns data field in JSON even if it's null
                return data
            if query_type == PostQueriesLaunchQueryRequestBodyQueryType.LOG:
                return LogResultData.from_dict(data)
            if query_type == PostQueriesLaunchQueryRequestBodyQueryType.PQ:
                _table_data = data
                resolved_table_data: Union[Unset, TableResultData]
                if isinstance(_table_data, Unset):
                    resolved_table_data = UNSET
                else:
                    resolved_table_data = TableResultData.from_dict(_table_data)
                return resolved_table_data
            if query_type == PostQueriesLaunchQueryRequestBodyQueryType.FACET_VALUES:
                _facet_data = data
                resolved_facet_data: Union[Unset, FacetValuesResultData]
                if isinstance(_facet_data, Unset):
                    resolved_facet_data = UNSET
                else:
                    resolved_facet_data = FacetValuesResultData.from_dict(_facet_data)
                return resolved_facet_data
            # TODO: must complete implementation of the remaining query types
            raise TypeError()

        data = _parse_data(d.pop("data", UNSET))

        query_result = cls(
            id=id,
            steps_completed=steps_completed,
            steps_total=steps_total,
            resolved_time_range=resolved_time_range,
            error=error,
            data=data,
        )

        query_result.additional_properties = d
        return query_result

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
