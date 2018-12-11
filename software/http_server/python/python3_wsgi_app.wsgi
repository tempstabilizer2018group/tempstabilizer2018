# -*- coding: utf-8 -*-

import os
import sys
import cgi

strFileDirectory = os.path.dirname(__file__)
sys.path.append(strFileDirectory)
sys.path.append(os.path.join(strFileDirectory, '../../node/config'))
sys.path.append(os.path.join(strFileDirectory, '../../node/program'))

import config_app
import portable_firmware_constants

strSTATUS_200 = '200 OK'
strSTATUS_204 = '204 NO_CONTENT'
strSTATUS_301 = '301 MOVED_PERMANENTLY'
strSTATUS_400 = '400 BAD_REQUEST'
strCONTENTTYPE_TEXT = 'text/plain'
strCONTENTTYPE_HTML = 'text/html'
strCONTENTTYPE_BINARY = 'application/octet-stream'

def getContentType(strUrl):
  strExt = os.path.splitext(strUrl)[1]
  strContentType = dictContentTypes.get(strExt, strCONTENTTYPE_TEXT)
  return strContentType

def responseBytes(start_response, strMessage, strStatus=strSTATUS_200, strContentType=strCONTENTTYPE_TEXT):
  response_headers = [('Content-type', strContentType),
                ('Content-Length', str(len(strMessage)))]
  start_response(strStatus, response_headers)
  return [strMessage]

def response(start_response, strMessage, strStatus=strSTATUS_200, strContentType=strCONTENTTYPE_TEXT):
  strMessage = bytes(strMessage, encoding='utf-8')
  return responseBytes(start_response, strMessage, strStatus, strContentType)

class WsgiException(Exception):
  def __init__(self, strMessage, strStatus=strSTATUS_400):
    super().__init__(strMessage)
    self.strMessage = strMessage
    self.strStatus = strStatus

  def getBadResponse(self, start_response):
    return response(start_response, self.strMessage, strStatus=self.strStatus)

def badRequest(start_response, strMessage):
  return response(start_response, strMessage, strStatus=strSTATUS_400)

def ok(start_response, strMessage):
  return response(start_response, strMessage, strStatus=strSTATUS_200)

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

  if strPathInfo == '/':
    response_headers = [('Content-type', strCONTENTTYPE_TEXT),
                ('Content-Length', '0'),
                ('Location', '/index.html')]
    start_response(strSTATUS_301, response_headers)
    return [b'']

  strMac = getArg(environ, portable_firmware_constants.strHTTP_ARG_MAC)
  strVersion = getArg(environ, portable_firmware_constants.strHTTP_ARG_VERSION)

  p = python3_github_pull.GitHubPullLocal()
  strVersionGit = p.setMac(strMac)

  if strPathInfo == portable_firmware_constants.strHTTP_PATH_SOFTWAREUPDATE:
    # GET /softwareupdate?mac=3C71BF0F97A4&version=heads-SLASH-master;1
    strTarContent = p.getTarContent()
    if strTarContent == None:
      # Unknown Mac
      # Return "204 No content"
      raise WsgiException('', strStatus=strSTATUS_204)

    return responseBytes(start_response, strTarContent, strStatus=strSTATUS_200, strContentType=strCONTENTTYPE_BINARY)

  if strPathInfo == portable_firmware_constants.strHTTP_PATH_VERSIONCHECK:
    # GET /versioncheck?mac=3C71BF0F97A4&version=heads-SLASH-master;1
    return ok(start_response, strVersionGit)

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

    strFilenameFull = python3_http_influxdb_loadfiles.http_write_data(strMac, strFilename, strLogData)
    strRespone = "<p>strLogData: '%s'...<p>\n" % strLogData[0:10]
    strRespone += "<p>strFilenameFull: '%s'<p>\n" % strFilenameFull

    return ok(start_response, strRespone)

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
    return badRequest(start_response, strResonse)

