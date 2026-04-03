# `DesignProblem` Keys Reference

This page documents design-specific dictionary keys that are required in addition to the common problem keys described in [Problem Definition](../index.md).

Additional helper code is allowed, but design problems must remain self-contained in the same problem module file; see [Problem Definition](../index.md).

## Core `DesignProblem` Keys

| Key | Required | Type | Meaning |
|---|---|---|---|
| `TargetBeta` | Exactly one of `TargetBeta` / `TargetPf` | `float` | Target reliability index for inverse reliability design |
| `TargetPf` | Exactly one of `TargetBeta` / `TargetPf` | `float` | Target probability of failure |
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

`DesignVariables` must be selected from `DeterministicVariables.name`.

!!! note "RBDO modeling assumption"
    In Reliafy's objective-optimization workflow, the optimized variables are assumed to be deterministic design variables, not stochastic variables. This is the standard RBDO formulation: the optimizer chooses deterministic design values, and reliability is then evaluated with respect to the stochastic variables.

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
- Every entry in `DesignVariables` must appear in `DeterministicVariables.name`.
- Objective return contract must match `DOFreturnsGradient` and `DOFreturnsHessian` flags.
- Reliability target (`TargetBeta` or `TargetPf`) is still required because optimization is reliability-constrained.
- Keep naming and order consistent with how `D` is used in `LSF(X, D)`.
- `cases` can also be used here for multi-scenario optimization; if omitted, a `default` case is created from `StochasticVariables`.

## Design Objective Function Contract

Your `DesignObjectiveFunction` must accept:

- `d`: the subset of deterministic-variable values being optimized
- `D`: the full deterministic-variable vector

Expected argument order:

- `d` follows the order of `DesignVariables`.
- `D` follows the order of `DeterministicVariables.name`.

This means `d` is the reduced design vector used by the optimizer, while `D` is the full deterministic state used by the problem definition.

Expected shape behavior:

- Vectorized mode (`DOFisVectorized=True`):
    - `d` can be `(n_design, n_samples)`
    - each row corresponds to one design variable in `DesignVariables` order.
- Single-point mode:
    - `d` can be `(n_design,)`.
- `D` follows the deterministic-variable ordering from `DeterministicVariables.name`.

### Required return values

Always return:

- `f`: objective-function value(s)
- `g`: gradient placeholder (`[]` when `DOFreturnsGradient=False` or not evaluated)
- `h`: Hessian placeholder (`[]` when `DOFreturnsHessian=False` or not evaluated)

The return signature remains:

- `return f, g, h`

Typical patterns are:

- Without derivatives: `return f, [], []`
- With derivatives in single-point mode: `return f, g, h`

### Gradient (`g`) definition

For a single point (`d.ndim == 1`):

- `g` is the derivative vector `df/dd_i` in the same order as `DesignVariables`.
- Shape should be `(n_design,)`.

For vectorized evaluations, return `[]` unless your implementation explicitly supports batched derivatives. In the current examples, derivatives are only returned in single-point mode.

### Hessian (`h`) definition

For a single point (`d.ndim == 1`):

- `h` is the matrix of second derivatives `d2f/(dd_i dd_j)`.
- Shape should be `(n_design, n_design)`.
- Keep symmetry when mathematically expected.

As with the gradient, `h` should only be returned for single-point evaluations in the standard pattern used by Reliafy examples.

## DOF Derivative Return Modes

Use the flags to match what your objective function returns:

| `DOFreturnsGradient` | `DOFreturnsHessian` | `DesignObjectiveFunction` expectation |
|---|---|---|
| `False` | `False` | Return placeholders for `g`, `h` (often empty lists) |
| `True` | `False` | Return valid `g` in single-point mode; `h` can be placeholder |
| `True` | `True` | Return valid `g` and `h` in single-point mode |

## Worked DOF Example (`Sorensen81Problem.py`)

In `Sorensen81Problem.py`, the only design variable is `z`, so:

- `DesignVariables = ["z"]`
- `d = [z]`
- `D = [z]` because `z` is also the full deterministic-variable list in that problem

The objective function is:

```python
def DOF(d, D):
        z = d
        f = z

        g = []
        h = []
        if d.ndim == 1:
                g = np.array([1.0])
                h = np.array([[0.0]])

        return f, g, h
```

For that example:

- `f = z`
- `df/dz = 1`
- `d2f/dz2 = 0`

So the valid single-point derivative returns are:

```python
g = np.array([1.0])
h = np.array([[0.0]])
```

The `if d.ndim == 1` guard is important: it keeps vectorized objective evaluations lightweight while still providing derivatives when the optimizer needs them for single-point steps.

See [Objective Optimization](optimization.md) for a worked example and checklist.

## Validation Checklist

1. `DesignProblem` exists when running `reliafy design ...`.
2. Exactly one of `TargetBeta` or `TargetPf` is provided.
3. `fractiles` matches the stochastic variable dimension.
4. If `cases` are provided, each case uses a valid variable name set and consistent array lengths.
5. If `cases` are omitted, confirm the implicit `default` case from `StochasticVariables` is the intended scenario.
6. If analytic derivatives are advertised (`LSFreturnsGradient`/`LSFreturnsHessian`), `LSF` actually returns valid derivatives in single-point mode.
7. For objective optimization, `DesignObjectiveFunction` accepts `(d, D)` with the documented ordering for `DesignVariables` and `DeterministicVariables.name`.
8. For objective optimization, `DesignObjectiveFunction` and its derivative flags are consistent with the actual DOF return signature.
9. If analytic objective derivatives are advertised (`DOFreturnsGradient`/`DOFreturnsHessian`), the DOF returns valid derivatives in single-point mode and placeholders otherwise.
