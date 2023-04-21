from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.facet_data import FacetData


T = TypeVar("T", bound="TopFacetsResultData")


@attr.s(auto_attribs=True)
class TopFacetsResultData:
    """Results of a `TOP_FACETS` query.

    Attributes:
        sampled_event_count (Union[Unset, int]): Total count of events sampled for facet information.
        facets (Union[Unset, List['FacetData']]): The list of top facets.
    """

    sampled_event_count: Union[Unset, int] = UNSET
    facets: Union[Unset, List["FacetData"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        sampled_event_count = self.sampled_event_count
        facets: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.facets, Unset):
            facets = []
            for facets_item_data in self.facets:
                facets_item = facets_item_data.to_dict()

                facets.append(facets_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sampled_event_count is not UNSET:
            field_dict["sampledEventCount"] = sampled_event_count
        if facets is not UNSET:
            field_dict["facets"] = facets

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.facet_data import FacetData

        d = src_dict.copy()
        sampled_event_count = d.pop("sampledEventCount", UNSET)

        facets = []
        _facets = d.pop("facets", UNSET)
        for facets_item_data in _facets or []:
            facets_item = FacetData.from_dict(facets_item_data)

            facets.append(facets_item)

        top_facets_result_data = cls(
            sampled_event_count=sampled_event_count,
            facets=facets,
        )

        top_facets_result_data.additional_properties = d
        return top_facets_result_data

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
