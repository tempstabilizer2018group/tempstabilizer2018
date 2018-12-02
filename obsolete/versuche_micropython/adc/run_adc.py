# Erkenntnisse
# A: Vref
#   ADC misst etwa 0 bis 3.3 V, was 0 bis 4095 entspricht
#   Die Referenzspannung ist 1.21V
#   Die Referenzspannung kann auf Channel 17 gelesen werden (ca. 1500)
#   Die gemessenen Spannung ist: gemessen*1.21V/gemessene_vref

# B: Vref ignorieren
# In "adc.c" steht: #define ADC_SCALE (3.3f / 4095)
#   Die gemessene Spannung ist: gemessen*3.3V/4095
import pyb

adc = pyb.ADC(pyb.Pin.board.A1)  
adc.read() 

#            8765432109876543210
# 0x70000  0b1110000000000000000 channel 16, 17, 18
#          0b1110000000000000001
adcall = pyb.ADCAll(12, 0x70000) # 12 bit resolution, internal channels
adcall.read_core_temp()
29.34426
adcall.read_core_vref() # Reference volatage of 1.21V
1.216044


adcall = pyb.ADCAll(12, 0b1110000000000000010) # 12 bit resolution, internal channels
adcall.read_channel(1) # A1
adcall.read_channel(16) # core temp 
adcall.read_channel(17) # vref
adcall.read_channel(18) # vbat

0V: 0
3.3V: 4094

# A: Spannung messen
adcall = pyb.ADCAll(12, 0b0100000000000000000) # 12 bit resolution, internal channels
i_vref_1 = adcall.read_channel(17)
i_pin_1 = adcall.read_channel(1)
f_pin_Volt = i_pin_1*1.21/i_vref_1
f_pin_Volt

# B: Spannung messen
adc = pyb.ADC(pyb.Pin.board.A1)
adc.read() * 3.3 / 4095.0