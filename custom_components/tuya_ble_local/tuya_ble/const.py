"""Tuya BLE Protocol-level Constants."""

from __future__ import annotations

from enum import IntEnum

# 📡 BLE Connection Constants
GATT_MTU = 20  # Tuya BLE MTU size—max payload per write
DEFAULT_ATTEMPTS = 0xFFFF  # Retry attempts for pairing or command retries

CHARACTERISTIC_NOTIFY = "00002b10-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_WRITE = "00002b11-0000-1000-8000-00805f9b34fb"

SERVICE_UUID = "0000a201-0000-1000-8000-00805f9b34fb"
MANUFACTURER_DATA_ID = 0x07D0  # Tuya-specific identifier in BLE advertisement
RESPONSE_WAIT_TIMEOUT = 60  # Seconds to wait for device reply (for handshake, pairing, etc.)

# (Optional) CCCD notification enable payload (if needed)
CCCD_NOTIFY_ENABLE = b"\x01\x00"


class TuyaBLECode(IntEnum):
    """Tuya BLE protocol function codes (host→device and device→host)."""

    def uses_login_key(self) -> bool:
        return self == TuyaBLECode.FUN_SENDER_DEVICE_INFO

    # Host-initiated
    FUN_SENDER_DEVICE_INFO = 0x0000
    FUN_SENDER_PAIR = 0x0001
    FUN_SENDER_DPS = 0x0002
    FUN_SENDER_DEVICE_STATUS = 0x0003
    FUN_SENDER_UNBIND = 0x0005
    FUN_SENDER_DEVICE_RESET = 0x0006

    # OTA updates
    FUN_SENDER_OTA_START = 0x000C
    FUN_SENDER_OTA_FILE = 0x000D
    FUN_SENDER_OTA_OFFSET = 0x000E
    FUN_SENDER_OTA_UPGRADE = 0x000F
    FUN_SENDER_OTA_OVER = 0x0010

    # DPS v4 (compressed)
    FUN_SENDER_DPS_V4 = 0x0027

    # Device-initiated (incoming)
    FUN_RECEIVE_DP = 0x8001
    FUN_RECEIVE_TIME_DP = 0x8003
    FUN_RECEIVE_SIGN_DP = 0x8004
    FUN_RECEIVE_SIGN_TIME_DP = 0x8005
    FUN_RECEIVE_DP_V4 = 0x8006
    FUN_RECEIVE_TIME_DP_V4 = 0x8007

    # Device requests time sync
    FUN_RECEIVE_TIME1_REQ = 0x8011
    FUN_RECEIVE_TIME2_REQ = 0x8012


class TuyaBLEDataPointType(IntEnum):
    """Supported Tuya BLE Data Point types."""

    DT_RAW = 0
    DT_BOOL = 1
    DT_VALUE = 2
    DT_STRING = 3
    DT_ENUM = 4
    DT_BITMAP = 5
