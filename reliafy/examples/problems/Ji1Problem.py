# Author: Cesar Carrasco
# Description: Robust reliability-based design approach by inverse FORM with adaptive conjugate search algorithm, Ji et al. Problem 1
# https://onlinelibrary.wiley.com/doi/10.1002/nag.3524

import numpy as np


def Problem():

    Problem = {
        "Name": "Ji et al. Problem 1",
        "LimitStateFunction": LSF,
        "LSFisVectorized": True,
        "LSFisSmooth": True,
        "LSFreturnsGradient": True,
        "LSFreturnsHessian": True,
        "LSFreturnsLandR": False,
        "DeterministicVariables": {
            "name": ["Lambda"],
            "value": [1.0],
        },
        "StochasticVariables": {
            "name": ["x1", "x2", "x3", "x4", "t"],
            "type": ["normal", "normal", "normal", "normal", "lognormal"],
            "mean": [0, 0, 0, 0, 1],
            "std": [1, 1, 1, 1, 0.8],
        },
        "DesignProblem": {
            "DesignObjectiveFunction": DOF,
            "DOFreturnsGradient": True,
            "DOFisVectorized": True,
            "DOFisSmooth": True,
            "DOFreturnsHessian": True,
            "DesignVariables": ["Lambda"],
            "InitialGuess": [0.4],
            "lb": [-10.0],
            "ub": [10.0],
            "TargetBeta": 2.0,
        },
    }

    return Problem


def DOF(d, D):
    # Objective function returns the function value, gradient and hessian
    # d is a (n,) array where n is the number of design variables
    # D is a (m,) array where m is the number of deterministic variables exluding the design variables

    Lambda = d
    f = Lambda

    g = []
    h = []
    if d.ndim == 1:
        g = np.array([1.0])
        h = np.array([[0.0]])

    return f, g, h


def LSF(X, D):
    # X is a nxm matrix where n is the number of stochatic variables and m is the number of samples
    # If X.ndim == 1 then X is a (n,) matrix where n is the number of stochastic variables
    # D is a (n,) array where n is the number of deterministic variables
    # print(X,D)
    x1, x2, x3, x4, t = X
    Lambda = D

    # Limit state
    g = np.exp(-t * Lambda * (x1 + 2 * x2 + 3 * x3)) - x4 + 1.5

    R = []
    L = []

    # Gradient and Hessian of limit state
    gg = []
    gh = []

    if X.ndim == 1:
        A = x1 + 2 * x2 + 3 * x3
        E = np.exp(-t * Lambda * A)

        # Gradient of limit state
        gg = np.array(
            [
                -t * Lambda * E,
                -2 * t * Lambda * E,
                -3 * t * Lambda * E,
                -1,
                -Lambda * A * E,
            ]
        )

        # Hessian of limit state
        coeffs = np.array([1, 2, 3])
        gh = np.zeros((5, 5))
        # x1, x2, x3 block
        for i in range(3):
            for j in range(3):
                gh[i, j] = coeffs[i] * coeffs[j] * (t * Lambda) ** 2 * E
        # x1, x2, x3 with t
        for i in range(3):
            gh[i, 4] = gh[4, i] = coeffs[i] * Lambda * E * (-1 + t * Lambda * A)
        # x4 derivatives
        gh[3, :] = 0
        gh[:, 3] = 0
        # t, t
        gh[4, 4] = Lambda**2 * A**2 * E

    return g, gg, gh, L, R


# Path: Problems/Ji2Problem.py
