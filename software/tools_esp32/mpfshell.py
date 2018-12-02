#!c:\program files\python27\python.exe

import sys

from mp.mpfshell import main

try:
    main()
except Exception as e:
    sys.stderr.write(str(e) + "\n")
    exit(1)
