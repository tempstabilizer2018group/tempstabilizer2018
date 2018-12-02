# -*- coding: utf-8 -*-
import config_app
import config_node

import portable_constants
import portable_ticks
import simulation_controller
import http_server_lib
import http_influxdb_loadfiles

config_node.strNode = 4712
config_node.strSite = 'httptest'

config_app.bUseNetwork = True
config_app.bSimulationUseHttpPost = False
config_app.iPollForWlanInterval_ms = 10*portable_constants.HOUR_MS
config_app.iLogSimuliertPlotInterval_ms = 10*portable_constants.MINUTE_MS
config_app.iLogInterval_ms = config_app.iLogSimuliertPlotInterval_ms
config_app.iExperimentDuration_ms = 1*portable_constants.HOUR_MS
config_app.iExperimentDuration_ms = 1*portable_constants.WEEK_MS
# config_app.iPollForWlanInterval_ms = 2 * config_app.iExperimentDuration_ms
config_app.fStart_Increment_fTempO_C = 0.0 # Soll beim Start nicht heizen

if False:
  # Little data and POST
  config_app.iExperimentDuration_ms = 30*portable_constants.MINUTE_MS
  config_app.iPollForWlanInterval_ms = 25*portable_constants.MINUTE_MS
  config_app.bSimulationUseHttpPost = True

if __name__ == '__main__':
  controller = simulation_controller.SimuliertController(__file__)
  controller.runForever()

  strDirectory = http_server_lib.strHttpServerToProcessDirectory
  if config_app.bUseNetwork:
    import simulation_http_server_utils
    strDirectory = simulation_http_server_utils.strNodeDataDirectory

  http_influxdb_loadfiles.processFiles(strDirectory, bWritePng=True)

