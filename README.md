# Govee H6004 Bluetooth for Home Assistant -- AI Generated: Do not run in prooduction

This custom integration uses Home Assistant's Bluetooth adapter or an active
Bluetooth proxy. Home Assistant installs the pinned `govee-ble-local==1.10.0`
dependency when loading it. No Raspberry Pi script, MQTT broker, or Govee
account is needed.

## Install

1. Extract this ZIP. Copy the included `custom_components/govee_h6004`
   directory into the `custom_components` directory next to your Home
   Assistant `configuration.yaml`. Create `custom_components` if needed.
   The resulting path should end in `custom_components/govee_h6004/manifest.json`.
2. Restart Home Assistant.
3. Open **Settings → Devices & services → Add integration** and search for
   **Govee H6004 Bluetooth**. The form defaults to `D0:C9:07:EC:95:85`.
   For another H6004, use its address from the Bluetooth Advertisement monitor.
4. Open the new light entity. Test on, pick red, adjust the brightness slider,
   then test off. Both controls are in the light's details.

To upgrade an existing install, overwrite the files in
`custom_components/govee_h6004` and restart Home Assistant. The existing
integration entry and light entity are reused.

The entity tracks acknowledged commands and uses the last recorded state
after restarting. Changes made outside Home Assistant do not synchronize.
The first state is unknown until you send a command. The entity needs a
connectable Bluetooth source that can hear the bulb. If it is unavailable,
check the Advertisement monitor. For a command or dependency error, check
**Settings → System → Logs** for `govee_h6004`.

To remove it, delete the integration entry and its `govee_h6004` folder,
then restart Home Assistant.
