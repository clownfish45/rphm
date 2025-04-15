import os
import sys
import RPi.GPIO as GPIO
import time
import serial
import adafruit_fingerprint
from threading import Thread
import pyautogui



dir = "/home/theapplepi/Documents/theApplePi/"

def sleepAndDetect(dir):

    print("whats cooking good lookin")

    menu1 = ["_GRAPHSTART_", "_COHEREBUTTON_", "_DELETE_", "_LOGOUT_"]
    menu2 = ["_READMODE_", "_GRAPHCANVAS_", "_GRAPH_", "_STATS_", "_BACK_"]
    menu3 = ["_LOGIN1_", "_NEWUSER_", "_SIGNIN_", "_EXIT_"]
    menuSelect = ["_TEMP_", "_HR_", "_BLOODOXYGEN_", "_ALL_", "_SELBACK_"]
    menuai = ["_COHERE_", "_COHEREBACK_"]

    uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)
    finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
    sleep = False
    lastmenu = str()
    while True:
        if sleep:
            os.system("xset dpms force off")
            while finger.get_image() != adafruit_fingerprint.OK:
                pass
            if finger.image_2_tz(1) == adafruit_fingerprint.OK:
                sleep = False
                lastmenu = str()
                os.system("xset dpms force on")
            time.sleep(0.1)
        else:
            with open(f"{dir}last/lastmenu.txt", "r") as fo:
                lastmenu = fo.read()
            i = 0
            while i < 61:
                print(i)
                time.sleep(1)
                tempText = str()
                with open(f"{dir}last/lastmenu.txt", "r") as f:
                    tempText = f.read()

                if str(lastmenu) == str(tempText):
                    i = i + 1
                    tempText = str()
                else:
                    i = 0
                    with open(f"{dir}last/lastmenu.txt", "r") as fo:
                        lastmenu = fo.read()
                    tempText = str()
            sleep = True
            time.sleep(0.1)
        time.sleep(0.1)






GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

with open(f"{dir}last/lastmenu.txt", "w") as fo:
    fo.write("") 
tup = tuple(pyautogui.size())
if tup == (480, 800) or tup == (800, 480):
    os.system("xrandr -o right")
#os.system("xrandr -o right")# <---uncomment
#os.system(f"lxterminal -e python3 {dir}main_alphav2.py")
Thread(target = sleepAndDetect, daemon = True, args=(dir,)).start()
os.system(f"python3 {dir}main_release.py")

#sys.exit()