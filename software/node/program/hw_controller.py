# -*- coding: utf-8 -*-
import uos
import sys
import utime
import machine
import network

import hw_hal
import hw_urequests
import hw_update_ota
import config_app
import portable_ticks
import portable_controller
import portable_constants
import portable_firmware_constants
import portable_grafana_log_writer

bDataDirectoryExists = False
def createDataDirectory():
  global bDataDirectoryExists
  if bDataDirectoryExists:
    return False
  try:
    uos.mkdir(config_app.DIRECTORY_DATA)
    print('Created directory: "%s"' % config_app.DIRECTORY_DATA)
    return True
  except:
    print('Directory already exists: "%s"' % config_app.DIRECTORY_DATA)
    return False

def logException(objException, strMsg):
  print(strMsg)
  sys.print_exception(objException)

  createDataDirectory()
  with open(config_app.DIRECTORY_DATA + '/' + config_app.LOGFILENAME_ERROR, 'w') as fError:
    fError.write(strMsg)
    fError.write('\n\n\n')
    sys.print_exception(objException, fError)

def updateConfigAppByVERSION():
  try:
    strAux = '-'
    # hw_update_ota.strSwVersion = heads/master;1;iPollForWlanInterval_ms=60*1000;iHwLedModulo=10
    print('MAC:', config_app.strMAC)
    print('VERSION.TXT:', hw_update_ota.strSwVersion)

    # strAux = 1;config-UNDERSCORE-app.iPollForWlanInterval-UNDERSCORE-ms=60*1000;config-UNDERSCORE-app.iHwLedModulo=12
    strAux = hw_update_ota.strSwVersion.split(';', 1)[1]
    # Unescape
    for strChar, strEscape in portable_constants.listReplacements:
      strAux = strAux.replace(strEscape, strChar)
    # strAux = 1;iPollForWlanInterval_ms=60*1000;iHwLedModulo=12

    print('exec("' + strAux + '")')
    exec(strAux)
  except Exception as e:
    logException(e, 'update configuration from "config_nodes.py" for %s: %s' % (config_app.strMAC, strAux))

