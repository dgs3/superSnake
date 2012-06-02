class ConflictingChromosomeLengthError(Exception):
  """
  A ConflictingChromosomeLengthError is raised during crossover 
  if the two parents have chromosomes of conflicting lengths
  """

class SmallPopulationError(Exception):  """
  A SmallPopulationError is thrown when the EA tries to make a population with one or less individuals
  """

