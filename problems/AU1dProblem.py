# https://people.duke.edu/~hpgavin/risk/Au-1999.pdf

import numpy as np


def Problem():

    Problem = {
        "Name": "AU1d",
        "LimitStateFunction": LSF,
        "LSFisVectorized": True,
        "LSFisSmooth": True,
        "LSFisParallelizable": True,
        "LSFreturnsGradient": True,
        "LSFreturnsHessian": True,
        "LSFreturnsLandR": False,
        "DeterministicVariables": {
            "name": ["c"],
            "value": [5.0],
        },
        "StochasticVariables": {
            "name": ["T1", "T2"],
            "type": ["normal", "normal"],
            "mean": [0.0, 0.0],
            "std": [1.0, 1.0],
        },
        "LSFplot": {
            "x_var": "T1",
            "x_lim": [-4.0, 4.0],
            "y_var": "T2",
            "y_lim": [-0.0, 6.0],
        },
        "ISplot": {
            "x_var": "T1",
            "x_lim": [-3.0, 3.0],
            "y_var": "T2",
            "y_lim": [+0.0, 6.0],
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

    # Limit state
    g = 3 - T2 + (4 * T1) ** 4

    # Load and resistance
    L = []
    R = []

    # Gradient and Hessian of limit state
    gg = []
    gh = []

    if X.ndim == 1:
        gg = np.array([16 * (4 * T1) ** 3, -1])
        gh = np.array(
            [
                [16 * 3 * (4**3) * T1**2, 0],
                [0, 0],
            ]
        )

    return g, gg, gh, L, R
