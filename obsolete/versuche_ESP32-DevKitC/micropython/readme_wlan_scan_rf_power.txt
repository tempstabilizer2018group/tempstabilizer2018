Wird RF gesendet während WLAN-Scan?
===================================

import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.scan()

wlan.scan(scan_time_ms, channel)
wlan.scan(-200, 0)

>>> wlan.scan()
I (21470) network: event 1
[
(b'waffenplatzstrasse26', b'\xa0\xf3\xc1KIP', 6, -78, 4, False),
(b'Roks_Air_Guest', b'|\xb73\x9e3\xed', 1, -92, 3, False),
]

wlan.isconnected()
wlan.connect('waffenplatzstrasse26', 'guguseli')
wlan.config('mac')
wlan.ifconfig()


wlan.disconnect()
wlan.active(False)

wlan.connect('dymmy', 'dummy')


https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/wifi.rst

WLAN Power

https://docs.espressif.com/projects/esp-idf/en/latest/api-guides/wifi.html
https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/wifi.rst
All-Channel Foreground Passive Scan

esp_wifi_scan_start()
  https://github.com/espressif/esp-idf/issues/326
    a scan of all 11 channels takes 2.2 seconds

micropython/ports/esp32/network.c
  wifi_scan_config_t

https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/wifi/esp_wifi.html
https://github.com/espressif/esp-idf/blob/master/components/esp32/include/esp_wifi_types.h
/** @brief Parameters for an SSID scan. */
typedef struct {
    uint8_t *ssid;               /**< SSID of AP */
    uint8_t *bssid;              /**< MAC address of AP */
    uint8_t channel;             /**< channel, scan the specific channel */
    bool show_hidden;            /**< enable to scan AP whose SSID is hidden */
    wifi_scan_type_t scan_type;  /**< scan type, active or passive */
    wifi_scan_time_t scan_time;  /**< scan time per channel */
} wifi_scan_config_t;

https://github.com/espressif/esp-idf/blob/master/components/esp32/esp_err_to_name.c
  ERR_TBL_IT(ESP_ERR_INVALID_ARG),                        /*   258 0x102 Invalid argument */