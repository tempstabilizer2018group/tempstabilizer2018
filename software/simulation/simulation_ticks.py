# -*- coding: utf-8 -*-
import sys
import portable_ticks

#
# We are running on Windows or Unix
#
def delay_ms(iDelay_ms):
  # Simulation: We never wait!
  pass

'''
  TICKS: a unsigned integer which overflows. The methods ticks_add() and ticks_diff() must be used.
  TIME: a unsigned integer or float which does NOT overlow.
    Time-Methods only exist on the simulator. The hardware only knows portable_ticks. The server then must count the overflows.
'''
class Ticks:
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
    for strTag in sorted(portable_ticks.dictCounter.keys()):
      fOut.write('Counter %8d: %s\n' % (portable_ticks.dictCounter[strTag], strTag))

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
