
from copy import deepcopy
import threading
import json                 # NOTE: Remove this line

from Individual import Individual

class Population():
    def __init__(self,
                 utils,
                 list_indi=None,
                 popId=None,
                 nThread=4):

        self.popId = popId
        self.population                 = []
        self.fronts                     = []


        ## Các biến sau là các holder
        self.utils                      = utils
        self.current_generation         = 0
        self.nThread                    = nThread




        #######################
        ## Khởi tạo các individuals
        #######################
        if list_indi is not None:
            self.population.extend(list_indi)
        else:
            for _ in range(self.utils.n_individuals):
                individual = Individual(self.utils.variables_ranges)
                self.utils.calculate_objectives(individual)
                self.population.append(individual)

    def __len__(self):
        return len(self.population)

    def __iter__(self):
        return self.population.__iter__()



    def start_thread(self):
        return threading.Thread(target=self.run, args=())

    def run(self):
        """ Tiến hành tiến hóa 1 thế hệ
        """

        for _ in range(1):

            # print("{} ==> 1.  {:.6f}".format(self.popId, self.population[0].objectives[0]))


            self.utils.fast_nondominated_sort(self)

            ## Tính toán crowding distance của các front
            for front in self.fronts:
                self.utils.calculate_crowding_distance(front)

            ## Tạo danh sách các offspring individuals
            children = self.utils.create_children(self)

            # print("{} ==> 2.1 {:.6f}".format(self.popId, children[0].objectives[0]))

            #####################################
            ### Sát nhập các cá thể con vào quần thể chung
            #####################################
            self.population.extend(children)


            self.utils.fast_nondominated_sort(self)

            # print("{} ==> 2.2. {:.6f}".format(self.popId, self.population[0].objectives[0]))


            #####################################
            ### Tạo một quần thể mới từ tập hợp quần thể cũ và các cá thể con
            #####################################

            new_population = []             ## biến này sẽ chứa quần thể mới, mà cuối cùng sẽ được gán ngược
                                            ## trở lại cho self.population


            nth_front = 0
            while len(new_population) + len(self.fronts[nth_front]) <= self.utils.n_individuals:
                self.utils.calculate_crowding_distance(self.fronts[nth_front])    ## NOTE: [May 29] : Sau khi chạy ổn định có thể comment dòng này
                new_population.extend(self.fronts[nth_front])
                nth_front += 1


            # print("{} ==> 3.  {:.6f}".format(self.popId, new_population[0].objectives[0]))

            ## front tại vị trí nth_front là front cần phải tính crowding distance để chọn ra những cá thể phù hợp
            self.utils.calculate_crowding_distance(self.fronts[nth_front])


            # print("{} ==> 4.  {:.6f}".format(self.popId, new_population[0].objectives[0]))

            self.fronts[nth_front].sort(key=lambda individual: individual.crowding_distance, reverse=True)
            new_population.extend(self.fronts[nth_front][0 : self.utils.n_individuals-len(new_population)])

            # print("{} ==> 5.  {:.6f}".format(self.popId, new_population[0].objectives[0]))


            self.population = new_population

            ################################
            ## DEBUG
            ################################
            #     self.population[0].check(self.popId)
        # print("{} ==> 1.  {:.6f}".format(self.popId, self.population[0].objectives[0]))

        # if self.population[0].objectives[0] == 0 and self.popId == 0:
        #     # print("here is 0")



    def extend(self, new_individuals):
        self.population.extend(new_individuals)

    def append(self, new_individual):
        self.population.append(new_individual)

    def remove(self):
        del self.population[-self.nThread:]


    #####################################
    # FOR TESTING PURPOSE
    #####################################
    def check(self):
        self.population[0].check(self.popId)
