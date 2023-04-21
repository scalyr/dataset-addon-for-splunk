from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.log_event import LogEvent


T = TypeVar("T", bound="LogResultData")


@attr.s(auto_attribs=True)
class LogResultData:
    """Results of a `LOG` query.

    Attributes:
        estimated_match_count (Union[Unset, float]): Count of events matched in this query. May be exact, but for many
            queries it will be approximate.
        matches (Union[Unset, List['LogEvent']]): The list of log events that matched this query.

            This list is always returned in ascending timestamp order, regardless of the value of the `ascending` field in
            the query request.
    """

    estimated_match_count: Union[Unset, float] = UNSET
    matches: Union[Unset, List["LogEvent"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        estimated_match_count = self.estimated_match_count
        matches: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.matches, Unset):
            matches = []
            for matches_item_data in self.matches:
                matches_item = matches_item_data.to_dict()

                matches.append(matches_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if estimated_match_count is not UNSET:
            field_dict["estimatedMatchCount"] = estimated_match_count
        if matches is not UNSET:
            field_dict["matches"] = matches

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.log_event import LogEvent

        d = src_dict.copy()
        estimated_match_count = d.pop("estimatedMatchCount", UNSET)

        matches = []
        _matches = d.pop("matches", UNSET)
        for matches_item_data in _matches or []:
            matches_item = LogEvent.from_dict(matches_item_data)

            matches.append(matches_item)

        log_result_data = cls(
            estimated_match_count=estimated_match_count,
            matches=matches,
        )

        log_result_data.additional_properties = d
        return log_result_data

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
