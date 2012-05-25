import serial
import time
import sys

s = serial.Serial('/dev/tty.usbserial-A7006Qhs', '115200', timeout=.5)
time.sleep(5)
print s.readline()
written = s.write("4,0,0,0;")
print s.readline()
