LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_ARM_MODE := arm
LOCAL_CFLAGS := -Wno-overflow
LOCAL_C_INCLUDES := $(LOCAL_PATH)/

LOCAL_MODULE    := vuln
LOCAL_SRC_FILES := vuln.c

include $(BUILD_EXECUTABLE)
