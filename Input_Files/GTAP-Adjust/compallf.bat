rem  recompile all programs (EXE/Fortran version)
echo off 
call compit gtp2norm  
if errorlevel 1 goto error
call compit gtpvew  
if errorlevel 1 goto error
call compit norm2gtp  
if errorlevel 1 goto error
call compit normchek  
if errorlevel 1 goto error
call compit GtapAdjust  
if errorlevel 1 goto error
call compit GTAP  
if errorlevel 1 goto error

echo ###### BATCH JOB SUCCESSFUL #####
goto endbat
:error
echo ###### ERROR: BATCH JOB FAILED #####
:endbat

