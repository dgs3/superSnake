import unittest2 as unittest

import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import copy
import sets
import OroBot

class GenotypeTest(unittest.TestCase):

  def setUp(self):
    self.g = OroBot.Genotype(2)

  def tearDown(self):
    self.g = None

  def test_copy(self):
    copy = self.g.copy()
    self.assertTrue(self.g.isEqual(copy))

  def test_is_equal_short_chromosomes(self):
    p = OroBot.Genotype(1)
    self.assertFalse(self.g.isEqual(p))

  def test_is_equal(self):
    p = OroBot.Genotype(2)
    self.assertTrue(self.g.isEqual(p))

  def test_mutate(self):
    copy = self.g.copy()
    self.assertTrue(self.g.isEqual(copy))
    self.g.mutate()
    numDifferent = 0
    for gChrom, pChrom in zip(
        self.g.chromosomes,
        copy.chromosomes,
        ):
      if not gChrom.isEqual(pChrom):
        numDifferent += 1 
    self.assertTrue(numDifferent == 1)

  def test_cross_over_parent_has_no_chromosomes(self):
    p = OroBot.Genotype(2)
    p.chromosomes = []
    self.assertRaises(OroBot.ConflictingChromosomeLengthError, self.g.crossOver, p)

  def test_cross_over_parent_has_fewer_chromosomes(self):
    p = OroBot.Genotype(1)
    self.assertRaises(OroBot.ConflictingChromosomeLengthError, self.g.crossOver, p)

  def test_cross_over_parent_short_chromosome(self):
    p = OroBot.Genotype(2)
    p.chromosomes[0].chromosome['theta_1'] = [0, 0]
    self.assertRaises(OroBot.ConflictingChromosomeLengthError, self.g.crossOver, p)

  def test_cross_over_parent_missing_chromosomes(self):
    p = OroBot.Genotype(2)
    p.chromosomes[0].chromosome = {
        'theta_1'     :     [0, 0, 0],
        'theta_2'     :     [0, 0, 0],
        }
    self.assertRaises(OroBot.ConflictingChromosomeLengthError, self.g.crossOver, p)

  def test_cross_over(self):
    p = OroBot.Genotype(2)
    for chromosome in p.chromosomes:
      chromosome.chromosome = {
          'theta_1'     :     [60, 60, 60],
          'interval'    :     [1000, 1000, 1000],
          'theta_2'     :     [60, 60, 60],
          }
    child = self.g.crossOver(p)
    fromG = 0
    fromP = 0  
    for i in range(len(child.chromosomes)):
      for key in child.chromosomes[i].chromosome:
        for j in range(
            len(child.chromosomes[i].chromosome[key])
            ):
          if child.chromosomes[i].chromosome[key][j] == self.g.chromosomes[i].chromosome[key][j]:
            fromG += 1
          elif child.chromosomes[i].chromosome[key][j] == p.chromosomes[i].chromosome[key][j]:
            fromP += 1
          else:
            self.assertTrue(False)
    totalLoci = 0
    for chromosome in child.chromosomes:
      for key in chromosome.chromosome:
        totalLoci += len(chromosome.chromosome[key])
    self.assertTrue(abs(fromG-fromP) <= 1)

if __name__ == '__main__':
  unittest.main()
