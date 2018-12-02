http://claytondarwin.com/projects/ESP32/MicroPython/


--------------------------------------
import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.scan()
wlan.isconnected()
wlan.connect('waffenplatzstrasse26', 'guguseli')
wlan.config('mac')
wlan.ifconfig()

import ntptime
ntptime.time()
590348250
--------------------------------------
Modules in: ~/micropython/esp32/micropython/ports/esp32/modules

https://pypi.org/project/urequests/0.1.2/
import upip
upip.install('urequests')

from upysh import *

------------------------------------
# http://docs.micropython.org/en/v1.9.3/esp8266/library/uos.html?highlight=statvfs#uos.statvfs
# https://stackoverflow.com/questions/4274899/get-actual-disk-space
import uos

uos.getcwd()
listStat = uos.statvfs('/')

print('Free %d' % (listStat[4] * listStat[1]))
print('Total %d' % (listStat[2] * listStat[1]))
print('Used %d' % ((listStat[2] - listStat[3]) * listStat[1]))


>>> print('Free %d' % (listStat[4] * listStat[1]))
Free 0
>>> print('Total %d' % (listStat[2] * listStat[1]))
Total 2072576
>>> print('Used %d' % ((listStat[2] - listStat[3]) * listStat[1]))
Used 2072576
------------------------------------
import esp
import esp32
import machine
https://boneskull.com/micropython-on-esp32-part-2/
  esp.osdebug(None)       # turn off vendor O/S debugging messages
  esp.osdebug(0)          # redirect vendor O/S debugging messages to UART(0)

machine.reset()
''.join(map(lambda c: '%02X' % c, machine.unique_id()))
''.join(['%02X'%i for i in machine.unique_id()])
'240AC4A1BB6C'

