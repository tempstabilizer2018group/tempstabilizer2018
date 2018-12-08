# -*- coding: utf-8 -*-

import io
import os
import logging

# https://docs.python.org/3/library/tarfile.html
import tarfile

# pip3 install PyGithub
# https://pygithub.readthedocs.io/en/latest/introduction.html
import github

# Rate Limit
# https://api.github.com/rate_limit
# https://developer.github.com/v3/rate_limit/
# https://developer.github.com/v3/#rate-limiting

# https://raw.githubusercontent.com/hmaerki/temp_stabilizer_2018/master/software/http_server/python/config_http_server.py

import python3_config_nodes_lib

strGithubRepoConfig = 'hmaerki/temp_stabilizer_2018'
strGithubUser = 'tempstabilizer2018user'
strGithubPw = 'xxx'
strGithubToken = None

strFILENAME_CONFIG_NODES = '/software/http_server/python/config_nodes.py'
strDIRECTORY_NODE = 'software/node'
assert strFILENAME_CONFIG_NODES.startswith('/')
assert '\\' not in strFILENAME_CONFIG_NODES
assert not strDIRECTORY_NODE.startswith('/')
assert '\\' not in strDIRECTORY_NODE

listReplacements = (
    ('_', '-UNDERSCORE-'),
    ('/', '-SLASH-'),
    (';', '-SEMICOLON-'),
    (':', '-COLON-'),
)

def escape(s):
  for strChar, strEscape in listReplacements:
    s = s.replace(strChar, strEscape)
  return s

strFILENAME_VERSION = 'VERSION.TXT'

class GithubPull:
  def __init__(self, strDirectory=None):
    if strDirectory == None:
      strDirectory = os.path.join(os.path.dirname(__file__), '..', 'webroot')
    self.__strDirectory = os.path.abspath(strDirectory)

  def setMac(self, strMac):
    # Get the most actual config file from github
    objConfigNodes = self.__getConfigNodesFromGithub()

    # Find the mac we are looking for
    objNode = objConfigNodes.findNodeByMac(strMac)

    # remember it
    self.setTags(objNode.strGitRepo, objNode.strGitTags, objNode.strUserTag)

  def setTags(self,  strGitRepo, strGitTags, strUserTag):
    self.__strGitRepo = strGitRepo
    self.__strGitTags = strGitTags
    # Escape characters in the tags, but not the ';' between the git-tags
    strGitTags = ';'.join(map(escape, strGitTags.split(';')))
    strUserTag = escape(strUserTag)

    self.__strTarFilename = 'node_%s_%s.tar' % (strGitTags, strUserTag)
    self.__strTarFilenameFull = os.path.join(self.__strDirectory, self.__strTarFilename)

  def __openRepo(self, strGithubRepo):
    # objGithub = github.Github(strGithubUser, strGithubPw)
    if strGithubToken == None:
      objGithub = github.Github()
    else:
      objGithub = github.Github(login_or_token=strGithubToken)
    return objGithub.get_repo(strGithubRepo)

  def __getConfigNodesFromGithub(self):
    '''
      We read 'config_nodes.py' from github.
      Then we call findTagsByMac(strMac) to get strGitTags, strUserTag
    '''
    logging.info('Get "config_nodes.py" from github....')
    dictConfigNodes = self._getConfigNodesFromGithub2()
    objConfigNodes = python3_config_nodes_lib.ConfigNodes(dictConfigNodes)
    return objConfigNodes

  def _getConfigNodesFromGithub2(self):
    objGitRepro = self.__openRepo(strGithubRepoConfig)
    objGitFile = objGitRepro.get_file_contents(path=strFILENAME_CONFIG_NODES, ref='heads/master')
    strConfigNodes = objGitFile.decoded_content
    dictGlobals = {}
    dictLocals = {}
    exec(strConfigNodes, dictGlobals, dictLocals)
    return dictLocals['dictConfigNodes']

  def getTar(self):
    if os.path.exists(self.__strTarFilenameFull):
      logging.info('Tarfile already in cache. skip download....')
      return self.__strTarFilenameFull
    dictFiles = self._fetchFromGithub()
    self.__writeTar(dictFiles)
    return self.__strTarFilenameFull

  def _selectFile(self, strFilenameRelative):
    '''
      strFilenameRelative is absolute within the Git-repostitory and in the local filesystem relativ to the Git-root.
      The filename returned is relative to the node-folder which will be deployed to the target.
    '''
    assert not strFilenameRelative[0] in r'.\/'
    if not strFilenameRelative.startswith(strDIRECTORY_NODE):
      # We are only interested in files of the node-directory
      return None
    strFilenameRelative2 = strFilenameRelative[len(strDIRECTORY_NODE)+1:]
    if strFilenameRelative2.endswith('.py'):
      # We are only interested in python-files
      return strFilenameRelative2
    return None

  def _fetchFromGithub(self):
    objGitRepro = self.__openRepo(self.__strGitRepo)

    dictFiles = {}

    for strGitTag in self.__strGitTags.split(';'):
      logging.debug('  Tag: %s' % strGitTag)
      try:
        objGitTag = objGitRepro.get_git_ref(strGitTag)
      except github.UnknownObjectException:
        raise Exception('Tag "%s" does not exist in git-repository "%s"' % (strGitTag, self.__strGitRepo))

      objGitTree = objGitRepro.get_git_tree(objGitTag.object.sha, recursive=True)
      for objGitFile in objGitTree.tree:
        logging.debug('    File: %s' % objGitFile.path)
        strFilenameRelative2 = self._selectFile(objGitFile.path)
        if strFilenameRelative2 == None:
          continue
        if objGitFile.path in dictFiles:
          logging.debug('      Alreadey added, would be overwritten - skipped....')
          continue
        if objGitFile.type != 'blob':
          logging.debug('      Not a blob, skipped....')
          continue
        objGitContents = objGitRepro.get_file_contents(path=objGitFile.path, ref=strGitTag)
        dictFiles[strFilenameRelative2] = objGitContents.decoded_content
    return dictFiles

  def __writeTar(self, dictFiles):
    dictFiles[strFILENAME_VERSION] = bytes(self.__strTarFilename.encode('utf8'))

    with tarfile.open(self.__strTarFilenameFull, 'w') as tar:
      for strFilename, byteData in dictFiles.items():
        info = tarfile.TarInfo(name=strFilename)
        info.size = len(byteData)
        tar.addfile(info, io.BytesIO(byteData))

