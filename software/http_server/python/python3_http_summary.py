# -*- coding: utf-8 -*-

import time
from dataclasses import dataclass
import influxdb
import config_http_server
import portable_grafana_datatypes
import python3_config_nodes_lib
import python3_github_pull
import config_nodes

from flask import Markup

class Row:
  def __init__(self):
    self.listCells = []

  def append(self, html):
    self.listCells.append(Markup(html))

listColumnsConfig = (
        # ('Lab', lambda o: o.strLabLabel),
        ('Node', lambda o: o.strName),
        ('Mac', lambda o: o.strMac),
        ('SW-Version', lambda o: o.strGitTags),
)

listColumnsGrafana = (
        ('SW-Version', portable_grafana_datatypes.TAG_GRAFANA_VERSION_SW),
        ('Firmware-Version', portable_grafana_datatypes.TAG_GRAFANA_VERSION_FIRMWARE),
        ('I2C [Hz]', portable_grafana_datatypes.TAG_GRAFANA_I2C_FREQUENCY_SELECTED_HZ),
        ('Last Error', portable_grafana_datatypes.TAG_GRAFANA_ERROR),
        ('Age [min]', portable_grafana_datatypes.TAG_GRAFANA_NTP),
)


class Table:
  def __init__(self):
    self.listColumnsConfig_len = len(listColumnsConfig)
    self.listColumnsGrafana_len = len(listColumnsGrafana)
    self.listColumnsAll = listColumnsConfig + listColumnsGrafana

    db = influxdb.InfluxDBClient(config_http_server.strInfluxDbHost, config_http_server.strInfluxDbPort, '', '', config_http_server.strInfluxDbDatabase)
    assert db != None
    q = db.query("SELECT * FROM /.*/ where type = '%s' group by node order by time desc limit 1" % portable_grafana_datatypes.INFLUXDB_TYPE_SUMMARY, epoch='s')
    influxdb_points = list(q.get_points())
    db.close()

    dictGrafanaNodes = {}
    for objPoint in influxdb_points:
      strNode = objPoint[config_http_server.strInfluxDbSummaryPrefix+portable_grafana_datatypes.INFLUXDB_TAG_NODE]
      dictGrafanaNodes[strNode] = objPoint

    self.listNodeLines = []
    for objPoint in influxdb_points:
      self.listNodeLines.append(Markup(objPoint))
    self.listNodeLines.append(', '.join(dictGrafanaNodes.keys()))

    self.listRows = self.get_rows(dictGrafanaNodes)

  def get_rows(self, dictGrafanaNodes):
    listRows = []

    p = config_http_server.factoryGitHubPull()
    objConfigNodes = p._getConfigNodesFromGithub()

    for dictLab, iterLabs in objConfigNodes.iterLabs():
      strLabLabel = dictLab[python3_config_nodes_lib.LAB_LABEL]
      
      row = Row()
      listRows.append(row)
      row.append(f'<th colspan="{ len(self.listColumnsAll) }">{strLabLabel}</th>')

      # Data rows
      for objNode in iterLabs:
        # strHtml += '<tr>\n'
        row = Row()
        listRows.append(row)

        # Config-Columns
        for _strDummy, func in listColumnsConfig:
          row.append(f'<td>{ Markup.escape(func(objNode)) }</td>')

        # Grafana Columns
        dictGrafanaNode = dictGrafanaNodes.get(objNode.strName, None)
        if dictGrafanaNode is None:
          # No data for this node
          row.append(f'<td colspan="{ len(listColumnsGrafana) }">node not seen</td>')
          continue
        for _strDummy, strTag in listColumnsGrafana:
          def get_value():
            strValue = dictGrafanaNode.get(config_http_server.strInfluxDbSummaryPrefix+strTag, None)
            if strValue == None:
              return '-'
            if strTag == portable_grafana_datatypes.TAG_GRAFANA_NTP:
              iAge_min = (int(time.time()) - int(strValue)//1000)//60
              return str(iAge_min)
            if strTag == portable_grafana_datatypes.TAG_GRAFANA_VERSION_SW:
              # heads-SLA-master;2;strRepo=-APR-local-SP-on-SP-raspberrypi-APR-
              # ->
              # heads/master;2
              return python3_github_pull.unescapeSwVersion(strValue)
            return strValue
          row.append(f'<td>{ Markup.escape(get_value()) }</td>')

    return listRows

if __name__ == '__main__':
  table = Table()
