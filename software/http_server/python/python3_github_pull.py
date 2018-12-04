# -*- coding: utf-8 -*-

import io
import os
import logging

# https://docs.python.org/3/library/tarfile.html
import tarfile

# pip install PyGithub
# https://pygithub.readthedocs.io/en/latest/introduction.html
import github

# Rate Limit
# https://api.github.com/rate_limit
# https://developer.github.com/v3/rate_limit/
# https://developer.github.com/v3/#rate-limiting

import python3_config_nodes_lib

strGithubRepo = 'hmaerki/ota_test'
strGithubUser = 'tempstabilizer2018user'
strGithubPw = 'xxx'
strGithubToken = 'xxxxx'

strNodesFile = '/software/http_server/python/config_nodes.py'

# https://raw.githubusercontent.com/hmaerki/temp_stabilizer_2018/master/software/http_server/python/config_http_server.py


class GithubPull:
  def __init__(self, strDirectory):
    self.__strDirectory = strDirectory
    # objGithub = github.Github(strGithubUser, strGithubPw)
    # objGithub = github.Github()
    objGithub = github.Github(login_or_token=strGithubToken)
    self.__objGitRepro = objGithub.get_repo(strGithubRepo)

  def setMac(self, strMac):
    # Get the most actual config file from github
    objConfigNodes = self.__getConfigNodesFromGithub()

    # Find the mac we are looking for
    objNode = objConfigNodes.findNodeByMac('840D8E1BC40C')

    # remember it
    self.setTags(objNode.strGitTags, objNode.strUserTag)

  def setTags(self,  strGitTags, strUserTag):
    for strGitTag in strGitTags.split(';'):
      self.__testAllowedCharacters(strGitTag)
    self.__testAllowedCharacters(strUserTag)

    self.__strGitTags = strGitTags
    self.__strTarFilename = 'node_%s_%s.tar' % (strGitTags, strUserTag)
    self.__strTarFilenameFull = os.path.join(self.__strDirectory, self.__strTarFilename)

  def __getConfigNodesFromGithub(self):
    '''
      We read 'config_nodes.py' from github.
      Then we call findTagsByMac(strMac) to get strGitTags, strUserTag
    '''
    logging.info('Get "config_nodes.py" from github....')
    objGitFile = self.__objGitRepro.get_file_contents(path=strNodesFile, ref='master')
    strConfigNodes = objGitFile.decoded_content
    dictGlobals = {}
    dictLocals = {}
    exec(strConfigNodes, dictGlobals, dictLocals)
    dictConfigNodes = dictLocals['dictConfigNodes']
    objConfigNodes = python3_config_nodes_lib.ConfigNodes(dictConfigNodes)
    return objConfigNodes

  def getTar(self):
    if os.path.exists(self.__strTarFilenameFull):
      logging.info('Tarfile already in cache. skip download....')
      return self.__strTarFilenameFull
    dictFiles = self.__fetchFromGithub()
    self.__writeTar(dictFiles)
    return self.__strTarFilenameFull

  def __testAllowedCharacters(self, strTag):
    strCharactersForbidden = "_;:"
    for c in strCharactersForbidden:
      if c in strTag:
        raise Exception(' Tag "%s" must not contain %s' % (strTag, '/'.join(strCharactersForbidden)))

  def __fetchFromGithub(self):
    dictFiles = {}

    for strGitTag in self.__strGitTags.split(';'):
      logging.debug('  Tag:', strGitTag)
      try:
        objGitTag = self.__objGitRepro.get_git_ref('tags/' + strGitTag)
      except github.UnknownObjectException:
        raise Exception('Tag "%s" does not exist in git-repository "%s"' % (strGitTag, strGithubRepo))

      objGitTree = self.__objGitRepro.get_git_tree(objGitTag.object.sha, recursive=True)
      for objGitFile in objGitTree.tree:
        logging.debug('    File:', objGitFile.path)
        if objGitFile.path in dictFiles:
          logging.debug('      Alreadey added, would be overwritten - skipped....')
          continue
        if objGitFile.type != 'blob':
          logging.debug('      Not a blob, skipped....')
          continue
        objGitContents = self.__objGitRepro.get_file_contents(path=objGitFile.path, ref=strGitTag)
        dictFiles[objGitFile.path] = objGitContents.decoded_content
    return dictFiles

  def __writeTar(self, dictFiles):
    with tarfile.open(self.__strTarFilenameFull, 'w') as tar:
      for strFilename, strContents in dictFiles.items():
        data = strContents # .encode('utf8')
        info = tarfile.TarInfo(name=strFilename)
        info.size = len(data)
        tar.addfile(info, io.BytesIO(data))

if __name__ == '__main__':
  p = GithubPull('x1.0;y1.1')
  strTarFilenameFull = p.getTar()
