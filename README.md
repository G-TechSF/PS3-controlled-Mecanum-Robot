# PS3-controlled-Mecanum-Robot
By G-TechSF 2019
README

This python3 script (messenger.py) and companion Arduino .INO sketch 
allow the Nexus 4WD Mecanum robot to be controlled via PS3 controller.
A raspberry pi connected to the robot via USB is used to run messenger.py
Using sixpair, the PS3 controller is paired to the pi via bluetooth
A modified Arduino sketch from Nexus allows the robot to interpret commands
over USB, generated and filtered by messenger.py based on PS3 controller input.

DEPENDENCIES

+ sixpair (For pairing PS3 controller via Bluetooth)
+ python3 (For the client side)
+ PyCmdMessenger and pygame (use pip3 to install)

INSTALL

+ Pair PS3 controller with the pi

+ Connect USB A-B cable to USB port on robot !DO NOT SUPPLY MOTOR POWER!

+ Use Arduino IDE to upload .INO sketch to robot. !ONLY FOR NEXUS 4WD MECANUM ROBOT!
  + Under Tools->Board, use: Arduino Duemilanove or Diecimila
  + Under Processor, use: ATmega328P
  + Under Port, click /dev/ttyUSB0 or /dev/ttyUSB1 - take note of which USB is listed
  + Click Sketch -> Upload, wait for compile and upload to complete with no errors.

+ Check messenger.py to make sure correct /dev/ttyUSB is declared

+ Make sure PS3 controller is turned on and paired

TO RUN
+ In terminal or shell run: python3 messenger.py
