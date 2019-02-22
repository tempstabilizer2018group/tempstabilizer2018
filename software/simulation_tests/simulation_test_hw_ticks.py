# -*- coding: utf-8 -*-
import portable_ticks
import portable_constants

def doit(fOut):
  def write(*args):
    fOut.write('\t'.join(map(lambda v: str(v), args)))
    fOut.write('\n')

  iModuloPoll = 27
  iModuloForceReset = 551
  iForce_ms = 55
  iInterval = 300
  iMaxTicks_ms = 1000
  portable_ticks.reset()
  portable_ticks.init(iMaxTicks_ms=iMaxTicks_ms)
  iIntervalCounter = 0
  iForceCounter = None

  objInterval = portable_ticks.Interval(iInterval, bForceFirstTime=False)

  for iTime_ms in range(0, 1000*iMaxTicks_ms):
    iTicks_ms = portable_ticks.objTicks.ticks_ms()
    if (iTime_ms%iModuloPoll) == 0:
      bTrigger, iEffectiveIntervalDuration_ms = objInterval.isIntervalOver()
      write(iTime_ms, iTicks_ms, 'poll', iIntervalCounter, bTrigger, iEffectiveIntervalDuration_ms)
      if bTrigger:
        if iIntervalCounter != None:
          assert iIntervalCounter >= iInterval
          assert iIntervalCounter < iInterval + iModuloPoll

        if iForceCounter != None:
          # assert iForceCounter >= iForce_ms
          assert iForceCounter < iForce_ms + iModuloForceReset
          assert iForceCounter < iInterval + iModuloPoll

        iIntervalCounter = 0
        iForceCounter = None

    if (iTime_ms%iModuloForceReset) == 0:
      write(iTime_ms, iTicks_ms, 'forcereset', iIntervalCounter)
      objInterval.doForce(iForce_ms)
      iIntervalCounter = None
      iForceCounter = 0

    portable_ticks.objTicks.increment_ticks_ms(1)
    if iIntervalCounter != None:
      iIntervalCounter += 1
    if iForceCounter != None:
     iForceCounter += 1


if __name__ == '__main__':
  with open(__file__.replace('.py', '_tmp.txt'), 'w') as fOut:
    doit(fOut)
