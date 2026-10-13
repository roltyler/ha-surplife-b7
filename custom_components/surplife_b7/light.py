"""On/off-only light entity for confirmed Surplife B7 commands."""
from __future__ import annotations
from homeassistant.components.light import LightEntity, ColorMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.exceptions import HomeAssistantError
from .const import DOMAIN, DEFAULT_PORT
from .protocol import write_power

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    async_add_entities([SurplifeB7Light(hass.data[DOMAIN][entry.entry_id], entry)])

class SurplifeB7Light(CoordinatorEntity, LightEntity):
    _attr_has_entity_name = True
    _attr_name = "Light"
    _attr_icon = "mdi:lightbulb"
    _attr_supported_color_modes = {ColorMode.ONOFF}
    _attr_color_mode = ColorMode.ONOFF

    def __init__(self, coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._host = entry.data["host"]
        self._port = entry.data.get("port", DEFAULT_PORT)
        self._attr_unique_id = f"{entry.entry_id}_light"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.unique_id or entry.entry_id)},
            name=entry.title,
            manufacturer="Surplife-compatible",
            model="EA-81 model B7 (experimental)"
        )

    @property
    def is_on(self) -> bool | None:
        if not self.coordinator.data:
            return None
        value = self.coordinator.data.power_state
        return {"on": True, "off": False}.get(value)

    async def async_turn_on(self, **kwargs) -> None:
        await self._set_power(True)

    async def async_turn_off(self, **kwargs) -> None:
        await self._set_power(False)

    async def _set_power(self, on: bool) -> None:
        try:
            await write_power(self._host, self._port, on)
            await self.coordinator.async_request_refresh()
        except (OSError, TimeoutError, EOFError, ValueError) as exc:
            raise HomeAssistantError(f"Failed to control Surplife B7 at {self._host}: {exc}") from exc
