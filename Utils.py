''' File này chứa class Utils, nó chứa các hàm sử dụng chung bởi các class trong toàn bộ project
'''

import random
import json

from Population import Population, Individual


class Utils:
    def __init__( self,
                  n_individuals,
                  n_variables,
                  list_objectives,
                  variables_range,
                  expand,
                  same_range,
                  dict_genOperaions):

        self.variables_ranges = [variables_range[0] for _ in range(n_variables)] if same_range else variables_range

        self.n_individuals      = n_individuals
        self.list_objectives    = list_objectives
        self.expand             = expand

        if dict_genOperaions is not None:
            self.n_tourParticips    = dict_genOperaions['n_tourParticips']
            self.tournament_prob    = dict_genOperaions['tournament_prob']
            self.crossover_param    = dict_genOperaions['crossover_param']
            self.mutation_param     = dict_genOperaions['mutation_param']
        else:
            self.n_tourParticips    = 2
            self.tournament_prob    = 0.9
            self.crossover_param    = 2
            self.mutation_param     = 5


    ##########################################################
    ## Phần liên quan tới Individual
    ##########################################################

    def calculate_objectives(self, individual: Individual):
        """Tính toán các giá trị của các hàm objectives

        Arguments:
            individual {Individual} -- cá thể dùng để tính các giá trị của các hàm objectives
        """
        if self.expand:
            individual.objectives = [f(*individual.features) for f in self.list_objectives]
        else:
            individual.objectives = [f(individual.features) for f in self.list_objectives]




    ##########################################################
    ## Phần liên quan tới Population
    ##########################################################


    def fast_nondominated_sort(self, population: Population):   # DEBUG: Xem lại trường hợp có 200 Indi nhưng chỉ tạo 1 front có 82
        """ Triển khai thuật toán Fast Nondominated Sort trên `population`

        Arguments:
            population {Population} -- quần thể cần triển khai thuật toán sắp xếp
        """

        population.fronts = [[]]        # NOTE: Place "fronts" changed


        for individual in population:
            individual.domination_count     = 0
            individual.dominated_solutions  = []
            # self.calculate_objectives(individual)

            for other_individual in population:
                if individual.dominates(other_individual):
                    individual.dominated_solutions.append(other_individual)
                elif other_individual.dominates(individual):
                    individual.domination_count += 1

            if individual.domination_count == 0:
                individual.rank = 0
                population.fronts[0].append(individual)

        i = 0
        while len(population.fronts[i]) > 0:
            temp = []
            for individual in population.fronts[i]:
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i+1
                        temp.append(other_individual)
            i = i+1
            population.fronts.append(temp)



    def calculate_crowding_distance(self, front: list):
        """ Tính crowding distance cho từng cá thể trong front

        Arguments:
            front {list(Individual)} -- list các Individual
        """
        if len(front) > 0:
            solutions_num = len(front)

            for individual in front:
                individual.crowding_distance = 0

            for m in range(len(front[0].objectives)):
                front.sort(key=lambda individual: individual.objectives[m])
                front[0].crowding_distance = 10**9
                front[solutions_num-1].crowding_distance = 10**9
                m_values = [individual.objectives[m] for individual in front]
                scale = max(m_values) - min(m_values)
                if scale == 0:
                    scale = 1

                for i in range(1, solutions_num-1):
                    front[i].crowding_distance += (front[i+1].objectives[m] - front[i-1].objectives[m])/scale


    def create_children(self, population: Population) -> list:
        """Tạo quần thể con bằng genetic operations, các cá thể offspring
        tạo ra sẽ được gộp lại với parent population

        Arguments:
            population {Population} -- quần thể cha mẹ

        Returns:
            list(Individual) -- list các cá thể con mới được tạo ra
        """

        children = []               ## list chứa các cá thể con tạo ra

        while len(children) < len(population):
            parent1 = self.__tournament(population)
            parent2 = parent1
            while parent1 == parent2:
                parent2 = self.__tournament(population)
            child1, child2 = self.__crossover(parent1, parent2)
            self.__mutate(child1)
            self.__mutate(child2)
            self.calculate_objectives(child1)
            self.calculate_objectives(child2)
            children.append(child1)
            children.append(child2)

        return children





    #################################################################
    # Phần liên quan tới GENETICS OPERATIONS and associated stuffs
    #################################################################

    ####################################################
    ## Operation: Crossover
    ####################################################
    def __crossover(self, individual1:Individual, individual2:Individual) -> (Individual, Individual):
        """Lai tạo

        Arguments:
            individual1 {Individual} -- cá thể thứ nhất dùng để lai tạo
            individual2 {Individual} -- cá thể thứ hai dùng để lai tạo

        Returns:
            tuple -- 2 cá thể mới sau khi được lai tạo
        """
        child1 = Individual(self.variables_ranges)
        child2 = Individual(self.variables_ranges)
        num_of_features = len(child1.features)
        genes_indexes = range(num_of_features)
        for i in genes_indexes:
            beta = self.__get_beta()
            x1 = (individual1.features[i] + individual2.features[i])/2
            x2 = abs((individual1.features[i] - individual2.features[i])/2)
            child1.features[i] = x1 + beta*x2
            child2.features[i] = x1 - beta*x2
        return child1, child2

    def __get_beta(self):
        u = random.random()
        if u <= 0.5:
            return (2*u)**(1/(self.crossover_param+1))
        return (2*(1-u))**(-1/(self.crossover_param+1))


    ####################################################
    ## Operation: Mutation
    ####################################################
    def __mutate(self, child):
        num_of_features = len(child.features)
        for gene in range(num_of_features):
            u, delta = self.__get_delta()
            if u < 0.5:
                child.features[gene] += delta*(child.features[gene] - self.variables_ranges[gene][0])
            else:
                child.features[gene] += delta*(self.variables_ranges[gene][1] - child.features[gene])
            if child.features[gene] < self.variables_ranges[gene][0]:
                child.features[gene] = self.variables_ranges[gene][0]
            elif child.features[gene] > self.variables_ranges[gene][1]:
                child.features[gene] = self.variables_ranges[gene][1]

    def __get_delta(self):
        u = random.random()
        if u < 0.5:
            return u, (2*u)**(1/(self.mutation_param + 1)) - 1
        return u, 1 - (2*(1-u))**(1/(self.mutation_param + 1))


    ####################################################
    ## Operation: Tournament selection
    ####################################################
    def __tournament(self, population):
        participants = random.sample(population.population, self.n_tourParticips)
        best = None
        for participant in participants:
            if best is None or (self.crowding_operator(participant, best) == 1 and self.__choose_with_prob(self.tournament_prob)):
                best = participant

        return best

    def crowding_operator(self, individual: Individual, other_individual: Individual):
        """Toán tử crowding dùng trong so sánh ở bước tournament

        Arguments:
            individual {Individual} -- [description]
            other_individual {Individual} -- [description]

        Returns:
            [type] -- [description]
        """

        if  (individual.rank < other_individual.rank) or \
            (\
                (individual.rank == other_individual.rank) and\
                (individual.crowding_distance > other_individual.crowding_distance)
            ):
            return 1

        return -1


    def __choose_with_prob(self, prob):
        return random.random() <= prob
