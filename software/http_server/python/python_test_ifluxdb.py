# -*- coding: utf-8 -*-

import python3_rfc3339
import influxdb
import config_http_server

def doit():
  # fSecondsSince1970_UnixEpochStart_EndOfFile = time.time()
  # strTime = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(fSecondsSince1970_UnixEpochStart_EndOfFile))
  # strTimeEnd = python3_rfc3339.timestamptostr(iTime_ms/1000.0 + self.__fSecondsSince1970_UnixEpochStart + 60*1000)

  listMeasurements = []

  for strTime, strTimeEnd in (
      ('2019-02-21T19:10:51Z', '2019-02-21T19:50:51Z'),
      ('2019-02-21T20:10:51Z', '2019-02-21T20:40:51Z'),
    ):
    for strLab, fLab in (
        ('labTest1', 0.0),
        ('labTest2', 10.0),
      ):
      for strNode, fNode in (
          ('20', 0.0),
          ('21', 1.0),
          ('22', 2.0),
        ):
        dictMeasurement = {
                    'measurement': strLab,
                    'time': strTime,
                    'fields': {
                      'fTempO_C': 26.8 + fNode + fLab,
                    },
                    'tags': {
                      'node': strNode,
                      'origin': 'tempstabilizer2018',
                    },
                  }
        listMeasurements.append(dictMeasurement)

        dictMeasurement = {
                    'measurement': strLab,
                    'time': strTime,
                    'timeEnd': strTimeEnd,
                    'fields': {
                      'tags': 'info,error',
                      'title': 'Title_%s_%s' % (strLab, strNode),
                      'text': 'Text_%s_%s' % (strLab, strNode),
                    },
                    'tags': {
                      'node': strNode,
                      'type': 'event',
                      'severity': 'info',
                      'origin': 'tempstabilizer2018',
                    },
          }
        listMeasurements.append(dictMeasurement)

  db = influxdb.InfluxDBClient(config_http_server.strInfluxDbHost, config_http_server.strInfluxDbPort, '', '', config_http_server.strInfluxDbDatabase)
  assert db != None
  db.drop_database(config_http_server.strInfluxDbDatabase)
  db.create_database(config_http_server.strInfluxDbDatabase)
  db.switch_database(config_http_server.strInfluxDbDatabase)
  # db.delete_series()
  # db.delete_series('/.*/')
  bSuccess = db.write_points(listMeasurements, time_precision='s', protocol='json')
  assert bSuccess == True
  db.close()


if __name__ == '__main__':
  doit()