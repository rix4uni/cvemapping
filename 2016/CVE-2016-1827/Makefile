TARGET = flow_divert-heap-overflow

all: $(TARGET)

CFLAGS = -O3 -Wall -Werror -Wpedantic

$(TARGET): $(TARGET).c
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f -- $(TARGET)
