# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FacetValuesAttributes")


@attr.s(auto_attribs=True)
class FacetValuesAttributes:
    """Attributes specific to the `FACET_VALUES` query type.

    Attributes:
        filter_ (Union[Unset, str]): Specifies which events to match, using the same syntax as the Expression field in
            the query UI.

            To match all events, omit this field or pass an empty string.
        name (Union[Unset, str]): Specifies the facet name to get values for.
        max_values (Union[Unset, int]): The maximum number of unique values to return per facet for the request.
            Default: 100.
        determine_numeric (Union[Unset, bool]): Whether to determine if a value is numeric.
    """

    filter_: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    max_values: Union[Unset, int] = 100
    determine_numeric: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        filter_ = self.filter_
        name = self.name
        max_values = self.max_values
        determine_numeric = self.determine_numeric

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if name is not UNSET:
            field_dict["name"] = name
        if max_values is not UNSET:
            field_dict["maxValues"] = max_values
        if determine_numeric is not UNSET:
            field_dict["determineNumeric"] = determine_numeric

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        filter_ = d.pop("filter", UNSET)

        name = d.pop("name", UNSET)

        max_values = d.pop("maxValues", UNSET)

        determine_numeric = d.pop("determineNumeric", UNSET)

        facet_values_attributes = cls(
            filter_=filter_,
            name=name,
            max_values=max_values,
            determine_numeric=determine_numeric,
        )

        facet_values_attributes.additional_properties = d
        return facet_values_attributes

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
