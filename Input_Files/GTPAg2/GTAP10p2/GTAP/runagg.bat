REM Next few lines below are standard -- do not change
@echo off 
if "%2" == "" (
echo 2 parameters required, eg: RunAgg 2004 Default.Txt
echo 1st parameter is location of input files 
echo 2nd parameter is a FlexAgg mapping file 
echo optional 3nd parameter is location of output files 
GOTO :errbat
)
@echo on

del *.log
del *.har
rd/s/q output
md output

REM Next lines are only active if run from GTAPAGG2   
REM They are to assist automatic updating of AggHAR and Txt2Har
REM If main folder has newer version of AggHAR.exe or Txt2Har.exe, copy that here.
REM /D means, copy only if newer; /Y means, suppress overwrite prompt.
if "%2" == "AUTO" (
xcopy /D /Y ..\..\agghar.exe . 
xcopy /D /Y ..\..\txt2har.exe . 
)

REM copy all input files to "input" subfolder [eases CMF preparation]
rd/s/q input
md input
copy %1\*.* input
copy tstrade\*.* input

REM GTAPAgg has already prepared the maphar.dat file and calls RunAgg with %2="AUTO"
if "%2" == "AUTO" GOTO mapready

REM If NOT run by GTAPAgg, translate FlexAgg mapping file into HAR file maphar.dat 
del maphar.dat
txt2har %2 maphar.dat
if errorlevel 1 goto errbat

:mapready
REM end of standard lines 

Rem check maphar.dat and make aggsupp.har file for agghar  
aggcheck -cmf aggcheck.cmf  >>wholejob.log
if errorlevel 1 goto errbat

agghar.exe input\basedata.har aggmain.har aggsupp.har -PMF >>wholejob.log
if errorlevel 1 goto errbat

rem make aggregate sets and flows files
aggdat -cmf aggdat.cmf >>wholejob.log
if errorlevel 1 goto errbat

rem make aggregate parameter file
aggpar -cmf aggpar.cmf >>wholejob.log
if errorlevel 1 goto errbat

rem run gtapview on aggregated data
gtapview -cmf gtapview.cmf >>wholejob.log
if errorlevel 1 goto errbat

rem create samview of aggregated data
samview -cmf samview.cmf >>wholejob.log
if errorlevel 1 goto errbat

REM  Next job aggregates input\gsdvole.har if it is present
if exist input\gsdvole.har (
agghar.exe input\gsdvole.har output\gsdvole.har aggsupp.har -PMF >>wholejob.log
rem aggvole -cmf aggvole.cmf >>wholejob.log
if errorlevel 1 goto errbat
)

REM  Next job aggregates input\co2.har if it is present
if exist input\co2.har (
rem aggemiss -cmf aggemiss.cmf >>wholejob.log
agghar.exe input\co2.har output\co2.har aggsupp.har -PMF >>wholejob.log
if errorlevel 1 goto errbat
)

REM  Next job aggregates input\tstrade.har if it is present
if exist input\tstrade.har (
agghar.exe input\tstrade.har output\tstrade.har aggsupp.har -PMF >>wholejob.log
rem aggtrade -cmf aggtrade.cmf >>wholejob.log
if errorlevel 1 goto errbat
)

REM lines below this are standard -- do not change
copy input\metadata.har output
@echo Finished OK, creating following output files:
dir/od/b output
if not "%3" == "" copy output\*.* %3
exit /b 0 

:errbat
@echo List of files in creation order >>wholejob.log
dir/od >>wholejob.log
REM existence of file error.log tells GTAPAgg that there was a problem
copy wholejob.log error.log
@echo THERE WAS AN ERROR -- see end of ERROR.LOG
exit /b 1 

