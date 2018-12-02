# -*- coding: utf-8 -*-
import os
import pyplot_xy_config
import pyplot_xy

def getTemplate(strFilename):
  return '''# -*- coding: utf-8 -*-
import pyplot_xy_config
import pyplot_xy

while True:
  objPlotHelper = pyplot_xy.PlotHelper('%s', pyplot_xy_config.getPlotConfig)
  objPlotHelper.show()

  try:
    # Python 2
    reload(pyplot_xy_config)
  except NameError:
    # Python 3.4 and above
    import imp
    imp.reload(pyplot_xy_config)

''' % strFilename

def getPlotFiles(strDirectory):
  listFilenames = []
  for strFilename in os.listdir(strDirectory):
    matchFilename = pyplot_xy_config.reFilename.match(strFilename)
    if matchFilename:
      listFilenames.append(strFilename);
  return listFilenames

def run(strDirectory):
  for strFilename in getPlotFiles(strDirectory):
    print('--> %s' % strFilename)
    strFilenameCsv = strDirectory + '/' + strFilename
    objPlotHelper = pyplot_xy.PlotHelper(strFilenameCsv, pyplot_xy_config.getPlotConfig)
    for strFileformat in pyplot_xy_config.listFileformats:
      strFilenameCsvWithoutExtension, strExtensionDummy = os.path.splitext(strFilenameCsv)
      strFilenameNew = strFilenameCsvWithoutExtension + strFileformat
      print(' --> %s' % strFilenameNew)
      assert strFilenameNew != strFilenameCsvWithoutExtension
      if (strFilenameNew.endswith('.py')):
        with open(strFilenameNew, 'w') as fOut:
          fOut.write(getTemplate(strFilenameCsv))
        continue
      objPlotHelper.safe(strFilenameNew)
    # objPlotHelper.show()

if __name__ == '__main__':
  run('.')