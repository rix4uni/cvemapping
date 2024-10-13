import deviceleaks 
import setArgs
import sys
import time


def main():
    
    getArgs = setArgs.args

    
    startScan = deviceleaks.Scans()
    chkDefPass = deviceleaks.Leaks('http://cisco.com/jnap/core/IsAdminPasswordDefault')
    hitNumber = deviceleaks.hitList


    if getArgs.checkPass and getArgs.file:
        print("Checkpass and file  was selected")
        startScan.file_scan()
        chkDefPass.check_pass()
        if getArgs.save:
            startScan.save_hits()

    elif getArgs.target and getArgs.checkPass:
        startScan.single_scan()
        chkDefPass.check_pass()
        if getArgs.save:
            startScan.save_hits()
    
    elif getArgs.file and getArgs.save:
        startScan.file_scan()
        startScan.save_hits()

    elif getArgs.target:
        print("Starting scan on single target " + startScan.singleIP)
        time.sleep(2)
        startScan.single_scan()
        if getArgs.save:
            startScan.save_hits()

    elif getArgs.file:
        print("Searching for linksys devices from : " + getArgs.file)
        startScan.file_scan()

        print(str(len(hitNumber)) + " Linksys Devices found")


    elif getArgs.checkPass:
        print("only pass arg was given" + '\n' + 
        "Please use either the --file or --target arguement or use -h for help")

    elif getArgs.save:
        print("only save arg was given" + '\n' + 
        "Please use either the --file or --target arguement or use -h for help")

    elif getArgs.port:
        print("only port arg was given" + '\n' + 
        "Please use either the --file or --target arguement or use -h for help")

    elif getArgs.timeout:
        print("only timeout arg was given" + '\n' + 
        "Please use either the --file or --target arguement or use -h for help")

    
if __name__ == "__main__":
    main()
