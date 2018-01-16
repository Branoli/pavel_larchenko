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

    def _search_currect_chromosome(self):
        for i in range(len(self.chromosomes)):
            check = True
            for j in range(len(self.chromosomes)):
                if self.chromosomes[j] != self.chromosomes[i] and i != j:
                    if fabs(int(self.chromosomes[j], 2) - int(self.chromosomes[i], 2)) == fabs(j - i):
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
