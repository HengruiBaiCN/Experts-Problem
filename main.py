from ast import Pow
from cmath import e, log
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
    # print(list(range(days)))
    
    for day in range(days):
        # collect the prediction of each expert and calculate the majority vote
        yes, no = 0, 0
        for i in range(experts):
            # save prediction_
            predict = expert.call_experts(i, day, outcomes)
            # print(outcomes)
            # print(predict)
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
    mistake_bound = 2.41*(min(mistakes.values())+math.log(experts))
    regret_bound = 1.41*(min(mistakes.values())+math.log(experts))
    return alg_mistakes, regret, mistake_bound, regret_bound, mistakes



def mwu(days, c, experts, epsilon):
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
    for i in range(experts):
        weights[i] = 1
        experts_costs[i] = 0
        pass
    for i in range(experts):
        distributions[i] = weights[i]/sum(weights.values())
        pass
    
    # calculate the expected cost in each day
    for day in range(days):
        expected_costs[day] = 0
        for i in range(experts):
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
        for i in range(experts):
            distributions[i] = weights[i]/sum(weights.values())
            pass
        # print(distributions)
        pass
    
    total_costs = sum(expected_costs.values())
    regret = total_costs - min(experts_costs.values())
    cost_bound = min(experts_costs.values()) + math.log(experts)/epsilon + epsilon*days
    regret_bound = math.log(experts)/epsilon + epsilon*days
    return total_costs, regret, cost_bound, regret_bound, experts_costs



if __name__ == "__main__":
    experts_num = 4
    x_axis = []
    wma_mistakes, wma_regret, mwu_costs, mwu_regrets = [], [], [], []
    wma_mistakes_bound, wma_regret_bound, mwu_costs_bound, mwu_regrets_bound = [], [], [], []
    experts_outcomes = dict()
    # experts_costs = dict()

    # set epsilon = 0.1, change day
    num_of_days = 10
    while num_of_days < 200:
        
        x_axis.append(num_of_days)
        
        # generate problem instances
        costs, outcomes = expert.adversary(num_of_days, experts_num)
        
        a, b, c, d, e = wma(num_of_days, outcomes, experts_num)
        wma_mistakes.append(a)
        wma_regret.append(b)
        wma_mistakes_bound.append(c)
        wma_regret_bound.append(d)
        for i in range(experts_num):
            if i not in experts_outcomes.keys():
                experts_outcomes[i] = []
                pass
            experts_outcomes[i].append(e[i])
            pass
        
        
        a1, b1, c1, d1, e1 = mwu(num_of_days, costs, experts_num, 0.8)
        mwu_costs.append(a1)
        mwu_regrets.append(b1)
        mwu_costs_bound.append(c1)
        mwu_regrets_bound.append(d1)
        # for i in range(experts_num):
        #     if i not in experts_costs.keys():
        #         experts_costs[i] = []
        #         pass
        #     experts_costs[i].append(e1[i])
        #     pass
        
        num_of_days += 2
        pass
    
    # plot 1
    plt.plot(x_axis, wma_mistakes, label="real mistakes")
    plt.plot(x_axis, wma_mistakes_bound, label="bounds")
    for i in range(experts_num):
        plt.plot(x_axis, experts_outcomes[i], label=f"expects{i+1}'s mistakes")
        pass
    plt.xlabel('x - days')
    plt.ylabel('y - mistakes')
    plt.title('weighted majority algorithm - mistakes')
    plt.legend()
    plt.show()
    
    # plot 2
    plt.plot(x_axis, wma_regret, label="real regrets")
    plt.plot(x_axis, wma_regret_bound, label="bounds")
    print(wma_regret)
    plt.xlabel('x - days')
    plt.ylabel('y - regrets')
    plt.title('weighted majority algorithm - regrets')
    plt.legend()
    plt.show()
    
    # plot 3
    plt.plot(x_axis, mwu_costs, label="total expected costs")
    plt.plot(x_axis, mwu_costs_bound, label="bounds")
    # for i in range(experts_num):
    #     plt.plot(x_axis, experts_costs[i], label=f"expects{i+1}'s costs")
    #     pass
    plt.xlabel('x - days')
    plt.ylabel('y - costs')
    plt.title('multiplicative weights update algorithm - costs')
    plt.legend()
    plt.show()
    
    # plot 4
    plt.plot(x_axis, mwu_regrets, label="real regrets")
    plt.plot(x_axis, mwu_regrets_bound, label="bounds")
    plt.xlabel('x - days')
    plt.ylabel('y - regrets')
    plt.title('multiplicative weights update algorithm - regrets')
    plt.legend()
    plt.show()
    
    
    # set day = 10, change epsilon, clean the data list
    epsilon = 0.01
    x_axis = []
    mwu_costs, mwu_regrets, mwu_costs_bound, mwu_regrets_bound = [], [], [], []
    # experts_costs = dict()
    while epsilon < 1:
        
        x_axis.append(epsilon)
        # generate problem instances
        costs, outcomes = expert.adversary(50, experts_num)
        
        a1, b1, c1, d1, e1 = mwu(50, costs, experts_num, epsilon)
        mwu_costs.append(a1)
        mwu_regrets.append(b1)
        mwu_costs_bound.append(c1)
        mwu_regrets_bound.append(d1)
        # for i in range(experts_num):
        #     if i not in experts_costs.keys():
        #         experts_costs[i] = []
        #         pass
        #     experts_costs[i].append(e1[i])
        #     pass
        
        epsilon += 0.01
        pass
    
    # plot 5
    plt.plot(x_axis, mwu_costs, label="total expected costs")
    plt.plot(x_axis, mwu_costs_bound, label="bounds")
    # for i in range(experts_num):
    #     plt.plot(x_axis, experts_costs[i], label=f"expects{i+1}'s costs")
    #     pass
    plt.xlabel('x - epsilon')
    plt.ylabel('y - costs')
    plt.title('multiplicative weights update algorithm - costs')
    plt.legend()
    plt.show()
    
    # plot 6
    plt.plot(x_axis, mwu_regrets, label="real regrets")
    plt.plot(x_axis, mwu_regrets_bound, label="bounds")
    plt.xlabel('x - epsilon')
    plt.ylabel('y - regrets')
    plt.title('multiplicative weights update algorithm - regrets')
    plt.legend()
    plt.show()


    
    
    
    
    