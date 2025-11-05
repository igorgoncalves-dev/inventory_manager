from enum import Enum


class MachineStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    IN_USE = "IN_USE"
    MAINTENANCE = "MAINTENANCE"
    DEPRECATED = "DEPRECATED"
