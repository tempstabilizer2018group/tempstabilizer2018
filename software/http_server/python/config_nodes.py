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
listNodes.append({ MAC: 'B4E62DF69969', SERIAL: '20181217_21', NAME: '21', }) # viele Bauteile ersetzt, uebel geloetet 
listNodes.append({ MAC: '3C71BF16BCA0', SERIAL: '20181217_22', NAME: '22', })
listNodes.append({ MAC: '3C71BF16BCC0', SERIAL: '20181217_23', NAME: '23', })
listNodes.append({ MAC: '3C71BF16D05C', SERIAL: '20181217_24', NAME: '24', })
listNodes.append({ MAC: '3C71BF16BCA4', SERIAL: '20181217_25', NAME: '25', })

listNodes.append({ MAC: '3C71BFA6E474', SERIAL: '20181217_99', NAME: 'devkitc', })

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
  # setVirgin: as new, no persistent history, no heating, polling for new version
  # ;config_app.setVirgin()
  # setFixtemp: heating to fix temperature
  # ;config_app.setFixtemp(27.0)
  # setOff: heating off, Setpoint and history persist, temperatures are measured and loged to grafana
  # ;config_app.setOff()
  # ;config_app.iPollForWlanInterval_ms=60*60*1000
  GIT_TAGS: 'heads/master;1',
  NODES: (
    ('20181217_22', ''),
    ('20181217_99', ''),
  )
})


listLabs.append({
  LAB_LABEL: 'ETH-E9',
  LAB_NAME: 'Hoenggerberg',
  RESPONSIBLE: 'Peter Maerki',
  GIT_REPO: 'tempstabilizer2018group/tempstabilizer2018',
  GIT_TAGS: 'heads/master;3;config_app.iPollForWlanInterval_ms=20*60*1000',
  NODES: (
    ('20181217_25', ''),
  )
})

listLabs.append({
  LAB_LABEL: 'ETH-eichlera',
  LAB_NAME: 'Hoenggerberg',
  RESPONSIBLE: 'Alexander Eichler',
  GIT_REPO: 'tempstabilizer2018group/tempstabilizer2018',
  GIT_TAGS: 'heads/master;3;config_app.iPollForWlanInterval_ms=20*60*1000',
  NODES: (
    ('20181217_17', ''),
    ('20181217_20', ''),
  )
})


listLabs.append({
  LAB_LABEL: 'HPF B18',
  LAB_NAME: 'ETH, HPF B18',
  RESPONSIBLE: 'Robin',
  GIT_REPO: 'tempstabilizer2018group/tempstabilizer2018',
  GIT_TAGS: 'heads/master;13;config_app.iPollForWlanInterval_ms=60*60*1000',
  NODES: (
    ('20180907_03', ''), 
    ('20181217_13', ''), # Aluklotz A, gross, mit EOM
    ('20181217_14', ''), # Aluklotz A, gross, mit EOM
    ('20181217_18', ''), # Aluklotz B, klein, mit EOM
    ('20181217_19', ''), # Aluklotz B, klein, mit EOM
    ('20181217_21', ''), # Auf Aluklotz 180x80x20 in Flowbox
  )
})

listLabs.append({
  LAB_LABEL: 'labReserve',
  LAB_NAME: 'dummy',
  RESPONSIBLE: 'Peter Maerki',
  GIT_REPO: 'tempstabilizer2018group/tempstabilizer2018',
  GIT_TAGS: 'heads/master;1',
  NODES: (
    ('20180907_01', ''),
    ('20181217_12', ''),
    ('20181217_15', ''), # heizt nicht, defekt   
    ('20181217_23', ''),
    ('20181217_24', ''),
    ('20181217_11', ''), # parat fuer Experimente  
    ('20181217_16', ''), # parat fuer Experimente 

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
