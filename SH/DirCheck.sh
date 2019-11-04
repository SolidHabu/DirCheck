#!/bin/bash
#A script that can be run in a cron job to check hidden directories and log new changes... like my own homebrewed file/directory watcher.
PWD=$(pwd)
OLD=$(ls $PWD | egrep -i "oldCheck.txt")
BASE=$(ls $PWD | egrep -i "baseCheck.txt")

if [ -f "$PWD/newCheck*.txt" ]
#If newcheck.txt exists, move it to oldCheck.txt to make it results of 'last' run.
then
        echo "NOTIFY: Moving newCheck to oldCheck.txt"
        mv newCheck.txt oldCheck.txt
fi
if [ ! -f "$PWD/$OLD" ]
#First run... create your oldCheck.txt file as well as baseCheck.txt (Use as baseline..)
then
        find / -type d -user root -iname ".*" -exec ls -d '{}' \; 2>/dev/null >$PWD/newCheck.txt
        cp newCheck* baseCheck.txt
        cp newCheck* oldCheck.txt
        rm -f newCheck*
        echo "NOTIFY: First run of hiddenDirCheck complete...run again to check for new hidden directories!"
else
#Second run...create newCheck.txt and see if it is different from oldcheck.txt.
        find / -type d -user root -iname ".*" -exec ls -d '{}' \; 2>/dev/null >$PWD/newCheck.txt
        NEW=$(ls $PWD | egrep -i "newCheck")
        if [ "$(diff $OLD $NEW | egrep -i ">")" ]
        #Action if new directories detected
        then
                zenity --warning --title="HIDDENDIRCHECK" --no-wrap --text="WARNING: New hidden directories found! Check syslog!"
                echo -e "WARNING: Check out the following directories -\n\n$(diff $OLD $NEW | egrep -i ">" | sed -e "s,>,,g")"
                for DIR in $(diff $OLD $NEW | egrep -i ">" | sed -e "s,>,,g") 
                do 
                        logger -p user.warning "HIDDENDIRCHECK: New directory detected!!! - $DIR"
                done 
        else
        #Action if no new directory detected
                echo "NOTIFY: Second run of hiddenDirCheck run complete... no new directories!" 
        fi
fi
