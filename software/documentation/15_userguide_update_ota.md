# Userguide: Software Update

## Step 1: Hotspot
Setup Hotspot
- SID: TempSabilizer2018
- PW: wmm_enabled
- WPA PSK
- Channel 6

## Step 2: Format Filesystem

- Power down
- Press button
- Power on
- Wait till led flasheds
  - The filesystem is now formated
- Release button

## Step 3: Update software

If the filesystem is empty, a software update will be started.

- Place the Raspberry Pi in WLAN-reach
- Raspberry Pi: Start the update-server
- You may want to observer the update
  - Raspberry Pi: tail -f '/home/pi/tempstabilizer2018/software/http_server/node_data/apache_logs/access.log'
  - Observe the ESP32-RS232-Output
  - Observe the events on Grafana
  - Observe the update-page on the webserver
- Power on the temp_stabilizer_2018
  - The temp_stabilizer_2018 will start the software-update
