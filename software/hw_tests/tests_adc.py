#
# Copy and paste the code below into REPL
#
import machine
import hw_mcp3021

pin_sda = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP) 
pin_scl = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
i2c = machine.I2C(freq=1000000, scl=pin_scl, sda=pin_sda) 


adc = hw_mcp3021.MCP3021(i2c)

while True:
  print('readRaw: %d, readV: %0.3f' % (adc.readRaw(), adc.readV()))

