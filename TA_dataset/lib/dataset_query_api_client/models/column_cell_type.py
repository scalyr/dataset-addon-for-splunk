# -*- coding: utf-8 -*-
from enum import Enum


class ColumnCellType(str, Enum):
    NUMBER = "NUMBER"
    PERCENTAGE = "PERCENTAGE"
    STRING = "STRING"
    TIMESTAMP = "TIMESTAMP"

    def __str__(self) -> str:
        return str(self.value)
