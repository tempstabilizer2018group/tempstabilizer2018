# -*- coding: utf-8 -*-
import portable_constants
import config_app
import portable_ticks
import portable_tempstabilizer
import portable_simuliert_tagesmodell
import hw_controller

config_app.iLogInterval_ms = 1 * portable_constants.SECOND_MS
config_app.iExperimentDuration_ms = 6*portable_constants.MINUTE_MS

listTemperatures_ms = (
  (0, 0.0),
  (int(0.1*config_app.iExperimentDuration_ms), 1.0),
  (int(0.5*config_app.iExperimentDuration_ms), 2.0),
  (int(0.9*config_app.iExperimentDuration_ms), -1.0),
)
iTimeEnd_ms = int(1.1*config_app.iExperimentDuration_ms)

objMyTagesmodell = portable_simuliert_tagesmodell.TagesmodellList(listTemperatures_ms)
fTempH_Start = None

class MyTempStabilizer(portable_tempstabilizer.TempStabilizer):
  '''
    TempStabilizer is overridden and returns fTempH_Setpoint_C
  '''
  @property
  def fTempH_Setpoint_C(self):
    # Gibt die Temperatur des Tagesmodells zurück
    return fTempH_Start + objMyTagesmodell.get_fTemp_C(iTime_ms=portable_ticks.objTicks.time_ms())

class MyController(hw_controller.HwController):
  def factoryHw(self):
    objHw = hw_controller.HwController.factoryHw(self)
    global fTempH_Start
    fTempH_Start = objHw.messe_fTempH_C
    return objHw

  def factoryTempStabilizer(self):
    return MyTempStabilizer()

controller = MyController(__file__)
controller.runForever()
