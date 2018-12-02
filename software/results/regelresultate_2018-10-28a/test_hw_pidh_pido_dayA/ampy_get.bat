set COMPORT=COM39

ampy --port %COMPORT% get /log_00.txt log_00.txt
ampy --port %COMPORT% get /log_grafana_00.txt log_grafana_00.txt

pause
