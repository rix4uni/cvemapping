CFLAGS=-Wall -O2 -std=gnu11 -D=_GNU_SOURCE

all: gen-core cve-2021-3864

gen-core: gen-core.o
	$(CC) $(LDFLAGS) -o $@ $?

cve-2021-3864: cve-2021-3864.o
	$(CC) $(LDFLAGS) -o $@ $?

clean:
	rm -f *.o

distclean: clean
	rm -f gen-core cve-2021-3864

.PHONY: clean distclean
