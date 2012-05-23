import serial
import time
import sys

s = serial.Serial('/dev/tty.usbserial-A7006Qhs', '115200', timeout=.5)

thetas = [0, 45, 90, 135, 180]
while True:
  for theta in thetas:
    payload = "4,9,"+str(theta)+";"
    #s.write(payload.encode('ascii'))
    s.write(payload)
    s.flush()
    time.sleep(.5)
    sys.stdout.write('.')
  print "reversing"
  thetas.reverse()
  
