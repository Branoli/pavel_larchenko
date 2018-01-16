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

    def solve(self, min_fitness=0.9, max_epochs=10000):
        index_correct_solution = None

        pop = self.create_pop()
        self.search_fit(pop)

        count_epochs = 0
        while count_epochs < max_epochs:

            new_pop = self.to_crossing_over(self.create_roulette(pop))
            self.search_fit(new_pop)

            pop.clear()

            pop = self.reduction_new_pop(new_pop)
            self.search_fit(pop)

            '''
                Поиск правильного решения
            '''
            for j in range(len(pop)):
                if len(pop[j].correct_chromosomes) == 8:
                    min_fitness = pop[j].fit
                    index_correct_solution = j
                    break

            if index_correct_solution != None:
                break

            count_epochs += 1

        '''
            Вывод
        '''
        visualization = self.create_visualization(pop[index_correct_solution].correct_chromosomes)
        best_fit = min_fitness
        epoch_num = count_epochs

        return best_fit, epoch_num, visualization

    '''
        Геннетический алгоритм
    '''
    def create_pop(self):
        pop = []
        for i in range(self.pop_size):
            individ_list = ["000", "001", "010", "011", "100", "101", "110", "111"]
            for j in range(10):
                one_index = random.randint(0, 7)
                two_index = random.randint(0, 7)

                temp = individ_list[one_index]
                individ_list[one_index] = individ_list[two_index]
                individ_list[two_index] = temp
            pop.append(individ.Individual(individ_list))

        return pop

    def search_fit(self, pop):
        for i in range(len(pop)):
            summ_fit = 0
            for j in range(len(pop)):
                summ_fit = summ_fit + pop[j].count_correct_chromosome
            pop[i].fit = pop[i].count_correct_chromosome / summ_fit

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
                if select >= list_rulet[i][1][0]:
                    if select < list_rulet[i][1][1]:
                        selected_pop.append(list_rulet[i][0])
                        break
                if select < list_rulet[i][1][1]:
                    if select >= list_rulet[i][1][0]:
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

                point_crossingover = random.randint(1, 24 - 1)

                one_child = selected_pop[index_one_parent].genotype[0: point_crossingover] + \
                            selected_pop[index_two_parent].genotype[point_crossingover: len(selected_pop[index_two_parent].genotype)]

                two_child = selected_pop[index_two_parent].genotype[0: point_crossingover] + \
                            selected_pop[index_one_parent].genotype[point_crossingover: len(selected_pop[index_one_parent].genotype)]

                childs.append(individ.Individual(self.reform(self.to_mutate(one_child))))
                childs.append(individ.Individual(self.reform(self.to_mutate(two_child))))

        return childs

    def to_mutate(self, child):
        if self.random_mut():

            mut_point = random.randint(1, len(child) - 1)

            one_part = child[0: mut_point - 1]
            two_part = child[mut_point: len(child)]

            if child[mut_point - 1: mut_point] == "0":

                if one_part == '':
                    mut_child = "1" + two_part

                elif two_part == '':
                    mut_child = one_part + "1"

                else:
                    mut_child = one_part + "1" + two_part

                child = mut_child
            else:
                if one_part == '':
                    mut_child = "0" + two_part

                elif two_part == '':
                    mut_child = one_part + "0"

                else:
                    mut_child = one_part + "0" + two_part
                child = mut_child

            return child
        else:
            return child

    def reduction_new_pop(self, new_pop):
        pop = []
        for j in range(self.pop_size):
            max_individ = (new_pop[0], new_pop[0].fit)
            index_max = 0
            for k in range(len(new_pop)):
                if (max_individ[1] <= new_pop[k].fit) and (max_individ[0] != new_pop[k]):
                    max_individ = (new_pop[k], new_pop[k].fit)
                    index_max = k
            pop.append(max_individ[0])
            del new_pop[index_max]

        return pop

    def reform(self, child):
        list_chromosome = []
        temp = 0
        for i in range(8):
            list_chromosome.append(child[temp: 3 + temp])
            temp += 3
        return list_chromosome

    '''
        Батюшка-рандом
    '''
    def random_cross(self):
        prob = random.random()
        if prob > self.cross_prob:
            return False
        else:
            return True

    def random_mut(self):
        prob = random.random()
        if prob > self.mut_prob:
            return False
        else:
            return True

    '''
        Вывод
    '''
    def create_visualization(self, correct_solution):
        visualization = ""
        _correct_solution = correct_solution
        for row in range(len(_correct_solution)):
            for b in range(len(_correct_solution)):
                if b == int(_correct_solution[row], 2):
                    visualization += "Q"
                else:
                    visualization += "+"
            visualization += '\n'
        return visualization




