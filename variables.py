import PySimpleGUI as sg
from datetime import date
import json
from random import randint
import cohere
from max30105 import MAX30105, HeartRate
from w1thermsensor import W1ThermSensor, Unit
import dictdatabase as DDB
import time
import serial
import adafruit_fingerprint
import os
import max30102
import hrcalc


uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

font = "Silkscreen 26"
sg.change_look_and_feel("DarkBlue14")
title = "APPLEPI"
prevval = ""
jsondir = "/home/theapplepi/Documents/theApplePi/userData" #------> jsondir for rpi
#jsondir = "/Users/chmy_kh/Documents/theApplePi/userData" #--------> jsondir for mac
DDB.config.storage_directory = "/home/theapplepi/Documents/theApplePi/"
graphcol = "lightblue"
lastmenu = ""
coheretext = ""

GRAPH_SIZE = (400,200)
GRAPH_STEP_SIZE = 15
amount = 0
lasty = y = x = lastx = highesty = 0
preventIndex = 0 		#index that shows the recording number
maxUserCount = 50
bpm  = float()
avg_bpm = float()

goBack = False
graphactive = False
login = True
delay = None
newfile = None
ai = False
once = True
allgraph = False
stopgraph = False
graphStage = 0
beat = bool()


menu1 = ["_GRAPHSTART_", "_COHEREBUTTON_", "_DELETE_", "_LOGOUT_"]
menu2 = ["_READMODE_", "_GRAPHCANVAS_", "_GRAPH_", "_STATS_", "_BACK_"]
menu3 = ["_LOGIN1_", "_NEWUSER_", "_SIGNIN_", "_EXIT_"]
menuSelect = ["_TEMP_", "_HR_", "_BLOODOXYGEN_", "_ALL_", "_SELBACK_"]
menuai = ["_COHERE_", "_COHEREBACK_"]
lastmenu = []

keylist = menu1 + menu2 + menu3 + menuSelect + menuai

menustate = {}
hello = {}

dbval = dict()
userNum = int()


class variableStorage:
	finishedTask= False
	tempText = str()
	userNum = int()
	err = False
	readmode = str()


vs = variableStorage()



readmodes = ["temperature", "heartbeat", "bloodoxygen"]
readmode = ""


co = cohere.Client('bE0FaKsN0Cs3Z0nl9DNJ9ko6bctPqUrpBfMLcsJp')


m = max30102.MAX30102()

max30105 = MAX30105()
max30105.setup(led_power=50, leds_enable=2)

def read_hr():
	# Read data from the sensor
	red, ir = m.read_sequential()
	# Calculate heart rate and SpO2
	hr, hr_valid, spo2, spo2_valid = hrcalc.calc_hr_and_spo2(ir, red)

	# Check if valid readings are obtained
	if hr_valid:
		return hr
	else:
		return -1

def read_bloodoxygen():
	red, ir = m.read_sequential()
	# Calculate heart rate and SpO2
	hr, hr_valid, spo2, spo2_valid = hrcalc.calc_hr_and_spo2(ir, red)

	# Check if valid readings are obtained
	if spo2_valid:
		return round(spo2, 2)
	else:
		return -1




for i in range(len(keylist)):
	menustate[keylist[i]] = True






def jsonChange(x, y, z):		#when called if it's in write or append mode writes (or appends) to the json file (z directory) with y. when in read mode syncs y with json file (z directory).
	if x == "w" or x == "a":	# USED WHEN WORKING WITH EXTERNAL JSON FILE
		with open(z, x) as file:
			json.dump(y, file, indent = 2)
	elif x == "r":
		with open(z, x) as file:
			y = json.load(file)

def timeReplaceAppend(x = None, y = None): ##creates a date variable, if x and y are called appends the y variable to x, the dictionary. USED WHEN WORKING WITH LOCAL DICTIONARY
	if y == None or x == None:
		return str(date.today()).replace("-", "")
	else:
		return x.append(y)

def dateToday():
	return str(date.today()).replace("-", "")

def newdb(hello):
	'''
	if DDB.at("log").exists() == False:
		hello[timeToday()][str(preventIndex)] = {"temperature1" : [], "temperature2" : [], "heartbeat" : []}
		DDB.at("log").create(hello)

	new structure = {
					0:{
						heartbeat:{"06122025":[]}
						temperature:{}
						bloodoxygen:{}
						
					}}
	'''


