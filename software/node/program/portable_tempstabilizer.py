# -*- coding: utf-8 -*-
import math

import config_app
import portable_daymaxestimator
import portable_ticks
import portable_pid_controller

# Hardware Limits [C]
fTempO_Limit_Low = -30.0
fTempO_Limit_High = 40.0
fTempH_Limit_High = 140.0

fFetMin_W = 0.0 # [W] Limiten des H-Reglers

fTemp_Tolerance_MAX30205 = 0.5

# Zeitkonstante zum Erhoehen der Spannung
fTauIncrease_fHeat_s = 10.0

# Falls zu heiss: Leistungslimit reduzieren
fHeat_W_reduction_per_s = 0.1

class FloatAvg:
  '''
    Averaging.
  '''
  def __init__(self):
    self.__reset()

  def __reset(self):
    self.__fSum = 0.0
    self.__iCount = 0

  def push(self, fValue):
    self.__fSum += fValue
    self.__iCount += 1

  def getValueAndReset(self):
    assert self.__iCount > 0
    fAvg = self.__fSum/self.__iCount
    self.__reset()
    return fAvg

class TempStabilizer:
  def __init__(self, objDayMaxEstimator=None, objPidO=None, objPidH=None):
    self.fHeat_W_gefiltert = 0.0
    self.fHeat_W_LimitHigh = 0.0
    self.bZeroHeatForecast = False
    self.objAvgHeat_W = FloatAvg()
    self.objAvgTempO_C = FloatAvg()

    self._objDayMaxEstimator = objDayMaxEstimator
    if objDayMaxEstimator == None:
      if config_app.bSetpointFix:
        class SetpointFix:
          def __init__(self):
            self.fOutputValue = config_app.fTempSetpointFix_C
          def start(self, iTicks_ms, fTempO_Sensor, objPersist=None):
            pass
          def process(self, iTicks_ms, fTempO_Sensor, bFetMin_W_Limit_Low):
            pass
        self._objDayMaxEstimator = SetpointFix()
      else:
        self._objDayMaxEstimator = portable_daymaxestimator.DayMaxEstimator(portable_ticks.objTicks.ticks_ms())
      print('Setpoint from ' + self._objDayMaxEstimator.__class__.__name__)

    self._objPidO = objPidO
    if objPidO == None:
      self._objPidO = portable_pid_controller.PidController('PidO')

    self._objPidH = objPidH
    if objPidH == None:
      self._objPidH = portable_pid_controller.PidController('PidH')

    # fDACzeroHeat_V: Soll adaptiv justiert werden
    self.fDACzeroHeat_V = None # None, um sicherzustellen, dass find_fDACzeroHeat() aufgerufen wird!

  def find_fDACzeroHeat(self, objHw):
    if not objHw.bZeroHeat:
      print('TempStabilizer.find_fDACzeroHeat(): fDac_V = 0.0')
      objHw.fDac_V = 0.0
      portable_ticks.objTicks.sleep_ms(1000)

    portable_ticks.count('TempStabilizer.find_fDACzeroHeat()')

    iTicksStart_ms = portable_ticks.objTicks.ticks_ms()
    for iDAC_uV in range(0, 3300000, 500):
      self.fDACzeroHeat_V = iDAC_uV / 1000000.0
      objHw.fDac_V = self.fDACzeroHeat_V
      if not objHw.bZeroHeat:
        iDuration_ms = portable_ticks.objTicks.ticks_diff(portable_ticks.objTicks.ticks_ms(), iTicksStart_ms)
        fCorrection_V = 1.58350 - 1.60900 # Fehlerkorrektur durch schnelle Rampe (siehe unten)
        self.fDACzeroHeat_V += fCorrection_V
        print('TempStabilizer.find_fDACzeroHeat(): fDACzeroHeat_V %0.5f in %d ms' % (self.fDACzeroHeat_V, iDuration_ms))
        objHw.fDac_V = 0.0
        return
      portable_ticks.objTicks.sleep_ms(1)

    # Messungen OHNE KORREKTUR:
    # sleep_ms(0): TempStabilizer.find_fDACzeroHeat(): fDACzeroHeat_V 1.68550 in 1753 ms
    # sleep_ms(1): TempStabilizer.find_fDACzeroHeat(): fDACzeroHeat_V 1.60900 in 5247 ms
    # sleep_ms(5): TempStabilizer.find_fDACzeroHeat(): fDACzeroHeat_V 1.58350 in 17833 ms

    # TODO: Zulässig 0.3 bis 3.0 V. Die Spannung konnte nicht bestimmt werden. Die Hardware ist futsch!

  def start(self, iTimeOH_ms=0, iTimeDayMaxEstimator=0, fTempH_Start=47.11, fTempO_Sensor=47.11, objPersist=None):
    assert self.fDACzeroHeat_V!= None
    self._objDayMaxEstimator.start(iTicks_ms=iTimeDayMaxEstimator, fTempO_Sensor=fTempO_Sensor, objPersist=objPersist)
    self._objPidO.start(iTimeOH_ms, fKp=8.0, fKi=0.1*2.0, fKd=0.0, fOutputValue=fTempH_Start-0.5)
    self._objPidH.start(iTimeOH_ms, fKp=0.6, fKi=0.06, fKd=0.0)

  @property
  def fHeat_W(self):
    return self._objPidH.fOutputValueLimited

  def fDac_V(self, objHw, fSupplyHV_V):
    # [V]
    # 0 bis 3.3V

    # Fehlerkorrektur:
    fCurrent = self.fHeat_W / fSupplyHV_V
    fDAC_V = -0.2724*math.exp(-fCurrent/0.01068)+3.003*fCurrent+0.3045 + self.fDACzeroHeat_V - 0.161
    # Limitieren auf den möglichen Spannungsbereich des DAC
    fDAC_V = min(max(0.0, fDAC_V), 3.3)
    
    if (not self.bZeroHeatForecast) and objHw.bZeroHeat:
      self.fDACzeroHeat_V += 0.00001
    if self.bZeroHeatForecast and (not objHw.bZeroHeat):
      self.fDACzeroHeat_V -= 0.00001
    # Prognose wie bZeroHeat sein sollte
    self.bZeroHeatForecast = fCurrent < 0.004
    return fDAC_V

  @property
  def bFetMax_W_Limit_High(self):
    return self._objPidH.bLimitHigh

  @property
  def fPidO_fI(self):
    return self._objPidO.fI

  @property
  def bFetMin_W_Limit_Low(self):
    return self._objPidH.bLimitLow

  @property
  def fTempH_Setpoint_C(self):
    return self._objPidO.fOutputValueLimited

  @property
  def bTempO_Limit_High(self):
    return self._objPidO.bLimitHigh

  @property
  def bTempO_Limit_Low(self):
    return self._objPidO.bLimitLow

  @property
  def fTempO_Setpoint_C(self):
    assert self._objDayMaxEstimator.fOutputValue != None
    return self._objDayMaxEstimator.fOutputValue

  @property
  def fTempO_C(self):
    return self._objPidO.fSensorValue

  @property
  def fTempH_C(self):
    return self._objPidH.fSensorValue

  # Aktualisiert: self._objDayMaxEstimator.fOutputValue
  def processDayMaxEstimator(self, iTime_ms, fTempO_Sensor):
    portable_ticks.count('TempStabilizer.processDayMaxEstimator()')
    self.objAvgTempO_C.push(fTempO_Sensor)
    self._objDayMaxEstimator.process(iTicks_ms=iTime_ms, objAvgTempO_C=self.objAvgTempO_C, objAvgHeat_W=self.objAvgHeat_W, bFetMin_W_Limit_Low=self.bFetMin_W_Limit_Low)

  def processO(self, iTime_ms, fTempO_Sensor):
    portable_ticks.count('TempStabilizer.processO()')
    fTempH_Limit_Low = fTempO_Sensor - fTemp_Tolerance_MAX30205

    # Falls der H-Regler ansteht, so soll der I-Anteil des O-Regler nicht verschlimmert werden.
    bAllowIncreaseI=not self._objPidH.bLimitHigh
    bAllowDecreaseI=not self._objPidH.bLimitLow

    self._objPidO.process(iTime_ms,
                         fSetpoint=self.fTempO_Setpoint_C,
                         fSensorValue=fTempO_Sensor,
                         fLimitOutLow=fTempH_Limit_Low,
                         fLimitOutHigh=fTempH_Limit_High,
                         bAllowIncreaseI=bAllowIncreaseI,
                         bAllowDecreaseI=bAllowDecreaseI)

  def processH(self, iTime_ms, fTempH_Sensor, fTempO_Sensor, bZeroHeat):
    portable_ticks.count('TempStabilizer.processH()')

    fTimeDelta_s = self._objPidH.process(iTime_ms,
                         fSetpoint=self.fTempH_Setpoint_C,
                         fSensorValue=fTempH_Sensor,
                         fLimitOutLow=fFetMin_W,
                         fLimitOutHigh=self.fHeat_W_LimitHigh)

    self.objAvgHeat_W.push(self.fHeat_W)

    self.__ajust_fHeat_W_LimitHigh__(fTimeDelta_s, fTempH_Sensor, fTempO_Sensor)

  def __ajust_fHeat_W_LimitHigh__(self, fTimeDelta_s, fTempH_Sensor, fTempO_Sensor):
    self.fHeat_W_gefiltert = self.fHeat_W_gefiltert + (self.fHeat_W - self.fHeat_W_gefiltert) / fTauIncrease_fHeat_s * fTimeDelta_s

    fTempDiff_HO_C = fTempH_Sensor - fTempO_Sensor

    # Bei dickem Alu: 8W bei fTempLimit_C=5C
    # Bei Chromstahl: 1.5W
    # Ohne Blech: 0.8W
    fTempLimit_C = 5.0
    if fTempDiff_HO_C < fTempLimit_C:
      # Leistung erhöhen
      self.fHeat_W_LimitHigh = max(self.fHeat_W_LimitHigh, self.fHeat_W_gefiltert + 0.5)
      self.fHeat_W_LimitHigh = min(self.fHeat_W_LimitHigh, 8.0) # maximal 8 W gemaess Datenblatt BUK9875-100A
      portable_ticks.count('portable_tempstabilizer.TempStabilizer.__ajust_fHeat_W_LimitHigh__(Leistung erhoehen)')
      return

    if fTempDiff_HO_C > (fTempLimit_C + 0.2):
      # Achtung, wir sind zu heiss: Leistung senken
      portable_ticks.count('portable_tempstabilizer.TempStabilizer.__ajust_fHeat_W_LimitHigh__(Leistung senken)')
      self.fHeat_W_LimitHigh -= fTimeDelta_s * fHeat_W_reduction_per_s

  def logHeader(self, fLog):
    listColumns = (
                    'iTime_s',
                    'fTempH_C',
                    'fTempO_C',
                    'fDac_V',
                    'fHeat_W',
                    'fTempH_Setpoint_C',
                    'fTempO_Setpoint_C',
                    'PidH_bLimitLow',
                    'PidH_bLimitHigh',
                    'PidO_bLimitLow',
                    'PidO_bLimitHigh',
                    'PidO_fI',
                    'fTempEnvirons_C',
                    'fDACzeroHeat_V',
                    'fHeat_W_LimitHigh',
                  )
    fLog.write('\t'.join(listColumns) + '\n')

  def log(self, fLog, objHw):
    fTempEnvirons_C = objHw.messe_fTempEnvirons_C
    strTempEnvirons_C = '-'
    if fTempEnvirons_C != None:
      strTempEnvirons_C = '%0.2f' % fTempEnvirons_C

    listColumns = (
                    '%0.1f' % (portable_ticks.objTicks.ticks_ms()/1000.0),
                    '%0.2f' % self.fTempH_C,
                    '%0.3f' % self.fTempO_C,
                    '%0.2f' % self.fDac_V,
                    '%0.2f' % self.fHeat_W,
                    '%0.2f' % self.fTempH_Setpoint_C,
                    '%0.3f' % self.fTempO_Setpoint_C,
                    '%d' % self._objPidH.bLimitLow,
                    '%d' % self._objPidH.bLimitHigh,
                    '%d' % self._objPidO.bLimitLow,
                    '%d' % self._objPidO.bLimitHigh,
                    '%0.2f' % self._objPidO.fI,
                    strTempEnvirons_C,
                    '%0.5f' % self.fDACzeroHeat_V,
                    '%0.3f' % self.fHeat_W_LimitHigh,
                  )
    fLog.write('\t'.join(listColumns) + '\n')
