# -*- coding: utf-8 -*-

import wsgiref.simple_server

import python3_wsgi_app

PORT = 80

def run():
  httpd = wsgiref.simple_server.make_server('', PORT, python3_wsgi_app.application)
  print('Serving on port %d...' % PORT)
  httpd.serve_forever()

if __name__=='__main__':
  run()
