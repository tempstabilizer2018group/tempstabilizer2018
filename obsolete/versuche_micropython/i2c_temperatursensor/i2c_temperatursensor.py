
import os
import pyb
import micropython

# A2, A1, A0
I2C_ADDRESS_A = 0x90  # 0, 0, 0
I2C_ADDRESS_B = 0x92  # 0, 0, 1
I2C_ADDRESS_C = 0x94 # 0, 1, 0
I2C_ADDRESS_D = 0x96 # 0, 1, 1

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

switch = pyb.Switch()

i2c = pyb.I2C(1, pyb.I2C.MASTER, baudrate=100000)
i2c.scan()

# def oneShotExtended():
#   # Start Oneshot
#   i2c.mem_write(REG_CONFIG_ONESHOT | REG_CONFIG_DATAFORMAT, I2C_ADDRESS_A, REG_CONFIG)
#   # read temperature (2 bytes)
#   bTemp = i2c.mem_read(2, I2C_ADDRESS_A, REG_TEMP)
#   # Shutdown
#   i2c.mem_write(REG_CONFIG_SHUTDOWN, I2C_ADDRESS_A, REG_CONFIG)
#   iTemp = int((bTemp[0]<<8) | bTemp[1])
#   fTemp = iTemp*64.0/TEMP_64C
#   return bTemp

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

# oneShotNormal(I2C_ADDRESS_A)

def logToFile(listAddresses, filename='temperature_log.txt'):
  with open(filename, 'w') as f:
    f.write('time[ms]\t%s\n' % '\t'.join(['0x%04x' % addr for addr in listAddresses]))
    while not switch.value():
      [oneShotNormalA(addr) for addr in listAddresses]
      pyb.delay(CONVERSION_TIME_MS)
      listTemperatures = [oneShotNormalB(addr) for addr in listAddresses]
      strLine = '%d\t%s' % (pyb.millis(), '\t'.join(['%.3f' % fTemp for fTemp in listTemperatures]))
      print(strLine)
      f.write(strLine + '\n')
      pyb.delay(500-pyb.millis()%500)
      # os.sync()

logToFile((I2C_ADDRESS_A, I2C_ADDRESS_B, I2C_ADDRESS_C, I2C_ADDRESS_D))
