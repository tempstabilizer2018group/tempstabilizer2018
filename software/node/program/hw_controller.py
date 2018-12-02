# -*- coding: utf-8 -*-
import uos
import sys
import utime
import machine
import network

import hw_hal
import hw_urequests
import config_app
import config_node
import portable_ticks
import portable_controller
import portable_grafana_log_writer

class HwController(portable_controller.Controller):
  def __init__(self, strFilenameFull):
    self.strFilenameFull = strFilenameFull
    print('Programm: %s' % self.strFilenameFull)
    portable_controller.Controller.__init__(self)
    self.__objLogConsoleInterval = portable_ticks.Interval(iInterval_ms=config_app.iLogHwConsoleInterval_ms)
    self.__objWlan = network.WLAN(network.STA_IF)

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

  def logConsole(self):
    bIntervalOver, iEffectiveIntervalDuration_ms = self.__objLogConsoleInterval.isIntervalOver()
    portable_ticks.bDoStopwatch = False
    if bIntervalOver:
      # During the next loop, the Stopwatch will log
      portable_ticks.bDoStopwatch = True
      fTempEnvirons_C = self.objHw.messe_fTempEnvirons_C
      strTempEnvirons_C = '-'
      if fTempEnvirons_C != None:
        strTempEnvirons_C = '%0.2fC' % fTempEnvirons_C
      print('%0.3fs %s %0.2f(%0.2f)C %0.2f(%0.2f)C %0.3f' % (portable_ticks.objTicks.ticks_ms()/1000.0, strTempEnvirons_C, self.objTs.fTempO_C, self.objTs.fTempO_Setpoint_C, self.objTs.fTempH_C, self.objTs.fTempH_Setpoint_C, self.objTs.fDac_V))

  def reboot(self):
    machine.reset()

  def remove(self, strFilenameFull):
    uos.remove(strFilenameFull)

  def delay_ms(self, iDelay_ms):
    portable_ticks.delay_ms(iDelay_ms)

  def networkFindWlans(self):
    '''Return true if required Wlan found'''
    if config_app.strWlanSidForTrigger == None:
      return True

    self.__objWlan.active(True)
    # wlan.scan(scan_time_ms, channel)
    # scan_time_ms > 0: Active scan
    # scan_time_ms < 0: Passive scan
    # channel: 0: All 11 channels
    scan_time_ms = 200
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
      strSid = listWlan[0].decode()
      if strSid == config_app.strWlanSidForTrigger:
        print('strWlanSidForTrigger "%s": SEEN!' % config_app.strWlanSidForTrigger)
        return True;
    print('strWlanSidForTrigger "%s": NOT SEEN!' % config_app.strWlanSidForTrigger)
    return False

  def networkFreeResources(self):
    print('networkFreeResources()')
    if self.__objWlan.active():
      if self.__objWlan.isconnected():
        self.__objWlan.disconnect()
      self.__objWlan.active(False)

  def isNetworkConnected(self):
    return self.__objWlan.isconnected()

  def networkConnect(self):
    print('networkConnect("%s")' % config_app.strWlanSid)
    if not self.__objWlan.active():
      self.__objWlan.active(True)
    self.__objWlan.connect(config_app.strWlanSid, config_app.strWlanPw)
    # Wait some time to get connected
    for iPause in range(10):
      # Do not use self.delay_ms(): Light sleep will kill the wlan!
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
    except Exception as e:
      self.logException(e, '__networkReplicate()')

    self.openLogs()

  def __networkReplicate(self):
    # TODO:
    # merge with simulation_controller.__doHttpPost
    # merge with simulation_controller.networkReplicate

    for strFromFilename in uos.listdir(config_app.DIRECTORY_DATA):
      if strFromFilename == config_app.LOGFILENAME_PERSIST:
        # This is a persistent file and must not be processed
        continue
      strFilenameFull = '%s/%s' % (config_app.DIRECTORY_DATA, strFromFilename)
      strFilenameBase = strFromFilename.split('.')[0]
      self.__doHttpPost(strFilenameFull, strFilenameBase)

  def __doHttpPost(self, strFilenameFull, strFilenameBase):
    # uos.stat('main.py')
    # (32768, 0, 0, 0, 0, 0, 318, 595257990, 595257990, 595257990)
    iStreamlen = uos.stat(strFilenameFull)[6]

    with open(strFilenameFull, 'r') as fStream:
      strParams = '?site=%s&node=%s&filename=%s' % (config_node.strSite, config_node.strNode, strFilenameBase)
      strHttpPostUrl = config_app.strHttpPostUrl + strParams
      print('POST: %s, len: %s' % (strHttpPostUrl, iStreamlen))

      # strHttpPostUrl: http://tempstabilizer.positron.ch/push/upload.grafana?site=waffenplatz&node=4711&filename=grafana
      dictHeaders = {'Content-Type': 'application/text'}
      objResponse = hw_urequests.post(strHttpPostUrl, stream=fStream, streamlen=iStreamlen, headers=dictHeaders)

    print('Response: %d %s' % (objResponse.status_code, objResponse.text))

    if objResponse.status_code == 200:
      # If no error: Remove file
      uos.remove(strFilenameFull)

