@echo off
rem =======================================================================
rem GBARUN.BAT: Aggregation Program Batch File
rem This BAT file is for use in generating an aggregation from the
rem      GTAP global database with dimensions defined in input file.
rem      It produces aggregated sets, data, and parameters files.
rem R.A. McDougall, Betina Dimaranan.  2001-06-21
rem Substantial modifications by Nelson Villoria and Robert McDougall
rem (2010-19-05)
rem =======================================================================

rem initialize
rem ----------

:: These two variables help displaying error messages when FlexAgg is
:: used from elsewhere in the file system.
set AGGDIR=%CD%
set BATCHDIR=%~dp0

if "%1" == "" goto usage
if "%1" == "custom_prefix" goto usage
if not exist %1.txt goto nosuch
rem The first value after data-agg is the aggregation file, always.
set AGGFILE=%1
 
if "%2" == "" goto default
rem this is for newer syntax of the form:
rem data-agg %1=my_agg %2=custom_prefix %3=prefix
if "%2" == "custom_prefix" goto custom

set GTAPOUT=%2
if not "%GTAPOUT%" == "%2" goto errenv
if not exist %GTAPOUT%\NUL goto nosuch

rem Default is short syntax DATA-AGG map-file:
rem DATA_AGG %1=map-file 
:default 
if errorlevel 1 goto usage
if not exist %1\NUL mkdir %1
set GTAPOUT=%1
set GTAPWORK=.
set PREFIX=gsd
rem checks that the gsdset, gsddat, and gsdpar, are indeed in the folder
IF NOT exist gsdset.har goto gsd_err
IF NOT exist gsddat.har goto gsd_err
IF NOT exist gsdpar.har goto gsd_err
goto startmap

rem: Syntax 3, custom prefix:
rem DATA-AGG %1=my_agg %2=custom_prefix %3=prefix
:custom 
if errorlevel 1 goto usage
if not exist %1\NUL mkdir %1
set GTAPOUT=%1
set GTAPWORK=.
set PREFIX=%3
rem checks that the *set, *dat, and *par, are indeed in the folder
IF NOT exist %PREFIX%set.har goto pre_err
IF NOT exist %PREFIX%dat.har goto pre_err
IF NOT exist %PREFIX%par.har goto pre_err
goto startmap

rem read sets and mapping schemes
rem -----------------------------

:startmap
echo Processing aggregation mapping/sets information. . .

rem Reads GEMPACK txt mapping file and converts it to gmap.har
 >%GTAPWORK%\gmap.sti echo bat  !  This runs the program in "batch" mode
>>%GTAPWORK%\gmap.sti echo. 
>>%GTAPWORK%\gmap.sti echo n
>>%GTAPWORK%\gmap.sti echo %GTAPWORK%\gmap.har
>>%GTAPWORK%\gmap.sti echo at
>>%GTAPWORK%\gmap.sti echo %AGGFILE%.txt
>>%GTAPWORK%\gmap.sti echo s
>>%GTAPWORK%\gmap.sti echo. 
>>%GTAPWORK%\gmap.sti echo. 
>>%GTAPWORK%\gmap.sti echo. 
>>%GTAPWORK%\gmap.sti echo. 
>>%GTAPWORK%\gmap.sti echo. 
>>%GTAPWORK%\gmap.sti echo XXX
>>%GTAPWORK%\gmap.sti echo XXX
>>%GTAPWORK%\gmap.sti echo. 
>>%GTAPWORK%\gmap.sti echo ex
>>%GTAPWORK%\gmap.sti echo 0
modhar < %GTAPWORK%\gmap.sti > %GTAPWORK%\gmap.log
if errorlevel 1 goto maperr
del gmap.sti gmap.log

echo Checking that aggregated sets are well defined. . .
> %GTAPWORK%\aggcheck.sti echo bat  !  This runs the program in "batch" mode
>> %GTAPWORK%\aggcheck.sti echo. 
>> %GTAPWORK%\aggcheck.sti echo %PREFIX%set.har
>> %GTAPWORK%\aggcheck.sti echo gmap.har
>> %GTAPWORK%\aggcheck.sti echo aggcheck.har
aggcheck < aggcheck.sti > aggcheck.log
if errorlevel 1 goto set_err
del aggcheck.har aggcheck.sti aggcheck.log

echo Processing user provided parameters . . .
 >%GTAPWORK%\gepar.sti echo bat  !  This runs the program in "batch" mode
