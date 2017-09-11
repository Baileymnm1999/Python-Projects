import os, time, exceptions

FRIENDLY_BSSID = "8A:DC:96:3F:91:CD"    #Friendly solo
ENEMY_BSSID = "8A:DC:96:3F:6E:EE"   	#Enemy solo
DLINK_BSSID = "68:7F:74:0C:8E:53"    	#DLink

#Starts wifi card in monitor mode
os.system("airmon-ng start wlan0")

#Deletes previous capture output and saves new capture output
os.system("echo 'Attempting to delete previous capture.'")
os.system("rm -f /root/Desktop/Summer/recon-01.csv")
os.system("clear && echo 'Previous capture deleted, Creating new capture.'")	
os.system("gnome-terminal -e 'timeout 22 airodump-ng -w recon --output-format csv --write-interval 4 wlan0mon'")
time.sleep(22)
os.system("clear && echo 'New capture created.'")
time.sleep(2)
os.system("pkill airodump-ng")
os.system("clear")

#Parse capture output for friendly and enemy network channels
file = open("/root/Desktop/Summer/recon-01.csv", "r")
content = file.read()
try:
	our_channel = content[content.index("8A:DC:96:3F:91:CD") +61 :]
	our_channel = our_channel[:our_channel.index("54") -3]
except:
	os.system("clear")
	raw_input("Friendly network not found, exiting.")
	#exit()
try:
	their_channel = content[content.index("8A:DC:96:3F:6E:EE") +61 :]
	their_channel = their_channel[:their_channel.index("54") -3]
except:
	os.system("clear")
	raw_input("Enemy network not found, exiting.")
	#exit()
file.close()

#Finds MAC addresses on given network
def survey_network(channel, bssid, log_name):
	#Deletes previous capture output and saves new capture output targeting specific network
	os.system("echo 'Attempting to delete previous network capture.'")
	os.system("rm -f /root/Desktop/Summer/survey-01.csv")
	os.system("clear && echo 'Previous capture deleted, Creating new network capture.'")	
	os.system("gnome-terminal -e 'airodump-ng -w survey --output-format csv --write-interval 6 -c "+channel+" --bssid "+bssid+" wlan0mon'")
	os.system("clear && echo 'New capture created.'")
	time.sleep(2)
	os.system("clear")

	#Loop to read capture and log MACs on our network
	while True:
		time.sleep(6)
		os.system("clear")
		survey = open("/root/Desktop/Summer/survey-01.csv", "r")
		survey_content = survey.read()
		survey_content = survey_content[survey_content.index("ESSIDs") +8:]
		lines = survey_content.splitlines()
		macs_log = open("/root/Desktop/Summer/"+log_name, "a+")
		macs_content = macs_log.read()
		for line in lines:
			line = line[:17]
			print line
			if line in macs_content:
				pass
			else:
				macs_log.write(line +"\n")
		survey.close()


def prompt():
	#Creation of menu
	os.system("clear")
	os.system("echo '1. Survey our network'")
	os.system("echo '2. Survey their network'")

	#Selection of what you want to do
	mode = int(raw_input())
	if mode == 1:
		survey_network(our_channel, FRIENDLY_BSSID, "friendly_log")
	elif mode == 2:
		survey_network(their_channel, ENEMY_BSSID, "enemy_log")
	else:
		raw_input("Invalid response")
		prompt()

prompt()