class HwController(portable_controller.Controller):
  def __init__(self, strFilenameFull):
    self.strFilenameFull = strFilenameFull
    print('Programm: %s' % self.strFilenameFull)
    bCreated = createDataDirectory()
    portable_controller.Controller.__init__(self)
    if bCreated:
      self.objGrafanaProtocol.logWarning('SW-Update: ' + hw_update_ota.strSwVersion)
    self.__objLogConsoleInterval = portable_ticks.Interval(iInterval_ms=config_app.iLogHwConsoleInterval_ms)
    self.__objWlan = None

  def directoryData(self):
    return config_app.DIRECTORY_DATA

  def filenameLog(self):
    return '%s/%s' % (config_app.DIRECTORY_DATA, config_app.LOGFILENAME_TABDELIMITED) 
    # return portable_grafana_log_writer.nextFilename('log_%02d.txt')

  def filenameGrafanaLog(self):
    return '%s/%s' % (config_app.DIRECTORY_DATA, config_app.LOGFILENAME_GRAFANA) 
    # return portable_grafana_log_writer.nextFilename('log_grafana_%02d.txt')

  def factoryHw(self):
    return hw_hal.Hw()

  def logException2(self, objException, strMsg):
    logException(objException, strMsg)

  def logConsole(self):
    bIntervalOver, iEffectiveIntervalDuration_ms = self.__objLogConsoleInterval.isIntervalOver()
    portable_ticks.bDoStopwatch = False
    if bIntervalOver:
      # During the next loop, the Stopwatch will log
      portable_ticks.bDoStopwatch = True
      strTempEnvirons_C = '-'
      listTempEnvirons_C = self.objHw.messe_listTempEnvirons_C
      if len(listTempEnvirons_C) > 0:
        strTempEnvirons_C = ','.join(map(lambda f:'%0.2fC' % f, listTempEnvirons_C ))
      print('%0.3fs %s %0.2f(%0.2f)C %0.2f(%0.2f)C %0.3f' % (portable_ticks.objTicks.ticks_ms()/1000.0, strTempEnvirons_C, self.objTs.fTempO_C, self.objTs.fTempO_Setpoint_C, self.objTs.fTempH_C, self.objTs.fTempH_Setpoint_C, self.objHw.fDac_V))

  def reboot(self):
    hw_update_ota.objGpio.pwmLedReboot()
    machine.reset()

  def remove(self, strFilenameFull):
    uos.remove(strFilenameFull)

  def delay_ms(self, iDelay_ms):
    portable_ticks.delay_ms(iDelay_ms)

  def __createWlan(self):
    if self.__objWlan is None:
      self.__objWlan = network.WLAN(network.STA_IF)
  
  def networkFindWlans(self):
    '''Return true if required Wlan found'''
    if config_app.strWlanSidForTrigger == None:
      return True

    hw_update_ota.objGpio.pwmLedWlanScan()
    self.__createWlan()
    self.__objWlan.active(True)
    # wlan.scan(scan_time_ms, channel)
    # scan_time_ms > 0: Active scan
    # scan_time_ms < 0: Passive scan
    # channel: 0: All 11 channels
    scan_time_ms = 200
    if config_app.strWlanChannel == 0:
      scan_time_ms = 2200
    channel = config_app.strWlanChannel
    listWlans = self.__objWlan.scan(scan_time_ms, channel)
    # wlan.scan()
    # I (5108415) network: event 1
    # [
    # (b'rumenigge', b'Dn\xe5]$D', 1, -37, 3, False),
    # (b'waffenplatzstrasse26', b'\xa0\xf3\xc1KIP', 6, -77, 4, False),
    # (b'ubx-92907', b'\x08j\n.a\x00', 10, -92, 3, False)
    # ]
    for listWlan in listWlans:
      strSsid = listWlan[0].decode()
      if strSsid == config_app.strWlanSidForTrigger:
        print('strWlanSidForTrigger "%s": SEEN!' % config_app.strWlanSidForTrigger)
        return True
    print('strWlanSidForTrigger "%s": NOT SEEN!' % config_app.strWlanSidForTrigger)
    return False

  def networkFreeResources(self):
    print('networkFreeResources()')
    if self.__objWlan is None:
      return
    if self.__objWlan.active():
      if self.__objWlan.isconnected():
        self.__objWlan.disconnect()
      self.__objWlan.active(False)

  def isNetworkConnected(self):
    return self.__objWlan.isconnected()

  def networkConnect(self):
    print('networkConnect("%s")' % config_app.strWlanSsid)
    self.__createWlan()
    if not self.__objWlan.active():
      self.__objWlan.active(True)
    hw_update_ota.objGpio.pwmLedWlanConnected()
    self.__objWlan.connect(config_app.strWlanSsid, config_app.strWlanPw)
    # Wait some time to get connected
    for iPause in range(10):
      # Do not use self.delay_ms(): Light sleep will kill the wlan!
      hw_hal.feedWatchdog()
      utime.sleep_ms(1000)
      if self.__objWlan.isconnected():
        return

  def networkReplicate(self):
    self.closeLogs()

    if config_app.iHttpPostBigTestfile != None:
      # Create a big file to verify, if it may be sent in a post
      with open(config_app.DIRECTORY_DATA + '/bigfile.txt', 'w') as fOut:
        fOut.seek(config_app.iHttpPostBigTestfile)

    try:
      self.__networkReplicate()
    except MemoryError:
      raise
    except Exception as e:
      self.logException(e, '__networkReplicate()')

    self.openLogs()
    self.attachFileToGrafanaProtocol()

  def __networkReplicate(self):
    # TODO:
    # merge with simulation_controller.__doHttpPost
    # merge with simulation_controller.networkReplicate

    for strFromFilename in uos.listdir(config_app.DIRECTORY_DATA):
      if strFromFilename == config_app.LOGFILENAME_PERSIST:
        # This is a persistent file and must not be processed
        continue
      hw_hal.feedWatchdog()
      strFilenameFull = '%s/%s' % (config_app.DIRECTORY_DATA, strFromFilename)
      strFilenameBase = strFromFilename.split('.')[0]
      self.__doHttpPost(strFilenameFull, strFilenameBase)

    hw_hal.feedWatchdog()
    bNewSwVersion = hw_update_ota.checkIfNewSwVersion(self.__objWlan)
    if bNewSwVersion:
      hw_hal.feedWatchdog()
      self.objHw.fDac_V = 0.0
      uos.remove(portable_firmware_constants.strFILENAME_VERSION)
      self.__objWlan.disconnect()
      print('Reboot for Software update.')
      machine.reset()

  def __doHttpPost(self, strFilenameFull, strFilenameBase):
    # uos.stat('main.py')
    # (32768, 0, 0, 0, 0, 0, 318, 595257990, 595257990, 595257990)
    iStreamlen = uos.stat(strFilenameFull)[6]
    strHttpPostUrl = '%s%s?%s=%s&%s=%s' % (
      config_app.strHttpPostServer,
      config_app.strHttpPostPath,
      portable_firmware_constants.strHTTP_ARG_MAC, config_app.strMAC,
      portable_firmware_constants.strHTTP_ARG_FILENAME, strFilenameBase
    )

    print('POST %dBytes: %s' % (iStreamlen, strHttpPostUrl))

    # strHttpPostUrl: http://www.tempstabilizer2018.org/upload?mac=ab01cd02ef03&filename=grafana
    with open(strFilenameFull, 'rb') as fStream:
      dictHeaders = {'Content-Type': 'application/text'}
      objResponse = hw_urequests.post(strHttpPostUrl, stream=fStream, streamlen=iStreamlen, headers=dictHeaders)

    print('Response: %d' % objResponse.status_code)
    while True:
      # This corresponds to 'objResponse.text' but doesn't allocate much memory
      # s = objResponse.raw.read(1024).decode('utf-8')
      b = objResponse.raw.read(1024)
      if len(b) == 0:
        break
      print(b.decode('utf-8'), end='')
    print('')

    if objResponse.status_code == 200:
      # If no error: Remove file
      uos.remove(strFilenameFull)

