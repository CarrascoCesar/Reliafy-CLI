# Description: Chan and Low 2011 problem 2 page 1397
# https://onlinelibrary.wiley.com/doi/full/10.1002/nag.1057

import math

import numpy as np


def Problem():

    Problem = {
        "Name": "Chan2",
        "LimitStateFunction": LSF,
        "LSFisVectorized": True,
        "LSFisSmooth": True,
        "LSFreturnsGradient": False,
        "LSFreturnsHessian": False,
        "LSFreturnsLandR": True,
        "DeterministicVariables": {
            "name": ["B", "L", "D", "h"],
            "value": [5.0, 25.0, 1.8, 2.5],
        },
        "StochasticVariables": {
            "name": ["cp", "fp", "g", "Ph", "Pv"],
            "type": ["normal", "normal", "normal", "normal", "normal"],
            "cor": [
                [1.0, -0.5, 0.0, 0.0, 0.0],
                [-0.5, 1.0, 0.5, 0.0, 0.0],
                [0.0, 0.5, 1.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 1.0, 0.5],
                [0.0, 0.0, 0.0, 0.5, 1.0],
            ],
            "mean": [15.0, 25.0, 20.0, 400.0, 800.0],
            "std": [4.5, 5.0, 2.0, 40.0, 80.0],
        },
        "LSFplot": {
            "x_var": "Pv",
            "x_param": "value",
            "x_lim": [600.0, 950],
            "x_func": lambda S, D: S[4],
            "x_label": "Pv",
            "y_var": "cp",
            "y_param": "value",
            "y_lim": [6.0, 18.0],
            "y_func": lambda S, D: S[0],
            "y_label": "cp",
            "z_var": "Ph",
        },
    }

    return Problem


def LSF(X, D):
    # X is a (n, m) matrix where n is the number of stochatic variables and
    # m is the number of samples
    # If X.ndim == 1 then X is a (n,) matrix where n is the number of
    # stochastic variables
    # D is a (n,) array where n is the number of deterministic variables

    cp, fp, g, Ph, Pv = X
    B, L, D, h = D

    fp = np.deg2rad(fp)
    tan_fp = np.tan(fp)

    Nq = np.exp(np.pi * tan_fp) * np.square(np.tan(math.pi / 4.0 + fp / 2.0))
    Nc = (Nq - 1.0) / tan_fp
    Ng = 2.0 * (Nq - 1.0) * tan_fp
    eb = Ph * h / Pv
    Bp = B - 2.0 * eb
    Lp = L
    sq = 1.0 + (Bp / Lp) * np.sin(fp)
    sc = (sq * Nq - 1.0) / (Nq - 1.0)
    sg = 1.0 - 0.3 * Bp / Lp
    m = (2.0 + Bp / Lp) / (1.0 + Bp / Lp)

    power_arg = 1.0 - Ph / (Pv + Bp * Lp * cp / tan_fp)
    valid = power_arg > 0
    safe_power_arg = np.where(valid, power_arg, np.nan)
    iq = np.where(valid, np.power(safe_power_arg, m), np.nan)
    ig = np.where(valid, np.power(safe_power_arg, m + 1.0), np.nan)
    ic = np.where(valid, iq - (1.0 - iq) / (Nc * tan_fp), np.nan)

    Resistance = cp * Nc * sc * ic + g * D * Nq * sq * iq + 0.5 * g * Bp * Ng * sg * ig
    Load = Pv / Bp

    g = Resistance - Load

    gg = []
    gh = []

    return g, gg, gh, Load, Resistance


# Path: Problems/Chan2Problem.py
