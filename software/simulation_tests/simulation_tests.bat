@rem call simulation_tests_clean_results.bat
del simulation_test_*.txt
del simulation_test_*.png

set PYTHON="C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\python.exe"
set PYTHONPATH=..\tools_pyplot;..\node\config;..\node\program;..\simulation;..\http_server\python
%PYTHON% simulation_test_hw_hal.py
%PYTHON% simulation_test_schrittantwort.py
%PYTHON% simulation_test_tagesmodell.py
%PYTHON% simulation_test_dayestimator.py
%PYTHON% simulation_test_pidh.py
%PYTHON% simulation_test_pidh_pido.py
%PYTHON% simulation_test_pidh_pido_log_grafana.py
%PYTHON% simulation_test_pidh_pido_day.py
pause
