@echo off
setlocal

REM Ruta del script de Python
set SCRIPT_PATH=%~dp0src\python-code\verificar_inicio.py

REM Ruta del archivo bat que se copiará al inicio
set BAT_FILE=%~dp0verificar_inicio.bat

REM Crear el archivo bat que llamará al script de Python
echo @echo off > "%BAT_FILE%"
echo python "%SCRIPT_PATH%" >> "%BAT_FILE%"

REM Ruta del directorio de inicio
set STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup

REM Copiar el archivo bat al directorio de inicio
copy "%BAT_FILE%" "%STARTUP_DIR%"

echo El archivo verificar_inicio.bat ha sido copiado al directorio de inicio.

endlocal
pause