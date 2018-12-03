# -*- coding: utf-8 -*-

import pyplot_xy

strMarker=pyplot_xy.MARKER_NONE
strMarker=pyplot_xy.MARKER_PLUS

def getPlotConfig(listColumnsToChooseFrom=None):
  objPlot = pyplot_xy.ConfigPlot('iTime_s', 'Time [s]', listColumnsToChooseFrom=listColumnsToChooseFrom)
  objAxisY1 = objPlot.AddAxisY1('Temperature [C]')
  objAxisY1.Add('fTempEnvirons_C', strMarker=strMarker, strColor='black', fLineWidth=1.0, fOpaque=0.2)

  objAxisY1.Add('fTempH_Setpoint_C', strMarker=strMarker, strColor='blue')
  objAxisY1.Add('fTempH_C', strMarker=strMarker, strColor='skyblue', fLineWidth=0.5)

  objAxisY1.Add('fTempO_C', strMarker=strMarker, strColor='limegreen', fLineWidth=0.5)
  objAxisY1.Add('fTempO_Setpoint_C', strMarker=strMarker, strColor='green', strLinestyle=pyplot_xy.LINESTYLE_DASHED)

  objAxisY2 = objPlot.AddAxisY2('Heat [W]')
  objAxisY2.Add('fHeat_W', strMarker=strMarker, strColor='red', fOpaque=0.3)
  objAxisY2.Add('fDac_V', strMarker=strMarker, strColor='red')
  objAxisY2.Add('PidH_bLimitLow', strMarker=strMarker, strColor='gold', strLinestyle=pyplot_xy.LINESTYLE_DASHED)
  objAxisY2.Add('PidH_bLimitHigh', strMarker=strMarker, strColor='red', fOpaque=0.3, strLinestyle=pyplot_xy.LINESTYLE_DASHED)
  objAxisY2.Add('fHeat_W_LimitHigh', strMarker=strMarker, strColor='red', fOpaque=0.3, strLinestyle=pyplot_xy.LINESTYLE_DOTTED)

  objAxisY2.Add('fDACzeroHeat_V', strMarker=strMarker, strColor='green', fOpaque=0.3, strLinestyle=pyplot_xy.LINESTYLE_DOTTED)
  objAxisY2.Add('fDiskFree_MBytes', strMarker=strMarker, strColor='green', fOpaque=0.2, strLinestyle=pyplot_xy.LINESTYLE_DASHED)
  return objPlot
