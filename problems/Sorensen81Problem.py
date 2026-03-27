# Description: Sorensen, Notes in Structural Reliability Theory And Risk Analysis Problem 1, chapter 8, page 141
# https://filelist.tudelft.nl/TBM/Over%20faculteit/Afdelingen/Values%2C%20Technology%20and%20Innovation/People/Full%20Professors/Pieter%20van%20Gelder/Citations/citatie215.pdf

# Note: Partial safety factors in Sorensen depend on weather the variables are a load or a resistance effect
# If a variable is a load, the partial safety factor is calculated by dividing the design value by the characteristic value
# If a variable is a resistance effect, the partial safety factor is calculated by dividing the characteristic value by the its design value
# However, in this code the partial safety factors are calculated by dividing the design value by the characteristic value regardless of the variable type

import numpy as np


def Problem():

    Problem = {
        "Name": "Sorensen 8.1",
        "LimitStateFunction": LSF,
        "LSFisVectorized": True,
        "LSFisSmooth": True,
        "LSFreturnsGradient": True,
        "LSFreturnsHessian": True,
        "LSFreturnsLandR": True,
        "DeterministicVariables": {
            "name": ["z"],
            "value": [10],
        },
        "StochasticVariables": {
            "name": ["R", "G", "Q"],
            "type": ["LogNormal", "Normal", "GumbelMax"],
            "mean": [1.0, 2.0, 3.0],
            "cv": [0.15, 0.10, 0.4],
        },
        "DesignProblem": {
            "DesignObjectiveFunction": DOF,
            "DOFisVectorized": True,
            "DOFisSmooth": True,
            "DOFreturnsGradient": True,
            "DOFreturnsHessian": True,
            "DesignVariables": ["z"],
            "InitialGuess": [1],
            "lb": [0.0],
            "ub": [np.inf],
            "TargetBeta": 3.8,
            "fractiles": [0.05, 0.5, 0.98],
        },
        "LSFplot": {
            "x_var": "R",
            "x_param": "value",
            "x_lim": [0.8, 1.2],
            "x_func": lambda S, D: S[0],
            "x_label": "Resistance: R",
            "y_var": "G",
            "y_param": "value",
            "y_lim": [1.5, 2.5],
            "y_func": lambda S, D: S[1] + S[2],
            "y_label": "Load: G + Q",
        },
        "ISplot": {
            "x_var": "R",
            "x_lim": [0.8, 1.2],
            "x_label": "Resistance: R",
            "y_var": "G",
            "y_lim": [1.5, 2.5],
            "y_label": "Load: G",
        },
    }

    return Problem


def DOF(d, D):
    # Objective function returns the function value, gradient and hessian
    # d is a (n,) design variable array where n is the number of design variables
    # D is a (m,) deterministic variable array where m is the number of deterministic variables excluding the design variables

    z = d
    f = z

    g = []
    h = []
    if d.ndim == 1:
        g = np.array([1.0])
        h = np.array([[0.0]])

    return f, g, h


def LSF(X, D):
    # X is a (n, m) matrix where n is the number of stochatic variables and
    # m is the number of samples
    # If X.ndim == 1 then X is a (n,) matrix where n is the number of
    # stochastic variables
    # D is a (n,) array where n is the number of deterministic variables

    z = D
    R, G, Q = X

    # Limit state
    Resistance = z * R
    Load = G + Q

    g = Resistance - Load

    # Gradient and Hessian of limit state
    gg = []
    gh = []

    if X.ndim == 1:
        gg = np.array([z, -1, -1])
        gh = np.zeros((3, 3))

    return g, gg, gh, Load, Resistance


# Path: ./problems/Sorensen81Problem.py
