# -*- coding: utf-8 -*-
import pyplot
import portable_constants
import portable_ticks

import portable_simuliert_tagesmodell
import portable_daymaxestimator

def doit(iTimeEnd_ms, iIncrementTicks_ms, strFilename):
  portable_ticks.reset()
  portable_ticks.init(iMaxTicks_ms=portable_constants.YEAR_MS)

  objTagesmodell = portable_simuliert_tagesmodell.Tagesmodell()
  objDayMaxEstimator = portable_daymaxestimator.DayMaxEstimator(portable_ticks.objTicks.ticks_ms())
  fTempO_Sensor = objTagesmodell.get_fTemp_C(iTime_ms=0)
  objDayMaxEstimator.start(portable_ticks.objTicks.ticks_ms(), fTempO_Sensor=fTempO_Sensor)

  objCurveTempSensor = pyplot.Curve('TempO_Sensor', 'blue')
  objCurveTempSetpoint = pyplot.Curve('TempO_Setpoint', 'green')
  fTempO_Setpoint_C = 0.0

  for iTime_ms in range(0,  iTimeEnd_ms, iIncrementTicks_ms):
    fTempO_Sensor = objTagesmodell.get_fTemp_C(iTime_ms)
    assert iTime_ms == portable_ticks.objTicks.ticks_ms()
    portable_ticks.objTicks.increment_ticks_ms(iIncrementTicks_ms)
    bFetMin_W_Limit_Low = fTempO_Sensor >= fTempO_Setpoint_C
    objDayMaxEstimator.process(portable_ticks.objTicks.ticks_ms(), fTempO_Sensor=fTempO_Sensor, bFetMin_W_Limit_Low=bFetMin_W_Limit_Low)
    fTempO_Setpoint_C = objDayMaxEstimator.fOutputValue
    objCurveTempSensor.point(float(iTime_ms)/portable_constants.HOUR_MS, fTempO_Sensor)
    objCurveTempSetpoint.point(float(iTime_ms)/portable_constants.HOUR_MS, fTempO_Setpoint_C)

  plot = pyplot.Plot('Time [h]')
  plot.PlotY1('Temperature [C]', objCurveTempSensor, objCurveTempSetpoint)
  plot.PlotSave(strFilename)
  portable_ticks.objTicks.print_statistics()

def run():
  doit(iTimeEnd_ms=2*portable_constants.WEEK_MS,
       iIncrementTicks_ms=6*portable_constants.MINUTE_MS,
       strFilename='simulation_test_dayestimator.png')

  doit(iTimeEnd_ms=10*portable_constants.HOUR_MS,
       iIncrementTicks_ms=portable_constants.MINUTE_MS,
       strFilename='simulation_test_dayestimator_short.png')

if __name__ == "__main__":
  run()