>>%GTAPWORK%\gepar.sti echo. 
>>%GTAPWORK%\gepar.sti echo n
>>%GTAPWORK%\gepar.sti echo %GTAPWORK%\gepar.har
>>%GTAPWORK%\gepar.sti echo at
>>%GTAPWORK%\gepar.sti echo %AGGFILE%.txt
>>%GTAPWORK%\gepar.sti echo s
>>%GTAPWORK%\gepar.sti echo XXX 
>>%GTAPWORK%\gepar.sti echo XXX
>>%GTAPWORK%\gepar.sti echo XXX 
>>%GTAPWORK%\gepar.sti echo XXX
>>%GTAPWORK%\gepar.sti echo XXX
>>%GTAPWORK%\gepar.sti echo. 
>>%GTAPWORK%\gepar.sti echo. 
>>%GTAPWORK%\gepar.sti echo XXX 
>>%GTAPWORK%\gepar.sti echo ex
>>%GTAPWORK%\gepar.sti echo 0
modhar < %GTAPWORK%\gepar.sti > %GTAPWORK%\gepar.log
if errorlevel 1 goto err_mpha
del gepar.sti gepar.log

rem data file
rem ---------

echo Aggregating data file %PREFIX%dat.har to %PREFIX%gdat.har. . .
 >%GTAPWORK%\aggdat.sti echo BAT                        
>>%GTAPWORK%\aggdat.sti echo.                           
>>%GTAPWORK%\aggdat.sti echo %PREFIX%dat.har                 
>>%GTAPWORK%\aggdat.sti echo %PREFIX%set.har        
>>%GTAPWORK%\aggdat.sti echo gmap.har
>>%GTAPWORK%\aggdat.sti echo %GTAPOUT%\%PREFIX%gdat.har         
>>%GTAPWORK%\aggdat.sti echo %GTAPOUT%\%PREFIX%gset.har         
aggdat <%GTAPWORK%\aggdat.sti >%GTAPWORK%\aggdat.log
if errorlevel 1 goto err_data
del aggdat.sti aggdat.log

rem parameters file
rem ---------------

echo Aggregating parameters file %PREFIX%par.har to %PREFIX%gpar.har. . .
 >%GTAPWORK%\aggpar.sti echo bat  !  This runs the program in "batch" mode
>>%GTAPWORK%\aggpar.sti echo. 
>>%GTAPWORK%\aggpar.sti echo %PREFIX%dat.har
>>%GTAPWORK%\aggpar.sti echo %PREFIX%par.har
>>%GTAPWORK%\aggpar.sti echo gepar.har
>>%GTAPWORK%\aggpar.sti echo %PREFIX%set.har
>>%GTAPWORK%\aggpar.sti echo gmap.har
>>%GTAPWORK%\aggpar.sti echo %GTAPOUT%\%PREFIX%gpar.har
aggpar <%GTAPWORK%\aggpar.sti > %GTAPWORK%\aggpar.log
if errorlevel 1 goto err_prmt
del aggpar.sti aggpar.log

rem energy volume data
rem ------------------
IF NOT EXIST %GTAPWORK%\%PREFIX%vole.har echo No energy volumes to be aggregated...
IF NOT EXIST %GTAPWORK%\%PREFIX%vole.har goto trade

echo Aggregating energy volume data file . . .

 >%GTAPWORK%\aggvole.sti echo BAT                        
>>%GTAPWORK%\aggvole.sti echo.                           
>>%GTAPWORK%\aggvole.sti echo %PREFIX%vole.har                
>>%GTAPWORK%\aggvole.sti echo %PREFIX%set.har                 
>>%GTAPWORK%\aggvole.sti echo gmap.har        
>>%GTAPWORK%\aggvole.sti echo %GTAPOUT%\%PREFIX%gvole.har        
aggvole <%GTAPWORK%\aggvole.sti >%GTAPWORK%\aggvole.log
if errorlevel 1 goto err_evdt
del aggvole.sti aggvole.log

rem time series trade data
rem ------------------
:trade

IF NOT EXIST %GTAPWORK%\%PREFIX%trade.har echo No time series trade data to be aggregated...
IF NOT EXIST %GTAPWORK%\%PREFIX%trade.har goto views

echo Aggregating the time series trade data file . . .
 >%GTAPWORK%\aggtrade.sti echo BAT                        
>>%GTAPWORK%\aggtrade.sti echo.                           
>>%GTAPWORK%\aggtrade.sti echo %PREFIX%trade.har                
>>%GTAPWORK%\aggtrade.sti echo %PREFIX%set.har                 
>>%GTAPWORK%\aggtrade.sti echo gmap.har        
>>%GTAPWORK%\aggtrade.sti echo %GTAPOUT%\%PREFIX%gtrade.har        
aggtrade <%GTAPWORK%\aggtrade.sti >%GTAPWORK%\aggtrade.log
if errorlevel 1 goto err_trade
del aggtrade.sti aggtrade.log

:views
rem gtapview and gtaptax files
rem --------------------------
echo Creating GTAPView and GTAPTax files . . .
 >%GTAPWORK%\gtapview.sti echo BAT                        
