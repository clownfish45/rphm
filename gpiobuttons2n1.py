import RPi.GPIO as GPIO
import time
import pyautogui
import json
from threading import Thread
import dictdatabase as DDB

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.OUT, initial = 1)
GPIO.setup(37, GPIO.OUT, initial = 1)

menu1 = ["_GRAPHSTART_", "_COHEREBUTTON_", "_DELETE_", "_LOGOUT_"]
menu2 = ["_READMODE_", "_GRAPHCANVAS_", "_GRAPH_", "_STATS_", "_BACK_"]
menu3 = ["_LOGIN1_", "_NEWUSER_", "_SIGNIN_", "_EXIT_"]
menuSelect = ["_TEMP_", "_HR_", "_BLOODOXYGEN_", "_ALL_", "_SELBACK_"]
menuai = ["_COHERE_", "_COHEREBACK_"]

def gpioengine1():
	global menu1 ,menu2, menu3, menuSelect, menuai
	press = False
	i = 0
	menu1pos = [(388, 153), (372, 109), (371, 72), (374, 42)]
	menu2pos = [(444, 305)]
	menu3pos = [(430, 93), (489, 58), (390, 55)]
	menuSelectpos = [(379, 192), (376, 150), (377, 109), (389, 63), (400, 16)]
	menuaipos = [(447, 352)]
	currentpos = []

	GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	while True:
		
		with open("/home/theapplepi/Documents/theApplePi/last/lastmenu.txt", "r") as fo:
			lastmenu = fo.read()
		
		if lastmenu == str(menu1):
			currentpos = menu1pos
		elif lastmenu == str(menu2):
			currentpos = menu2pos
		elif lastmenu == str(menu3):
			currentpos = menu3pos
		elif lastmenu == str(menuSelect):
			currentpos = menuSelectpos
		elif lastmenu == str(menuai):
			currentpos = menuaipos



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
		elif GPIO.input(40) == GPIO.HIGH and press == True:
			pyautogui.click()
			time.sleep(0.5)
		time.sleep(0.05)

def gpioengine2():
	global menu1 ,menu2, menu3, menuSelect, menuai
	press = False
	
	menu1pos = [(374, 42), (371, 72), (372, 109), (388, 153)]#
	menu2pos = [(444, 305)]#
	menu3pos = [(390, 55), (489, 58), (430, 93)]#
	menuSelectpos = [(400, 16), (389, 63), (377, 109), (376, 150), (379, 192)]#
	menuaipos = [(447, 352)]#
	currentpos = []
	
	'''
	menu1pos = [(388, 153), (372, 109), (371, 72), (374, 42)]
	menu2pos = [(444, 305)]
	menu3pos = [(430, 93), (489, 58), (390, 55)]
	menuSelectpos = [(379, 192), (376, 150), (377, 109), (389, 63), (400, 16)]
	menuaipos = [(463, 138)]
	
	'''

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
		elif lastmenu == str(menuSelect):
			currentpos = menuSelectpos
		elif lastmenu == str(menuai):
			currentpos = menuaipos
		

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
		elif GPIO.input(38) == GPIO.HIGH and press == True:
			pyautogui.click()
			time.sleep(0.5)
		time.sleep(0.05)
		
		
		


		
		
			

'''
menu3:
(67, 81), (710, 79), (572, 149)

menu1:
(403, 29), (413, 78), (418, 142), (415, 197)

menuSelect
(425, 31), (418, 85), (416, 138), (404, 204), (404, 250)

graphend
(424, 334)

ai
(409, 217)
'''


#Point(x=447, y=352)
#(447, 352)