"""Home Assistant RGB light backed by the H6004 BLE protocol."""

import asyncio
import logging

from govee_ble_local import create_device

from homeassistant.components import bluetooth
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_RGB_COLOR,
    ColorMode,
    LightEntity,
)
from homeassistant.const import CONF_ADDRESS, STATE_OFF, STATE_ON
from homeassistant.core import callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.device_registry import CONNECTION_BLUETOOTH, DeviceInfo
from homeassistant.helpers.restore_state import RestoreEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([H6004Light(entry.data[CONF_ADDRESS])])


class H6004Light(LightEntity, RestoreEntity):
    _attr_should_poll = False
    _attr_has_entity_name = True
    _attr_name = None
    _attr_color_mode = ColorMode.RGB
    _attr_supported_color_modes = {ColorMode.RGB}
    _attr_is_on = None
    _attr_rgb_color = None
    _attr_brightness = None

    def __init__(self, address):
        self._address = address
        self._command_lock = asyncio.Lock()
        self._attr_unique_id = address
        self._attr_device_info = DeviceInfo(
            connections={(CONNECTION_BLUETOOTH, address)},
            name=f"Govee H6004 {address[-5:].replace(':', '')}",
            manufacturer="Govee",
            model="H6004",
        )

    @property
    def available(self):
        return bluetooth.async_address_present(
            self.hass, self._address, connectable=True
        )

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        if (last_state := await self.async_get_last_state()) is not None:
            if last_state.state in (STATE_ON, STATE_OFF):
                self._attr_is_on = last_state.state == STATE_ON
            if (rgb := last_state.attributes.get(ATTR_RGB_COLOR)) is not None:
                self._attr_rgb_color = tuple(rgb)
            self._attr_brightness = last_state.attributes.get(ATTR_BRIGHTNESS)

        @callback
        def seen(_info, _change):
            self.async_write_ha_state()

        @callback
        def unavailable(_info):
            self.async_write_ha_state()

        self.async_on_remove(
            bluetooth.async_register_callback(
                self.hass,
                seen,
                {"address": self._address, "connectable": True},
                bluetooth.BluetoothScanningMode.ACTIVE,
            )
        )
        self.async_on_remove(
            bluetooth.async_track_unavailable(
                self.hass, unavailable, self._address, connectable=True
            )
        )

    async def async_turn_on(self, **kwargs):
        await self._async_send(
            True,
            rgb=kwargs.get(ATTR_RGB_COLOR),
            brightness=kwargs.get(ATTR_BRIGHTNESS),
        )

    async def async_turn_off(self, **kwargs):
        await self._async_send(False)

    async def _async_send(self, on, rgb=None, brightness=None):
        async with self._command_lock:
            info = bluetooth.async_last_service_info(
                self.hass, self._address, connectable=True
            )
            if info is None or not self.available:
                raise HomeAssistantError(
                    f"No connectable Bluetooth source sees {self._address}."
                )

            try:
                light = create_device(info.device, "H6004", info.advertisement)
                try:
                    if on:
                        await light.turn_on()
                    else:
                        await light.turn_off()
                    self._attr_is_on = on
                    if rgb is not None:
                        await light.set_rgb(tuple(rgb))
                        self._attr_rgb_color = tuple(rgb)
                    if brightness is not None:
                        # HA uses 0–255 and handles zero as a turn-off request.
                        percent = max(1, round(brightness * 100 / 255))
                        await light.set_brightness(percent)
                        self._attr_brightness = brightness
                finally:
                    try:
                        await light.stop()
                    except Exception:
                        _LOGGER.debug("Could not close H6004 Bluetooth session", exc_info=True)
                    self.async_write_ha_state()
            except Exception as error:
                raise HomeAssistantError(
                    f"H6004 Bluetooth command failed for {self._address}: {error}"
                ) from error
