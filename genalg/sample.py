import spec
import sonicfeatures
import display

import random
import os

class Sample:
    """Keep track of samples and their stuff."""

    def __init__(self, genotype, gen=0, index=0, parents=None, fitness_func=None):
        self.genotype = genotype
        self.phentype = None
        self.fitness_func = fitness_func
        self.gen = gen
        self.index = index
        self.parents = parents
        self.mutant = False
        self.score = None
        self.rid = None

    @classmethod
    def random_sample(cls, index, randorams, spec, fitness_func=None):
        """A random Sample."""
        # return cls([spec.map_spec(param, random.random()) for i in range(4) for param in randorams], index)
        random_sample = cls([spec.map_spec(param, random.random()) for i in range(4) for param in randorams], 
                            gen=0, 
                            index=index,
                            parents=None,
                            fitness_func=fitness_func)
        random_sample.phenotype = random_sample.to_phenotype(randorams, spec)
        return random_sample

    def to_phenotype(self, randorams, spec):
        """Map genotype [0,1] to through param spec."""
        return [spec.map_spec(param, gene) for gene,param in zip(self.genotype, randorams)]

    def render(self, renderer, filename='sample', verbose=True):
        """Ask rs server to render me."""
        renderer.render(self, filename=filename, verbose=verbose)
        return self

    def render_and_do(self, renderer, do_func, func_args, filename='sample', verbose=True):
        """Render and do do_func upon completion."""
        renderer.render_and_do(self, do_func, func_args, filename, verbose)
        return self

    def render_and_score(self, renderer, filename='sample', verbose=True):
        """Render and score fitness."""
        renderer.render_and_score(self, filename, verbose)
        return self

    def fitness(self, renderer, deleteme=True):
        """Evalute fitness. Assume we are rendered."""
        # print('{0}evaluating fitness: {1}'.format(NW_THRD, self.rid))
        filename = '{0}/{1}.wav'.format(renderer.render_params['foldername'], self.filename)
        fitness = self.fitness_func(filename)
        print('{0}done evaluating fitness: {1}, index: {3} = {2}'.format(display.NOTIFY, self.rid, fitness, self.index))
        # delete file for space 
        if deleteme: os.system('rm "{0}"'.format(filename))
        # do this last cuz triggers stuff
        self.score = fitness
        return self

    def __repr__(self):
        return '<Sample(gen: {0.gen!r}, index: {0.index!r}, rid: {0.rid!r}, score: {0.score!r})>'.format(self)
