import os
import urllib
import http.server
import socketserver
import http

PORT = 8000

DIR_BOARD_WEBROOT='board_webroot'
strUrlBoardDir = os.path.join(os.path.abspath(os.path.dirname(__file__)), DIR_BOARD_WEBROOT)

class NodeDoesNotExistException(Exception):
  def __init__(self, strMessage):
    self.strMessage = strMessage

# strFilename: version.txt, 4711/version.txt
# strVersion: 123
def fileversionChanged(strFilename, strVersion):
  strFilenameFull = os.path.join(strUrlBoardDir, strFilename)
  if not os.path.exists(strFilenameFull):
    raise NodeDoesNotExistException('Files does not exist: ' + strFilenameFull)
  with open(strFilenameFull) as f:
    strData = f.read()
    bVersionChanged = strData != strVersion
    return bVersionChanged

def appendFiles(listFilenames, strDirectoryPath, strDirectoryUrl):
  strDirectoryFull = os.path.join(strUrlBoardDir, strDirectoryPath)
  for strFilename in os.listdir(strDirectoryFull):
    strFilenameFull = os.path.join(strDirectoryFull, strFilename)
    if os.path.isfile(strFilenameFull):
      strFilenameRelative = strDirectoryUrl + strFilename
      listFilenames.append(strFilenameRelative)

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
  # http://localhost:8000/filelist?program_version=122&param_version=3&node=4711
  def do_GET(self):
    objParts = urllib.parse.urlsplit(self.path)
    if objParts.path == '/filelist':
      dictQuery = urllib.parse.parse_qs(objParts.query)
      strNode = dictQuery['node'][0]
      strProgramVersion = dictQuery['program_version'][0]
      strParamVersion = dictQuery['param_version'][0]

      listFilenames = []
      try:
        if fileversionChanged('version.txt', strProgramVersion):
          appendFiles(listFilenames, '.', '')
        if fileversionChanged('%s/version.txt' % strNode, strParamVersion):
          appendFiles(listFilenames, strNode, strNode + '/')
        strResponse = '\n'.join(listFilenames)
      except NodeDoesNotExistException as ex:
        strResponse = 'ERROR: ' + ex.strMessage

      bResponse = strResponse.encode()
      self.send_response(http.HTTPStatus.OK)
      self.send_header("Content-type", 'text/plain')
      self.send_header("Content-Length", str(len(bResponse)))
      self.end_headers()
      self.wfile.write(bResponse)
      return
    http.server.SimpleHTTPRequestHandler.do_GET(self)

  # Get files
  # http://localhost:8000/version.txt
  # http://localhost:8000/4711/version.txt
  def translate_path(self, path):
    path = strUrlBoardDir + path
    # return http.server.SimpleHTTPRequestHandler.translate_path(self, path)
    return path

def run():
  with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()

if __name__=='__main__':
  run()
