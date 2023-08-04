# -*- coding: utf-8 -*-
from enum import Enum


class PQResultType(str, Enum):
    PLOT = "PLOT"
    TABLE = "TABLE"

    def __str__(self) -> str:
        return str(self.value)
