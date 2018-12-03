from mod_python import apache

from urlparse import parse_qs
import time
import platform
import os.path

import python3_http_influxdb_loadfiles
import python3_http_server_lib
import config_node
import config_app

def write_data(strSite, strNode, strFilenameBase, strLogData):
  fSecondsSince1970_UnixEpochStart_EndOfFile = time.time()
  strTime = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(fSecondsSince1970_UnixEpochStart_EndOfFile))

  strFilenameFull = http_server_lib.getToProcessFilenameFull(strFilenameBase, config_node.strSite, config_node.strNode)

  print('strFilenameFull:'+strFilenameFull)

  with open(strFilenameFull, 'w') as fOut:
    fOut.write(strLogData)

    # Add a timestamp to the file
    fOut.write('1000 ntptime %d\n' % fSecondsSince1970_UnixEpochStart_EndOfFile)

  return strFilenameFull

def handler(req):
  req.content_type = "text/html"

  dictArgs = parse_qs(req.args)
  def getArg(strTag):
    listArg = dictArgs.get(strTag, None)
    if listArg == None:
      req.write("<p>args: '%s'</p>" % req.args)
      req.write("<p>ERROR: Required argument missing='%s'!</p>" % strTag)
      # raise(apache.SERVER_RETURN(apache.HTTP_BAD_REQUEST))
      raise(apache.SERVER_RETURN(apache.DONE))
    if len(listArg) == 0:
      req.write("<p>args: '%s'</p>" % req.args)
      req.write("<p>ERROR: Parameter for argument '%s' missing!</p>" % strTag)
      raise(apache.SERVER_RETURN(apache.DONE))
    return listArg[0]
         
  strSite = getArg('site')
  strNode = getArg('node')
  strFilename = getArg('filename')
  strDirectoryHttpServer = req.document_root()

  req.write("<p>python version: '%s'</p>" % platform.python_version())
  req.write("<p>strSite: '%s'</p>" % strSite)
  req.write("<p>strNode: '%s'</p>" % strNode)
  req.write("<p>strFilename: '%s'</p>" % strFilename)
  # req.write("<p>strTime: '%s'</p>" % strTime)
  req.write("<p>strDirectoryHttpServer: '%s'<p>" % strDirectoryHttpServer)
  req.write("<p>method: '%s'<p>" % req.method)

  if req.method == 'POST':
    strLogData = req.read()
    req.write("<p>strLogData: '%s'...<p>" % strLogData[0:10])
    strFilenameFull = write_data(strSite, strNode, strFilename, strLogData)
    req.write("<p>strFilenameFull: '%s'<p>" % strFilenameFull)

    http_influxdb_loadfiles.processFiles(http_server_lib.strHttpServerToProcessDirectory,
                                         http_server_lib.strHttpServerProcessedDirectory,
                                         http_server_lib.strHttpServerFailedDirectory,
                                         bWritePng=False)

  req.write("<p>---</p>")

  return apache.OK

