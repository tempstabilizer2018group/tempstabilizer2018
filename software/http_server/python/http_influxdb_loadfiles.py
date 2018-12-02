# -*- coding: utf-8 -*-
import os
import shutil
import traceback

import rfc3339
import influxdb

import config_app
import config_http_server
import time
import http_server_lib
import grafana_log_reader_lib
import grafana_log_reader

class GrafanaInfluxGetNtpTime(grafana_log_reader_lib.GrafanaDumper):
  def __init__(self):
    grafana_log_reader_lib.GrafanaDumper.__init__(self)
    self.fSecondsSince1970_UnixEpochStart_StartOfFile = None

  def handleNtpTime(self, iTime_ms, iSecondsSince1970_UnixEpoch):
    self.fSecondsSince1970_UnixEpochStart_StartOfFile = iSecondsSince1970_UnixEpoch - iTime_ms/1000.0

class GrafanaInfluxDbDumper(grafana_log_reader_lib.GrafanaDumper):
  def __init__(self, fSecondsSince1970_UnixEpochStart_StartOfFile):
    grafana_log_reader_lib.GrafanaDumper.__init__(self)
    self.__fSecondsSince1970_UnixEpochStart = fSecondsSince1970_UnixEpochStart_StartOfFile
    self.__listMeasurements = []

  def handleNode(self, iTime_ms, strSite, strNode):
    self.__strSite = strSite
    self.__strNode = strNode

  def addMeasurement(self, objGrafanaValue, iTime_ms, strValue):
    fValue = objGrafanaValue.convert2float(strValue)

    # 09/15/2018 17:37:30

    #import time
    #x = rfc3339.timestamptostr(time.time())
    # 09/15/2018 20:27:42
    #print(strTime, x)

    # time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(1541350369))
    # '2018-11-04T17:52:49Z'
    # rfc3339.timestramptostr(1541350369)
    # Traceback (most recent call last):
    #   File "<stdin>", line 1, in <module>
    # AttributeError: 'module' object has no attribute 'timestramptostr'
    # rfc3339.timestamptostr(1541350369)
    # '2018-11-04T16:52:49Z'

    # https://github.com/BeyondTheClouds/enos/blob/master/enos/ansible/plugins/callback/influxdb_events.py
    # import time
    # t = time.localtime(self.fSecondsSince1970_UnixEpoch + 0.001*iTime_ms)
    # strTime = time.strftime('%Y-%m-%dT%H:%M:%SZ', t)
    strTime = rfc3339.timestamptostr(iTime_ms/1000.0 + self.__fSecondsSince1970_UnixEpochStart)

    dictMeasurement = {
      'time': strTime,
      'measurement': self.__strSite,
      'tags': {
        'node': self.__strNode,
      },
      'fields': {
        objGrafanaValue.strName: fValue,
      },
    }

    self.__listMeasurements.append(dictMeasurement)

  def __writeToInfluxDB(self, strFilenameFull):
    # Set up influxDB connection
    # url, port, user, pw, db
    objInfluxDBClient = influxdb.InfluxDBClient(config_http_server.strInfluxDbHost, config_http_server.strInfluxDbPort, '', '', config_http_server.strInfluxDbDatabase)

    # Write data to influxDB
    # https://influxdb-python.readthedocs.io/en/latest/api-documentation.html?highlight=time_precision
    print('%s: Writing %d measurements to InfluxDB...' % (os.path.basename(strFilenameFull), len(self.__listMeasurements)))
    objInfluxDBClient.write_points(self.__listMeasurements, time_precision='s', protocol='json')

  def readFileAndWriteToDB(self, strFilenameFull):
    self.readFile(strFilenameFull)
    self.__writeToInfluxDB(strFilenameFull)

def loadFileIntoInfluxDb(strFilenameFull):
  objNtpTimeDumper = GrafanaInfluxGetNtpTime()
  objNtpTimeDumper.readFile(strFilenameFull)
  fSecondsSince1970_UnixEpochStart_StartOfFile = objNtpTimeDumper.fSecondsSince1970_UnixEpochStart_StartOfFile
  objInfluxDbDumper = GrafanaInfluxDbDumper(fSecondsSince1970_UnixEpochStart_StartOfFile)
  objInfluxDbDumper.readFileAndWriteToDB(strFilenameFull)

def writePng(strFilenameFull):
  strFilenamePngFull = strFilenameFull.replace('.txt', '.png')
  assert strFilenamePngFull != strFilenameFull

  print('%s: Writing PNG' % os.path.basename(strFilenamePngFull))

  import grafana_log_config

  objDumper = grafana_log_reader.GrafanaPlotDumper(grafana_log_config.getPlotConfig())
  objDumper.readFile(strFilenameFull)
  objDumper.plot(strFilenamePngFull)

def processFiles(strDirectoryToBeProcessed, strDirectoryProcessed=None, strDirectoryFailed=None, bWritePng=False):
  for strFilename in os.listdir(strDirectoryToBeProcessed):
    if not strFilename.endswith('.txt'):
      continue
    strFromFilenameFull = os.path.join(strDirectoryToBeProcessed, strFilename)

    if strFilename.endswith(config_app.LOGFILENAME_GRAFANA):
      try:
        loadFileIntoInfluxDb(strFromFilenameFull)
      except Exception as e:
        print('loadFileIntoInfluxDb() failed: %s' % str(e))
        traceback.print_exc(e)
        if strDirectoryFailed != None:
          strToFilenameFull = os.path.join(strDirectoryFailed, strFilename)
          shutil.move(strFromFilenameFull, strToFilenameFull)
          continue

      if bWritePng:
        writePng(strFromFilenameFull)

    if strDirectoryProcessed != None:
      strToFilenameFull = os.path.join(strDirectoryProcessed, strFilename)
      shutil.move(strFromFilenameFull, strToFilenameFull)

if __name__ == '__main__':
  # loadFileIntoInfluxDb(r'C:\Projekte\temp_stabilizer_2018\temp_stabilizer_2018\software_regler\http_server\node_data\to_process\2018-11-04_16-52-47_httptest_4712_grafana.txt')
  # processFiles(http_server_lib.strHttpServerToProcessDirectory)
  
  processFiles(http_server_lib.strHttpServerToProcessDirectory,
                                         http_server_lib.strHttpServerProcessedDirectory,
                                         http_server_lib.strHttpServerFailedDirectory,
                                         bWritePng=False)