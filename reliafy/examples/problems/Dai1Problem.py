# https://www.sciencedirect.com/science/article/pii/S0167473014000162

import numpy as np


def Problem():

    Problem = {
        "Name": "Dai 1",
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
            "name": ["X1", "X2"],
            "type": ["normal", "normal"],
            "mean": [0.0, 0.0],
            "std": [1.0, 1.0],
        },
        "LSFplot": {
            "x_var": "X1",
            "x_lim": [-8, 8],
            "y_var": "X2",
            "y_lim": [-8, 8],
        },
        "ISplot": {
            "x_var": "X1",
            "x_lim": [-8, 8],
            "y_var": "X2",
            "y_lim": [-8, 8],
        },
    }

    return Problem


def LSF(X, D):
    # X is a (n, m) matrix where n is the number of stochatic variables and
    # m is the number of samples
    # If X.ndim == 1 then X is a (n,) matrix where n is the number of
    # stochastic variables
    # D is a (n,) array where n is the number of deterministic variables
    X1, X2 = X

    # Limit state
    g1 = 3 + (X1 - X2)**2/10 - (X1 + X2) / np.sqrt(2)
    g2 = 3 + (X1 - X2)**2/10 + (X1 + X2) / np.sqrt(2)
    g3 = X1 - X2 + 7 / np.sqrt(2)
    g4 = X2 - X1 + 7 / np.sqrt(2)
    g = np.minimum(np.minimum(g1, g2), np.minimum(g3, g4))

    # Load and resistance
    L = []
    R = []

    # Gradient and Hessian of limit state
    gg = []
    gh = []

    return g, gg, gh, L, R
