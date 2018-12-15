# Userguide for the Raspberry Pi

- Note that everything in Userguide HTTP also is valid for the Raspberry Pi.

## Stop WLAN

```bash
sudo systemctl stop hostapd
sudo systemctl start hostapd
```

## Connect to the node using RS232

```bash
sudo picocom -b 115200 /dev/ttyUSB0
```
