#from gpiobuttons2n1 import * test only
from variables import *
from threading import Thread
from random import randint
import dictdatabase as DDB
import sys

print("\n\n\n\n new")
''' test only
Thread(target = gpioengine1, daemon = True).start()
Thread(target = gpioengine2, daemon = True).start()
Thread(target = getheart, daemon = True).start()
'''
menu(menu3)
#window.TKroot["cursor"] = "none"
while True:							 # Event Loop
	event, values = window.read(timeout = delay)
	if newfile == False:
		trytuple[0] = hello
		trytuple[1] = preventIndex
	if event == "_EXIT_" or event == sg.WIN_CLOSED:
		break
	elif login == False:

		menu(menu3)
		#Thread(target = get_fingerprint_detail, daemon = True).start()
		#window["_LOGIN1_"].update(text = "Scanning the finger...")
		delay = 500
		
		#window["_LOGIN1_"].update(text = "Scanning the finger...")
	
	if event == "_SIGNIN_":
		window["_LOGIN1_"].update("Scanning the finger...")
		window.refresh()
		time.sleep(0.3)
		
		'''
		get_fingerprint_detail(userNum)
		if userNum != 0:
			menu(menu1)
			login = True
			dbval = DDB.at("log").read()
		'''

		check = Thread(target = get_fingerprint, daemon = True)
		check.start()

		while check.is_alive():
			if event == "_EXIT_":
				sys.exit(0)
			window["_LOGIN1_"].update(vs.tempText)
			window.refresh()
			#print("this is happening")
			#print(vs.tempText, "were doing something")
			time.sleep(0.1)
		
		#print("it has ended")
		
		if vs.userNum != 0:
			menu(menu1)
			login = True
			dbval = DDB.at("log").read()
			userNum = vs.userNum
			vs.tempText = "Successful login"
		
		delay = None
		event = None

		
	elif event == "_NEWUSER_":
		if DDB.at("log").exists() == False:
			userNum = 1
			dbval = {
						"lastuser": 1,
						"userquantity": 1,
						"1": {
							"heartbeat":{},
							"temperature":{},
							"bloodoxygen":{}
						}
					}
			
			event = None
			ef = Thread(target = enroll_finger, daemon = True, args=(1,))
			ef.start()

			
			cancel = False
			
			while ef.is_alive():
				if event == "_RETRY_" or event == "_NEWUSER_":
					window["_LOGIN1_"].update("Cancelling user creation")
					window.refresh()
					cancel = True
				elif event == "_EXIT_":
					sys.exit(0)
				else:
					window["_LOGIN1_"].update(vs.tempText)
					window.refresh()
					#print(vs.tempText, "were doing something")
					time.sleep(0.1)


			if vs.finishedTask == True and cancel == False and vs.err == False:
				DDB.at("log").create(dbval)
				window["_LOGIN1_"].update("Created a new user!")
				window.refresh()
				vs.finishedTask = False
			else:
				vs.err = False
				window["_LOGIN1_"].update("Could not create a user!")
				window.refresh()
				vs.finishedTask = False
		elif DDB.at("log").read()["userquantity"] >= 4:
			window["_LOGIN1_"].update("User limit reached: 4")
			window.refresh()
		else:
			dbval = DDB.at("log").read()
			userNum = dbval["lastuser"] + 1

			event = None
			ef = Thread(target = enroll_finger, daemon = True, args=(userNum,))
			ef.start()

			
			cancel = False
			
			while ef.is_alive():
				if event == "_RETRY_" or event == "_NEWUSER_":
					window["_LOGIN1_"].update("Cancelling user creation")
					window.refresh()
					cancel = True
				elif event == "_EXIT_":
					finger.delete_model(userNum)
					sys.exit(0)
				else:
					window["_LOGIN1_"].update(vs.tempText)
					window.refresh()
					#print(vs.tempText, "were doing something")
					time.sleep(0.1)


			if vs.finishedTask == True and cancel == False and vs.err == False:
				with DDB.at("log").session() as (session, log):
					log[f"{userNum}"] = {"heartbeat":{},"temperature":{},"bloodoxygen":{}}
					log["lastuser"] = userNum
					log["userquantity"] += 1
					session.write()
				window["_LOGIN1_"].update("Created a new user!")
				window.refresh()
				vs.finishedTask = False
				dbval = DDB.at("log").read()
			else:
				vs.err = False
				window["_LOGIN1_"].update("Could not create a user!")
				window.refresh()
				finger.delete_model(userNum)
				vs.finishedTask = False

			
	if event == "_DELETE_":
		dbval = DDB.at("log").read()

		if dbval["lastuser"] == userNum:
			dbval["lastuser"] = userNum - 1
		
		dbval["userquantity"] -= 1
		
		try:
			del dbval[str(userNum)]
			finger.delete_model(userNum)
			
			os.remove(f"{DDB.config.storage_directory}log.json")
			DDB.at("log").create(dbval)
			login = False
			menu(menu3)
		except:
			print("The key does not exist! line 168 main alpha")


		

		


	'''
	if event == "_USER1_":
		jsondircache = jsondir + "/" + "_USER1_".lower() + ".json"
		with open("/home/theapplepi/Documents/theApplePi/last/lastjsondir.txt", "w") as f:
			f.write(jsondircache)
		#prevval = event
		#bigboy
		preventDel()
		print(str(newfile))
		print(str(hello) + "menuchange")
		menu(menu1)
		login = True
	elif event == "_USER2_":
		jsondircache = jsondir + "/" + "_USER2_".lower() + ".json"
		with open("/home/theapplepi/Documents/theApplePi/last/lastjsondir.txt", "w") as f:
			f.write(jsondircache)
		#prevval = event
		#bigboy
		preventDel()
		print(str(newfile))
		print(str(hello) + "menuchange")
		menu(menu1)
		login = True
	elif event == "_USER3_":
		jsondircache = jsondir + "/" + "_USER3_".lower() + ".json"
		with open("/home/theapplepi/Documents/theApplePi/last/lastjsondir.txt", "w") as f:
			f.write(jsondircache)
		#prevval = event
		#bigboy
		preventDel()
		print(str(newfile))
		print(str(hello) + "menuchange")
		menu(menu1)
		login = True
	elif event == "_USER4_":
		jsondircache = jsondir + "/" + "_USER4_".lower() + ".json"
		with open("/home/theapplepi/Documents/theApplePi/last/lastjsondir.txt", "w") as f:
			f.write(jsondircache)
		#prevval = event
		#bigboy
		preventDel()
		print(str(newfile))
		print(str(hello) + "menuchange")
		menu(menu1)
		login = True
		#jsondircache = jsondir + "/" + str(event).lower() + ".json"
		
		with open("/home/theapplepi/Documents/theApplePi/last/lastjsondir.txt", "w") as f:
			f.write(jsondircache)
		#prevval = event
		#bigboy
		preventDel()
		print(str(newfile))
		print(str(hello) + "menuchange")
		menu(menu1)
		login = True
	'''
		#if str(event) == prevval:
		#	delay = None
		
	'''
		else:
			jsondircache = jsondir + "/" + str(event).lower() + ".json"
			prevval = str(event)
			#bigboy
			preventDel()
			print(str(newfile))
			if newfile == True:
				hello[timeReplaceAppend()] = {str(preventIndex) : {"temperature" : []}}
				newfile = False
			print(str(hello) + "menuchange")
			menu(menu1)
			login = True
		'''

	if event == "_LOGOUT_":
		delay = None
		login = False
		
		vs.finishedTask= False
		vs.tempText = str()
		vs.userNum = int()

		userNum = int()
		dbval = dict()

		menu(menu3)
	elif event == "_GRAPHSTART_":
		graphactive = True
		preventDel()
		menu(menu2)
		scale()
		print(hello)
		try:
			hello[timeReplaceAppend()][str(preventIndex)] = {"temperature1" : [], "temperature2" : [], "heartbeat" : []}
		except:
			hello[timeReplaceAppend()] = {str(preventIndex) : {"temperature1" : [], "temperature2" : [], "heartbeat" : []}}
		readmode = "temperature1"
		delay = 500
	elif event == "_COHEREBUTTON_":
		ai = True
		delay = 500

	elif ai == True:
		if once == True:
			menu(menuai)
			with open(jsondircache, "r") as j:
				hello = dict(json.load(j))
			try :
				ls = hello[str(timeReplaceAppend())][str(preventIndex)]["temperature1"]
				lb = hello[str(timeReplaceAppend())][str(preventIndex)]["temperature2"]
				lg = hello[str(timeReplaceAppend())][str(preventIndex)]["heartbeat"]
			except:
				ls = hello[str(timeReplaceAppend())][str(preventIndex - 1)]["temperature1"]
				lb = hello[str(timeReplaceAppend())][str(preventIndex - 1)]["temperature2"]
				lg = hello[str(timeReplaceAppend())][str(preventIndex - 1)]["heartbeat"]
			response = co.generate(
				prompt = f"The latest temperature mesurements of my body	 in degrees C were {ls}. \
				The heartbeat rate per minute were {lg}\
				The other temperature for a good measure were {lb}\
				What are your opinions on the temperatures and what do you\
				 suggest the person should do to improve them? Also, what are your opinions on the heartbeat of the person? Answer in one sentence",
			)
			response = list(response)
			coheretext = str(response[0])
			print(coheretext)
			'''
			hl = len(coheretext)
			for i in range(hl // 75 + 1):
				num = int(hl / hl // 75 + 1 * i)
				l = list(coheretext)
				l[num] = "/n"
				coheretext = "".join(l)
				print(l)
			'''
			#window["_COHERE_"].update(coheretext)
			sg.popup_timed(coheretext)
			once = False
		if event == "_COHEREBACK_":
			once = True
			ai = False
			menu(menu1)	

	elif graphactive == True:
		if event == "_BACK_":
			graphactive = False
			if x < 180:
				if amount != 0:
					window["_GRAPH_"].Move(GRAPH_STEP_SIZE * amount, 0)
					amount = 0
				window["_GRAPH_"].erase()
			lastx = lasty = y = 0
			x = 0
			preventIndex += 1
			jsonChange("w", hello, jsondircache)
			menu(menu1)
		if x >= 180:
			if amount != 0:
				window["_GRAPH_"].Move(GRAPH_STEP_SIZE * amount, 0)
				amount = 0
			else:
				window["_GRAPH_"].erase()   #finsih!!!!
			jsonChange("w", hello, jsondircache)
		if event == "_READING_":
			pos = readmodes.index(readmode)
			if pos == 2:
				readmode = readmodes[0]
			else:
				readmode = readmodes[pos + 1]

		'''
		test only
		if readmode == "temperature1":
			y = max30105.get_temperature()
			window["_READMODE_"].update("temperature1")
		elif readmode == "temperature2":
			y = tempsensor.get_temperature(Unit.DEGREES_C)
			window["_READMODE_"].update("temperature2")
		elif readmode == "heartbeat":
			hr = HeartRate(max30105)
			hr.on_beat(storeheartbeat, average_over = 4)
			y = avg_bpm
			window["_READMODE_"].update("heartbeat")

		'''
		if readmode == "temperature1" or readmode == "temperature2" or readmode == "heartbeat":
			y = randint(20,100)
			window["_READMODE_"].update("heartbeat") #test only

		if x < GRAPH_SIZE[0] and graphactive == True and x < 180:			   # if still drawing initial width of graph
			''' test only
			hr = HeartRate(max30105)
			hr.on_beat(storeheartbeat, average_over = 4)
			'''
			hr = randint(80,120)

			if y != 0.0 and y != 0:
				window["_GRAPH_"].DrawLine((lastx+2, lasty * 2), (x+2, y * 2), width=1)
				amount += 1
			else:
				sg.popup_timed("HEY! There's an incorrect reading. Make sure to push your fingers against the sensors or check the connections!")

			print(preventDel())
			preventDel()
			print(hello[timeReplaceAppend()])
			'''test only
			timeReplaceAppend(hello[timeReplaceAppend()][str(preventIndex)]["temperature1"], max30105.get_temperature())
			timeReplaceAppend(hello[timeReplaceAppend()][str(preventIndex)]["temperature2"], tempsensor.get_temperature(Unit.DEGREES_C))
			timeReplaceAppend(hello[timeReplaceAppend()][str(preventIndex)]["heartbeat"], avg_bpm)
			'''


			jsonChange("w", hello, jsondircache)
		elif graphactive == True and x < 180:							   # finished drawing full graph width so move each time to make room
			hr = HeartRate(max30105)
			hr.on_beat(storeheartbeat, average_over = 4)

			if y != 0.0 and y != 0:
				window["_GRAPH_"].DrawLine((lastx+2, lasty * 2), (x+2, y * 2), width=1)
				window["_GRAPH_"].Move(-GRAPH_STEP_SIZE, 0)
				amount += 1
				x -= GRAPH_STEP_SIZE
			else:
				sg.popup_timed("HEY! There's an incorrect reading. Make sure to push your fingers against the sensors or check the connections!")
			preventDel()
			print(hello[timeReplaceAppend()])
			'''test only
			timeReplaceAppend(hello[timeReplaceAppend()][str(preventIndex)]["temperature1"], max30105.get_temperature())
			timeReplaceAppend(hello[timeReplaceAppend()][str(preventIndex)]["temperature2"], tempsensor.get_temperature(Unit.DEGREES_C))
			if avg_bpm != 0.0:
				timeReplaceAppend(hello[timeReplaceAppend()][str(preventIndex)]["heartbeat"], avg_bpm)
			'''
			jsonChange("w", hello, jsondircache)
		lastx, lasty = x, y
		x += GRAPH_STEP_SIZE
#	print(graphactive, login, prevval, values["_PROMPT_"])
window.close()