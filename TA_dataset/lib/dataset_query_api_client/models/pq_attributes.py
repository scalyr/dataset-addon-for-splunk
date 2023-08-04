# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.pq_result_type import PQResultType

T = TypeVar("T", bound="PQAttributes")


@attr.s(auto_attribs=True)
class PQAttributes:
    """Attributes specific to the `PQ` query type.

    Attributes:
        query (str): The power query to execute.
        result_type (PQResultType): Specifies the result type of a power query. Default: PQResultType.TABLE.
    """

    query: str
    result_type: PQResultType = PQResultType.TABLE
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        query = self.query
        result_type = self.result_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
                "resultType": result_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        query = d.pop("query")

        result_type = PQResultType(d.pop("resultType"))

        pq_attributes = cls(
            query=query,
            result_type=result_type,
        )

        pq_attributes.additional_properties = d
        return pq_attributes

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
