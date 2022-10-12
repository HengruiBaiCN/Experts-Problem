from ast import Pow
from cmath import log
import random
from itertools import chain, combinations
from re import A
import time
import matplotlib.pyplot as plt
import math
import expert
from statistics import mode

import numpy as np


def wma(days, outcomes, experts):
    """_summary_

    Args:
        days (_type_): _description_
        outcomes (_type_): _description_
        experts (_type_): _description_

    Returns:
        _type_: _description_
    """
    # initial the weight of each expert equal 1
    mistakes = dict()
    weights = dict()
    for i in range(experts):
        weights[i] = 1
        mistakes[i] = 0
        pass
    
    # calculate the accuray of WMU
    mistakes["alg"] = 0
    
    for day in range(1, days):
        # collect the prediction of each expert
        yes = 0
        no = 0
        for i in range(experts):
            # save prediction_
            predict = expert.call_experts(i, day, outcomes)
            
            # check prediction
            if(predict == 1):
                # increase the votes of yes
                yes += weights[i]
                # check correctness
                if predict != outcomes[day]:
                    weights[i] = weights[i]/2
                    mistakes[i] += 1
                    pass
                pass
            else:
                # increase the votes of no
                no += weights[i]
                # check correctness
                if predict != outcomes[day]:
                    weights[i] = weights[i]/2
                    mistakes[i] += 1
                    pass
                pass
            pass
        
        # aggregates the prediction and make decioson based on a majority vote
        decision = 0
        if yes > no:
            decision = 1
            pass
        if outcomes[day] != decision:
            mistakes["alg"] += 1
            pass
        print(weights)
        pass
    regret = mistakes["alg"] - min(mistakes.values())
    return mistakes["alg"], regret



def mwu(d, c, e, epsilon):
    """_summary_

    Args:
        d (_type_): _description_
        c (_type_): _description_
        e (_type_): _description_
        epsilon (_type_): _description_

    Returns:
        _type_: _description_
    """
    # initial the weight and probability distribution
    expected_costs = dict()
    experts_costs = dict()
    weights = dict()
    distributions = dict()
    for i in range(e):
        weights[i] = 1
        experts_costs[i] = 0
        pass
    for i in range(e):
        distributions[i] = weights[i]/sum(weights.values())
        pass
    
    # calculate the expected cost in each day
    for day in range(1, d):
        expected_costs[day] = 0
        for i in range(e):
            # collect the cost of following expert i on day t
            m = c[day][i]
            # calculate the expected cost of following expert i on day t
            expected_expert_cost = distributions[i] * m
            # sum the expected cost of following each expert on day t
            expected_costs[d] = expected_expert_cost
            # update the weight
            weights[i] = weights[i] * (math.exp(-epsilon*m))
            
            # sum the expert cost in each day
            experts_costs[i] += m
            pass
        
        # update the distribution of each expert in next day
        for i in range(e):
            distributions[i] = weights[i]/sum(weights.values())
            pass
        # print(distributions)
        pass
    
    total_costs = sum(expected_costs.values())
    regret = total_costs - min(experts_costs.values())
    print(experts_costs)
    return total_costs, regret



if __name__ == "__main__":
    num_of_days = 20
    epsilon = 0.5
    experts_num = 4
    # generate problem instances
    costs, outcomes = expert.adversary(num_of_days, epsilon, experts_num)
    # print(costs)
    print(outcomes)
    x1, y1 = wma(num_of_days, outcomes, experts_num)
    print(x1, y1)
    x2, y2 = mwu(num_of_days, costs, experts_num, epsilon)
    print(x2, y2)
    


    
    
    
    
    