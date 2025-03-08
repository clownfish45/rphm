from gpiobuttons2n1 import *# test only
from variables import *
from threading import Thread
from random import randint
import dictdatabase as DDB
import sys

print("\n\n\n\n new")
#test only
Thread(target = gpioengine1, daemon = True).start()
Thread(target = gpioengine2, daemon = True).start()
#Thread(target = getheart, daemon = True).start()

menu(menu3)
#window.TKroot["cursor"] = "none"
while True:							 # Event Loop
	event, values = window.read(timeout = delay)
	if newfile == False:
		'''
		trytuple[0] = hello
		trytuple[1] = preventIndex
		'''
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
			vs.userNum = userNum

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
				menu(menu1)
				login = True
				dbval = DDB.at("log").read()
				userNum = vs.userNum
			else:
				vs.err = False
				vs.userNum = 0
				window["_LOGIN1_"].update("Could not create a user!")
				window.refresh()
				vs.finishedTask = False
		elif DDB.at("log").read()["userquantity"] >= maxUserCount:
			window["_LOGIN1_"].update(f"User limit reached: {maxUserCount}")
			window.refresh()
		else:
			dbval = DDB.at("log").read()
			userNum = int(dbval["lastuser"]) + 1
			print(f"\nusernum at creation = {userNum}\n")
			vs.userNum = userNum

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
				menu(menu1)
				login = True
				userNum = vs.userNum
			else:
				vs.err = False
				time.sleep(0.5)
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
			print("The key does not exist! line 186 main alpha")

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
		#stop = True
		menu(menuSelect)
		stopgraph = False
		print(userNum, "usernum at graphstart\n\n")

		'''
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
		'''
	elif event == "_TEMP_":
		graphactive = True
		preventDel()
		menu(menu2)
		scale()
		readmode = "temperature"
		graph_avg = 0
		delay = 500

	elif event == "_HR_":
		graphactive = True
		preventDel()
		menu(menu2)
		scale()
		readmode = "heartbeat"
		graph_avg = 0
		delay = 500

	elif event == "_BLOODOXYGEN_":
		graphactive = True
		preventDel()
		menu(menu2)
		scale()
		readmode = "bloodoxygen"
		graph_avg = 0
		delay = 500

	elif event == "_SELBACK_":
		menu(menu1)

	elif event == "_ALL_":
		graphactive = True
		preventDel()
		menu(menu2)
		scale()
		readmode = "all"
		temp_avg = 0
		hr_avg = 0
		bloodoxygen_avg = 0
		delay = 500
		allgraph = True

	elif event == "_COHEREBUTTON_":
		ai = True
		delay = 500

	elif ai == True:
		if once == True:
			menu(menuai)
			'''
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
			'''
			dbval = DDB.at("log").read()
			try:
				temp = dbval[str(userNum)]["temperature"][dateToday()]
				hr = dbval[str(userNum)]["heartbeat"][dateToday()]
				bloodoxygen = dbval[str(userNum)]["bloodoxygen"][dateToday()]
				response = co.generate(
					prompt = f"The latest temperature mesurements of my body in degrees C were {temp}. \
					The heartbeat rate per minute were {hr}\
					The blood oxygen concentration was {bloodoxygen}\
					What are your opinions on the temperatures and what do you\
					suggest the person should do to improve them? Also, what are your opinions on the heartbeat of the person? Answer in one sentence",
				)
				response = list(response)
				coheretext = str(response[0])
				print(coheretext)
				
				#window["_COHERE_"].update(coheretext)
				sg.popup_timed(coheretext)
				once = False
			except:
				print(dbval)
				sg.popup_timed("WARNING! You have not taken a reading of all your statistics today! Please take a reading and choose the 'read all' option")
				once = False
				

		if event == "_COHEREBACK_":
			once = True
			ai = False
			menu(menu1)	

	elif graphactive == True:
		if event == "_BACK_":
			allgraph = False
			
			print(x)
			if x < 180:
				if amount != 0:
					window["_GRAPH_"].Move(GRAPH_STEP_SIZE * amount, 0)
					amount = 0
				window["_GRAPH_"].erase()

				#stop = True
			else:
				dbval = DDB.at("log").read()
				dbval[str(userNum)][readmode][dateToday()] = round(graph_avg, 2)

				os.remove(f"{DDB.config.storage_directory}log.json")
				DDB.at("log").create(dbval)
				#stop = True
			graphactive = False


			lastx = lasty = y = x = 0
			preventIndex += 1
			#jsonChange("w", hello, jsondircache)
			menu(menu1)
		if x >= 180 and allgraph == False:
			if amount != 0:
				window["_GRAPH_"].Move(GRAPH_STEP_SIZE * amount, 0)
				amount = 0
			else:
				window["_GRAPH_"].erase()   #finsih!!!!
				window["_READMODE_"].update("DONE!")
				window["_STATS_"].update("press 'go back'")
				x = 9999
				#readmode = ""
			#jsonChange("w", hello, jsondircache)
		elif x>=180 and allgraph == True:
			if amount != 0:
				window["_GRAPH_"].Move(GRAPH_STEP_SIZE * amount, 0)
				amount = 0
			else:
				window["_GRAPH_"].erase()
				graphStage+=1
				lastx = lasty = x = y = 0
				#readmode = ""

		'''
		if event == "_READING_":
			pos = readmodes.index(readmode)
			if pos == 2:
				readmode = readmodes[0]
			else:
				readmode = readmodes[pos + 1]
		'''
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

		if readmode == "temperature" and x != 9999:
			allgraph = False
			#y = randint(20,100)
			y = round(max30105.get_temperature(), 2) + 5
			if graph_avg == 0:
				graph_avg += y
			else:
				graph_avg = (graph_avg + y)/2
			window["_STATS_"].update(f"current:{round(y, 2)}, average:{round(graph_avg, 2)}")
			window["_READMODE_"].update("temperature") #test only
			window.refresh()

		elif readmode == "heartbeat" and x != 9999:
			allgraph = False
			#y = randint(20,100)
			y = read_hr()
			if y == -1:
				window["_STATS_"].update("bad reading: press your finger against the sensor and/or clean the surfaces!")
				window.refresh()
			else:
				if graph_avg == 0:
					graph_avg += y
				else:
					graph_avg = (graph_avg + y)/2
				window["_STATS_"].update(f"current:{round(y, 2)}, average:{round(graph_avg, 2)}")
				window["_READMODE_"].update("heart rate") #test only
				window.refresh()

		elif readmode == "bloodoxygen" and x != 9999:
			allgraph = False
			#y = randint(20,100)
			y = read_bloodoxygen()
			if y == -1:
				window["_STATS_"].update("bad reading: press your finger against the sensor and/or clean the surfaces!")
				window.refresh()
			else:
				if graph_avg == 0:
					graph_avg += y
				else:
					graph_avg = (graph_avg + y)/2
				window["_STATS_"].update(f"current:{round(y, 2)}, average:{round(graph_avg, 2)}")
				window["_READMODE_"].update("blood oxygen") #test only
				window.refresh()
		
		elif readmode == "all":
			if graphStage == 0:
				#y = randint(20,100)
				y = round(max30105.get_temperature(), 2) + 5
				if temp_avg == 0:
					temp_avg += y
				else:
					temp_avg = (temp_avg + y)/2
				window["_STATS_"].update(f"current:{round(y, 2)}, average:{round(temp_avg, 2)}")
				window["_READMODE_"].update("temperature") #test only
				window.refresh()
			elif graphStage == 1:
				#y = randint(20,100)
				y = read_hr()
				if y == -1:
					window["_STATS_"].update("bad reading: press your finger against the sensor and/or clean the surfaces!")
					window.refresh()
				else:
					if hr_avg == 0:
						hr_avg += y
					else:
						hr_avg = (hr_avg + y)/2
					window["_STATS_"].update(f"current:{round(y, 2)}, average:{round(hr_avg, 2)}")
					window["_READMODE_"].update("heart rate") #test only
					window.refresh()
			elif graphStage == 2:
				#y = randint(20,100)
				y = read_bloodoxygen()
				if y == -1:
					window["_STATS_"].update("bad reading: press your finger against the sensor and/or clean the surfaces!")
					window.refresh()
				else:
					if bloodoxygen_avg == 0:
						bloodoxygen_avg += y
					else:
						bloodoxygen_avg = (bloodoxygen_avg + y)/2
					window["_STATS_"].update(f"current:{round(y, 2)}, average:{round(bloodoxygen_avg, 2)}")
					window["_READMODE_"].update("blood oxygen") #test only
					window.refresh()
			elif graphStage == 3:
				dbval = DDB.at("log").read()
				dbval[str(userNum)]["temperature"][dateToday()] = round(temp_avg, 2)
				dbval[str(userNum)]["heartbeat"][dateToday()] = round(hr_avg, 2)
				dbval[str(userNum)]["bloodoxygen"][dateToday()] = round(bloodoxygen_avg, 2)
				os.remove(f"{DDB.config.storage_directory}log.json")
				DDB.at("log").create(dbval)
				bloodoxygen_avg = temp_avg = hr_avg = 0
				window["_READMODE_"].update("DONE!")
				window["_STATS_"].update("press 'go back'")
				x = 190

		if x < GRAPH_SIZE[0] and graphactive == True and x < 180:			   # if still drawing initial width of graph
			''' test only
			hr = HeartRate(max30105)
			hr.on_beat(storeheartbeat, average_over = 4)
			'''
			#hr = randint(80,120)

			if y != 0.0 and y != 0:
				window["_GRAPH_"].DrawLine((lastx+2, lasty * 2), (x+2, y * 2), width=1)
				window.refresh()
				amount += 1
			else:
				pass

			'''
			print(preventDel())
			preventDel()
			print(hello[timeReplaceAppend()])
			'''
			'''test only
			timeReplaceAppend(hello[timeReplaceAppend()][str(preventIndex)]["temperature1"], max30105.get_temperature())
			timeReplaceAppend(hello[timeReplaceAppend()][str(preventIndex)]["temperature2"], tempsensor.get_temperature(Unit.DEGREES_C))
			timeReplaceAppend(hello[timeReplaceAppend()][str(preventIndex)]["heartbeat"], avg_bpm)
			'''


			#jsonChange("w", hello, jsondircache)
		elif graphactive == True and x < 180:							   # finished drawing full graph width so move each time to make room
			#hr = HeartRate(max30105) <--test only
			#hr.on_beat(storeheartbeat, average_over = 4) <---test only

			if y != 0.0 and y != 0:
				window["_GRAPH_"].DrawLine((lastx+2, lasty * 2), (x+2, y * 2), width=1)
				window["_GRAPH_"].Move(-GRAPH_STEP_SIZE, 0)
				window.refresh()
				amount += 1
				x -= GRAPH_STEP_SIZE
			else:
				pass
			preventDel()
			print(hello[timeReplaceAppend()])
			'''test only
			timeReplaceAppend(hello[timeReplaceAppend()][str(preventIndex)]["temperature1"], max30105.get_temperature())
			timeReplaceAppend(hello[timeReplaceAppend()][str(preventIndex)]["temperature2"], tempsensor.get_temperature(Unit.DEGREES_C))
			if avg_bpm != 0.0:
				timeReplaceAppend(hello[timeReplaceAppend()][str(preventIndex)]["heartbeat"], avg_bpm)
			'''
			#jsonChange("w", hello, jsondircache)
		lastx, lasty = x, y
		x += GRAPH_STEP_SIZE
#	print(graphactive, login, prevval, values["_PROMPT_"])
window.close()