# -*- coding: utf-8 -*-
TAG_GRAFANA_VERSION = 'version'
TAG_GRAFANA_MAC = 'mac'
TAG_GRAFANA_DATATYPE = 'grafana_type'
TAG_GRAFANA_VALUE = 'v'
TAG_GRAFANA_NTP = 'ntptime'
TAG_GRAFANA_INFO = 'info'
TAG_GRAFANA_WARNING = 'warning'
TAG_GRAFANA_ERROR = 'error'
TAG_GRAFANA_MESSINTERVAL_MS = 'messinterval_ms'
TAG_GRAFANA_MAXTICK_MS = 'portable_ticks.iMaxTick_ms'
TAG_GRAFANA_I2C_FREQUENCY_SELECTED_HZ = 'iI2cFrequencySelected_Hz'
INFLUXDB_TAG_NODE = 'node'
INFLUXDB_TAG_ENVIRONS = 'environs'

def Instantiate(strConstructor):
  objGrafanaValue = eval(strConstructor)
  return objGrafanaValue

class GrafanaValueBase:
  def __init__(self, strInfluxDbTag, strTag, strName):
    self.strInfluxDbTag = strInfluxDbTag
    self.strTag = strTag
    self.strName = strName
    self.__strValueActual = None

  def _pullValue(self, strValue):
    if self.__strValueActual != strValue:
      self.__strValueActual = strValue
      return strValue
    return None

  def getConstructor(self):
    strAdditionalArguments = self._getAdditionalArguments()
    return "%s('%s', '%s', '%s'%s)" % (type(self).__name__, self.strInfluxDbTag, self.strTag, self.strName, strAdditionalArguments)

class GrafanaValueFloatAvg(GrafanaValueBase):
  '''
    Der Wert wird gemittelt.
    Hat der Wert sich nicht geändert, so wird '' zurückgegeben.
  '''
  def __init__(self, strInfluxDbTag, strTag, strName, __fFactor=100000.0):
    GrafanaValueBase.__init__(self, strInfluxDbTag, strTag, strName)
    self.__fFactor = __fFactor
    self.__fSum = 0.0
    self.__iCount = 0

  def pushValue(self, fValue):
    self.__fSum += fValue
    self.__iCount += 1
      
  def pullValue(self):
    if self.__iCount == 0:
      return None
    fAvg = 0.0
    fAvg = self.__fSum/self.__iCount
    strValue = str(int(self.__fFactor*fAvg))
    v = self._pullValue(strValue)
    self.__fSum = 0.0
    self.__iCount = 0
    return v

  def _getAdditionalArguments(self):
    strFactor = ', %f' % self.__fFactor
    # strFactor: '100000.000000' / '100000.000000'
    return strFactor.rstrip('0')

  def convert2float(self, strValue):
    return int(strValue)/self.__fFactor

class GrafanaValueFloat(GrafanaValueBase):
  '''
    Hat der Wert sich nicht geändert, so wird '' zurückgegeben.
  '''
  def __init__(self, strInfluxDbTag, strTag, strName, __fFactor=100000.0):
    GrafanaValueBase.__init__(self, strInfluxDbTag, strTag, strName)
    self.__fFactor = __fFactor
    self.fValue = None

  def pushValue(self, fValue):
    # Diese Funktion bildet keinen Mittelwert. pushValue() und pullValue() sollten abwechsungsweise aufgerufen werden.
    assert self.fValue == None
    self.fValue = fValue

  def pullValue(self):
    # Diese Funktion bildet keinen Mittelwert. pushValue() und pullValue() sollten abwechsungsweise aufgerufen werden.
    assert self.fValue != None
    strValue = str(int(self.__fFactor*self.fValue))
    v= self._pullValue(strValue)
    self.fValue = None
    return v

  def _getAdditionalArguments(self):
    strFactor = ', %f' % self.__fFactor
    return strFactor.rstrip('0')

  def convert2float(self, strValue):
    return int(strValue)/self.__fFactor

class GrafanaValueBoolTrue(GrafanaValueBase):
  '''
    Falls der Wert irgendwann True war, wird '+' zurückgegeben, sonst '-'.
    Hat der Wert sich nicht geändert, so wird '' zurückgegeben.
  '''
  def __init__(self, strInfluxDbTag, strTag, strName):
    GrafanaValueBase.__init__(self, strInfluxDbTag, strTag, strName)
    self.bValue = False

  def pushValue(self, bValue):
    if bValue:
       self.bValue = True

  def pullValue(self):
    strValue = {True: '+'}.get(self.bValue, '-')
    v = self._pullValue(strValue)
    self.bValue = False
    return v

  def _getAdditionalArguments(self):
    return ''

  def convert2float(self, strValue):
    return {'+': 1.0}.get(strValue, 0.0)
