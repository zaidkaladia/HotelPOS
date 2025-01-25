@echo off
start /B "pythonw app.py" 
timeout /t 5
start http://127.0.0.1:54321/
