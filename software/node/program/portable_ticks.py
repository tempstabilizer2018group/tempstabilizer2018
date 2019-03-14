# -*- coding: utf-8 -*-
import config_app

try:
  import hw_ticks as portable_ticks
  import gc
  import utime
  import hw_hal
  import hw_utils
  import machine
  funcMemfree = gc.mem_free
  funcCollect = gc.collect
  funcMemUsage = hw_utils.print_mem_usage

  def delay_ms(iDelay_ms):
    if config_app.bHwDoLightSleep:
      hw_hal.pin_gpio5.value(True)
      # TODO: Do we use the correct sleep?
      machine.sleep(iDelay_ms)
      hw_hal.pin_gpio5.value(False)
      return
    # TODO: Do we use the correct sleep?
    utime.sleep_ms(iDelay_ms)

except ImportError:
  import simulation_ticks as portable_ticks

  funcMemfree = lambda: 1
  funcCollect = lambda: None
  funcMemUsage = lambda: None

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

def init(iMaxTicks_ms=20000):
  global objTicks
  assert objTicks == None
  objTicks = portable_ticks.Ticks()

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

