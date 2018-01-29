from math import fabs


class Individual:

    def __init__(self, gray_list_chromosome):

        self.list_correct_chromosomes = []
        self.genotype = ""
        self.fit = 0
        self.count_correct_chromosome = 0
        self.binary_list_chromosome = []

        self._gray_to_binary(gray_list_chromosome)
        self._search_correct_chromosome()
        self._create_genotype(gray_list_chromosome)

        self.target_function = self.count_correct_chromosome / 8

    def _search_correct_chromosome(self):
        for i in range(len(self.binary_list_chromosome)):
            check = True
            for j in range(len(self.binary_list_chromosome)):
                if self.binary_list_chromosome[j] != self.binary_list_chromosome[i] \
                        and i != j \
                        and fabs(int(self.binary_list_chromosome[j], 2) - int(self.binary_list_chromosome[i], 2)) == fabs(j - i):
                    check = False
                    break
                elif self.binary_list_chromosome[j] == self.binary_list_chromosome[i] and i != j:
                    check = False
                    break
            if check:
                self.count_correct_chromosome = self.count_correct_chromosome + 1
                self.list_correct_chromosomes.append(self.binary_list_chromosome[i])

    def _gray_to_binary(self, gray_list_chromosome):
        for i in range(len(gray_list_chromosome)):
            if gray_list_chromosome[i] == "000":
                self.binary_list_chromosome.append("000")
            elif gray_list_chromosome[i] == "001":
                self.binary_list_chromosome.append("001")
            elif gray_list_chromosome[i] == "011":
                self.binary_list_chromosome.append("010")
            elif gray_list_chromosome[i] == "010":
                self.binary_list_chromosome.append("011")
            elif gray_list_chromosome[i] == "110":
                self.binary_list_chromosome.append("100")
            elif gray_list_chromosome[i] == "111":
                self.binary_list_chromosome.append("101")
            elif gray_list_chromosome[i] == "101":
                self.binary_list_chromosome.append("110")
            elif gray_list_chromosome[i] == "100":
                self.binary_list_chromosome.append("111")

    def _create_genotype(self, gray_list_chromosome):
        for i in range(len(gray_list_chromosome)):
            self.genotype = self.genotype + gray_list_chromosome[i]
