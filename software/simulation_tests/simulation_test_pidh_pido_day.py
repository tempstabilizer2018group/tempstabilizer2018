# -*- coding: utf-8 -*-
import portable_ticks
import portable_constants
import config_app
import portable_daymaxestimator
import simulation_controller

iMaxTicks_ms = portable_daymaxestimator.TIME_PROCESS_DAYMAXESTIMATOR_MS
config_app.iSimulationInitiMaxTicks_ms = int(1.33*iMaxTicks_ms)

config_app.iLogSimuliertPlotInterval_ms = min(iMaxTicks_ms, portable_constants.HOUR_MS)
config_app.iLogInterval_ms = config_app.iLogSimuliertPlotInterval_ms
config_app.iExperimentDuration_ms = 2*portable_constants.DAY_MS
config_app.fStart_Increment_fTempO_C = 0.0 # Soll beim Start nicht heizen

if __name__ == '__main__':
  controller = simulation_controller.SimuliertController(__file__)
  controller.runForever()
