# 🔑 Getting Your Tuya Local Key

To control your Tuya BLE device locally using this integration, you'll need a special key called the **local_key**. This 16-character string allows encrypted communication with the device—completely offline.

This guide explains how to safely retrieve it once and never worry about the cloud again.

---

## 🧭 What Is the Local Key?

The `local_key` is a unique secret stored on your device and Tuya's servers. It is used for AES encryption when sending commands or receiving updates from your Tuya BLE device.

Once you obtain it, **you can operate your device locally and securely, with zero cloud communication**.

---

## 🚀 How to Get Your Local Key

### Option 1: Using `tuya-cli` (Simplest & Recommended)

1. [Install Node.js](https://nodejs.org/) (if not already installed)

2. Install Tuya CLI:

   ```bash
   npm install -g @tuyapi/cli

3. Log in to your Tuya developer account (Smart Life or Tuya Smart login):
     
   Bash
   tuya-cli wizard

4. Follow the instructions to discover your devices.

5. Copy down the following from the output:

  - device_id

  - local_key

  - product_id

6. Use these values in the integration setup screen.

👉 You may need to enable “Smart Home Data API” in your Tuya IoT project, and link the correct data center region (e.g. Western Europe, US, Asia).

—--

Option 2: Using Tuya Cloudcutter (Advanced)

Cloudcutter is a popular ESP-based exploit to extract local keys from devices using OTA hijacking.

Works best on certain device firmware versions.

Requires a Linux-based environment and an ESP8266.

Visit Cloudcutter GitHub for full instructions.

—--

Option 3: Intercepting App Traffic (Forensic)
By setting up a tool like mitmproxy and spoofing TLS traffic from the Tuya mobile app, it's possible to extract keys during device onboarding. This requires:

  - An emulator or rooted phone

  - TLS interception certs

  - Debugging effort

⚠️ Not recommended unless you’re familiar with app reverse-engineering.

---

✅ Once You Have the Key
Just enter the following during integration setup:

  - mac_address: BLE device address (e.g. F4:A5:26:01:9C:3E)

  - device_id: From Tuya device listing

  - product_id: Optional, but helps with discovery

  - local_key: 16-char string like abcdef1234567890

After that, you're free to delete the Tuya app entirely.

---

🛡️ Tips

  - You only need the key once. Store it securely (e.g. in a password manager).

  - It won’t change unless the device is reset and rebound in the Tuya app.

  - This integration does not send any data to Tuya. Once paired, communication is 100% local.

---

Need help? Open an issue or reach out in Discussions — we're happy to help.


