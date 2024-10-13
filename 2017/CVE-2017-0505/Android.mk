LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := cve-2017-0505

LOCAL_SRC_FILES := \
    cve-2017-0505.c

include $(BUILD_EXECUTABLE)

$(call import-add-path, $(LOCAL_PATH))