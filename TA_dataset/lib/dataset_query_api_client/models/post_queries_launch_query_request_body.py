from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.post_queries_launch_query_request_body_query_priority import (
    PostQueriesLaunchQueryRequestBodyQueryPriority,
)
from ..models.post_queries_launch_query_request_body_query_type import PostQueriesLaunchQueryRequestBodyQueryType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.distribution_attributes import DistributionAttributes
    from ..models.facet_values_attributes import FacetValuesAttributes
    from ..models.log_attributes import LogAttributes
    from ..models.plot_attributes import PlotAttributes
    from ..models.pq_attributes import PQAttributes
    from ..models.top_facets_attributes import TopFacetsAttributes


T = TypeVar("T", bound="PostQueriesLaunchQueryRequestBody")


@attr.s(auto_attribs=True)
class PostQueriesLaunchQueryRequestBody:
    """
    Attributes:
        query_type (PostQueriesLaunchQueryRequestBodyQueryType): Specifies the type of query to launch.

            * `LOG`: Fetch a time-ordered list of matching events, with support for pagination.
            * `TOP_FACETS`: Find the top facets & facet values for all matching events.
            * `FACET_VALUES`: Find the top values for a particular facet across all matching events.
            * `PLOT`: Generate a plot of a numeric function applied to all matching events. The plot can be broken down by
            values of a certain facet, if needed.
            * `PQ`: Fetch data matching Dataset's Power Query language. Results can be returned as a table or a plot.
            * `DISTRIBUTION`: Map, as a histogram, the distribution of values for a facet.
        start_time (Union[Unset, str]): Specifies start of the time range to query, using the same syntax as the Start
            and End fields in the query UI.

            You can also supply a simple timestamp, measured in seconds, milliseconds, or nanoseconds since 1/1/1970.

            The default is to query the last 24 hours. If you specify startTime but not endTime, the query covers 24 hours
            beginning at the startTime. If you specify endTime but not startTime, the query covers 24 hours ending at the
            endTime.
        end_time (Union[Unset, str]): Specifies end of the time range to query, using the same syntax as the Start and
            End fields in the query UI.

            You can also supply a simple timestamp, measured in seconds, milliseconds, or nanoseconds since 1/1/1970.

            The default is to query the last 24 hours. If you specify startTime but not endTime, the query covers 24 hours
            beginning at the startTime. If you specify endTime but not startTime, the query covers 24 hours ending at the
            endTime.
        account_emails (Union[Unset, List[str]]): List of account emails to query.  Cannot be used together with
            `accountIds`.
        account_ids (Union[Unset, List[str]]): List of account ids to query. Cannot be used together with
            `accountEmails`.
        query_priority (Union[Unset, PostQueriesLaunchQueryRequestBodyQueryPriority]): Specifies the execution priority
            for this query; defaults to "LOW". Use "LOW" for background operations where a delay of a second or so is
            acceptable.
            LOW-priority queries have more generous rate limits.
            * `HIGH`: Standard query priority for API requests, with tighter rate limits.
            * `LOW`: Use low priority for scripted queries where a slight delay is acceptable; low priority queries are
            subject to less rate limiting. Default: PostQueriesLaunchQueryRequestBodyQueryPriority.LOW.
        log (Union[Unset, LogAttributes]): Attributes specific to the `LOG` query type.
        top_facets (Union[Unset, TopFacetsAttributes]): Attributes specific to the `TOP_FACETS` query type.
        facet_values (Union[Unset, FacetValuesAttributes]): Attributes specific to the `FACET_VALUES` query type.
        plot (Union[Unset, PlotAttributes]): Attributes specific to the `PLOT` query type.
        pq (Union[Unset, PQAttributes]): Attributes specific to the `PQ` query type.
        distribution (Union[Unset, DistributionAttributes]): Attributes specific to the `DISTRIBUTION` query type.
    """

    query_type: PostQueriesLaunchQueryRequestBodyQueryType
    start_time: Union[Unset, str] = UNSET
    end_time: Union[Unset, str] = UNSET
    account_emails: Union[Unset, List[str]] = UNSET
    account_ids: Union[Unset, List[str]] = UNSET
    query_priority: Union[
        Unset, PostQueriesLaunchQueryRequestBodyQueryPriority
    ] = PostQueriesLaunchQueryRequestBodyQueryPriority.LOW
    log: Union[Unset, "LogAttributes"] = UNSET
    top_facets: Union[Unset, "TopFacetsAttributes"] = UNSET
    facet_values: Union[Unset, "FacetValuesAttributes"] = UNSET
    plot: Union[Unset, "PlotAttributes"] = UNSET
    pq: Union[Unset, "PQAttributes"] = UNSET
    distribution: Union[Unset, "DistributionAttributes"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        query_type = self.query_type.value

        start_time = self.start_time
        end_time = self.end_time
        account_emails: Union[Unset, List[str]] = UNSET
        if not isinstance(self.account_emails, Unset):
            account_emails = self.account_emails

        account_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.account_ids, Unset):
            account_ids = self.account_ids

        query_priority: Union[Unset, str] = UNSET
        if not isinstance(self.query_priority, Unset):
            query_priority = self.query_priority.value

        log: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.log, Unset):
            log = self.log.to_dict()

        top_facets: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.top_facets, Unset):
            top_facets = self.top_facets.to_dict()

        facet_values: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.facet_values, Unset):
            facet_values = self.facet_values.to_dict()

        plot: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.plot, Unset):
            plot = self.plot.to_dict()

        pq: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pq, Unset):
            pq = self.pq.to_dict()

        distribution: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.distribution, Unset):
            distribution = self.distribution.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "queryType": query_type,
            }
        )
        if start_time is not UNSET:
            field_dict["startTime"] = start_time
        if end_time is not UNSET:
            field_dict["endTime"] = end_time
        if account_emails is not UNSET:
            field_dict["accountEmails"] = account_emails
        if account_ids is not UNSET:
            field_dict["accountIds"] = account_ids
        if query_priority is not UNSET:
            field_dict["queryPriority"] = query_priority
        if log is not UNSET:
            field_dict["log"] = log
        if top_facets is not UNSET:
            field_dict["topFacets"] = top_facets
        if facet_values is not UNSET:
            field_dict["facetValues"] = facet_values
        if plot is not UNSET:
            field_dict["plot"] = plot
        if pq is not UNSET:
            field_dict["pq"] = pq
        if distribution is not UNSET:
            field_dict["distribution"] = distribution

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.distribution_attributes import DistributionAttributes
        from ..models.facet_values_attributes import FacetValuesAttributes
        from ..models.log_attributes import LogAttributes
        from ..models.plot_attributes import PlotAttributes
        from ..models.pq_attributes import PQAttributes
        from ..models.top_facets_attributes import TopFacetsAttributes

        d = src_dict.copy()
        query_type = PostQueriesLaunchQueryRequestBodyQueryType(d.pop("queryType"))

        start_time = d.pop("startTime", UNSET)

        end_time = d.pop("endTime", UNSET)

        account_emails = cast(List[str], d.pop("accountEmails", UNSET))

        account_ids = cast(List[str], d.pop("accountIds", UNSET))

        _query_priority = d.pop("queryPriority", UNSET)
        query_priority: Union[Unset, PostQueriesLaunchQueryRequestBodyQueryPriority]
        if isinstance(_query_priority, Unset):
            query_priority = UNSET
        else:
            query_priority = PostQueriesLaunchQueryRequestBodyQueryPriority(_query_priority)

        _log = d.pop("log", UNSET)
        log: Union[Unset, LogAttributes]
        if isinstance(_log, Unset):
            log = UNSET
        else:
            log = LogAttributes.from_dict(_log)

        _top_facets = d.pop("topFacets", UNSET)
        top_facets: Union[Unset, TopFacetsAttributes]
        if isinstance(_top_facets, Unset):
            top_facets = UNSET
        else:
            top_facets = TopFacetsAttributes.from_dict(_top_facets)

        _facet_values = d.pop("facetValues", UNSET)
        facet_values: Union[Unset, FacetValuesAttributes]
        if isinstance(_facet_values, Unset):
            facet_values = UNSET
        else:
            facet_values = FacetValuesAttributes.from_dict(_facet_values)

        _plot = d.pop("plot", UNSET)
        plot: Union[Unset, PlotAttributes]
        if isinstance(_plot, Unset):
            plot = UNSET
        else:
            plot = PlotAttributes.from_dict(_plot)

        _pq = d.pop("pq", UNSET)
        pq: Union[Unset, PQAttributes]
        if isinstance(_pq, Unset):
            pq = UNSET
        else:
            pq = PQAttributes.from_dict(_pq)

        _distribution = d.pop("distribution", UNSET)
        distribution: Union[Unset, DistributionAttributes]
        if isinstance(_distribution, Unset):
            distribution = UNSET
        else:
            distribution = DistributionAttributes.from_dict(_distribution)

        post_queries_launch_query_request_body = cls(
            query_type=query_type,
            start_time=start_time,
            end_time=end_time,
            account_emails=account_emails,
            account_ids=account_ids,
            query_priority=query_priority,
            log=log,
            top_facets=top_facets,
            facet_values=facet_values,
            plot=plot,
            pq=pq,
            distribution=distribution,
        )

        post_queries_launch_query_request_body.additional_properties = d
        return post_queries_launch_query_request_body

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
