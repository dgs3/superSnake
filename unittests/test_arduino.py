import unittest2 as unittest
import serial
import time

import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import OroBot


class ArduinoTest(unittest.TestCase):

  def setUp(self):
    self.s = serial.Serial('/dev/tty.usbserial-A7006Qhs', '115200', timeout=.5)
    time.sleep(2)
    self.s.readline()
    
  def tearDown(self):
    self.s = None

  def test_send_garbage(self):
    cmd = '125lah'
    self.s.write(cmd)
    response = self.s.readline()
    self.assertEqual('', response)

  def test_send_command_no_semicolon(self):
    cmd = '0'
    self.s.write(cmd)
    response = self.s.readline()
    self.assertEqual('', response)

  def test_unrecognized_command(self):
    """test sending cmd I probably will never implement""" 
    cmd = '50;'
    self.s.write(cmd)
    response = self.s.readline()
    self.assertEqual(OroBot.errorDict['kERR'], int(response[0]))

  def test_set_servo_position_no_servo(self):
    cmd = str(OroBot.actionDict['setServoVelocity'])+';'
    self.s.write(cmd)
    response = self.s.readline()
    self.assertEqual(OroBot.errorDict['kERR'], int(response[0]))

  def test_set_servo_position_no_theta(self):
    cmd = str(OroBot.actionDict['setServoVelocity'])+',0;'
    self.s.write(cmd)
    response = self.s.readline()
    self.assertEqual(OroBot.errorDict['kERR'], int(response[0]))

  def test_set_servo_position_no_time(self):
    cmd = str(OroBot.actionDict['setServoVelocity'])+',0,0;'
    self.s.write(cmd)
    response = self.s.readline()
    self.assertEqual(OroBot.errorDict['kERR'], int(response[0]))

  def test_set_servo_position(self):
    cmd = str(OroBot.actionDict['setServoVelocity'])+',0,12,7;'
    self.s.write(cmd)
    response = self.s.readline()
    response = response[:-3].split(',')
    self.assertEqual(OroBot.errorDict['kACK'], int(response[0]))
    self.assertEqual('0', response[1])
    self.assertEqual('12', response[2])
    self.assertEqual('7', response[3])

  def test_get_position_no_sevo(self):
    cmd = str(OroBot.actionDict['getPosition'])+';'
    self.s.write(cmd)
    response = self.s.readline()
    self.assertEqual(OroBot.errorDict['kERR'], int(response[0]))

  def test_get_position(self):
    cmd = str(OroBot.actionDict['getPosition'])+',1;'
    self.s.write(cmd)
    response = self.s.readline()
    response = response[:-3].split(',')
    self.assertEqual(OroBot.errorDict['kACK'], int(response[0]))
    self.assertEqual('1', response[1])
    self.assertEqual('0', response[2])

  def test_set_position_no_servo(self):
    cmd = str(OroBot.actionDict['setPosition'])+';'
    self.s.write(cmd)
    response = self.s.readline()
    self.assertEqual(OroBot.errorDict['kERR'], int(response[0]))

  def test_set_position_no_theta(self):
    cmd = str(OroBot.actionDict['setPosition'])+',0,;'
    self.s.write(cmd)
    response = self.s.readline()
    self.assertEqual(OroBot.errorDict['kERR'], int(response[0]))

  def test_set_position(self):
    self.s.write(str(OroBot.actionDict['getPosition'])+',0;')
    getPositionResponse = self.s.readline()
    getPositionResponse = getPositionResponse[:-3].split(',')
    position = int(getPositionResponse[2])
    delta = 42
    newPosition = position+delta
    cmd = str(OroBot.actionDict['setPosition'])+',0,'+str(newPosition)+';'
    self.s.write(cmd)
    response = self.s.readline()
    response = response[:-3].split(',')
    self.assertEqual(OroBot.errorDict['kACK'], int(response[0]))
    self.assertEqual('0', response[1])
    self.assertEqual(str(newPosition), response[2])

  def test_move_servo(self):
    """
    THIS TEST WILL ONLY WORK IF TIMEOUT IS DISABLED ON THE ARDUINO
    """
    #Set Position to 0
    self.s.write(str(OroBot.actionDict['setPosition'])+',0,0;')
    self.s.readline()
    theta = 100
    time = 2
    #Set the servo position with time
    setServoCmd = str(OroBot.actionDict['setServoVelocity'])+',0,'+str(theta) + ',' + str(time) + ';'
    self.s.write(setServoCmd)
    self.s.readline()
    #Move The Servo one tick (one ms)
    self.s.write(str(OroBot.actionDict['moveServos'])+';')
    self.s.readline()
    #Get the position
    timeout = 100
    self.s.write(str(OroBot.actionDict['getPosition'])+',0;')
    getPositionResponse = self.s.readline()
    getPositionResponse = getPositionResponse[:-3].split(',')
    self.assertEqual(str(50*timeout), getPositionResponse[2])

if __name__ == "__main__":
  unittest.main()
    

