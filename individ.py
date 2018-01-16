from math import fabs


class Individual:

    def __init__(self, list_chromosome):

        self.chromosomes = list_chromosome
        self.correct_chromosomes = []
        self.genotype = ""
        self.fit = 0
        self.count_correct_chromosome = 0

        self._search_currect_chromosome()
        self._create_genotype()
        print(self.genotype)

    def _search_currect_chromosome(self):
        for i in range(len(self.chromosomes)):
            check = True
            for j in range(len(self.chromosomes)):
                if self.chromosomes[j] != self.chromosomes[i] and i != j:
                    if round(fabs(int(self.chromosomes[j], 2) - int(self.chromosomes[i], 2))) == round(fabs(j - i)):
                        check = False
                        break
                elif i != j:
                    check = False
                    break
            if check:
                self.count_correct_chromosome = self.count_correct_chromosome + 1
                self.correct_chromosomes.append(self.chromosomes[i])

    def _create_genotype(self):
        for i in range(len(self.chromosomes)):
            self.genotype = self.genotype + self.chromosomes[i]

    def get_correct_chromosome(self):
        return self.count_correct_chromosome

    def get_list_currect_cromosome(self):
        return self.correct_chromosomes

    def get_list_chromosome(self):
        return self.chromosomes

    def get_fit(self):
        return self.fit

    def get_genotype(self):
        return self.genotype

    def search_fit(self, individuals):
        summ_fit = 0
        for i in range(len(individuals)):
            summ_fit = summ_fit + individuals[i].get_correct_chromosome()
        self.fit = self.count_correct_chromosome / summ_fit

