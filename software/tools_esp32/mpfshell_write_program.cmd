
call ../set_environment.cmd

@rem https://github.com/wendlers/mpfshell

%PYTHON% mpfshell.py --nocache -n -s mpfshell_mkfs.mpf %COMPORT%

@echo ...filesystem initialized
@echo Type 'enter' to write files to the ESP32...
@pause

@rem %PYTHON% mpfshell.py -o %COMPORT% --loglevel DEBUG --script mpfshell_write_program.mpf
@rem %PYTHON% mpfshell.py --loglevel DEBUG --logfile mpfshell_write_program_log.txt -s mpfshell_write_program.mpf %COMPORT%
%PYTHON% mpfshell.py --nocache -s mpfshell_write_program.mpf %COMPORT%

pause
