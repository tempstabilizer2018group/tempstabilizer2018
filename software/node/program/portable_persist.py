# -*- coding: utf-8 -*-

try:
  import hw_rtc_mem
  objRtcMem = hw_rtc_mem.objRtcMem
except ModuleNotFoundError:
  class RtcMem:
    @property
    def loaded(self): return False
    def writeRtcMemDict(self, d): pass
  objRtcMem = RtcMem()
import config_app
import portable_ticks

class Persist:
  def __init__(self, strDirectory):
    self.__dictPersist = {}
    self.__bLoaded = False
    self.__strFilenameFull = '%s/%s' % (strDirectory, config_app.LOGFILENAME_PERSIST)
    if config_app.iPersistInterval_ms is None:
      self.trash()
      print(config_app.LOGFILENAME_PERSIST + ': inactiv')
      return
    self.__objInterval = portable_ticks.Interval(iInterval_ms=config_app.iPersistInterval_ms, bForceFirstTime=False)
    try:
      self.__dictPersist = objRtcMem.readRtcMemDict()
      if len(self.__dictPersist) > 0:
        # It was a warm reboot and the rtc-mem was defined
        print('Restore persist from rtc-mem!', str(self.__dictPersist))
        self.__bLoaded = True
        return
      # Fallback (common case) read from file.
      with open(self.__strFilenameFull, 'r') as fIn:
        strPersist = fIn.read()
      self.__dictPersist = eval(strPersist)
      self.__bLoaded = True
      objRtcMem.writeRtcMemDict(self.__dictPersist)
      print(config_app.LOGFILENAME_PERSIST + ': loaded')
    except:
      print(config_app.LOGFILENAME_PERSIST + ': missing')

  @property
  def loaded(self):
    return self.__bLoaded

  def trash(self):
    # Trash contents of persist.txt
    self.__dictPersist = {}
    self.__persist()
    print(config_app.LOGFILENAME_PERSIST + ': trashed')

  def setValue(self, strTag, strValue):
    self.__dictPersist[strTag] = strValue

  def getValue(self, strTag, strDefault=None):
    return self.__dictPersist.get(strTag, strDefault)

  def persist(self, bForce=False):
    if config_app.iPersistInterval_ms == None:
      return

    bIntervalOver, iDummy = self.__objInterval.isIntervalOver()
    # print('bIntervalOver', bIntervalOver)
    # print('bForce', bForce)
    if bForce or bIntervalOver:
      self.__persist()

  def __persist(self):
    objRtcMem.writeRtcMemDict(self.__dictPersist)
    try:
      with open(self.__strFilenameFull, 'w') as fOut:
        strPersist = str(self.__dictPersist)
        fOut.write(strPersist)
      print(config_app.LOGFILENAME_PERSIST + ': written')
    except Exception as e:
      print(config_app.LOGFILENAME_PERSIST + ': failed to write. ' + str(e))
