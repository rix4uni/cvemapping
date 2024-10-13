LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_SRC_FILES := main.c
LOCAL_MODULE    := main
LOCAL_LDFLAGS   += -static

include $(BUILD_EXECUTABLE)
