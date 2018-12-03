
call ../set_environment.cmd

del simulation_test_*.txt
del simulation_test_*.png

%PYTHON% simulation_test_hw_hal.py
%PYTHON% simulation_test_schrittantwort.py
%PYTHON% simulation_test_tagesmodell.py
%PYTHON% simulation_test_dayestimator.py
%PYTHON% simulation_test_pidh.py
%PYTHON% simulation_test_pidh_pido.py
%PYTHON% simulation_test_pidh_pido_log_grafana.py
%PYTHON% simulation_test_pidh_pido_day.py
pause
