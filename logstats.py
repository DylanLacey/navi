#!/usr/bin/python

import time, threading
import subprocess
import re
import httplib, urllib

def send_memory_to_server():
	params = create_post_params(check_memory())
	connection = httplib.HTTPSConnection('brasskittens.herokuapp.com')
	request = connection.request('POST', '/stat/memory', params)
	print(connection.getresponse().read())

def create_post_params(memory):
	t = time.ctime()
	active = memory["active"]
	free = memory["free"]
	total = memory["total"]

	return urllib.urlencode({'active': active, 'free': free, 'total': total, 'time': t})

def log_memory_repeatedly():
	send_memory_to_server()
	threading.Timer(1, log_memory_repeatedly).start()

def check_memory():
	ps = subprocess.Popen(['ps', '-caxm', '-orss,comm'], stdout=subprocess.PIPE).communicate()[0].decode()
	vm = subprocess.Popen(['vm_stat'], stdout=subprocess.PIPE).communicate()[0].decode()
	
	# Iterate processes
	processLines = ps.split('\n')
	sep = re.compile('[\s]+')
	rssTotal = 0 # kB
	for row in range(1,len(processLines)):
	    rowText = processLines[row].strip()
	    rowElements = sep.split(rowText)
	    try:
	        rss = float(rowElements[0]) * 1024
	    except:
	        rss = 0 # ignore...
	    rssTotal += rss

	# Process vm_stat
	vmLines = vm.split('\n')
	sep = re.compile(':[\s]+')
	vmStats = {}
	for row in range(1,len(vmLines)-2):
	    rowText = vmLines[row].strip()
	    rowElements = sep.split(rowText)
	    vmStats[(rowElements[0])] = int(rowElements[1].strip('\.')) * 4096

	return {'active': (vmStats["Pages active"]/1024/1024), 'free': (vmStats["Pages free"]/1024/1024), 'total': ( rssTotal/1024/1024 )}
	#('Active:\t\t%d MB, Free:\t\t%d MB, Total:\t%.3f MB' % ((vmStats["Pages active"]/1024/1024),(vmStats["Pages free"]/1024/1024),( rssTotal/1024/1024 )))

log_memory_repeatedly()
#log_memory_repeatedly()