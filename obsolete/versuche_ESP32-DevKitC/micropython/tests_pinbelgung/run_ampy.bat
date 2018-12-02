set COMPORT=COM39

@rem ampy --port %COMPORT% ls
@rem ampy --port %COMPORT% put read_temperature.py
ampy --port %COMPORT% put read_temperature.py
ampy --port %COMPORT% run tests_pinbelegung.py

pause