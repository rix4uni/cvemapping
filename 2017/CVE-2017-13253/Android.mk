LOCAL_PATH:= $(call my-dir)

include $(CLEAR_VARS)

LOCAL_SRC_FILES := icrypto_overflow.cpp

LOCAL_SHARED_LIBRARIES := libmedia libutils libbinder libmediadrm

LOCAL_CFLAGS += -Wall

LOCAL_MODULE:= icrypto_overflow

include $(BUILD_EXECUTABLE)
