LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_CFLAGS += -fPIE
LOCAL_LDFLAGS += -fPIE -pie

LOCAL_MODULE := pwn
LOCAL_SRC_FILES := pwn.c

include $(BUILD_EXECUTABLE)