import random
import copy

class Chromosome(object):

  def __init__(self, inChromosome = None):
    if inChromosome == None:
      self.chromosome = {
          'theta_1'     :     0,
          'theta_2'     :     0, 
          }
    else:
      self.chromosome = copy.deepcopy(inChromosome)
    self.fitness = 0
    self.valueMap = [0, 90, 180]

  def mutate(self):
    """
    Mutates one random loci on one random chromosome 
    Uses the clampMap to get upper bounds
    """
    mutKey = random.choice(self.chromosome.keys())
    self.chromosome[mutKey] = random.choice(self.valueMap)

  def isEqual(self, p):
    return self.chromosome == p.chromosome

  def copy(self):
    copyChrom = copy.deepcopy(self.chromosome)
    return Chromosome(copyChrom)

  def randomize(self):
    for key in self.chromosome:
      self.chromosome[key] = random.choice(self.valueMap)
