"""Config flow for Surplife B7."""
from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from .const import DEFAULT_PORT, DOMAIN
from .protocol import read_status

class SurplifeB7ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            host = user_input["host"].strip()
            port = user_input["port"]
            await self.async_set_unique_id(f"{host}:{port}")
            self._abort_if_unique_id_configured()
            try:
                await read_status(host, port)
            except (OSError, TimeoutError, EOFError, ValueError):
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(title=f"Surplife B7 ({host})", data={"host": host, "port": port})
        return self.async_show_form(step_id="user", data_schema=vol.Schema({
            vol.Required("host", default="192.168.0.9"): str,
            vol.Required("port", default=DEFAULT_PORT): vol.All(vol.Coerce(int), vol.Range(min=1, max=65535)),
        }), errors=errors)
