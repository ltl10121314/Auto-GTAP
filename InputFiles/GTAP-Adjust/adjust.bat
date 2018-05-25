@echo off 
goto endtext

This BAT file runs GTAP adjuster.
Input files should be in INPUT folder:
      basedata.har
      default.prm 
      sets.har 
Adjusted outputs should appear in OUTPUT folder,
also called         basedata.har default.prm sets.har.
Other (intermediate of diagnostic) outputs should appear in WORK folder.

:endtext

rem   Clean up junk files.
del *.bak 2>nul
del *.log 2>nul
del *.gss 2>nul
del *.gst 2>nul
rem   Ensure that work and output folders exist.
md work   2>nul
md output 2>nul
rem   Remove all files in work and output folders.
del/Q work\*.*
del/Q output\*.*

rem   Gtp2Norm turns a standard GTAP database [at input\basedata.har] into a 
rem   simplified [normalized] form [at work\orig.har] which is easier to manipulate.
call runjob Gtp2Norm Gtp2Norm.cmf 
if errorlevel 1 goto error

rem   Parameters file is copied unchanged.
copy input\default.prm output >nul

rem   Next reads unadjusted GTAP data (in normalized form) at work\orig.har to 
rem   produce a standard set of summaries/checks/diagnostics in work\normchk0.har.  
call runjob normchek normchk0.cmf  
if errorlevel 1 goto error

rem   Next reads unadjusted GTAP data (in normalized form) at work\orig.har to 
rem   produce adjusted data at work\adjusted.har.
call runjob GtapAdjust input\GtapAdjust.cmf
if errorlevel 1 goto error

echo running DiffHar to compare adjusted with unadjusted data
rem   Next makes report of all percent changes in flows caused by GtapAdjust  
diffhar work\orig.har work\adjusted.har work\PctDiffs.har P  >diffhar1.log
if errorlevel 1 goto error
rem   Next makes report of all ordinary changes in flows caused by GtapAdjust  
diffhar work\orig.har work\adjusted.har work\OrdDiffs.har D  >diffhar2.log
if errorlevel 1 goto error

rem   Next reads adjusted data at work\adjusted.har to produce a standard
rem   set of summaries/checks/diagnostics in work\normchk1.har  
call runjob NormChek NormChk1.cmf  
if errorlevel 1 goto error

rem   Next converts final scaled data in "normalized" format at work\adjusted.har
rem   into final GTAP format files basedata.har and sets.har in output folder
call runjob Norm2Gtp Norm2Gtp.cmf 
if errorlevel 1 goto error

rem   Next produces standard GTAP summary/diagnostics from output\basedata.har.
rem   Report files are output\gtapview.har and output\taxrates.har.
call runjob GtpVew GtpVew.cmf 
if errorlevel 1 goto error

rem   Next is optional: uses files in output folder to run standard GTAP simulation
rem call runjob GTAP GTAP.cmf 
rem if errorlevel 1 goto error

echo.
echo BATCH JOB SUCCESSFUL -- see following files in output folder:
dir/b output 
goto endbat
:error
echo ###### ERROR: BATCH JOB FAILED #####
echo Check log file; most recent is listed last
dir/b/od *.log
:endbat
