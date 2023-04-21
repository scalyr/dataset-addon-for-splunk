from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.facet_fn_operator import FacetFnOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="FacetFn")


@attr.s(auto_attribs=True)
class FacetFn:
    """Aggregation function applied on the expression supplied by the plot query.

    Attributes:
        operator (Union[Unset, FacetFnOperator]): Operator applied on an expression.

            `count` - the number of samples in each time period

            `countPerSecond` - the number of samples per second (mean across each time period)

            `max` - the maximum sample in each time period

            `mean` - the mean of all samples in each time period

            `min` - the minimum sample in each time period

            `p` - the nth percentile of all samples, n is supplied as the param value whose's magnitude can be anywhere
            between 0 and 1.

            `p10` - the 10th percentile of all samples in each time period

            `p50` - the median of all samples in each time period

            `p90` - the 90th percentile of all samples in each time period

            `p95` - the 95th percentile of all samples in each time period

            `p99` - the 99th percentile of all samples in each time period

            `p999` - the 99.9th percentile of all samples in each time period

            `sum` - the sum of all time-series in each time period

            `sumPerSecond` - the sum of all time-series in each time period, divided by the number of seconds covered
        param (Union[Unset, float]): Statistical parameter to be used in conjunction with the operator.

            This is largely applicable for the percentile operators i.e. for p10 this param would 0.1.
    """

    operator: Union[Unset, FacetFnOperator] = UNSET
    param: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        operator: Union[Unset, str] = UNSET
        if not isinstance(self.operator, Unset):
            operator = self.operator.value

        param = self.param

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if operator is not UNSET:
            field_dict["operator"] = operator
        if param is not UNSET:
            field_dict["param"] = param

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _operator = d.pop("operator", UNSET)
        operator: Union[Unset, FacetFnOperator]
        if isinstance(_operator, Unset):
            operator = UNSET
        else:
            operator = FacetFnOperator(_operator)

        param = d.pop("param", UNSET)

        facet_fn = cls(
            operator=operator,
            param=param,
        )

        facet_fn.additional_properties = d
        return facet_fn

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
