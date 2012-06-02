import unittest2 as unittest

import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import copy
import mock
import sets
import OroBot

class GenotypeTest(unittest.TestCase):

  def setUp(self):
    reload(OroBot)
    self.g = OroBot.Genotype(2)

  def tearDown(self):
    self.g = None

  def test_newChromosomes(self):
    newChromosomes = ['asdf']
    g = OroBot.Genotype(2, newChromosomes)
    self.assertEqual(newChromosomes, g.chromosomes)

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
    toMutate = OroBot.Genotype(1)
    theMock = mock.Mock(OroBot.Chromosome)
    toMutate.chromosomes[0] = theMock
    toMutate.mutate()
    theMock.mutate.assert_called_once_with()

  def test_cross_over_parent_has_no_chromosomes(self):
    p = OroBot.Genotype(2)
    p.chromosomes = []
    self.assertRaises(OroBot.ConflictingChromosomeLengthError, self.g.crossOver, p)

  def test_cross_over_parent_has_fewer_chromosomes(self):
    p = OroBot.Genotype(1)
    self.assertRaises(OroBot.ConflictingChromosomeLengthError, self.g.crossOver, p)


  def test_cross_over_parent_missing_chromosomes(self):
    p = OroBot.Genotype(2)
    p.chromosomes[0].chromosome = {
        'theta_1'     :     0,
        }
    self.assertRaises(OroBot.ConflictingChromosomeLengthError, self.g.crossOver, p)

  def test_cross_over(self):
    p = OroBot.Genotype(2)
    for chromosome in p.chromosomes:
      chromosome.chromosome = {
          'theta_1'     :     p.chromosomes[0].valueMap[-1],
          'theta_2'     :     p.chromosomes[0].valueMap[-1],
          }
    child = self.g.crossOver(p)
    fromG = 0
    fromP = 0  
    for i in range(len(child.chromosomes)):
      for key in child.chromosomes[i].chromosome:
          if child.chromosomes[i].chromosome[key] == self.g.chromosomes[i].chromosome[key]:
            fromG += 1
          elif child.chromosomes[i].chromosome[key] == p.chromosomes[i].chromosome[key]:
            fromP += 1
          else:
            self.assertTrue(False)
    self.assertTrue(abs(fromG-fromP) <= 1)

if __name__ == '__main__':
  unittest.main()
