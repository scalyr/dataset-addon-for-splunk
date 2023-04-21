from enum import Enum


class FacetFnOperator(str, Enum):
    COUNT = "count"
    COUNTPERSECOND = "countPerSecond"
    MAX = "max"
    MEAN = "mean"
    MIN = "min"
    P = "p"
    P10 = "p10"
    P50 = "p50"
    P90 = "p90"
    P95 = "p95"
    P99 = "p99"
    P999 = "p999"
    PERCENTILE = "percentile"
    SUM = "sum"
    SUMPERSECOND = "sumPerSecond"

    def __str__(self) -> str:
        return str(self.value)
