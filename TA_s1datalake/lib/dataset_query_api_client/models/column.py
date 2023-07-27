from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.column_cell_type import ColumnCellType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Column")


@attr.s(auto_attribs=True)
class Column:
    """
    Attributes:
        name (Union[Unset, str]):
        cell_type (Union[Unset, ColumnCellType]): Data type of the cell value.

            `NUMBER`: Number format with possible decimal places, except for "NaN", "-Infinity" and "+Infinity" which will
            be strings.

            `PERCENTAGE`: Number from 0 - 100, used only in reports.

            `STRING`: Basic string format.

            `TIMESTAMP`: Timestamp in epoch ns, μs, ms, or s.
        decimal_places (Union[Unset, int]): Number of decimal places for `NUMBER` format.
    """

    name: Union[Unset, str] = UNSET
    cell_type: Union[Unset, ColumnCellType] = UNSET
    decimal_places: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        cell_type: Union[Unset, str] = UNSET
        if not isinstance(self.cell_type, Unset):
            cell_type = self.cell_type.value

        decimal_places = self.decimal_places

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if cell_type is not UNSET:
            field_dict["cellType"] = cell_type
        if decimal_places is not UNSET:
            field_dict["decimalPlaces"] = decimal_places

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        _cell_type = d.pop("cellType", UNSET)
        cell_type: Union[Unset, ColumnCellType]
        if isinstance(_cell_type, Unset):
            cell_type = UNSET
        else:
            cell_type = ColumnCellType(_cell_type)

        decimal_places = d.pop("decimalPlaces", UNSET)

        column = cls(
            name=name,
            cell_type=cell_type,
            decimal_places=decimal_places,
        )

        column.additional_properties = d
        return column

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
