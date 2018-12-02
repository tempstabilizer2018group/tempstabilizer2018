# Speicher als: main.py
#
# Das Script misst die Zeit, um den uP zu starten.
#
# Funktionsweise:
# Das System schläft für 10ms
# Das System wacht auf, schreibt die RTC-Time auf die Konsole und schläft wieder.
# Abbrechen: Viele Male <ctrl-C> drücken.
import time
import machine

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
  if machine.wake_reason() == machine.TIMER_WAKE:
    rtc = machine.RTC()

    yyyy, mm, dd, dummy, hh, mm, ss, ms = rtc.datetime()
    print('rtc raise: %04d.%03d s' % (60*mm+ss, ms))

    time.sleep(1.0)

    yyyy, mm, dd, dummy, hh, mm, ss, ms = rtc.datetime()
    print('rtc set: %04d.%03d s' % (60*mm+ss, ms))
    print()
    time.sleep(0.002)

    machine.deepsleep(10)


# File schreiben
f = open('main.py', 'w')
f.write('''
...
''')
f.close()

# Programm starten
import machine
machine.deepsleep(10)


rtc raise: 0662.596322 s
rtc set: 0663.599255 s

rtc raise: 0663.943802 s
rtc set: 0664.946734 s

rtc raise: 0665.290960 s
rtc set: 0666.293893 s

rtc raise: 0666.638311 s
rtc set: 0667.641244 s

rtc raise: 0667.985810 s
rtc set: 0668.988743 s
  -> 0.3442 s
rtc raise: 0669.332968 s
rtc set: 0670.335900 s
  -> 0.3445 s
rtc raise: 0670.680438 s

Zeit für Wakeup: 0.3445s!!!