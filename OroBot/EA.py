from genotype import *

class EA(object):
  def __init__(self, popSize, numServos):
    self.popSize = popSize
    self.pop = []
    self.numServos = numServos  
 
  def seedPop(self):
    self.pop = [Genotype(self.numServos) for i in range(self.popSize)] 

#  def makePop(self):
#    while len(self.pop) < self.popSize:
#      child = 

  def childInPop(self, child):
    for member in self.pop:
      if member.isEqual(child):
        return True
    return False

  def getIndividuals(self, number):
    if number > len(self.pop):
      raise ValueError
    elif number == len(self.pop):
      return self.pop
    else:
      indivs = []
      indivs.append(random.choice(self.pop))
      while len(indivs) < number:
        g = random.choice(self.pop)
        goodPick = True
        for i in indivs:
          if i.isEqual(g):
            goodPick = False
        if goodPick:
          indivs.append(g)

