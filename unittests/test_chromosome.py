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

  def test_in_chromosome(self):
    inChrom = {
        'theta_1' : -1,
        'theta_2' : -1,
        }
    chrom = OroBot.Chromosome(inChrom)
    self.assertEqual(chrom.chromosome, inChrom)

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
        'theta_1'   :   0
        }
    self.assertFalse(self.c.isEqual(p))

  def test_is_equal_extra_chromosome(self):
    p = OroBot.Chromosome()
    p.chromosome['theta_3'] = 0
    self.assertFalse(self.c.isEqual(p))

  def test_is_equal_unequal_loci(self):
    p = OroBot.Chromosome()
    p.chromosome['theta_1'] = 90
    self.assertFalse(self.c.isEqual(p))

  def test_is_equal(self):
    p = OroBot.Chromosome()
    self.assertTrue(self.c.isEqual(p))

  def test_mutate(self):
    curChromosome = copy.deepcopy(self.c.chromosome)
    self.c.mutate()
    totalDifference = 0
    for key in curChromosome:
      if curChromosome[key] != self.c.chromosome[key]:
        totalDifference += 1
    self.assertEqual(totalDifference, 1)

  def test_randomize(self):
    curChrom = copy.deepcopy(self.c.chromosome)
    self.c.randomize()
    for key in self.c.chromosome:
        self.assertNotEqual(
            self.c.chromosome[key], 
            curChrom[key],
            )

if __name__ == '__main__':
  unittest.main()
