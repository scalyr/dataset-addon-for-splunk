# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.facet_data import FacetData


T = TypeVar("T", bound="FacetValuesResultData")


@attr.s(auto_attribs=True)
class FacetValuesResultData:
    """Results of a `FACET_VALUES` query.

    Attributes:
        facet (Union[Unset, FacetData]): Holds facet information.
    """

    facet: Union[Unset, "FacetData"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        facet: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.facet, Unset):
            facet = self.facet.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if facet is not UNSET:
            field_dict["facet"] = facet

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.facet_data import FacetData

        d = src_dict.copy()
        _facet = d.pop("facet", UNSET)
        facet: Union[Unset, FacetData]
        if isinstance(_facet, Unset):
            facet = UNSET
        else:
            facet = FacetData.from_dict(_facet)

        facet_values_result_data = cls(
            facet=facet,
        )

        facet_values_result_data.additional_properties = d
        return facet_values_result_data

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
