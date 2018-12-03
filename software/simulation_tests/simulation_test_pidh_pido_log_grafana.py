# -*- coding: utf-8 -*-
import python3_grafana_log_config
import python3_grafana_log_reader

def run(strFilename):
  strFilenamePng = strFilename.replace('.txt', '.png')
  assert strFilenamePng != strFilename

  objDumper = grafana_log_reader.GrafanaPlotDumper(grafana_log_config.getPlotConfig())
  objDumper.readFile(strFilename)
  objDumper.plot(strFilenamePng)
  # objDumper.show()

if __name__ == '__main__':
  run('simulation_test_pidh_pido_log_grafana.txt')
