import time

from nsga2.problem import Problem
from nsga2.evolution import Evolution

def optimizator(nGeneration=1000, nVariables=1, objectives=None, varRange=None, same_range=None, nIndividuals=50):
    """Hàm tìm bộ tham số tối ưu để tối thiểu hóa các hàm `objectives`

    Keyword Arguments:
        nGeneration {int} -- Số lượng thế hệ muốn chạy tìm tối ưu (default: {1000})
        nVariables {int} -- Số lượng biến trong hàm tối ưu (default: {1})
        objectives {list} -- Danh sách các hàm cần tối ưu (default: {None})
        varRange {list} -- Danh sách các tuple là khoảng giá trị của các biến trong các hàm `objectives` (default: {None})

    Returns:
        list, list -- danh sách các giá trị của biến khiến các hàm `objectives` đạt tối thiểu, danh sách các giá trị tối thiểu của các hàm
        float -- time
    """


    ##############################
    # Định nghĩa problem cần minimize
    ##############################
    problem = Problem(
        num_of_variables=nVariables,
        objectives=objectives,
        variables_range=varRange,
        same_range=same_range)


    ##############################
    # Tiến hành minimize
    ##############################
    evo = Evolution(
        problem,
        num_of_generations=nGeneration,
        num_of_individuals=nIndividuals)

    start = time.time()

    evol = evo.evolve()

    end = time.time()

    return evol[0].features, evol[0].objectives, end - start

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


        cul_distance = distances[list_cities[0]][list_cities[len(list_cities) - 1]]
        ####################################
        ## Tính toán đường đi
        ####################################
        for i in range(1, len(list_cities), 1):
            cul_distance += distances[list_cities[i - 1]][list_cities[i]]

        return cul_distance


    params, score, elapsedTime = optimizator(
        nGeneration=1000,
        nIndividuals=70,
        nVariables=48,
        objectives=[kernel_optimizator],
        varRange=[(0, 47.9)],
        same_range=True
    )


    print("==> Objective  : {}".format(["{:10.5f}".format(x) for x in score]))
    print("==> Elaped time: {}".format(elapsedTime))
