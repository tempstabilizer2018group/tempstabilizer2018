set COMPORT=COM39

@rem ampy --port %COMPORT% ls
@rem ampy --port %COMPORT% put read_temperature.py
ampy --port %COMPORT% put read_temperature.py
ampy --port %COMPORT% put tests_pinbelegung.py
ampy --port %COMPORT% put mcp4725.py
ampy --port %COMPORT% put tests_dac.py
ampy --port %COMPORT% run tests_dac.py
ampy --port %COMPORT% run tests_pinbelegung.py

pause