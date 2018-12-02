# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.colors as colors

# https://matplotlib.org/api/legend_api.html
LOC_UPPER_RIGHT=1
LOC_UPPER_LEFT=2

# See: https://matplotlib.org/gallery/api/two_scales.html#sphx-glr-gallery-api-two-scales-py
class Plot:
  def __init__(self, strXLabel):
    self.strXLabel = strXLabel
    self.figure, self.axis1 = plt.subplots()
    self.namecolors = colors.get_named_colors_mapping()

  def PlotY1(self, strYLabel, *listCurves):
    self.axis1.set_xlabel(self.strXLabel)
    self.axis1.set_ylabel(strYLabel)
    self.__plot(self.axis1, listCurves, LOC_UPPER_LEFT)

  def PlotY2(self, strYLabel, *listCurves):
    axis2 = self.axis1.twinx()  # instantiate a second axes that shares the same x-axis
    axis2.set_ylabel(strYLabel)
    self.__plot(axis2, listCurves, LOC_UPPER_RIGHT)

  def __plot(self, axis, listCurves, loc=LOC_UPPER_LEFT):
    for objCurve in listCurves:
      axis.plot(objCurve.listX, objCurve.listY, 'k', color=self.namecolors[objCurve.strColor], linewidth=objCurve.fLineWidth, alpha=objCurve.fOpaque)
    plt.legend([objCurve.strName for objCurve in listCurves], loc=loc)
    # otherwise the right y-label is slightly clipped
    self.figure.tight_layout()

  def PlotSave(self, strFilename):
    print('PlotSave("%s")' % strFilename)
    plt.savefig(strFilename)

  def PlotShow(self):
    plt.show()

class Curve:
  def __init__(self, strName, strColor='red', fLineWidth=0.5, fOpaque=1.0):
    self.strName = strName
    self.strColor = strColor
    self.fLineWidth = fLineWidth
    self.fOpaque = fOpaque
    self.listX = []
    self.listY = []

  def point(self, fX, fY):
    self.listX.append(fX)
    self.listY.append(fY)

