# -*- coding: utf-8 -*-
import portable_grafana_datatypes

def ValuesIterator(strPayload):
  '''
    'O20000H0U19000LS19000z1525'
    O 20000
    H 0
    U 19000
    L
    S 19000
    z 1525
    k
  '''
  iPosStart = 0
  assert len(strPayload) >= 1
  assert strPayload[0].isalpha()
  for iPos in range(1, len(strPayload)):
    if strPayload[iPos].isalpha():
      yield strPayload[iPosStart], strPayload[iPosStart+1:iPos]
      iPosStart = iPos
  yield strPayload[iPosStart], strPayload[iPosStart+1:len(strPayload)]

if False:
  for strTag, strValue in ValuesIterator('O20000H0U19000LS19000z1525k'):
    print(strTag, strValue)


class GrafanaDumper:
  def __init__(self):
    self.__dictLastValues = {}
    self.__dictObjGrafana = {}
    self.__dictValueMessinterval_ms = {}

  def handleMac(self, iTime_ms, strMac):
    # May be overridden
    pass

  def handleNtpTime(self, iTime_ms, iSecondsSince1970_UnixEpoch):
    # May be overridden
    pass

  def addMeasurement(self, objGrafanaValue, iTime_ms, strValue):
    # May be overridden
    pass

  def readFile(self, strFilename):
    with open(strFilename, 'r') as fLog:
      self.__readFile(fLog)

  def __readFile(self, fLog):
    '''
      funcLine(iTime_ms, strVerb, strPayload)
    '''
    iTime_ms = 0
    for strLine in fLog.readlines():
      strLine = strLine.strip()
      iTickDiff_ms, strVerb, strPayload = strLine.split(' ', 2)
      iTime_ms += int(iTickDiff_ms)

      self.handleLine(iTime_ms, strVerb, strPayload)

    self.dumpLastValues(iTime_ms)

  def dumpLastValues(self, iTime_ms):
    '''
      When we used the hint 'iValueMessinterval_ms' then we should add the horizontal line to the right side of the graph.
    '''
    for strTag, strValue in self.__dictLastValues.items():
      objGrafanaValue = self.__dictObjGrafana[strTag]
      self.addMeasurement(objGrafanaValue, iTime_ms, strValue)

  def handleLine(self, iTime_ms, strVerb, strPayload):
    if strVerb == portable_grafana_datatypes.TAG_GRAFANA_NTP:
      if False:
        # Seconds since 2000-01-01
        iSecondsSince2000 = int(strPayload)
        # https://www.unixtimestamp.com/index.php
        iSecondsSince1970_UnixEpoch = int(iSecondsSince2000 + 946684800.0)
      iSecondsSince1970_UnixEpoch = int(strPayload)
      self.handleNtpTime(iTime_ms, iSecondsSince1970_UnixEpoch)

    if strVerb == portable_grafana_datatypes.TAG_GRAFANA_VERSION:
      self.strVersion = strPayload
      return

    if strVerb == portable_grafana_datatypes.TAG_GRAFANA_MAC:
      self.handleMac(iTime_ms, strMac=strPayload)
      return

    if strVerb == portable_grafana_datatypes.TAG_GRAFANA_DATATYPE:
      strConstructor = strPayload
      objGrafanaValue = portable_grafana_datatypes.Instantiate(strConstructor)
      strTag = objGrafanaValue.strTag
      self.__dictObjGrafana[strTag] = objGrafanaValue
      return

    if strVerb == portable_grafana_datatypes.TAG_GRAFANA_MESSINTERVAL_MS:
      strTag, strMessinterval_ms = strPayload.split()
      self.__dictValueMessinterval_ms[strTag] = int(strMessinterval_ms)
      return

    if strVerb == portable_grafana_datatypes.TAG_GRAFANA_VALUE:
      self.handleMeasurements(iTime_ms, strPayload)
      return

  def handleMeasurements(self, iTime_ms, strPayload):
    for strTag, strValue in ValuesIterator(strPayload):
      objGrafanaValue = self.__dictObjGrafana.get(strTag, None)
      if objGrafanaValue == None:
        print('INFO: Missing tag "%s". This may happen, if a Environs-Sensor was plugged in during operation.' % strTag)
        continue

      if strValue == '':
        strValue = self.__dictLastValues.get(strTag, None)
        if strValue == None:
          print('Why? "%s"' % strTag)
        continue
      if True:
        # Add a value backward using the hint 'iValueMessinterval_ms'.
        strLastValue = self.__dictLastValues.get(strTag, None)
        iValueMessinterval_ms = self.__dictValueMessinterval_ms.get(strTag, None)
        if (strLastValue != None) and (iValueMessinterval_ms != None):
          fValue = objGrafanaValue.convert2float(strLastValue)
          self.addMeasurement(objGrafanaValue, iTime_ms-iValueMessinterval_ms, strLastValue)
      self.addMeasurement(objGrafanaValue, iTime_ms, strValue)
      self.__dictLastValues[strTag] = strValue
