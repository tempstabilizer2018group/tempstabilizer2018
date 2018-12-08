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
  GIT_REPO: 'tempstabilizer2018group/tempstabilizer2018',
  # Select a tag: 'tags/v1.0.0'
  # Select the head of a branch: 'heads/master', 'heads/branchX'
  # GIT_TAGS: 'tags/x1.0;tags/y1.1',
  GIT_TAGS: 'heads/master;1',
  NODES: (
    '20180907_01',
  )
})


listLabs.append({
  LAB_LABEL: 'labY',
  LAB_NAME: 'ETH, LabY',
  RESPONSIBLE: 'Robin',
  GIT_REPO: 'tempstabilizer2018group/tempstabilizer2018',
  # GIT_TAGS: 'tags/y1.1;tags/x1.0',
  GIT_TAGS: 'heads/master;1',
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
    if strMac == '840D8E1BC40x':
      p = python3_github_pull.GitHubPullLocal()
    else:
      # p = python3_github_pull.GitHubApiPull()
      p = python3_github_pull.GitHubPublicPull()
    p.setMac(strMac)
    strTarFilenameFull = p.getTar()
    pass

  if False:
    import python3_config_nodes_lib
    python3_config_nodes_lib.testConsitencyLabs(listLabs)



