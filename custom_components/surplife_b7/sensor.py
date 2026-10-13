"""Read-only diagnostic sensor for Surplife B7."""
from __future__ import annotations
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    async_add_entities([SurplifeB7Status(hass.data[DOMAIN][entry.entry_id], entry)])

class SurplifeB7Status(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True
    _attr_name = "Protocol response"
    _attr_icon = "mdi:lan-connect"

    def __init__(self, coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_response"
        self._attr_device_info = DeviceInfo(identifiers={(DOMAIN, entry.unique_id or entry.entry_id)}, name=entry.title, manufacturer="Surplife-compatible", model="EA-81 model B7 (experimental)")

    @property
    def native_value(self) -> str | None:
        return self.coordinator.data.signature if self.coordinator.data else None

    @property
    def extra_state_attributes(self) -> dict:
        state = self.coordinator.data
        return {
            "raw_hex": state.raw_hex,
            "raw_length": state.raw_length,
            "model_byte": f"0x{state.model_byte:02X}",
            "power_state": state.power_state,
            "candidate_brightness_percent": state.reported_level,
            "byte_15_raw": state.reported_level_hex,
            "byte_7_raw": state.mode_byte,
            "candidate_brightness_note": "Byte 15 only appears brightness-related in some modes; scene semantics unknown.",
        } if state else {}
