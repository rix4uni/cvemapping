# CVE-2016-5983
IBM WebSphere deserialization of untrusted data - IBM WebSphere 7,8,8.5,9

- Link to Original Writeup Source: <https://techblog.mediaservice.net/2016/10/cve-2016-5983-ibm-websphere-deserialization-of-untrusted-data/>

Title:	IBM WebSphere deserialization of untrusted data 

   Application:	IBM WebSphere 7,8,8.5,9

   Description:	The application server deserializes unstrusted data when the 

                WASPostParam cookie is present. This can lead to a DoS via 

                resource exhaustion and potentially remote code execution.

       Authors: Federico Dotta <federico.dotta@mediaservice.net>

                Maurizio Agazzini <inode@mediaservice.net>

 Vendor Status: Fixed (PI62375)

 CVE Candidate: The Common Vulnerabilities and Exposures project has assigned

                the name CVE-2016-5983 to this issue.           

    References: http://lab.mediaservice.net/advisory/2016-02-websphere.txt

                http://lab.mediaservice.net/code/websphere_payload.zip

                http://www-01.ibm.com/support/docview.wss?uid=swg21990060

 

1. Abstract.

 

When using custom form authentication, IBM WebSphere automatically sets the

cookies WASPostParam and WASReqURL when the LtpaToken2 session cookie is

invalid. The data contained in these cookies is used when the user logs in

again to retrieve the last visited page and related parameters.

 

The WASPostParam is a serialized Java object that is deserialized without

checking the object type. This behavior can be exploited to cause a denial of 

service and potentially execute arbitrary code.

 

The objects that can cause the DoS are based on known disclosed payloads

taken from:

 

- https://gist.github.com/coekie/a27cc406fc9f3dc7a70d

 

Currently there is no known chain that allows code execution on IBM WebSphere,

however new chains are discovered every day.

 

2. Example Attack Session.

 

The attack can be reproduced as follows:

 

- create an application with custom form authentication

- after user login, the LtpaToken2 is set by the application server

- make a HTTP GET request that contains the WASPostParam cookie with one of 

  these contents:

 

    * 01_BigString_limited_base64.txt: it's a string object; the server will

      reply in a normal way (object size similar to the next one).

    * 02_SerialDOS_limited_base64.txt: the application server will require

      about 2 minutes to execute the request with 100% CPU usage.

    * 03_BigString_base64.txt it's a string object; the server will

      reply in a normal way (object size similar to the next one).

    * 04_SerialDOS_base64.txt: the application server will require an 

      unknown amount of time to execute the request with 100% CPU usage.

 

3. Affected Platforms.

 

This vulnerability affects the following versions and releases of

IBM WebSphere Application Server and priors versions:

 

 - Liberty 16.0.0.2

 - 9.0.0.1

 - 8.5.5.10

 - 8.0.0.12

 - 7.0.0.41

 

4. Fix.

 

Apply Interim Fix PI62375

http://www-01.ibm.com/support/docview.wss?uid=swg24042712

 

5. Proof Of Concept.
   - See the 4 .txt files...
   - Make and HTTP GET request and set the WAPPostParam cookie equal to the contents of one of the files.

 

6. Timeline

 

20/08/2016 - First communication sent to IBM PSIRT (psirt at us.ibm.com)

22/08/2016 - IBM Response, PSIRT Advisory 6345 assigned to the bug

05/10/2016 - Communication from IBM with fix information (PI62375)

07/10/2016 - Security Advisory released
