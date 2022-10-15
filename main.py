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
        days (int): the number of days
        outcomes (dictionary): the real trend/outcomes in each day
        experts (int): the number of experts

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
    
    # count the number of mistakes the alg make
    alg_mistakes = 0
    
    for day in range(1, days):
        # collect the prediction of each expert and calculate the majority vote
        yes, no = 0, 0
        for i in range(experts):
            # save prediction_
            predict = expert.call_experts(i, day, outcomes)
            # check correctness
            if predict != outcomes[day]:
                weights[i] = weights[i]/2
                mistakes[i] += 1
                pass
            
            # calculate majority voter
            if(predict == 1):
                yes += weights[i]
                pass
            else:
                no += weights[i]
                pass
            pass
        
        # aggregates the prediction and make decision based on a majority vote
        decision = 0
        if yes > no:
            decision = 1
            pass
        if outcomes[day] != decision:
            alg_mistakes += 1
            pass
        # print(weights)
        pass
    
    regret = alg_mistakes - min(mistakes.values())
    return alg_mistakes, regret



def mwu(d, c, e, epsilon):
    """_summary_
    
    Args:
        d (int): the number of days
        c (dictionary): the dictionary that save the a list of cost of following each expert i on different day
        e (int): the number of experts
        epsilon (float): a constant to change the weight of each expert

    Returns:
        float, float: the total expected cost of the alg and the regret of the alg
    """
    # a dictionay to save the expected cost of the alg in each day
    expected_costs = dict()
    # a dictionary to save the total cost of each expert
    experts_costs = dict()
    # initial the weight and probability distribution
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
    for day in range(d):
        expected_costs[day] = 0
        for i in range(e):
            # collect the cost of following expert i on day t
            m = c[day][i]
            # calculate the expected cost of following expert i on day t
            expected_expert_cost = distributions[i] * m
            # sum the expected cost of following each expert on day t
            expected_costs[day] += expected_expert_cost
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
    


    
    
    
    
    