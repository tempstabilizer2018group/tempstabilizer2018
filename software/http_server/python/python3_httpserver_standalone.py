import os
import urllib
import http.server
import socketserver
import http

PORT = 8000

DIR_BOARD_WEBROOT='board_webroot'
strUrlBoardDir = os.path.join(os.path.abspath(os.path.dirname(__file__)), DIR_BOARD_WEBROOT)

# http://localhost:8000/version.txt
# http://localhost:8000/filelist.txt
# http://localhost:8000/nodes/4711/version.txt
def run():
  os.chdir(strUrlBoardDir)
  with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()

if __name__=='__main__':
  run()
