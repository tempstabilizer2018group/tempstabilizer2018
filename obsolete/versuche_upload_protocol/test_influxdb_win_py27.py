# -*- coding: utf-8 -*-
# https://influxdb-python.readthedocs.io/en/latest/examples.html

import time
import random
import rfc3339
import influxdb

DATABASE = 'tempstabilizer'
# strHost = '10.0.11.237'
strHost = 'www.maerki.com'
# Set up influxDB connection
client = influxdb.InfluxDBClient(strHost, 8086, '', '', DATABASE) # url, port, user, pw, db


def measurement(strTime, strSite, strNode, strValue, fValue):
  return {
    'time': strTime,
    'measurement': strValue,
    'tags': {
      'node': strNode,
      'site': strSite,
    },
    'fields': {
      'value': fValue,
      'min': fValue - 0.5,
      'max': fValue + 0.2,
    },
  }

def annotation(strTime, strTitle, strText):
  # https://www.programcreek.com/python/example/107755/influxdb.InfluxDBClient
  return {
    'time': strTime,
    'measurement': 'events',
    # 'tags': {
    #   'node': 'node4711',
    #   'tags': '4711',
    #   'type': 'play',
    # },
    'fields': {
      'title': strTitle,
      'text': strText,
      'node': 'node4711',
      'site': 'test',
      # 'tags': 'node4711,node4712',
    },
  }


# '2018-09-06T11:52:34Z'
def getNow():
  # x = rfc3339.datetimetostr(datetime.time(tzinfo=rfc3339.UTC_TZ))
  x = rfc3339.timestamptostr(time.time())
  # x = rfc3339.timetostr(rfc3339.now())

  # https://github.com/BeyondTheClouds/enos/blob/master/enos/ansible/plugins/callback/influxdb_events.py
  # current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')

  return x


listMeasurements = []

strTime = getNow()
for strSite, strNode in (
      ('test', 'node4711'),
      ('test', 'node4712'),
      ('test', 'node4713'),
      ('cryostatX', 'amplifierX'),
      ('cryostatX', 'amplifierY'),
    ):
  for strTemp, fTemp in (
        ('tempO', 22.6),
        ('tempH', 25.6),
      ):
    fTemp += random.randrange(-200, 200)/100.0
    listMeasurements.append(measurement(strTime, strSite, strNode, strTemp, fTemp))


if True:
  # Write data to influxDB
  # https://influxdb-python.readthedocs.io/en/latest/api-documentation.html?highlight=time_precision
  client.write_points(listMeasurements, time_precision='s', protocol='json')

if True:
  listAnnotations = []
  listAnnotations.append(annotation(strTime, 'Reboot', 'Hello <i>Grafana</i>'))
  client.write_points(listAnnotations, tags={'node': 'node4711'}, protocol='json')

if False:
  # FUNKTIONIERT!
  # Messungen löschen aufgrund von tags

  result = client.query("DROP SERIES WHERE node='node4711'", database=DATABASE)
  # ResultSet: 2 Mal: [{u'columns': [...], u'name': u'tempO', u'values': [...]}]
  print(str(result))

  # FEHLER (POST nicht unterstützt)
  # result = client.query("DROP SERIES WHERE node='node4711'", database=DATABASE, method='POST')
  # influxdb.exceptions.InfluxDBClientError: 405: Method Not Allowed

  dictTags = {
    'node': 'node4712',
  }
  # FEHLER (POST nicht unterstützt)
  # client.delete_series(DATABASE, tags=dictTags)
  # InfluxDBClientError(u'405: Method Not Allowed\n',)
 
if False:
  # FUNKTIONIERT!
  databases = client.get_list_database()
  print(str(databases))
  # [{u'name': u'_internal'}, {u'name': u'tempstabilizer'}]

  # FUNKTIONIERT!
  result = client.query("select value from tempO where node='node4712';", database=DATABASE)
  # ResultSet: 2 Mal: [{u'columns': [...], u'name': u'tempO', u'values': [...]}]
  print(str(result))

if False:
  dbuser = 'maerki'
  dbuser_password = 'maerki'
  # username = 'maerki'
  # password = 'maerki'

  print('Get privileges for ' + dbuser)
  privileges = client.get_list_privileges(dbuser)
  print('Privileges: ' + str(privileges))
  # Privileges: []

  print('Drop database: ' + DATABASE)
  client.drop_database(DATABASE)
  # InfluxDBClientError(u'405: Method Not Allowed\n',)

  print('Create database: ' + DATABASE)
  client.create_database(DATABASE)

  # print('Create user: ' + dbuser)
  # client.create_user(username, password, admin=False)

  print('Switch user: ' + dbuser)
  client.switch_user(dbuser, dbuser_password)

if False:
  result = client.query('select value from tempO;')
  print('Result: {0}'.format(result))

