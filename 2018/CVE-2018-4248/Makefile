TARGET = xpc-string-leak

DEBUG      ?= 0
ARCH       ?= x86_64
SDK        ?= macosx
SIGNING_ID ?= -

SYSROOT  := $(shell xcrun --sdk $(SDK) --show-sdk-path)
ifeq ($(SYSROOT),)
$(error Could not find SDK "$(SDK)")
endif
CLANG    := $(shell xcrun --sdk $(SDK) --find clang)
CC       := $(CLANG) -isysroot $(SYSROOT) -arch $(ARCH)
CODESIGN := codesign

CFLAGS  = -O2 -Wall -Werror $(EXTRA_CFLAGS)
LDFLAGS =

ifneq ($(DEBUG),0)
DEFINES += -DDEBUG=$(DEBUG)
CFLAGS += -g
endif

FRAMEWORKS =

SOURCES = xpc-string-leak.c

HEADERS =

all: $(TARGET)

$(TARGET): $(SOURCES) $(HEADERS)
	$(CC) $(CFLAGS) $(LDFLAGS) $(FRAMEWORKS) $(DEFINES) -o $@ $(SOURCES)
	$(CODESIGN) -s '$(SIGNING_ID)' $@

clean:
	rm -f -- $(TARGET)
	rm -rf -- $(TARGET).dSYM
