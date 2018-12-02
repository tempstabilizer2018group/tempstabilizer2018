# -*- coding: utf-8 -*-
import pyplot
import portable_ticks

iPLOT_INTERVAL_MS = 2000
iNextPlotTime_ms = 0

objCurvePidO_fI = pyplot.Curve('PidO_fI', 'red')
objCurveHeat_W = pyplot.Curve('fHeat_W', 'red')
objCurveHeat_W_effektiv = pyplot.Curve('fHeat_W_effektiv', 'orange')
objCurveTempH_Sensor = pyplot.Curve('fTempH_Sensor_C', 'blue')
objCurveTempH_Setpoint = pyplot.Curve('fTempH_Setpoint_C', 'blue', fLineWidth=3.0, fOpaque=0.2)
objCurveTempO_Sensor = pyplot.Curve('fTempO_Sensor_C', 'green')
objCurveTempO_Setpoint = pyplot.Curve('fTempO_Setpoint_C', 'green', fLineWidth=3.0, fOpaque=0.2)
objCurveTempUmgebung = pyplot.Curve('fTempEnvirons_C', 'gray', fOpaque=0.2)

listCurvesY1 = [objCurveTempUmgebung, objCurveTempH_Sensor, objCurveTempH_Setpoint, objCurveTempO_Sensor, objCurveTempO_Setpoint]
listCurvesY2 = [objCurveHeat_W, objCurveHeat_W_effektiv]

def deleteCurve(strName):
  '''
    In simulation, often we are not interested in data which is not part of the test.
  '''
  for listCurves in (listCurvesY1, listCurvesY2):
    for objCurve in listCurves:
      if objCurve.strName == strName:
        listCurves.remove(objCurve)
        return
  raise Exception('deleteCurve("%s"): Curve not found!' % strName)

def plot_init():
  pass

def plot_plot(objTs, objHw):
  global iNextPlotTime_ms
  if iNextPlotTime_ms > portable_ticks.objTicks.time_ms():
    return
  iTime_ms = portable_ticks.objTicks.time_ms()
  iNextPlotTime_ms = iTime_ms + iPLOT_INTERVAL_MS

  fTime_s = iTime_ms / 1000.0
  fTempEnvirons_C = objHw.messe_fTempEnvirons_C
  objCurveTempUmgebung.point(fTime_s, fTempEnvirons_C)
  objCurveHeat_W.point(fTime_s, objTs.fHeat_W)
  objCurveHeat_W_effektiv.point(fTime_s, objHw.fHeat_W)

  objCurveTempH_Sensor.point(fTime_s, objTs.fTempH_C)
  objCurveTempH_Setpoint.point(fTime_s, objTs.fTempH_Setpoint_C)
  objCurveTempO_Sensor.point(fTime_s, objTs.fTempO_C)
  objCurveTempO_Setpoint.point(fTime_s, objTs.fTempO_Setpoint_C)
        
  objCurvePidO_fI.point(fTime_s, objTs.fPidO_fI)


def plot_show(strFilename):
  plot = pyplot.Plot('Time [s]')
  plot.PlotY1('Temperature [C]', *listCurvesY1)
  plot.PlotY2('Heat [W]', *listCurvesY2)
  # plot.PlotY2('PidO fI [-]', objCurvePidO_fI)
  plot.PlotSave(strFilename)
