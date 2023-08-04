# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.plot_data import PlotData
    from ..models.plot_result_data_slice_info import PlotResultDataSliceInfo


T = TypeVar("T", bound="PlotResultData")


@attr.s(auto_attribs=True)
class PlotResultData:
    """Results of a `PLOT` or `PQ` query with result type `PLOT`.

    Attributes:
        omitted_events (Union[Unset, float]): If we exceeded our memory or cardinality limits for a `PQ` query, this
            will hold the number of events which (as a result) are not reflected in the output. Otherwise 0. Always in the
            range [0, matchCount].
        match_count (Union[Unset, float]): Count of events matched in this query. May be exact, but for many queries it
            will be approximate.
        slice_info (Union[Unset, PlotResultDataSliceInfo]): Provides various slice sizes when autoAlign is `true`,
            otherwise this property is set to `null`.
        x_axis (Union[Unset, List[int]]): Timestamps for the xAxis of the graph.
        plots (Union[Unset, List['PlotData']]): Plots for this graph.
    """

    omitted_events: Union[Unset, float] = UNSET
    match_count: Union[Unset, float] = UNSET
    slice_info: Union[Unset, "PlotResultDataSliceInfo"] = UNSET
    x_axis: Union[Unset, List[int]] = UNSET
    plots: Union[Unset, List["PlotData"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        omitted_events = self.omitted_events
        match_count = self.match_count
        slice_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.slice_info, Unset):
            slice_info = self.slice_info.to_dict()

        x_axis: Union[Unset, List[int]] = UNSET
        if not isinstance(self.x_axis, Unset):
            x_axis = self.x_axis

        plots: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.plots, Unset):
            plots = []
            for plots_item_data in self.plots:
                plots_item = plots_item_data.to_dict()

                plots.append(plots_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if omitted_events is not UNSET:
            field_dict["omittedEvents"] = omitted_events
        if match_count is not UNSET:
            field_dict["matchCount"] = match_count
        if slice_info is not UNSET:
            field_dict["sliceInfo"] = slice_info
        if x_axis is not UNSET:
            field_dict["xAxis"] = x_axis
        if plots is not UNSET:
            field_dict["plots"] = plots

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.plot_data import PlotData
        from ..models.plot_result_data_slice_info import PlotResultDataSliceInfo

        d = src_dict.copy()
        omitted_events = d.pop("omittedEvents", UNSET)

        match_count = d.pop("matchCount", UNSET)

        _slice_info = d.pop("sliceInfo", UNSET)
        slice_info: Union[Unset, PlotResultDataSliceInfo]
        if isinstance(_slice_info, Unset):
            slice_info = UNSET
        else:
            slice_info = PlotResultDataSliceInfo.from_dict(_slice_info)

        x_axis = cast(List[int], d.pop("xAxis", UNSET))

        plots = []
        _plots = d.pop("plots", UNSET)
        for plots_item_data in _plots or []:
            plots_item = PlotData.from_dict(plots_item_data)

            plots.append(plots_item)

        plot_result_data = cls(
            omitted_events=omitted_events,
            match_count=match_count,
            slice_info=slice_info,
            x_axis=x_axis,
            plots=plots,
        )

        plot_result_data.additional_properties = d
        return plot_result_data

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
