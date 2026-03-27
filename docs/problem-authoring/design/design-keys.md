# `DesignProblem` Keys Reference

This page documents design-specific dictionary keys that are required in addition to the common problem keys described in [Problem Definition](../index.md).

Additional helper code is allowed, but design problems must remain self-contained in the same problem module file; see [Problem Definition](../index.md).

## Core `DesignProblem` Keys

| Key | Required | Type | Meaning |
|---|---|---|---|
| `TargetBeta` | One of `TargetBeta` / `TargetPf` | `float` | Target reliability index for inverse reliability design |
| `TargetPf` | One of `TargetBeta` / `TargetPf` | `float` | Target probability of failure |
| `fractiles` | Yes for Inverse FORM | `list[float]` | Fractile level used to compute characteristic values and partial factors |
| `cases` | Optional (both design types) | `dict` | Named design scenarios overriding base stochastic definitions |

`cases` is not limited to Inverse FORM. It can be used in both Inverse FORM and objective optimization runs.
If `cases` is omitted, Reliafy builds a `default` case from the top-level `StochasticVariables` definition.

## Additional Keys For Objective Optimization

When `design_type` is objective optimization (as in `Sorensen81Problem.py`), the following keys are required in `DesignProblem`.

| Key | Required | Type | Meaning |
|---|---|---|---|
| `DesignObjectiveFunction` | Yes | callable | Objective function used by the design optimizer |
| `DOFisVectorized` | Yes | `bool` | Whether objective can process vectorized design inputs |
| `DOFisSmooth` | Yes | `bool` | Signals smooth objective behavior for derivative-based optimization |
| `DOFreturnsGradient` | Yes | `bool` | If `True`, objective must return gradient in single-point mode |
| `DOFreturnsHessian` | Yes | `bool` | If `True`, objective must return Hessian in single-point mode |
| `DesignVariables` | Yes | `list[str]` | Names of deterministic design variables to optimize |
| `InitialGuess` | Yes | `list[float]` | Starting point for optimization |
| `lb` | Yes | `list[float]` | Lower bounds for design variables |
| `ub` | Yes | `list[float]` | Upper bounds for design variables |

## Inverse FORM Pattern

Typical shape:

```python
"DesignProblem": {
    "TargetBeta": 2.0,
    "fractiles": [0.5, 0.5, 0.5],
    "cases": {
        "1": {
            "name": ["N", "M", "Y"],
            "mean": [1.0, 0.01, 126.0],
            "cv": [0.10, 0.21, 0.26],
        }
    },
}
```

Rules:

- Define either `TargetBeta` or `TargetPf` (the other can be derived).
- `fractiles` length must match the number of stochastic variables in the active case.
- Each case must define arrays with consistent lengths.
- Case variable names should match stochastic variable names used by `LimitStateFunction`.
- If `cases` is not provided, a `default` case is created from `StochasticVariables`.

## Objective Optimization Pattern

Typical shape:

```python
"DesignProblem": {
    "DesignObjectiveFunction": DOF,
    "DOFisVectorized": True,
    "DOFisSmooth": True,
    "DOFreturnsGradient": True,
    "DOFreturnsHessian": True,
    "DesignVariables": ["z"],
    "InitialGuess": [1.0],
    "lb": [0.0],
    "ub": [np.inf],
    "TargetBeta": 3.8,
    "fractiles": [0.05, 0.5, 0.98],
}
```

Rules:

- `len(DesignVariables) == len(InitialGuess) == len(lb) == len(ub)`.
- Objective return contract must match `DOFreturnsGradient` and `DOFreturnsHessian` flags.
- Reliability target (`TargetBeta` or `TargetPf`) is still required because optimization is reliability-constrained.
- If a design variable is also present in `DeterministicVariables.name`, keep naming and order consistent with how `D` is used in `LSF(X, D)`.
- `cases` can also be used here for multi-scenario optimization; if omitted, a `default` case is created from `StochasticVariables`.

See [Objective Optimization](optimization.md) for a worked example and checklist.

## Validation Checklist

1. `DesignProblem` exists when running `reliafy design ...`.
2. `TargetBeta` and `TargetPf` are not contradictory.
3. `fractiles` matches the stochastic variable dimension.
4. If `cases` are provided, each case uses a valid variable name set and consistent array lengths.
5. If `cases` are omitted, confirm the implicit `default` case from `StochasticVariables` is the intended scenario.
6. If analytic derivatives are advertised (`LSFreturnsGradient`/`LSFreturnsHessian`), `LSF` actually returns valid derivatives in single-point mode.
7. For objective optimization, `DesignObjectiveFunction` and its derivative flags are consistent with the actual DOF return signature.
