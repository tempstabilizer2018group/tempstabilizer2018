# -*- coding: utf-8 -*-
import sys
import config_app
'''
  TICKS: a unsigned integer which overflows. The methods ticks_add() and ticks_diff() must be used.
  TIME: a unsigned integer or float which does NOT overlow.
    Time-Methods only exist on the simulator. The hardware only knows portable_ticks. The server then must count the overflows.
'''

class I2cException(Exception): pass

dictCounter = {}

if config_app.bRunStatisticsCounter:
  def count(strTag):
    iCount = dictCounter.get(strTag, 0)
    dictCounter[strTag] = iCount+1
else:
  def count(strTag):
    pass

objTicks = None

if sys.platform == 'esp32':
  #
  # We are running on the hardware
  #

  import utime
  import machine

  import hw_hal

  def delay_ms(iDelay_ms):
    if config_app.bHwDoLightSleep:
      hw_hal.pin_gpio5.value(True)
      machine.sleep(iDelay_ms)
      hw_hal.pin_gpio5.value(False)
      return
    utime.sleep_ms(iDelay_ms)

  def init(iMaxTicks_ms=20000):
    global objTicks
    assert objTicks == None
    objTicks = TicksHw()

  class TicksHw:
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

else:
  #
  # We are running on Windows or Unix
  #
  def delay_ms(iDelay_ms):
    # Simulation: We never wait!
    pass

  # def init(iMaxTicks_ms=1000000000):
  def init(iMaxTicks_ms):
    global objTicks
    assert objTicks == None
    objTicks = TicksSimuliert(iMaxTicks_ms)

  def reset():
    global objTicks
    objTicks = None

  class TicksSimuliert:
    def __init__(self, iMaxTicks_ms):
      assert type(iMaxTicks_ms) == type(0)
      assert iMaxTicks_ms > 0
      self.__iMaxTicks_ms = iMaxTicks_ms
      self.__iTime_ms = 0
      self.__iStatisticsMaxDiff = 0
      self.__iStatisticsMaxAdd = 0
      self.__iStatisticsOverflows = 0
      self.__iStatisticsAddOverflows = 0
      self.__iStatisticsDiffUnderflows = 0

    @property
    def iMaxTicks_ms(self):
      return self.__iMaxTicks_ms

    def statistics(self):
      return 'Statistics TicksSimuliert: MaxTick %d, Overflows %d, AddOverflows %d, DiffUnderflows %d, MaxDiff %d, MaxAdd %d\n' % (self.__iMaxTicks_ms, self.__iStatisticsOverflows, self.__iStatisticsAddOverflows, self.__iStatisticsDiffUnderflows, self.__iStatisticsMaxDiff, self.__iStatisticsMaxAdd)

    def print_statistics(self, fOut=sys.stdout):
      fOut.write(self.statistics())
      for strTag in sorted(dictCounter.keys()):
        fOut.write('Counter %8d: %s\n' % (dictCounter[strTag], strTag))

    def ticks_ms(self):
      '''
      See: https://docs.micropython.org/en/latest/pyboard/library/utime.html
      '''
      return self.__iTime_ms

    def time_ms(self):
      return self.__iStatisticsOverflows * self.__iMaxTicks_ms + self.__iTime_ms

    def ticks_add(self, portable_ticks, delta):
      '''
      See: https://docs.micropython.org/en/latest/pyboard/library/utime.html
      '''
      assert abs(delta) < self.__iMaxTicks_ms
      self.__iStatisticsMaxAdd = max(self.__iStatisticsMaxAdd, delta)
      ticks_add = portable_ticks + delta
      if ticks_add < 0:
        ticks_add += self.__iMaxTicks_ms
        self.__iStatisticsDiffUnderflows += 1
        return ticks_add
      bOverflow, iTicks_ms = self.__do_overflow(ticks_add)
      if bOverflow:
        self.__iStatisticsAddOverflows += 1
      return iTicks_ms

    def ticks_diff(self, ticks1, ticks2):
      '''
      See: https://docs.micropython.org/en/latest/pyboard/library/utime.html
      '''
      assert abs(ticks2) < self.__iMaxTicks_ms
      iDiff_ms = ticks1 - ticks2
      self.__iStatisticsMaxDiff = max(iDiff_ms, self.__iStatisticsMaxDiff)
      if iDiff_ms < 0:
        iDiff_ms += self.__iMaxTicks_ms
        self.__iStatisticsDiffUnderflows += 1
      assert iDiff_ms >= 0
      assert iDiff_ms < self.__iMaxTicks_ms
      return iDiff_ms

    def set_ticks_ms_obsolete(self, portable_ticks):
      self.__iTime_ms = portable_ticks

    def increment_ticks_ms(self, portable_ticks):
      self.__iTime_ms += portable_ticks

      bOverflow, self.__iTime_ms = self.__do_overflow(self.__iTime_ms)
      if bOverflow:
        self.__iStatisticsOverflows += 1

    def __do_overflow(self, portable_ticks):
      bOverflow = portable_ticks >= self.__iMaxTicks_ms
      if bOverflow:
        portable_ticks -= self.__iMaxTicks_ms
      assert portable_ticks >= 0
      assert portable_ticks < self.__iMaxTicks_ms
      return bOverflow, portable_ticks

    def sleep_ms(self, ms):
      pass

