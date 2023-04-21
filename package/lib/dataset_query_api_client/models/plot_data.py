from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.facet_fn import FacetFn


T = TypeVar("T", bound="PlotData")


@attr.s(auto_attribs=True)
class PlotData:
    """Holds plot information.

    Attributes:
        label (Union[Unset, str]): Label representing this plot.
        fn (Union[Unset, FacetFn]): Aggregation function applied on the expression supplied by the plot query.
        total (Union[Unset, float]): Total of the sample data.
        samples (Union[Unset, List[float]]): Y axis data points for this plot.
    """

    label: Union[Unset, str] = UNSET
    fn: Union[Unset, "FacetFn"] = UNSET
    total: Union[Unset, float] = UNSET
    samples: Union[Unset, List[float]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        label = self.label
        fn: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fn, Unset):
            fn = self.fn.to_dict()

        total = self.total
        samples: Union[Unset, List[float]] = UNSET
        if not isinstance(self.samples, Unset):
            samples = self.samples

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if label is not UNSET:
            field_dict["label"] = label
        if fn is not UNSET:
            field_dict["fn"] = fn
        if total is not UNSET:
            field_dict["total"] = total
        if samples is not UNSET:
            field_dict["samples"] = samples

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.facet_fn import FacetFn

        d = src_dict.copy()
        label = d.pop("label", UNSET)

        _fn = d.pop("fn", UNSET)
        fn: Union[Unset, FacetFn]
        if isinstance(_fn, Unset):
            fn = UNSET
        else:
            fn = FacetFn.from_dict(_fn)

        total = d.pop("total", UNSET)

        samples = cast(List[float], d.pop("samples", UNSET))

        plot_data = cls(
            label=label,
            fn=fn,
            total=total,
            samples=samples,
        )

        plot_data.additional_properties = d
        return plot_data

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
