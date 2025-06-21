from dataclasses import dataclass
import logging
from .const import DEVICE_DEF_MANUFACTURER
from .tuya_ble import TuyaBLEDevice
from typing import Optional

_LOGGER = logging.getLogger(__name__)

@dataclass
class TuyaBLEProductInfo:
    product_id: str
    name: str
    model: str
    category: str
    platforms: list[str]
    manufacturer: str = DEVICE_DEF_MANUFACTURER
    fingerbot: Optional[TuyaBLEFingerbotInfo] = None

def log_if_fallback(product_info: TuyaBLEProductInfo, product_id: str, category: str) -> None:
    if product_info.name == "Unknown Device":
        _LOGGER.warning(
            "🧩 Product fallback used for product_id=%s, category=%s. No match in PRODUCT_MAP.",
            product_id,
            category,
        )

def get_device_product_info(device: TuyaBLEDevice) -> TuyaBLEProductInfo | None:
    product_id = device.product_id
    if not product_id:
        _LOGGER.warning("Device %s has no product ID", device.address)
        return None

    entry = PRODUCT_MAP.get(product_id)
    if entry:
        return TuyaBLEProductInfo(
            product_id=product_id,
            name=entry["name"],
            model=entry["model"],
            category=entry["category"],
            platforms=entry["platforms"],
        )

    fallback = TuyaBLEProductInfo(
        product_id=product_id,
        name="Unknown Device",
        model="Unknown",
        category="unknown",
        platforms=["sensor"],
    )
    log_if_fallback(fallback, product_id, device.category or "unknown")
    return fallback
