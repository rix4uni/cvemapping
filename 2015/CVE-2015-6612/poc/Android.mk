LOCAL_PATH:= $(call my-dir)
include $(CLEAR_VARS)

LOCAL_SRC_FILES:= \
	service.cpp \

LOCAL_C_INCLUDES += external/stlport/stlport/ \
	bionic \
	bionic/libstdc++/include \
	frameworks/av/include/ndk \
	frameworks/av/include/media/stagefright/foundation/ \
	frameworks/av/include/media/stagefright/ \
LOCAL_SHARED_LIBRARIES += libutils libbinder libmedia libcutils libgui libmediandk libstagefright libstagefright_foundation
#LOCAL_STATIC_LIBRARIES += libmediandk
LOCAL_LDLIBS += -lmediandk -lutils -lbinder -lmedia -lstagefright -lstagefright_foundation

ifeq ($(TARGET_OS),linux)
	LOCAL_CFLAGS += -DXP_UNIX
	#LOCAL_SHARED_LIBRARIES += librt
endif

LOCAL_CFLAGS += -O0
CFLAGS += -S

LOCAL_MODULE:= servicefuzz

include $(BUILD_EXECUTABLE)
