import time
import serial
import adafruit_fingerprint


uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

def get_fingerprint():
    """Get a finger print image, template it, and see if it matches!"""
    print("Waiting for image...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Searching...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True


def get_fingerprint_detail():
    """Get a finger print image, template it, and see if it matches!
    This time, print out each error instead of just returning on failure"""
    #print("Getting image...", end="")
    window["_LOGIN1_"].update(values = "Scanning the finger...")
    i = finger.get_image()
    if i == adafruit_fingerprint.OK:
        pass
        #print("Image taken")
    else:
        if i == adafruit_fingerprint.NOFINGER:
            #print("")
            window("_LOGIN1_").update(text = "No finger detected")
        elif i == adafruit_fingerprint.IMAGEFAIL:
            #print("Imaging error")
            window("_LOGIN1_").update(text = "Imaging error")
        else:
            window("_LOGIN1_").update(text = "Unknown error!")
            #print("Other error")
        return False

    #print("Templating...", end="")
    i = finger.image_2_tz(1)
    if i == adafruit_fingerprint.OK:
        #print("Templated")
        pass
    else:
        if i == adafruit_fingerprint.IMAGEMESS:
            print("Image too messy")
            window("_LOGIN1_").update(text = "Image distorted! Clean the sensor and or your hands!")
        elif i == adafruit_fingerprint.FEATUREFAIL:
            print("Could not identify features")
            window("_LOGIN1_").update(text = "Could not recognize a human fingerprint.")
        elif i == adafruit_fingerprint.INVALIDIMAGE:
            window("_LOGIN1_").update(text = "Invalid image")
            print("Image invalid")
        else:
            window("_LOGIN1_").update(text = "Unknown error!")
            print("Other error")
        return False

    #print("Searching...", end="")
    i = finger.finger_fast_search()
    # pylint: disable=no-else-return
    # This block needs to be refactored when it can be tested.
    if i == adafruit_fingerprint.OK:
        print("Found fingerprint!")
        window("_LOGIN1_").update(text = f"Found user! (user {i})")
        return True
    else:
        if i == adafruit_fingerprint.NOTFOUND:
            print("No match found")
            window("_LOGIN1_").update(text = "User not found! create a new user or try again!")
        else:
            print("Other error")
            window("_LOGIN1_").update(text = "Unknown error!")
        return False



def enroll_finger(location): #usage: enroll_finger(get_num(finger.library_size))
    """Take a 2 finger images and template it, then store in 'location'"""
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            window["_LOGIN1_"].update("Place your finger on the sensor...")
            print("Place finger on sensor...", end="")
        else:
            time.sleep(0.5)
            print("Place same finger again...", end="")
            window["_LOGIN1_"].update("Place your finger on the sensor again...")

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="")
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                window["_LOGIN1_"].update("Imaging error!")
                time.sleep(0.5)
                return False
            else:
                print("Other error")
                window["_LOGIN1_"].update("Unknown error!")
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
                window["_LOGIN1_"].update("Image too messy! clean your finger and or the sensor")
                time.sleep(0.5)
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("Could not identify features")
                window["_LOGIN1_"].update("Could not identify a finger!")
                time.sleep(0.5)
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
                window["_LOGIN1_"].update("Invalid image!")
                time.sleep(0.5)
            else:
                print("Other error")
                window["_LOGIN1_"].update("Unknown error!")
                time.sleep(0.5)
            return False

        if fingerimg == 1:
            print("Remove finger")
            window["_LOGIN1_"].update("Remove finger")
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
            window["_LOGIN1_"].update("Fingers did not match!")
            time.sleep(0.5)
        else:
            print("Other error")
            window["_LOGIN1_"].update("Unknown error!")
            time.sleep(0.5)
        return False

    print("Storing model #%d..." % location, end="")
    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        print("Stored")
        window["_LOGIN1_"].update("User fingerprint stored!")
        time.sleep(0.5)
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            print("Bad storage location")
            window["_LOGIN1_"].update("Bad storage location!")
            time.sleep(0.5)
        elif i == adafruit_fingerprint.FLASHERR:
            print("Flash storage error")
            window["_LOGIN1_"].update("Flash storage error!")
            time.sleep(0.5)
        else:
            print("Other error")
            window["_LOGIN1_"].update("Unknown error!")
            time.sleep(0.5)
        return False

    return True


def findFinger():
	if get_fingerprint():
		print("Detected #", finger.finger_id)
		return int(finger.finger_id)
	else:
		print("Finger not found")
		return -1
'''
def get_num(max_number):
    """Use input() to get a valid number from 0 to the maximum size
    of the library. Retry till success!"""
    i = -1
    while (i > max_number - 1) or (i < 0):
        try:
            i = int(input("Enter ID # from 0-{}: ".format(max_number - 1)))
        except ValueError:
            pass
    return i
'''
findFinger()