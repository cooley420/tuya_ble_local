# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog],
and this project adheres to [Semantic Versioning].

## [0.1.0] - 2023-04-22

- Initial release


## [0.1.1] - 2023-04-26

### Added

- Added new product_id for Fingerbot Plus (#1)

### Fixed

- Fixed problem in options flow.

### Changed

- Updated strings.json


## [0.1.2] - 2023-04-26

### Changed

- Changed a way to obtain device credentials from Tuya IOT cloud, possible fix to (#2)

## [0.1.4] - 2023-04-30

### Added

- Added support of CUBETOUCH 1s, thanks @damiano75
- Added new product_ids for Fingerbot.
- Added new product_ids for Fingerbot Plus.
- First attempt to support Smart Lock device.

### Fixed

- Fixed possible disconnect of BLE device.

## [0.1.5] - 2023-06-01

### Added

- Added new product_ids for Fingerbot.
- Added event "fingerbot_button_pressed" which is fired on Fingerbot Plus touch button press.
- First attempt to add support of climate entity.

## [0.1.6] - 2023-06-01

### Added

- Added new product_ids for Fingerbot and Fingerbot Plus.

### Changed

- Updated sources to conform Python 3.11

## [0.1.7] - 2023-06-01

### Added

- Added new product_ids.
- Added full support of BLE TRV provided by @forabi
- Added support of programming mode for Fingerbot Plus, thanks @redphx for information.

### Changed

- Improved connection stability.

## [0.1.8] - 2023-07-09

### Added

- Added support of 'Irrigation computer', thanks to @SanMiggel.
- Added new product_ids for Smart locks, thanks to @drewpo28.

### Changed

- Connection to the device is postponed now. Previously some out of range device might prevents HA from fully booting.
- Improved connection stability.

## [0.2.0] - 2025-06-10

### Added

Refactored BLE packet handler with:

CRC16 validation

Fragment reassembly

Secure AES handshake and retry logic

Bluetooth discovery via async_step_bluetooth with automatic mac_address and product_id detection

DPS support for new Fingerbot features: programming state, idle positions, touch events

BLE signal strength sensor, battery enums, and icon switching based on enum value

Brandable .github/branding/ folder with polished icons, logos, and HACS banners

hacs.json metadata with discovery filters, iot_class: local_push, and description

Support for ESPHome BLE proxies and multi-adapter environments

### Changed

# Architecture

Replaced Tuya cloud auth with pure local key + DPS decoding for secure offline control

Hardened BLE communication stack (tuya_ble.py) with full disconnect handling, packet flow separation, and protocol versioning

Refactored datapoint parsing and dispatch into modular handlers

Restructured __init__.py, exceptions.py, and all platform files for modular, testable design

# UX & Platform

Unified device mappings and product metadata in devices.py for scalable, category-aware behavior

Rebuilt config_flow.py with manual setup and BLE discovery fallback

Refined entity update logic with flexible enum/icon mapping, signal strength support, and dynamic availability checks

Full codebase upgraded to align with Python 3.11+ best practices

All logging, error handling, and user-facing strings updated for clarity

# Removed

All cloud logic: token auth, Tuya IoT API calls, legacy polling or fallback mechanisms

Credential fetching via manager.py, cloud.py, and Tuya-linked config entries

# Breaking Changes

Old config entries that relied on Tuya cloud integration are not compatible

Devices must be re-added via the new config flow using their device_id, product_id, and local_key

See the [Local Key Guide](https://github.com/cooley420/tuya_ble_local/wiki/Getting-Your-Local-Key)

You can safely uninstall the official Tuya integration—this version is fully local and does not depend on the cloud
