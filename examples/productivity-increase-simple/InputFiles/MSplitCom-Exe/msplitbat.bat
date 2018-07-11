@echo off 
rem runs multiple SPLITCOM
rem inputs should be in INPUT folder:
rem         basedata.har default.prm secsplit.har sets.har userwgt.har
rem final outputs should appear in OUTPUT folder:
rem         basedata.har default.prm sets.har
rem other outputs should appear in WORK folder.

rem cleanup junk files
del *.bak 2>nul
del *.log 2>nul
del *.flg 2>nul
rem ensure that work and output folders exist
md work   2>nul
md output 2>nul

rem goto stage3

rem --------------- STAGE 1 -- split original data, and scale to impose balance

rem remove all files in work and output folders
del/Q work\*.*
del/Q output\*.*

REM Split1 reads and checks new sector sets and mappings in input\secsplit.har
REM and creates work\splitwgt.har: a dummy user file of splitting weight
echo doing split1
split1 -cmf split1.cmf >nul  
if errorlevel 1 goto error
if not exist input\userwgt.har copy work\splitwgt.har input\userwgt.har

REM gtp2norm turns a standard GTAP database [at input\basedata.har] into a 
REM simplified [normalized] form [at work\orig.har] which is easier to manipulate.
echo doing gtp2norm  
gtp2norm -cmf gtp2norm.cmf >nul
if errorlevel 1 goto error

REM next reads original GTAP data at work\orig.har to produce a standard set of
REM summaries/checks/diagnostics in work\normchk0.har  []
echo doing normchek 
normchek -cmf normchk0.cmf >nul
if errorlevel 1 goto error

REM next is checking that SMRY, WSUM and WGTS headers calculated by gtp2norm
REM from original GTAP format are the same as SMRY, WSUM and WGTS headers
REM calculated by NORMCHEK for normalized format
echo doing diffhar 
diffhar work\gtp2norm.har work\normchk0.har diffs.har D  >diffhar0.log
if errorlevel 1 goto error

rem scale users WGTS and WSUM headers to add up to original GTAP data, and be consistent
echo doing sumsplit 
sumsplit -cmf sumsplit.cmf >nul
if errorlevel 1 goto error

rem produce SMRY header which adds up to original GTAP data, and is consistent
echo doing fullsum 
fullsum -cmf fullsum.cmf >nul
if errorlevel 1 goto error

:stage2
rem --------------- STAGE 2 -- split original data, and scale to impose balance

rem construct full-size splitting weights from SMRY
echo doing expwgt 
expwgt -cmf expwgt.cmf >nul
if errorlevel 1 goto error

rem next uses full-size splitting weights to expand the data to new dimensions
echo doing splitflo 
splitflo -cmf splitflo.cmf >nul
if errorlevel 1 goto error

REM next reads expanded unscaled data at work\splitflo.har to produce a standard
REM set of summaries/checks/diagnostics in work\normchk1.har  
echo doing normchek 
normchek -cmf normchk1.cmf >nul
if errorlevel 1 goto error
echo doing balflo   ... this takes a bit longer
balflo -cmf balflo.cmf >nul
if errorlevel 1 goto error

REM next creates postbal.har
echo doing postbal 
postbal -cmf postbal.cmf >nul
if errorlevel 1 goto error

REM next reads expanded scaled data at work\postbal.har to produce a standard
REM set of summaries/checks/diagnostics in work\normchk2.har  
echo doing normchek 
normchek -cmf normchk2.cmf >nul
if errorlevel 1 goto error

REM next compares postbal.har with splitflo.har -- showing % changes made by balflo.
echo doing diffhar 
diffhar work\postbal.har work\splitflo.har work\balpcent.har P >diffhar1.log
if errorlevel 1 goto error
 
:stage3 
rem --------------- STAGE 3 -- converting back to GTAP format and checking

REM next converts final scaled data in "normalized" format at work\postbal.har
REM into final GTAP format files basedata.har and sets.har in output folder
echo doing norm2gtp 
norm2gtp -cmf norm2gtp.cmf >nul
if errorlevel 1 goto error

rem next produces standard GTAP summary/diagnostics
echo doing gtpvew 
gtpvew -cmf gtpvew.cmf >nul
if errorlevel 1 goto error

rem next aggregates final output back to original dimensions
echo doing agghar 
agghar output\basedata.har work\reagg.har work\aggsupp.har -PM >agghar.log
if errorlevel 1 goto error
rem and checks that aggregated values match originals
echo doing diffhar 
diffhar input\basedata.har work\reagg.har work\diffs.har D >diffhar2.log
if errorlevel 1 goto error

echo.
echo BATCH JOB SUCCESSFUL -- see following files in output folder:
dir/b output 
goto endbat
:error
echo ###### ERROR: BATCH JOB FAILED #####
echo Check log file; most recent is listed last
dir/b/od *.log
rem  SplitCom detects errors through the existence of err.flg
dir/od *.log >err.flg
rem echo Please press CTRL-C to terminate batch job
rem pause
:endbat
