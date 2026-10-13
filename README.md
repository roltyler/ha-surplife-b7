# Surplife B7 Diagnostics for Home Assistant

Experimental, **read-only** Home Assistant custom integration for Surplife-compatible LED controllers that return a 27-byte `EA-81` frame containing model byte `B7`.

**Status:** v0.1.0 diagnostic prototype. Not yet validated running in Home Assistant. This does **not** provide a light entity or control on/off, colours, or brightness.

## Install using HACS

1. In **HACS**, open the three-dot menu and choose **Custom repositories**.
2. Add `https://github.com/roltyler/ha-surplife-b7` with category **Integration**.
3. Search for **Surplife B7 Diagnostics** and choose **Download**.
4. Restart Home Assistant.
5. Go to **Settings → Devices & Services → Add Integration → Surplife B7 Diagnostics**.
6. Enter your controller IP (the original Formby's controller is `192.168.0.9`) and port `5577`.
7. Check the **Protocol response** sensor; its `raw_hex`, `raw_length`, and `model_byte` attributes show the response.

You can leave the existing **Magic Home** integration in place; this integration uses a separate domain (`surplife_b7`). If both connect to the same controller, disable the failing Magic Home entry during diagnostics to reduce competing requests.

## What it does

- Queries TCP port 5577 with the observed, non-mutating request `81 8A 8B 96` every 30 seconds.
- Accepts a 27-byte response beginning with `EA 81` and reporting `B7` at byte offset four.
- Reports the unmodified frame as diagnostic sensor attributes.

Observed example:

```text
EA-81-02-00-B7-0B-23-25-65-50-F0-B4-64-64-FF-00-1E-00-3D-00-00-00-20-01-00-00-05
```

**Limitations:** The meanings of the B7 model's brightness, power, RGB and RGBIC effect fields have not been verified. This first release deliberately sends no lighting-control commands. TCP frame structure and model position were inferred from one observed controller and may differ on other firmware. Compatibility with other devices is unproven.

## Next development step

Validate the sensor in Home Assistant, then investigate B7 control commands using deliberate tests outside business hours. Avoid assuming the existing B6 protocol mappings work for B7.

## Credits

Protocol investigation informed by [lightinglibs/flux_led](https://github.com/lightinglibs/flux_led); no upstream source code is bundled.