def menu(x):
	nkeylist = []
	nkeylist += keylist
	for i in range(len(x)):
		window[x[i]].update(visible = True)
		window[x[i]].unhide_row()
		menustate[x[i]] = True
	for y in range(len(x)):
		nkeylist.remove(x[y])
	for p in range(len(nkeylist)):
		if menustate[nkeylist[p]] == True:
			window[nkeylist[p]].hide_row()
			window[nkeylist[p]].update(visible = False)
			menustate[nkeylist[p]] = False
	with open("/home/theapplepi/Documents/theApplePi/last/lastmenu.txt", "w") as f:
		f.write(str(x))

def scale():
	window["_GRAPHCANVAS_"].DrawLine((2, 0), (2, 200), width = 1)
	for i in range(1, int(200 / 5)):
			window["_GRAPHCANVAS_"].DrawLine((0, i * 10), (4, i * 10), width = 1)
			window["_GRAPHCANVAS_"].draw_text(location = (6, i * 10), text = str(i * 10), font = "Silkscreen 16", color = "black")

def preventDel():
	global hello, preventIndex, jsondircache, newfile
	with open("/home/theapplepi/Documents/theApplePi/last/lastjsondir.txt") as file:
		jsondircache = file.read()
		print(jsondircache)
	try:
		'''
		with open(jsondircache) as f:  			#checks if the file already exists. if it does, writes the jsonfile to preventRemove	
			print(str(preventRemove) + "1 happened")
		'''
		with open(jsondircache, "r") as j:
			preventRemove = dict(json.load(j))
		print(str(preventRemove) + "1 happened")

		try:
			print(preventRemove, "im trying")
			print(preventRemove[str(timeReplaceAppend())], "im tryingagain")	#checks if the date already exists in the dictionary
			preventIndex = len(preventRemove[timeReplaceAppend()])
			print("preventindex is ", len(preventRemove[timeReplaceAppend()]))
			preventIndex = str(preventIndex)
			hello = preventRemove
			print(str(hello) + "2 happened")
			del preventRemove
		except:
			hello = preventRemove
			hello[timeReplaceAppend()] = {0 : {"temperature1" : [], "temperature2" : [], "heartbeat" : []}}
			del preventRemove
			print(str(hello) + "3 happened")
			with open(jsondircache, "w") as file:
				json.dump(hello, file, indent = 2)
	except:
		newfile = True
		hello = {}
		jsonChange("w", hello, jsondircache)
		print(str(hello) + "4 happened")
	'''
	print(preventIndex)
	temp = preventIndex["temperature"]
	print(temp)
	'''
	trytuple = (hello, preventIndex, newfile)
	return trytuple



	## FINISH LATER THE FUNC. or no?



layout = [  
	[sg.Text(text="hello! pick a user!", key = "_LOGIN1_", visible = False)],
	[sg.Text(readmode, key = "_READMODE_", visible = False)],
#'''
#	[sg.Button("USER 1", key = "_USER1_", visible = False, size = 25), sg.Button("USER 2", key = "_USER2_", visible = False, size = 25)],
#	[sg.Button("USER 3", key = "_USER3_", visible = False, size = 25), sg.Button("USER 4", key = "_USER4_", visible = False, size = 25)],
#'''	
	[sg.InputText(key = "_LOGINPROMPT_", visible = False)],
	[sg.Button("NEW USER", key = "_NEWUSER_", visible = False, size = 25), sg.Button("SIGN IN", key = "_SIGNIN_", visible = False, size = 25)],
	[sg.Submit(key = "_LOGIN2_", size = 100, visible = False)],
	[sg.Button("Take a reading", key = "_GRAPHSTART_", visible = False, size = 100)],
	[sg.Exit(key = "_EXIT_", size = 50, visible = False)],
	[sg.Button("ASK AI", key = "_COHEREBUTTON_", visible = False, size = 100)],
	[sg.Button("DELETE USER", key = "_DELETE_", visible = False, size = 100)],
	[sg.Button("LOGOUT", key = "_LOGOUT_", visible = False, size = 100)],
	[sg.Graph(canvas_size=(40, 200), graph_bottom_left=(0, 0), graph_top_right=(8, 200), background_color = graphcol, key = "_GRAPHCANVAS_", visible = False), sg.Graph(GRAPH_SIZE, (0,0), GRAPH_SIZE, key="_GRAPH_", background_color = graphcol, visible = False),],
	[sg.Text(text="", key = "_STATS_", visible = False)],
	[sg.Button("GO BACK", key = "_BACK_", visible = False, size = 100)],
	[sg.Text("", key = "_COHERE_", visible = False, auto_size_text = False, size = (700, 15), expand_y=True, font="Silkscreen 26")],#expand_x=True, 
	[sg.Button("GO BACK", key = "_COHEREBACK_", visible = False, size = 25), sg.Button("DIFFERENT reading", key = "_READING_", visible = False, size = 25)],
	[sg.Button("temperature", key = "_TEMP_", visible = False, size = 100)],
	[sg.Button("heart rate", key = "_HR_", visible = False, size = 100)],
	[sg.Button("BLOOD OXYGEN", key = "_BLOODOXYGEN_", visible = False, size = 100)],
	[sg.Button("read all", key = "_ALL_", visible = False, size = 100)],
	[sg.Button("BAck", key = "_SELBACK_", visible = False, size = 100)],
	
	
]


