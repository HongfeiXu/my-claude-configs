@echo off
setlocal

set "SOURCE=%~dp0skills"
set "TARGET=%USERPROFILE%\.claude\skills"

if not exist "%SOURCE%" (
    echo Error: skills directory not found at %SOURCE%
    exit /b 1
)

if not exist "%TARGET%" mkdir "%TARGET%"

echo Syncing skills from %SOURCE% to %TARGET%
echo.

for /D %%d in ("%SOURCE%\*") do (
    echo  [+] %%~nxd
    robocopy "%%d" "%TARGET%\%%~nxd" /E /MIR /NJH /NJS /NDL /NFL >nul
)

echo.
echo Done. Installed skills:
for /D %%d in ("%TARGET%\*") do echo  - %%~nxd
