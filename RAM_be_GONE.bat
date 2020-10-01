@echo off

echo program starting...

:pythonStart

echo starting again...
python "path to script"
timeout /t 10	 

goto pythonStart