/*
** Tool to deny system-wide execution of mysecureshell (http://mysecureshell.sourceforge.net/)
**
** Copyright (C) 2013 Sebastian Pipping <sebastian@pipping.org>
** Licensed under GPL v3 or later
*/
#define _XOPEN_SOURCE

#include <sys/types.h>
#include <assert.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>


/* BEGIN INTERFACE (mysecureshell 1.31) */

#define SFTPWHO_MAXCLIENT    128

#define SFTPWHO_EMPTY        0
#define SFTPWHO_IDLE         1
#define SFTPWHO_GET          2
#define SFTPWHO_PUT          3
#define SFTPWHO_STATUS_MASK  0xff

static char *_shmfile  = "/dev/null";
static int _shmkey     = 0x0787;

typedef struct s_sftpglobal {
	u_int32_t download_max;
	u_int32_t upload_max;
	u_int32_t download_by_client;
	u_int32_t upload_by_client;
} t_sftpglobal;

typedef struct s_sftpwho {
	char user[30];
	char ip[30];
	char path[200];
	char file[200];
	char home[196];

	u_int32_t status;
	u_int32_t pid;
	u_int16_t mode;

	u_int16_t download_pos;
	u_int32_t download_current;
	u_int32_t download_total;
	u_int32_t download_max;
	u_int32_t upload_current;
	u_int32_t upload_total;
	u_int32_t upload_max;

	u_int32_t time_maxidle;
	u_int32_t time_maxlife;
	u_int32_t time_idle;
	u_int32_t time_total;
	u_int32_t time_begin;
	u_int32_t time_transf;
} t_sftpwho;

typedef struct s_shm {
	t_sftpglobal global;
	t_sftpwho who[SFTPWHO_MAXCLIENT];
} t_shm;

/* END INTERFACE */


#define SEGMENTS_TO_TRY  3
#define MAGIC_PID        ((u_int32_t)-1)
#define BLOCKED_STATUS   SFTPWHO_PUT
#define MAXIMUM_FUTURE   ((u_int32_t)-1)

#define CHAR_BLOCKED  '/'
#define CHAR_CLIENT   'C'
#define CHAR_EMPTY    '.'


typedef enum _task_t {
	TASK_BLOCK,
	TASK_UNBLOCK,
	TASK_SHOW
} task_t;


static void print_status(u_int32_t status, u_int32_t pid) {
	char char_to_print;
	switch (status) {
	case SFTPWHO_EMPTY:
		char_to_print = CHAR_EMPTY;
		break;
	case BLOCKED_STATUS:
		if (pid == MAGIC_PID) {
			char_to_print = CHAR_BLOCKED;
		} else {
			char_to_print = CHAR_CLIENT;
		}
		break;
	default:
		char_to_print = CHAR_CLIENT;
		break;
	}

	fprintf(stdout, "%c", char_to_print);
}


static void process(t_sftpwho * who, task_t task) {
	size_t i = 0;
	for (; i < SFTPWHO_MAXCLIENT; i++) {
		if ((i > 0) && (i % 64 == 0)) {
			fprintf(stdout, "\n");
		}

		switch (task) {
		case TASK_BLOCK:
			if (who[i].status == SFTPWHO_EMPTY) {
				/* mark as occupied */
				who[i].status = BLOCKED_STATUS;

				/* make us recognize it later */
				who[i].pid = MAGIC_PID;

				/* exclude from clean up procedure
				 * by making <time_begin + time_total + 10> equal 2^32-1 seconds
				 * so that it is larger than any current system time */
				who[i].time_begin = ((u_int32_t)-1) - 10;
				who[i].time_total = 0;
			}
			break;
		case TASK_UNBLOCK:
			if ((who[i].status == BLOCKED_STATUS)
					&& (who[i].pid == MAGIC_PID)) {
				who[i].pid = 0;
				who[i].time_begin = 0;
				who[i].time_total = 0;

				who[i].status = SFTPWHO_EMPTY;
			}
			break;
		default:
			break;
		}

		print_status(who[i].status, who[i].pid);
	}
	fprintf(stdout, "\n");
}


static int usage(int argc, char ** argv) {
	(void)argc;
	fprintf(stderr, "USAGE:\n  %s (block|unblock|show)\n", argv[0]);
	return EXIT_FAILURE;
}


static void legend() {
	fprintf(stdout, "LEGEND\n");
	fprintf(stdout, "  %c = used by a client\n", CHAR_CLIENT);
	fprintf(stdout, "  %c = blocked\n", CHAR_BLOCKED);
	fprintf(stdout, "  %c = unused\n", CHAR_EMPTY);
	fprintf(stdout, "\n");
}


int main(int argc, char ** argv) {
	if (argc != 2) {
		return usage(argc, argv);
	}
	assert(argc == 2);

	task_t task = TASK_SHOW;
	if (strcmp(argv[1], "block") == 0) {
		task = TASK_BLOCK;
	} else if (strcmp(argv[1], "unblock") == 0) {
		task = TASK_UNBLOCK;
	} else if (strcmp(argv[1], "show") == 0) {
	} else {
		return usage(argc, argv);
	}

	legend();

	int project_id_offset = 0;
	for (; project_id_offset < SEGMENTS_TO_TRY; project_id_offset++) {
		fprintf(stdout, "SEGMENT %d\n", project_id_offset + 1);
		const key_t segment_key = ftok(_shmfile, _shmkey + project_id_offset);
		assert(segment_key != 0);

		const int segment_id = shmget(segment_key, sizeof(t_shm), IPC_CREAT | 0666);
		assert(segment_id != -1);

		void * const segment_address = shmat(segment_id, 0, 0);
		assert(segment_address != (void *)-1);

		t_sftpwho * const who = ((t_shm *)segment_address)->who;
		process(who, task);

		const int detach_res = shmdt(segment_address);
		assert(detach_res != -1);

		if (project_id_offset < SEGMENTS_TO_TRY - 1) {
			fprintf(stdout, "\n");
		}
	}

	return EXIT_SUCCESS;
}
