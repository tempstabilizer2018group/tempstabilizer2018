# -*- coding: utf-8 -*-
"""
  Installing:
    https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation
    Download https://bootstrap.pypa.io/get-pip.py
    As Admin:
      python get-pip.py
    https://matplotlib.org/users/installing.html#windows
    As Admin:
      python -mpip install -U pip
      python -mpip install -U matplotlib
"""
import csv

import matplotlib.pyplot as plt
import matplotlib.colors as colors

# https://matplotlib.org/api/legend_api.html
LOC_UPPER_RIGHT=1
LOC_UPPER_LEFT=2

dictColorNames = colors.get_named_colors_mapping()

# See: https://matplotlib.org/api/colors_api.html?highlight=color#module-matplotlib.colors
# See: https://xkcd.com/color/rgb/
COLOR_XKCD_GREEN = 'xkcd:green'
COLOR_XKCD_LIMEGREEN = 'xkcd:lime green'
# See: http://whathowblog.com/index.php/2017/09/18/all-about-color-and-line-style-in-matplotlib/
# See: http://whathowblog.com/wp-content/uploads/2017/09/named_colors-768x481.jpg
COLOR_GREEN = 'green'
COLOR_DARK_GREEN = 'darkgreen'

# See: https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.plot.html#matplotlib.axes.Axes.plot
LINESTYLE_SOLID = 'solid'
LINESTYLE_DASHED = 'dashed'
LINESTYLE_DASDOT = 'dashdot'
LINESTYLE_DOTTED = 'dotted'

# See: https://matplotlib.org/api/markers_api.html#module-matplotlib.markers
MARKER_NONE = ''
MARKER_POINT = '.'
MARKER_PIXEL = ','
MARKER_CIRCLE = 'o'
MARKER_SQUARE = 's'
MARKER_STAR = '*'
MARKER_PLUS_FILLED = 'p'
MARKER_PLUS = '+'
MARKER_X = 'x'
MARKER_X_FILLED = 'X'

# See: https://matplotlib.org/gallery/api/two_scales.html#sphx-glr-gallery-api-two-scales-py

class ConfigPlot:
  def __init__(self, strColumnName, strName, fFactorX=1.0, listColumnsToChooseFrom=None):
    self.strColumnName = strColumnName
    self.strName = strName
    self.fFactorX = fFactorX
    self.listColumnsToChooseFrom = listColumnsToChooseFrom
    self.objAxisY1 = None
    self.objAxisY2 = None

    self.clear()

  def AddAxisY1(self, strAxisName):
    self.objAxisY1 = ConfigAxis(self, strAxisName)
    return self.objAxisY1

  def AddAxisY2(self, strAxisName):
    self.objAxisY2 = ConfigAxis(self, strAxisName)
    return self.objAxisY2

  def clear(self):
    for objAxisY in (self.objAxisY1, self.objAxisY2):
      if objAxisY != None:
        objAxisY.clear()

  def addValue(self, strValue, fX, fY):
    fX *= self.fFactorX
    for objAxisY in (self.objAxisY1, self.objAxisY2):
      for objColumn in objAxisY.listColumns:
        if strValue == objColumn.strColumnName:
          objColumn.AddPoint(fX, fY)
          return
    print('pyplot_xy.py: Not found: "%s, %f %f"' % (strValue, fX, fY))

  def readFile(self, csvIn):
    iIndexX = csvIn.fieldnames.index(self.strColumnName)

    for objLine in csvIn.reader:
      fX = float(objLine[iIndexX])
      fX *= self.fFactorX
      for objAxisY in (self.objAxisY1, self.objAxisY2):
        if objAxisY == None:
          continue
        for objColumn in objAxisY.listColumns:
          iIndexY = csvIn.fieldnames.index(objColumn.strColumnName)
          fY = float(objLine[iIndexY])
          objColumn.AddPoint(fX, fY)

    self.plot()

  def plot(self):
    def __plot(objAxis, objAxisY, loc=LOC_UPPER_LEFT):
      listColumns = []
      for objColumn in objAxisY.listColumns:
        if len(objColumn.listX) > 0:
          listColumns.append(objColumn)
          continue
        print('pyplot.py: No datapoints for "%s"' % objColumn.strName)

      for objColumn in listColumns:
        objAxis.plot(objColumn.listX, objColumn.listY, **objColumn.dictPlotArgs)
      plt.legend([objColumn.strName for objColumn in listColumns], loc=loc)
      # otherwise the right y-label is slightly clipped
      objFigure.tight_layout()

    objFigure, objAxis1 = plt.subplots()
    assert(self.objAxisY1 != None)
    objAxis1.set_xlabel(self.strName)
    objAxis1.set_ylabel(self.objAxisY1.strName)
    __plot(objAxis1, self.objAxisY1, LOC_UPPER_LEFT)

    if self.objAxisY2 != None:
      # instantiate a second axes that shares the same x-axis
      objAxis2 = objAxis1.twinx()
      objAxis2.set_ylabel(self.objAxisY2.strName)
      __plot(objAxis2, self.objAxisY2, LOC_UPPER_RIGHT)

  def plotSave(self, strFilenamePng, **kwargs):
    plt.savefig(strFilenamePng, **kwargs)

  def plotShow(self):
    plt.show()

