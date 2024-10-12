# CVE-2024-34313
[![Product](https://img.shields.io/badge/product-Virtual%20Programming%20Lab%20for%20Moodle%20Jail%20System%20%3C4.0.3-orange?style=for-the-badge&logo=GitHub)](https://github.com/jcrodriguez-dis/vpl-jail-system)
[![CWE](https://img.shields.io/badge/CWE-22-%23f0f0f0?style=for-the-badge&logo=OWASP)](https://cwe.mitre.org/data/definitions/22.html)
[![CWE](https://img.shields.io/badge/CWE-284-%23f0f0f0?style=for-the-badge&logo=OWASP)](https://cwe.mitre.org/data/definitions/284.html)

Description
---
[VPL Jail System](https://vpl.dis.ulpgc.es/) **up to v4.0.2** was discovered to contain a **Path Traversal** vulnerability allowing arbitrary file overrides and thereby privilege escalation to root user.

This vulnerability can be chained with [CVE-2024-34312](https://github.com/vincentscode/CVE-2024-34312) to take over a Moodle instance remotely without any prior authentication required.

Additional Details
---
The jail server is a C++ server that runs untrusted code in a sandboxed environment as an unprivileged user. The server listens for incoming connections on a specified port and spawns a new process for each connection.
The commandUpdate function in `jail.cpp` receives a map of files and their contents from the client.
`ProcessMonitor::writeFile` is called with the name of the file and its contents and simply concatenates the jail user's home directory with the file name to get the full path.
The file is then written to the filesystem using `Util::writeFile`.
This allows an attacker to write arbitrary files to the filesystem through path traversal.

Exploitation
---
This vulnerability can be used by an attacker to overwrite `/etc/ld.so.preload` with the path to a shared object file that will be loaded by every dynamically linked executable on the system as explained [here](https://book.hacktricks.xyz/linux-hardening/privilege-escalation/write-to-root). This shared object file can then be used to execute arbitrary code as root such as spawning a reverse shell. To make the exploit easier, the shared object file is also loaded whenever a setuid binary is executed and the request to the server can include a script that will try to execute a setuid binary such as sudo, ensuring that the shared object file is loaded immediately.

In the default configuration of the jail system, the attacker does not need any authentication.

An example payload to write "hello-world.txt" to the root of the system would be:
```json
{
    "method": "request",
    "params": {
        "filestodelete": [],
        "files": {
            "../../../hello-world.txt": "Hello, world!"
        },
        "fileencoding": {
            "../../../hello-world.txt": 0
        },
        "adminticket": "82350372182271",
        "pluginversion": 2021061600,
    },
    "id": "3-32354-684945600",
}
```
The adminticket can be easily obtained by sending an unauthenticated request to the jail system. Despite its name, it is just a form of a session token. Base64-encoded binary files can be uploaded by setting the fileencoding to 1.

The vulnerable code snippet is listed below.
```cpp
bool Jail::commandUpdate(string adminticket, RPC &rpc){
	processMonitor pm(adminticket);
	try {
		mapstruct files = rpc.getFiles();
		Logger::log(LOG_INFO,"parse files %lu", (long unsigned int)files.size());
		mapstruct fileencoding = rpc.getFileEncoding();
		//Save files to execution dir and options, decode data if needed
		for(mapstruct::iterator i = files.begin(); i != files.end(); i++){
			string name = i->first;
			string data = i->second->getString();
			if ( fileencoding.find(name) != fileencoding.end()
					&& fileencoding[name]->getInt() == 1 ) {
				Logger::log(LOG_INFO, "Decoding file %s from b64", name.c_str());
				data = Base64::decode(data);
				if ( name.length() > 4 && name.substr(name.length() - 4, 4) == ".b64") {
					name = name.substr(0, name.length() - 4);
				}
			}
			Logger::log(LOG_INFO, "Write file %s data size %lu", name.c_str(), (long unsigned int)data.size());
			pm.writeFile(name, data);
		}
		return true;
	}
	catch(...){
        // ...
	}
	return false;
}

void processMonitor::writeFile(string name, const string &data) {
	string homePath = getHomePath();
	string fullName = homePath + "/" + name;
	bool isScript = name.size()>4 && name.substr(name.size()-3) == ".sh";
	if (isScript) { //Endline converted to linux
		string newdata;
		for (size_t i = 0; i < data.size(); i++) {
			if (data[i] != '\r') {
				newdata += data[i];
			} else {
				char p = ' ', n = ' ';
				if (i > 0) p = data[i-1];
				if (i + 1 < data.size()) n = data[i + 1];
				if (p != '\n' && n != '\n') newdata += '\n';
			}
		}
		Util::writeFile(fullName, newdata, getPrisonerID(), homePath.size() + 1);
	}else{
		Util::writeFile(fullName, data, getPrisonerID(), homePath.size() + 1);
	}
}

static void Util::writeFile(string name, const string &data,uid_t user = 0,size_t pos = 0){
    FILE *fd=fopen(name.c_str(),"wb");
    if (fd == NULL) {
        string dir = getDir(name);
        Logger::log(LOG_DEBUG,"path '%s' dir '%s'",name.c_str(), dir.c_str());
        if (dir.size())
            createDir(dir,user,pos);
        fd = fopen(name.c_str(),"wb");
        if (fd == NULL)
            throw HttpException(internalServerErrorCode
                    ,"I can't write file");
    }
    if (data.size() > 0 && fwrite(data.data(), data.size(), 1, fd) != 1) {
        fclose(fd);
        throw HttpException(internalServerErrorCode
                ,"I can't write to file");
    }
    fclose(fd);
    if (lchown(name.c_str(),user,user))
        Logger::log(LOG_ERR, "Can't change file owner %m");
    bool isScript = name.size() > 4 && name.substr(name.size() - 3) == ".sh";
    if (chmod(name.c_str(), isScript ? 0700 : 0600))
        Logger::log(LOG_ERR, "Can't change file perm %m");
}
```


References
---
* **CVE Record**: https://www.cve.org/CVERecord?id=CVE-2024-34313
* **Vendor URL**: https://vpl.dis.ulpgc.es/
* **Fixed Release**: https://github.com/jcrodriguez-dis/vpl-jail-system/releases/tag/V4.0.3
* **CWE**: https://cwe.mitre.org/data/definitions/22.html, https://cwe.mitre.org/data/definitions/284.html
