# Description: Ang and Tang Vol II 1990 pg. 428 problem 6.24

import numpy as np


def Problem():

    Problem = {
        "Name": "Ang and Tang 6.24",
        "LimitStateFunction": LSF,
        "LSFisVectorized": True,
        "LSFisSmooth": True,
        "LSFreturnsGradient": True,
        "LSFreturnsHessian": True,
        "LSFreturnsLandR": False,
        "DeterministicVariables": {
            "name": [],
            "value": [],
        },
        "StochasticVariables": {
            "name": ["N", "M", "Y"],
            "type": ["normal", "normal", "normal"],
            "mean": [1.0, 0.05, 25.8],
            "cv": [0.10, 0.21, 0.26],
        },
        "DesignProblem": {
            "TargetPf": 0.02275,
            "fractiles": [0.5, 0.5, 0.5],
            "cases": {
                "1": {
                    "name": ["N", "M", "Y"],
                    "mean": [1.0, 0.01, 126.0],
                    "cv": [0.10, 0.21, 0.26],
                },
                "2": {
                    "name": ["N", "M", "Y"],
                    "mean": [1.0, 0.05, 25.8],
                    "cv": [0.10, 0.21, 0.26],
                },
                "3": {
                    "name": ["N", "M", "Y"],
                    "mean": [1.0, 0.10, 13.3],
                    "cv": [0.10, 0.21, 0.26],
                },
                "4": {
                    "name": ["N", "M", "Y"],
                    "mean": [1.0, 0.50, 3.22],
                    "cv": [0.10, 0.21, 0.26],
                },
            },
        },
        "LSFplot": {
            "x_var": "N",
            "x_param": "value",
            "x_lim": [0.5, 1.5],
            "x_func": lambda S, D: S[0],
            "x_label": "Correction: N",
            "y_var": "M",
            "y_param": "value",
            "y_lim": [0.01, 0.1],
            "y_func": lambda S, D: S[1],
            "y_label": "Pressure Ratio: M",
            "z_var": "Y",
        },
        "ISplot": {
            "x_var": "Y",
            "x_lim": [22, 28],
            "y_var": "M",
            "y_lim": [0.01, 0.1],
        },
    }

    return Problem


def LSF(X, D):
    # X is a (n, m) matrix where n is the number of stochatic variables and
    # m is the number of samples
    # If X.ndim == 1 then X is a (n,) matrix where n is the number of
    # stochastic variables
    # D is a (n,) array where n is the number of deterministic variables
    N, M, Y = X

    # Limit state
    g = 1 - N * Y * np.log10(1 + M)

    L = []  # Load
    R = []  # Resistance

    # Gradient and Hessian of limit state
    gg = []
    gh = []

    if X.ndim == 1:
        # Gradient of limit state
        gg = np.array([-Y * np.log10(1 + M), -N * Y / (1 + M) / np.log(10), -N * np.log10(1 + M)])

        # # Hessian of limit state
        gh = np.array(
            [
                [0, -Y / (1 + M) / np.log(10), -np.log10(1 + M)],
                [-Y / (1 + M) / np.log(10), N * Y / (1 + M) ** 2 / np.log(10), -N / (1 + M) / np.log(10)],
                [-np.log10(1 + M), -N / (1 + M) / np.log(10), 0],
            ]
        )

    return g, gg, gh, L, R


# Path: Problems/AT625Problem.py
