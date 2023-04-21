from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="HistogramResultData")


@attr.s(auto_attribs=True)
class HistogramResultData:
    """Results of a `DISTRIBUTION` query.

    Attributes:
        match_count (Union[Unset, float]): Count of events matched in this query. May be exact, but for many queries it
            will be approximate.
        min_positive (Union[Unset, float]): Smallest positive index required on x-axis of graph
        max_positive (Union[Unset, float]): Largest positive index required on x-axis of graph
        min_negative (Union[Unset, float]): Smallest negative index required on x-axis of graph
        max_negative (Union[Unset, float]): Largest negative index required on x-axis of graph
        bucket_ratio (Union[Unset, float]): Ratio of values in a bucket. e.g. 1.1 means that the bucket counts values in
            the range [min, min * 1.1)
        positive_sample_counts (Union[Unset, List[float]]): Number of samples in each bucket representing positive
            values
        negative_sample_counts (Union[Unset, List[float]]): Number of samples in each bucket representing negative
            values
        positive_x_axis (Union[Unset, List[float]]): Plots on positive axis corresponding to each bucket in
            positiveSampleCounts
        negative_x_axis (Union[Unset, List[float]]): Plots on negative axis corresponding to each bucket in
            negativeSampleCounts
        positive_bucket_widths (Union[Unset, List[float]]): Widths of buckets on positive x axis corresponding to each
            midpoint in positiveXAxis.

            Widths need to be used only if the client is plotting the data in linear space. For log space, buckets will be
            of equal width
        negative_bucket_widths (Union[Unset, List[float]]): Widths of buckets on negative x axis corresponding to each
            midpoint in negativeXAxis.

            Widths need to be used only if the client is plotting the data in linear space. For log space, buckets will be
            of equal width.
        zero_count (Union[Unset, float]): Number of samples representing zero values
        mean (Union[Unset, float]): mean of the samples
        median (Union[Unset, float]): median of the samples
        min_ (Union[Unset, float]): min of the samples
        max_ (Union[Unset, float]): max of the samples
        p10 (Union[Unset, float]): p10 of the samples
        p90 (Union[Unset, float]): p90 of the samples
        p99 (Union[Unset, float]): p99 of the samples
        p999 (Union[Unset, float]): p999 of the samples
    """

    match_count: Union[Unset, float] = UNSET
    min_positive: Union[Unset, float] = UNSET
    max_positive: Union[Unset, float] = UNSET
    min_negative: Union[Unset, float] = UNSET
    max_negative: Union[Unset, float] = UNSET
    bucket_ratio: Union[Unset, float] = UNSET
    positive_sample_counts: Union[Unset, List[float]] = UNSET
    negative_sample_counts: Union[Unset, List[float]] = UNSET
    positive_x_axis: Union[Unset, List[float]] = UNSET
    negative_x_axis: Union[Unset, List[float]] = UNSET
    positive_bucket_widths: Union[Unset, List[float]] = UNSET
    negative_bucket_widths: Union[Unset, List[float]] = UNSET
    zero_count: Union[Unset, float] = UNSET
    mean: Union[Unset, float] = UNSET
    median: Union[Unset, float] = UNSET
    min_: Union[Unset, float] = UNSET
    max_: Union[Unset, float] = UNSET
    p10: Union[Unset, float] = UNSET
    p90: Union[Unset, float] = UNSET
    p99: Union[Unset, float] = UNSET
    p999: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        match_count = self.match_count
        min_positive = self.min_positive
        max_positive = self.max_positive
        min_negative = self.min_negative
        max_negative = self.max_negative
        bucket_ratio = self.bucket_ratio
        positive_sample_counts: Union[Unset, List[float]] = UNSET
        if not isinstance(self.positive_sample_counts, Unset):
            positive_sample_counts = self.positive_sample_counts

        negative_sample_counts: Union[Unset, List[float]] = UNSET
        if not isinstance(self.negative_sample_counts, Unset):
            negative_sample_counts = self.negative_sample_counts

        positive_x_axis: Union[Unset, List[float]] = UNSET
        if not isinstance(self.positive_x_axis, Unset):
            positive_x_axis = self.positive_x_axis

        negative_x_axis: Union[Unset, List[float]] = UNSET
        if not isinstance(self.negative_x_axis, Unset):
            negative_x_axis = self.negative_x_axis

        positive_bucket_widths: Union[Unset, List[float]] = UNSET
        if not isinstance(self.positive_bucket_widths, Unset):
            positive_bucket_widths = self.positive_bucket_widths

        negative_bucket_widths: Union[Unset, List[float]] = UNSET
        if not isinstance(self.negative_bucket_widths, Unset):
            negative_bucket_widths = self.negative_bucket_widths

        zero_count = self.zero_count
        mean = self.mean
        median = self.median
        min_ = self.min_
        max_ = self.max_
        p10 = self.p10
        p90 = self.p90
        p99 = self.p99
        p999 = self.p999

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if match_count is not UNSET:
            field_dict["matchCount"] = match_count
        if min_positive is not UNSET:
            field_dict["minPositive"] = min_positive
        if max_positive is not UNSET:
            field_dict["maxPositive"] = max_positive
        if min_negative is not UNSET:
            field_dict["minNegative"] = min_negative
        if max_negative is not UNSET:
            field_dict["maxNegative"] = max_negative
        if bucket_ratio is not UNSET:
            field_dict["bucketRatio"] = bucket_ratio
        if positive_sample_counts is not UNSET:
            field_dict["positiveSampleCounts"] = positive_sample_counts
        if negative_sample_counts is not UNSET:
            field_dict["negativeSampleCounts"] = negative_sample_counts
        if positive_x_axis is not UNSET:
            field_dict["positiveXAxis"] = positive_x_axis
        if negative_x_axis is not UNSET:
            field_dict["negativeXAxis"] = negative_x_axis
        if positive_bucket_widths is not UNSET:
            field_dict["positiveBucketWidths"] = positive_bucket_widths
        if negative_bucket_widths is not UNSET:
            field_dict["negativeBucketWidths"] = negative_bucket_widths
        if zero_count is not UNSET:
            field_dict["zeroCount"] = zero_count
        if mean is not UNSET:
            field_dict["mean"] = mean
        if median is not UNSET:
            field_dict["median"] = median
        if min_ is not UNSET:
            field_dict["min"] = min_
        if max_ is not UNSET:
            field_dict["max"] = max_
        if p10 is not UNSET:
            field_dict["p10"] = p10
        if p90 is not UNSET:
            field_dict["p90"] = p90
        if p99 is not UNSET:
            field_dict["p99"] = p99
        if p999 is not UNSET:
            field_dict["p999"] = p999

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        match_count = d.pop("matchCount", UNSET)

        min_positive = d.pop("minPositive", UNSET)

        max_positive = d.pop("maxPositive", UNSET)

        min_negative = d.pop("minNegative", UNSET)

        max_negative = d.pop("maxNegative", UNSET)

        bucket_ratio = d.pop("bucketRatio", UNSET)

        positive_sample_counts = cast(List[float], d.pop("positiveSampleCounts", UNSET))

        negative_sample_counts = cast(List[float], d.pop("negativeSampleCounts", UNSET))

        positive_x_axis = cast(List[float], d.pop("positiveXAxis", UNSET))

        negative_x_axis = cast(List[float], d.pop("negativeXAxis", UNSET))

        positive_bucket_widths = cast(List[float], d.pop("positiveBucketWidths", UNSET))

        negative_bucket_widths = cast(List[float], d.pop("negativeBucketWidths", UNSET))

        zero_count = d.pop("zeroCount", UNSET)

        mean = d.pop("mean", UNSET)

        median = d.pop("median", UNSET)

        min_ = d.pop("min", UNSET)

        max_ = d.pop("max", UNSET)

        p10 = d.pop("p10", UNSET)

        p90 = d.pop("p90", UNSET)

        p99 = d.pop("p99", UNSET)

        p999 = d.pop("p999", UNSET)

        histogram_result_data = cls(
            match_count=match_count,
            min_positive=min_positive,
            max_positive=max_positive,
            min_negative=min_negative,
            max_negative=max_negative,
            bucket_ratio=bucket_ratio,
            positive_sample_counts=positive_sample_counts,
            negative_sample_counts=negative_sample_counts,
            positive_x_axis=positive_x_axis,
            negative_x_axis=negative_x_axis,
            positive_bucket_widths=positive_bucket_widths,
            negative_bucket_widths=negative_bucket_widths,
            zero_count=zero_count,
            mean=mean,
            median=median,
            min_=min_,
            max_=max_,
            p10=p10,
            p90=p90,
            p99=p99,
            p999=p999,
        )

        histogram_result_data.additional_properties = d
        return histogram_result_data

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
