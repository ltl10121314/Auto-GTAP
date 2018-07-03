
rem  This is file MKDIST.BAT.
rem  It creates msplitcom.ZIP for distribution.

del msplitcom.zip

zip msplitcom input\basedata.har 
zip msplitcom input\default.prm 
zip msplitcom input\secsplit.har 
zip msplitcom input\sets.har 
zip msplitcom input\userwgt.har 

rem  Next line adds in files listed in vital.fil
zip msplitcom -@ <vital.fil
dir msplitcom.zip
 
rem  Test the zip 
rd/s/q test
md test
copy msplitcom.zip test
cd test
unzip msplitcom
call compallf.bat
call msplitbat.bat

:endbat
rem  End of MKDIST.BAT

