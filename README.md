AUTHOR: Solid_HabuRex 

VERSION: 1.0 

DESCRIPTION:
This is a small script I've written to allow you to perform a baseline scan and then a comparative scan versus the baseline or the results from the last run scan. It has functionality that allows you to create a wholey new baseline as well as will notify you via terminal output if it found something AND log it in the Syslog. 

ARCHITECTUE:
Currently this script is confirmed working on Ubunutu 18.04.1 LTS, however it SHOULD work on ANY Unix system provided that /var/log/syslog is the path that your syslog lives at.

CAVEATS: 
Because of the nature of what it is doing ( a full dirwalk as well as writing to the Syslog) you are going to want to make sure that this script is run as root.

SYNTAX:
python3.6 hiddenDirCheck.py [ < -l | --lastscan > || < -b | --basescan > || < -n | --newbase > ]


