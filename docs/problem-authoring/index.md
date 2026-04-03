# Problem Definition

This section explains how to define a Reliafy problem module (`*.py`) that can be selected from the `problems/` directory and solved by `analyze`, `design`, or `simulate` commands.

For result-folder location and output filename conventions, see [CLI Result Files](../cli/results-files.md).

## Minimal File Pattern

A problem module should expose `Problem()` (or `problem()`) and return a dictionary.

```python
import numpy as np


def Problem():
    return {
        "Name": "MyProblem",
        "LimitStateFunction": LSF,
        "LSFisVectorized": True,
        "LSFisSmooth": True,
        "LSFisParallelizable": True,
        "LSFreturnsGradient": False,
        "LSFreturnsHessian": False,
        "LSFreturnsLandR": False,
        "DeterministicVariables": {"name": [], "value": []},
        "StochasticVariables": {
            "name": ["X1", "X2"],
            "type": ["normal", "normal"],
            "mean": [10.0, 4.0],
            "std": [1.0, 0.5],
        },
    }


def LSF(X, D):
    X1, X2 = X
    g = X1 - X2
    gg = []
    gh = []
    L = []
    R = []
    return g, gg, gh, L, R
```

## Module Self-Containment

Problem modules may define additional variables, arrays, dictionaries, helper functions, and preprocessing logic beyond the required contracts such as `LimitStateFunction` and (for design runs) `DesignObjectiveFunction`.

All data structures and helper logic used by the problem must be defined inside the same problem module (`*.py`). External data files are not supported for problem execution.

## Submission Safety Validation

For platform safety, submitted problem modules are validated and may be rejected if they contain unsafe execution patterns.

When a module is rejected, the API returns a validation error describing the disallowed category.

## Top-Level Problem Keys

