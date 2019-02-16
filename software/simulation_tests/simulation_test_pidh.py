# -*- coding: utf-8 -*-
import portable_ticks
import portable_constants
import config_app
import portable_tempstabilizer
import simulation_controller
import simulation_hw_hal
import portable_simuliert_tagesmodell
import simulation_pyplot

config_app.iLogSimuliertPlotInterval_ms = 1000
# TODO(Hans): Fix crash when enabling log
# config_app.iLogInterval_ms = config_app.iLogSimuliertPlotInterval_ms
config_app.iExperimentDuration_ms = 100 * 1000
config_app.iTimeProcess_O_H_ms = 10
config_app.fStart_Increment_fTempO_C = 0.1 # Damit es etwas zu Heizen gibt

listTemperatures_ms = (
  (0, 20.0),
  (int(0.1*config_app.iExperimentDuration_ms), 21.0),
  (int(0.5*config_app.iExperimentDuration_ms), 22.0),
  (int(0.7*config_app.iExperimentDuration_ms), 19.0),
)
iTimeEnd_ms = int(1.1*config_app.iExperimentDuration_ms)

objMyTagesmodell = portable_simuliert_tagesmodell.TagesmodellList(listTemperatures_ms)

class MyTempStabilizer(portable_tempstabilizer.TempStabilizer):
  '''
    TempStabilizer is overridden and returns fTempH_Setpoint_C
  '''
  @property
  def fTempH_Setpoint_C(self):
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
    return simulation_hw_hal.Hw(objTagesmodell=portable_simuliert_tagesmodell.TagesmodellConstant(fTempEnvirons_C=20.0))

  def logConsoleRemoveCurves(self):
    simulation_pyplot.deleteCurve('fTempO_Sensor_C')
    simulation_pyplot.deleteCurve('fTempO_Setpoint_C')

if __name__ == '__main__':
  controller = MyController(__file__)
  controller.runForever()
