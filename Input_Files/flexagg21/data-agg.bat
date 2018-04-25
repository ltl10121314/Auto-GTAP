@echo off
rem DATA-AGG.BAT
rem ************
rem
rem aggregates the GTAP data base
rem --  calls command interpreter %COMSPEC% to set up a temporary
rem     environment to avoid environment space problems
rem --  calls GBARUN.BAT to do the work
rem 

%COMSPEC% /e:2048 /c gbarun %1 %2 %3 

rem %1  is always the name of the mapping aggregation 
rem GEMPACK text file, with sufix .txt
rem %2 can be empty, in which case custom behavior is triggered, 
rem or it can be equal to "custom_prefix". 
rem If the latter, then %3 should be equal to the prefix..
