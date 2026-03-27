# Objective Optimization Example: `Sorensen81Problem.py`

This page documents a full `design` run where the objective function is minimized subject to a target reliability constraint.

Note: Table values are rounded to 4 significant figures for readability. Very small/large values use scientific notation. Refer to the Excel/JSON result files for full precision.
Note: Advanced solver diagnostics (for example `br_mult`, `lsf_mult`, and `bnds_mult` Lagrange multipliers) are included in the Excel/JSON result files and are not shown in the tables below.

## Run Context

Problem module:

- `problems/Sorensen81Problem.py`

Recorded result set:

- `results/2026-03-15/16-10-50/Sorensen 8.1-010a8.xlsx`
- `results/2026-03-15/16-10-50/Sorensen 8.1-010a8.json`
- `results/2026-03-15/16-10-50/Sorensen 8.1-010a8.py`
- `results/2026-03-15/16-10-50/profile-010a8.yaml`

Profile and run mode from saved profile:

- Profile used: `default`
- `run_type: design`
- `include_sorm: false`
- `include_mc: false`

For results-folder and filename conventions, see [CLI Result Files](../../cli/results-files.md).

Equivalent command shape:

```bash
reliafy design <profile>
```

## Plot Behavior For `design` Runs

Reliafy does not generate plots as part of `design` runs (including objective optimization).
This keeps outputs manageable when a problem defines multiple design cases.

If plots are needed, run `analyze` or `simulate` afterward using the optimized design parameters and enable the desired plot/report options.

## Profile Customization

This optimization example uses the `default` profile, but optimization and reliability settings are configurable. See [Profile Options Reference](../../profiles/profile-reference.md).

- Optimization controls: `reliability_options.design_xtol`, `design_gtol`, `design_maxiter`, `design_random_start`.
- Reliability constraint controls: `reliability_options.form_xtol`, `form_gtol`, `form_maxiter`, `alpha_direction`.
- Optional method/report toggles: `run_configuration.include_sorm`, `include_mc`, plus `reporting_options.*`.

## Problem File Used

**Source:** Sørensen, J. D., *Notes in Structural Reliability Theory and Risk Analysis*, Aalborg University, ch. 8, p. 141, Problem 8.1. [→](https://filelist.tudelft.nl/TBM/Over%20faculteit/Afdelingen/Values%2C%20Technology%20and%20Innovation/People/Full%20Professors/Pieter%20van%20Gelder/Citations/citatie215.pdf)

### Additional `DesignProblem` Keys Used By Optimization

`Sorensen81Problem.py` extends `DesignProblem` beyond Inverse FORM keys by adding a design objective function contract and design-variable bounds:

- `DesignObjectiveFunction: DOF`
- `DOFisVectorized: true`
- `DOFisSmooth: true`
- `DOFreturnsGradient: true`
- `DOFreturnsHessian: true`
- `DesignVariables: ["z"]`
- `InitialGuess: [1]`
- `lb: [0.0]`
- `ub: [np.inf]`
- `TargetBeta: 3.8`
- `fractiles: [0.05, 0.5, 0.98]`

In this example, the objective function is `DOF(d, D) = z`, so the solver seeks the minimum feasible value of `z` while satisfying the reliability target.

`DesignProblem.cases` is not explicitly defined in `Sorensen81Problem.py`, so Reliafy creates a `default` case from `StochasticVariables`.

## Extracted Results Worksheet Tables

The tables below are transcribed from the `Results` worksheet in `Sorensen 8.1-010a8.xlsx`.

### Header Information

| Field | Value |
|---|---|
| Problem | `Sorensen 8.1` |
| Request ID | `997f5a4d29f444f0bffa424ee74010a8` |
| Run time | `00 min 00.91 sec` |

### Design Data (Default Case)

| obj_value | target_beta | actual_beta | target_pf | actual_pf | use_sorm | dof_count | beta_count | nit | min_tries | min_method | br_mult |
|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---|---|
| 15.58 | 3.8 | 3.8 | 7.235e-05 | 7.236e-05 | False | 7 | 16 | 10 | 1 | tr_interior_point | |

### Design Variables Result

| var_name | opt_value | lb | ub |
|---|---:|---:|---|
| z | 15.58 | 0 | inf |

### Design Point Stochastic Variables Result

| var_name | x | fractile | char_value | partial_factor |
|---|---:|---:|---:|---:|
| R | 0.7612 | 0.05 | 0.7738 | 0.9837 |
| G | 2.04 | 0.5 | 2 | 1.02 |
| Q | 9.82 | 0.98 | 6.111 | 1.607 |

### Load and Resistance Partial Factors

| Load | Resistance |
|---:|---:|
| 1.462 | 0.9837 |

### FORM Results (At Optimum)

| beta | pf | beta_count | hbeta_count | lsf_count | glsf_count | hlsf_count | min_method |
|---:|---:|---:|---:|---:|---:|---:|---|
| 3.8 | 7.236e-05 | 102 | 102 | 102 | 102 | 102 | tr_interior_point |

### Notes Reported by Reliafy

1. Validation: Stochastic variables definition and limit state function validation required 2 function calls.
2. Validation: Design problem validation required 2 calls to the design objection function.
3. Validation: Validation of the limit state function's analytic gradient and hessian required 37 function calls.
4. Validation: Validation of the design objective function's analytic gradient and hessian required 12 function calls.
5. FORM case (`default`): Active bound multipliers reported for `R`, `G`, and `Q`.
6. Design: Active bound multipliers reported for design variable `z` in case `default`.

## Interpretation Snapshot

- The optimizer converged in `10` iterations and found `z = 15.5812409574229`.
- Reliability target matching is tight: `actual_beta = 3.799975486073672` versus `target_beta = 3.8`.
- The objective and design variable are the same in this problem (`obj_value = z`), so objective minimization directly maps to minimizing `z` under reliability constraints.
