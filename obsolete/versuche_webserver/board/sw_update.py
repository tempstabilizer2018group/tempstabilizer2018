import urequests
import uos

strBaseUrl = 'http://localhost:8000'
strProgramBasePath = 'program'
strParamBasePath = 'param'
FILENAME_VERSION = 'version.txt'
FILENAME_FILELIST = 'filelist.txt'

def downloadFile(strRelativeUrl, strFilename):
  strUrlFull = '%s/%s%s' % (strBaseUrl, strRelativeUrl, strFilename)
  # print(strUrlFull)
  try:
    response = urequests.get(strUrlFull)
    if response.status_code != 200:
      raise Exception('ERROR: %s returned %d' % (strUrlFull, response.status_code))
    return response.content.decode('ascii')
  finally:
    response.close()
 
def getLocalFilename(strRelativePath, strFilename):
  strFilenameFull = '%s/%s' % (strRelativePath, strFilename)
  return strFilenameFull

def versionChanged(strRelativeUrl, strRelativePath):
  strVersionServer = downloadFile(strRelativeUrl, FILENAME_VERSION)

  strFilenameFull = getLocalFilename(strRelativePath, FILENAME_VERSION)
  # print(strFilenameFull)
  with open(strFilenameFull, 'r') as f:
    strVersionClient = f.read()

  strVersionClient = strVersionClient.strip()
  strVersionServer = strVersionServer.strip()
  # print(strVersionServer, strVersionClient)
  bChanged = strVersionServer != strVersionClient
  return bChanged

strNodeRelativeUrl = 'nodes/4711/'
def getFilelist(strRelativeUrl, strRelativePath):
  return downloadFile(strRelativeUrl, FILENAME_FILELIST)

def deleteFilesInDirectory(strRelativePath):
  # print('deleteFilesInDirectory("%s")' % strRelativePath)
  for listFileTuple in uos.ilistdir(strRelativePath):
    strType = listFileTuple[1]
    if strType != 0x8:
      continue
    strFilename = listFileTuple[0]
    strFilenameFull = '%s/%s' % (strRelativePath, strFilename)
    print('deleteFilesInDirectory("%s")' % strFilenameFull)
    uos.unlink(strFilenameFull)
  
def writeFile(strRelativePath, strFilename, strContent):
  strFilenameFull = getLocalFilename(strRelativePath, strFilename)
  print('writeFile("%s")' % strFilenameFull)
  with open(strFilenameFull, 'w') as f:
    f.write(strContent)

def downloadFileAndWriteLocal(strRelativeUrl, strRelativePath, strFile):
  strContent = downloadFile(strRelativeUrl, strFile)
  writeFile(strRelativePath, strFile, strContent)

def downloadFiles(strRelativeUrl, strRelativePath):
  strFiles = getFilelist(strRelativeUrl, strRelativePath)
  listFiles = strFiles.split()
  for strFile in listFiles:
    downloadFileAndWriteLocal(strRelativeUrl, strRelativePath, strFile)

def downloadFilesIfVersionChanged(strRelativeUrl, strRelativePath):
  if versionChanged(strRelativeUrl, strRelativePath):
    deleteFilesInDirectory(strRelativePath)
    downloadFiles(strRelativeUrl, strRelativePath)
    downloadFileAndWriteLocal(strRelativeUrl, strRelativePath, FILENAME_VERSION)

downloadFilesIfVersionChanged('', strProgramBasePath)
downloadFilesIfVersionChanged(strNodeRelativeUrl, strParamBasePath)
