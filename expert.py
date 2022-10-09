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


def A(day, history):
    """_summary_
    Expert who makes a uniformly random prediction all the time
    Args:
        days (_type_): _description_
        history (_type_): _description_

    Returns:
        _type_: _description_
    """
    prediction = random.randint(0, 1)
    return prediction

def B(day, outcomes):
    """_summary_
    Expert who always predicts the same as the outcome of the previous day
    Args:
        days (_type_): _description_
        history (_type_): _description_

    Returns:
        _type_: _description_
    """
    prediction = outcomes[day-1]
    return prediction

def C(day, outcomes):
    """_summary_
    Expert who predicts the future the outcome of the next day with accuracy of 1/2 + δ, where δ is a small constant
    Args:
        days (_type_): _description_
        history (_type_): _description_

    Returns:
        _type_: _description_
    """
    theta = 0.1
    correct = outcomes[day]
    wrong = 0
    if correct != 1:
        wrong = 1
        pass
    prediction = choices([wrong, correct], [0.5 - theta, 0.5 + theta])
    return prediction

def D(days, history):
    """_summary_
    My own expert: pessimist, believe the stock market will go down forever.
    Args:
        days (_type_): _description_
        history (_type_): _description_

    Returns:
        _type_: _description_
    """
    prediction = 0
    return prediction


def adversary(days, epsilon):
    """_summary_
    Generate the outcome of each day based on a uniform distribution
    Args:
        days (_type_): _description_
        epsilon (_type_): _description_

    Returns:
        _type_: _description_
    """
    outcomes = dict()
    for t in range(1, days):
        res =random.randint(0, 1)
        outcomes[t] = res
    return None