window = sg.Window(title, layout, size = (800, 480),element_justification = "c", font = font, finalize = True)


#window("_LOGIN1_").update(text = "whatever")


def get_fingerprint_detail():
	

	'''
	if DDB.at("log").exists() == False:
		#window["_LOGIN1_"].update("No users exist yet! Create a new one!")
		vs.tempText = "No users exist yet! Create a new one!"
		time.sleep(2)
		return False
	'''
	
	#vs.tempText = "Scanning the finger..." <--undo
	#time.sleep(0.2) <--undo
	#print("we got to here")
	i = finger.get_image()
	#print("we got past the roadblock!!!")
	if i == adafruit_fingerprint.OK:
		pass
		#print("Image taken")
	else:
		print("point 0.5 (oops....)")
		if i == adafruit_fingerprint.NOFINGER:
			#print("")
			#window["_LOGIN1_"].update("No finger detected")
			vs.tempText = "No finger detected"
		elif i == adafruit_fingerprint.IMAGEFAIL:
			#print("Imaging error")
			#window["_LOGIN1_"].update("Imaging error")
			vs.tempText = "Imaging error"
		else:
			#window["_LOGIN1_"].update("Unknown error!")
			print("Other error")
			vs.tempText = "Unknown error!"
		return False

	print("point 1")

	#print("Templating...", end="")
	i = finger.image_2_tz(1)
	if i == adafruit_fingerprint.OK:
		#print("Templated")
		pass
	else:
		if i == adafruit_fingerprint.IMAGEMESS:
			print("Image too messy")
			vs.tempText = "Image distorted! Clean the sensor and or your hands!"
			#window["_LOGIN1_"].update("Image distorted! Clean the sensor and or your hands!")
		elif i == adafruit_fingerprint.FEATUREFAIL:
			print("Could not identify features")
			vs.tempText = "Culd not recognize a human fingerprint"
			#window["_LOGIN1_"].update("Could not recognize a human fingerprint.")
		elif i == adafruit_fingerprint.INVALIDIMAGE:
			#window["_LOGIN1_"].update("Invalid image")
			vs.tempText = "Invalid image"
			print("Image invalid")
		else:
			#window["_LOGIN1_"].update("Unknown error!")
			vs.tempText = "Unknown error!"
			print("Other error")
		return False
	print("point 2")
	#print("Searching...", end="")
	i = finger.finger_fast_search()
	# pylint: disable=no-else-return
	# This block needs to be refactored when it can be tested.
	if i == adafruit_fingerprint.OK:
		print("Found fingerprint!")
		#window["_LOGIN1_"].update(f"Found user! (user {i})")
		vs.tempText = f"Found user! (user{i})"
		userNum = i
		time.sleep(0.1)
		vs.userNum = i
		return True
	else:
		if i == adafruit_fingerprint.NOTFOUND:
			print("No match found")
			#window["_LOGIN1_"].update("User not found! create a new user or try again!")
			vs.tempText = "User not found! create a new user or try again!"
		else:
			print("Other error")
			vs.tempText = "Unknown error!"
			#window["_LOGIN1_"].update("Unknown error!")
		return False
	


