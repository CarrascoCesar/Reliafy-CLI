# Description: Ang and Tang Vol II 1990 pg. 368 problem 6.10


import numpy as np


def Problem():

    Problem = {
        "Name": "AT610",
        "LimitStateFunction": LSF,
        "LSFisVectorized": True,
        "LSFisSmooth": True,
        "LSFisParallelizable": True,
        "LSFreturnsGradient": True,
        "LSFreturnsHessian": True,
        "LSFreturnsLandR": True,
        "DeterministicVariables": {
            "name": [],
            "value": [],
        },
        "StochasticVariables": {
            "name": ["Y", "Z", "M"],
            "type": ["lognormal", "lognormal", "gumbelmax"],
            "cor_list": [["Y", "Z", 0.4]],
            "mean": [40.0, 50.0, 1000.0],
            "std": [5.0, 2.5, 200.0],
        },
        "LSFplot": {
            "x_var": "Y",
            "x_lim": [20.0, 50.0],
            "y_var": "M",
            "y_lim": [900, 1900],
            "z_var": "Z",
        },
        "RFADplot": {
            "x_var": "Y",
            "x_param": "mean",
            "x_lim": [20.0, 50.0],
            "y_var": "M",
            "y_param": "mean",
            "y_lim": [900, 1900],
        },
        "ISplot": {
            "x_var": "Y",
            "y_var": "M",
        },
    }

    return Problem


def LSF(X, D):
    # X is a (n, m) matrix where n is the number of stochatic variables and
    # m is the number of samples
    # If X.ndim == 1 then X is a (n,) matrix where n is the number of
    # stochastic variables
    # D is a (n,) array where n is the number of deterministic variables
    Y, Z, M = X

    L = M  # Load
    R = Y * Z  # Resistance

    # Limit state
    g = R - L

    # Gradient and Hessian of limit state
    gg = []
    gh = []
    if X.ndim == 1:
        # Limit state gradient
        gg = np.array([Z, Y, -1.0])

        # Limit state Hessian
        gh = np.array([[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]])

    return g, gg, gh, L, R


# Path: Problems/AT610Problem.py
