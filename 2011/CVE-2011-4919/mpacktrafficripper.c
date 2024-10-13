/*
** Copyright (C) 2011  Sebastian Pipping <sebastian@pipping.org>
** Licensed under GPL v3 or later
*/
#define PACKAGE_NAME     "mpack traffic ripper"
#define PACKAGE_VERSION  "2011.12.31.19.27"

#define _GNU_SOURCE

#include <sys/inotify.h>
#include <stdio.h>
#include <assert.h>
#include <limits.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <stdbool.h>
#include <pthread.h>
#include <errno.h>
#include <time.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>

#define BUFFER_LEN  (sizeof(struct inotify_event) + PATH_MAX)
#define BLOCK_SIZE  4096


struct thread_data {
	int min_fd;
	volatile int max_fd;
	const char * mails_outdir;
};


static pthread_mutex_t max_fd_mutex = PTHREAD_MUTEX_INITIALIZER;


static bool has_trailing_slash(const char * dirname) {
	assert(dirname);
	size_t len_dirname = strlen(dirname);
	assert(len_dirname > 0);
	return (dirname[len_dirname - 1] == '/');
}


static char * malloc_concat_dirname_basename(
		const char * dirname, const char * basename) {
	assert(dirname && basename);
	size_t len_dirname = strlen(dirname);
	assert(len_dirname > 0);
	const bool trailing_slash = has_trailing_slash(dirname);
	const size_t len_basename = strlen(basename);
	const size_t len_res = len_dirname + (trailing_slash ? 0 : 1) + len_basename;
	char * const res = malloc(len_res + 1);
	assert(res);
	const int len_copied = snprintf(res, len_res + 1, "%s%s%s",
			dirname, (trailing_slash ? "" : "/"), basename);
	assert(len_copied == (int)len_res);
	return res;
}


void ripp_file(int input_fd, char * buffer, size_t buffer_size, const char * mails_outdir) {
	struct timespec ts;

	const int gettime_res = clock_gettime(CLOCK_REALTIME, &ts);
	if (gettime_res) {
		fprintf(stderr, "[%d]   ERROR: Could not get system time to make file name, error %d.\n", input_fd, errno);
		return;
	}

	char filename[PATH_MAX];

	const bool trailing_slash = has_trailing_slash(mails_outdir);
	const int len_copied = snprintf(filename, PATH_MAX, "%s%smpack-%ld-%ld.eml",
			mails_outdir, trailing_slash ? "" : "/", (long)ts.tv_sec, ts.tv_nsec);
	if ((len_copied < 0) || (len_copied > PATH_MAX - 1)) {
		fprintf(stderr, "[%d]   ERROR: Could not make file name, error %d.\n", input_fd, errno);
		return;
	}

	const int output_fd = open(filename, O_WRONLY | O_CREAT | O_EXCL, 0600);
	if (output_fd == -1) {
		fprintf(stderr, "[%d]   ERROR: Could not open file \"%s\" for writing, error %d.\n",
				input_fd, filename, errno);
	} else {
		unsigned long total_written = 0;
		bool write_error_reported = false;

		for (;;) {
			const int bytes_read = read(input_fd, buffer, buffer_size);
			if (bytes_read == -1) {
				fprintf(stderr, "[%d]   ERROR: Could not read from file descriptor, error %d.\n", input_fd, errno);
				break;
			}

			const int bytes_written = write(output_fd, buffer, bytes_read);
			if (bytes_written < bytes_read) {
				fprintf(stderr, "[%d]   ERROR: Could not write to file \"%s\", error %d.\n",
						input_fd, filename, errno);
				write_error_reported = true;
				break;
			}
			total_written += bytes_written;

			if (bytes_read < (int)buffer_size) {
				/* End of file */
				break;
			}
		}
		close(output_fd);

		if (! write_error_reported)
			printf("[%d]   Ripped, %lu bytes written to \"%s\".\n",
					input_fd, total_written, filename);
	}

	close(input_fd);
}


