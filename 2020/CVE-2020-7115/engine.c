#include <unistd.h>

__attribute__((constructor))
static void init() {
    execl("/bin/sh", "sh", "-c","echo 'arbitrary code'");
}
