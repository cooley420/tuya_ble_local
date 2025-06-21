"""Config flow for Tuya BLE Local integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.bluetooth import BluetoothServiceInfoBleak
from homeassistant.core import callback
from homeassistant.const import CONF_ADDRESS, CONF_NAME
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

def build_schema(
    mac_address: str = "",
    device_id: str = "",
    product_id: str = "",
    local_key: str = "",
    name: str = "Tuya BLE Device"
) -> vol.Schema:
    _LOGGER.debug(
        "🔧 build_schema called with → mac_address=%s, device_id=%s, product_id=%s, local_key=%s, name=%s",
        mac_address,
        device_id,
        product_id,
        local_key,
        name,
    )

    return vol.Schema({
        vol.Required(CONF_ADDRESS, default=mac_address or ""): str,
        vol.Optional("device_id", default=device_id or ""): str,
        vol.Optional("product_id", default=product_id or ""): str,
        vol.Optional("local_key", default=local_key or ""): str,
        vol.Optional("name", default=name or "Tuya BLE Device"): str,
    }, extra=vol.ALLOW_EXTRA)

class TuyaBLELocalConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Tuya BLE Local."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        if user_input:
            _LOGGER.debug("async_step_user received: %s", user_input)

            # Normalize input: allow "address" or "mac_address" to fill CONF_ADDRESS
            if "address" in user_input and CONF_ADDRESS not in user_input:
                user_input[CONF_ADDRESS] = user_input.pop("address")
            if "mac_address" in user_input and CONF_ADDRESS not in user_input:
                user_input[CONF_ADDRESS] = user_input.pop("mac_address")

            # Hard fail if still missing MAC
            if CONF_ADDRESS not in user_input:
                _LOGGER.error("No MAC address found in user_input. Aborting.")
                return self.async_abort(reason="invalid_address")

            # Normalize MAC (no colons, lowercase)
            user_input[CONF_ADDRESS] = user_input[CONF_ADDRESS].lower().replace(":", "")
            mac = user_input[CONF_ADDRESS]
            await self.async_set_unique_id(mac)
            self._abort_if_unique_id_configured()

            user_input[CONF_NAME] = user_input.get(CONF_NAME) or "Tuya BLE Device"

            return self.async_create_entry(
                title=user_input.get(CONF_NAME, "Tuya BLE Device"),
                data={
                    CONF_ADDRESS: user_input.get(CONF_ADDRESS, ""),
                    "device_id": user_input.get("device_id", ""),
                    "product_id": user_input.get("product_id", ""),
                    "local_key": user_input.get("local_key", ""),
                },
            )

        _LOGGER.debug("Showing user form with default schema")
        _LOGGER.debug("🧪 Default discovery fallback: %s", getattr(self, "_discovery_defaults", "NOT SET"))

        def colonify_mac(address: str) -> str:
            return ":".join(address[i:i+2] for i in range(0, 12, 2)).upper()

        defaults = getattr(self, "_discovery_defaults", {})
        mac_raw = defaults.get("mac_address", "")
        colon_mac = colonify_mac(mac_raw) if mac_raw else ""

        return self.async_show_form(
            step_id="user",
            data_schema=build_schema(
                mac_address=colon_mac,
                device_id=defaults.get("device_id", ""),
                product_id=defaults.get("product_id", ""),
                local_key=defaults.get("local_key", ""),
                name=defaults.get("name", "Tuya BLE Device"),
            ),
        )

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfoBleak
    ) -> config_entries.FlowResult:
        mac_address = discovery_info.address.lower().replace(":", "")
        name = discovery_info.name or mac_address
        product_id = ""

        _LOGGER.debug("BLE discovery → MAC: %s, Name: %s", mac_address, name)

        for flow in self._async_in_progress():
            if flow["context"].get("unique_id") == mac_address:
                _LOGGER.debug("Duplicate discovery for %s ignored: flow already in progress", mac_address)
                return self.async_abort(reason="already_in_progress")

        service_data = discovery_info.service_data.get("0000a201-0000-1000-8000-00805f9b34fb")
        if service_data:
            try:
                product_id = service_data[1:].decode("utf-8", errors="ignore").strip("\x00").strip()
            except Exception as ex:
                _LOGGER.debug("Failed to decode product_id from service data: %s", ex)

        device_title = f"TY({product_id})" if product_id else name
        _LOGGER.debug("Discovered BLE device: %s (%s)", device_title, mac_address)

        await self.async_set_unique_id(mac_address)
        self._abort_if_unique_id_configured()

        self.context["title_placeholders"] = {"name": device_title}
        self._discovery_defaults = {
            "mac_address": mac_address,
            "device_id": "",
            "product_id": product_id,
            "local_key": "",
            "name": device_title,
        }

        return await self.async_step_user()

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return TuyaBLEOptionsFlow(config_entry)

class TuyaBLEOptionsFlow(config_entries.OptionsFlow):
    """Handle Tuya BLE Local options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        return self.async_show_form(step_id="init", data_schema=vol.Schema({}))
