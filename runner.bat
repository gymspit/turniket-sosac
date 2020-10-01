@echo off

echo program starting...

:pythonStart

echo starting the script again...
python "path to script"
timeout /t 10	 

goto pythonStart