def get_fingerprint():

	if DDB.at("log").exists() == False:
		#window["_LOGIN1_"].update("No users exist yet! Create a new one!")
		vs.tempText = "No users exist yet! Create a new one!"
		time.sleep(2)
		return False

	"""Get a finger print image, template it, and see if it matches!"""
	#print("Waiting for image...")
	vs.tempText = "Scanning finger..."
	while finger.get_image() != adafruit_fingerprint.OK:
		pass
	#print("Templating...")
	if finger.image_2_tz(1) != adafruit_fingerprint.OK:
		vs.tempText = "Failed to identify finger! Clean the sensor!"
		time.sleep(2)
		return False
		
	#print("Searching...")
	if finger.finger_search() != adafruit_fingerprint.OK:
		vs.tempText = "The fingerprint could not be found in the database."
		time.sleep(2)
		return False
	vs.tempText = f"Found user! (user{finger.finger_id})"
	userNum = finger.finger_id
	time.sleep(1)
	vs.userNum = finger.finger_id
	return True


def enroll_finger(location): #usage: enroll_finger(get_num(finger.library_size))
	"""Take a 2 finger images and template it, then store in 'location'"""
	for fingerimg in range(1, 3):
		if fingerimg == 1:
			vs.tempText = "Place your finger on the sensor..."
			print("Place finger on sensor...", end="")
		else:
			time.sleep(0.5)
			print("Place same finger again...", end="")
			vs.tempText = "Place your finger on the sensor again..."

		while True:
			i = finger.get_image()
			if i == adafruit_fingerprint.OK:
				print("Image taken")
				break
			if i == adafruit_fingerprint.NOFINGER:
				print(".", end="")
			elif i == adafruit_fingerprint.IMAGEFAIL:
				print("Imaging error")
				vs.tempText = "Imaging error!"
				vs.err = True
				time.sleep(0.5)
				return False
			else:
				print("Other error")
				vs.tempText = "Unknown error!"
				vs.err = True
				time.sleep(0.5)
				return False

		#print("Templating...", end="")
		i = finger.image_2_tz(fingerimg)
		if i == adafruit_fingerprint.OK:
			#print("Templated")
			pass
		else:
			if i == adafruit_fingerprint.IMAGEMESS:
				print("Image too messy")
				vs.tempText = "Image too messy! clean your finger and or the sensor"
				vs.err = True
				time.sleep(0.5)
			elif i == adafruit_fingerprint.FEATUREFAIL:
				print("Could not identify features")
				vs.tempText = "Could not identify a finger!"
				vs.err = True
				time.sleep(0.5)
			elif i == adafruit_fingerprint.INVALIDIMAGE:
				print("Image invalid")
				vs.tempText = "Invalid image!"
				vs.err = True
				time.sleep(0.5)
			else:
				print("Other error")
				vs.tempText = "Unknown error!"
				vs.err = True
				time.sleep(0.5)
			return False

		if fingerimg == 1:
			print("Remove finger")
			vs.tempText = "Remove finger"
			time.sleep(0.5)
			time.sleep(1)
			while i != adafruit_fingerprint.NOFINGER:
				i = finger.get_image()

	print("Creating model...", end="")
	i = finger.create_model()
	if i == adafruit_fingerprint.OK:
		print("Created")
		
	else:
		if i == adafruit_fingerprint.ENROLLMISMATCH:
			print("Prints did not match")
			vs.tempText = "Fingers did not match!"
			vs.err = True
			time.sleep(0.5)
		else:
			print("Other error")
			vs.tempText = "Unknown error!"
			vs.err = True
			time.sleep(0.5)
		return False
	
	#print("Storing model #%d..." % location, end="")
	vs.tempText = f"Storing model #{location}"
	i = finger.store_model(location)
	if i == adafruit_fingerprint.OK:
		print("Stored")
		vs.tempText = "Stored the fingerprint successfully! User created"
		vs.finishedTask = True
	else:
		if i == adafruit_fingerprint.BADLOCATION:
			vs.tempText = "Bad storage location"
			vs.err = True
		elif i == adafruit_fingerprint.FLASHERR:
			vs.tempText = "Flash storage error"
			vs.err = True
		else:
			vs.tempText = "Other error"
			vs.err = True
		return False

	return True


# size = (800, 480),

#previous version in diff hunk

if __name__ == "__main__":
	sg.Popup("You are not supposed to run this file!")
	exit();

window.maximize()# <------ undo this later
