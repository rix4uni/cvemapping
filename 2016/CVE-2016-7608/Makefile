TARGET = IOFireWireFamily-overflow

all: $(TARGET)

CFLAGS = -O3 -Wall -Werror -Wpedantic

FRAMEWORKS = -framework IOKit

$(TARGET): $(TARGET).c
	$(CC) $(CFLAGS) $(FRAMEWORKS) -o $@ $^

clean:
	rm -f -- $(TARGET)
