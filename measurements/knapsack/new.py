import json
import time

from Problem import Problem

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

    # problem = Problem(
    #     n_variables=MAX_N_THINGS,
    #     objectives=[f_value, f_constraint1],
    #     variables_range=[(0, 1)],
    #     same_range=True,
    #     expand=False)
    problem = Problem(
        n_generations=500,
        n_individuals=20,
        n_variables=MAX_N_THINGS,
        variables_range=[(0, 1)],
        same_range=True,
        expand=False,
        objectives=[f_value, f_constraint1],
        nThread=2
    )


    start = time.time()


    problem.start()

    end = time.time()

    problem.check()

    print("==> Elapsed time: {:.6f}".format(end - start))
