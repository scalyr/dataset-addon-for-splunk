from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.log_event_server_info import LogEventServerInfo
    from ..models.log_event_values import LogEventValues


T = TypeVar("T", bound="LogEvent")


@attr.s(auto_attribs=True)
class LogEvent:
    """
    Attributes:
        cursor (Union[Unset, str]): Unique cursor which can be used for pagination.
        server_info (Union[Unset, LogEventServerInfo]): Collection of fields derived from configurations.
        session_id (Union[Unset, str]): The session id associated with this log event.
        severity (Union[Unset, int]): Severity level of this log event.
        thread_id (Union[Unset, str]): The thread id associated with this log event.
        timestamp (Union[Unset, int]): Nanosecond timestamp when the event occurred.
        values (Union[Unset, LogEventValues]): Collection of fields derived from the log event.
    """

    cursor: Union[Unset, str] = UNSET
    server_info: Union[Unset, "LogEventServerInfo"] = UNSET
    session_id: Union[Unset, str] = UNSET
    severity: Union[Unset, int] = UNSET
    thread_id: Union[Unset, str] = UNSET
    timestamp: Union[Unset, int] = UNSET
    values: Union[Unset, "LogEventValues"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cursor = self.cursor
        server_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.server_info, Unset):
            server_info = self.server_info.to_dict()

        session_id = self.session_id
        severity = self.severity
        thread_id = self.thread_id
        timestamp = self.timestamp
        values: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.values, Unset):
            values = self.values.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cursor is not UNSET:
            field_dict["cursor"] = cursor
        if server_info is not UNSET:
            field_dict["serverInfo"] = server_info
        if session_id is not UNSET:
            field_dict["sessionId"] = session_id
        if severity is not UNSET:
            field_dict["severity"] = severity
        if thread_id is not UNSET:
            field_dict["threadId"] = thread_id
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if values is not UNSET:
            field_dict["values"] = values

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.log_event_server_info import LogEventServerInfo
        from ..models.log_event_values import LogEventValues

        d = src_dict.copy()
        cursor = d.pop("cursor", UNSET)

        _server_info = d.pop("serverInfo", UNSET)
        server_info: Union[Unset, LogEventServerInfo]
        if isinstance(_server_info, Unset):
            server_info = UNSET
        else:
            server_info = LogEventServerInfo.from_dict(_server_info)

        session_id = d.pop("sessionId", UNSET)

        severity = d.pop("severity", UNSET)

        thread_id = d.pop("threadId", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        _values = d.pop("values", UNSET)
        values: Union[Unset, LogEventValues]
        if isinstance(_values, Unset):
            values = UNSET
        else:
            values = LogEventValues.from_dict(_values)

        log_event = cls(
            cursor=cursor,
            server_info=server_info,
            session_id=session_id,
            severity=severity,
            thread_id=thread_id,
            timestamp=timestamp,
            values=values,
        )

        log_event.additional_properties = d
        return log_event

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
