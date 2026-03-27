# Description: The effect of corrosion defects on the burst pressure of pipelines, Netto et al. 2005
# https://www.sciencedirect.com/science/article/pii/S0143974X05000453
#
# Data from:
# Uncertainty in the Estimation of Partial Safety Factors for Different Steel-Grade Corroded Pipelines
# https://www.mdpi.com/2077-1312/11/1/177
import numpy as np


def Problem():
    Problem = {
        "Name": "Pipe Corrosion",
        "LimitStateFunction": corrosion_func,
        "LSFisVectorized": True,
        "LSFisSmooth": True,
        "LSFreturnsGradient": True,
        "LSFreturnsHessian": False,
        "LSFreturnsLandR": True,
        "DeterministicVariables": {
            "name": ["Xr"],
            "value": [1.0],
        },
        "StochasticVariables": {
            "name": ["Xm", "Y", "t", "Do", "d", "l", "Po"],
            "type": ["frechet", "lognormal", "normal", "normal", "weibull", "lognormal", "gumbelmax"],
            "mean": [1.0, 328.8, 6.450, 324, 1.00, 100, 9.10],
            "std": [0.17, 26.30, 0.064, 3.24, 0.17, 57, 0.64],
            "lb": np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]) + 0.0001,
            "ub": [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf],
            "constraints": [
                {"fun": d_over_t, "lb": [0.1], "ub": [0.8], "jac": d_over_t_gradient},
                {"fun": l_over_Do, "lb": [0.0], "ub": [1.5]},
            ],
        },
        "DesignProblem": {
            "DesignObjectiveFunction": DOF,
            "DOFisVectorized": True,
            "DOFisSmooth": True,
            "DOFreturnsGradient": True,
            "DOFreturnsHessian": True,
            "DesignVariables": ["Xr"],
            "InitialGuess": [0.5],
            "lb": [0.0],
            "ub": [10.0],
            "TargetBeta": 2.47,
            "useSORM": False,
            "fractiles": [0.05, 0.05, 0.5, 0.5, 0.5, 0.5, 0.95],
            "cases": {
                "Low Grade": {
                    "mean": [1.0, 328.8, 6.450, 324, 1.00, 100, 9.10],
                    "std": [0.17, 26.30, 0.064, 3.24, 0.17, 57, 0.64],
                },
                "Medium Grade": {
                    "mean": [1.0, 429.6, 6.350, 508, 1.00, 100, 7.44],
                    "std": [0.22, 34.40, 0.063, 5.08, 0.17, 57, 0.52],
                },
            },
        },
        "LSFplot": {
            "x_var": "t",
            "x_lim": [6.0, 7.0],
            "y_var": "d",
            "y_lim": [0.5, 1.5],
        },
        "ISplot": {
            "x_var": "Po",
            "y_var": "Y",
        },
    }

    return Problem


def d_over_t(X, D):
    # X is a nxm matrix where n is the number of stochatic variables and m is the number of samples
    # D is a (n,) array where n is the number of deterministic variables
    Xm, Y, t, Do, d, l, Po = X
    Xr = D

    g = d / t

    return g


def d_over_t_gradient(X, D):
    Xm, Y, t, Do, d, l, Po = X
    Xr = D

    gg = np.array([0.0, 0.0, -d / (t**2), 0.0, 1.0 / t, 0.0, 0.0])

    return gg


def l_over_Do(X, D):
    # X is a nxm matrix where n is the number of stochatic variables and m is the number of samples
    # D is a (n,) array where n is the number of deterministic variables
    Xm, Y, t, Do, d, l, Po = X
    Xr = D

    g = l / Do

    return g


def DOF(d, D):
    # Objective function, gradient vector and Hessian matrix
    Xr = d
    f = Xr
    g = []
    h = []
    if d.ndim == 1:
        g = np.array([1.0])
        h = np.array([[0.0]])

    return f, g, h


def corrosion_func(X, D):
    # X is a (n, m) matrix where n is the number of stochatic variables and
    # m is the number of samples
    # If X.ndim == 1 then X is a (n,) matrix where n is the number of
    # stochastic variables
    # D is a (n,) array where n is the number of deterministic variables

    Xm, Y, t, Do, d, l, Po = X
    Xr = D

    # Limit state
    Load = Po
    Resistance = Xr * Xm * (2.2 * Y * t / Do) * (1 - 0.9435 * (d / t) ** 1.6 * (l / Do) ** 0.4)
    g = Resistance - Load

    gg = []
    gh = []

    if X.ndim == 1:
        # Gradient of limit state
        gg = Xr * np.array(
            [
                -(2.2 * Y * t * (0.9435 * (l / Do) ** 0.4 * (d / t) ** 1.6 - 1)) / Do,
                -(2.2 * Xm * t * (0.9435 * (l / Do) ** 0.4 * (d / t) ** 1.6 - 1)) / Do,
                (3.3211 * Xm * d * Y * (l / Do) ** 0.4 * (d / t) ** 0.6) / (Do * t)
                - (2.2 * Xm * Y * (0.9435 * (l / Do) ** 0.4 * (d / t) ** 1.6 - 1)) / Do,
                (2.2 * Xm * Y * t * (0.9435 * (l / Do) ** 0.4 * (d / t) ** 1.6 - 1)) / Do**2
                + (0.8303 * Xm * l * Y * t * (d / t) ** 1.6) / (Do**3 * (l / Do) ** 0.6),
                -(3.3211 * Xm * Y * (l / Do) ** 0.4 * (d / t) ** 0.6) / Do,
                -(2.2 * Xm * Y * t * (0.4 * 0.9435 * l ** (0.4 - 1) * (d / t) ** 1.6)) / Do**1.4,
                -1.0 / Xr,
            ]
        )

    return g, gg, gh, Load, Resistance
