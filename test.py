import serial
import time
import sys
import OroBot

s = serial.Serial('/dev/tty.usbserial-A7006Qhs', '115200', timeout=.5)
time.sleep(2)
print s.readline()
s.write(str(OroBot.actionDict['setServoPosition'])+', 0, 0;')
time.sleep(2)
s.write(str(OroBot.actionDict['setServoPosition'])+', 0, 180;')
