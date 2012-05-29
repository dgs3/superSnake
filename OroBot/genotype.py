from constants import *
from chromosome import *
from errors import *
import time
import random
import serial 

class Genotype(object):

  def __init__(self, numChromosomes):
    self.numChromosomes = numChromosomes
    self.chromosomes = [Chromosome() for i in range(numChromosomes)]
    self.fitness = 0

  def mutate(self):
    """
    Mutates one random loci on one random chromosome 
    Uses the clampMap to get upper bounds
    """
    random.choice(self.chromosomes).mutate()

  def crossOver(self, p):
    """
    Crosses over one parent with this genotype.
    We incorporte a uniform crossover function, where each
    parent has a 50% chance to donate any particular loci.
    The end result is a genotype that is half of each
    parent.
    @param genotype p: The other genotype to breed with
    @return genotype g: The newly formed genotype
    """
    if len(self.chromosomes) != len(p.chromosomes):
      raise ConflictingChromosomeLengthError
    newChromosomes = []
    for gChrom, pChrom in zip(
        self.chromosomes, 
        p.chromosomes,
        ):
      if len(gChrom.chromosome) != len(pChrom.chromosome):
        raise ConflictingChromosomeLengthError
      toAdd = {}
      for key in gChrom.chromosome:
        if len(gChrom.chromosome[key]) != len(pChrom.chromosome[key]):
          raise ConflictingChromosomeLengthError
        toAdd[key] = []
        for gVal, pVal in zip(
              gChrom.chromosome[key], 
              pChrom.chromosome[key]
              ):
          toAdd[key].append(random.choice([gVal, pVal]))
      newChromosomes.append(Chromosome(toAdd))
    child = Genotype(self.numChromosomes)
    child.chromosomes = newChromosomes
    return child

  def isEqual(self, p):
    if len(self.chromosomes) != len(p.chromosomes):
      return False
    else:
      for gChrom, pChrom in zip(
          self.chromosomes,
          p.chromosomes
          ):
        if not gChrom.isEqual(pChrom):
          return False
    return True

  def copy(self):
    copyChroms = []
    for chromosome in self.chromosomes:
      copyChroms.append(chromosome.copy())
    copy = Genotype(self.numChromosomes)
    copy.chromosomes = copyChroms
    return copy
