bQuickie=False
# How the measure Setresponse
#
# Script-Duration: 2300s => 38min
#
# Prepare SDCARD
#    Copy files to sdcard:
#      boot.py
#      main.py
#    bQuickie=True: (Settle=3s, Heating=5s)
#    Eject sdcard from windows (using menue)
#    Remove sdcard
#
# Measure Setresponse
#   Insert SDCARD into pyboard
#   Unconnect and connect USB cable
#   Watch the leds:
#     orange: on during measurement
#     red: on during heating
#     blue: on during I2C communication
#   When orange is off: Remove SDCARD from pyboard.
#
#  Read results into PC
#    Insert SDCARD into PC
#    Move stepresponse_log_XX.txt to the PC
#    Eject sdcard from windows (using menue)
#    Remove sdcard
#
# Connecting pyboard to peripherals
#   PB6: SCL
#   PB7: SCA
#   PA0: Heat
#
import os
import pyb
import uos
import micropython

# A2, A1, A0
I2C_ADDRESS_A = 0x90  # 0, 0, 0
I2C_ADDRESS_B = 0x92  # 0, 0, 1
I2C_ADDRESS_C = 0x94 # 0, 1, 0
I2C_ADDRESS_D = 0x96 # 0, 1, 1
I2C_ADDRESS_E = 0x9E

REG_TEMP = 0x00
REG_CONFIG = 0x01
REG_T_HYST = 0x02
REG_T_OS = 0x03

REG_CONFIG_ONESHOT = 0b10000000
REG_CONFIG_TIMEOUT = 0b01000000
REG_CONFIG_DATAFORMAT = 0b00100000
REG_CONFIG_FAULTQUEUE = 0b00011000
REG_CONFIG_OSPOLARITY = 0b00000100
REG_CONFIG_COMPARATOR = 0b00000010
REG_CONFIG_SHUTDOWN = 0b00000001

TEMP_0C = 0x0000
TEMP_64C = 0x4000

CONVERSION_TIME_MS = 50

i2c = pyb.I2C(1, pyb.I2C.MASTER, baudrate=100000)
# i2c.scan()

def oneShotNormalA(i2cAddress):
  # Start Oneshot and Shutdown afterwards
  i2c.mem_write(REG_CONFIG_ONESHOT|REG_CONFIG_SHUTDOWN, i2cAddress>>1, REG_CONFIG)

def oneShotNormalB(i2cAddress):
  # read temperature (2 bytes)
  bTemp = i2c.mem_read(2, i2cAddress>>1, REG_TEMP)
  iTemp = int((bTemp[0]<<8) | bTemp[1])
  fTemp = iTemp*64.0/TEMP_64C
  return fTemp

def oneShotNormal(i2cAddress):
  oneShotNormalA(i2cAddress)
  pyb.delay(CONVERSION_TIME_MS)
  return oneShotNormalB(i2cAddress)

def nextFilename():
  listFiles = os.listdir()
  for i in range(100):
    strFilename = 'stepresponse_log_%02d.txt' % i
    if strFilename in listFiles:
      continue
    print('strFilename: %s\n' % strFilename)
    return strFilename
  raise Exception('nextFilename()')

# ledGreenDone = pyb.LED(1)
ledBlueI2c = pyb.LED(2)
ledOrangeWorking = pyb.LED(3)
ledRedHeat = pyb.LED(4)
gpioPower = pyb.Pin.board.A0
gpioPower.init(pyb.Pin.OUT_PP)

TIME_SETTLE_S = 300
TIME_HEAT_S = 2000
if bQuickie:
  TIME_SETTLE_S = 3
  TIME_HEAT_S = 5

def logStepresponseToFile():
  # ledGreenDone.off()
  ledBlueI2c.off()
  ledOrangeWorking.on()
  ledRedHeat.off()
  gpioPower.low()

  iTimeStart = pyb.millis()
  with open(nextFilename(), 'w') as f:
    f.write('time[s]\ttime_effective[ms]\tpower[1]\tTO[C]\tTH[C]\tTOunten[C]\n')
    for iTime_s in range(0, TIME_SETTLE_S+TIME_HEAT_S, 1):
      iTime_ms = iTime_s * 1000
      iDelay = iTime_ms-pyb.elapsed_millis(iTimeStart)
      print('iDelay: %d' % iDelay)
      if iDelay > 0:
        pyb.delay(iDelay)
      iTimeEffective_ms = pyb.elapsed_millis(iTimeStart)
      bPower = iTime_s >= TIME_SETTLE_S
      if bPower:
        ledRedHeat.on()
        gpioPower.high()
      else:
        ledRedHeat.off()
        gpioPower.low()
      ledBlueI2c.on()
      fTempA_C = oneShotNormal(I2C_ADDRESS_A)
      fTempB_C = oneShotNormal(I2C_ADDRESS_B)
      fTempE_C = oneShotNormal(I2C_ADDRESS_E)
      ledBlueI2c.off()
      strLine = '%d\t%d\t%d\t%.3f\t%.3f\t%.3f\n' % (iTime_s, iTimeEffective_ms, bPower, fTempA_C, fTempB_C, fTempE_C)
      f.write(strLine)
      print(strLine)
  # ledGreenDone.on()
  ledRedHeat.off()
  ledOrangeWorking.off()
  gpioPower.low()

logStepresponseToFile()
