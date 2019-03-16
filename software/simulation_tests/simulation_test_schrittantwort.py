# -*- coding: utf-8 -*-
import config_app
import portable_ticks
import portable_constants
import simulation_hw_hal
import portable_simuliert_tagesmodell_SKIP as portable_simuliert_tagesmodell

config_app.iTimeProcess_O_H_ms = 10

def Schrittantwort():
  import pyplot

  # objOverflowCounter = OverflowCounter(portable_ticks.objTicks)
  objCurveO = pyplot.Curve('O', 'red')
  objCurveH = pyplot.Curve('H', 'blue')

  hw = simulation_hw_hal.Hw(objTagesmodell=portable_simuliert_tagesmodell.TagesmodellConstant(fTempEnvirons_C=20.0))
  for iTimeIncrement in range(5000):
    hw.timeIncrement(iDelay_ms=config_app.iTimeProcess_O_H_ms, fDac_V=1.9)
    # objOverflowCounter.detectOverflow()
    # print("%i,%5.4f,%5.4f" % (hw.iTime_ms, hw.messe_fTempO_C, hw.messe_fTempH_C))
    iTime_ms = portable_ticks.objTicks.time_ms()
    fTime_s = iTime_ms/1000.0
    objCurveO.point(fTime_s, hw.messe_fTempO_C)
    objCurveH.point(fTime_s, hw.messe_fTempH_C)

  plot = pyplot.Plot('Time [s]')
  plot.PlotY1('Temperature [C]', objCurveO, objCurveH)
  plot.PlotSave('simulation_test_schrittantwort.png')
  portable_ticks.objTicks.print_statistics()

if __name__ == "__main__":
  portable_ticks.init(iMaxTicks_ms=portable_constants.YEAR_MS)

  Schrittantwort()