class ConfigAxis:
  def __init__(self, objPlot, strName):
    self.objPlot = objPlot
    self.strName = strName
    self.listColumns = []

  def Add(self, strColumnName, strName=None, strColor='red', strLinestyle=LINESTYLE_SOLID, fLineWidth=1, strMarker=MARKER_NONE, fMarkerSize=10, fOpaque=1.0):
    dictPlotArgs = {
      'color': dictColorNames[strColor],
      'marker': strMarker,
      'linestyle': strLinestyle,
      'linewidth': fLineWidth,
      'markersize': fMarkerSize,
      'alpha': fOpaque,
    }
    objColumn = ConfigColumn(self, strColumnName, strName, dictPlotArgs)
    self.listColumns.append(objColumn)
    return objColumn
  
  def clear(self):
    return
    if objColumn in self.listColumns:
      objColumn.clear()

class ConfigColumn:
  def __init__(self, objAxis, strColumnName, strName, dictPlotArgs):
    assert(objAxis != None)
    self.objAxis = objAxis
    assert(strColumnName != None)
    self.strColumnName = strColumnName
    self.strName = strName
    if strName == None:
      self.strName = self.strColumnName
    assert(dictPlotArgs != None)
    self.dictPlotArgs = dictPlotArgs
    self.exceptionIfColumnNotExists()
    self.clear()

  def exceptionIfColumnNotExists(self):
    listColumnsToChooseFrom = self.objAxis.objPlot.listColumnsToChooseFrom
    if listColumnsToChooseFrom == None:
      return
    if not self.strColumnName in listColumnsToChooseFrom:
      raise Exception('ConfigColumn "%s" does not exist. Choose one of %s!' % (self.strColumnName, ','.join(listColumnsToChooseFrom)))

  def AddPoint(self, fX, fY):
    self.listX.append(fX)
    self.listY.append(fY)

  def clear(self):
    self.listX = []
    self.listY = []

class PlotHelper:
  def __init__(self, strFilename, getPlotConfig):
    plt.clf() # Clear figure
    plt.cla() # Clear axis
    plt.close() # Close window
    with open(strFilename, 'r') as fIn:
      self.csvIn = csv.DictReader(fIn, delimiter='\t')
      self.objPlotConfig = getPlotConfig(self.csvIn.fieldnames)
      self.objPlot = self.readFile()

  def getPlotConfig(self):
    return getPlotConfig(self.csvIn.fieldnames)

  def readFile(self):
    return self.objPlotConfig.readFile(self.csvIn)

  def safe (self, strFilename):
    '''
      See: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.savefig.html?highlight=savefig#matplotlib.pyplot.savefig
      png, pdf, ps, eps, svg
    '''
    plt.savefig(strFilename, dpi=300, papertype='A0')

  def show(self):
    plt.show()


def run():
  import pyplot_xy_config

  strFilenameCsv = 'test_hw_pidh_pido_day_log_01.txt'
  objPlotHelper = PlotHelper(strFilenameCsv, pyplot_xy_config.getPlotConfig)
  objPlotHelper.safe(strFilenameCsv.replace('.txt', '_tmp.png'))
  objPlotHelper.safe(strFilenameCsv.replace('.txt', '_tmp.pdf'))
  objPlotHelper.safe(strFilenameCsv.replace('.txt', '_tmp.svg'))
  objPlotHelper.safe(strFilenameCsv.replace('.txt', '_tmp.eps'))
  objPlotHelper.show()

if __name__ == '__main__':
  run()