For full return-signature details for `LimitStateFunction` and related `LSFreturns*` flags, see [Limit State Function Contract](#limit-state-function-contract).

For detailed key-by-key guidance beyond this summary table, see the sections below: [StochasticVariables Keys](#stochasticvariables-keys), [Plot Definition Keys (`LSFplot`, `RFADplot`, `ISplot`)](#plot-definition-keys-lsfplot-rfadplot-isplot), [Limit State Function Contract](#limit-state-function-contract), and the design-focused pages linked in [Next Pages](#next-pages).

| Key | Required | Type | Purpose | Example (`AT610`) |
|---|---|---|---|---|
| `Name` | Yes | `str` | Human-readable problem name used in outputs | `"AT610"` |
| `LimitStateFunction` | Yes | callable | Function implementing `g(X, D)` with return contract `g, gg, gh, L, R` (placeholders allowed; see Limit State Function Contract) | `LSF` |
| `LSFisVectorized` | Yes | `bool` | Whether `LSF` can process batched samples (`X` with shape `(n_var, n_samples)`) | `True` |
| `LSFisSmooth` | Yes | `bool` | Signals smoothness for derivative-based reliability methods | `True` |
| `LSFisParallelizable` | Yes | `bool` | Signals that evaluations are safe for parallel execution | `True` |
| `LSFreturnsGradient` | Yes | `bool` | If `True`, `LSF` should return gradient `gg` for 1-point evaluation; otherwise return placeholder `[]` | `True` |
| `LSFreturnsHessian` | Yes | `bool` | If `True`, `LSF` should return Hessian `gh` for 1-point evaluation; otherwise return placeholder `[]` | `True` |
| `LSFreturnsLandR` | Yes | `bool` | If `True`, `LSF` should return non-empty load/resistance values `(L, R)` for reporting and plots; otherwise return placeholders such as `[]`, `[]` | `True` |
| `DeterministicVariables` | Yes | `dict` | Deterministic variables and fixed values | empty in `AT610` |
| `StochasticVariables` | Yes | `dict` | Random variable definition (names, distributions, moments, correlations) | `Y,Z,M` |
| `LSFplot` | Optional | `dict` | Axis mapping and limits for LSF plots | present in `AT610` |
| `RFADplot` | Optional | `dict` | Axis mapping and limits for RFAD plots | present in `AT610` |
| `ISplot` | Optional | `dict` | Axis mapping for importance-sampling diagnostic plots | present in `AT610` |
| `DesignProblem` | Required for `design` runs | `dict` | Design-specific definitions (objective, constraints, variables) | not used in `AT610` |

## `DeterministicVariables` Keys

| Key | Required | Type | Meaning |
|---|---|---|---|
| `name` | Yes | `list[str]` | Deterministic variable names (order matters) |
| `value` | Yes | `list[float]` | Deterministic values in same order as `name` |

Rules:

- `len(name)` must match `len(value)`.
- Keep deterministic variable order consistent with how `D` is unpacked inside `LSF(X, D)`.

## `StochasticVariables` Keys

Core keys used in all example problems:

| Key | Required | Type | Meaning |
|---|---|---|---|
| `name` | Yes | `list[str]` | Random variable names (defines variable order in `X`) |
| `type` | Yes | `list[str]` | Distribution per variable, e.g. `normal`, `lognormal`, `gumbelmax` |
| `mean` | Yes | `list[float]` | Mean values |
| `std` | Yes | `list[float]` | Standard deviations |
| `cor_list` | No | `list[list]` | Pairwise correlation entries `[var_i, var_j, rho]` |
| `cor` | No | `list[list]` | Full correlation matrix in variable order |

Advanced/optional fields can also be used depending on model needs:

| Key | Required | Type | Meaning |
|---|---|---|---|
| `lb` | Conditional | `list[float]` | Lower bounds per stochastic variable; required for some distributions and optional otherwise |
| `ub` | Conditional | `list[float]` | Upper bounds per stochastic variable; required for some distributions and optional otherwise |
| `truncated` | No | `list[bool]` | Whether each variable distribution is truncated to `[lb, ub]` |
| `constraints` | No | `list[dict]` | Additional nonlinear constraints on stochastic variables |

Rules:

- All lists must have the same length `n` (`name`, `type`, `mean`, `std`).
- Variable order in `name` must match `X` unpacking in `LSF`.
- If neither `cor_list` nor `cor` is provided, Reliafy assumes zero correlation between all variables.
- `cor_list` references variable names from `name`.
- `cor`, when used, should be an `n x n` correlation matrix in the same variable order as `name`.
- Use either `cor_list` or `cor` to define correlation inputs.
- If defined, `lb`, `ub`, and `truncated` must each have length `n`.
- You can set individual bounds to `-np.inf` and `np.inf` to indicate no lower/upper bound for that variable.
- If `lb`, `ub`, and/or `truncated` are omitted, defaults are used: no bounds and `truncated=False` for all variables.
- In FORM, Inverse FORM, and `design` runs, `lb`/`ub` are applied as constraints in the underlying minimization problems.
- If `truncated[i]` is `True`, the corresponding variable's distribution is truncated to `[lb[i], ub[i]]`.
- `constraints`, when provided, follows a dictionary format similar to SciPy `optimize.minimize` constraints (Reliafy uses SciPy optimization internally).
- Constraint callables are defined on the stochastic-variable vector and may optionally include Jacobians.

Example definition reference:

- `problems/PipecorrProblem.py` shows `constraints` entries under `StochasticVariables` (for example `d_over_t` and `l_over_Do` bounds).
- This is a key-format reference only; it is not used as a worked run in the `analyze`, `design`, or `simulate` documentation pages.

## Supported Statistical Distributions

The table below lists all supported `StochasticVariables.type` values with their `scipy.stats` equivalents and natural parameters. Reference links to Wikipedia and SciPy documentation are provided for each distribution.

For each stochastic variable, you can define the distribution either with:

- `mean` and `std`, or
- `param1` and `param2` (natural distribution parameters shown below, when applicable).

Per-variable input rule:

- The four lists (`mean`, `std`, `param1`, `param2`) can all be present in the same problem.
- For each variable index `i`, use exactly one pair:
    - either `mean[i]` and `std[i]`, with `param1[i] = None` and `param2[i] = None`
    - or `param1[i]` and `param2[i]`, with `mean[i] = None` and `std[i] = None`
- This allows mixed entry modes across variables in one model (for example, one variable by moments and another by natural parameters).

Example pattern (`None` marks the unused pair for that variable):

```python
"StochasticVariables": {
        "name":   ["X1",    "X2",    "X3"],
        "type":   ["normal", "gumbelmax", "uniform"],
        "mean":   [10.0,     None,     None],
        "std":    [2.0,      None,     None],
        "param1": [None,     100.0,    0.0],
        "param2": [None,     15.0,     20.0],
}
```

| Reliafy `type` | `scipy.stats` equivalent | Mean | Std | `param1` | `param2` | `lb`/`ub` |
|---|---|---|---|---|---|---|
| `normal` | `norm` | Yes | Yes | `μ` | `σ` | Optional |
| `lognormal` | `lognormal` (`lognorm`) | Yes | Yes | `μ_ln` | `σ_ln` | Optional |
| `gumbelmax` | `gumbel_r` | Yes | Yes | `μ` | `β` | Optional |
| `gumbelmin` | `gumbel_l` | Yes | Yes | `μ` | `β` | Optional |
| `exponential` | `expon` | Yes | No | `λ` | `None` | Optional |
| `gamma` | `gamma` | Yes | Yes | `κ` | `θ` | Optional |
| `weibull` | `weibull_min` | Yes | Yes | `κ` | `λ` | Optional |
| `beta` | `beta` | Yes | Yes | `α` | `β` | Required |
| `triangular` | `triang` | Yes | No | `Mo` (mode) | `None` | Required |
| `uniform` | `uniform` | Yes | Yes | `a` | `b` | `*` |
| `frechet` | `invweibull` | Yes | Yes | `s` | `α` | Optional |
| `pareto` | `pareto` | Yes | Yes | `xm` | `α` | Optional |
| `rayleigh` | `rayleigh` | Yes | No | `σ` | `None` | Optional |

`*` Uniform distribution guidance:

- When `mean` and `std` are specified, set both `lb` and `ub` to `None`.
- When using distribution parameters (`lb`, `ub`), set `param1` and `param2` to `None`.

Greek symbols shown for `param1` and `param2` follow the standard notation used in the linked Wikipedia references (where applicable).

Parameterizations can differ across sources; Reliafy follows the parameter definitions documented by the linked SciPy distributions.

For correlated non-normal variables, Reliafy uses an isoprobabilistic transformation (Nataf) to map variables into standard normal space during reliability computations.

Reference links (from source doc):

- `normal`: [Wikipedia](https://en.wikipedia.org/wiki/Normal_distribution), [SciPy `norm`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html)
- `lognormal`: [Wikipedia](https://en.wikipedia.org/wiki/Log-normal_distribution), [SciPy `lognorm`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.lognorm.html)
- `gumbelmax`: [NIST Gumbel](https://www.itl.nist.gov/div898/handbook/eda/section3/eda366g.htm), [SciPy `gumbel_r`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gumbel_r.html)
- `gumbelmin`: [NIST Gumbel](https://www.itl.nist.gov/div898/handbook/eda/section3/eda366g.htm), [SciPy `gumbel_l`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gumbel_l.html)
- `exponential`: [Wikipedia](https://en.wikipedia.org/wiki/Exponential_distribution), [SciPy `expon`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.expon.html)
- `gamma`: [Wikipedia](https://en.wikipedia.org/wiki/Gamma_distribution), [SciPy `gamma`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gamma.html)
- `weibull`: [Wikipedia](https://en.wikipedia.org/wiki/Weibull_distribution), [SciPy `weibull_min`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.weibull_min.html)
- `beta`: [Wikipedia](https://en.wikipedia.org/wiki/Beta_distribution), [SciPy `beta`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.beta.html)
- `triangular`: [Wikipedia](https://en.wikipedia.org/wiki/Triangular_distribution), [SciPy `triang`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.triang.html)
- `uniform`: [Wikipedia](https://en.wikipedia.org/wiki/Continuous_uniform_distribution), [SciPy `uniform`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.uniform.html)
- `frechet`: [Wikipedia](https://en.wikipedia.org/wiki/Fr%C3%A9chet_distribution), [SciPy `invweibull`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.invweibull.html)
- `pareto`: [Wikipedia](https://en.wikipedia.org/wiki/Pareto_distribution), [SciPy `pareto`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pareto.html)
- `rayleigh`: [Wikipedia](https://en.wikipedia.org/wiki/Rayleigh_distribution), [SciPy `rayleigh`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rayleigh.html)

Type strings are case-insensitive: both lowercase (for example `"lognormal"`) and camelCase (for example `"gumbelMax"`) are accepted.

## Plot Definition Keys (`LSFplot`, `RFADplot`, `ISplot`)

These blocks are optional for computation but needed for plot commands and richer diagnostics.

### `LSFplot`

`LSFplot` defines a 2D plot showing the limit state function contour and the mean-point location. It is used when running `reliafy analyze -l`.

**Required and optional keys:**

| Key | Type | Required | Meaning |
|---|---|---|---|
| `x_var` | `str` | Yes | Stochastic variable name for x axis |
| `x_lim` | `list[float]` | Yes | Plot window `[min, max]` for x axis |
| `y_var` | `str` | Yes | Stochastic variable name for y axis |
| `y_lim` | `list[float]` | Yes | Plot window `[min, max]` for y axis |
| `x_func` | `callable` or omitted | No | Transformation function `lambda S, D: ...` for x axis. If omitted, x axis displays `x_var` directly. |
| `y_func` | `callable` or omitted | No | Transformation function `lambda S, D: ...` for y axis. If omitted, y axis displays `y_var` directly. |
| `x_label` | `str` or omitted | No | Custom label for x axis (can include LaTeX). If omitted, defaults to variable name. |
| `y_label` | `str` or omitted | No | Custom label for y axis (can include LaTeX). If omitted, defaults to variable name. |
| `z_var` | `str` | Optional | Third variable held fixed/parameterized for advanced 3D layout choices. |

**Transformation function signature:**

- `x_func(S, D)` and `y_func(S, D)` receive:
  - `S`: array of stochastic variable values in the order defined in `StochasticVariables.name`.
  - `D`: array of deterministic variable values in the order defined in `DeterministicVariables.name`.
- Return a scalar value or array to be plotted.
- Typical use: combine multiple variables (e.g., `lambda S, D: S[0] * S[1]` for resistance as product) or apply scaling/Log transforms.

**Example from `AT68Problem.py`:**

```python
"LSFplot": {
    "x_var": "Y",
    "x_lim": [30.0, 50.0],
    "x_func": lambda S, D: S[0] * S[1],      # Resistance: product of Y and Z
    "x_label": "Resistance: Y*Z",
    "y_var": "M",
    "y_lim": [800, 1200],
    "y_func": lambda S, D: S[2],              # Load: just M
    "y_label": "Load: M",
}
```

Here, stochastic variables are indexed as `S[0]` for Y, `S[1]` for Z, and `S[2]` for M (in `StochasticVariables.name` order). The Plot shows a 2D contour where failure occurs when resistance ≤ load. Pages 2–3 of the run PDF display the LSF visualization with the mean point overlaid.

### `RFADplot`

`RFADplot` defines the axes of a Reliability-based Failure Assessment Diagram (RFAD). Reliafy sweeps the `x_param` of `x_var` across `x_lim` and the `y_param` of `y_var` across `y_lim`, computing the reliability index, probability of failure, and alpha vectors for each combination to produce an iso-reliability contour map. Run with `reliafy analyze -r`.

**Required and optional keys:**

| Key | Type | Required | Meaning |
|---|---|---|---|
| `x_var` | `str` | Yes | Stochastic variable whose parameter is swept along the x axis |
| `x_param` | `str` | Yes | Parameter to sweep, e.g. `"mean"` |
| `x_lim` | `list[float]` | Yes | Sweep range `[min, max]` for the x parameter |
| `y_var` | `str` | Yes | Stochastic variable whose parameter is swept along the y axis |
| `y_param` | `str` | Yes | Parameter to sweep, e.g. `"mean"` |
| `y_lim` | `list[float]` | Yes | Sweep range `[min, max]` for the y parameter |
| `x_func` | `callable` or omitted | No | Transformation `lambda S, D: ...` mapping the swept stochastic values to the plotted x quantity. If omitted, the swept parameter value is plotted directly. |
| `y_func` | `callable` or omitted | No | Transformation `lambda S, D: ...` mapping the swept stochastic values to the plotted y quantity. If omitted, the swept parameter value is plotted directly. |
| `x_label` | `str` or omitted | No | Custom label for x axis (can include LaTeX). If omitted, defaults to variable name. |
| `y_label` | `str` or omitted | No | Custom label for y axis (can include LaTeX). If omitted, defaults to variable name. |

`x_func` and `y_func` follow the same signature as in `LSFplot`: they receive `S` (stochastic variable values array in `StochasticVariables.name` order) and `D` (deterministic variable values array) and return the quantity to plot.

**Example from `AT68Problem.py`:**

```python
"RFADplot": {
    "x_var": "Y",
    "x_param": "mean",
    "x_lim": [10.0, 70.0],
    "x_func": lambda S, D: S[0] * S[1],           # Resistance: μ(Y) * μ(Z)
    "x_label": "Resistance: \\mu(Y)*\\mu(Z)",
    "y_var": "M",
    "y_param": "mean",
    "y_lim": [500.0, 1500.0],
    "y_func": lambda S, D: S[2],                   # Load: μ(M)
    "y_label": "Load: \\mu(M)",
}
```

Here `S[0]` is Y, `S[1]` is Z, and `S[2]` is M. As Reliafy sweeps `mean(Y)` and `mean(M)`, `x_func` converts the current Y mean into ` μ(Y)·μ(Z)` (resistance) and `y_func` passes `mean(M)` through as the load axis. The RFAD contour plot is included in the run PDF.

### `ISplot`

`ISplot` defines the axis variables and plot extents used for importance-sampling proposal diagnostics when running `reliafy simulate -i`. If `ISplot` is omitted, IS proposal diagnostic figures are not generated. If sampled points fall outside the specified limits, Reliafy automatically expands the displayed axis ranges.

| Key | Required if `ISplot` exists | Meaning |
|---|---|---|
| `x_var` | Yes | Stochastic variable name used on the x axis for IS proposal diagnostics |
| `x_lim` | Yes | Plot range `[min, max]` for the x axis |
| `y_var` | Yes | Stochastic variable name used on the y axis for IS proposal diagnostics |
| `y_lim` | Yes | Plot range `[min, max]` for the y axis |

## Limit State Function Contract

Your `LSF` must accept:

- `X`: stochastic variables
- `D`: deterministic variables

Expected argument order:

- `X` follows the order of `StochasticVariables.name`.
- `D` follows the order of `DeterministicVariables.name`.

This means `X` is the stochastic-variable vector (or batch of vectors), while `D` is the deterministic state used by the problem definition.

Expected shape behavior:

- Vectorized mode (`LSFisVectorized=True`):
  - `X` can be `(n_var, n_samples)`
  - each row corresponds to one variable in `StochasticVariables.name` order.
- Single-point mode:
  - `X` can be `(n_var,)`.
- `D` follows the deterministic-variable ordering from `DeterministicVariables.name`.

### Required return values

Always return:

- `g`: limit state value(s), with failure when `g <= 0`.
- `gg`: gradient placeholder (`[]` when `LSFreturnsGradient=False`).
- `gh`: Hessian placeholder (`[]` when `LSFreturnsHessian=False`).
- `L`: load placeholder/value (`[]` when `LSFreturnsLandR=False`).
- `R`: resistance placeholder/value (`[]` when `LSFreturnsLandR=False`).

The `LSFreturnsGradient`, `LSFreturnsHessian`, and `LSFreturnsLandR` flags change whether `gg`, `gh`, `L`, and `R` contain meaningful values or placeholders, but the return signature remains:

- `return g, gg, gh, L, R`

Typical patterns are:

- Without load/resistance reporting: `return g, gg, gh, [], []`
- With load/resistance reporting: `return g, gg, gh, L, R`

### Gradient (`gg`) definition

For a single point (`X.ndim == 1`):

- `gg` is the derivative vector `dg/dx_i` in the same variable order as `name`.
- Shape should be `(n_var,)`.

For vectorized evaluations, many examples return `[]` and only compute derivatives in single-point mode.

### Hessian (`gh`) definition

For a single point (`X.ndim == 1`):

- `gh` is the matrix of second derivatives `d2g/(dx_i dx_j)`.
- Shape should be `(n_var, n_var)`.
- Keep symmetry when mathematically expected.

As with the gradient, `gh` is typically only returned for single-point evaluations in the standard Reliafy authoring pattern.

## LSF Derivative Return Modes

Use the flags to match what your function returns:

| `LSFreturnsGradient` | `LSFreturnsHessian` | `LSF` expectation |
|---|---|---|
| `False` | `False` | Return placeholders for `gg`, `gh` (often empty lists), plus `L`, `R` placeholders or values |
| `True` | `False` | Return valid `gg`; `gh` can be placeholder; still return `L`, `R` |
| `True` | `True` | Return valid `gg` and `gh`; still return `L`, `R` |

## Worked LSF Example (`AT610Problem.py`)

In `AT610Problem.py`, the stochastic variables are `Y`, `Z`, and `M`, and there are no deterministic variables:

- `StochasticVariables.name = ["Y", "Z", "M"]`
- `DeterministicVariables.name = []`

The limit state function is:

```python
def LSF(X, D):
    Y, Z, M = X

    L = M  # Load
    R = Y * Z  # Resistance

    g = R - L

    gg = []
    gh = []
    if X.ndim == 1:
        gg = np.array([Z, Y, -1.0])
        gh = np.array([
            [0.0, 1.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
        ])

    return g, gg, gh, L, R
```

For that example:

- `R = Y * Z`
- `L = M`
- `g = R - L = YZ - M`

Analytical gradient:

- `dg/dY = Z`
- `dg/dZ = Y`
- `dg/dM = -1`

So:

```python
gg = np.array([Z, Y, -1.0])
```

Analytical Hessian:

- `d2g/dYdZ = 1`
- `d2g/dZdY = 1`
- all other second derivatives are zero

```python
gh = np.array([
    [0.0, 1.0, 0.0],
    [1.0, 0.0, 0.0],
    [0.0, 0.0, 0.0],
])
```

`AT610` sets both derivative flags to `True`, so Reliafy uses the analytic gradient and Hessian during FORM convergence and SORM curvature fitting.

## Common Authoring Pitfalls

- Variable order mismatch between `StochasticVariables.name` and `X` unpacking in `LSF`.
- Returning scalar `g` for vectorized inputs when an array is expected.
- Setting derivative flags to `True` but returning placeholders.
- Returning only `g, gg, gh` instead of the full `g, gg, gh, L, R` contract.
- Defining `cor_list` pairs with variable names not present in `name`.
- Defining a `cor` matrix with the wrong size or variable order.
- Forgetting `DesignProblem` when running `reliafy design ...`.

## Next Pages

- [FORM Only](analyze/form-only.md): analyze example using FORM only (`AT610`).
- [SORM and Monte Carlo](analyze/sorm-monte-carlo.md): analyze example using `-s -m` (`Chan3`).
- [Design Overview](design/index.md): design authoring overview and workflow split (Inverse FORM vs objective optimization).
- [Design Keys Reference](design/design-keys.md): `DesignProblem` key reference and validation checklist.
- [Inverse FORM Examples](design/inverse-form.md): worked inverse FORM examples (`AT625` single-case and `AT624` multi-case).
- [Objective Optimization](design/optimization.md): objective optimization example and checklist.
- [Classic Monte Carlo](simulate/classic-monte-carlo.md): simulation example using plain Monte Carlo (Chan2).
- [Importance Sampling](simulate/importance-sampling.md): simulation example using importance sampling (AU2).
