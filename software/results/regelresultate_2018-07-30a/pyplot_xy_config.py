import re
import sys

strPathTo_plot_xy_processfiles = '../../versuche_pyplot'
sys.path.append(strPathTo_plot_xy_processfiles)

reFilename = re.compile(r'^test_.*\.txt$')
# listFileformats = ('_tmp.png', '_tmp.pdf', '_tmp.svg', '_tmp.eps')
listFileformats = ('_tmp.png', '_show_tmp.py' )

# Colors
# See: https://xkcd.com/color/rgb/
# COLOR_XKCD_GREEN = 'xkcd:green'
# See: http://whathowblog.com/index.php/2017/09/18/all-about-color-and-line-style-in-matplotlib/
# See: http://whathowblog.com/wp-content/uploads/2017/09/named_colors-768x481.jpg

def getPlotConfig(listColumnsToChooseFrom=None):
  import pyplot_xy
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
  # objAxisY2.Add('PidH_bLimitLow_W', strColor='gold', fOpaque=0.2)
  return objPlot

if __name__ == '__main__':
  import pyplot_xy_processfiles
  pyplot_xy_processfiles.run('.')
