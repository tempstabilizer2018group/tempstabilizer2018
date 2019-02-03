# -*- coding: utf-8 -*-

from python3_config_nodes_lib import *

listNodes = []
listLabs = []

# Version 20180907
listNodes.append({ MAC: '3C71BF0F97A4', SERIAL: '20180907_01', NAME: 'steel', })
listNodes.append({ MAC: '840D8E1BC40C', SERIAL: '20180907_03', NAME: 'aluminium', })

# Version 20181217
listNodes.append({ MAC: '3C71BF16D068', SERIAL: '20181217_11', NAME: '11', })
listNodes.append({ MAC: '3C71BF16D090', SERIAL: '20181217_12', NAME: '12', })
listNodes.append({ MAC: '3C71BF16D070', SERIAL: '20181217_13', NAME: '13', })
listNodes.append({ MAC: '3C71BF16BC9C', SERIAL: '20181217_14', NAME: '14', })
listNodes.append({ MAC: '3C71BF16D064', SERIAL: '20181217_15', NAME: '15', })
listNodes.append({ MAC: '3C71BF16D038', SERIAL: '20181217_16', NAME: '16', })
listNodes.append({ MAC: '3C71BF16D098', SERIAL: '20181217_17', NAME: '17', })
listNodes.append({ MAC: '807D3AF3288C', SERIAL: '20181217_18', NAME: '18', })
listNodes.append({ MAC: '3C71BF16D044', SERIAL: '20181217_19', NAME: '19', })
listNodes.append({ MAC: '3C71BF16D020', SERIAL: '20181217_20', NAME: '20', })
listNodes.append({ MAC: '3C71BF16D03C', SERIAL: '20181217_21', NAME: '21', })
listNodes.append({ MAC: '3C71BF16BCA0', SERIAL: '20181217_22', NAME: '22', })
listNodes.append({ MAC: '3C71BF16BCC0', SERIAL: '20181217_23', NAME: '23', })
listNodes.append({ MAC: '3C71BF16D05C', SERIAL: '20181217_24', NAME: '24', })
listNodes.append({ MAC: '3C71BF16BCA4', SERIAL: '20181217_25', NAME: '25', })

listLabs.append({
  LAB_LABEL: 'labHombi',
  LAB_NAME: 'hombrechtikon',
  RESPONSIBLE: 'Peter Maerki',
  GIT_REPO: 'tempstabilizer2018group/tempstabilizer2018',
  # Select a tag: 'tags/v1.0.0'
  # Select the head of a branch: 'heads/master', 'heads/branchX'
  # GIT_TAGS: 'tags/x1.0;tags/y1.1',
  #
  # Examples
  # ;config_app.setVirgin()
  # ;config_app.iHwLedModulo=30
  # ;config_app.setFixtemp(27.0)
  # ;config_app.iPollForWlanInterval_ms=60*60*1000
  # ;config_app.setOff()
  GIT_TAGS: 'heads/master;1',
  NODES: (
    ('20180907_01', ''),

    ('20181217_11', ''),
    ('20181217_12', ''),
    ('20181217_13', ''),
    ('20181217_14', ''),
    ('20181217_15', ''),
    ('20181217_16', ''),
    ('20181217_17', ''),
    ('20181217_18', ';config_app.setFixtemp(20.0)'),
    ('20181217_19', ''),
    ('20181217_20', ''),
    ('20181217_21', ''),
    ('20181217_22', ''),
    ('20181217_23', ''),
    ('20181217_24', ''),
    ('20181217_25', ''),
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
    ('20180907_03', ''),
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

  if False:
    import config_http_server
    p = config_http_server.factoryGitHubPull()
    strTarFilenameFull = p.getTar()
    pass
