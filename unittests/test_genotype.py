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

  def test_mutate(self):
    chromosomes = copy.deepcopy(self.g.chromosomes)
    self.assertEqual(chromosomes,self.g.chromosomes)
    self.g.mutate()
    self.assertNotEqual(chromosomes, self.g.chromosomes)

  def test_cross_over_parent_has_no_genotype(self):
    p = OroBot.Genotype()
    p.chromosomes = None
    self.assertRaises(TypeError, self.g.crossOver, p)

  def test_cross_over_parent_short_chromosome(self):
    p = OroBot.Genotype()
    p.chromosomes['theta_1'] = [0, 0]
    self.assertRaises(IndexError, self.g.crossOver, p)

  def test_cross_over_parent_missing_chromosomes(self):
    p = OroBot.Genotype()
    p.chromosomes = {
        'theta_1'     :     [0, 0, 0],
        'theta_2'     :     [0, 0, 0],
        }
    self.assertRaises(KeyError, self.g.crossOver, p)

  def test_cross_over(self):
    p = OroBot.Genotype()
    p.chromosomes = {
        'theta_1'     :     [60, 60, 60],
        'interval'    :     [1000, 1000, 1000],
        'theta_2'    :     [60, 60, 60],
        }
    child = self.g.crossOver(p)
    fromG = 0
    fromP = 0 
    for key in child.chromosomes:
      for i in range(len(child.chromosomes[key])):
        if child.chromosomes[key][i] == self.g.chromosomes[key][i]:
          fromG += 1
        elif child.chromosomes[key][i] == p.chromosomes[key][i]:
          fromP += 1
        else:
          self.assertTrue(False)
    totalLoci = 0
    for key in self.g.chromosomes:
      totalLoci += len(self.g.chromosomes[key])
    self.assertTrue(abs(fromG-fromP) <= 1)


if __name__ == '__main__':
  unittest.main()
