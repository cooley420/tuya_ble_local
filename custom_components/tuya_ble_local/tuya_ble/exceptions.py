"""Tuya BLE Local – Exception definitions."""

from __future__ import annotations


__all__ = [
    "TuyaBLEError",
    "TuyaBLEEnumValueError",
    "TuyaBLEDataFormatError",
    "TuyaBLEDataCRCError",
    "TuyaBLEDataLengthError",
    "TuyaBLEDeviceError",
]


class TuyaBLEError(Exception):
    """Base class for Tuya BLE errors."""

    def __str__(self):
        return self.args[0] if self.args else self.__class__.__name__


class TuyaBLEEnumValueError(TuyaBLEError):
    """Raised when a DP_ENUM datapoint receives a value of unexpected type."""

    def __init__(self) -> None:
        super().__init__("Value of DP_ENUM datapoint must be an unsigned integer.")


class TuyaBLEDataFormatError(TuyaBLEError):
    """Raised when incoming BLE data is improperly formatted."""

    def __init__(self) -> None:
        super().__init__("Incoming packet is formatted incorrectly.")


class TuyaBLEDataCRCError(TuyaBLEError):
    """Raised when a data packet fails CRC validation."""

    def __init__(self) -> None:
        super().__init__("Incoming packet failed CRC validation.")


class TuyaBLEDataLengthError(TuyaBLEError):
    """Raised when a data packet has an invalid length."""

    def __init__(self) -> None:
        super().__init__("Incoming packet has an invalid length.")


class TuyaBLEDeviceError(TuyaBLEError):
    """Raised when the BLE device returns an error in response to a command."""

    def __init__(self, code: int) -> None:
        self.code = code
        super().__init__(f"BLE device returned error code 0x{code:04X}")
