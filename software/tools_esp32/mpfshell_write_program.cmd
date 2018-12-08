
call ../set_environment.cmd

@rem https://github.com/wendlers/mpfshell

set PATH=%PYTHONDIR%

python.exe --version

python.exe mpfshell.py -s mpfshell_mkfs.mpf %COMPORT%

@echo ...filesystem initialized
@echo Type 'enter' to write files to the ESP32...
@pause

@rem %PYTHON% mpfshell.py -o %COMPORT% --loglevel DEBUG --script mpfshell_write_program.mpf
@rem %PYTHON% mpfshell.py --loglevel DEBUG --logfile mpfshell_write_program_log.txt -s mpfshell_write_program.mpf %COMPORT%
python.exe mpfshell.py -s mpfshell_write_program.mpf %COMPORT%

pause
