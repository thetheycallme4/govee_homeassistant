"""Configure a bulb by its Bluetooth address."""

import re

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_ADDRESS

from . import DOMAIN


class H6004ConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        default_address = ""
        if user_input is not None:
            default_address = user_input[CONF_ADDRESS].strip().upper()
            if re.fullmatch(r"(?:[0-9A-F]{2}:){5}[0-9A-F]{2}", default_address):
                await self.async_set_unique_id(default_address)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"Govee H6004 {default_address[-5:].replace(':', '')}",
                    data={CONF_ADDRESS: default_address},
                )
            errors[CONF_ADDRESS] = "invalid_address"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_ADDRESS, default=default_address): str}
            ),
            errors=errors,
        )
