@echo off
setlocal

REM Ruta del script de Python
set SCRIPT_PATH=%~dp0src\python-code\verificar_inicio.py

REM Ruta del directorio de inicio
set STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup

REM Ruta del archivo bat que se creará en el inicio
set BAT_FILE=%STARTUP_DIR%\verificar_inicio.bat

REM Crear el archivo bat que llamará al script de Python directamente en el directorio de inicio
echo @echo off > "%BAT_FILE%"
echo python "%SCRIPT_PATH%" >> "%BAT_FILE%"

echo El archivo verificar_inicio.bat ha sido creado en el directorio de inicio.

endlocal
pause