class Interval:
  '''
    This class eases the triggering of a interval for example every 2s.
    Every 2s, isIntervalOver() will return True and the exact duration will be returned.
    doForce() may be forced next isIntervalOver() to trigger.
  '''
  def __init__(self, iInterval_ms, bForceFirstTime=True):
    self.__iLastTicksEff_ms = self.__iLastTicks_ms = objTicks.ticks_ms()
    self.__iInterval_ms = iInterval_ms
    if bForceFirstTime:
      self.doForce()

  def doForce(self, iNextIriggerIn_ms=0):
    '''
      isIntervalOver() will be triggered in 'iNextTriggerIn_ms'.
    '''
    iTicksNow_ms = objTicks.ticks_ms()
    iLastTicks_ms = objTicks.ticks_add(iTicksNow_ms, iNextIriggerIn_ms-self.__iInterval_ms)
    iDiff = objTicks.ticks_diff(iLastTicks_ms, self.__iLastTicks_ms)
    if iDiff < 0:
      # Only apply the force trigger if it arrives earlier than the interval trigger!
      self.__iLastTicks_ms = iLastTicks_ms

  def iTimeElapsed_ms(self, iTicksNow_ms):
    '''
      Returns the time already spent in this interval
    '''
    return objTicks.ticks_diff(iTicksNow_ms, self.__iLastTicksEff_ms)

  def isIntervalOver(self):
    '''
      return bIntervalOver, iEffectiveIntervalDuration_ms
      bIntervalOver == True: If the interval has finished
      iEffectiveIntervalDuration_ms: The time of the last interval
    '''
    iTicksNow_ms = objTicks.ticks_ms()
    iIntervalDurationEff_ms = self.iTimeElapsed_ms(iTicksNow_ms)
    iIntervalDuration_ms = objTicks.ticks_diff(iTicksNow_ms, self.__iLastTicks_ms)
    assert iIntervalDurationEff_ms >= 0
    assert iIntervalDuration_ms >= 0
    if iIntervalDuration_ms >= self.__iInterval_ms:
      self.__iLastTicksEff_ms = self.__iLastTicks_ms = iTicksNow_ms
      # Triggered
      return True, iIntervalDurationEff_ms
    # We still have to wait for the interval to finish
    return False, 0



bDoStopwatch = False

def stopwatch():
  pass

def stopwatch_end(iTickStart_us, strName):
  pass

listStopwatch = []

def enableStopwatch():
  '''
    This method will be called when 'bRunStopwatch=True'.
    The stopwatch-functions will be replaced by the real functions.
  '''
  global stopwatch
  global stopwatch_end
  def stopwatch():
    return utime.ticks_us()

  def stopwatch_end(iTickStart_us, strName):
    global listStopwatch
    if bDoStopwatch:
      iStopwatch_us = objTicks.ticks_diff(utime.ticks_us(), iTickStart_us)
      listStopwatch.append((iStopwatch_us, strName))
      return
    if len(listStopwatch) > 0:
      for s in listStopwatch:
        print('  Stopwatch %5d us: %s' % s)
      listStopwatch = []


if __name__ == "__main__":
  def test():
    """
    >>> init(1000)
    >>> objTicks.ticks_ms()
    """
    pass

  # import doctest
  # doctest.testmod()

  init(1000)
  iTicks_ms = objTicks.ticks_ms()
  assert iTicks_ms == 0
  iTimePast_ms = 10
  iTicksPast_ms = objTicks.ticks_add(iTicks_ms, -iTimePast_ms)
  assert iTicksPast_ms == 990
  iTicksDiff_ms = objTicks.ticks_diff(iTicks_ms, iTicksPast_ms)
  assert iTicksDiff_ms == 10
