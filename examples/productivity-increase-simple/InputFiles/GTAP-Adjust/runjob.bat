echo running %1 with %2 

del %1.gst 2>nul
del %1.gss 2>nul
tablo -pgs %1 >tablo_%1.log
if errorlevel 1 goto error
gemsim -cmf %2 >nul
rem   If using Fortran-based exes, "rem" out the 5 lines above
rem   and activate the line below
rem %1 -cmf %2 >nul
if errorlevel 1 goto error

goto endbat
:error
ECHO  ERROR running program %1 using %2 
:endbat
