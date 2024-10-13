# Copyright (C) 2016 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE    := CVE-2017-0564
LOCAL_SRC_FILES := poc.c
LOCAL_MULTILIB := both
LOCAL_MODULE_STEM_32 := $(LOCAL_MODULE)32
LOCAL_MODULE_STEM_64 := $(LOCAL_MODULE)64

# Tag this module as a cts test artifact
LOCAL_COMPATIBILITY_SUITE := cts vts general-tests
LOCAL_CTS_TEST_PACKAGE := android.security.cts

LOCAL_ARM_MODE := arm
LOCAL_CFLAGS += -Wall -Werror -W -g -O2 -Wimplicit -D_FORTIFY_SOURCE=2 -D__linux__ -Wdeclaration-after-statement
LOCAL_CFLAGS += -Wformat=2 -Winit-self -Wnested-externs -Wpacked -Wshadow -Wswitch-enum -Wundef
LOCAL_CFLAGS += -Wwrite-strings -Wno-format-nonliteral -Wstrict-prototypes -Wno-shadow
LOCAL_CFLAGS += -Iinclude -fPIE
LOCAL_LDFLAGS += -fPIE -pie
LDFLAGS += -rdynamic
include $(BUILD_CTS_EXECUTABLE)
