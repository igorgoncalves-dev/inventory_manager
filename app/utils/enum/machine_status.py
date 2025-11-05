from enum import Enum


class DeviceStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    IN_USE = "IN_USE"
    MAINTENANCE = "MAINTENANCE"
    DEPRECATED = "DEPRECATED"
