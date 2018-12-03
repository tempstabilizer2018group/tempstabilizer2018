@echo "%0": initializing environment


IF %computername%==MAERKI-LENOVO @set PYTHONDIR="C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64"

@set PYTHON=%PYTHONDIR%\python.exe
@set PYTHONPATH=%~dp0\tools_pyplot;%~dp0\node\config;%~dp0\node\program;%~dp0\simulation;%~dp0\http_server\python

