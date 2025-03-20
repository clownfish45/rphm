1. Get a raspberry pi 4 and following parts: https://thepihut.com/products/3-2-ips-hdmi-lcd-display-for-raspberry-pi-480x800 , https://thepihut.com/products/max30105-breakout-heart-rate-oximeter-smoke-sensor , https://thepihut.com/products/camjam-edukit-2-sensors, https://thepihut.com/products/gpio-ribbon-cable-for-raspberry-pi-model-a-b-pi-2-pi-3, https://thepihut.com/products/basic-fingerprint-sensor-with-socket-header-cable, Solder the headers onto the max30101 sensor

2. 3D Print the 3D models named rphm_model.stl, put the max30101 sensor into the flat 3d printed sensor holder. Put the two buttons into holders with a wall inside

3. Attach the ribbon to the gpio headers on the raspberrypi 4 model b. File down the connector connected to the raspberry pi and mount the display. Screw the display onto the 3D printed plate and install the plate into the main box. Install raspberry pi os on an sd card and insert it inside the raspberry pi. Make sure the os works. Male a user called theapplepi. In the terminal run the following command: "sudo apt-get install python3 python3-pip"

4. Click on the raspberry pi logo at the top left of your desktop. Then click on preferences and then click on raspberry pi configuration. Go to interfaces, and enable spi, i2c, serial port and 1-wire. Reboot

5. Download the software from https://www.github.com/clownfish45/theApplePi/tree/main , create a folder named "theApplePi" in the "Documents" folder and put the software there. Then open the terminal, and type “pip install -r /home/theapplepi/Documents/theApplePi/requirements.txt --break-system-packages”

6. Switch off the raspberrypi. Put the sensors and two buttons on the 3d printed board in this order for right-handed people - fingerprint sensor, button, button, max30101. Using the pinout document, connect the wires of the sensors and buttons to respective pins on the ribbon cable as outlined in PINOUT.md using the wires from the camjam edukit.

7. Switch on the raspberrypi. Go into terminal and type "sudo nano /etc/xdg/autostart/display.desktop". Paste in the following: 
[Desktop Entry]
Name=RPHM
Exec=/usr/bin/python3 /home/theapplepi/Documents/theApplePi/start.py

8. Connect the display connector to the onboard screen and reboot

9. Once rebooted, the app should run on startup. Then put your thumb on the fingerprint reader, and the main app should start working. You can navigate the menu using the two buttons - one makes the selection go up, other goes down. Long click on either will press a button.
