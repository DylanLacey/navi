#!/usr/bin/python

import time, threading
import subprocess
import re
import httplib, urllib
import sys

def send_ping_to_server(domain):
	post_log("Inside of Send Ping to Server")
	params = create_post_params(check_ping(domain))
	print(params)
	connection = httplib.HTTPSConnection('brasskittens.herokuapp.com')
	request = connection.request('POST', '/stat/ping', params)
	print(connection.getresponse().read())

def post_log(message):
	t = time.ctime()
	print(message)
	connection = httplib.HTTPSConnection('brasskittens.herokuapp.com')
	request = connection.request('POST', '/stat/log', urllib.urlencode({'time': t, 'message': message}))
	print(connection.getresponse().read())

def create_post_params(memory):
	t = time.ctime()
	result = memory

	# active = memory["active"]
	# free = memory["free"]
	# total = memory["total"]

	# return urllib.urlencode({'active': active, 'free': free, 'total': total, 'time': t})
	return urllib.urlencode({'time': t, 'result': result})

def log_ping_repeatedly():
	print("Checking ping for " + sys.argv[1])
	send_ping_to_server(sys.argv[1])
	threading.Timer(5, log_ping_repeatedly).start()

def check_ping(domain):
	post_log("Checking again for " + domain)
	sub = subprocess.Popen(['/sbin/ping', '-c1', domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	# sub.wait()
	# return_code = sub.returncode

	# print("Returncode from Subprocess was {}".format(return_code))
	post_log("Process Began")
	subprocess_pipes = sub.communicate()
	stdout = subprocess_pipes[0].decode()
	stderr = subprocess_pipes[1].decode()

	post_log("Any errors?")	
	post_log(stderr)
	# ping_results = subprocess.Popen(['mtr', domain], stdout=subprocess.PIPE).communicate()[0].decode()
	post_log("got results")
	post_log(stdout)
	# Just find the results
	result_lines = stdout.split('\n')
	useful_line = result_lines[4]

	post_log(useful_line)
	return useful_line

# def check_memory():
# 	ps = subprocess.Popen(['ps', '-caxm', '-orss,comm'], stdout=subprocess.PIPE).communicate()[0].decode()
# 	vm = subprocess.Popen(['vm_stat'], stdout=subprocess.PIPE).communicate()[0].decode()
	
# 	# Iterate processes
# 	processLines = ps.split('\n')
# 	sep = re.compile('[\s]+')
# 	rssTotal = 0 # kB
# 	for row in range(1,len(processLines)):
# 	    rowText = processLines[row].strip()
# 	    rowElements = sep.split(rowText)
# 	    try:
# 	        rss = float(rowElements[0]) * 1024
# 	    except:
# 	        rss = 0 # ignore...
# 	    rssTotal += rss

# 	# Process vm_stat
# 	vmLines = vm.split('\n')
# 	sep = re.compile(':[\s]+')
# 	vmStats = {}
# 	for row in range(1,len(vmLines)-2):
# 	    rowText = vmLines[row].strip()
# 	    rowElements = sep.split(rowText)
# 	    vmStats[(rowElements[0])] = int(rowElements[1].strip('\.')) * 4096

# 	return {'active': (vmStats["Pages active"]/1024/1024), 'free': (vmStats["Pages free"]/1024/1024), 'total': ( rssTotal/1024/1024 )}
# 	#('Active:\t\t%d MB, Free:\t\t%d MB, Total:\t%.3f MB' % ((vmStats["Pages active"]/1024/1024),(vmStats["Pages free"]/1024/1024),( rssTotal/1024/1024 )))

log_ping_repeatedly()
#log_memory_repeatedly()