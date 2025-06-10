"""Constants for the Tuya BLE Local integration."""
from __future__ import annotations

from typing_extensions import Final
from enum import StrEnum

# Core domain
DOMAIN: Final = "tuya_ble_local"

# Tuya BLE metadata
DEVICE_METADATA_UUIDS: Final = "uuids"
DEVICE_DEF_MANUFACTURER: Final = "Tuya"
SET_DISCONNECTED_DELAY = 10 * 60

# Config Entry keys
CONF_ADDRESS: Final = "mac_address"
CONF_LOCAL_KEY: Final = "local_key"
CONF_UUID: Final = "uuid"
CONF_CATEGORY: Final = "category"
CONF_PRODUCT_ID: Final = "product_id"
CONF_DEVICE_NAME: Final = "device_name"
CONF_PRODUCT_MODEL: Final = "product_model"
CONF_PRODUCT_NAME: Final = "product_name"

# BLE identifiers
SERVICE_DATA_UUID: Final = "0000a201-0000-1000-8000-00805f9b34fb"

# Platform types (optional, shared across init/setup)
PLATFORM_TYPES: Final = (
    "button",
    "climate",
    "number",
    "sensor",
    "binary_sensor",
    "select",
    "switch",
    "text",
)

# Battery state constants
BATTERY_STATE_LOW: Final = "low"
BATTERY_STATE_NORMAL: Final = "normal"
BATTERY_STATE_HIGH: Final = "high"

BATTERY_NOT_CHARGING: Final = "not_charging"
BATTERY_CHARGING: Final = "charging"
BATTERY_CHARGED: Final = "charged"

# CO₂ level states
CO2_LEVEL_NORMAL: Final = "normal"
CO2_LEVEL_ALARM: Final = "alarm"

# Fingerbot-specific values
class FingerbotMode(StrEnum):
    PUSH = "push"
    SWITCH = "switch"
    PROGRAM = "program"

FINGERBOT_BUTTON_EVENT: Final = "fingerbot_button_pressed"
