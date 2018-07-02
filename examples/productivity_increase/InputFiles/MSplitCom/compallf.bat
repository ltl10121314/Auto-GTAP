
rem  recompile all MSplitCom programs (EXE/Fortran version)

@echo off 
call compit balflo  
if errorlevel 1 goto error
call compit postbal  
if errorlevel 1 goto error
call compit expwgt  
if errorlevel 1 goto error
call compit fullsum  
if errorlevel 1 goto error
call compit gtp2norm  
if errorlevel 1 goto error
call compit gtpvew  
if errorlevel 1 goto error
call compit norm2gtp  
if errorlevel 1 goto error
call compit normchek  
if errorlevel 1 goto error
call compit sumsplit  
if errorlevel 1 goto error
call compit split1  
if errorlevel 1 goto error
call compit splitflo  
if errorlevel 1 goto error

echo ###### BATCH JOB SUCCESSFUL #####
goto endbat
:error
echo ###### ERROR: BATCH JOB FAILED #####
:endbat

