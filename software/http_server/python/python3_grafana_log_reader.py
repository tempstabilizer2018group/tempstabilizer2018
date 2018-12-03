# -*- coding: utf-8 -*-
import python3_grafana_log_reader_lib

class GrafanaPlotDumper(python3_grafana_log_reader_lib.GrafanaDumper):
  def __init__(self, objPlot):
    python3_grafana_log_reader_lib.GrafanaDumper.__init__(self)
    self.objPlot = objPlot

  def addMeasurement(self, objGrafanaValue, iTime_ms, strValue):
    fValue = objGrafanaValue.convert2float(strValue)
    self.objPlot.addValue(objGrafanaValue.strName, iTime_ms/1000.0, fValue)

  def plot(self, strFilenamePng):
    self.objPlot.plot()
    self.objPlot.plotSave(strFilenamePng, dpi=300, papertype='A0')

  def show(self):
    self.objPlot.plotShow()
