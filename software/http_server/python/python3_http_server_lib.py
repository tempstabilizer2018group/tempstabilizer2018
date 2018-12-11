# -*- coding: utf-8 -*-
import os
import time

strHttpServerDirectory = os.path.dirname(os.path.dirname(__file__))
strHttpServerToProcessDirectory = os.path.join(strHttpServerDirectory, 'node_data', 'grafana_to_process')
strHttpServerProcessedDirectory = os.path.join(strHttpServerDirectory, 'node_data', 'grafana_processed')
strHttpServerFailedDirectory = os.path.join(strHttpServerDirectory, 'node_data', 'grafana_failed')

def getTimeGmt():
  t = time.gmtime()
  strTime = time.strftime('%Y-%m-%d_%H-%M-%S', t)
  return strTime

def getToProcessFilenameFull(strFilenameBase, strMac, strTime=None):
  return os.path.join(strHttpServerToProcessDirectory, getToProcessFilename(strFilenameBase, strMac, strTime))

def getToProcessFilename(strFilenameBase, strMac, strTime=None):
  if strTime == None:
    strTime = getTimeGmt()
  return '%s_%s_%s.txt' % (strTime, strMac, strFilenameBase)

