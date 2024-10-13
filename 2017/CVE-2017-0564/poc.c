/*
 * Copyright (C) 2017 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#define _GNU_SOURCE

#include <pthread.h>
#include <stdio.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <sys/time.h>
#include <sys/mman.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <errno.h>

// Include a fixed version of the ion.h file because it changes per kernel.
// This test is going to be extremely brittle due to it's dependency on
// a structure that is going to change with different kernels.
#include "kernel-headers/linux/ion.h"

#define ION_HEAP(bit) (1 << (bit))

enum ion_heap_ids {
    INVALID_HEAP_ID = -1,
    ION_CP_MM_HEAP_ID = 8,
    ION_SECURE_HEAP_ID = 9,
    ION_SECURE_DISPLAY_HEAP_ID = 10,
    ION_CP_MFC_HEAP_ID = 12,
    ION_CP_WB_HEAP_ID = 16, /* 8660 only */
    ION_CAMERA_HEAP_ID = 20, /* 8660 only */
    ION_SYSTEM_CONTIG_HEAP_ID = 21,
    ION_ADSP_HEAP_ID = 22,
    ION_PIL1_HEAP_ID = 23, /* Currently used for other PIL images */
    ION_SF_HEAP_ID = 24,
    ION_SYSTEM_HEAP_ID = 25,
    ION_PIL2_HEAP_ID = 26, /* Currently used for modem firmware images */
    ION_QSECOM_HEAP_ID = 27,
    ION_AUDIO_HEAP_ID = 28,
    ION_MM_FIRMWARE_HEAP_ID = 29,
    ION_HEAP_ID_RESERVED = 31 /** Bit reserved for ION_FLAG_SECURE flag */
};

static unsigned int ion_type[] = {
    ION_HEAP(ION_CP_MM_HEAP_ID),
    ION_HEAP(ION_CP_MFC_HEAP_ID),
    ION_HEAP(ION_SYSTEM_CONTIG_HEAP_ID),
    ION_HEAP(ION_ADSP_HEAP_ID ),
    ION_HEAP(ION_SF_HEAP_ID),
    ION_HEAP(ION_SYSTEM_HEAP_ID),
    ION_HEAP(ION_QSECOM_HEAP_ID),
    ION_HEAP(ION_AUDIO_HEAP_ID),
};

#define NEW_ION
int ion_alloc(int fd, int len, int *hdl, unsigned int ion_type)
{
    int ret;
    struct ion_allocation_data req = {
        .len = len,
#ifdef NEW_ION
        .heap_id_mask = ion_type,
        //.flags = ION_SECURE | ION_FORCE_CONTIGUOUS,
        //.flags = (1 << 0),
        .flags = 0x0,
#else
        .flags = ION_SECURE | ION_FORCE_CONTIGUOUS | ION_HEAP(ION_CP_MM_HEAP_ID),
#endif
        .align = len,
    };

    ret = ioctl(fd, ION_IOC_ALLOC, &req);
    if (ret) {
        return ret;
    }

    *hdl = req.handle;

    return 0;
}

int ion_free(int fd, int hdl)
{
    int ret;
    struct ion_handle_data req = {
        .handle = hdl,
    };

    ret = ioctl(fd, ION_IOC_FREE, &req);
    if (ret) {
        return ret;
    }

    return 0;
}

int ion_map(int fd, int hdl)
{
    int ret;
    struct ion_fd_data req = {
        .handle = hdl,
    };

    ret = ioctl(fd, ION_IOC_MAP, &req);
    if (ret) {
        return ret;
   }

   return req.fd;
}

int ion_fd;
int ion_handle;
int status[2];
int cmd = 0;

void *threadForIonFree01()
{
    status[0] = 1;

    while (cmd == 0) {
        usleep(10);
    }
    if (cmd == -1)
        goto failed;

    usleep(50);
    ion_free(ion_fd, ion_handle);

failed:
    status[0] = 2;
    return NULL;
}


void *threadForIonFree02()
{
    status[1] = 1;

    while (cmd == 0) {
        usleep(10);
    }
    if(cmd == -1)
        goto failed;

    usleep(50);
    ion_free(ion_fd, ion_handle);

failed:
    status[1] = 2;
    return NULL;
}

int main()
{
    int ret, count;
    pthread_t tid_free[2];

    count = 0;
retry:
    status[0] = 0;
    status[1] = 0;
    cmd = 0;
    ion_fd = open("/dev/ion", O_RDONLY| O_SYNC, 0);
    if (ion_fd < 0) {
	return -1;
    }

    size_t i;
    for (i=0; i < sizeof(ion_type)/sizeof(ion_type[0]); i++) {
        ret = ion_alloc(ion_fd, 0x1000, &ion_handle, ion_type[i]);
        if (ret == 0) {
            break;
        }
    }

    if (i == sizeof(ion_type)/sizeof(ion_type[0])) {
        goto failed;
    }

    ret = pthread_create(&tid_free[0], NULL, threadForIonFree01, NULL);
    if (ret != 0) {
        goto failed;
    }

    ret = pthread_create(&tid_free[1], NULL, threadForIonFree02, NULL);
    if (ret != 0) {
        cmd = -1;
        goto failed;
    }

    while (status[0] != 1 || status[1] != 1) {
        usleep(50);
    }

    cmd = 1;
    ret = ion_map(ion_fd, ion_handle);

    while (status[0] != 2 || status[1] != 2) {
        usleep(50);
    }

failed:
    ion_free(ion_fd,ion_handle);
    close(ion_fd);
    goto retry;

    return 0;
}

