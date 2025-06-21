"""The Tuya BLE Local integration."""
from __future__ import annotations
from dataclasses import dataclass

import logging
from homeassistant.const import CONF_ADDRESS, CONF_DEVICE_ID

from homeassistant.core import CALLBACK_TYPE, HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import (
    DeviceInfo,
    EntityDescription,
    generate_entity_id,
)
from homeassistant.helpers.event import async_call_later
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from home_assistant_bluetooth import BluetoothServiceInfoBleak
from .tuya_ble import (
    TuyaBLEDataPoint,
    TuyaBLEDevice,
    TuyaBLEDeviceCredentials,
)

from .const import (
    DEVICE_DEF_MANUFACTURER,
    DOMAIN,
    FINGERBOT_BUTTON_EVENT,
    SET_DISCONNECTED_DELAY,
)

from .product_map import get_device_product_info, TuyaBLEProductInfo

_LOGGER = logging.getLogger(__name__)


@dataclass
class TuyaBLEFingerbotInfo:
    switch: int
    mode: int
    up_position: int
    down_position: int
    hold_time: int
    reverse_positions: int
    manual_control: int = 0
    program: int = 0


class TuyaBLEEntity(CoordinatorEntity):
    """Tuya BLE base entity."""

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: TuyaBLECoordinator,
        device: TuyaBLEDevice,
        product: TuyaBLEProductInfo,
        description: EntityDescription,
    ) -> None:
        super().__init__(coordinator)
        self._hass = hass
        self._coordinator = coordinator
        self._device = device
        self._product = product
        if description.translation_key is None:
            self._attr_translation_key = description.key
        self.entity_description = description
        self._attr_has_entity_name = True
        self._attr_device_info = get_device_info(self._device)
        self._attr_unique_id = f"{self._device.device_id}-{description.key}"
        self.entity_id = generate_entity_id(
            "sensor.{}", self._attr_unique_id, hass=hass
        )

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self._coordinator.connected

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()


