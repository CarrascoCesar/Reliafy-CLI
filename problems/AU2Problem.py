# https://people.duke.edu/~hpgavin/risk/Au-1999.pdf

import numpy as np


def Problem():

    Problem = {
        "Name": "AU2",
        "LimitStateFunction": LSF,
        "LSFisVectorized": True,
        "LSFisSmooth": True,
        "LSFisParallelizable": True,
        "LSFreturnsGradient": False,
        "LSFreturnsHessian": False,
        "LSFreturnsLandR": False,
        "DeterministicVariables": {
            "name": ["c"],
            "value": [5],
        },
        "StochasticVariables": {
            "name": ["T1", "T2"],
            "type": ["normal", "normal"],
            "mean": [0.0, 0.0],
            "std": [1.0, 1.0],
        },
        "LSFplot": {
            "x_var": "T1",
            "x_lim": [-5.0, 5.0],
            "y_var": "T2",
            "y_lim": [-5.0, 5.0],
        },
        "ISplot": {
            "x_var": "T1",
            "x_lim": [-5.0, 5.0],
            "y_var": "T2",
            "y_lim": [-5.0, 5.0],
        },
    }

    return Problem


def LSF(X, D):
    # X is a (n, m) matrix where n is the number of stochatic variables and
    # m is the number of samples
    # If X.ndim == 1 then X is a (n,) matrix where n is the number of
    # stochastic variables
    # D is a (n,) array where n is the number of deterministic variables
    T1, T2 = X
    c = D

    # Limit state
    g1 = c - 1 - T2 + np.exp(-(T1**2) / 10) + (T1 / 5) ** 4
    g2 = (c**2) / 2 - T1 * T2
    g = np.minimum(g1, g2)

    # Load and resistance
    L = []
    R = []

    # Gradient and Hessian of limit state
    gg = []
    gh = []

    return g, gg, gh, L, R
