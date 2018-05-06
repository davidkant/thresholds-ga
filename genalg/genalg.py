import sample
import display

import random
import pickle
import matplotlib.pyplot as plt

class GeneticAlgorithm:
    """A very simple Genetic Algorithm."""

    def __init__(self, renderer, model):
        self.renderer = renderer
        self.model = model
        self.log = []
        self.gen = 0

    # default functions ----------------------------------------------------------------------

    def random_individual(self, index):
        """Generate a random individual phenotype."""
        return sample.Sample.random_sample(index, self.model.randorams, self.model.spec, self.model.fitness_func)

    def to_weight(self, fitness, m=100, b=1):
        """Convert from fitness score to probability weighting."""
        return int(round(fitness*m + b))

    def reproduce(self, parent1, parent2, index1, index2):
        """Generate offspring using random crossover."""

        # verbose
        print('mating parent {0} + parent {1} -> children {2} and {3}'
              .format(parent1.index, parent2.index, index1, index2))

        # random crossover point
        crossover = random.randrange(0, len(parent1.genotype))

        # construct children
        child1 = sample.Sample(parent1.genotype[0:crossover] + parent2.genotype[crossover:], 
                               gen = parent1.gen + 1, # note: gen comes from parent 1
                               index = index1,
                               parents = [parent1, parent2],
                               fitness_func = self.model.fitness_func) 
        child2 = sample.Sample(parent2.genotype[0:crossover] + parent1.genotype[crossover:], 
                               gen = parent1.gen + 1,
                               index = index2,
                               parents = [parent1, parent2],
                               fitness_func = self.model.fitness_func)

        # return children
        return child1, child2

    def mutate(self, sample, mutation_prob=0.05, inbreeding_prob=0.5):
        """Mutate."""

        # increased mutation prob if parents are the same
        if sample.parents is not None and sample.parents[0].genotype == sample.parents[1].genotype:
            mutation_prob = inbreeding_prob

        if random.random() <= mutation_prob:
            print('*** muuuuutating sample {0}'.format(sample))
            gene_index = random.randrange(len(sample.genotype))
            sample.genotype[gene_index] = random.random() # note: map_spec will clip to [0,1]
            sample.mutant = True
        
        return sample

    # the guts -------------------------------------------------------------------------------

    def initialize_population(self):
        """Initialize the population."""

        # store population size
        self.population_size = self.model.ga_params['population_size']
        # initialize individuals
        self.population = [self.random_individual(i) for i in range(self.population_size)]
        # initialize fitness to 0 for all
        self.fitness = [[0, individual] for individual in self.population]
        return self

    def initialize_population_and_render(self):
        """Initialize and render and score, to be used with evolve once."""

        # initialize population
        self.initialize_population()

        # evaluate fitness over the entire population
        self.renderer.batch_render_single_analysis(self.population, batch_size=self.model.render_params['batch_size'])
        # self.renderer.batch_render(self.population, batch_size=self.model.render_params['batch_size'])
        # print('\n{0}waiting for all samples to be generated and scored\n'. format(display.WAITING)),
        while any([y.score is None for y in self.population]): pass
        print('\n{0}ready for the NEXT generation'.format(display.NOTIFY))
        self.fitness = [(y.score,y) for y in self.population]

        # log it
        self.log.append(self.fitness)
        print('\nthe LOG:')
        print([x[0] for x in self.log[-1]])

        # save it
        self.save(gen=0)

        return self

    def evolve(self, iters=6):
        """Run the GA."""

        # initialize
        self.initialize_population_and_render()
        self.save(gen=0)

        # loop iters
        for i in range(iters):
            self.evolve_once()
            # self.save(gen=i+1)

    def evolve_once(self):
        """Evolve one generation using fitness scores in self.fitness."""

        self.gen = self.gen + 1

        # construct mating pool of probabilities weighted by fitness score
        print('\nmating...')
        mating_pool = reduce(lambda x,y: x+y, [[individual]*self.to_weight(score) 
                                               for (score,individual) in self.fitness])
        # uh oh that'd be bad
        if len(mating_pool) == 0: 
            mating_pool = reduce(lambda x,y: x+y, [[individual]*1 
                                                   for (score,individual) in self.fitness])

        # select population_size/2 pairs of parents from the mating pool
        parents = [(random.choice(mating_pool), random.choice(mating_pool)) 
                   for i in range(self.population_size/2)]

        # generate new offspring from parents
        offspring = reduce(lambda x,y: x+y, [self.reproduce(parent1, parent2, 2*index, 2*index+1) 
                                             for index, (parent1,parent2) in enumerate(parents)])

        # mutate
        map(lambda x: self.mutate(x), offspring)

        # update the population
        self.population = offspring
        
        # evaluate fitness over the entire population
        # self.renderer.batch_render(self.population, batch_size=self.model.render_params['batch_size'])
        self.renderer.batch_render_single_analysis(self.population, batch_size=self.model.render_params['batch_size'])
        # print('\n{0}waiting for all samples to be generated and scored\n'. format(display.WAITING)),
        while any([y.score is None for y in self.population]): pass
        print('\n{0}ready for the NEXT generation'.format(display.NOTIFY))
        self.fitness = [(y.score,y) for y in self.population]

        # log it
        self.log.append(self.fitness)
        print('\nthe LOG')
        print([x[0] for x in self.log[-1]])

        # save it
        self.save(gen=self.gen)

        return self

    def save(self, gen=0):
        """Save current population to disk."""
        # f = open('{0}/data/gen-{1:02d}'.format(self.model.render_params['foldername'], gen), 'wb')
        f = open('{0}/gen-{1:02d}'.format(self.model.render_params['foldername'], gen), 'wb')
        pickle.dump(self.population, f)
        f.close()
        return self
