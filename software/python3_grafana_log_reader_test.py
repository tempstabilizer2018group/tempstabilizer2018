# -*- coding: utf-8 -*-
import python3_rfc3339
import influxdb

import portable_grafana_log_reader

class InfluxDumper:
  def __init__(self):
    self.fSecondsSince1970_UnixEpoch = None
    self.strSite = None
    self.strNode = None
    self.dictValues = {}
    self.listMeasurements = []

  def funcLine(self, iTime_ms, strVerb, strPayload):
    if strVerb == TAG_GRAFANA_NTP:
      # Seconds since 2000-01-01
      iSecondsSince2000 = int(strPayload)
      # https://www.unixtimestamp.com/index.php
      self.fSecondsSince1970_UnixEpoch = iSecondsSince2000 + 946684800.0
      return 

    if strVerb == TAG_GRAFANA_SITE_NODE:
      self.strSite, self.strNode = strPayload.split()
      return

    if strVerb == TAG_GRAFANA_VERSION:
      self.handleMeasurements(iTime_ms, strPayload)
      return

  def handleMeasurements(self, iTime_ms, strPayload):
    def measurement(strTag, strValue, funcConvert):
      if strValue == '':
        fValue = self.dictValues[strTag]
      else:
        fValue = funcConvert(strValue)
        self.dictValues[strTag] = fValue
      dictMeasurement = {
        'time': strTime,
        'measurement': strTag,
        'tags': {
          'node': self.strNode,
          'site': self.strSite,
        },
        'fields': {
          'value': fValue,
        },
      }
      self.listMeasurements.append(dictMeasurement)

    strTime = rfc3339.timestamptostr(self.fSecondsSince1970_UnixEpoch + 0.001*iTime_ms)
    # 09/15/2018 17:37:30

    #import time
    #x = rfc3339.timestamptostr(time.time())
    # 09/15/2018 20:27:42
    #print(strTime, x)

    # https://github.com/BeyondTheClouds/enos/blob/master/enos/ansible/plugins/callback/influxdb_events.py
    # import time
    # t = time.localtime(self.fSecondsSince1970_UnixEpoch + 0.001*iTime_ms)
    # strTime = time.strftime('%Y-%m-%dT%H:%M:%SZ', t)
    for strTag, strValue in portable_grafana_log_reader.ValuesIterator(strPayload):
      # if strTag == 'H':
      #   measurement('Heat', strValue, lambda v: int(v)/100.0)

      if strTag == 'O':
        measurement('fTempO_C', strValue, lambda v: int(v)/1000.0)
      if strTag == 'S':
        measurement('fTempO_Setpoint_C', strValue, lambda v: int(v)/1000.0)
      if strTag == 'H':
        measurement('fHeat_W', strValue, lambda v: int(v)/100.0)
      if strTag == 'U':
        measurement('fTempEnvirons_C', strValue, lambda v: int(v)/1000.0)
      if strTag == 'z':
        measurement('fDACzeroHeat_V', strValue, lambda v: int(v)/1000.0)
      if strTag == 'L':
        measurement('PidH_bLimitHigh', strValue, lambda v: v == '+')

  def writeToInfluxDB(self):
    DATABASE = 'tempstabilizer'
    # strHost = '10.0.11.237'
    strHost = 'www.maerki.com'
    # Set up influxDB connection
    objInfluxDBClient = influxdb.InfluxDBClient(strHost, 8086, '', '', DATABASE) # url, port, user, pw, db

    # Write data to influxDB
    # https://influxdb-python.readthedocs.io/en/latest/api-documentation.html?highlight=time_precision
    print('Writing %d measurements...' % len(self.listMeasurements))
    objInfluxDBClient.write_points(self.listMeasurements, time_precision='s', protocol='json')

  '''
  GrafanaValueFloatAvg('O', 'fTempO_C', 1000.0),
  GrafanaValueFloatAvg('S', 'fTempO_Setpoint_C', 1000.0),
  GrafanaValueFloatAvg('H', 'fHeat_W',  100.0),
  GrafanaValueFloatAvg('U', 'fTempEnvirons_C',  1000.0),
  GrafanaValueBoolTrue('L', 'PidH_bLimitHigh'),
  GrafanaValueFloatAvg('z', 'portable_tempstabilizer.fDACzeroHeat_V', 1000.0),
  '''

def run(strFilename):
  objDumper = InfluxDumper()
  with open(strFilename, 'r') as fLog:
    portable_grafana_log_reader.read(fLog, objDumper.funcLine)
  objDumper.writeToInfluxDB()

if __name__ == '__main__':
  # run('simuliert_hw_pidh_pido_log_grafana.txt')
  run('regelresultate_2018-09-16a/test_hw_pidh_pido_day_log_grafana_01.txt')
