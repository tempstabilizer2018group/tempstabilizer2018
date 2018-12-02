import re
import sys

strPathTo_plot_xy_processfiles = '.'
sys.path.append(strPathTo_plot_xy_processfiles)

reFilename = re.compile(r'^test_.*\.txt$')
# listFileformats = ('_tmp.png', '_tmp.pdf', '_tmp.svg', '_tmp.eps')
listFileformats = ('_tmp.png', '_show_tmp.py' )

def getPlotConfig(listColumnsToChooseFrom=None):
  import pyplot_xy
  objPlot = pyplot_xy.ConfigPlot('iTime_s', 'Time [s]', listColumnsToChooseFrom=listColumnsToChooseFrom)
  objAxisY1 = objPlot.AddAxisY1('Temperature [C]')
  objAxisY1.Add('fTempH', strColor='blue', fLineWidth=0.5, strLinestyle=pyplot_xy.LINESTYLE_DOTTED)
  objAxisY1.Add('fTempH_Setpoint', strColor='deepskyblue', strMarker=pyplot_xy.MARKER_PLUS, fMarkerSize=12.0)
  objAxisY2 = objPlot.AddAxisY2('Heat [W]')
  objAxisY2.Add('fHeat_W', strColor='orangered', fLineWidth=2.0, fOpaque=0.1)
  # objAxis.Add('fHeat_W_effektiv', 'orange')
  return objPlot

if __name__ == '__main__':
  import pyplot_xy_processfiles
  pyplot_xy_processfiles.run('.')