class GitHubPullLocal(GithubPull):
  '''
    Instead of connecting to Github, this class reads from the local filesystem.
    This is useful when developing software on the raspberry pi: When the node
    does an update, the local code will be deployed.
  '''
  def __init__(self, strDirectory=None):
    import config_nodes
    self.__strSourceDirectory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    self.__dictConfigNodes = config_nodes.dictConfigNodes

    GithubPull.__init__(self, strDirectory)
  
  def _getConfigNodesFromGithub2(self):
    return self.__dictConfigNodes

  def _fetchFromGithub(self):
    dictFiles = {}
    for strRootDirectory, listDirsDummy, listFilenames in os.walk(self.__strSourceDirectory):
      if strRootDirectory.find(r'\.') >= 0:
        # For example the '.git'-directory
        continue

      assert strRootDirectory.startswith(self.__strSourceDirectory)
      strRootDirectoryRelative = strRootDirectory[len(self.__strSourceDirectory)+1:]
      strRootDirectoryRelative = strRootDirectoryRelative.replace('\\', '/')
      for strFilename in listFilenames:
        strFilenameRelative = strRootDirectoryRelative + '/' + strFilename
        strFilenameRelative2 = self._selectFile(strFilenameRelative)
        if strFilenameRelative2 == None:
          continue
        print(strFilenameRelative2)
        strFilenameFull = os.path.join(strRootDirectory, strFilename)
        with open(strFilenameFull, 'r', encoding='utf-8') as fIn:
          strContents = fIn.read()
          strContents = strContents.encode('utf8')
          dictFiles[strFilenameRelative2] = strContents
    return dictFiles

if __name__ == '__main__':
  pass
  # p = GithubPull('x1.0;y1.1')
  # strTarFilenameFull = p.getTar()
