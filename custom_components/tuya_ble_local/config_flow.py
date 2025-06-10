"""Config flow for Tuya BLE Local integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.bluetooth import BluetoothServiceInfoBleak
from homeassistant.core import callback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

def build_schema(
    mac_address: str = "",
    device_id: str = "",
    product_id: str = "",
    local_key: str = "",
    name: str = "Tuya BLE Device"
) -> vol.Schema:
    return vol.Schema({
        vol.Required("mac_address", default=mac_address): str,
        vol.Required("device_id", default=device_id): str,
        vol.Required("product_id", default=product_id): str,
        vol.Required("local_key", default=local_key): str,
        vol.Optional("name", default=name): str,
    })


class TuyaBLELocalConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Tuya BLE Local."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        if user_input:
            mac = user_input["mac_address"].lower().replace(":", "")
            await self.async_set_unique_id(mac)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=user_input["name"],
                data={
                    "mac_address": user_input["mac_address"],
                    "device_id": user_input["device_id"],
                    "product_id": user_input["product_id"],
                    "local_key": user_input["local_key"],
                },
            )

        return self.async_show_form(step_id="user", data_schema=build_schema())

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfoBleak
    ) -> config_entries.FlowResult:
        mac = discovery_info.address.lower().replace(":", "")
        name = discovery_info.name or mac
        product_id = ""

        # Attempt to extract product_id from service data
        service_data = discovery_info.service_data.get("0000a201-0000-1000-8000-00805f9b34fb")
        if service_data:
            try:
                product_id = service_data[1:].decode("utf-8", errors="ignore")
            except Exception as ex:
                _LOGGER.debug("Failed to decode product_id from service data: %s", ex)

        _LOGGER.debug("Discovered BLE device: %s (%s)", name, mac)

        await self.async_set_unique_id(mac)
        self._abort_if_unique_id_configured()

        self.context["title_placeholders"] = {"name": name}

        return self.async_show_form(
            step_id="user",
            description_placeholders={"name": name},
            data_schema=build_schema(
                mac_address=discovery_info.address,
                product_id=product_id,
                name=name,
            ),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return TuyaBLEOptionsFlow(config_entry)


class TuyaBLEOptionsFlow(config_entries.OptionsFlowWithConfigEntry):
    """Handle Tuya BLE Local options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        # Add options schema here in future if needed
        return self.async_show_form(step_id="init", data_schema=vol.Schema({}))
