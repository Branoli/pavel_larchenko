from math import fabs


class Individual:

    def __init__(self, list_chromosome):

        self.list_correct_chromosomes = []
        self.genotype = ""
        self.fit = 0
        self.count_correct_chromosome = 0

        self._search_correct_chromosome(list_chromosome)
        self._create_genotype(list_chromosome)

        self.target_function = self.count_correct_chromosome / 8

    def _search_correct_chromosome(self, list_chromosome):
        for i in range(len(list_chromosome)):
            check = True
            for j in range(len(list_chromosome)):
                if list_chromosome[j] != list_chromosome[i] \
                        and i != j \
                        and fabs(int(list_chromosome[j], 2) - int(list_chromosome[i], 2)) == fabs(j - i):
                    check = False
                    break
                elif list_chromosome[j] == list_chromosome[i] and i != j:
                    check = False
                    break
            if check:
                self.count_correct_chromosome = self.count_correct_chromosome + 1
                self.list_correct_chromosomes.append(list_chromosome[i])

    def _create_genotype(self, list_chromosome):
        for i in range(len(list_chromosome)):
            self.genotype = self.genotype + list_chromosome[i]
