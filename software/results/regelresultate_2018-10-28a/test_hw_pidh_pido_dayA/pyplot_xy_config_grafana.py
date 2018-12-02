# -*- coding: utf-8 -*-
import sys

strTop = '../..'
sys.path.append(strTop + '/libportable')
import portable_grafana_log_reader

sys.path.append(strTop + '/../versuche_pyplot')
import matplotlib.pyplot as plt
import pyplot_xy

def getPlotConfig(listColumnsToChooseFrom=None):
  objPlot = pyplot_xy.ConfigPlot('iTime_s', 'Time [s]', listColumnsToChooseFrom=listColumnsToChooseFrom)
  objAxisY1 = objPlot.AddAxisY1('Temperature [C]')
  objAxisY1.Add('fTempEnvirons_C', strColor='black', fLineWidth=1.0, fOpaque=0.2)

  objAxisY1.Add('fTempH_Setpoint_C', strColor='blue')
  objAxisY1.Add('fTempH_C', strColor='skyblue', fLineWidth=0.5)

  objAxisY1.Add('fTempO_C', strColor='limegreen', fLineWidth=0.5)
  objAxisY1.Add('fTempO_Setpoint_C', strColor='green', strLinestyle=pyplot_xy.LINESTYLE_DASHED)

  objAxisY2 = objPlot.AddAxisY2('Heat [W]')
  objAxisY2.Add('fHeat_W', strColor='red', fOpaque=0.3)
  objAxisY2.Add('fDac_V', strColor='red')
  objAxisY2.Add('PidH_bLimitLow', strColor='gold', strLinestyle=pyplot_xy.LINESTYLE_DASHED)
  objAxisY2.Add('PidH_bLimitHigh', strColor='red', fOpaque=0.3, strLinestyle=pyplot_xy.LINESTYLE_DASHED)
  objAxisY2.Add('fHeat_W_LimitHigh', strColor='red', fOpaque=0.3, strLinestyle=pyplot_xy.LINESTYLE_DOTTED)

  objAxisY2.Add('fDACzeroHeat_V', strColor='green', fOpaque=0.3, strLinestyle=pyplot_xy.LINESTYLE_DOTTED)
  return objPlot

class PlotDumper:
  def __init__(self):
    self.objPlot = getPlotConfig()
    self.dictValues = {}

  def funcLine(self, iTime_ms, strVerb, strPayload):
    if strVerb == 'ntptime':
      # Seconds since 2000-01-01
      iSecondsSince2000 = int(strPayload)
      # https://www.unixtimestamp.com/index.php
      self.fSecondsSince1970_UnixEpoch = iSecondsSince2000 + 946684800.0
      return 

    if strVerb == 'node':
      self.strSite, self.strNode = strPayload.split()
      return

    if strVerb == 'v':
      self.handleMeasurements(iTime_ms, strPayload)
      return

  def handleMeasurements(self, iTime_ms, strPayload):

    for strTag, strValue in portable_grafana_log_reader.ValuesIterator(strPayload):
      def plotValue(strName, funcConversion):
        if strValue == '':
          fValue = self.dictValues.get(strTag, None)
          if fValue == None:
            print('Why? "%s"' % strTag)
            return
        else:
          fValue = funcConversion(strValue)
          self.dictValues[strTag] = fValue
        self.objPlot.addValue(strName, iTime_ms, fValue)

      if strTag == 'O':
        plotValue('fTempO_C', lambda v: int(v)/1000.0)
      if strTag == 'S':
        plotValue('fTempO_Setpoint_C', lambda v: int(v)/1000.0)
      if strTag == 'H':
        plotValue('fHeat_W', lambda v: int(v)/100.0)
      if strTag == 'U':
        plotValue('fTempEnvirons_C', lambda v: int(v)/1000.0)
      if strTag == 'z':
        plotValue('fDACzeroHeat_V', lambda v: int(v)/1000.0)
      if strTag == 'L':
        plotValue('PidH_bLimitHigh', lambda v: {'+': 1.0}.get(v, 0.0))

  def plot(self, strFilenamePng):
    self.objPlot.plot()
    plt.savefig(strFilenamePng, dpi=300, papertype='A0')

  def show(self):
    plt.show()

def run(strFilename):
  objDumper = PlotDumper()
  with open(strFilename, 'r') as fLog:
    portable_grafana_log_reader.read(fLog, objDumper.funcLine)
  strFilenamePng = strFilename.replace('.txt', '.png')
  assert(strFilenamePng != strFilename)
  objDumper.plot(strFilenamePng)
  objDumper.show()

if __name__ == '__main__':
  run('log_grafana_00.txt')
