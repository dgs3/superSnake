import unittest2 as unittest

import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import copy
import sets
import OroBot

class ChromosomeTest(unittest.TestCase):

  def setUp(self):
    self.c= OroBot.Chromosome()

  def tearDown(self):
    self.c = None

  def test_copy(self):
    copyChrom = self.c.copy()
    self.assertTrue(copyChrom.isEqual(self.c))

  def test_is_equal_other_is_None(self):
    p = OroBot.Chromosome()
    p.chromosome = None
    self.assertFalse(self.c.isEqual(p))

  def test_is_equal_short_chromosome(self):
    p = OroBot.Chromosome()
    p.chromosome = {
        'theta_1'   :   [0, 0, 0],
        'interval'  :   [0, 0, 0],
        }
    self.assertFalse(self.c.isEqual(p))

  def test_is_equal_short_loci(self):
    p = OroBot.Chromosome()
    p.chromosome['theta_1'] = [0, 0]
    self.assertFalse(self.c.isEqual(p))

  def test_is_equal_long_loci(self):
    p = OroBot.Chromosome()
    p.chromosome['theta_1'] = [0, 0, 0, 0]
    self.assertFalse(self.c.isEqual(p))

  def test_is_equal_extra_chromosome(self):
    p = OroBot.Chromosome()
    p.chromosome['theta_3'] = [0, 0, 0]
    self.assertFalse(self.c.isEqual(p))

  def test_is_equal_unequal_loci(self):
    p = OroBot.Chromosome()
    p.chromosome['theta_1'] = [0, 0, 1]
    self.assertFalse(self.c.isEqual(p))

  def test_is_equal(self):
    p = OroBot.Chromosome()
    self.assertTrue(self.c.isEqual(p))

  def test_mutate(self):
    curChromosome = copy.deepcopy(self.c.chromosome)
    self.c.mutate()
    totalDifference = 0
    for key in curChromosome:
      curSet = sets.Set(curChromosome[key])
      newSet = sets.Set(self.c.chromosome[key])
      totalDifference += len(newSet - curSet)
    self.assertEqual(totalDifference, 1)

if __name__ == '__main__':
  unittest.main()
