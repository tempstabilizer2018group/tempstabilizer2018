Mouser-Nr.: 895-FT2232HMINIMOD
Herst.- Nr.: FT2232H MINI MODULE
CHF27
https://www.mouser.ch/datasheet/2/163/DS_FT2232H_Mini_Module-3949.pdf

--------------------------------
Multi Protocol Synchronous Serial Engine (MPSSE) is generic hardware found in several FTDI chips that allows these chips to communicate with a synchronous serial device such an I2C device, an SPI device or a JTAG device. The MPSSE is currently available on the FT2232D...

USB powered (DS_FT2232H_Mini_Module-3949.pdf, page 7)
  1) Connect VCC (5.0V): CN3.1 with CN3.3
  2) Connect VIO (3.3V): CN2.1 with CN2.11

I2C-Pins (AN_113_FTDI_Hi_Speed_USB_To_I2C_Example.pdf, page 5)
  SDA: ADBUS1(17)-ADBUS2(18)     CN2.10-CN2.9
  SCL: ADBUS0(16)                CN2.7
  GND                            CN2.6

  http://www.onsemi.com/pub/Collateral/NB3H5150MNGEVB_SCHEMATIC.PDF.PDF
    Schema:
      SDA: CN2.10-CN2.9
      SCL: CN2.7

Python
  pylibftdi 0.17.0
  pylibftdi is a minimal Pythonic interface to FTDI devices using libftdi.
  https://pypi.org/project/pylibftdi
  https://github.com/eblot/pyftdi

  pyftdi 0.29.0
  PyFtdi aims at providing a user-space driver for modern FTDI devices, implemented in pure Python language
  https://pypi.org/project/pyftdi/
  http://bitbucket.org/codedstructure/pylibftdi

  https://libusb.info
  https://www.intra2net.com/en/developer/libftdi
  https://sourceforge.net/projects/picusb/files/

----------------------------
  http://www.onsemi.com/PowerSolutions/evalBoard.do?id=NB3H5150MNGEVB
    Python-App, welche dasselbe Modul verwendet. Mit Schema!
  http://www.ftdichip.com/Support/Documents/AppNotes/AN_113_FTDI_Hi_Speed_USB_To_I2C_Example.pdf
    Sample Project with FTDI click. Including Schema.
-----------------------------
  https://www.allaboutcircuits.com/technical-articles/getting-started-with-openocd-using-ft2232h-adapter-for-swd-debugging/
  Getting Started with OPENOCD Using FT2232H Adapter for SWD Debugging
  Sehr schöne Einführung in "FT2232H MINI MODULE".
  Alibaba-Verweise "ShenZhen ShengXin ver 5.0 2017/01/01"
-----------------------------
  https://www.mikroe.com/ftdi-click
  Including Schema and Source
-------------------------------
  https://www.chd.at/sites/default/files/files/FTDI.cs
  https://www.chd.at/blog/electronic/FTDI-in-CS
  libMPSSE.dll
  Guter C# Programming-Style
-------------------------------
https://github.com/yangcol/devicedriver/blob/master/TuningChannelDriver/libMPSSE-I2C/Release-I2C/samples/I2C/sample-dynamic.c
  24LC024H http://ww1.microchip.com/downloads/en/devicedoc/22102a.pdf
  C# Code