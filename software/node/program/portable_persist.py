# -*- coding: utf-8 -*-

import hw_rtc_mem
import config_app
import portable_ticks

class Persist:
  def __init__(self, strDirectory):
    self.__dictPersist = {}
    self.__bLoaded = False
    self.__strFilenameFull = '%s/%s' % (strDirectory, config_app.LOGFILENAME_PERSIST)
    if config_app.iPersistInterval_ms != None:
      self.__objInterval = portable_ticks.Interval(iInterval_ms=config_app.iPersistInterval_ms, bForceFirstTime=False)
    try:
      self.__dictPersist = hw_rtc_mem.objRtcMem.readRtcMemDict()
      if len(self.__dictPersist) > 0:
        # It was a warm reboot and the rtc-mem was defined
        print('Restore persist from rtc-mem!')
        self.__bLoaded = True
        return
      with open(self.__strFilenameFull, 'r') as fIn:
        strPersist = fIn.read()
      self.__dictPersist = eval(strPersist)
      self.__bLoaded = True
      hw_rtc_mem.objRtcMem.writeRtcMemDict(self.__dictPersist)
      print(config_app.LOGFILENAME_PERSIST + ': loaded')
    except:
      print(config_app.LOGFILENAME_PERSIST + ': missing')

  @property
  def loaded(self):
    return self.__bLoaded

  def delete(self, funcRemove):
    # Delete persist-file
    try:
      funcRemove(self.__strFilenameFull)
      print(config_app.LOGFILENAME_PERSIST + ': deleted')
    except:
      print(config_app.LOGFILENAME_PERSIST + ': not deleted (does not exist)')

  def setValue(self, strTag, strValue):
    self.__dictPersist[strTag] = strValue

  def getValue(self, strTag):
    return self.__dictPersist.get(strTag, '')

  def persist(self, bForce=False):
    if config_app.iPersistInterval_ms == None:
      return

    bIntervalOver, iDummy = self.__objInterval.isIntervalOver()
    # print('bIntervalOver', bIntervalOver)
    # print('bForce', bForce)
    if bForce or bIntervalOver:
      self.__persist()

  def __persist(self):
    hw_rtc_mem.objRtcMem.writeRtcMemDict(self.__dictPersist)
    try:
      with open(self.__strFilenameFull, 'w') as fOut:
        strPersist = str(self.__dictPersist)
        fOut.write(strPersist)
        print(config_app.LOGFILENAME_PERSIST + ': written')
    except:
        print(config_app.LOGFILENAME_PERSIST + ': failed to write')
