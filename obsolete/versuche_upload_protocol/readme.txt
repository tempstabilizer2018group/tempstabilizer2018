


iTime_s	iTimeEff_s	fTempO	fDac	fHeat_W	fTempH_Setpoint	fTempO_Setpoint	PidH_bLimitLow	PidH_bLimitHigh	PidO_bLimitLow	PidO_bLimitHigh	PidO_fI	fTemp_Umgebung
1.8	1.751	26.34	24.64	0.42	0.10	26.49	24.71	0	0	0	0	129.56	25.04

Logfile
=======
<ms> slow  <fTempO_Setpoint>
<ms> fast  <fTempO fTempH>  <fTempH_Setpoint>
<ms> ntp 2018-08-14_11:25
<ms> download file1.txt(123) file2.txt(224)
<ms> upload file1.txt(234)
<ms> boot
<ms> tempO_setpoint

Statefile
=========
daymaxestimator.py.TempO_SetpointWhenSet.fTempO_C = 26.5
daymaxestimator.py.TempO_SetpointWhenSet.objTimeDelta.iTimeLast_ms = << Bereits verstrichene Zeit in ms.
daymaxestimator.py.TemperatureList.listTemp_C = 22.3, None, 22.6, ...
daymaxestimator.py.TemperatureList.iLastDatapoint = 5

LastNtp = 1234 2018-08-14_11:25

==> Lösungsanzsatz
==> Verwendung von utime.ticks_ms()
==> Angenommen ticks_ms ist 31bit signed, so ist der Overflow nach (2**30)/1000.0/3600.0/24.0 = 12.4 Tage (http://docs.micropython.org/en/v1.9.3/pyboard/library/pyb.html)
==> Es gibt nur eine Zeit: utime.ticks_ms()
==> Jede Stunde wird der Zustand gespeichert in 'statefile'
==> Bei einem Warm- oder Kaltstart wird eine Pause von 0 (eventeulle einer halben Stunde) angenommen.

Es wird geloggt:
  Warmboot oder Kaltboot
  RTC wird NICHT verwendet


Verdichten der Daten
--------------------
Varianten:
 - Tiefbass
 - Mitteln seit dem letzen Messpunkt
 - Tiefbass und Streung
 - Max- Min- überwachen

Daten auslassen falls:
 - Wert nicht verändert
 - Wert weniger als x% verändert
 - Wert bereits vor weniger als xs geschrieben
 - Max grösser als x% von Min

Entscheid mit Peter
-------------------
 - Umgebung_C
 - TempO_C
 - O_Setpoint_C
    3 Stellen, mC
 - fHeat_W
    2 Stellen, dW
 ==> avg Alle 10 Minuten

 - PidH_bLimitHigh
   Falls aufgetreten in diesen 10 Minuten

  Pro Tag 6*24 Zeilen: 100 Zeilen
