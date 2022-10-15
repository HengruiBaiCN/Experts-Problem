from ast import Pow
from cmath import log
from random import choices
import random
from itertools import chain, combinations
from re import A
import time
import matplotlib.pyplot as plt
import math

import numpy as np


def A(day, outcomes):
    """_summary_

    Args:
        day (int): the current day
        outcomes (dictionary): the real trend/outcomes in each day

    Returns:
        int: the trend: 0 or 1
    """
    prediction = random.randint(0, 1)
    return prediction


def B(day, outcomes):
    """_summary_

    Args:
        day (int): the current day
        outcomes (dictionary): the real trend/outcomes in each day

    Returns:
        int: the trend: 0 or 1
    """
    if day == 0:
        return outcomes["zero"]
    prediction = outcomes[day-1]
    return prediction


def C(day, outcomes):
    """_summary_

    Args:
        day (int): the current day
        outcomes (dictionary): the real trend/outcomes in each day

    Returns:
        int: the trend: 0 or 1
    """
    theta = 0.05
    correct = outcomes[day]
    wrong = 0
    if correct != 1:
        wrong = 1
        pass
    prediction = choices([wrong, correct], [0.5 - theta, 0.5 + theta])[0]
    return prediction

def D(day, outcomes):
    """_summary_
    My own experts: pessimist, believe the market will keep going down
    Args:
        day (int): the current day
        outcomes (dictionary): the real trend/outcomes in each day

    Returns:
        int: the trend: 0 or 1
    """
    prediction = 0
    return prediction

def call_experts(e, d, o):
    """_summary_

    Args:
        num (int): index correspond to different expert
        d (int): the current day
        o (dictionary): the real trend/outcomes in each day

    Returns:
        int: the prediction of one of experts
    """
    res = 0
    if e == 0:
        res = A(d, o)
        pass
    elif e == 1:
        res = B(d, o)
        pass
    elif e == 2:
        res = C(d, o)
        pass
    else:
        res = D(d, o)
        pass
    return res


def adversary(days, experts):
    """_summary_
    Generate the outcome of each day based on a uniform distribution
    Args:
        days (_type_): _description_
        experts (_type_): _description_

    Returns:
        _type_: _description_
    """
    costs = dict()
    outcomes = dict()
    day0 = random.randint(0, 1)
    outcomes["zero"] = day0
    for t in range(days):
        res =random.randint(0, 1)
        cost = []
        outcomes[t] = res
        for i in range(experts):
            cost.append(random.uniform(-1, 1))
            pass
        costs[t] = cost
        pass
    return costs, outcomes