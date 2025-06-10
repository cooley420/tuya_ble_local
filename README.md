🌐 Tuya BLE Local — Offline Smart Control, Reinvented


Overview
-----------

Tuya BLE Local is a fully offline Home Assistant integration that enables encrypted control of Tuya Bluetooth Low Energy devices—without the Tuya app, cloud pairing, or developer account.

This is a next-gen rewrite of ha_tuya_ble, rebuilt from the ground up to support:

🔐 AES-encrypted DPS decoding

💡 BLE service data parsing

📡 Multi-adapter and ESPHome BLE proxy support

📱 BLE fingerprinting by mac_address, product_id, and local_key

No Tuya tokens. No account. No internet. Just rock-solid local control.

---


🔧 Features
---------------

✅ 100% offline BLE pairing and communication 

🔒 Encrypted AES key handshake using your device’s local_key 

🧬 Decodes DPS payloads for sensor, switch, climate, lock, and Fingerbot devices 

📶 Native BLE signal strength and passive polling 

🛰️ Multi-adapter + ESPHome BLE proxy compatibility 

🧠 Flexible fallback logic for unknown product types 

💥 BLE event support (fingerbot_button_pressed) 

📊 Local-only sensors with auto-created device entities 

🎨 Polished device names, icons, and translation strings 

📁 HACS-friendly branding, docs, and config

---


📦 Installation
-----------------

Option 1: HACS (Recommended)

1. Open Home Assistant → HACS → Integrations

2. Click “+” and select Custom repositories

3. Enter: https://github.com/cooley420/tuya_ble_local

4. Select category Integration, click Add

5. Install Tuya BLE Local, then restart Home Assistant


Option 2: Manual

Place the `tuya_ble_local` folder inside your `custom_components/` directory:

config/
└── custom_components/
    └── tuya_ble_local/

Then restart Home Assistant.

---


🚀 Setup Instructions
-----------------------

1. Open Settings → Devices & Services

2. Click Add Integration → Tuya BLE Local

3. If your device is broadcasting, Bluetooth discovery will pre-fill:

 - mac_address

 - product_id

 - device name

If not, you can enter the details manually:

---------------------------------------------------------------------------
|       Field         |                Description                        |
---------------------------------------------------------------------------
|  MAC address        |       Bluetooth address (e.g. F4:A5:26:01:9C:3E)  |
---------------------------------------------------------------------------
|  Device ID          |      From Tuya app or tuya-cli output             |
---------------------------------------------------------------------------
|  Product ID         |      Optional, helps resolve correct DPS mappings |
---------------------------------------------------------------------------
|  Local key          |      Required. Used to decrypt communication      |
---------------------------------------------------------------------------
|  Name (optional)    |      Friendly name for the device                 |
--------------------------------------------------------------------------=

Click Submit to complete encrypted local pairing.

---


📌 Need help retrieving your local key? See the [Local Key Guide](https://github.com/cooley420/blob/main/tuya_ble_local/wiki/Getting_Your_Local_Key.md)


---


📚 Supported Devices
---------------------

This integration supports dozens of BLE-powered Tuya devices, including:

🤖 Fingerbots (Standard, Plus, CubeTouch)

🌱 Soil moisture and temperature sensors

🧊 CO₂ monitors and air quality sensors

🔒 Smart locks (BLE-only or dual-mode)

🌡️ Radiator valves and climate controllers

🚿 Irrigation systems and faucet valves

💧 Water bottles (yes, really)

See the full list in devices.py

---


🧠 Credits
------------

This integration builds on the incredible reverse engineering work of:

@PlusPlus-ua — original BLE parser and DPS decoder

@redphx — Fingerbot command mapping and security handshake details

🔧 Refactored and locally re-architected by @cooley420 to support secure, scalable BLE integrations without a single cloud call.

---


🤝 Contributing
-----------------

We welcome pull requests! You can contribute by:

Adding new device product_id mappings

Enhancing encrypted packet decoding

Improving fallback detection logic

Submitting branding, banners, or localization

Expanding the Local Key Guide

Together, we’re building a better, cloudless smart home.
