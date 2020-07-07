import time

from Problem import Problem


if __name__ == "__main__":
    ###################################
    ## Đọc file dữ liệu các cities
    ###################################
    distances = []
    with open('measurements/tsp48/data_48cities.txt', 'r') as dat_file:
        n = 10
        for line in dat_file.readlines():
            distances.append([int(line[i:i+n]) for i in range(0, len(line) - 1, n)])



    ###################################
    ## Đọc file dữ liệu các cities
    ###################################
    def kernel_optimizator(args):
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


    problem = Problem(
        n_generations=1000,
        n_individuals=70,
        n_variables=48,
        variables_range=[(0, 47.9)],
        same_range=True,
        expand=False,
        objectives=[kernel_optimizator],
        nThread=2)

    start = time.time()


    problem.start()

    end = time.time()

    print("============================================")

    problem.check()
    print("==> Elapsed time: {:.6f}".format(end - start))
