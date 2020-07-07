

from Population import Population

from Utils import Utils




class Problem:
    def __init__( self,
                  n_individuals     : int,
                  n_generations     : int,
                  n_variables       : int,
                  objectives        : list,
                  variables_range   : list,
                  isSame            : bool =False,
                  dict_genOperaions : dict =None,
                  expand            : bool =True,
                  same_range        : bool =False,
                  nThread           : int  =4):

        ## D
        self.list_populations   = None


        ## Các biến holder - là các biến giữ một giá trị đặc biệt nào đó
        self.n_individuals      = n_individuals // nThread
        self.n_generations      = n_generations // nThread
        self.current_generation = 0
        self.nThread            = nThread


        #######################
        ## Tiến hành khởi tạo các population
        #######################
        if not isSame:
            self.utils              = Utils(
                n_individuals=self.n_individuals,
                n_variables=n_variables,
                list_objectives=objectives,
                variables_range=variables_range,
                expand=expand,
                same_range=same_range,
                dict_genOperaions=dict_genOperaions)
            self.list_populations = [
                Population(self.utils, popId=i, nThread=nThread)
                for i in range(nThread)
            ]
        else:
            self.utils              = Utils(
                n_individuals=self.n_individuals,
                n_variables=n_variables,
                list_objectives=objectives[0],
                variables_range=variables_range,
                expand=expand,
                same_range=same_range,
                dict_genOperaions=dict_genOperaions)
            self.list_populations = [
                Population(
                    Utils(
                        n_individuals=self.n_individuals,
                        n_variables=n_variables,
                        list_objectives=[objectives[i]],
                        variables_range=variables_range,
                        expand=expand,
                        same_range=same_range,
                        dict_genOperaions=dict_genOperaions),
                    popId=i,
                    nThread=nThread)
                for i in range(nThread)
            ]




    def start(self):
        """Kích hoạt việc tiến hóa của các population
        """


        while True:
            # print("* Current: {:3d}".format(self.current_generation))



            #######################
            ### Cho các population tiến hóa
            #######################
            self.evolve_all()



            ######################
            ## Lấy ra Elite group từ các population
            ## và chọn ra best elite
            ######################

            ## Lấy ra các elite
            list_elites = [
                population.population[:2]
                for population in self.list_populations
            ]



            ## Trong từng nhóm elite, lấy ra phần tử đầu tiên
            list_representativeElite = []
            for nth, elites in enumerate(list_elites):
                representative = elites[0]
                representative.eliteID = nth

                list_representativeElite.append(representative)

            ## Chọn ra elite tốt nhất
            selectivePop = Population(self.utils, list_representativeElite, nThread=self.nThread)
            self.utils.fast_nondominated_sort(selectivePop)
            n_bestEliteSet = selectivePop.fronts[0][0].eliteID



            #######################
            ## Lây lan
            #######################
            for nth, population in enumerate(self.list_populations):
                if nth == n_bestEliteSet:
                    continue

                self.spread(list_elites[n_bestEliteSet], population)



            #######################
            ## Cập nhật lại các giá trị holder
            #######################
            self.current_generation += 1


            #######################
            ### Kiểm tra điều kiện hội tụ
            ### hoặc chạy hết số generation cho phép
            #######################
            # for population in self.list_populations:
            #     population.check()
            # self.list_populations[0].check()

            if self.current_generation >= self.n_generations:
            # if self.current_generation >= 2:
                break



    def evolve_all(self):
        """ Tiến hành tiến hóa với mọi quần thể
        """
        #######################
        ## Vì các population cũng chính là các thread
        ## nên ta sẽ kích hoạt việc tiến hóa bằng cách chạy
        ## các thread
        #######################

        list_threads = []
        for population in self.list_populations:
            list_threads.append(
                population.start_thread()
            )

        for _thread in list_threads:
            _thread.start()

        for _thread in list_threads:
            _thread.join()





    def spread(self, list_indi: list, population: Population):
        """ Lây lan `list_indi` vào quần thể `population`

        Arguments:
            list_indi {list of Individual} -- cá thể tối ưu đủ điều kiện để phân bổ vào các quần thể khác
        """
        for indiA, indiB in zip(population.population[-len(list_indi):],list_indi):
            indiA.features   = indiB.features.copy()
            # self.utils.calculate_objectives(indiA)
            indiA.objectives = indiB.objectives.copy()


    #####################################
    # FOR TESTING PURPOSE
    #####################################
    def check(self):
        for n_th, x in enumerate(self.list_populations):
            print("- Pop {:2d}: ".format(n_th))
            x.check()

    def check2(self):
        for n_th, x in enumerate(self.list_populations):
            print("- Pop {:2d}".format(n_th))
            x.check2()
