"""Tuya BLE Device Credentials container."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class TuyaBLEDeviceCredentials:
    """Holds credentials and metadata for Tuya BLE decryption and identification."""

    address: str
    device_id: str
    local_key: str

    # Optional metadata for richer device context
    category: Optional[str] = None
    product_id: Optional[str] = None
    device_name: Optional[str] = None
    uuid: Optional[str] = None
    product_model: Optional[str] = None
    product_name: Optional[str] = None

    def __post_init__(self):
        # Normalize MAC address for consistency across the integration
        self.address = self.address.lower().replace(":", "")
