from enum import Enum


class PlotAttributesFrequency(str, Enum):
    HIGH = "HIGH"
    LOW = "LOW"

    def __str__(self) -> str:
        return str(self.value)
