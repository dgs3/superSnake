Orobot
==========
Supersnake is an evolvable organism consisting of a set of connected servos with an accelerometer, all connected through an arduino microcontroller.  It is driven by an evolutionary algorithm.
#Genotype
The genotype is used carry the genetic code.  It can also breed with other genotypes via crossover.  It also has the ability to mutate its genome.

##The Chromosomes
The chromosomes are represented by a python dictionary.  Each servo is controlled by an entry which is a list of 6 elements:

'''
First Angle To Move To
Time To Pause For After That Command Is Sent
Second Angle To Move To
'''

##Crossover
Crossover is used to breed with another genome.  It is modeled after biological reproduction; half of one genotype's chromosomes are combined with half of another genotype's chromosomes, forming a new genotype.

The flavor of crossover we incorporate is uniform crossover.  Uniform crossover represents actual sexual reproduction, where one parent's randomly selected gamete is combined with another, forming a new set of chromosomes.

In this case, crossover is done on a per-loci basis, where we look at each element for each dictionary entry, and copy over one of the parent's values.

##Mutation
Mutation is done in a straightforward manner, where a random number of values will be mutated.  Certain values will be clamped:
'''
Angles Are Clamped To 180 degrees
Time To Pause For is clamped to 5000 ms
'''

#Fitness Evaluation
Fitness evaluation is being kept as simple as possible: A genotype's accelerometer value in the forward (X) direction is directly proportional to their fitness.

#The Evolutionary Algorithm
Th/ algorithm is the crux of the whole technique.  It generates a population, sorts that population by fitness, selects organisms to breed, does mutation, assesses fitness, and then culls the population.

##Population Generation
Populations are generated using the two genetic operators of crossover and mutation. First, we select members of the population to cross over.  After crossing over, we can mutate a certain percentage of our population.  Mutation is what helps cover a vast serach space, but too much mutation will turn the EA into a random hill climber.  So, we only want to mutate 1% of our total population.

##Sorting
A population-wise fitness is first assessed, and each individual is given a normalized fitness of 0-1.  Then the entire population is sorted from greatest fitness to least.

##Selection
We use tournament selection to find candidates to breed.  Tournament selection is comprised of two steps:

'''
Randomly Select Three Candidates
Choose the one with the highest fitness
'''

#Talking to the Orobot 
The Orobot is controlled by an Arduino microcontroller, and can be conversed with over a serial port at a baudrate of 115200.  There is essentially only one command it needs to understand, the setServoPosition command.  To give the Orobot a command:
'''
4,servo,theta;
'''
where 4 is the number of the command, servo is the servo we are going to move and theta is angle.  We execute the bot's gate by Setting all servo positions.  Then we set a timer, and set the second position when the servo's timer is elapsed.  We dont start the next move until all second positions are sent.
