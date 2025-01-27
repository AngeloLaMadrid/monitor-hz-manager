@echo off
setlocal

:menu
cls
echo ==========================================
echo            MENU PRINCIPAL
echo ==========================================
echo 1. Aplicar ambas acciones (RECOMENDADO!)
echo 2. Ejecutar al inicio
echo 3. Sincronizar icono con Hz al inicio (Evita problemas con iconos) 
echo 4. Salir
echo ==========================================
set /p choice="Seleccione una opcion (1-4): "

if "%choice%"=="1" goto aplicar_ambas
if "%choice%"=="2" goto crear_bat
if "%choice%"=="3" goto colocar_icono
if "%choice%"=="4" goto salir
goto menu

:colocar_icono
python "%~dp0src\python-code\crear_acceso_directo.py"
echo ==========================================
pause
goto menu

:crear_bat
set SCRIPT_PATH=%~dp0src\python-code\verificar_inicio.py
set STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set BAT_FILE=%STARTUP_DIR%\verificar_inicio.bat
echo @echo off > "%BAT_FILE%"
echo python "%SCRIPT_PATH%" >> "%BAT_FILE%"
echo El archivo verificar_inicio.bat ha sido creado en el directorio de inicio.
echo ==========================================
pause
goto menu

:aplicar_ambas
python "%~dp0src\python-code\crear_acceso_directo.py"
set SCRIPT_PATH=%~dp0src\python-code\verificar_inicio.py
set STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set BAT_FILE=%STARTUP_DIR%\verificar_inicio.bat
echo @echo off > "%BAT_FILE%"
echo python "%SCRIPT_PATH%" >> "%BAT_FILE%"
echo El archivo verificar_inicio.bat ha sido creado en el directorio de inicio.
echo ==========================================
pause
goto menu

:salir
endlocal
exit