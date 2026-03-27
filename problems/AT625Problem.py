# Description: Ang and Tang Vol II 1990 pg. 431 problem 6.25

import numpy as np


def Problem():

    Problem = {
        "Name": "Ang and Tang 6.25",
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
            "name": ["f", "N", "Y", "Q"],
            "type": ["normal", "normal", "normal", "GumbelMax"],
            "mean": [0.0246 * 100, 1.1 * 10, 9.76, 1.0e4],
            "cv": [0.11, 0.11, 0.04, 0.25],
            "cor_list": [["Y", "N", 0.5]],
        },
        "DesignProblem": {
            "TargetBeta": 1.28,
            "fractiles": [0.5, 0.5, 0.5, 0.5],
        },
        "LSFplot": {
            "x_var": "f",
            "x_param": "value",
            "x_lim": [0.023 * 100, 0.026 * 100],
            "x_func": lambda S, D: S[0],
            "x_label": "Friction: (f)",
            "y_var": "N",
            "y_param": "value",
            "y_lim": [1.0 * 10, 1.2 * 10],
            "y_func": lambda S, D: S[1],
            "y_label": "Correction: (N)",
        },
        "ISplot": {
            "x_var": "f",
            "y_var": "Q",
        },
    }

    return Problem


def LSF(X, D):
    # X is a (n, m) matrix where n is the number of stochatic variables and
    # m is the number of samples
    # If X.ndim == 1 then X is a (n,) matrix where n is the number of
    # stochastic variables
    # D is a (n,) array where n is the number of deterministic variables

    f, N, Y, Q = X

    # Limit state
    Load = Q
    Resistance = 201.6 * N * f ** (-0.5) * Y
    g = Resistance - Load

    # Gradient and Hessian of limit state
    gg = []
    gh = []

    if X.ndim == 1:
        # Gradient of limit state
        gg = np.array([201.6 * (-0.5) * (f**-1.5) * N * Y, 201.6 * (f**-0.5) * Y, 201.6 * (f**-0.5) * N, -1.0])

        # Hessian of limit state
        gh = np.array(
            [
                [
                    201.6 * (+0.75) * (f**-2.5) * N * Y,
                    201.6 * (-0.50) * (f**-1.5) * Y,
                    201.6 * (-0.50) * (f**-1.5) * N,
                    0.0,
                ],
                [201.6 * (-0.5) * (f**-1.5) * Y, 0.0, 201.6 * (f**-0.5), 0.0],
                [201.6 * (-0.5) * (f**-1.5) * N, 201.6 * (f**-0.5), 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0],
            ]
        )

    return g, gg, gh, Load, Resistance


# Path: Problems/AT625Problem.py
