import unittest2 as unittest
import serial
import time

import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import OroBot

class ArduinoTestInit(unittest.TestCase):
  def setUp(self):
    self.s = serial.Serial('/dev/tty.usbserial-A7006Qhs', '115200', timeout=.5)
    time.sleep(5)

  def tearDown(self):
    self.s = None

  def test_init(self):
    response = self.s.readline()
    self.assertEqual(OroBot.errorDict['kARDUINO_READY'], int(response[0]))


class ArduinoTest(unittest.TestCase):

  def setUp(self):
    self.s = serial.Serial('/dev/tty.usbserial-A7006Qhs', '115200', timeout=.5)
    time.sleep(5)
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
    cmd = '4;'
    self.s.write(cmd)
    response = self.s.readline()
    self.assertEqual(OroBot.errorDict['kERR'], int(response[0]))

  def test_set_servo_position_no_theta(self):
    cmd = '4,0;'
    self.s.write(cmd)
    response = self.s.readline()
    self.assertEqual(OroBot.errorDict['kERR'], int(response[0]))

  def test_set_servo_position_no_time(self):
    cmd = '4,0,0;'
    self.s.write(cmd)
    response = self.s.readline()
    self.assertEqual(OroBot.errorDict['kERR'], int(response[0]))

  def test_set_servo_position(self):
    cmd = '4,0,1,2;'
    self.s.write(cmd)
    response = self.s.readline()
    self.assertEqual(OroBot.errorDict['kACK'], int(response[0]))
    self.assertEqual('0', response[2])
    self.assertEqual('1', response[4])
    self.assertEqual('2', response[6])

if __name__ == "__main__":
  unittest.main()
    

