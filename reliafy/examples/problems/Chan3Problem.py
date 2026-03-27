# Description: Chan and Low 2011 problem 3 page 1399
# https://onlinelibrary.wiley.com/doi/full/10.1002/nag.1057

import math

import numpy as np


def Problem():

    Problem = {
        "Name": "Chan3",
        "LimitStateFunction": LSF,
        "LSFisVectorized": True,
        "LSFisSmooth": True,
        "LSFreturnsGradient": True,
        "LSFreturnsHessian": False,
        "LSFreturnsLandR": True,
        "DeterministicVariables": {
            "name": ["d", "L", "a"],
            "value": [0.5, 10.0, 1.0],
        },
        "StochasticVariables": {
            "name": ["Qv", "cp", "cs"],
            "type": ["beta", "beta", "beta"],
            "cor_list": [["cp", "cs", 0.5]],
            "param1": [5.0, 1.5, 1.5],
            "param2": [1.5, 5.0, 5.0],
            "lb": [90.0, 27.125, 19.375],
            "ub": [441.0, 61.25, 43.75],
        },
        "LSFplot": {
            "x_var": "Qv",
            "x_param": "value",
            "x_lim": [390.0, 400.0],
            "y_var": "cp",
            "y_param": "value",
            "y_lim": [30.0, 40.0],
            "z_var": "cs",
        },
        "ISplot": {
            "x_var": "Qv",
            "x_lim": [390.0, 480.0],
            "y_var": "cp",
            "y_lim": [20.0, 40.0],
        },
    }

    return Problem


def LSF(X, D):
    # X is a (n, m) matrix where n is the number of stochatic variables and
    # m is the number of samples
    # If X.ndim == 1 then X is a (n,) matrix where n is the number of
    # stochastic variables
    # D is a (n,) array where n is the number of deterministic variables

    Qv, cp, cs = X
    d, L, a = D

    Ap = math.pi * d**2 / 4
    As = math.pi * d * L

    Resistance = 9 * cp * Ap + a * cs * As
    Load = Qv

    g = Resistance - Load

    gg = []
    gh = []
    if X.ndim == 1:
        gg = np.array(
            [
                -1.0,
                9 * Ap,
                a * As,
            ]
        )

    return g, gg, gh, Load, Resistance


# Path: Problems/Chan3Problem.py
