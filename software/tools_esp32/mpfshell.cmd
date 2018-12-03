call ../set_environment.cmd

@rem %PYTHON% mpfshell.py --nocache -c "open %COMPORT%"
%PYTHON% mpfshell.py %COMPORT%
pause
