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

import python3_config_nodes_lib

strGithubRepoConfig = 'hmaerki/temp_stabilizer_2018'
strGithubUser = 'tempstabilizer2018user'
strGithubPw = 'xxx'
strGithubToken = 'xxxxx'

strNodesFile = '/software/http_server/python/config_nodes.py'
strNodeDirectory = 'software/node'

# https://raw.githubusercontent.com/hmaerki/temp_stabilizer_2018/master/software/http_server/python/config_http_server.py


class GithubPull:
  def __init__(self, strDirectory):
    self.__strDirectory = strDirectory

  def setMac(self, strMac):
    # Get the most actual config file from github
    objConfigNodes = self.__getConfigNodesFromGithub()

    # Find the mac we are looking for
    objNode = objConfigNodes.findNodeByMac(strMac)

    # remember it
    self.setTags(objNode.strGitRepo, objNode.strGitTags, objNode.strUserTag)

  def setTags(self,  strGitRepo, strGitTags, strUserTag):
    for strGitTag in strGitTags.split(';'):
      self.__testAllowedCharacters(strGitTag)
    self.__testAllowedCharacters(strUserTag)

    self.__strGitRepo = strGitRepo
    self.__strGitTags = strGitTags
    self.__strTarFilename = 'node_%s_%s.tar' % (strGitTags, strUserTag)
    self.__strTarFilenameFull = os.path.join(self.__strDirectory, self.__strTarFilename)

  def __openRepo(self, strGithubRepo):
    # objGithub = github.Github(strGithubUser, strGithubPw)
    objGithub = github.Github()
    # objGithub = github.Github(login_or_token=strGithubToken)
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
    objGitFile = objGitRepro.get_file_contents(path=strNodesFile, ref='master')
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

  def __testAllowedCharacters(self, strTag):
    strCharactersForbidden = "_;:"
    for c in strCharactersForbidden:
      if c in strTag:
        raise Exception(' Tag "%s" must not contain %s' % (strTag, '/'.join(strCharactersForbidden)))

  def _fetchFromGithub(self):
    objGitRepro = self.__openRepo(self.__strGitRepo)

    dictFiles = {}

    for strGitTag in self.__strGitTags.split(';'):
      logging.debug('  Tag:', strGitTag)
      try:
        objGitTag = objGitRepro.get_git_ref('tags/' + strGitTag)
      except github.UnknownObjectException:
        raise Exception('Tag "%s" does not exist in git-repository "%s"' % (strGitTag, self.__strGitRepo))

      objGitTree = objGitRepro.get_git_tree(objGitTag.object.sha, recursive=True)
      for objGitFile in objGitTree.tree:
        logging.debug('    File:', objGitFile.path)
        if objGitFile.path in dictFiles:
          logging.debug('      Alreadey added, would be overwritten - skipped....')
          continue
        if objGitFile.type != 'blob':
          logging.debug('      Not a blob, skipped....')
          continue
        objGitContents = objGitRepro.get_file_contents(path=objGitFile.path, ref=strGitTag)
        dictFiles[objGitFile.path] = objGitContents.decoded_content
    return dictFiles

  def __writeTar(self, dictFiles):
    with tarfile.open(self.__strTarFilenameFull, 'w') as tar:
      for strFilename, strContents in dictFiles.items():
        data = strContents # .encode('utf8')
        info = tarfile.TarInfo(name=strFilename)
        info.size = len(data)
        tar.addfile(info, io.BytesIO(data))

class GitHubPullLocal(GithubPull):
  '''
    Instead of connecting to Github, this class reads from the local filesystem.
    This is useful when developing software on the raspberry pi: When the node
    does an update, the local code will be deployed.
  '''
  def __init__(self, strDirectory):
    import config_nodes
    self.__strSourceDirectory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    self.__dictConfigNodes = config_nodes.dictConfigNodes

    GithubPull.__init__(self, strDirectory)
  
  def _getConfigNodesFromGithub2(self):
    return self.__dictConfigNodes

  def _selectFile(self, strFilenameRelative):
    '''
      strFilenameRelative is absolute within the Git-repostitory and in the local filesystem relativ to the Git-root.
      The filename returned is relative to the node-folder which will be deployed to the target.
    '''
    if strFilenameRelative.startswith('.'):
      # For example '.git/file.y'
      return False
    assert not strFilenameRelative[0] in r'.\/'
    if strFilenameRelative.endswith('.py'):
      # We are only interested in python-files
      if strFilenameRelative.startswith(strNodeDirectory):
        # We are only interested in files of the node-directory
        # True: This file will be deployed to the node
        return strFilenameRelative[len(strNodeDirectory):]
    return None

  def _fetchFromGithub(self):
    dictFiles = {}
    for strRootDirectory, listDirsDummy, listFilesnames in os.walk(self.__strSourceDirectory):
      for strFilename in listFilesnames:
        strFilenameFull = os.path.abspath(os.path.join(strRootDirectory, strFilename))
        assert strFilenameFull.startswith(self.__strSourceDirectory)
        strFilenameRelative = strFilenameFull[len(self.__strSourceDirectory)+1:]
        strFilenameRelative2 = self._selectFile(strFilenameRelative)
        if strFilenameRelative2 == None:
          continue
        with open(strFilenameFull, 'r') as fIn:
          strContents = fIn.read()
        dictFiles[strFilenameRelative2] = strContents


if __name__ == '__main__':
  pass
  # p = GithubPull('x1.0;y1.1')
  # strTarFilenameFull = p.getTar()
