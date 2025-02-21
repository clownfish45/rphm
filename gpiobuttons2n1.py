import RPi.GPIO as GPIO
import time
import pyautogui
import json
from threading import Thread
import dictdatabase as DDB

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.OUT, initial = 1)

menu1 = ["_GRAPHSTART_", "_COHEREBUTTON_", "_DELETE_", "_LOGOUT_"]
menu2 = ["_READMODE_", "_GRAPHCANVAS_", "_GRAPH_", "_READING_", "_BACK_"]
#menu3 = ["_LOGIN1_", "_USER1_", "_USER2_", "_USER3_", "_USER4_", "_EXIT_"]
menu3 = ["_LOGIN1_", "_NEWUSER_", "_SIGNIN_", "_EXIT_"]
menuSelect = ["_TEMP_", "_HB_", "_BLOODOXYGEN_", "_SELBACK_"]
menuai = ["_COHERE_", "_COHEREBACK_"]

def gpioengine1():
	global menu1 ,menu2, menu3, menuai
	press = False
	
	menu1pos = [(393, 83), (400, 48), (397, 18)]
	menu2pos = [(413, 294), (413, 256)]
	menu3pos = [(322, 125), (428, 73), (248, 73), (428, 59), (248, 37)]
	#menu3pos = [(248, 37), (428, 59), (248, 73), (428, 73), (322, 125)]
	currentpos = []

	i = 0

	GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	while True:
		
		with open("/home/theapplepi/Documents/theApplePi/last/lastmenu.txt", "r") as fo:
			lastmenu = fo.read()
		
		if lastmenu == str(menu1):
			currentpos = menu1pos
		elif lastmenu == str(menu2):
			currentpos = menu2pos
		elif lastmenu == str(menu3):
			currentpos = menu3pos
		elif lastmenu == str(menuai):
			currentpos = [(410, 123)]
			i = len(currentpos)

		if GPIO.input(38) == GPIO.HIGH and press == False:
			press = True
			time.sleep(0.3)
			continue
		if GPIO.input(38) == GPIO.LOW and press == True:
			if i < len(currentpos):
				try:
					pyautogui.moveTo(currentpos[i])
					print("one click1")
					i += 1
				except:
					print("unsuccessful1")
			else:
				try:
					print("one click1")
					pyautogui.moveTo(currentpos[0])
					i = 1
				except:
					print("unsuccesssful1")
			time.sleep(0.1)
			press = False
			continue
		if GPIO.input(38) == GPIO.HIGH and press == True:
			pyautogui.click()
		
		
		

def gpioengine2():
	global menu1 ,menu2, menu3, menuai
	press = False
	i = 0
	menu1pos = [(397, 18), (400, 48), (393, 95)]
	menu2pos = [(413, 256), (413, 294)]	
	menu3pos = [(248, 37), (428, 59), (248, 73), (428, 73), (322, 125)]
	currentpos = []

	GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	while True:
		
		with open("/home/theapplepi/Documents/theApplePi/last/lastmenu.txt", "r") as fo:
			lastmenu = fo.read()
		
		if GPIO.input(40) == GPIO.HIGH and press == False:
			press = True
			time.sleep(0.3)
			continue
		if GPIO.input(40) == GPIO.LOW and press == True:
			if i < len(currentpos):
				try:
					pyautogui.moveTo(currentpos[i])
					i += 1
				except:
					print("unsuccessful2")
			else:
				try:
					pyautogui.moveTo(currentpos[0])
					i = 1
				except:
					print("unsuccesssful2")
			time.sleep(0.1)
			press = False
			continue
		if GPIO.input(40) == GPIO.HIGH and press == True:
			pyautogui.click()
		
		if lastmenu == str(menu1):
			currentpos = menu1pos
		elif lastmenu == str(menu2):
			currentpos = menu2pos
		elif lastmenu == str(menu3):
			currentpos = menu3pos
		elif lastmenu == str(menuai):
			currentpos = [(410, 123)]
			i = len(currentpos)

