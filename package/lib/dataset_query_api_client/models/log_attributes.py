from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LogAttributes")


@attr.s(auto_attribs=True)
class LogAttributes:
    """Attributes specific to the `LOG` query type.

    Attributes:
        filter_ (Union[Unset, str]): Specifies which events to match, using the same syntax as the Expression field in
            the query UI.

            To match all events, omit this field or pass an empty string. Default: ''.
        ascending (Union[Unset, bool]): If true, results are returned in order from oldest to newest; if false, results
            are returned in order from newest to oldest.
        limit (Union[Unset, int]): Limits the number of returned log events. Default: 1000.
        cursor (Union[Unset, str]): Cursor returned by a previous `log` query, used for pagination. Results are returned
            starting with this cursor (inclusive).

            If this parameter is not provided `ascending=true`` requests will start at the beginning of the provided time
            range and `ascending=false` requests will start at the end of the time range.
    """

    filter_: Union[Unset, str] = ""
    ascending: Union[Unset, bool] = False
    limit: Union[Unset, int] = 1000
    cursor: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        filter_ = self.filter_
        ascending = self.ascending
        limit = self.limit
        cursor = self.cursor

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if ascending is not UNSET:
            field_dict["ascending"] = ascending
        if limit is not UNSET:
            field_dict["limit"] = limit
        if cursor is not UNSET:
            field_dict["cursor"] = cursor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        filter_ = d.pop("filter", UNSET)

        ascending = d.pop("ascending", UNSET)

        limit = d.pop("limit", UNSET)

        cursor = d.pop("cursor", UNSET)

        log_attributes = cls(
            filter_=filter_,
            ascending=ascending,
            limit=limit,
            cursor=cursor,
        )

        log_attributes.additional_properties = d
        return log_attributes

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
