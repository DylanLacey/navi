#!/usr/bin/python

import time, threading
import subprocess
import re
import httplib, urllib
import sys

def send_ping_to_server(domain):
	params = create_post_params(check_ping(domain))
	print(params)
	connection = httplib.HTTPSConnection('brasskittens.herokuapp.com')
	request = connection.request('POST', '/stat/ping', params)
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
	print("Checking again for " + domain)
	# ping_results = subprocess.Popen(['ping', '-c1', domain], stdout=subprocess.PIPE).communicate()[0].decode()
	ping_results = subprocess.Popen(['mtr', domain], stdout=subprocess.PIPE).communicate()[0].decode()

	print(ping_results)
	# Just find the results
	result_lines = ping_results.split('\n')
	useful_line = result_lines[4]

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