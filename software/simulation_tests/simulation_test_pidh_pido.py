# -*- coding: utf-8 -*-
import portable_ticks
import portable_constants
import config_app
import portable_daymaxestimator
import portable_tempstabilizer
import simulation_pyplot
import portable_simuliert_tagesmodell
import simulation_controller
import simulation_hw_hal

config_app.iLogSimuliertPlotInterval_ms = 5*portable_constants.SECOND_MS
config_app.iLogInterval_ms = config_app.iLogSimuliertPlotInterval_ms
config_app.iExperimentDuration_ms = 500*portable_constants.SECOND_MS
config_app.iTimeProcess_O_H_ms = 10
config_app.fStart_Increment_fTempO_C = 0.1 # Damit es etwas zu Heizen gibt

listTemperatures_ms = (
  (0, 19.0),
  (int(0.05*config_app.iExperimentDuration_ms), 20.1),
  (int(0.3*config_app.iExperimentDuration_ms), 20.2),
  (int(0.6*config_app.iExperimentDuration_ms), 20.1),
)
iTimeEnd_ms = int(1.1*config_app.iExperimentDuration_ms)

objMyTagesmodell = portable_simuliert_tagesmodell.TagesmodellList(listTemperatures_ms)

class MyTempStabilizer(portable_tempstabilizer.TempStabilizer):
  '''
    TempStabilizer is overridden and returns fTempO_Setpoint_C
  '''
  @property
  def fTempO_Setpoint_C(self):
    # Gibt die Temperatur des Tagesmodells zurück
    iTime_ms = portable_ticks.objTicks.time_ms()
    return objMyTagesmodell.get_fTemp_C(iTime_ms=iTime_ms)

class MyController(simulation_controller.SimuliertController):
  def factoryTempStabilizer(self):
    return MyTempStabilizer()

  def factoryHw(self):
    '''
      This hardware provides a constant environment-temperature.
    '''
    return simulation_hw_hal.Hw(objTagesmodell=portable_simuliert_tagesmodell.TagesmodellConstant(fTempEnvirons_C=19.5))

if __name__ == '__main__':
  controller = MyController(__file__)
  controller.runForever()
