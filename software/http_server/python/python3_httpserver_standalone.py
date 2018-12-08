# -*- coding: utf-8 -*-

import os
import urllib
import http.server
import socketserver
import http

PORT = 80

DIR_BOARD_WEBROOT= 'webroot'
strUrlBoardDir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', DIR_BOARD_WEBROOT))

# http://localhost:8000/version.txt
# http://localhost:8000/filelist.txt
# http://localhost:8000/nodes/4711/version.txt
def run():
  os.chdir(strUrlBoardDir)
  print("serving at port", PORT)
  with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
    httpd.serve_forever()

if __name__=='__main__':
  run()
