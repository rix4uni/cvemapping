# CVE-2024-31989
# CVE-Exploit for Argo CD

This repository contains an exploit for CVE-2024-31989 that targets a Redis instance without a password in Argo CD.

## Description

Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes. This exploit leverages a vulnerability in Argo CD where a Redis instance is deployed without a password.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/vt0x78/CVE-2024-31989.git
   cd CVE-2024-31989
   go build -o <name>
   
or just download the binary in releases.

##### *Usage*
./K8sHijack -key \<path to key name\> -pod \<path to pod manifest to deploy\>

# Reference Article

For a detailed explanation of this exploit and its implications, please refer to my article [CVE-2024-31989](https://medium.com/@vt0x78/redis-aster-uncovering-a-critical-flaw-in-argo-cds-kubernetes-controller-cve-2024-31989-f01ae2a9e18e).
