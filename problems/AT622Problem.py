# Author: Cesar Carrasco
# Description: Ang and Tang Vol II 1990 pg. 423 problem 6.22

import numpy as np


def Problem():

    Problem = {
        "Name": "AT6.22",
        "LimitStateFunction": LSF,
        "LSFisVectorized": True,
        "LSFisSmooth": True,
        "LSFreturnsGradient": True,
        "LSFreturnsHessian": True,
        "LSFreturnsLandR": True,
        "DeterministicVariables": {
            "name": ["To"],
            "value": [180],
        },
        "StochasticVariables": {
            "name": ["x1", "x2", "x3"],
            "type": ["normal", "normal", "normal"],
            "mean": [40, 15, 50],
            "std": [10, 5, 10],
            "cor_list": [["x1", "x2", 0.5], ["x1", "x3", 0.5], ["x2", "x3", 0.5]],
        },
        "DesignProblem": {
            "DesignObjectiveFunction": DOF,
            "DOFisVectorized": True,
            "DOFisSmooth": True,
            "DOFreturnsGradient": True,
            "DOFreturnsHessian": True,
            "DesignVariables": ["To"],
            "InitialGuess": [100.0],
            "lb": [0.0],
            "ub": [200],
            "TargetBeta": 1.96,
            "fractiles": [0.5, 0.5, 0.5],
        },
        "LSFplot": {
            "x_var": "x1",
            "x_param": "value",
            "x_lim": [30.0, 50.0],
            "x_func": lambda S, D: S[0],
            "x_label": "Time: (x1)",
            "y_var": "x2",
            "y_param": "value",
            "y_lim": [10.0, 20.0],
            "y_func": lambda S, D: S[1],
            "y_label": "Time: (x2)",
        },
    }

    return Problem


def DOF(d, D):
    # Objective function returns the function value, gradient and hessian
    # d is a (n,) array where n is the number of design variables
    # D is a (m,) array where m is the number of deterministic variables exluding the design variables
    To = d
    f = To

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
    x1, x2, x3 = X
    To = D

    L = x1 + x2 + x3  # Load
    R = To  # Resistance

    # Limit state
    g = R - L

    # Gradient and Hessian of limit state
    gg = []
    gh = []

    if X.ndim == 1:
        # Gradient of limit state
        gg = np.array([-1.0, -1.0, -1.0])

        # Hessian of limit state
        gh = np.zeros((3, 3))

    return g, gg, gh, L, R


# Path: ./Problems/AT622Problem.py
