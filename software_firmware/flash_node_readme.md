# This is how to flash

https://micropython.org/download#esp32

Execute these commands on the pi as user pi


## Erase

python3 -m esptool --chip esp32 --port /dev/ttyUSB0 --baud 460800 erase_flash

## Flash

python3 -m esptool --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z --flash_mode dio --flash_freq 40m 0x1000 firmware/firmware_tempstab1.0.1.bin


## Hints

When the script produces this output:
  Connecting........_____....._____....._____....._____....._____....._____....._____
  A fatal error occurred: Failed to connect to ESP32: Timed out waiting for packet header

This may have to do with same resitors on the node which need a correct value.
Somewhere this must be documented in this repository...
