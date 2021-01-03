# -*- coding: utf-8 -*-

# TODO: OBSOLETE: REMOVE

import time
import influxdb
import config_http_server
import portable_grafana_datatypes
import python3_config_nodes_lib
import python3_github_pull
import config_nodes

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


def getSummary():
  strHtml = '''<html>
    <body>
      <h1>Temp Stabilizer 2018 - Summary</h1>
    '''
  strHtml += '<table border="1" cellspacing="0" bordercolorlight="#0FFFFF" bordercolordark="#0FFFFF">\n'
  # First header row
  strHtml += '<tr><th colspan="%d">config_nodes.py</th><th colspan="%d">live nodes</th></tr>\n' % (len(listColumnsConfig), len(listColumnsGrafana))
  # Second header row
  strHtml += '<tr>\n'
  for s, funcDummy in listColumnsConfig + listColumnsGrafana:
    strHtml += '<th>' + s + '</th>\n'
  strHtml += '</tr>\n'

  db = influxdb.InfluxDBClient(config_http_server.strInfluxDbHost, config_http_server.strInfluxDbPort, '', '', config_http_server.strInfluxDbDatabase)
  assert db != None
  q = db.query("SELECT * FROM /.*/ where type = '%s' group by node order by time desc limit 1" % portable_grafana_datatypes.INFLUXDB_TYPE_SUMMARY, epoch='s')
  dictGrafanaNodes = {}
  for objPoint in q.get_points():
    strNode_ = objPoint[config_http_server.strInfluxDbSummaryPrefix+portable_grafana_datatypes.INFLUXDB_TAG_NODE]
    dictGrafanaNodes[strNode_] = objPoint
    strHtml += '<!-- Node: %s -->\n' % str(objPoint)
  db.close()
  strHtml += '<!-- Nodes: %s -->\n\n' % (', '.join(dictGrafanaNodes.keys()))

  p = config_http_server.factoryGitHubPull()
  objConfigNodes = p._getConfigNodesFromGithub()

  for dictLab, iterLabs in objConfigNodes.iterLabs():
    strLabLabel = dictLab[python3_config_nodes_lib.LAB_LABEL]
    strHtml += '<tr><th colspan="%d">%s</th></tr>\n' % (len(listColumnsConfig)+len(listColumnsGrafana), strLabLabel)
    # Data rows
    for objNode in iterLabs:
      strHtml += '<tr>\n'

      # Config-Columns
      for strDummy, func in listColumnsConfig:
        strHtml += '<td>' + func(objNode) + '</td>\n'

      # Grafana Columns
      dictGrafanaNode = dictGrafanaNodes.get(objNode.strName, None)
      if dictGrafanaNode is None:
        # No data for this node
        strHtml += '<td colspan="%d">node not seen</td>\n' % len(listColumnsGrafana)
      else:
        for strDummy, strTag in listColumnsGrafana:
          strValue = dictGrafanaNode.get(config_http_server.strInfluxDbSummaryPrefix+strTag, None)
          if strTag == portable_grafana_datatypes.TAG_GRAFANA_NTP:
            iAge_min = (int(time.time()) - int(strValue)//1000)//60
            strValue = str(iAge_min)

            # The same, but with 'time' instead of 'ntptime'
            # iTime = dictGrafanaNode['time']
            # strTime = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(iTime))
            # iAge = (time.time()-iTime)/60.0

            # strHtml += '%d - %s' % (iAge, strTime)
          if strValue == None:
            strValue = '-'
          if strTag == portable_grafana_datatypes.TAG_GRAFANA_VERSION_SW:
            # heads-SLA-master;2;strRepo=-APR-local-SP-on-SP-raspberrypi-APR-
            # ->
            # heads/master;2
            strValue = python3_github_pull.unescapeSwVersion(strValue)
          strHtml += '<td>%s</td>\n' % strValue
      strHtml += '</tr>\n'

  strHtml += '''
    </table>
    </body>
    </html>
    '''
  return strHtml

if __name__ == '__main__':
  strHtml = getSummary()
  print(strHtml)
