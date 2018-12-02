# -*- coding: utf-8 -*-
import config_app
import portable_constants
import portable_simuliert_tagesmodell

def run1(objTagesmodell, strFilename, iTimeEnd_ms, iTimeIncrement_ms, iX_ms, strX_ms):
  import pyplot

  objCurveTemp = pyplot.Curve('Temp', 'blue')

  for iTime_ms in range(0, iTimeEnd_ms, iTimeIncrement_ms):
    fTemp_C = objTagesmodell.get_fTemp_C(iTime_ms)
    objCurveTemp.point(iTime_ms/float(iX_ms), fTemp_C)

  plot = pyplot.Plot('Time [%s]' % strX_ms)
  plot.PlotY1('Temperature [C]', objCurveTemp)
  plot.PlotSave(strFilename)

def run():
  run1(portable_simuliert_tagesmodell.Tagesmodell(), 'simulation_test_tagesmodell.png',
        iTimeEnd_ms=portable_constants.WEEK_MS,
        iTimeIncrement_ms=10*portable_constants.MINUTE_MS,
        iX_ms=portable_constants.HOUR_MS, strX_ms='h')

  config_app.iExperimentDuration_ms = 10000
  listTemperatures_ms = (
    (0, 19.0),
    (int(0.1*config_app.iExperimentDuration_ms), 21.0),
    (int(0.5*config_app.iExperimentDuration_ms), 22.0),
    (int(0.7*config_app.iExperimentDuration_ms), 19.0),
  )
  iTimeEnd_ms = int(1.1*config_app.iExperimentDuration_ms)

  run1(portable_simuliert_tagesmodell.TagesmodellList(listTemperatures_ms), 'simulation_test_tagesmodell_simple.png',
       iTimeEnd_ms=iTimeEnd_ms, iTimeIncrement_ms=100,
       iX_ms=1, strX_ms='ms')

if __name__ == "__main__":
  run()
