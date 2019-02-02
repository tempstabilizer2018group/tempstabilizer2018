# -*- coding: utf-8 -*-
import sys
import portable_constants
import portable_firmware_constants

LOGFILENAME_TABDELIMITED = 'log.txt'
LOGFILENAME_STATISTICS = 'statistics.txt'
LOGFILENAME_GRAFANA = 'grafana.txt'
LOGFILENAME_PERSIST = 'persist.txt'

DIRECTORY_DATA = 'data'
DIRECTORY_CONFIG = 'config'
DIRECTORY_PROGRAM = 'program'

strHttpPostPath = '/upload'
strHttpPostServer = 'http://www.tempstabilizer2018.org'
# strHttpPostServer = 'http://192.168.4.1'

strMAC = 'softmac'
if sys.platform == 'esp32':
  import hw_update_ota
  strMAC = hw_update_ota.strMAC

strWlanSsid = portable_firmware_constants.strWLAN_SSID
strWlanPw = portable_firmware_constants.strWLAN_PW
# Channel 0: All 11 channels
strWlanChannel = 6

# None: Es wird jedesmal versucht, über das Netzwerk Daten abzusetzen.
strWlanSidForTrigger = 'rumenigge'
strWlanSidForTrigger = None

# Use this to simulate the upload of a big file.
# A big file could break HTTP-Post when using to much memory.
iHttpPostBigTestfile = 1024*1024
iHttpPostBigTestfile = None

# When starting:
# fTempO_Start = messe_fTempO_C + fStart_Increment_fTempO_C
# fStart_Increment_fTempO_C>0.0: Setpoint higher than ambient, so we start with heating
# fStart_Increment_fTempO_C<0.0: Setpoint lower than ambient, so we start without heating
fStart_Increment_fTempO_C = -10.0 # Setpoint bezüglich fTempO_C nach einem Reset

# None: Forever
iExperimentDuration_ms = None

# None: No Log
iLogInterval_ms = 2 * portable_constants.SECOND_MS
iLogInterval_ms = None

# Write a file with statistics how many times which methtod was called.
bWriteLogStatistics = True

# bRunStopwatch: Will print some statistics where CPU-Time is spent:
#   Stopwatch 05 ms: self.logOnce()
#   Stopwatch 03 ms: self.objTs.processO(...)
#   Stopwatch 03 ms: self.objTs.processH(...)
#   Stopwatch 125 ms: self.runOnce()
bRunStopwatch = False

iGrafanaLogInterval_ms = 1 * portable_constants.SECOND_MS
# After this interval portable_pid_controller O and H will be called
iTimeProcess_O_H_ms = 200
fTimeDeltaMax_s = 5.0*iTimeProcess_O_H_ms/1000.0

bUseNetwork = False
# After this interval the WLAN will polled
iPollForWlanInterval_ms = 10 * portable_constants.MINUTE_MS

# Interval to write persist setpoint temperature and time
# None: Do not persist
iPersistInterval_ms = 10 * portable_constants.MINUTE_MS

# Hardware only
iLogHwConsoleInterval_ms = 2 * portable_constants.SECOND_MS
iLogHwConsoleInterval_ms = 30 * portable_constants.SECOND_MS
iHwI2cEnvironsInterval_ms = 10 * portable_constants.SECOND_MS
iHwLedModulo = 25
bHwDoLightSleep = True

# Simuliert only
iLogSimuliertPlotInterval_ms = 10 * portable_constants.SECOND_MS
# bSimulationUseHttpPost: True:  Files will be POST'd to the webserver
# bSimulationUseHttpPost: False: Files will be moved to the local webserver 'to_be_processed' directory and the written to InfluxDB.
bSimulationUseHttpPost = False

# Will be used to initialize portable_ticks.TicksSimuliert().
# A higher value will overflow later.
iSimulationMaxTicks_ms = portable_constants.YEAR_MS

# Grafana Log Writer
# If True: The grafana-log-file will be smaller, but the logic to read is complexer
bGrafanaSkipEqualValues = True
# Different values need to be logged more or less frequently.
# Every value belongs to a group.
# A iMODULO of 5 implies that the log interval will be 5*iGrafanaLogInterval_ms.
# Push implies a measurement is read for averaging.
# Pull means that a averaged measurment is written to the grafana-log
iMODULO_GRAFANALOG_MEDIUM_PUSH = 1
iMODULO_GRAFANALOG_MEDIUM_PULL = 5
iMODULO_GRAFANALOG_SLOW_PUSH = 10
iMODULO_GRAFANALOG_SLOW_PULL = 50
