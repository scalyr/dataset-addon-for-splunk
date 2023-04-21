from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.plot_attributes_frequency import PlotAttributesFrequency
from ..types import UNSET, Unset

T = TypeVar("T", bound="PlotAttributes")


@attr.s(auto_attribs=True)
class PlotAttributes:
    """Attributes specific to the `PLOT` query type.

    Attributes:
        filter_ (Union[Unset, str]): Specifies which events to match, using the same syntax as the Expression field in
            the query UI.

            To match all events, omit this field or pass an empty string.
        slices (Union[Unset, int]): Number of parts the time range will be divided into. Cannot be used together with
            `sliceWidth`.
        slice_width (Union[Unset, str]): Width in duration the time range will be divided into. Cannot be used together
            with `slices`.

            Supported units: `seconds` or `s`, `minutes` or `m`, `hours` or `h`, `days` or `d`, `weeks` or `w`.
        auto_align (Union[Unset, bool]): Based on a the time range and a target number of slices, auto aligns the slices
            to a meaningful boundary.
        auto_aggregate (Union[Unset, bool]): When set to true, no matter what function is specified in the expression,
            the result of this query will include a list of plots with the following aggregations applied:
            - count
            - mean
            - min
            - max
            - sum
            - sumPerSecond
            - countPerSecond
            - p10
            - p50
            - p90
            - p95
            - p99
            - p999
        expression (Union[Unset, str]): Expression to query and filter numeric data.
        breakdown_facet (Union[Unset, str]): Additional facet to breakdown by.
        frequency (Union[Unset, PlotAttributesFrequency]): Clients should set frequency to `HIGH` if the query with the
            same expression will be repeated.

            Defaults to `LOW`.
    """

    filter_: Union[Unset, str] = UNSET
    slices: Union[Unset, int] = UNSET
    slice_width: Union[Unset, str] = UNSET
    auto_align: Union[Unset, bool] = False
    auto_aggregate: Union[Unset, bool] = False
    expression: Union[Unset, str] = UNSET
    breakdown_facet: Union[Unset, str] = UNSET
    frequency: Union[Unset, PlotAttributesFrequency] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        filter_ = self.filter_
        slices = self.slices
        slice_width = self.slice_width
        auto_align = self.auto_align
        auto_aggregate = self.auto_aggregate
        expression = self.expression
        breakdown_facet = self.breakdown_facet
        frequency: Union[Unset, str] = UNSET
        if not isinstance(self.frequency, Unset):
            frequency = self.frequency.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if slices is not UNSET:
            field_dict["slices"] = slices
        if slice_width is not UNSET:
            field_dict["sliceWidth"] = slice_width
        if auto_align is not UNSET:
            field_dict["autoAlign"] = auto_align
        if auto_aggregate is not UNSET:
            field_dict["autoAggregate"] = auto_aggregate
        if expression is not UNSET:
            field_dict["expression"] = expression
        if breakdown_facet is not UNSET:
            field_dict["breakdownFacet"] = breakdown_facet
        if frequency is not UNSET:
            field_dict["frequency"] = frequency

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        filter_ = d.pop("filter", UNSET)

        slices = d.pop("slices", UNSET)

        slice_width = d.pop("sliceWidth", UNSET)

        auto_align = d.pop("autoAlign", UNSET)

        auto_aggregate = d.pop("autoAggregate", UNSET)

        expression = d.pop("expression", UNSET)

        breakdown_facet = d.pop("breakdownFacet", UNSET)

        _frequency = d.pop("frequency", UNSET)
        frequency: Union[Unset, PlotAttributesFrequency]
        if isinstance(_frequency, Unset):
            frequency = UNSET
        else:
            frequency = PlotAttributesFrequency(_frequency)

        plot_attributes = cls(
            filter_=filter_,
            slices=slices,
            slice_width=slice_width,
            auto_align=auto_align,
            auto_aggregate=auto_aggregate,
            expression=expression,
            breakdown_facet=breakdown_facet,
            frequency=frequency,
        )

        plot_attributes.additional_properties = d
        return plot_attributes

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
