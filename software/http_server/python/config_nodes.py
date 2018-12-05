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
  GIT_REPO: 'hmaerki/temp_stabilizer_2018',
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
  GIT_REPO: 'hmaerki/temp_stabilizer_2018',
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

  # Test if the configuration may collect all files from github.
  
  objConfigNodes = ConfigNodes(dictConfigNodes)
  objConfigNodes.verifyConsistency()

  if True:
    import python3_github_pull
    strMac = '840D8E1BC40C'
    if strMac == '840D8E1BC40C':
      p = python3_github_pull.GitHubPullLocal(strDirectory='.')
    else:
      p = python3_github_pull.GithubPull(strDirectory='.')
    p.setMac(strMac)
    strTarFilenameFull = p.getTar()

  if False:
    import python3_config_nodes_lib
    python3_config_nodes_lib.testConsitencyLabs(listLabs)