>>%GTAPWORK%\gtapview.sti echo.                           
>>%GTAPWORK%\gtapview.sti echo %GTAPOUT%\%PREFIX%gdat.har         
>>%GTAPWORK%\gtapview.sti echo %GTAPOUT%\%PREFIX%gset.har         
>>%GTAPWORK%\gtapview.sti echo %GTAPOUT%\%PREFIX%gpar.har         
>>%GTAPWORK%\gtapview.sti echo %GTAPOUT%\%PREFIX%gview.har        
>>%GTAPWORK%\gtapview.sti echo %GTAPOUT%\%PREFIX%gtax.har         
gtapview <%GTAPWORK%\gtapview.sti >%GTAPWORK%\gtapview.log
if errorlevel 1 goto err_gvew
del gtapview.sti gtapview.log

rem SAM files
rem --------------------------
echo Creating SAM view of the database . . .
 >%GTAPWORK%\samview.sti echo BAT                        
>>%GTAPWORK%\samview.sti echo.                           
>>%GTAPWORK%\samview.sti echo %GTAPOUT%\%PREFIX%gdat.har         
>>%GTAPWORK%\samview.sti echo %GTAPOUT%\%PREFIX%gset.har         
>>%GTAPWORK%\samview.sti echo %GTAPOUT%\%PREFIX%gpar.har         
>>%GTAPWORK%\samview.sti echo %GTAPOUT%\%PREFIX%gsam.har        
samview <%GTAPWORK%\samview.sti >%GTAPWORK%\samview.log
if errorlevel 1 goto err_sam
del samview.sti samview.log

rem summary in file info.txt
rem -------
> %GTAPOUT%\info.txt echo The following files were aggregated using %GTAPOUT%.txt:
IF EXIST %GTAPWORK%\%PREFIX%dat.har >> %GTAPOUT%\info.txt echo %PREFIX%dat.har
IF EXIST %GTAPWORK%\%PREFIX%par.har >> %GTAPOUT%\info.txt echo %PREFIX%par.har
IF EXIST %GTAPWORK%\%PREFIX%vole.har >> %GTAPOUT%\info.txt echo %PREFIX%vole.har
IF EXIST %GTAPWORK%\%PREFIX%trade.har >> %GTAPOUT%\info.txt echo %PREFIX%trade.har
>> %GTAPOUT%\info.txt echo on %date% - %time%
IF %GTAPWORK%==. >> %GTAPOUT%\info.txt echo with dissagregated data placed at %AGGDIR%.
>> %GTAPOUT%\info.txt echo The aggregated data is at %CD%\%GTAPOUT%.
del gmap.har gepar.har

echo Done . . .

goto end

rem error messages etc.
rem ------------------

:usage
echo Welcome to FlexAgg2.
echo USAGE:                                               
echo Syntax 1: DATA-AGG mapfile
echo Syntax 2: DATA-AGG mapfile custom_prefix
echo In mapfile, omit extension ".TXT"
echo Please see the README file for further details.
exit /b 1

:nosuch
echo ERROR:  User-specified mapping aggregation files does not exist.
exit /b 2

:gsd_err
echo ERROR: I can't find one (or more) of the following files:
echo        gsdset.har, gsddat.har, or gsdpar.har.
echo        Perhaps you want to use a custom prefix?
echo        If so, use:
echo        DATA-AGG mapfile custom_prefix prefix
exit /b 3

:pre_err
echo ERROR: I can't find one (or more) of the following files:
echo        %PREFIX%set.har, %PREFIX%dat.har, or %PREFIX%par.har.
echo        Are you sure you used the right prefix?
echo        Recall, prefix syntax is:
echo        DATA-AGG my_agg custom_prefix prefix
exit /b 4

:maperr
echo ERROR: There is an error in the aggregation mapping file. 
echo        See gmap.log in the user-selected directory.
exit /b 5

: set_err
echo ERROR: The aggregated and dissagregated sets are
echo        inconsistent. See aggcheck.log in the user-selected
echo        directory.
del gmap.har gepar.har aggcheck.har aggcheck.sti 
exit /b 6

:err_mpha
echo.  ERROR: can't convert mapping file to HAR format. See gmap.log
echo          in the user-selected directory.
exit /b 7

:err_data
echo.  ERROR: can't aggregate data file. See aggdat.log in the
echo          user-selected directory.
exit /b 8

:err_prmt
echo  ERROR: can't aggregate parameters file. See aggpar.log in
echo         the user-selected directory.
exit /b 9

:err_evdt
echo.  ERROR: can't aggregate energy volume data file. See aggvole.log
echo          in the user-selected directory.
goto end
exit /b 10

:err_trade
echo.  ERROR: can't aggregate the tiem series data file. See aggtrade.log
echo          in the user-selected directory.
goto end
exit /b 11


:err_gvew
echo.  ERROR: can't create gtapview file. See gtapview.log in the
echo          user-selected directory.
exit /b 12

:err_sam
echo.  ERROR: can't create SAM view file. See samview.log in the
echo          user-selected directory.
exit /b 13


:end
 
