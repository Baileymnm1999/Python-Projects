import os, threading, thread, time

text = "T"

def function():
	os.system("gnome-terminal -e 'airodump-ng wlan0mon'")

def update(recall):
	while True:
		os.system("pkill airodump-ng")
		file = open("/root/Desktop/Summer/test.txt", "a+")
		content = file.read()
		file.write(text)
		recall()
		time.sleep(5)

blacklist_update = threading.Thread(target=update, args=(function,))
blacklist_update.daemon = True
blacklist_update.start()

raw_input("Do something ")

