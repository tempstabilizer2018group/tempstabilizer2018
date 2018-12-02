# -*- coding: utf-8 -*-
import pyplot_xy_config
import pyplot_xy

while True:
  objPlotHelper = pyplot_xy.PlotHelper('./test_hw_pidh_pido_day_log_15.txt', pyplot_xy_config.getPlotConfig)
  objPlotHelper.show()

  try:
    # Python 2
    reload(pyplot_xy_config)
  except NameError:
    # Python 3.4 and above
    import imp
    imp.reload(pyplot_xy_config)

