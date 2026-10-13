"""Surplife B7 read-only diagnostic integration."""
from __future__ import annotations
from datetime import timedelta
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, DEFAULT_PORT
from .protocol import read_status

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    host = entry.data["host"]
    port = entry.data.get("port", DEFAULT_PORT)

    async def async_update():
        try:
            return await read_status(host, port)
        except (OSError, TimeoutError, EOFError, ValueError) as exc:
            raise UpdateFailed(f"Status query to {host}:{port} failed: {exc}") from exc

    coordinator = DataUpdateCoordinator(hass, _LOGGER, name=f"Surplife B7 {host}", update_method=async_update, update_interval=timedelta(seconds=30))
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    success = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if success:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return success
