# -*- coding: utf-8 -*-

from python3_config_nodes_lib import *

listNodes = []
listLabs = []

listNodes.append({
  SERIAL: '20180907_01',
  MAC: '3C71BF0F97A4',
  NAME: 'steel',
})

listNodes.append({
  SERIAL: '20180907_03',
  MAC: '840D8E1BC40C',
  NAME: 'aluminium',
})

listLabs.append({
  LAB_LABEL: 'labHombi',
  LAB_NAME: 'hombrechtikon',
  RESPONSIBLE: 'Peter Maerki',
  GIT_TAGS: 'x1.0;y1.1',
  USER_TAG: '1',
  NODES: (
    '20180907_01',
  )
})


listLabs.append({
  LAB_LABEL: 'labY',
  LAB_NAME: 'ETH, LabY',
  RESPONSIBLE: 'Robin',
  GIT_TAGS: 'y1.1;x1.0',
  USER_TAG: '1',
  NODES: (
    '20180907_03',
  )
})

dictConfigNodes = {
  LIST_LABS: listLabs,
  LIST_NODES: listNodes,
}

if __name__ == '__main__':
  import python3_github_pull

  # Test if the configuration may collect all files from github.
  
  objConfigNodes = ConfigNodes(dictConfigNodes)
  objConfigNodes.verifyConsistency()
  if True:
    p = python3_github_pull.GithubPull(strDirectory='.')
    p.setMac('840D8E1BC40C')
    strTarFilenameFull = p.getTar()

  if False:
    for strMac in sorted(dictMacs.keys):
      dictMac = dictMacs[strMAC]
      print('  %s: "%s" %s %s' % (strMac, dictMac[LAB_NAME], dictMac[GIT_TAGS], dictMac[USER_TAG]))

  for dictLab in listLabs:
    try:
      p = python3_github_pull.GithubPull(strDirectory='.')
      p.setTags(dictLab[GIT_TAGS], strUserTag=dictLab[USER_TAG])
      strTarFilenameFull = p.getTar()
      print('Lab "%s": %s' % (dictLab[LAB_LABEL], strTarFilenameFull))
    except Exception:
      print('ERROR in Lab "%s"' % dictLab[LAB_LABEL])
      raise