class TuyaBLECoordinator(DataUpdateCoordinator[None]):
    """Data coordinator for receiving Tuya BLE updates."""

    def __init__(self, hass: HomeAssistant, device: TuyaBLEDevice) -> None:
        """Initialise the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
        )
        self._device = device
        self._disconnected: bool = True
        self._unsub_disconnect: CALLBACK_TYPE | None = None
        device.register_connected_callback(self._async_handle_connect)
        device.register_callback(self._async_handle_update)
        device.register_disconnected_callback(self._async_handle_disconnect)

    @property
    def connected(self) -> bool:
        return not self._disconnected

    @callback
    def _async_handle_connect(self) -> None:
        if self._unsub_disconnect is not None:
            self._unsub_disconnect()
        if self._disconnected:
            self._disconnected = False
            self.async_update_listeners()

    @callback
    def _async_handle_update(self, updates: list[TuyaBLEDataPoint]) -> None:
        """Just trigger the callbacks."""
        self._async_handle_connect()
        self.async_set_updated_data(None)
        info = get_device_product_info(self._device)
        if info and info.fingerbot and info.fingerbot.manual_control != 0:
            for update in updates:
                if update.id == info.fingerbot.switch and update.changed_by_device:
                    self.hass.bus.fire(
                        FINGERBOT_BUTTON_EVENT,
                        {
                            CONF_ADDRESS: self._device.address,
                            CONF_DEVICE_ID: self._device.device_id,
                        },
                    )

    @callback
    def _set_disconnected(self, _: None) -> None:
        """Invoke the idle timeout callback, called when the alarm fires."""
        self._disconnected = True
        self._unsub_disconnect = None
        self.async_update_listeners()

    @callback
    def _async_handle_disconnect(self) -> None:
        """Trigger the callbacks for disconnected."""
        if self._unsub_disconnect is None:
            delay: float = SET_DISCONNECTED_DELAY
            self._unsub_disconnect = async_call_later(
                self.hass, delay, self._set_disconnected
            )


@dataclass
class TuyaBLEData:
    """Data for the Tuya BLE integration."""

    title: str
    device: TuyaBLEDevice
    product: TuyaBLEProductInfo
    coordinator: TuyaBLECoordinator


@dataclass
class TuyaBLECategoryInfo:
    products: dict[str, TuyaBLEProductInfo]
    info: TuyaBLEProductInfo | None = None


devices_database: dict[str, TuyaBLECategoryInfo] = {
    "co2bj": TuyaBLECategoryInfo(
        products={
            "59s19z5m": TuyaBLEProductInfo(
                product_id="59s19z5m",
                name="CO2 Detector",
                model="Unknown",
                category="co2bj",
                platforms=["sensor"],
            ),
        },
        info=TuyaBLEProductInfo(
            product_id="co2bj-fallback",
            name="Generic CO2 Device",
            model="Unknown",
            category="co2bj",
            platforms=["sensor"],
        ),
    ),
    "ms": TuyaBLECategoryInfo(
        products={
            **dict.fromkeys(
                ["ludzroix", "isk2p555"],
                TuyaBLEProductInfo(
                    product_id="shared-ms",
                    name="Smart Lock",
                    model="Unknown",
                    category="ms",
                    platforms=["lock"],
                ),
            ),
        },
        info=TuyaBLEProductInfo(
            product_id="ms-fallback",
            name="Generic Lock",
            model="Unknown",
            category="ms",
            platforms=["lock"],
        ),
    ),
    "szjqr": TuyaBLECategoryInfo(
        products={
            "3yqdo5yt": TuyaBLEProductInfo(
                product_id="3yqdo5yt",
                name="CUBETOUCH 1s",
                model="Unknown",
                category="szjqr",
                platforms=["switch"],
                fingerbot=TuyaBLEFingerbotInfo(
                    switch=1,
                    mode=2,
                    up_position=5,
                    down_position=6,
                    hold_time=3,
                    reverse_positions=4,
                ),
            ),
            "xhf790if": TuyaBLEProductInfo(
                product_id="xhf790if",
                name="CubeTouch II",
                model="Unknown",
                category="szjqr",
                platforms=["switch"],
                fingerbot=TuyaBLEFingerbotInfo(
                    switch=1,
                    mode=2,
                    up_position=5,
                    down_position=6,
                    hold_time=3,
                    reverse_positions=4,
                ),
            ),
            **dict.fromkeys(
                ["blliqpsj", "ndvkgsrm", "yiihr7zh", "neq16kgd"],
                TuyaBLEProductInfo(
                    product_id="fingerbot-plus",
                    name="Fingerbot Plus",
                    model="Unknown",
                    category="szjqr",
                    platforms=["switch"],
                    fingerbot=TuyaBLEFingerbotInfo(
                        switch=2,
                        mode=8,
                        up_position=15,
                        down_position=9,
                        hold_time=10,
                        reverse_positions=11,
                        manual_control=17,
                        program=121,
                    ),
                ),
            ),
            **dict.fromkeys(
                ["ltak7e1p", "y6kttvd6", "yrnk7mnn", "nvr2rocq", "bnt7wajf", "rvdceqjh", "5xhbk964"],
                TuyaBLEProductInfo(
                    product_id="fingerbot",
                    name="Fingerbot",
                    model="Unknown",
                    category="szjqr",
                    platforms=["switch"],
                    fingerbot=TuyaBLEFingerbotInfo(
                        switch=2,
                        mode=8,
                        up_position=15,
                        down_position=9,
                        hold_time=10,
                        reverse_positions=11,
                        program=121,
                    ),
                ),
            ),
        },
        info=TuyaBLEProductInfo(
            product_id="szjqr-fallback",
            name="Generic Fingerbot",
            model="Unknown",
            category="szjqr",
            platforms=["switch"],
        ),
    ),
    "wk": TuyaBLECategoryInfo(
        products={
            **dict.fromkeys(
                ["drlajpqc", "nhj2j7su"],
                TuyaBLEProductInfo(
                    product_id="wk-trv",
                    name="Thermostatic Radiator Valve",
                    model="Unknown",
                    category="wk",
                    platforms=["climate"],
                ),
            ),
        },
        info=TuyaBLEProductInfo(
            product_id="wk-fallback",
            name="Generic Radiator Valve",
            model="Unknown",
            category="wk",
            platforms=["climate"],
        ),
    ),
    "wsdcg": TuyaBLECategoryInfo(
        products={
            "ojzlzzsw": TuyaBLEProductInfo(
                product_id="ojzlzzsw",
                name="Soil moisture sensor",
                model="Unknown",
                category="wsdcg",
                platforms=["sensor"],
            ),
        },
        info=TuyaBLEProductInfo(
            product_id="wsdcg-fallback",
            name="Generic Soil Sensor",
            model="Unknown",
            category="wsdcg",
            platforms=["sensor"],
        ),
    ),
    "zwjcy": TuyaBLECategoryInfo(
        products={
            "gvygg3m8": TuyaBLEProductInfo(
                product_id="gvygg3m8",
                name="Soil Moisture Sensor (SGS01)",
                model="SGS01",
                category="zwjcy",
                platforms=["sensor"],
            ),
        },
        info=TuyaBLEProductInfo(
            product_id="zwjcy-fallback",
            name="Generic Soil Sensor",
            model="Unknown",
            category="zwjcy",
            platforms=["sensor"],
        ),
    ),
    "znhsb": TuyaBLECategoryInfo(
        products={
            "cdlandip": TuyaBLEProductInfo(
                product_id="cdlandip",
                name="Smart water bottle",
                model="Unknown",
                category="znhsb",
                platforms=["sensor"],
            ),
        },
        info=TuyaBLEProductInfo(
            product_id="znhsb-fallback",
            name="Generic Water Bottle",
            model="Unknown",
            category="znhsb",
            platforms=["sensor"],
        ),
    ),
    "ggq": TuyaBLECategoryInfo(
        products={
            "6pahkcau": TuyaBLEProductInfo(
                product_id="6pahkcau",
                name="Irrigation computer",
                model="Unknown",
                category="ggq",
                platforms=["switch"],
            ),
        },
        info=TuyaBLEProductInfo(
            product_id="ggq-fallback",
            name="Generic Irrigation Computer",
            model="Unknown",
            category="ggq",
            platforms=["switch"],
        ),
    ),
}


def get_product_info_by_ids(
    category: str, product_id: str
) -> TuyaBLEProductInfo:
    category_info = devices_database.get(category)
    if category_info:
        product_info = category_info.products.get(product_id)
        if product_info:
            return product_info

        if category_info.info:
            _LOGGER.debug(
                "No exact match for %s in category %s. Using fallback.", product_id, category
            )
            return category_info.info

    _LOGGER.warning(
        "Unknown device: product_id=%s, category=%s. Using safe fallback.",
        product_id, category
    )
    return TuyaBLEProductInfo(
        product_id=product_id,
        name="Unknown Device",
        manufacturer=DEVICE_DEF_MANUFACTURER,
        category=category or "unknown",
        model="Unknown",
        platforms=["sensor"],  # Default-safe
    )


def get_short_address(address: str) -> str:
    results = address.replace("-", ":").upper().split(":")
    return f"{results[-3]}{results[-2]}{results[-1]}"[-6:]


def get_device_readable_name(discovery_info: BluetoothServiceInfoBleak) -> str:
    """Generate a human-friendly name for a discovered device."""
    short_address = get_short_address(discovery_info.address)
    name = discovery_info.device.name or "Tuya BLE"
    return f"{name} {short_address}"


def get_device_info(device: TuyaBLEDevice) -> DeviceInfo | None:
    product_info = None
    if device.category and device.product_id:
        product_info = get_product_info_by_ids(device.category, device.product_id)
    product_name: str
    if product_info:
        product_name = product_info.name
    else:
        product_name = device.name
    result = DeviceInfo(
        connections={(dr.CONNECTION_BLUETOOTH, device.address)},
        hw_version=device.hardware_version,
        identifiers={(DOMAIN, device.address)},
        manufacturer=(
            product_info.manufacturer if product_info else DEVICE_DEF_MANUFACTURER
        ),
        model=("%s (%s)")
        % (
            device.product_model or product_name,
            device.product_id,
        ),
        name=("%s %s")
        % (
            product_name,
            get_short_address(device.address),
        ),
        sw_version=("%s (protocol %s)")
        % (
            device.device_version,
            device.protocol_version,
        ),
    )
    return result
