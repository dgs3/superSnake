import unittest2 as unittest
import time

import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import OroBot

class TestEA(unittest.TestCase):

  def setUp(self):
    self.popSize = 10
    self.numServos = 2
    self.ea = OroBot.EA(self.popSize, self.numServos)

  def tearDown(self):
    self.ea = None

  def test_seed_pop(self):
    self.assertTrue(len(self.ea.pop) == 0)
    self.ea.seedPop()
    self.assertTrue(len(self.ea.pop) == self.ea.popSize)

  def test_make_pop(self):
    self.ea.pop[0] = Genotype(1)
    self.ea.pop[1] = Genotype(1)
    self.ea.makePop()
    self.assertEqual(len(self.ea.pop), self.ea.popSize)
    for i in range(self.ea.popSize):
      for j in range(i+1, self.ea.popSize):
        self.assertNotTrue(self.ea.pop[i].isEqual(self.ea.pop[j]))

  def test_make_pop_one_or_less_members(self):
    self.ea.pop = []
    self.assertRaises(OroBot.SmallPopulationError, self.ea.makePop)

  def test_child_in_pop_duplicate_child(self):
    self.ea.seedPop()
    self.assertTrue(self.ea.childInPop(self.ea.pop[0]))

  def test_child_in_pop_not_in_pop(self):
    self.ea.seedPop()
    newChild = OroBot.Genotype(self.numServos)
    for chromosome in newChild.chromosomes:
      chromosome.randomize()
    self.assertFalse(self.ea.childInPop(newChild))

  def test_get_individuals_zero(self):
    self.assertEqual([], self.ea.getIndividuals(0))

  def test_get_individuals_value_error(self):
    self.ea.pop = [mock.Mock(OroBot.Genotype)]
    self.assertRaises(ValueError, self.ea.getIndividuals, 2)

  def test_get_individuals_three(self):
    indivs = self.ea.GetIndividuals(3)
    for i in range(len(indivs)):
      self.assertTrue(indivs[i] in self.ea.pop)
      for j in range(i+1, 3):
        self.assertFalse(indivs[i].isEqual(indivs[j]))

if __name__ == "__main__":
  unittest.main() 
