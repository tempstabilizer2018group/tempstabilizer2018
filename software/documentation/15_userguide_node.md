# Node

## Temperature Controller Hardware

### Keypress
short press: Force WLAN replication (longer than 0.2s)
- upload to graphana
- check for software updates

long press. LED on again.  (longer than 5s)
-delete persist data (SetPoint for example, history)

switch power on while Key pressed
-delete flash, force WLAN, try to get new software.

### Specification
Supply Voltage
-Full Range 4.5 to 55V
-Tested Range 12 to 50V

Supply Current: TPD

Heating Power Max
-On a thick Aluminium plate: approx 5W max
-lower on thin and bad conducting metal pieces

Temperature accuracy
See Datasheet MAX30205 for details
-approx +- 0.3 C at room temperature
-stability approx +- 5mK over a day. To get this stability, you have to average multiple measurements. 
