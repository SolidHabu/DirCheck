#!/usr/bin/python3

from pathlib import Path
from sys import exit
import argparse
import shutil
import datetime
import difflib 
import re 
import syslog

pwd = Path()
root = Path('/')

lastLog = pwd / 'last.log'
newLog = pwd / 'new.log'
baseLog = pwd / 'base.log'

reg = re.compile('^\\+/.*')

def log(directory):
    syslog.syslog(syslog.LOG_WARNING, f"WARNING: A hidden directory was found at {directory}") 

def scan():
    with newLog.open('w') as f:
        walk = root.glob("**/.*")
        now = datetime.datetime.now()
        dateTime = now.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Log last written to at: {dateTime}\n\n")
        for w in walk:
            f.write(str(w))
            f.write("\n")

def newToLast():
    print(f"[ ] Moving {newLog} to {newLog}")
    if shutil.copy(newLog, lastLog):
        print(f"[+] Moved {newLog} to {lastLog}!")
    else:
        print(f"[-] Something went wrong on the copy of {newLog} to {lastLog}!")
        exit(1)
    print(f"[ ] Removing {newLog}")
    try:
        newLog.unlink()
        print(f"[+] Removal of {newLog} complete!") 
    except:
        print(f"[-] Something went wrong during the removal of {newLog}") 

def diffCheck(comp): 
    with open(comp, 'r') as baseL:
        with open(newLog,'r') as newL:
            diff = difflib.unified_diff(
                baseL.readlines(),
                newL.readlines(),
                fromfile=str(baseLog),
                tofile=str(newLog),
                n=0
            )
            for line in diff:
                m = reg.match(line)
                if m:
                    match = m.group()
                    cleaned = re.sub('^\\+','',match)
                    print(f"[!] Hidden directory found at: {cleaned}")
                    log(cleaned)

def lastScan():
    print("[ ] Running scan!")    
    scan()
    print(f"[+] Scan complete, saved results to {newLog}!")
    print(f"[ ] Comparing {newLog} to {lastLog}!")
    diffCheck(lastLog.resolve())
    print(f"[+] Comparison between {newLog} and {lastLog} complete!")
    newToLast()
    print("[+] Last scan complete!")

def baseScan():
    print("[ ] Running scan!")
    scan()
    print(f"[+] Scan complete, saved results to {newLog}!")
    print(f"[ ] Comparing {newLog} to {baseLog}!")
    diffCheck(baseLog.resolve())
    print(f"[+] Comparison between {newLog} and {baseLog} complete!")
    newToLast()
    print("[+] Base scan complete!")

def newBase():
    if baseLog.exists() or lastLog.exists():
        c = str(input("[!] Files from your previous baseline exist, would you like to remove them and create a newbaseline? y/[N]: ") or "n").lower()
        if c == 'y':
            for f in pwd.iterdir():
                if f.match('*.log'):
                    f.unlink()
            print("[+] Removed files from previous baseline!")
        elif c == 'n':
            print("[+] You chose to not remove files from your previous run, exiting!") 
            exit(0)
        else: 
            print("[-] Sorry that is not a valid choice! Exiting!")
            exit(1)
    print("[ ] Doing scan and creating new baseline!")
    scan(baseLog) 
    print("[+] Created new baseline file!")
    print(f"[ ] Copying {baseLog} to {lastLog} !")
    if shutil.copy(baseLog, lastLog):
        print(f"[+] Copied {baseLog} to {lastLog} !")
    else:
        print(f"[-] Something went wrong on the copy of {baseLog} to {lastLog} !")
        exit(1)
    print("[+] Baseline finished! Please re-run the program with either the -l or -b option!")

def main():
    parser = argparse.ArgumentParser(description="A file watcher which can will look for hidden directories and alert if any new ones are created. Use by first running with the -n argument to create a new 'baseline' file. Then run subsequently using -b to compare the new scan to the baseline or -l to compare to the last ran scan. Both -l and -b will place their results into the last scan log file.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l','--lastscan', help="Compare new scan to last scan", action='store_true', default=False) 
    group.add_argument('-b','--basescan', help="Compare new scan to baseline scan", action='store_true', default=False)
    group.add_argument('-n','--new', help="Remove all files and create a new basline", action='store_true', default=False)
    
    args = parser.parse_args()
    argDict = vars(args)

    last = argDict['lastscan']
    base = argDict['basescan']
    new = argDict['new']
    
    if last:
        print("[ ] Starting last run check!")
        lastScan()
    elif base:
        print("[ ] Starting baseline check!") 
        baseScan()
    elif new:
        print("[ ] Creating a new baseline!") 
        newBase()
    else:
        print("[-] Something unexpected went wrong!")

if __name__ == "__main__":
    main()
