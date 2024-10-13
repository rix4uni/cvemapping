# CVE-2019-17633

## Eclipse Che CSRF leading to RCE

This bug allows a remote website to create and start an arbitrary docker container on machines running Che before versions 7.3.0 and 7.4.1 when a user visits a webpage. 

## Vulnerability

This is a CSRF bug that allows a remote website to create and start a docker container on the machine of anybody running Eclipse Che in standalone mode. Many parameters under the attacker's control allow a precise level of control. Some developers make use of Che in standalone mode as a convenient way to manage their local docker containers.  

This was possible because Che had CORS enabled by default. The issues with this are fairly obvious to people who understand what this means, but essentially Che would respond to requests from any source. Although browsers do their best to make CORS attacks difficult, when the server allows CORS it is possible to create a successful POST request to a locally running Che service from a remote site. 

Essentially, this means that any unauthenticated API method can be called when a computer running Che in standalone mode visits their website. This includes creating and running new Docker/OpenShift containers. 

A simple POC is included with this readme, but a viewing of the JSON posted to the local Che service reveals a number of fairly interesting parameters to be controlled, including which image, what commands to run on start, what servers to start in the container and other pretty interesting characteristics. 

## Exploitation

[![Eclipse Che RCE](https://img.youtube.com/vi/0e3ZFE5W6IM/0.jpg)](https://www.youtube.com/watch?v=0e3ZFE5W6IM)

To exploit this vulnerability, you must target somebody who is running Eclipse Che on their computer. You must get your target to visit a page that you control over HTTP. From there, the XMLHttpRequest does its job and you can go to town. To fully understand how to exploit this vulnerability, you should have a look at the Che source code to learn about the API or simply play with the POC I've placed in this repo. Essentially, you want to create either a container or a command in your newly launched container that gives you the sort of foothold you'd like. You could set up a server of your choosing or simply make the command run at launch download your payload and begin operating from there. This attack lends itself to either opportunistic or targetted attacks. 

For more detailed discussion, have a look at the bug tracked [here](https://bugs.eclipse.org/bugs/show_bug.cgi?id=551596). Most of it is simply repeating this post. 

**To successfully execute this attack, the page must be served from an HTTP(not HTTPS) server.** This is necessary because a local Che server runs over HTTP and popular browsers do not like to mix HTTP and HTTPS content. 


## Mitigation

To fix this issue, the Che team simply disabled CORS by default. This should at least make this sort of attack significantly more difficult in the future. If you're running Che locally to manage your docker images, consider upgrading. 

