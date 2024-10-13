LOCAL_PATH      := $(call my-dir)

include $(CLEAR_VARS)
LOCAL_CFLAGS    :=
LOCAL_LDLIBS    +=
LOCAL_LDFLAGS   := -static #-llog
LOCAL_MODULE    := main
LOCAL_SRC_FILES := main.cpp
LOCAL_STATIC_LIBRARIES :=
include $(BUILD_EXECUTABLE)