static void * ripper_thread(void * p) {
	struct thread_data * data = (struct thread_data *)p;

	char buffer[BLOCK_SIZE];

	int input_fd = data->min_fd;
	for (;;) {
		/* Test file descriptor */
		int bytes_read = pread(input_fd, buffer, sizeof(buffer), 0);
		if (bytes_read != -1) {
			ripp_file(input_fd, buffer, sizeof(buffer), data->mails_outdir);
		}

		pthread_mutex_lock(&max_fd_mutex);
		if (input_fd < data->max_fd) {
			input_fd++;
		} else {
			if (data->max_fd > data->min_fd)
				data->max_fd--;
			input_fd = data->min_fd;
		}
		pthread_mutex_unlock(&max_fd_mutex);
		sleep(1);
	}

	return NULL;
}


int main(int argc, char ** argv) {
	printf("Hello from %s version %s.\n"
			"Please use responsibly.  Thanks.\n"
			"\n",
			PACKAGE_NAME, PACKAGE_VERSION);

	if (argc != 2) {
		fprintf(stderr, "USAGE:\n  %s MAILS_OUTDIR\n", argv[0]);
		return 1;
	}

	pthread_t thread;

	const char * mails_outdir = argv[1];

	mkdir(mails_outdir, 0700);

	const int inotify_fd = inotify_init();
	assert(inotify_fd != -1);


	const char * const mpack_tmp_dirs[] = {"/tmp", "/var/tmp"};
	const char * wd_to_dir[30];
	bool at_least_one_watch = false;
	size_t i = 0;
	for (; i < sizeof(mpack_tmp_dirs) / sizeof(char *); i++) {
		const int wd = inotify_add_watch(inotify_fd, mpack_tmp_dirs[i], IN_CLOSE_WRITE);
		if (wd == -1) {
			fprintf(stderr, "ERROR: Could not listening to \"%s\".\n", mpack_tmp_dirs[i]);
			continue;
		}

		assert(wd < (int)(sizeof(wd_to_dir) / sizeof(char *)));
		wd_to_dir[wd] = mpack_tmp_dirs[i];

		at_least_one_watch = true;
		printf("Now listening to \"%s\"...\n", mpack_tmp_dirs[i]);
	}

	if (! at_least_one_watch) {
		return 1;
	}

	char buffer[BUFFER_LEN];

	struct thread_data data;
	data.min_fd = inotify_fd + 1;
	data.mails_outdir = mails_outdir;
	printf("Starting ripper thread...\n\n");
	const int pthread_create_res = pthread_create(&thread, NULL, ripper_thread, (void *)&data);
	assert(pthread_create_res == 0);

	for (;;) {
		const int bytes_read = read(inotify_fd, buffer, BUFFER_LEN);
		if (bytes_read == -1) {
			continue;
		}

		int bytes_processed = 0;
		while (bytes_processed < bytes_read) {
			struct inotify_event * const event = (struct inotify_event *)(buffer + bytes_processed);

			if (! strncmp(event->name, "mpack", sizeof("mpack") - 1)
					&& (strlen(event->name) >= (sizeof("mpack") - 1) + (sizeof("XXXXXX") - 1))) {
				char * const target = malloc_concat_dirname_basename(wd_to_dir[event->wd], event->name);
				assert(target);

				/* Idea is to leave to file open, ripper thread will get to it by himself */
				const int fd = open(target, O_RDONLY);
				if (fd != -1) {
					printf("[%d] Adding file \"%s\" to queue\n", fd, target);

					pthread_mutex_lock(&max_fd_mutex);
					if (fd > data.max_fd) {
						data.max_fd = fd;
					}
					pthread_mutex_unlock(&max_fd_mutex);
				} else {
					fprintf(stderr, "[X] ERROR: Failed to grab file \"%s\", error %d\n", target, errno);
				}

				free(target);
			}

			bytes_processed += sizeof(struct inotify_event) + event->len;
		}
	}

	close(inotify_fd);

	pthread_exit(NULL);

	return 0;
}
