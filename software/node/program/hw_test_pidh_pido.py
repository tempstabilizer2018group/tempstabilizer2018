# -*- coding: utf-8 -*-
import portable_ticks
import portable_constants
import config_app
import portable_tempstabilizer
import portable_simuliert_tagesmodell
import hw_controller

config_app.iLogInterval_ms = 1 * portable_constants.SECOND_MS
config_app.iExperimentDuration_ms = 500*portable_constants.SECOND_MS

listTemperatures_ms = (
  (0, -0.5),
  (int(0.05*config_app.iExperimentDuration_ms), 0.1),
  (int(0.3*config_app.iExperimentDuration_ms), 0.7),
  (int(0.6*config_app.iExperimentDuration_ms), -0.5),
)
iTimeEnd_ms = int(1.1*config_app.iExperimentDuration_ms)

objMyTagesmodell = portable_simuliert_tagesmodell.TagesmodellList(listTemperatures_ms)
fTempO_Start = None

class MyTempStabilizer(portable_tempstabilizer.TempStabilizer):
  '''
    TempStabilizer is overridden and returns fTempO_Setpoint_C
  '''
  @property
  def fTempO_Setpoint_C(self):
    # Gibt die Temperatur des Tagesmodells zurück
    return fTempO_Start + objMyTagesmodell.get_fTemp_C(iTime_ms=portable_ticks.objTicks.time_ms())

class MyController(hw_controller.HwController):
  def factoryHw(self):
    objHw = hw_controller.HwController.factoryHw(self)
    global fTempO_Start
    fTempO_Start = objHw.messe_fTempO_C
    return objHw

  def factoryTempStabilizer(self):
    return MyTempStabilizer()

controller = MyController(__file__)
controller.runForever()
