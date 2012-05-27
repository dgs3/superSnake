import serial
import time
import sys
import OroBot

s = serial.Serial('/dev/tty.usbserial-A7006Qhs', '115200', timeout=.5)
time.sleep(2)
print s.readline()
s.write(str(OroBot.actionDict['setServoVelocity'])+', 0, 180, 5000')
#print s.readline()
#time.sleep(2)
#s.write(str(OroBot.actionDict['setServoVelocity'])+', 0, 180, 5')
