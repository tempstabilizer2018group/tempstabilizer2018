# -*- coding: utf-8 -*-
'''
  Ableitung der Methoden für Simulation und Hardware.
'''
import sys

import config_app

import portable_ticks
import portable_constants
import portable_persist
import portable_controller
import portable_tempstabilizer
import portable_grafana_log_writer

class Controller:
  def __init__(self):
    self.ticks_init()
    self.__objPersist = portable_persist.Persist(self.directoryData())
    self.__iLedModulo = 0
    self.__iTicksButtonPressed_ms = None
    self.__fTempO_SensorLast = -1000.0
    self.__fTempH_SensorLast = -1000.0
    self.openLogs()
    self.objHw = self.factoryHw()
    # On reboot: start with Wlan
    bForceWlanFirstTime = self.objHw.isPowerOnReboot()
    if self.__fileExists(config_app.FILENAME_REPLICATE_ONCE):
      self.remove(config_app.FILENAME_REPLICATE_ONCE)
      print('removed:', config_app.FILENAME_REPLICATE_ONCE)
      bForceWlanFirstTime = True
    print('bForceWlanFirstTime:', bForceWlanFirstTime)
    self.__objPollForWlanInterval = portable_ticks.Interval(iInterval_ms=config_app.iPollForWlanInterval_ms, bForceFirstTime=bForceWlanFirstTime)
    self.objGrafanaProtocol = self.factoryGrafanaProtocol()
    self.attachFileToGrafanaProtocol()
    self.objTs = self.factoryTempStabilizer()

  def ticks_init(self):
    # May be derived and overridden
    portable_ticks.init(config_app.iSimulationMaxTicks_ms)

  def exit(self):
    # May be derived and overridden
    if config_app.iExperimentDuration_ms == None:
      return False
    bExit = config_app.iExperimentDuration_ms < portable_ticks.objTicks.time_ms()
    return bExit

  def done(self):
    # May be derived and overridden
    self.objHw.fDac_V = 0.0
    self.__objPersist.persist()
    self.closeLogs()
    return False

  def openLogs(self):
    self.fLog = self.factoryLog()
    if self.fLog != None:
      self.objTs.logHeader(self.fLog)

  def closeLogs(self):
    if self.fLog != None:
      self.fLog.close()
    if self.objGrafanaProtocol != None:
      self.objGrafanaProtocol.close()

  def getStartTime_ms(self):
    # May be derived and overridden
    return portable_ticks.objTicks.ticks_add(portable_ticks.objTicks.ticks_ms(), -config_app.iTimeProcess_O_H_ms)

  def __fileExists(self, strFilename):
    try:
      with open(strFilename, 'r') as fIn:
        return True
    except:
       return False

  def directoryData(self):
    raise Exception('Needs to be derived...')

  def filenameLog(self):
    raise Exception('Needs to be derived...')

  def filenameGrafanaLog(self):
    raise Exception('Needs to be derived...')

  def factoryCachedFile(self, strFilename):
    # May be derived and overridden
    fOut = portable_grafana_log_writer.CachedLog(strFilename)
    return fOut

  def factoryGrafanaProtocol(self):
    return portable_grafana_log_writer.GrafanaProtocol(self.objHw.listEnvironsAddressI2C)

  def attachFileToGrafanaProtocol(self):
    strFilename = self.filenameGrafanaLog()
    bFileExists = self.__fileExists(strFilename)
    objCachedFile = self.factoryCachedFile(strFilename)
    self.objGrafanaProtocol.attachFile(objCachedFile)
    if not bFileExists:
      self.objGrafanaProtocol.writeHeader(self.objHw.iI2cFrequencySelected)

  def factoryLog(self):
    # May be derived and overridden
    if config_app.iLogInterval_ms == None:
      return None

    self.__objLogInterval = portable_ticks.Interval(iInterval_ms=config_app.iLogInterval_ms)
    strFilename = self.filenameLog()
    return self.factoryCachedFile(strFilename)

  def factoryHw(self):
    raise Exception('Needs to be derived...')

  def factoryTempStabilizer(self):
    # May be derived and overridden
    return portable_tempstabilizer.TempStabilizer()

  def reboot(self):
    raise Exception('Needs to be derived...')
  
  def remove(self, strFilenameFull):
    raise Exception('Needs to be derived...')

  def prepare(self):
    if config_app.bRunStopwatch:
      portable_ticks.enableStopwatch()

    # In case we restarted and the hardware ist still active
    self.networkFreeResources()

    self.objHw.startTempMeasurement()

    print('portable_tempstabilizer.prepare(): Supply Voltage fSupplyHV_V is %0.2f V' % self.objHw.messe_fSupplyHV_V)

    self.objTs.find_fDACzeroHeat(self.objHw)

    self.__fTempO_SensorLast = self.objHw.messe_fTempH_C
    self.__fTempH_SensorLast = self.objHw.messe_fTempO_C
    fTempH_Start = self.__fTempO_SensorLast
    fTempO_Start = self.__fTempH_SensorLast + config_app.fStart_Increment_fTempO_C
    iStartTicks_ms = self.getStartTime_ms()
    self.objTs.start(iTimeOH_ms=iStartTicks_ms, iTimeDayMaxEstimator=iStartTicks_ms, fTempH_Start=fTempH_Start, fTempO_Sensor=fTempO_Start, objPersist=self.__objPersist)

  def isNetworkConnected(self):
    raise Exception('Needs to be derived...')

  def networkFreeResources(self):
    raise Exception('Needs to be derived...')

  def ledBlink(self):
    self.__iLedModulo += 1
    if self.__iTicksButtonPressed_ms == None:
      bOn = self.__iLedModulo % config_app.iHwLedModulo == 0
      self.objHw.setLed(bOn)

  def runOnce(self):
    '''
      return False: I2C-Readerror. Tray again next time
    '''
    try:
      iStopwatch_us = portable_ticks.stopwatch()
      fTempO_Sensor = self.objHw.messe_fTempO_C
      portable_ticks.stopwatch_end(iStopwatch_us, 'self.objHw.messe_fTempO_C')
      fTempDiff_C = abs(fTempO_Sensor - self.__fTempO_SensorLast)
      self.__fTempO_SensorLast = fTempO_Sensor
      if fTempDiff_C > 10.0:
        print('WARNING: self.objHw.messe_fTempO_C() diff = %f C' % fTempDiff_C)
        return False

      iStopwatch_us = portable_ticks.stopwatch()
      fTempH_Sensor = self.objHw.messe_fTempH_C  
      portable_ticks.stopwatch_end(iStopwatch_us, 'self.objHw.messe_fTempH_C')
      fTempDiff_C = abs(fTempH_Sensor - self.__fTempH_SensorLast)
      self.__fTempH_SensorLast = fTempH_Sensor
      if fTempDiff_C > 10.0:
        print('WARNING: self.objHw.messe_fTempH_C() diff = %f C' % fTempDiff_C)
        return False
    except Exception as e:
      self.logException(e, 'self.objHw.messe_fTempO_C / self.objHw.messe_fTempH_C')
      self.delay_ms(iDelay_ms=1000)
      return

    iNowTicks_ms = portable_ticks.objTicks.ticks_ms()

    iStopwatch_us = portable_ticks.stopwatch()
    self.objTs.processDayMaxEstimator(iNowTicks_ms, fTempO_Sensor)
    portable_ticks.stopwatch_end(iStopwatch_us, 'self.objTs.processDayMaxEstimator(...)')

    iStopwatch_us = portable_ticks.stopwatch()
    self.objTs.processO(iNowTicks_ms, fTempO_Sensor)
    portable_ticks.stopwatch_end(iStopwatch_us, 'self.objTs.processO(...)')

    iStopwatch_us = portable_ticks.stopwatch()
    self.objTs.processH(iNowTicks_ms, fTempH_Sensor, fTempO_Sensor, self.objHw.bZeroHeat)
    portable_ticks.stopwatch_end(iStopwatch_us, 'self.objTs.processH(...)')

    iStopwatch_us = portable_ticks.stopwatch()
    self.objHw.fDac_V = self.objTs.fDac_V(self.objHw.messe_fSupplyHV_V)
    portable_ticks.stopwatch_end(iStopwatch_us, 'self.objTs.fDac_V')
    return True

  def logOnce(self):
    self.objGrafanaProtocol.logTempstablilizer(self.objTs, self.objHw)
    self.logConsole()

    if self.fLog != None:
      self.log()

  def log(self):
    # May be derived and overridden
    if self.fLog == None:
      return

    bIntervalOver, iDummy = self.__objLogInterval.isIntervalOver()
    if bIntervalOver:
      self.objTs.log(self.fLog, self.objHw)
      portable_ticks.count('HwController.log()')

  def logConsole(self):
    raise Exception('Needs to be derived...')

  def sleepOnce(self, iStartTicks_ms):
    iDelay_ms = config_app.iTimeProcess_O_H_ms - portable_ticks.objTicks.ticks_diff(portable_ticks.objTicks.ticks_ms(), iStartTicks_ms)
    # print('iDelay_ms: %d' % iDelay_ms)
    if iDelay_ms > 0:
      self.delay_ms(iDelay_ms)

  def delay_ms(self, iDelay_ms):
    raise Exception('Needs to be derived...')

  def logException(self, objException, strFunction):
    # if type(objException) == OSError:
    #  uerrno.errorcode[uerrno.EEXIST]
    strMsg = '%s returned %s' % (strFunction, str(objException))
    self.objGrafanaProtocol.logWarning(strMsg)
    print(strMsg)
    sys.print_exception(objException)

  def runForever(self):
    self.prepare()
    while True:
      iStartTicks_ms = portable_ticks.objTicks.ticks_ms()

      self.ledBlink()

      iStopwatch_us = portable_ticks.stopwatch()
      self.networkOnce()
      portable_ticks.stopwatch_end(iStopwatch_us, 'self.networkOnce()')

      if False:
        iTimeDelta_ms = portable_ticks.objTicks.ticks_diff(portable_ticks.objTicks.ticks_ms(), iStartTicks_ms)
        if iTimeDelta_ms > 100:
          strMsg = 'networkOnce() took %s ms' % iTimeDelta_ms
          self.objGrafanaProtocol.logInfo(strMsg)
          print(strMsg)

      self.handleButton()

      portable_ticks.count('portable_controller.runForever().runOnce()')
      iStopwatch_us = portable_ticks.stopwatch()
      bSuccess = self.runOnce()
      portable_ticks.stopwatch_end(iStopwatch_us, 'self.runOnce()')
      if  bSuccess:
        portable_ticks.count('portable_controller.runForever().logOnce()')
        iStopwatch_us = portable_ticks.stopwatch()
        self.logOnce()
        portable_ticks.stopwatch_end(iStopwatch_us, 'self.logOnce()')
        self.__objPersist.persist()

      portable_ticks.count('portable_controller.runForever().sleepOnce()')
      self.sleepOnce(iStartTicks_ms)
      if self.exit():
        break
      self.objHw.startTempMeasurement()
    self.done()

  def handleButton(self):
    if self.__iTicksButtonPressed_ms == None:
      if self.objHw.bButtonPressed:
        # Button was released and now is pressed
        self.__iTicksButtonPressed_ms = portable_ticks.objTicks.ticks_ms()
      return
    iButtonPressed_ms = portable_ticks.objTicks.ticks_diff(portable_ticks.objTicks.ticks_ms(), self.__iTicksButtonPressed_ms)

    if iButtonPressed_ms < 2*portable_constants.SECOND_MS:
      # 0-2s: LED off
      self.objHw.setLed(bOn=True)
      if not self.objHw.bButtonPressed:
        strMsg = 'Button pressed < 2s: Force WLAN replication'
        self.objGrafanaProtocol.logInfo(strMsg)
        print(strMsg)
        self.__objPollForWlanInterval.doForce()
        self.__iTicksButtonPressed_ms = None
      return

    if iButtonPressed_ms < 10*portable_constants.SECOND_MS:
      # 2-10s: LED on
      self.objHw.setLed(bOn=False)
      if not self.objHw.bButtonPressed:
        strMsg = 'Button pressed < 10s: Flush logs and %s, than reboot' % config_app.LOGFILENAME_PERSIST
        self.objGrafanaProtocol.logInfo(strMsg)
        print(strMsg)
        # Write Logs
        self.__objPersist.persist(bForce=True)
        self.done()
        self.reboot()
        # Will never get here!
      return

    # 10-99s: LED off
    self.objHw.setLed(bOn=True)
    if not self.objHw.bButtonPressed:
      strMsg = 'Button pressed > 10s: Delete "%s" and Reboot' % config_app.LOGFILENAME_PERSIST
      self.objGrafanaProtocol.logInfo(strMsg)
      print(strMsg)

      # Write Logs
      self.done()

      # Delete the file after self.done(): self.done() writes it!
      self.deletePersist()

      self.reboot()
      # Will never get here!
      return

  def deletePersist(self):
    # Delete setpoint of previous session in 'persist.txt'
    self.__objPersist.delete(self.remove)

  def networkOnce(self):
    '''Return ms spent'''
    if not config_app.bUseNetwork:
      return

    bIntervalOver, iEffectiveIntervalDuration_ms = self.__objPollForWlanInterval.isIntervalOver()
    if not bIntervalOver:
      return 0

    portable_ticks.count('portable_controller.networkOnce() find wlan')
    if self.networkFindWlans():
      portable_ticks.count('portable_controller.networkOnce() found wlan')
      self.networkConnect()
      if self.isNetworkConnected():
        portable_ticks.count('portable_controller.networkOnce() replication started')
        self.writeStatisticsFile()
        self.networkReplicate()
      else:
        print('Not connected!')
      self.networkFreeResources()

    iTimeDelta_ms = self.__objPollForWlanInterval.iTimeElapsed_ms(portable_ticks.objTicks.ticks_ms())
    if iTimeDelta_ms > 100:
      strMsg = 'networkOnce() took %s ms' % iTimeDelta_ms
      self.objGrafanaProtocol.logInfo(strMsg)
      print(strMsg)

  def writeStatisticsFile(self):
    if not config_app.bWriteLogStatistics:
      return
    strFilename = '%s/%s' % (self.directoryData(), config_app.LOGFILENAME_STATISTICS)
    with open(strFilename, 'w') as fOut:
      portable_ticks.objTicks.print_statistics(fOut)

  def networkConnect(self):
    raise Exception('Needs to be derived...')

  def networkReplicate(self):
    raise Exception('Needs to be derived...')

  def networkFindWlans(self):
    '''Return true if required Wlan found'''
    # TODO: Uncomment the following line
    raise Exception('Needs to be derived...')

  def networkDisconnect(self):
    raise Exception('Needs to be derived...')
