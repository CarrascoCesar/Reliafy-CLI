# Author: Cesar Carrasco
# Description: Ang and Tang Vol II 1990 pg. 363 problem 6.8

import numpy as np


def Problem():

    Problem = {
        "Name": "AT68",
        "LimitStateFunction": LSF,
        "LSFisVectorized": True,
        "LSFisSmooth": True,
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
            "mean": [40, 50.0, 1000.0],
            "cv": [0.125, 0.05, 0.2],
        },
        "RFADplot": {
            "x_var": "Y",
            "x_param": "mean",
            "x_lim": [10.0, 70.0],
            "x_func": lambda S, D: S[0] * S[1],
            "x_label": "Resistance: \\mu(Y)*\\mu(Z)",
            "y_var": "M",
            "y_param": "mean",
            "y_lim": [500.0, 1500.0],
            "y_func": lambda S, D: S[2],
            "y_label": "Load: \\mu(M)",
        },
        "LSFplot": {
            "x_var": "Y",
            "x_lim": [30.0, 50.0],
            "x_func": lambda S, D: S[0] * S[1],
            "x_label": "Resistance: Y*Z",
            "y_var": "M",
            "y_lim": [800, 1200],
            "y_func": lambda S, D: S[2],
            "y_label": "Load: M",
        },
    }

    return Problem


def resistance(S, D):
    return S[0] * S[1]


def LSF(X, D):
    # X is a nxm matrix where n is the number of stochatic variables and m is the number of samples
    # If X.ndim == 1 then X is a (n,) matrix where n is the number of stochastic variables
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
        # Gradient of limit state
        gg = np.array([Z, Y, -1.0])

        # Hessian of limit state
        gh = np.array([[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]])

    return g, gg, gh, L, R


# Path: Problems/AT68Problem.py
