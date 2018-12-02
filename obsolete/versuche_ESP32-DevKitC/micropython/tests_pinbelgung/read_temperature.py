import machine
import array
import time

####################################################################################
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

def oneShotNormalA(i2cAddress):
  # Start Oneshot and Shutdown afterwards
  # i2c.mem_write(REG_CONFIG_ONESHOT|REG_CONFIG_SHUTDOWN, i2cAddress>>1, REG_CONFIG)
  # i2c.writeto_mem(i2cAddress>>1, REG_CONFIG, REG_CONFIG_ONESHOT|REG_CONFIG_SHUTDOWN)
  i2c.writeto_mem(i2cAddress>>1, REG_CONFIG, array.array('b', (REG_CONFIG_ONESHOT|REG_CONFIG_SHUTDOWN,)))

def oneShotNormalB(i2cAddress):
  # read temperature (2 bytes)
  # bTemp = i2c.mem_read(2, i2cAddress>>1, REG_TEMP)
  bTemp = i2c.readfrom_mem(i2cAddress>>1, REG_TEMP, 2)
  iTemp = int((bTemp[0]<<8) | bTemp[1])
  fTemp = iTemp*64.0/TEMP_64C
  return fTemp

def oneShotNormal(i2cAddress):
  oneShotNormalA(i2cAddress)
  time.sleep(CONVERSION_TIME_MS*0.001)
  return oneShotNormalB(i2cAddress)
####################################################################################

if False:
  i2c = machine.I2C(freq=40000, scl=machine.Pin(2, machine.Pin.PULL_UP), sda=machine.Pin(15, machine.Pin.PULL_UP)) 

  fTemp = oneShotNormal(0x9E)
  print('%.3f' % fTemp)


if False:
  import machine
  i2c = machine.I2C(scl=machine.Pin(2, machine.Pin.PULL_UP), sda=machine.Pin(15, machine.Pin.PULL_UP), freq=10000)
  i2c.writeto_mem(0x9E>>1, 1, b'\x12')

  import machine
  i2c = machine.I2C(scl=machine.Pin(2, machine.Pin.PULL_UP), sda=machine.Pin(15, machine.Pin.PULL_UP), freq=100000)
  i2c.writeto_mem(0x9E>>1, 1, b'\x12')

  import machine
  i2c = machine.I2C(scl=machine.Pin(2), sda=machine.Pin(15), freq=100000)
  i2c.writeto_mem(0x9E>>1, 1, b'\x12')
  # ==> Interne Pullups haben KEINEN Einfluss!

