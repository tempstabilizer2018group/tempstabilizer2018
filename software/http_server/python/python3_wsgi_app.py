# -*- coding: utf-8 -*-

import os
import sys
import cgi

strFileDirectory = os.path.dirname(__file__)
sys.path.append(strFileDirectory)
sys.path.append(os.path.join(strFileDirectory, '../../node/config'))
sys.path.append(os.path.join(strFileDirectory, '../../node/program'))

import config_app
import config_http_server
import portable_firmware_constants
import python3_http_influxdb_loadfiles

strSTATUS_200 = '200 OK'
strSTATUS_204 = '204 NO_CONTENT'
strSTATUS_301 = '301 MOVED_PERMANENTLY'
strSTATUS_400 = '400 BAD_REQUEST'
strCONTENTTYPE_TEXT = 'text/plain'
strCONTENTTYPE_HTML = 'text/html'
strCONTENTTYPE_BINARY = 'application/octet-stream'

strHTTP_PATH_INFLUXDB_DELETE = '/influxdb_delete'
strHTTP_PATH_INFLUXDB_RELOAD_ALL = '/influxdb_reload_all'

def responseBytes(start_response, strMessage, strFilename=None, strStatus=strSTATUS_200, strContentType=strCONTENTTYPE_TEXT):
  response_headers = [('Content-type', strContentType),
                ('Content-Length', str(len(strMessage)))]
  if strFilename != None:
    response_headers.append(('Content-Disposition', 'attachment; filename="%s"' % strFilename))
  start_response(strStatus, response_headers)
  return [strMessage]

def response(start_response, strMessage, strStatus=strSTATUS_200, strContentType=strCONTENTTYPE_TEXT):
  strMessage = bytes(strMessage, encoding='utf-8')
  return responseBytes(start_response, strMessage, strStatus=strStatus, strContentType=strContentType)

class WsgiException(Exception):
  def __init__(self, strMessage, strStatus=strSTATUS_400):
    super().__init__(strMessage)
    self.strMessage = strMessage
    self.strStatus = strStatus

  def getBadResponse(self, start_response):
    return response(start_response, self.strMessage, strStatus=self.strStatus)

def badRequest(start_response, strMessage):
  return response(start_response, strMessage, strStatus=strSTATUS_400)

def ok(start_response, strMessage, strContentType):
  return response(start_response, strMessage, strStatus=strSTATUS_200, strContentType=strContentType)

def getArg(environ, strArg):
  # Returns a dictionary in which the values are lists
  d = cgi.parse_qs(environ['QUERY_STRING'])
   
  # Returns the first value.
  listValues = d.get(strArg, None)
  if listValues == None:
    raise NameError('Required argument "%s" missing!' % strArg)
  return listValues[0]

