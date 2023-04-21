from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TopFacetsAttributes")


@attr.s(auto_attribs=True)
class TopFacetsAttributes:
    """Attributes specific to the `TOP_FACETS` query type.

    Attributes:
        filter_ (Union[Unset, str]): Specifies which events to match, using the same syntax as the Expression field in
            the query UI.

            To match all events, omit this field or pass an empty string.
        num_values_to_return_per_facet (Union[Unset, int]): The maximum number of values to return per facet for the
            request
        determine_numeric (Union[Unset, bool]): Whether to determine if a value is numeric.
        num_facets_to_return (Union[Unset, int]): Number of facets to return.

            Before facets are returned, they are sorted by the number of events that have them, and in the event of a tie
            alphabetically.
    """

    filter_: Union[Unset, str] = UNSET
    num_values_to_return_per_facet: Union[Unset, int] = UNSET
    determine_numeric: Union[Unset, bool] = False
    num_facets_to_return: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        filter_ = self.filter_
        num_values_to_return_per_facet = self.num_values_to_return_per_facet
        determine_numeric = self.determine_numeric
        num_facets_to_return = self.num_facets_to_return

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if num_values_to_return_per_facet is not UNSET:
            field_dict["numValuesToReturnPerFacet"] = num_values_to_return_per_facet
        if determine_numeric is not UNSET:
            field_dict["determineNumeric"] = determine_numeric
        if num_facets_to_return is not UNSET:
            field_dict["numFacetsToReturn"] = num_facets_to_return

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        filter_ = d.pop("filter", UNSET)

        num_values_to_return_per_facet = d.pop("numValuesToReturnPerFacet", UNSET)

        determine_numeric = d.pop("determineNumeric", UNSET)

        num_facets_to_return = d.pop("numFacetsToReturn", UNSET)

        top_facets_attributes = cls(
            filter_=filter_,
            num_values_to_return_per_facet=num_values_to_return_per_facet,
            determine_numeric=determine_numeric,
            num_facets_to_return=num_facets_to_return,
        )

        top_facets_attributes.additional_properties = d
        return top_facets_attributes

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
