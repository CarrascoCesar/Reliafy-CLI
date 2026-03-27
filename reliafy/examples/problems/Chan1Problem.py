# Author: Cesar Carrasco
# Description: Chan and Low 2011 problem 1 page 1392
# https://onlinelibrary.wiley.com/doi/full/10.1002/nag.1057

import numpy as np


def Problem():

    Problem = {
        "Name": "Chan1",
        "LimitStateFunction": LSF,
        "LSFisVectorized": True,
        "LSFisSmooth": True,
        "LSFreturnsGradient": True,
        "LSFreturnsHessian": False,
        "LSFreturnsLandR": True,
        "DeterministicVariables": {
            "name": ["B", "m", "I1", "I2", "If", "dHlim"],
            "value": [30.0, 4.0, 0.073, 0.089, 0.95, 50],
        },
        "StochasticVariables": {
            "name": ["q", "v", "E"],
            "type": ["normal", "normal", "normal"],
            "mean": [280.0, 0.25, 50.0],
            "std": [40.0, 0.08, 2.5],
        },
        "LSFplot": {
            "x_var": "q",
            # "x_param": "value",
            "x_lim": [240.0, 380.0],
            # "x_func": lambda S, D: S[0],
            # "x_label": "q",
            "y_var": "v",
            # "y_param": "value",
            "y_lim": [0.10, 0.35],
            # "y_func": lambda S, D: S[1],
            # "y_label": "v",
            "z_var": "dHlim",
        },
    }

    return Problem


def LSF(X, D):
    # X is a (n, m) matrix where n is the number of stochatic variables and
    # m is the number of samples
    # If X.ndim == 1 then X is a (n,) matrix where n is the number of
    # stochastic variables
    # D is a (n,) array where n is the number of deterministic variables

    q, v, E = X

    B, m, I1, I2, If, R = D  # R = dHlim

    Is = I1 + I2 * (1.0 - 2.0 * v) / (1.0 - v)
    L = q * 0.5 * B * (1.0 - v**2.0) * m * Is * If / E

    g = R - L

    gg = []
    gh = []

    if X.ndim == 1:
        gg = np.array(
            [
                (-0.5 * B * If * Is * m * (1.0 - v**2)) / E,
                (2.0 * B * If * m * q * (I1 * (-0.5 + 0.5 * v) * v + I2 * (-0.25 - 0.75 * v + 1.0 * v**2)))
                / (E * (-1.0 + v)),
                (-0.5 * B * If * Is * m * q * (-1.0 + v**2)) / E**2,
            ]
        )

    return g, gg, gh, L, R


# Path: Problems/Chan1Problem.py
