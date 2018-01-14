# -*- coding: utf-8 -*-
import random
import individ


class Solver_8_queens:
    '''
    Dummy constructor representing proper interface
    '''
    def __init__(self, pop_size=50, cross_prob=0.6, mut_prob=0.7):
        self.pop_size = pop_size
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob
    '''
    Dummy method representing proper interface
    '''

    def solve(self, min_fitness=0.9, max_epochs=10000):
        best_fit = None
        epoch_num = None
        visualization = None

        pop = self._create_pop()
        self._search_fit(pop)

        i = 0
        check = False
        while i < max_epochs:
            selected_pop = self.selection_individuals(pop)
            new_pop = self.to_crossing_over(selected_pop)

            self._search_fit(new_pop)

            pop.clear()
            for j in range(self.pop_size):
                max_ob = (new_pop[0], new_pop[0].get_fit())
                index_max = 0
                for k in range(len(new_pop)):
                    if (max_ob[1] <= new_pop[k].get_fit()) and (max_ob[0] != new_pop[k]):
                        max_ob = (new_pop[k], new_pop[k].get_fit())
                        index_max = k
                pop.append(max_ob[0])
                del new_pop[index_max]

            self._search_fit(pop)

            for j in range(len(pop)):
                if len(pop[j].get_check_cromosome()) == 8:
                    min_fitness = pop[j].get_fit()

            i = i + 1
            #print(i)
            for j in range(len(pop)):
                if pop[j].get_fit() >= min_fitness:
                    visualization = ""
                    ff = pop[j].get_list_chromosome()
                    print(ff, "Лсит ферзей")
                    print(pop[j].get_check_cromosome(), "Ферьзи, которые не пересикаются")
                    print(pop[j].get_fit(), "фитнес этого решения")
                    for row in range(8):
                        for b in range(len(ff)):
                            if b == int(ff[row], 2):
                                visualization = visualization + "Q"
                            else:
                                visualization = visualization + "+"
                        visualization = visualization + '\n'
                    best_fit = min_fitness
                    epoch_num = i
                    check = True
                    break
            if check:
                break

        return best_fit, epoch_num, visualization

    def _create_pop(self):
        pop = []
        for i in range(self.pop_size):
            individerrrr = ["000", "001", "010", "011", "100", "101", "110", "111"]
            for j in range(10):
                one_index = random.randint(0, 7)
                two_index = random.randint(0, 7)

                temp = individerrrr[one_index]
                individerrrr[one_index] = individerrrr[two_index]
                individerrrr[two_index] = temp
            pop.append(individ.Individual(individerrrr))

        return pop

    def _search_fit(self, pop):
        for i in range(len(pop)):
            pop[i].search_fit(pop)

    def selection_individuals(self, pop):
        selected_pop = []
        list_rulet = []
        temp_one = 0
        temp_two = 0
        for i in range(len(pop)):
            #for j in range(pop[i].get_estim_number_chromosomes()):
                #selected_pop.append(pop[i])
            temp_two = temp_one
            temp_one = temp_one + pop[i].get_fit()
            list_rulet.append((pop[i], (temp_two, temp_one)))

        select = random.random()

        for k in range(self.pop_size):
            for i in range(len(list_rulet)):
                if select >= list_rulet[i][1][0]:
                    if select <= list_rulet[i][1][1]:
                        selected_pop.append(list_rulet[i][0])
                        break
                if select <= list_rulet[i][1][1]:
                    if select >= list_rulet[i][1][0]:
                        selected_pop.append(list_rulet[i][0])
                        break

        return selected_pop

    '''    
        ----------------
        ТУТ ДЛЯ ГЕНОТИПА
        ----------------    
    '''
    def to_crossing_over(self, selected_pop):
        childs = []

        for i in range(len(selected_pop)):
            index_one_parent = random.randint(1, len(selected_pop) - 1)
            index_two_parent = random.randint(1, len(selected_pop) - 1)

            while index_two_parent == index_one_parent:
                index_two_parent = random.randint(0, len(selected_pop) - 1)

            point_crossingover = random.randint(1, 24 - 1)

            one_child = selected_pop[index_one_parent].get_genotype()[0: point_crossingover] + selected_pop[index_two_parent].get_genotype()[point_crossingover: len(selected_pop[index_two_parent].get_genotype())]
            two_child = selected_pop[index_two_parent].get_genotype()[0: point_crossingover] + selected_pop[index_one_parent].get_genotype()[point_crossingover: len(selected_pop[index_one_parent].get_genotype())]

            childs.append(individ.Individual(self.reform(self.to_mutate_(one_child))))
            childs.append(individ.Individual(self.reform(self.to_mutate_(two_child))))
            #childs.append(individ.Individual(self.to_mutate_(two_child)))

        return childs

    def to_mutate_(self, child):
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

    def reform(self, child):
        list_chromosome = []
        temp = 0
        for i in range(8):
            list_chromosome.append(child[temp: 3 + temp])
            temp = temp + 3
        return list_chromosome

    '''
        -------------
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



