# -*- coding: utf-8 -*-
import os
import sys
import time
import shutil
# Python 2
# import urllib2
# Python 3
from urllib.request import urlopen, Request

import config_app
import config_node
import portable_ticks
import portable_constants
import portable_controller
import portable_grafana_log_writer
import simulation_hw_hal
import portable_simuliert_tagesmodell
import portable_grafana_datatypes
import simulation_pyplot
import simulation_http_server_utils
import http_server_lib

class SimuliertController(portable_controller.Controller):
  def __init__(self, strFilenameFull):
    self.strFilenameFull = strFilenameFull
    self.strFilenameWithoutExtension = os.path.splitext(os.path.basename(self.strFilenameFull))[0]
    self.__iSecondsSince1970_UnixEpochStart = int(time.time())
    self.objTagesmodell = portable_simuliert_tagesmodell.Tagesmodell()
    simulation_pyplot.plot_init()
    self.logConsoleRemoveCurves()
    self.__removeLogFiles()
    self.__bIsNetworkConnected = False

    portable_controller.Controller.__init__(self)
    self.iStartTime_ms = portable_ticks.objTicks.time_ms()
    self.__objPlotInterval = portable_ticks.Interval(iInterval_ms=config_app.iLogSimuliertPlotInterval_ms)

  def directoryData(self):
    return simulation_http_server_utils.strNodeDataDirectory;

  def filenameLog(self):
    if config_app.bUseNetwork:
      return os.path.join(simulation_http_server_utils.strNodeDataDirectory, config_app.LOGFILENAME_TABDELIMITED)
    return '%s_log.txt' % self.strFilenameWithoutExtension

  def filenameGrafanaLog(self):
    if config_app.bUseNetwork:
      return os.path.join(simulation_http_server_utils.strNodeDataDirectory, config_app.LOGFILENAME_GRAFANA)
    return '%s_log_grafana.txt' % self.strFilenameWithoutExtension

  def factoryCachedFile(self, strFilename):
    fOut = open(strFilename, 'w')
    return fOut

  def prepare(self):
    portable_controller.Controller.prepare(self)
    # Make shure, that we don't start with the setpoint of a previous measurement.
    self.deletePersist()


  def reboot(self):
    print('reboot()...')
    sys.exit()
  
  def remove(self, strFilenameFull):
    os.remove(strFilenameFull)

  def done(self):
    portable_controller.Controller.done(self)

    simulation_pyplot.plot_show('%s.png' % self.strFilenameWithoutExtension)
    portable_ticks.objTicks.print_statistics()

  def factoryHw(self):
    return simulation_hw_hal.Hw(objTagesmodell=portable_simuliert_tagesmodell.Tagesmodell())

  def logConsoleRemoveCurves(self):
    pass

  def logConsole(self):
    bIntervalOver, iEffectiveIntervalDuration_ms = self.__objPlotInterval.isIntervalOver()
    if bIntervalOver:
      simulation_pyplot.plot_plot(self.objTs, self.objHw)

  def delay_ms(self, iDelay_ms):
    self.objHw.timeIncrement(iDelay_ms=iDelay_ms, fDac_V=self.objTs.fDac_V)

  def networkFindWlans(self):
    '''Return true if required Wlan found'''
    return True

  def networkConnect(self):
    self.__bIsNetworkConnected = not self.__bIsNetworkConnected

  def isNetworkConnected(self):
    return self.__bIsNetworkConnected

  def networkFreeResources(self):
    pass

  def closeLogs(self):
    if not config_app.bSimulationUseHttpPost:
      if self.objGrafanaProtocol != None:
        # Add a timestamp to the file
        # iSecondsSince1970_UnixEpoch = self.__iSecondsSince1970_UnixEpochStart + portable_ticks.objTicks.time_ms()/1000.0
        # iSecondsSince1970_UnixEpoch = time.time() + portable_ticks.objTicks.time_ms()/1000.0
        iSecondsSince1970_UnixEpoch = time.time()
        self.objGrafanaProtocol.logNtpTime(iSecondsSince1970_UnixEpoch)

    portable_controller.Controller.closeLogs(self)

  def networkReplicate(self):
    self.closeLogs()

    for strFromFilename in os.listdir(simulation_http_server_utils.strNodeDataDirectory):
      if strFromFilename == config_app.LOGFILENAME_PERSIST:
        # This is a persistent file and must not be processed
        continue
      strFromFilenameFull = os.path.join(simulation_http_server_utils.strNodeDataDirectory, strFromFilename)
      strFromFilenameBase = os.path.splitext(strFromFilename)[0]
      if config_app.bSimulationUseHttpPost:
        self.__doHttpPost(strFromFilenameFull, strFromFilenameBase)
      else:
        strToFilenameFull = http_server_lib.getToProcessFilenameFull(strFromFilenameBase, config_node.strSite, config_node.strNode)
        shutil.move(strFromFilenameFull, strToFilenameFull)

    self.openLogs()

  def networkDisconnect(self):
    self.bIsConnected = False

  def __removeLogFiles(self):
    if not config_app.bUseNetwork:
      return

    def deleteFiles(strDirectory):
      for strFilename in os.listdir(strDirectory):
        if not strFilename.endswith('.txt'):
          if not strFilename.endswith('.png'):
            continue
        strFilenameFull = os.path.join(strDirectory, strFilename)
        os.remove(strFilenameFull)

    deleteFiles(simulation_http_server_utils.strNodeDataDirectory)
    deleteFiles(http_server_lib.strHttpServerToProcessDirectory)

  def __doHttpPost(self, strFilenameFull, strFilenameBase):
    with open(strFilenameFull, 'r') as fIn:
      strData = fIn.read()

    bytesData = bytes(strData, 'ansi')

    strParams = '?site=%s&node=%s&filename=%s' % (config_node.strSite, config_node.strNode, strFilenameBase)
    strHttpPostUrl = config_app.strHttpPostUrl + strParams
    print('POST: %s, len: %d' % (strHttpPostUrl, len(bytesData)))
    # strHttpPostUrl: http://tempstabilizer.positron.ch/push/upload.grafana?site=waffenplatz&node=4711&filename=grafana
    objRequest = Request(strHttpPostUrl)
    objRequest.add_header('Content-Type', 'application/text')
    objResponse = urlopen(objRequest, data=bytesData)
    print('Response: ' + str(objResponse.read()))

    # If no error: Remove file
    os.remove(strFilenameFull)
