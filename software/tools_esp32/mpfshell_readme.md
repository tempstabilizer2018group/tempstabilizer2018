https://github.com/wendlers/mpfshell

pip install mpfshell

C:\Program Files\Python27\Lib\site-packages\mp\mpfshell.py

C:\Program Files\Python27\Scripts\mpfshell.py
C:\Program Files\Python27\Scripts\mpfshell.bat


C:\Projekte\temp_stabilizer_2018\temp_stabilizer_2018\Tools>python mpfshell.py --help
usage: mpfshell.py [-h] [-c [COMMAND [COMMAND ...]]] [-s SCRIPT] [-n]
                   [--nocolor] [--nocache] [--logfile LOGFILE]
                   [--loglevel LOGLEVEL] [--reset] [-o BOARD]
                   [board]

positional arguments:
  board                 directly opens board

optional arguments:
  -h, --help            show this help message and exit
  -c [COMMAND [COMMAND ...]], --command [COMMAND [COMMAND ...]]
                        execute given commands (separated by ;)
  -s SCRIPT, --script SCRIPT
                        execute commands from file
  -n, --noninteractive  non interactive mode (don't enter shell)
  --nocolor             disable color
  --nocache             disable cache
  --logfile LOGFILE     write log to file
  --loglevel LOGLEVEL   loglevel (CRITICAL, ERROR, WARNING, INFO, DEBUG)
  --reset               hard reset device via DTR (serial connection only)
  -o BOARD, --open BOARD
                        directly opens board

C:\Projekte\temp_stabilizer_2018\temp_stabilizer_2018\Tools>