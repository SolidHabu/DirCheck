AUTHOR: Solid_HabuRex 

VERSION: 1.0 

DESCRIPTION:
This is a small script I've written to allow you to perform a baseline scan and then a comparative scan versus the baseline or the results from the last run scan. It has functionality that allows you to create a wholey new baseline as well as will notify you via terminal output if it found something AND log it in the Syslog. 

ARCHITECTUE:
Currently this script is confirmed working on Ubunutu 18.04.1 LTS, however it SHOULD work on ANY Unix system provided that /var/log/syslog is the path that your syslog lives at.

CAVEATS: 
Because of the nature of what it is doing ( a full dirwalk as well as writing to the Syslog) you are going to want to make sure that this script is run as root.


CAVEATS#2 && DIFFERENCES:
The PYTHON and BASH implementation function slightly differently. I had created the BASH version first and didn't feel like having it accept arguments. The BASH version can be run by the user, or periodically using CRON jobs. The BASH version will ALSO the zenity binary to create a popup when it runs and finds something. The PYTHON version will just log and spit something out to the console.

SYNTAX:
#PYTHON
python3.6 hiddenDirCheck.py [ < -l | --lastscan > || < -b | --basescan > || < -n | --newbase > ]

#BASH
DirCheck.sh 
