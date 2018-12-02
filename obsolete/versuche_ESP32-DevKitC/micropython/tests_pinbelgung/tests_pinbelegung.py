import machine
import time
import read_temperature

# Taster
pin_taster = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
# hv_ok
pin_hv_ok = machine.Pin(17, machine.Pin.IN)
# zero_heat
pin_zero_heat = machine.Pin(21, machine.Pin.IN)
# LED
pin_led = machine.Pin(22, machine.Pin.OUT)

# KO
pin_gpio5 = machine.Pin(5, machine.Pin.OUT)
pin_gpio18 = machine.Pin(18, machine.Pin.OUT)
pin_gpio19 = machine.Pin(19, machine.Pin.OUT)

pin_sda = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP) 
pin_scl = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
read_temperature.i2c = machine.I2C(freq=40000, scl=pin_scl, sda=pin_sda) 

def tasterInterrupt(p):
  print('tasterInterrupt:', p.value())

pin_taster.irq(trigger=machine.Pin.IRQ_FALLING, handler=tasterInterrupt)

i = 0
while True:
  i += 1
  if pin_taster.value() == 1:
    print('Taster')
  if pin_hv_ok.value() == 1:
    print('         hv_ok')
  if pin_zero_heat.value() == 1:
    print('                 zero_heat')
  pin_gpio18.value(i % 2)
  pin_gpio19.value(i % 3)
  pin_led.value(i % 5)

  fTemp = read_temperature.oneShotNormal(0x9E)
  print('%.3f' % fTemp)

  pin_gpio5.value(0)

  if False:
    fTemp = oneShotNormal(I2C_ADDRESS_A)
    print('%.3f' % fTemp)

  time.sleep(0.01)
  pin_gpio5.value(1)
  machine.sleep(100)

  # break
