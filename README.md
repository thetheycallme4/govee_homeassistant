# Govee H6004 Bluetooth for Home Assistant
This integration was made using AI. I had AI generate this integration because I could not get any existing HA integration to work with the Govee H6004 bulb. If it works, great, but keep in mind that it was created using AI.

This custom integration uses Home Assistant's Bluetooth adapter or an active
Bluetooth proxy. Home Assistant installs the pinned `govee-ble-local==1.10.0`
dependency when loading it. No Raspberry Pi script, MQTT broker, or Govee
account is needed.

## Install through Home Assistant Marketplace (2026.11 or later)

1. Publish this archive's extracted contents to a public GitHub repository.
   Place `hacs.json`, `README.md`, and `custom_components/` at its root.
2. In Home Assistant, open **Settings → Marketplace → Add from link** and
   enter the public repository URL. If prompted, select **Integration**.
3. Open the repository's Marketplace page, install, and restart Home Assistant.
4. In **Settings → Devices & services → Add integration**, select
   **Govee H6004 Bluetooth** and enter the bulb's Bluetooth address from
   the Bluetooth Advertisement monitor.

## Manual install

1. Extract this ZIP. Copy the included `custom_components/govee_h6004`
   directory into the `custom_components` directory next to your Home
   Assistant `configuration.yaml`. Create `custom_components` if needed.
   The resulting path should end in `custom_components/govee_h6004/manifest.json`.
2. Restart Home Assistant.
3. Open **Settings → Devices & services → Add integration** and search for
   **Govee H6004 Bluetooth**. Enter your bulb’s address from the Bluetooth
   Advertisement monitor.
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
