from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DistributionAttributes")


@attr.s(auto_attribs=True)
class DistributionAttributes:
    """Attributes specific to the `DISTRIBUTION` query type.

    Attributes:
        filter_ (Union[Unset, str]): Specifies which events to match, using the same syntax as the Expression field in
            the query UI.

            To match all events, omit this field or pass an empty string.
        facet (Union[Unset, str]): The facet to query and aggregate on.

            Currently all facet queries will be aggregated using the 'count' function.
    """

    filter_: Union[Unset, str] = UNSET
    facet: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        filter_ = self.filter_
        facet = self.facet

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if facet is not UNSET:
            field_dict["facet"] = facet

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        filter_ = d.pop("filter", UNSET)

        facet = d.pop("facet", UNSET)

        distribution_attributes = cls(
            filter_=filter_,
            facet=facet,
        )

        distribution_attributes.additional_properties = d
        return distribution_attributes

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
