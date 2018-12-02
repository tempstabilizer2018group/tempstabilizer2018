# -*- coding: utf-8 -*-

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
      with open(self.__strFilenameFull, 'r') as fIn:
        strPersist = fIn.read()
        self.__dictPersist = eval(strPersist)
        self.__bLoaded = True
      print(config_app.LOGFILENAME_PERSIST + ': loaded')
    except:
      print(config_app.LOGFILENAME_PERSIST + ': missing')
      pass

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
    try:
      with open(self.__strFilenameFull, 'w') as fOut:
        strPersist = str(self.__dictPersist)
        fOut.write(strPersist)
        print(config_app.LOGFILENAME_PERSIST + ': written')
    except:
        print(config_app.LOGFILENAME_PERSIST + ': failed to write')
