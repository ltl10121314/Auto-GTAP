echo TABLOing %1
tablo -wfp %1 >tb%1.log
if errorlevel 1 goto error
echo   LTGing %1
call ltg %1  >ltgout 2>&1
@echo off
if errorlevel 1 goto error

del opt*.
del *.inf
del *.min
echo Tablo/LTG of %1 finished OK
goto endbat
:error
dir/b tb%1.log
echo ###### %1 Tablo/LTG FAILED #####
echo  Please press Ctrl-C to terminate BAT, or
pause 
:endbat
echo -------


