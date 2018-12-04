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
GIT_TAGS = 'strGitTags'
USER_TAG = 'strUserTag'
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
  def mac(self):
    return self.__dictLab[MAC]

  @property
  def strGitTags(self):
    return self.__dictLab[GIT_TAGS]

  @property
  def strUserTag(self):
    return self.__dictLab[USER_TAG]

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
    # Loop throug all nodes to verify if they are defined
    for dictLab in self.__dictConfigNodes[LIST_LABS]:
      for strSerial in dictLab[NODES]:
        for dictNode in self.__dictConfigNodes[LIST_NODES]:
          strMac = dictNode[MAC]
          # Success, we get here!
          self.findNodeByMac(strMac)

