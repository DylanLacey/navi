#!/usr/bin/python

import time, threading
import subprocess
import re
import httplib, urllib
import sys

def send_traceroute_to_server(domain):
	params = create_post_params(check_traceroute(domain))
	connection = httplib.HTTPSConnection('brasskittens.herokuapp.com')
	request = connection.request('POST', '/stat/domain', params)
	print(connection.getresponse().read())

def post_log(message):
	print(message)
	t = time.ctime()
	connection = httplib.HTTPSConnection('brasskittens.herokuapp.com')
	request = connection.request('POST', '/stat/log', urllib.urlencode({'time': t, 'message': message}))
	print(connection.getresponse().read())

def create_post_params(route_data):
	t = time.ctime()
	return urllib.urlencode({'time': t, 'route_data': route_data})

def log_traceroute_repeatedly():
	post_log("Checking ping for " + sys.argv[1])
	send_traceroute_to_server(sys.argv[1])
	threading.Timer(5, log_traceroute_repeatedly).start()

def check_traceroute(domain):
	traceroute_results = subprocess.Popen(['/usr/sbin/traceroute', domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	# sub.wait()
	# return_code = sub.returncode

	# print("Returncode from Subprocess was {}".format(return_code))
	post_log("Process Began")
	subprocess_pipes = traceroute_results.communicate()
	stdout = subprocess_pipes[0].decode()
	stderr = subprocess_pipes[1].decode()

	# post_log("Any errors?")	
	# post_log(stderr)

	# result_lines = stdout.split('\n')
	return stdout

log_traceroute_repeatedly()