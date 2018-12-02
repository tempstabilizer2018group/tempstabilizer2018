@rem set PATH="c:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\"

@rem https://github.com/wendlers/mpfshell

python mpfshell.py --nocache -n -s mpfshell_mkfs.mpf COM4

@echo ...filesystem initialized
@echo Type 'enter' to write files to the ESP32...
@pause

@rem python mpfshell.py -o COM39 --loglevel DEBUG --script mpfshell_write_program.mpf
@rem python mpfshell.py --loglevel DEBUG --logfile mpfshell_write_program_log.txt -s mpfshell_write_program.mpf COM39
python mpfshell.py --nocache -s mpfshell_write_program.mpf COM4

pause
