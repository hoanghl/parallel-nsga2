
from random import random, uniform

class Individual:
    # def __init__(self, variables_ranges, features=None, objectives=None, rank=0, eliteID=0):
    def __init__(self, variables_ranges, eliteID=0):
        self.features               = [uniform(*x) for x in variables_ranges]
        self.objectives             = None


        ## Các biến sau là holder cho việc tính toán
        self.rank                   = None #0
        self.crowding_distance      = None
        self.domination_count       = None #0
        self.dominated_solutions    = None #[]

        self.eliteID                = eliteID

        #######################
        ## Khởi tạo các chromosome
        #######################
        # self.features = [uniform(*x) for x in variables_ranges] if self.features

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.features == other.features
        return False

    def dominates(self, other_individual) -> bool:
        """ Kiểm tra xem individual self có 'dorminates' với `other_individual`

        Arguments:
            other_individual {Individual} -- instance cần mang đi so sánh

        Returns:
            bool -- True nếu dorminate
        """
        and_condition = True
        or_condition = False
        for first, second in zip(self.objectives, other_individual.objectives):
            and_condition = and_condition and first <= second
            or_condition = or_condition or first < second
        return and_condition and or_condition


    #####################################
    # NOTE: FOR TESTING PURPOSE
    #####################################
    def check(self, tag):
        # print("-- Objective: {:8d} - {:8d}".format(self.objectives[0], self.objectives[1]))


        ######################
        # Type 2
        ######################
        # print("-- {}: Objective: {:.6f} -- features: {}".format(
        #     tag,
        #     self.objectives[0],
        #     ["{:5f}".format(x) for x in self.features]))


        ######################
        # Type 3
        ######################
        print("-- {}: Objective: {:10.5f}".format(
            tag,
            self.objectives[0]))

        ######################
        # Type 4
        ######################
        # print("{:10.5f}".format(
        #     self.objectives[0]))
