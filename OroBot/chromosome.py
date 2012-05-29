import random
import copy

class Chromosome(object):

  def __init__(self, inChromosome = None):
    if inChromosome == None:
      self.chromosome = {
          'theta_1'     :     [0, 0, 0],
          'interval'    :     [0, 0, 0],
          'theta_2'     :     [0, 0, 0], 
          }
    else:
      self.chromosome = copy.deepcopy(inChromosome)
    self.fitness = 0
    self.clampMap = {
        'theta_1'     :     [60, 60, 60],
        'interval'    :     [1000, 1000, 1000],
        'theta_2'    :     [60, 60, 60], 
        }

  def mutate(self):
    """
    Mutates one random loci on one random chromosome 
    Uses the clampMap to get upper bounds
    """
    mutKey = random.choice(self.chromosome.keys())
    loci = random.randint(
        0, 
        len(self.chromosome[mutKey])-1
        )
    self.chromosome[mutKey][loci] = random.randint(0, self.clampMap[mutKey][loci])


  def isEqual(self, p):
    return self.chromosome == p.chromosome

  def copy(self):
    copyChrom = copy.deepcopy(self.chromosome)
    return Chromosome(copyChrom)
