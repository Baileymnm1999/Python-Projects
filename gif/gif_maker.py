import os, time, subprocess, threading, datetime

x = 0
#n = float(raw_input("How many seconds would you like your gif? "))
#n = n*10.0
n = float(raw_input("How many images would you like to take? "))
filename = ""

def capture():
	record = subprocess.call("import -window root -resize 1280x720 '"+filename+".png'", shell=True)
	kill_thread(filename)

def create_thread(thread):
	try:		
		if thread.isAlive():
			thread.do_run = False
			thread.join()
	except AttributeError:
		pass
	thread = threading.Thread(target=capture, args=())
	thread.daemon = True
	thread.start()

def kill_thread(thread):
	if thread.isAlive():
		thread.do_run = False
		thread.join()

while True:
	start_time = datetime.datetime.now().time()
	if x < n:
		filename = str(x)
		record = subprocess.call("import -window root -resize x640 '"+filename+".png'", shell=True)
		x += 1
		print datetime.datetime.now().time()
		#time.sleep(0.1)
	else:
		end_time = datetime.datetime.now().time()
		print 'fininshed'
		#run_time = start_time[]-end_time[]
		print start_time[:7]
