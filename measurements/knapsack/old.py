import json
import time

from nsga2.problem import Problem
from nsga2.evolution import Evolution


def optimizator(nGeneration=1000, nVariables=1, objectives=None, varRange=None, same_range=None):
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
        same_range=same_range, expand=False)


    ##############################
    # Tiến hành minimize
    ##############################
    evo = Evolution(
        problem,
        num_of_generations=nGeneration,
        num_of_individuals=70)

    start = time.time()

    evol = evo.evolve()

    end = time.time()

    return evol[0].features, evol[0].objectives, end - start

if __name__ == "__main__":
    with open("measurements/knapsack/data.json", 'r') as file_data:
        data = json.load(file_data)

    MAX_WEIGHT   = data['constants']['max_weight']
    MAX_N_THINGS = len(data['things'])
    things       = data['things']


    def f_activation(v):
        return 1 if v >= 0.5 else 0

    def f_value(values):
        cumulative_val = 0
        for thing, val in zip(things, values):
            cumulative_val += f_activation(val) * thing[1]

        return -cumulative_val
    def f_constraint1(values):
        cumulative_weight = 0
        for thing, val in zip(things, values):
            cumulative_weight += f_activation(val) * thing[0]

        return abs(cumulative_weight - MAX_WEIGHT)

    # dict_genOperaions = {
    #     'n_tourParticips' : 2,
    #     'tournament_prob' : 0.9,
    #     'crossover_param' : 2,
    #     'mutation_param'  : 20,
    # }
    # problem = Problem(
    #     n_variables=MAX_N_THINGS,
    #     objectives=[f_value, f_constraint1],
    #     variables_range=[(0, 1)],
    #     same_range=True,
    #     expand=False)
    # evo = Evolution(
    #     problem,
    #     n_individuals=10,
    #     mutation_param=20,
    #     n_generations=20)
    # start = time.time()
    # evol, first = evo.evolve()
    # end = time.time()

    # # print(evol[0].features)
    # # print(evol[0].objectives)
    # print("==> Max value the thieft can steal: {:8d}".format(-evol[0].objectives[0]))
    # print("==> First conv: {}".format(first))
    # print("==> Elapsed time: {:.6f}".format(end - start))
    # # print(evol[0].features)


    param_set, score, elapsedTime = optimizator(
        nGeneration=1000,
        nVariables=MAX_N_THINGS,
        objectives=[f_value, f_constraint1],
        varRange=[(0, 1)],
        same_range=True)


    ##########################################################
    # Trả về kết quả
    ##########################################################
    # print("4. In kết quả")

    # print("* Bộ tham số đã tối ưu  : {}".format(param_set))
    # print("* Tổng sai khác         : {:6.3f}".format(score[0]))

    # for i, bds in enumerate(list_bds):
    #     print("- Post: {:5d} has score: {:6.3f}".format(i, bds['score']))

    print("==> Objective  : {}".format(["{:10.5f}".format(x) for x in score]))
    print("==> Elaped time: {}".format(elapsedTime))