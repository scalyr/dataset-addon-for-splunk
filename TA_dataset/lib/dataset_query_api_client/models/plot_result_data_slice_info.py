# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PlotResultDataSliceInfo")


@attr.s(auto_attribs=True)
class PlotResultDataSliceInfo:
    """Provides various slice sizes when autoAlign is `true`, otherwise this property is set to `null`.

    Attributes:
        default_size (Union[Unset, float]): The size of all the slices in milliseconds except possibly the first and
            last.
        first_size (Union[Unset, float]): The size of the first slice in milliseconds. This can be less than the sizes
            for subsequent slices due to alignment.
        last_size (Union[Unset, float]): The size of the last slice in milliseconds. This can be less than the sizes of
            earlier slices due to alignment.
        num_slices (Union[Unset, int]): The number of slices the query is divided into. This value could be greater than
            requested slices if autoAlign is `true`.
    """

    default_size: Union[Unset, float] = UNSET
    first_size: Union[Unset, float] = UNSET
    last_size: Union[Unset, float] = UNSET
    num_slices: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        default_size = self.default_size
        first_size = self.first_size
        last_size = self.last_size
        num_slices = self.num_slices

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if default_size is not UNSET:
            field_dict["defaultSize"] = default_size
        if first_size is not UNSET:
            field_dict["firstSize"] = first_size
        if last_size is not UNSET:
            field_dict["lastSize"] = last_size
        if num_slices is not UNSET:
            field_dict["numSlices"] = num_slices

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        default_size = d.pop("defaultSize", UNSET)

        first_size = d.pop("firstSize", UNSET)

        last_size = d.pop("lastSize", UNSET)

        num_slices = d.pop("numSlices", UNSET)

        plot_result_data_slice_info = cls(
            default_size=default_size,
            first_size=first_size,
            last_size=last_size,
            num_slices=num_slices,
        )

        plot_result_data_slice_info.additional_properties = d
        return plot_result_data_slice_info

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
