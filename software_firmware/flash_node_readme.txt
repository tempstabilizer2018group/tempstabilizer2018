This is how to flash
--------------------
https://micropython.org/download#esp32

Preparation
-----------
pip install esptool

Erase and Flash
---------------
run flash_node.cmd

Hints
-----
When the script produces this output:
  Connecting........_____....._____....._____....._____....._____....._____....._____
  A fatal error occurred: Failed to connect to ESP32: Timed out waiting for packet header

This may have to do with same resitors on the node which need a correct value.
Somewhere this must be documented in this repository...
