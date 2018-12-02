
import machine
import mcp4725

pin_sda = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP) 
pin_scl = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
i2c = machine.I2C(freq=1000000, scl=pin_scl, sda=pin_sda) 


#create the MCP4725 driver
dac = mcp4725.MCP4725(i2c, mcp4725.BUS_ADDRESS[0])

# 0 V
dac.write(0x0000)
# 1 V
dac.write(0x0480)
# 3.01
dac.write(0x0FFF)

# Nach Poweron: 0V
dac.config(power_down='Off' ,value=0x0000, eeprom=True)
