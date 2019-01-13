import machine

# Taster
pin_taster = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)

i = 0
def callback(p):
  global i
  i += 1
  print('taster', p.value(), i)

pin_taster.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=callback)

machine.sleep(10000)
