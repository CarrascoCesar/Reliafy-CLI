# Inverse FORM Examples

This page documents two inverse reliability design examples based on saved `design` runs.

Note: Table values are rounded to 4 significant figures for readability. Very small/large values use scientific notation. Refer to the Excel/JSON result files for full precision.
Note: Advanced solver diagnostics (for example `bsr_mult` and `bnds_mult` Lagrange multipliers) are included in the Excel/JSON result files and are not shown in the tables below.

## Plot Behavior For `design` Runs

Reliafy does not generate plots as part of `design` runs (including Inverse FORM).
This keeps outputs manageable when multiple design cases are included in one run.

If you need plots, use the resulting design parameters in a follow-up `analyze` or `simulate` run and enable plot/report options there.

In the Excel `Results` sheet, these details appear under each case as `Design point stochastic variables result:` and, when available, `Load and resistance partial factors:`.

## Profile Customization

These inverse FORM examples use the `default` profile, but solver behavior is configurable. See [Profile Options Reference](../../profiles/profile-reference.md).

- Inverse/design solver controls: `reliability_options.design_xtol`, `design_gtol`, `design_maxiter`, `design_random_start`.
- FORM controls used inside inverse iterations: `reliability_options.form_xtol`, `form_gtol`, `form_maxiter`, `alpha_direction`.
- Correlation handling and derivative checks: `reliability_options.use_nearest_correlation`, `check_lsf_diffs_wrtx`, `check_lsf_diffs_wrtu`.

## Example A: `AT625Problem.py` (Single Default Case)

### Run Context

Problem module:

- `problems/AT625Problem.py`

Recorded result set:

- `results/2026-03-15/15-01-56/Ang and Tang 6.25-88679.xlsx`
- `results/2026-03-15/15-01-56/Ang and Tang 6.25-88679.json`
- `results/2026-03-15/15-01-56/Ang and Tang 6.25-88679.py`
- `results/2026-03-15/15-01-56/profile-88679.yaml`

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

### Problem File Used

**Source:** Ang, A. H-S. and Tang, W. H., *Probability Concepts in Engineering Planning and Design, Vol. II*, Wiley, 1990, p. 431, Problem 6.25.

### Extracted Results Worksheet Tables

Run summary:

| Field | Value |
|---|---|
| Request ID | `e580592237a84a2ca36275f5bbd88679` |
| Target beta | `1.28` |
| Target pf | `0.1003` |
| Cases | `default` |

Default-case inverse FORM result:

| case | beta | pf | lsf_count | glsf_count | hlsf_count | nit |
|---|---:|---:|---:|---:|---:|---:|
| default | 1.28 | 0.1003 | 8 | 8 | 8 | 12 |

Design point stochastic variables result (`default`):

| var_name | x | fractile | char_value | partial_factor |
|---|---:|---:|---:|---:|
| f | 2.52 | 0.5 | 2.46 | 1.024 |
| N | 10.31 | 0.5 | 11 | 0.9374 |
| Y | 9.6 | 0.5 | 9.76 | 0.9836 |
| Q | 1.268e+04 | 0.5 | 9589 | 1.322 |

Load and resistance partial factors (`default`):

| Load | Resistance |
|---:|---:|
| 1.322 | 0.9109 |

Notes:

- This is the canonical single-case inverse FORM setup.
- `AT625` also reports load and resistance partial factors in the design output.

## Example B: `AT624Problem.py` (Multi-Case)

### Run Context

Problem module:

- `problems/AT624Problem.py`

Recorded result set:

- `results/2026-03-15/15-01-29/Ang and Tang 6.24-9e10e.xlsx`
- `results/2026-03-15/15-01-29/Ang and Tang 6.24-9e10e.json`
- `results/2026-03-15/15-01-29/Ang and Tang 6.24-9e10e.py`
- `results/2026-03-15/15-01-29/profile-9e10e.yaml`

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

### Problem File Used

**Source:** Ang, A. H-S. and Tang, W. H., *Probability Concepts in Engineering Planning and Design, Vol. II*, Wiley, 1990, p. 428, Problem 6.24.

### Extracted Results Worksheet Tables

Run summary:

| Field | Value |
|---|---|
| Request ID | `0a4040de1dc341adb06688f5cdd9e10e` |
| Target beta | `2.0` |
| Target pf | `0.02275` |
| Cases | `1`, `2`, `3`, `4` |

Case-by-case inverse FORM results:

| case | beta | pf | lsf_count | glsf_count | hlsf_count | nit |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 2.0 | 0.02275 | 7 | 7 | 7 | 10 |
| 2 | 2.0 | 0.02275 | 6 | 7 | 7 | 10 |
| 3 | 2.0 | 0.02275 | 7 | 7 | 7 | 10 |
| 4 | 2.0 | 0.02275 | 7 | 7 | 7 | 10 |

Design point stochastic variables result (all cases):

| case | var_name | x | fractile | char_value | partial_factor |
|---|---|---:|---:|---:|---:|
| 1 | N | 1.07 | 0.5 | 1 | 1.07 |
| 1 | M | 0.01259 | 0.5 | 0.01 | 1.259 |
| 1 | Y | 172.3 | 0.5 | 126 | 1.367 |
| 2 | N | 1.07 | 0.5 | 1 | 1.07 |
| 2 | M | 0.06278 | 0.5 | 0.05 | 1.256 |
| 2 | Y | 35.35 | 0.5 | 25.8 | 1.37 |
| 3 | N | 1.071 | 0.5 | 1 | 1.071 |
| 3 | M | 0.1252 | 0.5 | 0.1 | 1.252 |
| 3 | Y | 18.26 | 0.5 | 13.3 | 1.373 |
| 4 | N | 1.075 | 0.5 | 1 | 1.075 |
| 4 | M | 0.6145 | 0.5 | 0.5 | 1.229 |
| 4 | Y | 4.477 | 0.5 | 3.22 | 1.39 |

Load and resistance partial factors:

- No dedicated "Load and resistance partial factors" table was written in this `AT624` results workbook, because `LSFreturnsLandR = False` and therefore no load/resistance partial factors were calculated or reported.

Notes:

- This example demonstrates the `DesignProblem.cases` structure for running multiple reliability design scenarios in one command.
- All cases converge close to the same target reliability while using different case-level input statistics.

## Recommended Authoring Pattern

1. Start with a single-case definition (`default`) to validate setup and derivatives.
2. Add `cases` when you need scenario sweeps under a common target reliability.
3. Keep one summary table per run, then add per-case details (partial factors, design points, failure-point statistics) as needed.
