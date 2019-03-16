# -*- coding: utf-8 -*-
import pyplot
import portable_constants
import portable_ticks

import config_app
import portable_simuliert_tagesmodell_SKIP as portable_simuliert_tagesmodell
import portable_daymaxestimator
import portable_tempstabilizer

def doit(iTimeEnd_ms, iIncrementTicks_ms, strFilename, fFactorWeek_C=1.0, bPowerOffset=True):
  config_app.bPowerOffset = bPowerOffset
  portable_ticks.reset()
  portable_ticks.init(iMaxTicks_ms=portable_constants.YEAR_MS)

  objTagesmodell = portable_simuliert_tagesmodell.Tagesmodell(iTimeOffset=-8*portable_constants.HOUR_MS, fFactorWeek_C=fFactorWeek_C)
  objDayMaxEstimator = portable_daymaxestimator.DayMaxEstimator(portable_ticks.objTicks.ticks_ms())
  fTempO_Sensor = objTagesmodell.get_fTemp_C(iTime_ms=0)
  objDayMaxEstimator.start(portable_ticks.objTicks.ticks_ms(), fTempO_Sensor=fTempO_Sensor)

  objCurveTempSensor = pyplot.Curve('TempO_Sensor', 'blue')
  objCurveTempSetpoint = pyplot.Curve('TempO_Setpoint', 'green')
  objCurveHeat_W = pyplot.Curve('Heat_W', 'red')
  objCurveHeatMedian_W = pyplot.Curve('HeatMedian_W', 'orange')
  fTempO_Setpoint_C = 0.0

  for iTime_ms in range(0,  iTimeEnd_ms, iIncrementTicks_ms):
    fTempO_Sensor = objTagesmodell.get_fTemp_C(iTime_ms)
    assert iTime_ms == portable_ticks.objTicks.ticks_ms()
    portable_ticks.objTicks.increment_ticks_ms(iIncrementTicks_ms)
    bFetMin_W_Limit_Low = fTempO_Sensor >= fTempO_Setpoint_C

    objAvgTempO_C = portable_tempstabilizer.FloatAvg()
    objAvgTempO_C.push(fTempO_Sensor)

    objAvgHeat_W = portable_tempstabilizer.FloatAvg()
    fSimulatedAvgHeat_W = 1.0*(fTempO_Setpoint_C-fTempO_Sensor)
    fSimulatedAvgHeat_W = max(0.0, fSimulatedAvgHeat_W)
    objAvgHeat_W.push(fSimulatedAvgHeat_W)

    objDayMaxEstimator.process(portable_ticks.objTicks.ticks_ms(), objAvgTempO_C=objAvgTempO_C, objAvgHeat_W=objAvgHeat_W, bFetMin_W_Limit_Low=bFetMin_W_Limit_Low)

    fHeadMeadian_W = objDayMaxEstimator.objTemperatureList.getHeatMedian_W()
    fTempO_Setpoint_C = objDayMaxEstimator.fOutputValue
    fTime = float(iTime_ms)/portable_constants.HOUR_MS
    objCurveHeat_W.point(fTime, fSimulatedAvgHeat_W)
    objCurveHeatMedian_W.point(fTime, fHeadMeadian_W)
    objCurveTempSensor.point(fTime, fTempO_Sensor)
    objCurveTempSetpoint.point(fTime, fTempO_Setpoint_C)

  plot = pyplot.Plot('Time [h]')
  plot.PlotY1('Temperature [C]', objCurveTempSensor, objCurveTempSetpoint)
  plot.PlotY2('Power [W]', objCurveHeat_W, objCurveHeatMedian_W)
  # plot.PlotShow()
  plot.PlotSave(strFilename)
  portable_ticks.objTicks.print_statistics()

def run():
  doit(iTimeEnd_ms=1*portable_constants.WEEK_MS,
    iIncrementTicks_ms=6*portable_constants.MINUTE_MS,
    strFilename='simulation_test_dayestimator_fFactorWeek0.png',
    fFactorWeek_C=0.0,
    bPowerOffset=True)

  doit(iTimeEnd_ms=1*portable_constants.WEEK_MS,
    iIncrementTicks_ms=6*portable_constants.MINUTE_MS,
    strFilename='simulation_test_dayestimator_fFactorWeek0_bPowerOffsetFalse.png',
    fFactorWeek_C=0.0,
    bPowerOffset=False)

  doit(iTimeEnd_ms=2*portable_constants.WEEK_MS,
    iIncrementTicks_ms=6*portable_constants.MINUTE_MS,
    strFilename='simulation_test_dayestimator.png')

  doit(iTimeEnd_ms=18*portable_constants.HOUR_MS,
    iIncrementTicks_ms=portable_constants.MINUTE_MS,
    strFilename='simulation_test_dayestimator_short.png')

if __name__ == "__main__":
  run()