def handle_get(environ, start_response):
  import python3_github_pull

  strPathInfo = environ['PATH_INFO']

  if strPathInfo == '/intro.html':

    listLinks = []

    def addLink(strText, strLink):
      listLinks.append((strText, strLink))

    addLink('github', 'https://github.com/tempstabilizer2018group/tempstabilizer2018')
    addLink('grafana', 'http://%(HTTP_HOST)s:3000' % environ)
    addLink('summary (summary of configured against live nodes)', 'summary.html')
    addLink(portable_firmware_constants.strHTTP_PATH_VERSIONCHECK, '%(strHTTP_PATH_VERSIONCHECK)s?%(strHTTP_ARG_MAC)s=3C71BF0F97A4&%(strHTTP_ARG_VERSION)s=heads-SLASH-master;1' % portable_firmware_constants.__dict__)
    addLink(portable_firmware_constants.strHTTP_PATH_SOFTWAREUPDATE, '%(strHTTP_PATH_SOFTWAREUPDATE)s?%(strHTTP_ARG_MAC)s=3C71BF0F97A4&%(strHTTP_ARG_VERSION)s=heads-SLASH-master;1' % portable_firmware_constants.__dict__)

    addLink('influx db: delete (Dangerous! Will delete the whole database!)', strHTTP_PATH_INFLUXDB_DELETE)
    addLink('influx db: reload all datafiles (Dangerous! Will delete the whole database!)', strHTTP_PATH_INFLUXDB_RELOAD_ALL)

    strLinks = ''
    for strText, strLink in listLinks:
      strLinks += '<p><a target="_blank" href="%s">%s</a></p>\n' % (strLink, strText)
  
    strHtml = '''<html>
    <body>
      <h1>Temp Stabilizer 2018</h1>
      %s
    </body>
    </html>
    ''' % strLinks
    return ok(start_response, strHtml, strContentType=strCONTENTTYPE_HTML)

  if strPathInfo == '/summary.html':
    import python3_wsgi_app_summary
    strHtml = python3_wsgi_app_summary.getSummary()
    return ok(start_response, strHtml, strContentType=strCONTENTTYPE_HTML)

  if strPathInfo == strHTTP_PATH_INFLUXDB_DELETE:
    python3_http_influxdb_loadfiles.delete()
    return ok(start_response, 'done', strContentType=strCONTENTTYPE_TEXT)

  if strPathInfo == strHTTP_PATH_INFLUXDB_RELOAD_ALL:
    python3_http_influxdb_loadfiles.delete()
    python3_http_influxdb_loadfiles.reload_all()
    return ok(start_response, 'done', strContentType=strCONTENTTYPE_TEXT)

  if strPathInfo == '/':
    response_headers = [
            ('Content-type', strCONTENTTYPE_TEXT),
            ('Content-Length', '0'),
            ('Location', '/index.html'),
    ]
    start_response(strSTATUS_301, response_headers)
    return [b'']

  strMac = getArg(environ, portable_firmware_constants.strHTTP_ARG_MAC)
  strVersion = getArg(environ, portable_firmware_constants.strHTTP_ARG_VERSION)

  p = config_http_server.factoryGitHubPull()
  strVersionGit = p.setMac(strMac)

  if strPathInfo == portable_firmware_constants.strHTTP_PATH_SOFTWAREUPDATE:
    # GET /softwareupdate?mac=3C71BF0F97A4&version=heads-SLASH-master;1
    strTarFilename = p.strTarFilename
    strTarContent = p.getTarContent()
    if strTarContent == None:
      # Unknown Mac
      # Return "204 No content"
      raise WsgiException('', strStatus=strSTATUS_204)

    return responseBytes(start_response, strTarContent, strFilename=strTarFilename, strStatus=strSTATUS_200, strContentType=strCONTENTTYPE_BINARY)

  if strPathInfo == portable_firmware_constants.strHTTP_PATH_VERSIONCHECK:
    # GET /versioncheck?mac=3C71BF0F97A4&version=heads-SLASH-master;1
    return ok(start_response, strVersionGit, strContentType=strCONTENTTYPE_TEXT)

  raise WsgiException('Unkown path "%s"!' % environ['PATH_INFO'])

def handle_post(environ, start_response):
  # Returns a dictionary in which the values are lists
  d = cgi.parse_qs(environ['QUERY_STRING'])

  if environ['PATH_INFO'] == config_app.strHttpPostPath:
    import python3_http_influxdb_loadfiles

    # http://localhost/push/upload.grafana
    strMac = getArg(environ, portable_firmware_constants.strHTTP_ARG_MAC)
    strFilename = getArg(environ, portable_firmware_constants.strHTTP_ARG_FILENAME)

    # When the method is POST the variable will be sent^M
    # in the HTTP request body which is passed by the WSGI server^M
    # in the file like wsgi.input environment variable.^M
    try:
      request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
      request_body_size = 0
    strLogData = environ['wsgi.input'].read(request_body_size)
    strLogData = strLogData.decode('utf-8')

    if len(strLogData) == 0:
      return badRequest(start_response, 'No data received!')

    strFilenameFull = python3_http_influxdb_loadfiles.http_write_data(strMac, strFilename, strLogData)
    strRespone = "<p>strLogData: '%s'...<p>\n" % strLogData[0:10]
    strRespone += "<p>strFilenameFull: '%s'<p>\n" % strFilenameFull

    return ok(start_response, strRespone, strContentType=strCONTENTTYPE_HTML)

  raise WsgiException(start_response, 'Unkown path "%s"!' % environ['PATH_INFO'])

def application(environ, start_response):
  try:
    if environ['REQUEST_METHOD'] == 'GET':
      return handle_get(environ, start_response)
    
    if environ['REQUEST_METHOD'] == 'POST':
      return handle_post(environ, start_response)

    return badRequest(start_response, 'Unkown method "%s"!' % environ['REQUEST_METHOD'])

  except WsgiException as e:
    return e.getBadResponse(start_response)
  
  except:
    import traceback
    strResonse = traceback.format_exc()
    sys.stderr.write(strResonse + '\n')
    return badRequest(start_response, strResonse)

