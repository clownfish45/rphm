import os
import sys
import RPi.GPIO as GPIO
import time
import serial




Finger_WAKE_Pin   = 23
Finger_RST_Pin    = 24



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(Finger_WAKE_Pin, GPIO.IN)  
GPIO.setup(Finger_RST_Pin, GPIO.OUT, initial=GPIO.HIGH)


ser = serial.Serial("/dev/ttyS0", 19200)

while True:
    GPIO.output(Finger_RST_Pin, GPIO.LOW)
    if GPIO.input(Finger_WAKE_Pin) == 1:
        os.system("lxterminal -e python3 /home/theapplepi/Documents/theApplePi/main_alphav2.py")
        sys.exit()
    time.sleep(0.5)