INSTALL esptool
===============
cmd.exe (as administrator)

cd "C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\Scripts"
pip install esptool


FLASH image
===========
See: https://micropython.org/download/#esp32

cmd.exe
set PYTHONDIR="C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64"
set ESPTOOL=%PYTHONDIR%\lib\site-packages\esptool.py
set ESPCOM=COM39

cd "C:\Projekte\temp_stabilizer_2018\temp_stabilizer_2018\versuche_ESP32-DevKitC\download_micropython"

%ESPTOOL% --chip esp32 --port %ESPCOM% erase_flash
ok:
%ESPTOOL% --chip esp32 --port %ESPCOM% write_flash -z 0x1000 esp32-20180630-v1.9.4-227-gab02abe9.bin
failed:
%ESPTOOL% --chip esp32 --port %ESPCOM% write_flash -z 0x1000 esp32spiram-20180728-v1.9.4-410-g11a38d5dc.bin
%ESPTOOL% --chip esp32 --port %ESPCOM% write_flash -z 0x1000 esp32spiram-20180719-v1.9.4-383-g3ffcef8bd.bin


-----------------------------------------------
esp32spiram-20180630-v1.9.4-227-gab02abe9.bin

rst:0xc (SW_CPU_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)
configsip: 0, SPIWP:0xee
clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:2
load:0x3fff0018,len:4
load:0x3fff001c,len:4596
load:0x40078000,len:0
load:0x40078000,len:14140
entry 0x4007b288
E (251) cpu_start: Failed to init external RAM!
abort() was called at PC 0x40082e16 on core 0

Backtrace: 0x40090da3:0x3ffe3c50 0x40090dd4:0x3ffe3c70 0x40082e16:0x3ffe3c90 0x40079909:0x3ffe3cd0 0x4007b2e9:0x3ffe3d10 0x40007c31:0x3ffe3eb0 0x4000073d:0x3ffe3f20

Rebooting...
ets Jun  8 2016 00:22:57

rst:0xc (SW_CPU_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)

-----------------------------------------------
esp32-20180630-v1.9.4-227-gab02abe9.bin

ets Jun  8 2016 00:22:57

rst:0x1 (POWERON_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)
ets Jun  8 2016 00:22:57

rst:0x10 (RTCWDT_RTC_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)
configsip: 0, SPIWP:0xee
clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:2
load:0x3fff0018,len:4
load:0x3fff001c,len:4596
load:0x40078000,len:0
load:0x40078000,len:12768
entry 0x4007ad68
I (228) cpu_start: Pro cpu up.
I (228) cpu_start: Single core mode
I (228) heap_init: Initializing. RAM available for dynamic allocation:
I (232) heap_init: At 3FFAE6E0 len 00001920 (6 KiB): DRAM
I (238) heap_init: At 3FFC5858 len 0001A7A8 (105 KiB): DRAM
I (244) heap_init: At 3FFE0440 len 00003BC0 (14 KiB): D/IRAM
I (251) heap_init: At 3FFE4350 len 0001BCB0 (111 KiB): D/IRAM
I (257) heap_init: At 40091944 len 0000E6BC (57 KiB): IRAM
I (263) cpu_start: Pro cpu start user code
I (57) cpu_start: Starting scheduler on PRO CPU.
OSError: [Errno 2] ENOENT
MicroPython v1.9.4-227-gab02abe9 on 2018-06-30; ESP32 module with ESP32
Type "help()" for more information.
>>>

-----------------------------------------------

esp32spiram-20180728-v1.9.4-410-g11a38d5dc.bin

esptool.py v2.4.1
Serial port COM39
Connecting........_
Chip is ESP32D0WDQ5 (revision 0)
Features: WiFi, BT, Dual Core
MAC: 30:ae:a4:80:55:e0
Uploading stub...
Running stub...
Stub running...
Configuring flash size...
Auto-detected Flash size: 4MB
Compressed 1108080 bytes to 678101...
Wrote 1108080 bytes (678101 compressed) at 0x00001000 in 60.1 seconds (effective 147.5 kbit/s)...
Hash of data verified.

Leaving...
Hard resetting via RTS pin...

==> Crash (failed to init external RAM)

Rebooting...
ets Jun  8 2016 00:22:57

rst:0xc (SW_CPU_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)
configsip: 0, SPIWP:0xee
clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:2
load:0x3fff0018,len:4
load:0x3fff001c,len:4596
load:0x40078000,len:0
load:0x40078000,len:14140
entry 0x4007b288
E (252) cpu_start: Failed to init external RAM!
abort() was called at PC 0x40082e2a on core 0

Backtrace: 0x40090fa3:0x3ffe3c50 0x40090fd4:0x3ffe3c70 0x40082e2a:0x3f

-----------------------------------------------
esp32spiram-20180719-v1.9.4-383-g3ffcef8bd.bin

ets Jun  8 2016 00:22:57

rst:0xc (SW_CPU_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)
configsip: 0, SPIWP:0xee
clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:2
load:0x3fff0018,len:4
load:0x3fff001c,len:4596
load:0x40078000,len:0
load:0x40078000,len:14140
entry 0x4007b288
E (252) cpu_start: Failed to init external RAM!
abort() was called at PC 0x40082e2a on core 0

Backtrace: 0x40090fa3:0x3ffe3c50 0x40090fd4:0x3ffe3c70 0x40082e2a:0x3ffe3c90 0x40079909:0x3ffe3cd0 0x4007b2e9:0x3ffe3d10 0x40007c31:0x3ffe3eb0 0x4000073d:0x3ffe3f20

Rebooting...
