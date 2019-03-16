# -*- coding: utf-8 -*-
import gc
import sys
import utime
import machine

import hw_hal
import config_app

def delay_ms(iDelay_ms):
  if config_app.bHwDoLightSleep:
    hw_hal.pin_gpio5.value(True)
    # TODO: Do we use the correct sleep?
    machine.sleep(iDelay_ms)
    hw_hal.pin_gpio5.value(False)
    return
  # TODO: Do we use the correct sleep?
  utime.sleep_ms(iDelay_ms)

'''
  TICKS: a unsigned integer which overflows. The methods ticks_add() and ticks_diff() must be used.
  TIME: a unsigned integer or float which does NOT overlow.
    Time-Methods only exist on the simulator. The hardware only knows portable_ticks. The server then must count the overflows.
'''
class Ticks:
  def __init__(self):
    # >> '0x%X' % utime.ticks_add(0, -1)
    # 0x3FFFFFFF
    # >> '0x%X' % (2**30-1)
    # '0x3FFFFFFF'
    self.__iMaxTicks_ms = 2**30-1
    self.__iStartTicks_ms = self.ticks_ms()

  @property
  def iMaxTicks_ms(self):
    return self.__iMaxTicks_ms

  def statistics(self):
    print('TicksHw.statistics() not implemented on the hardware')

  def print_statistics(self, fOut=sys.stdout):
    for strTag in sorted(dictCounter.keys()):
      fOut.write('Counter %8d: %s\n' % (dictCounter[strTag], strTag))

  def ticks_ms(self):
    '''
    See: https://docs.micropython.org/en/latest/pyboard/library/utime.html
    '''
    return utime.ticks_ms()

  def time_ms(self):
    '''
      time_ms() is 0 at experiment start.
      It will overflow - so don't use it only for experiments
    '''
    iTime_ms = self.ticks_ms() - self.__iStartTicks_ms
    assert iTime_ms >= 0, "Overflow!"
    return iTime_ms

  def ticks_add(self, portable_ticks, delta):
    '''
    See: https://docs.micropython.org/en/latest/pyboard/library/utime.html
    '''
    return utime.ticks_add(portable_ticks, delta)

  def ticks_diff(self, ticks1, ticks2):
    '''
    See: https://docs.micropython.org/en/latest/pyboard/library/utime.html
    '''
    return utime.ticks_diff(ticks1, ticks2)

  def set_ticks_ms_obsolete(self, portable_ticks):
    print('TicksHw.set_ticks_ms() not implemented on the hardware')

  def increment_ticks_ms(self, portable_ticks):
    print('TicksHw.increment_ticks_ms() not implemented on the hardware')

  def sleep_ms(self, ms):
    '''
    See: https://docs.micropython.org/en/latest/pyboard/library/utime.html
    '''
    utime.sleep_ms(ms)
