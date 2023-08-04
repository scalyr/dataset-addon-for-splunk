# -*- coding: utf-8 -*-
from enum import Enum


class PostQueriesLaunchQueryRequestBodyQueryType(str, Enum):
    DISTRIBUTION = "DISTRIBUTION"
    FACET_VALUES = "FACET_VALUES"
    LOG = "LOG"
    PLOT = "PLOT"
    PQ = "PQ"
    TOP_FACETS = "TOP_FACETS"

    def __str__(self) -> str:
        return str(self.value)
