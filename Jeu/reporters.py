from __future__ import division, print_function
import time

from neat.reporting import BaseReporter
from neat.math_util import mean, stdev
from neat.six_util import itervalues, iterkeys


class VarReporter(BaseReporter):

    def __init__(self, show_species_detail, root, queue):

        self.pre_texte, self.post_texte, self.end_texte = "", "", ""

        self.show_species_detail = show_species_detail
        self.generation = None
        self.generation_start_time = None
        self.generation_times = []
        self.num_extinctions = 0

        self.queue = queue
        self.root = root

    def start_generation(self, generation):
        self.generation = generation
        self.pre_texte = ' ****** Running generation {0} ****** '.format(generation)
        self.generation_start_time = time.time()

        try:
            self.queue.put(self.pre_texte)
            self.root.event_generate('<<PreTextChanged>>', when='tail')
        except:
            print('error')

    def end_generation(self, config, population, species_set):
        ng = len(population)
        ns = len(species_set.species)
        if self.show_species_detail:
            self.end_texte = 'Population of {0:d} members in {1:d} species:\n'.format(ng, ns)
            sids = list(iterkeys(species_set.species))
            sids.sort()
            self.end_texte += "   ID   age  size  fitness  adj fit  stag\n"
            self.end_texte += "  ====  ===  ====  =======  =======  ====\n"
            for sid in sids:
                s = species_set.species[sid]
                a = self.generation - s.created
                n = len(s.members)
                f = "--" if s.fitness is None else "{:.1f}".format(s.fitness)
                af = "--" if s.adjusted_fitness is None else "{:.3f}".format(s.adjusted_fitness)
                st = self.generation - s.last_improved
                self.end_texte += "  {: >4}  {: >3}  {: >4}  {: >7}  {: >7}  {: >4}\n".format(sid, a, n, f, af, st)
        else:
            self.end_texte = 'Population of {0:d} members in {1:d} species\n'.format(ng, ns)

        elapsed = time.time() - self.generation_start_time
        self.generation_times.append(elapsed)
        self.generation_times = self.generation_times[-10:]
        average = sum(self.generation_times) / len(self.generation_times)
        self.end_texte += 'Total extinctions: {0:d}\n'.format(self.num_extinctions)
        if len(self.generation_times) > 1:
            self.end_texte += "Generation time: {0:.3f} sec ({1:.3f} average)\n".format(elapsed, average)
        else:
            self.end_texte += "Generation time: {0:.3f} sec".format(elapsed)

        try:
            self.queue.put(self.end_texte)
            self.root.event_generate('<<EndTextChanged>>', when='tail')
        except:
            print('error')

    def post_evaluate(self, config, population, species, best_genome):
        fitnesses = [c.fitness for c in itervalues(population)]
        fit_mean = mean(fitnesses)
        fit_std = stdev(fitnesses)
        best_species_id = species.get_species_id(best_genome.key)
        self.post_texte = 'Population\'s average fitness: {0:3.5f} stdev: {1:3.5f}\n'.format(fit_mean, fit_std)
        self.post_texte += 'Best fitness: {0:3.5f} - size: {1!r} - species {2} - id {3}\n'.format(best_genome.fitness, best_genome.size(),
                                                                                   best_species_id, best_genome.key)
        try:
            self.queue.put(self.post_texte)
            self.root.event_generate('<<PostTextChanged>>', when='tail')
        except:
            print('error')

    def complete_extinction(self):
        self.num_extinctions += 1
        self.post_texte += 'All species extinct.\n'

        self.post_var.set(self.post_texte)

    def found_solution(self, config, generation, best):
        self.post_texte += '\nBest individual in generation {0} meets fitness threshold - complexity: {1!r}\n'.format(
            self.generation, best.size())

        self.post_var.set(self.post_texte)

    def species_stagnant(self, sid, species):
        if self.show_species_detail:
            self.post_texte += "\nSpecies {0} with {1} members is stagnated: removing it\n".format(sid, len(species.members))
            self.post_var.set(self.post_texte)

    def info(self, msg):
        #print(msg)
        pass
