import json
import math
import csv
import time

from nsga2.problem import Problem
from nsga2.evolution import Evolution


from measurements.PO4000.utils import sort_by_rule


def getScore(params, bds):
    """ Tính điểm của `bds` dựa vào `params`, trường `case` và trường `diem_tuongdoi`
    Kết quả tính được sẽ gán thẳng vào trường 'score' của `bds`

    Lưu ý: Hàm này chính là hàm f1 trong phần 3. Phác thảo code
    :Args:
    - params - bộ tuple 5 tham số
    - bds - dict chứa thông tin vê bds

    :Rets:
    - Không có giá trị trả về
    """


    param_H1, param_H2, param_K1, param_K2, param_K3 = params



    if bds['case'] == 0:
        bds['score'] = -1000
    elif bds['case'] == 1:
        bds['score'] = bds['diem_tuongdoi'] * param_H1
    elif bds['case'] == 2:
        bds['score'] = bds['diem_tuongdoi'] * param_K1 * param_H1
    elif bds['case'] == 3:
        bds['score'] = bds['diem_tuongdoi'] * param_K2 * param_H1
    elif bds['case'] == 4:
        bds['score'] = bds['diem_tuongdoi'] * param_K3 * param_H1
    elif bds['case'] == 5:
        bds['score'] = bds['diem_tuongdoi'] * param_H2
    else:
        bds['score'] = bds['diem_tuongdoi'] * param_H2







def optimizator(nGeneration=1000, nIndividuals=50, nVariables=1, objectives=None, varRange=None, same_range=None):
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
    evo = Evolution(problem, num_of_generations=nGeneration, num_of_individuals=nIndividuals)

    start = time.time()

    evol = evo.evolve()

    end = time.time()

    return evol[0].features, evol[0].objectives, end - start




if __name__ == "__main__":

    rules = []

    print("1. Đọc data từ file 'data.json' và rule từ file `rules.csv`")
    with open("measurements/PO4000/data4000.json", 'r') as dat_file:
        list_bds = json.load(dat_file)

    with open('measurements/PO4000/rules/rules.csv', 'r') as file_rules:
        csv_reader = csv.reader(file_rules, delimiter=',')

        for row in csv_reader:
            if len(row) == 1:
                rules.append({
                    'queue' : [],
                    'rule' : row[0]
                })
            else:
                for single_rule in row:
                    rules.append({
                        'queue' : [],
                        'rule' : single_rule
                    })


    ##########################################################
    # Sắp xếp các bđs theo rule
    ##########################################################
    print("2. Sắp xếp các bđs theo rules để gán giá trị rank_kỳ_vọng cho từng bài")
    list_bds = sort_by_rule(list_bds, input_rules=rules)

    ##########################################################
    # Tiến hành tìm bộ tham số tối ưu
    ##########################################################
    print("3. Tiến hành tối ưu")


    def optimizator_kernel(*args):
        """Đây chính là hàm objective để chạy tối ưu NSGA-2

        Returns:
            [type] -- [description]
        """

        H1, H2, K1, K2, K3 = args

        ####################################
        ## Tính điểm cho từng bài bds
        ####################################
        for bds in list_bds:
            getScore(params=(H1, H2, K1, K2, K3), bds=bds)


        ####################################
        ## Sắp xếp các bài bds theo điểm
        ####################################
        list_bds.sort(key=lambda x:x['score'], reverse=True)


        ####################################
        ## Tính tổng sai khác thứ hạng
        ####################################
        return math.sqrt(sum([(i - bds['rank'])**2 for i, bds in enumerate(list_bds)]))


    param_set, score, elapsedTime = optimizator(
        nGeneration=1000,
        nVariables=5,
        objectives=[optimizator_kernel],
        varRange=[(0, 100)],
        nIndividuals=70,
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
