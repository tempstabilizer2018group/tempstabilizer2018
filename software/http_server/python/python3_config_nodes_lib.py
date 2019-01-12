# -*- coding: utf-8 -*-

# Node
MAC = 'strMac'
NAME = 'strName'
SERIAL = 'strSerial'
LAB_NAME = 'strLabName'
LAB_LABEL = 'strLabLabel'
DICT_NODE = 'dictNode'
# Lab
RESPONSIBLE = 'strResposible'
GIT_REPO = 'strGitRepo'
GIT_TAGS = 'strGitTags'
NODES = 'listNodes'
DICT_LAB = 'dictLab'
# Container
LIST_NODES = 'listNodes'
LIST_LABS = 'listLabs'

class ConfigNode:
  def __init__(self, dictLab, dictNode):
    self.__dictLab = dictLab
    self.__dictNode = dictNode

  @property
  def strMac(self):
    return self.__dictLab[MAC]

  @property
  def strSerial(self):
    return self.__dictNode[SERIAL]

  @property
  def strGitRepo(self):
    return self.__dictLab[GIT_REPO]

  @property
  def strGitTags(self):
    return self.__dictLab[GIT_TAGS]

  @property
  def strLabLabel(self):
    return self.__dictLab[LAB_LABEL]

class ConfigNodes:
  def __init__(self, dictConfigNodes):
    self.__dictConfigNodes = dictConfigNodes

  def findNodeByMac(self, strMac):
    # Find first the node
    for dictNode in self.__dictConfigNodes[LIST_NODES]:
       if strMac == dictNode[MAC]:
         break
    else:
      raise Exception('No node with mac "%s" found.' % strMac)

    strSerial = dictNode[SERIAL]
    for dictLab in  self.__dictConfigNodes[LIST_LABS]:
      if strSerial in dictLab[NODES]:
        return ConfigNode(dictLab, dictNode)

    raise Exception('Mac "%s" has serial "%s". But no lab uses this serial.' % (strMac, strSerial))

  def verifyConsistency(self):
    dictSerial2Lab = {}
    # Loop throug all nodes to verify if they are defined
    for dictNode in self.__dictConfigNodes[LIST_NODES]:
      strMac = dictNode[MAC]
      strHexUppderCase = '0123456789ABCDEF'
      if not all(c in '0123456789ABCDEF' for c in strMac):
        raise Exception('Mac "%s" must only contain uppercase characters "%s".' % (strMac, strHexUppderCase))
      # Success, we get here!
      objConfigNode = self.findNodeByMac(strMac)
      strSerial = objConfigNode.strSerial
      strLabLabel = objConfigNode.strLabLabel
      strLabLabel_ = dictSerial2Lab.get(strSerial, None)
      if strLabLabel_ != None:
        raise Exception('Mac "%s" may not be in two labs: %s/%s.' % (strLabLabel, strLabLabel_))

      dictSerial2Lab[strSerial] = objConfigNode.strLabLabel

def testConsitencyLabs(listLabs):
  ''' 
    Test if the configuration may collect all files from github.
  '''
  import python3_github_pull

  for dictLab in listLabs:
    try:
      p = python3_github_pull.GithubPull(strDirectory='.')
      p.setTags(dictLab[GIT_TAGS])
      strTarFilenameFull = p.getTar()
      print('Lab "%s": %s' % (dictLab[LAB_LABEL], strTarFilenameFull))
    except Exception:
      print('ERROR in Lab "%s"' % dictLab[LAB_LABEL])
      raise
