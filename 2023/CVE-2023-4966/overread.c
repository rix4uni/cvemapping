/*
 * overread.c - A program to demonstrate buffer overread (e.g. CVE-2023-4966)
 *
 * NB: Depending on your compiler and the size of the buffers used here, malloc
 * might introduce page-alignment padding which could break the demonstration.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PAYLOAD_BUFFER_SIZE 0x200
#define REQUEST_BUFFER_SIZE 0x200
#define LONG_STR_LENGTH 0x100
#define LINE_LENGTH 0x40

#define INVERSE "\x1B[7m"
#define RED "\x1B[31m"
#define GRAY "\x1B[90m"
#define NORMAL "\x1B[0m"

// Function to print memory in hex dump format, flagging overread memory
void dump_memory(int payload_size, int request_size, char *memory, int max_bytes)
{
	int safe_buffer_size = payload_size + request_size;

	for (int i = 0; i < max_bytes; ++i)
	{
		if (i % LINE_LENGTH == 0)
		{
			printf("%s%04x:%s ", GRAY, i, NORMAL);
		}

		char ch = (i < safe_buffer_size) ? memory[i] : -1;

		if (ch < 0)
		{
			printf("%s\u25b2%s", RED, NORMAL);
		}
		else
		{
			printf((i >= payload_size) ? RED : "");
			(ch < 32 || ch > 127) ? printf("%s%c", INVERSE, ch & 0x7F | 0x40) : putchar(ch);
			printf(NORMAL);
		}

		if ((i + 1) % LINE_LENGTH == 0)
		{
			puts("");
		}
	}
	puts("\n");
}

int main()
{
	// Sensitive API response template
	const char api_response[] =
		"{"
		"\"issuer\": \"https://%.*s\", "
		"\"authorization_endpoint\": \"https://%.*s\", "
		"\"token_endpoint\": \"https://%.*s/oauth/idp/token\", "
		"\"jwks_uri\":  \"https://%.*s/oauth/idp/certs\", "
		"}";

	// A long string to simulate data
	char long_string[LONG_STR_LENGTH];

	// Sample sensitive API endpoints
	const char *api_endpoints[] = {
		"password",
		"nuclear-code",
		"ssn",
		"financials",
		"private-key"};

	// A sensitive HTTP API request with a Set-Cookie header
	const char sample_request[] =
		"GET /%s HTTP/1.1\r\n"
		"Host: example.com\r\n"
		"Set-Cookie: secret_token=SUPERSECRET%0d\r\n"
		"\r\n";

	// Memory objects for payload and requests
	char *payload = malloc(PAYLOAD_BUFFER_SIZE);
	char *requests = malloc(REQUEST_BUFFER_SIZE);

	if (payload == NULL || requests == NULL)
	{
		fprintf(stderr, "Memory allocation failed.\n");
		return 1;
	}

	// Build a long string
	memset(long_string, 'a', LONG_STR_LENGTH - 1);
	long_string[LONG_STR_LENGTH - 1] = '\0';

	// Fill up the HTTP requests in the simulated "memory area" first
	size_t endpoint_count = sizeof(api_endpoints) / sizeof(api_endpoints[0]);
	char temp_request[sizeof(sample_request) + 128];

	for (int i = 0, secret = 0; i < REQUEST_BUFFER_SIZE;)
	{
		snprintf(temp_request, sizeof(temp_request), sample_request, api_endpoints[secret], secret);
		int t = strlen(temp_request);
		int p = t + i;
		if (p >= REQUEST_BUFFER_SIZE)
		{
			temp_request[t - (p - REQUEST_BUFFER_SIZE)] = '\0';
		}
		strcpy(&requests[i], temp_request);
		i += t;
		if (i < REQUEST_BUFFER_SIZE)
		{
			requests[i++] = '\0';
		}
		if (++secret % endpoint_count == 0)
		{
			secret = 0;
		}
	}

	// Write into the payload buffer
	int result = snprintf(payload, PAYLOAD_BUFFER_SIZE,
						  api_response,
						  LONG_STR_LENGTH, long_string,
						  LONG_STR_LENGTH, long_string,
						  LONG_STR_LENGTH, long_string,
						  LONG_STR_LENGTH, long_string);

	// Print information about the payload buffer
	printf("\nThe payload buffer size is %d (0x%04x)\n", PAYLOAD_BUFFER_SIZE, PAYLOAD_BUFFER_SIZE);
	printf("But the result from snprintf is %d (0x%04x)\n", result, result);

	// Print the contents of the "memory" buffer
	printf("\nMemory dump of the payload buffer %swith overread shown in red%s.\n", RED, NORMAL);
	printf("Unsafe memory shown as %s\u25b2%s and accessing it may cause a segfault!\n\n", RED, NORMAL);

	dump_memory(PAYLOAD_BUFFER_SIZE, REQUEST_BUFFER_SIZE, payload, result);

	// Free allocated memory
	free(payload);
	free(requests);

	return 0;
}

/* Expected output:

The payload buffer size is 512 (0x0200)
But the result from snprintf is 1169 (0x0491)

Memory dump of the payload buffer with overread shown in red.
Unsafe memory shown as ▲ and accessing it may cause a segfault!

0000: {"issuer": "https://aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
0040: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
0080: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
00c0: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
0100: aaaaaaaaaaaaaaaaaaa", "authorization_endpoint": "https://aaaaaaa
0140: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
0180: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
01c0: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@
0200: GET /password HTTP/1.1MJHost: example.comMJSet-Cookie: secret_to
0240: ken=SUPERSECRET0MJMJ@GET /nuclear-code HTTP/1.1MJHost: example.c
0280: omMJSet-Cookie: secret_token=SUPERSECRET1MJMJ@GET /ssn HTTP/1.1M
02c0: JHost: example.comMJSet-Cookie: secret_token=SUPERSECRET2MJMJ@GE
0300: T /financials HTTP/1.1MJHost: example.comMJSet-Cookie: secret_to
0340: ken=SUPERSECRET3MJMJ@GET /private-key HTTP/1.1MJHost: example.co
0380: mMJSet-Cookie: secret_token=SUPERSECRET4MJMJ@GET /password HTTP/
03c0: 1.1MJHost: example.comMJSet-Cookie: secret_token=SUPERSECRET0MJM
0400: ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
0440: ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
0480: ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
*/
