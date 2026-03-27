# https://people.duke.edu/~hpgavin/risk/Au-1999.pdf

import numpy as np


def Problem():

    Problem = {
        "Name": "AU3",
        "LimitStateFunction": LSF,
        "LSFisVectorized": True,
        "LSFisSmooth": True,
        "LSFisParallelizable": True,
        "LSFreturnsGradient": False,
        "LSFreturnsHessian": False,
        "LSFreturnsLandR": False,
        "DeterministicVariables": {
            "name": [],
            "value": [],
        },
        "StochasticVariables": {
            "name": ["T1", "T2", "T3", "T4", "T5", "T6", "T7"],
            "type": ["normal", "normal", "normal", "normal", "normal", "gumbelmax", "gumbelmax"],
            "mean": [60.0, 60.0, 60.0, 60.0, 60.0, 20.0, 25.0],
            "std": [6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 7.5],
        },
        "LSFplot": {
            "x_var": "T6",
            "x_lim": [0.0, 70.0],
            "y_var": "T7",
            "y_lim": [0.0, 70.0],
        },
        "ISplot": {
            "x_var": "T6",
            "y_var": "T7",
        },
    }

    return Problem


def LSF(X, D):
    # X is a (n, m) matrix where n is the number of stochatic variables and
    # m is the number of samples
    # If X.ndim == 1 then X is a (n,) matrix where n is the number of
    # stochastic variables
    # D is a (n,) array where n is the number of deterministic variables
    T1, T2, T3, T4, T5, T6, T7 = X

    # Limit state
    g1 = T1 + 2 * T3 + 2 * T4 + T5 - 5 * T6 - 5 * T7
    g2 = T1 + 2 * T2 + T4 + T5 - 5 * T6
    g3 = T2 + 2 * T3 + T4 - 5 * T7
    g = np.minimum(g1, np.minimum(g2, g3))

    # Load and resistance
    L = []
    R = []

    # Gradient and Hessian of limit state
    gg = []
    gh = []

    return g, gg, gh, L, R
