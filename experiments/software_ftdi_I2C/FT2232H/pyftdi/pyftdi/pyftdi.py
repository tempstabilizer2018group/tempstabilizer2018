

# http://eblot.github.io/pyftdi/api/i2c.html

from time import sleep

port = I2cController().get_port(0x56)

# emit a START sequence is read address, but read no data and keep the bus
# busy
port.read(0, relax=False)

# wait for ~1ms
sleep(0.001)

# write 4 bytes, without neither emitting the start or stop sequence
port.write(b'\x00\x01', relax=False, start=False)

# read 4 bytes, without emitting the start sequence, and release the bus
port.read(4, start=False)
