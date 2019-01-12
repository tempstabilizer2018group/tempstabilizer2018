# -*- coding: utf-8 -*-

from python3_config_nodes_lib import *

listNodes = []
listLabs = []

# Version 20180907
listNodes.append({ MAC: '3C71BF0F97A4', SERIAL: '20180907_01', NAME: 'steel', })
listNodes.append({ MAC: '840D8E1BC40C', SERIAL: '20180907_03', NAME: 'aluminium', })

# Version 20181217
listNodes.append({ MAC: '3C71BF16D068', SERIAL: '20181217_11', NAME: 'name_20181217_11', })
listNodes.append({ MAC: '3C71BF16D090', SERIAL: '20181217_12', NAME: 'name_20181217_12', })
listNodes.append({ MAC: '3C71BF16D070', SERIAL: '20181217_13', NAME: 'name_20181217_13', })
listNodes.append({ MAC: '3C71BF16BC9C', SERIAL: '20181217_14', NAME: 'name_20181217_14', })
listNodes.append({ MAC: '3C71BF16D064', SERIAL: '20181217_15', NAME: 'name_20181217_15', })
listNodes.append({ MAC: '3C71BF16D038', SERIAL: '20181217_16', NAME: 'name_20181217_16', })
listNodes.append({ MAC: '3C71BF16D098', SERIAL: '20181217_17', NAME: 'name_20181217_17', })
listNodes.append({ MAC: '807D3AF3288C', SERIAL: '20181217_18', NAME: 'name_20181217_18', })
listNodes.append({ MAC: '3C71BF16D044', SERIAL: '20181217_19', NAME: 'name_20181217_19', })
listNodes.append({ MAC: '3C71BF16D020', SERIAL: '20181217_20', NAME: 'name_20181217_20', })
listNodes.append({ MAC: '3C71BF16D03C', SERIAL: '20181217_21', NAME: 'name_20181217_21', })
listNodes.append({ MAC: '3C71BF16BCA0', SERIAL: '20181217_22', NAME: 'name_20181217_22', })
listNodes.append({ MAC: '3C71BF16BCC0', SERIAL: '20181217_23', NAME: 'name_20181217_23', })
listNodes.append({ MAC: '3C71BF16D05C', SERIAL: '20181217_24', NAME: 'name_20181217_24', })
listNodes.append({ MAC: '3C71BF16BCA4', SERIAL: '20181217_25', NAME: 'name_20181217_25', })

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

    '20181217_11',
    '20181217_12',
    '20181217_13',
    '20181217_14',
    '20181217_15',
    '20181217_16',
    '20181217_17',
    '20181217_18',
    '20181217_19',
    '20181217_20',
    '20181217_21',
    '20181217_22',
    '20181217_23',
    '20181217_24',
    '20181217_25',
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



