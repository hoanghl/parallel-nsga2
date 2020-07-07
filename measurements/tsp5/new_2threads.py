import time

from Problem import Problem

if __name__ == "__main__":
    ###################################
    ## Đọc file dữ liệu các cities
    ###################################
    distances = []
    with open('measurements/tsp5/data_5cities.txt', 'r') as dat_file:
        n = 5
        for line in dat_file.readlines():
            distances.append([float(line[i:i+n]) for i in range(0, len(line) - 1, n)])



    ###################################
    ## Đọc file dữ liệu các cities
    ###################################
    def kernel_optimizator(*args):
        ''' Đây là hàm nhân (kernel) của GA

        :Args:
        None

        :Rets:
        float - là fitness level của bộ tham số H1, H2, K1, K2, K3
        '''
        N = len(args) - 1

        list_cities = list(range(N + 1))

        ####################################
        ## Biến các input thành số nguyên và loại bỏ
        ## các gen không tốt
        ####################################
        for ith, x in enumerate(args):
            j = int(x)

            if ith < j <= N:
                list_cities[ith], list_cities[j] = list_cities[j], list_cities[ith]


        cul_distance = distances[list_cities[0]][list_cities[len(list_cities) - 1]]
        ####################################
        ## Tính toán đường đi
        ####################################
        for i in range(1, len(list_cities), 1):
            cul_distance += distances[list_cities[i - 1]][list_cities[i]]

        return cul_distance

    dict_genOperaions = {
        'n_tourParticips' : 2,
        'tournament_prob' : 0.9,
        'crossover_param' : 2,
        'mutation_param'  : 30,
    }
    # params, objectives = optimizator(
    #     nGeneration=30,
    #     nVariables=5,
    #     objectives=[kernel_optimizator],
    #     varRange=[(0, 4.9)],
    #     same_range=True,
    #     nIndividuals=500
    # )


    # print("Params    : {}".format(params))
    # print("Objectives: {}".format(objectives))
    problem = Problem(
        n_generations=500,
        n_individuals=70,
        n_variables=5,
        variables_range=[(0, 4.9)],
        same_range=True,
        expand=True,
        objectives=[kernel_optimizator],
        nThread=2)

    start = time.time()


    problem.start()

    end = time.time()

    problem.check()

    print("============================================")

    problem.check()
    print("==> Elapsed time: {:.6f}".format(end - start))
