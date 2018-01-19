# -*- coding: utf-8 -*-
import random
import individ


class Solver_8_queens:
    '''
    Dummy constructor representing proper interface
    '''
    def __init__(self, pop_size=75, cross_prob=1, mut_prob=1):
        self.pop_size = pop_size
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob
    '''
    Dummy method representing proper interface
    '''

    def solve(self, min_fitness=1, max_epochs=10000):
        pop = self.create_pop()
        self.search_fit(pop)

        count_epochs = 0
        while count_epochs < max_epochs:
            new_pop = self.to_crossing_over(self.create_roulette(pop))
            self.search_fit(new_pop)

            pop.clear()

            pop = self.reduction_new_pop(new_pop)
            self.search_fit(pop)
            pop.sort(key=self.sort_individ_fit)

            count_epochs += 1

            if (pop[self.pop_size - 1].count_correct_chromosome / 8) == min_fitness:
                break

        '''
            Вывод
        '''
        visualization = self.create_visualization(pop[self.pop_size - 1].correct_chromosomes)
        best_fit = min_fitness
        epoch_num = count_epochs

        return best_fit, epoch_num, visualization

    '''
        Геннетический алгоритм
    '''
    def create_pop(self):
        pop = []
        for i in range(self.pop_size):
            individ_list = ['000', '001', '010', '011', '100', '101', '110', '111']
            random.shuffle(individ_list)
            pop.append(individ.Individual(individ_list))
        return pop

    def search_fit(self, pop):
        summ_correcet_chromosome = 0
        for j in range(len(pop)):
            summ_correcet_chromosome = summ_correcet_chromosome + pop[j].count_correct_chromosome
        for i in range(len(pop)):
            pop[i].fit = pop[i].count_correct_chromosome / summ_correcet_chromosome

    def create_roulette(self, pop):
        list_rulet = []
        roulette_fit_start = 0
        for i in range(len(pop)):
            roulette_fit_end = roulette_fit_start
            roulette_fit_start = roulette_fit_start + pop[i].fit
            list_rulet.append((pop[i], (roulette_fit_end, roulette_fit_start)))

        return self.twist_roulette(list_rulet)

    def twist_roulette(self, list_rulet):
        selected_pop = []
        for k in range(self.pop_size):
            select = random.random()
            for i in range(len(list_rulet)):
                if (select >= list_rulet[i][1][0]) and (select < list_rulet[i][1][1]):
                    selected_pop.append(list_rulet[i][0])
                    break
        return selected_pop

    def to_crossing_over(self, selected_pop):
        childs = []

        for i in range(len(selected_pop)):
            if self.random_cross():
                index_one_parent = random.randint(1, len(selected_pop) - 1)
                index_two_parent = random.randint(1, len(selected_pop) - 1)

                while index_two_parent == index_one_parent:
                    index_two_parent = random.randint(0, len(selected_pop) - 1)

                point_crossingover = random.randint(1, len(selected_pop[index_one_parent].genotype) - 1)

                one_child = selected_pop[index_one_parent].genotype[0: point_crossingover] + \
                            selected_pop[index_two_parent].genotype[point_crossingover:
                                                                    len(selected_pop[index_two_parent].genotype)]

                two_child = selected_pop[index_two_parent].genotype[0: point_crossingover] + \
                            selected_pop[index_one_parent].genotype[point_crossingover:
                                                                    len(selected_pop[index_one_parent].genotype)]

                childs.append(individ.Individual(self.reform(self.to_mutate(one_child))))
                childs.append(individ.Individual(self.reform(self.to_mutate(two_child))))

        return childs

    def to_mutate(self, child):
        if self.random_mut():
            mut_point = random.randint(0, len(child) - 1)

            if child[mut_point] == "1":
                child = child[0: mut_point] + "0" + child[mut_point + 1: len(child)]

            elif child[mut_point] == "0":
                child = child[0: mut_point] + "1" + child[mut_point + 1: len(child)]
            return child

        else:
            return child

    def reduction_new_pop(self, new_pop):
        return sorted(new_pop, key=self.sort_individ_fit)[self.pop_size:]

    def reform(self, child):
        return [child[x: 3 + x] for x in range(0, len(child), 3)]

    '''
        Батюшка-рандом
    '''
    def random_cross(self):
        if random.random() > self.cross_prob:
            return False
        else:
            return True

    def random_mut(self):
        if random.random() > self.mut_prob:
            return False
        else:
            return True

    '''
        Вывод
    '''
    def create_visualization(self, correct_solution):
        visualization = ""
        for row in range(len(correct_solution)):
            for column in range(len(correct_solution)):
                if column == int(correct_solution[row], 2):
                    visualization += "Q"
                else:
                    visualization += "+"
            visualization += '\n'
        return visualization

    def sort_individ_fit(self, individ):
        return individ.fit
