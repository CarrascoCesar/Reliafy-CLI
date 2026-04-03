# Author: Cesar Carrasco
# Description: Robust reliability-based design approach by inverse FORM with adaptive conjugate search algorithm, Ji et al. Problem 2
# https://onlinelibrary.wiley.com/doi/10.1002/nag.3524

import numpy as np


def Problem():

    Problem = {
        "Name": "Ji et al. Problem 2",
        "LimitStateFunction": LSF,
        "LSFisVectorized": True,
        "LSFisSmooth": True,
        "LSFreturnsGradient": True,
        "LSFreturnsHessian": True,
        "LSFreturnsLandR": True,
        "DeterministicVariables": {
            "name": ["C", "Lambda"],
            "value": [18, 1],
        },
        "StochasticVariables": {
            "name": ["x1", "x2"],
            "type": ["normal", "normal"],
            "mean": [1, 9.9],
            # "std": [0.5, 5],
            "cv": [0.5, 0.5050505],  # knowing cv makes more sense (cheating?!?!)
        },
        "DesignProblem": {
            "DesignObjectiveFunction": DOF,
            "DOFisVectorized": True,
            "DOFreturnsGradient": True,
            "DOFreturnsHessian": True,
            "DesignVariables": ["Lambda"],
            "InitialGuess": [10],
            "lb": [0.0],
            "ub": [np.inf],
            "TargetBeta": 2.3,
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

    x1, x2 = X
    C, Lambda = D

    L = C  # Load
    R = (x1 * Lambda) ** 3 + ((x1 * Lambda) ** 2) * x2 + x2**3  # Resistance

    # Limit state
    g = R - L

    # Gradient and Hessian of limit state
    gg = []
    gh = []

    if X.ndim == 1:
        # Gradient of limit state
        gg = np.array(
            [
                3 * (x1 * Lambda) ** 2 * Lambda + 2 * x1 * Lambda * x2 * Lambda,
                (x1 * Lambda) ** 2 + 3 * x2**2,
            ]
        )

        # Hessian of limit state
        gh = np.array(
            [
                [6 * x1 * Lambda**3 + 2 * Lambda * x2 * Lambda, 2 * x1 * Lambda * Lambda],
                [2 * x1 * Lambda * Lambda, 6 * x2],
            ]
        )

    return g, gg, gh, L, R


# Path: Problems/Ji2Problem.py
