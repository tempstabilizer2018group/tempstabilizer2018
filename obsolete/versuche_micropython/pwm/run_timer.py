from pyb import Timer

p = pyb.Pin.board.A0 # X1 has TIM2, CH1: A0
tim = Timer(2, freq=1000)  # 1000 Hz
ch = tim.channel(1, Timer.PWM, pin=p)
ch.pulse_width_percent(50)

ch.pulse_width_percent(99.999)


ch.pulse_width(100)
# Gemessen: 1 us
# 1Puls: 10ns
# 100MHz

pulse_width_percent  pulse_width
0.0                  0
10.0                 8400
100.0                84000

3.3V auf PWM2
PWM auf PWM1

pulse_width_percent	mA
50	0
60	10
70	53
80	99
90	106
100	112


