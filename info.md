# Tuya BLE Local

**Secure, offline control of Tuya BLE devices—without the cloud.**

Tuya BLE Local is a next-generation Home Assistant integration for pairing and managing Tuya Bluetooth Low Energy devices locally. No app, no tokens, no cloud dependencies—just encrypted local control.

---

### 🚀 Features

- 🔐 AES-encrypted DPS decoding
- 📡 Passive BLE device detection with fingerprinting
- 📶 ESPHome BLE proxy & multi-adapter support
- 🌱 Supports sensors, switches, locks, TRVs, Fingerbots & more
- 🧠 Fallback logic for unknown devices
- ✨ Beautiful device names, icons, and HACS branding

---

### 🔧 Setup

After install, add new devices via:

**Settings → Devices & Services → Add Integration → Tuya BLE Local**

Broadcasting devices will autofill their info. Others can be added manually with `mac_address`, `product_id`, and `local_key`.

🔑 Need help finding your local key?  
See the [Local Key Guide](https://github.com/cooley420/blob/main/tuya_ble_local/wiki/Getting_Your_Local_Key.md)

---

### 📎 Requirements

- Home Assistant 2024.4.0+
- Devices must use Tuya BLE protocol and support DPS encryption

---

Together, we're building a better, local-first smart home.  
#NoCloudNoCompromise
