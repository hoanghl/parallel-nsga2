
from copy import deepcopy
import json
import math
import csv
import time


from Problem import Problem

from measurements.PO600.utils import sort_by_rule



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






if __name__ == "__main__":

    rules = []

    print("1. Đọc data từ file 'data.json' và rule từ file `rules.csv`")
    with open("measurements/PO600/data600.json", 'r') as dat_file:
        list_bds = json.load(dat_file)

    with open('measurements/PO600/rules/rules.csv', 'r') as file_rules:
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

    list_bds_backup = deepcopy(list_bds)
    list_bds_backup2 = deepcopy(list_bds)
    list_bds_backup3 = deepcopy(list_bds)

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

    def optimizator_kernel2(*args):
        """Đây chính là hàm objective để chạy tối ưu NSGA-2

        Returns:
            [type] -- [description]
        """

        H1, H2, K1, K2, K3 = args

        ####################################
        ## Tính điểm cho từng bài bds
        ####################################

        for bds in list_bds_backup:
            getScore(params=(H1, H2, K1, K2, K3), bds=bds)


        ####################################
        ## Sắp xếp các bài bds theo điểm
        ####################################
        list_bds_backup.sort(key=lambda x:x['score'], reverse=True)


        ####################################
        ## Tính tổng sai khác thứ hạng
        ####################################
        return math.sqrt(sum([(i - bds['rank'])**2 for i, bds in enumerate(list_bds_backup)]))


    # param_set, score = optimizator(
    #     nGeneration=1000,
    #     nVariables=5,
    #     objectives=[optimizator_kernel],
    #     varRange=[(0, 100)],
    #     same_range=True)

    problem = Problem(
        n_generations=1000,
        n_individuals=70,
        n_variables=5,
        variables_range=[(0, 1)],
        same_range=True,
        objectives=[optimizator_kernel, optimizator_kernel2],
        nThread=2,
        isSame=True)


    start = time.time()

    problem.start()

    end = time.time()
    print("============================================")

    problem.check()
    print("==> Elapsed time: {:.6f}".format(end - start))

    # print(optimizator_kernel(
    #     0.802623, 0.641936, 0.628745, 0.715153, 0.766243
    # ))
