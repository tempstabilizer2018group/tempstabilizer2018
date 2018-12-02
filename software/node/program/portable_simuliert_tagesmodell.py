# -*- coding: utf-8 -*-
import math
import random

import portable_constants
import config_app

class Tagesmodell:
  def __init__(self, fRandom=0.1, fTempBase_C=22.0, fFactorDay_C=2.0, fFactorWeek_C=1.0):
    random.seed(9001)
    self.fRandom = fRandom
    self.fTempBase_C = fTempBase_C
    self.fFactorDay_C = fFactorDay_C
    self.fFactorWeek_C = fFactorWeek_C

  def get_fTemp_C(self, iTime_ms):
    assert type(iTime_ms) == type(0)
    fTime_s = iTime_ms/1000.0
    fTemp_C = self.fTempBase_C + math.sin(2.0*math.pi*fTime_s/portable_constants.DAY_S)*self.fFactorDay_C + math.sin(2.0*math.pi*fTime_s/portable_constants.WEEK_S)*self.fFactorWeek_C
    if self.fRandom != None:
      fTemp_C += random.uniform(-self.fRandom, self.fRandom)
    return fTemp_C

class TagesmodellList:
  def __init__(self, listTemperatures_ms):
    self.listTemperatures_ms = list(listTemperatures_ms)
    self.listTemperatures_ms.sort()

  def get_fTemp_C(self, iTime_ms):
    assert type(iTime_ms) == type(0)
    fTemp_C = 0.0
    for iTime_ms_, fTemp_C_ in self.listTemperatures_ms:
      if iTime_ms_ <= iTime_ms:
        fTemp_C = fTemp_C_
        continue
      break
    return fTemp_C

class TagesmodellConstant:
  def __init__(self, fTempEnvirons_C):
    self.fTempEnvirons_C = fTempEnvirons_C

  def get_fTemp_C(self, iTime_ms):
    return self.fTempEnvirons_C
