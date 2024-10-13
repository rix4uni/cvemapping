# CVE-2017-6206

The DGS-1510 Websmart switch series firmware has been found to have security vulneratiblies. The vulnerabilities include unauthenticated command bypass and unauthenticated information disclosure.

exploit.sh contains both PoC code and it will create a remote user at specified D-Link Enterprise Switch Without Authentication 

vamin$ sh exploit.sh "1.1.1.1"


 ####################################################################
 # exploit.sh 				                            #
 # D-link DGS Authentication Bypass  0-day 	                    #
 # By  : Varang Amin & Aditya Sood                                  #
 #####################################################################

Steps


      1. Collect The User Info From DGS Vulnerable Switch
      2. Add a user name dlinktest into DGS swith
      3. Collect The User Info & verify the new dlinktest  user added with Admin Access

