# -*- coding: utf-8 -*-
import os
import time

strHttpServerDirectory = os.path.dirname(os.path.dirname(__file__))
strHttpServerToProcessDirectory = os.path.join(strHttpServerDirectory, 'node_data', 'to_process')
strHttpServerProcessedDirectory = os.path.join(strHttpServerDirectory, 'node_data', 'processed')
strHttpServerFailedDirectory = os.path.join(strHttpServerDirectory, 'node_data', 'failed')

def getTimeGmt():
  t = time.gmtime()
  strTime = time.strftime('%Y-%m-%d_%H-%M-%S', t)
  return strTime

def getToProcessFilenameFull(strFilenameBase, strSite, strNode, strTime=None):
  return os.path.join(strHttpServerToProcessDirectory, getToProcessFilename(strFilenameBase, strSite, strNode, strTime))

def getToProcessFilename(strFilenameBase, strSite, strNode, strTime=None):
  if strTime == None:
    strTime = getTimeGmt()
  return '%s_%s_%s_%s.txt' % (strTime, strSite, strNode, strFilenameBase)

