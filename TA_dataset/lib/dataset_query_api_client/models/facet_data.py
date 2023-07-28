from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.facet_value import FacetValue


T = TypeVar("T", bound="FacetData")


@attr.s(auto_attribs=True)
class FacetData:
    """Holds facet information.

    Attributes:
        name (Union[Unset, str]): Name of the facet.
        is_numeric (Union[Unset, bool]): Is set to `true` if the facet has primarily numeric values, otherwise is set to
            `false`.
        match_count (Union[Unset, float]): Number of events matching this facet. This is an estimate, and is the minimum
            of

            1) the facet sample match estimate, and
            2) the overall sample estimate for all facets
        sampled_match_count (Union[Unset, float]): Number of events matched in the sample.

            This is an estimate, computed as the sample's total estimated event match count
            divided by 2 * how many times the sample was reduced by half.
        unique_values_count (Union[Unset, int]): Number of unique values for this facet.
        values (Union[Unset, List['FacetValue']]): List of values of this facet. Caridinality may be smaller than
            uniqueValuesCount if request constrained maximum number of values to return.
    """

    name: Union[Unset, str] = UNSET
    is_numeric: Union[Unset, bool] = UNSET
    match_count: Union[Unset, float] = UNSET
    sampled_match_count: Union[Unset, float] = UNSET
    unique_values_count: Union[Unset, int] = UNSET
    values: Union[Unset, List["FacetValue"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        is_numeric = self.is_numeric
        match_count = self.match_count
        sampled_match_count = self.sampled_match_count
        unique_values_count = self.unique_values_count
        values: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.values, Unset):
            values = []
            for values_item_data in self.values:
                values_item = values_item_data.to_dict()

                values.append(values_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if is_numeric is not UNSET:
            field_dict["isNumeric"] = is_numeric
        if match_count is not UNSET:
            field_dict["matchCount"] = match_count
        if sampled_match_count is not UNSET:
            field_dict["sampledMatchCount"] = sampled_match_count
        if unique_values_count is not UNSET:
            field_dict["uniqueValuesCount"] = unique_values_count
        if values is not UNSET:
            field_dict["values"] = values

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.facet_value import FacetValue

        d = src_dict.copy()
        name = d.pop("name", UNSET)

        is_numeric = d.pop("isNumeric", UNSET)

        match_count = d.pop("matchCount", UNSET)

        sampled_match_count = d.pop("sampledMatchCount", UNSET)

        unique_values_count = d.pop("uniqueValuesCount", UNSET)

        values = []
        _values = d.pop("values", UNSET)
        for values_item_data in _values or []:
            values_item = FacetValue.from_dict(values_item_data)

            values.append(values_item)

        facet_data = cls(
            name=name,
            is_numeric=is_numeric,
            match_count=match_count,
            sampled_match_count=sampled_match_count,
            unique_values_count=unique_values_count,
            values=values,
        )

        facet_data.additional_properties = d
        return facet_data

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
