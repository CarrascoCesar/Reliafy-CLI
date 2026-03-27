# Simulate Example: Chan2 (Classic Monte Carlo)

This page documents a simulate run in plain Monte Carlo mode (without importance sampling).

Note: Table values are rounded to 4 significant figures for readability. Very small/large values use scientific notation. Refer to the Excel/JSON result files for full precision.

## Run Context

Problem module:

- `problems/problems2/Chan2Problem.py`

Recorded result set:

- `results/2026-03-16/10-52-46/Chan2-51baa.xlsx`
- `results/2026-03-16/10-52-46/Chan2-51baa.json`
- `results/2026-03-16/10-52-46/Chan2-51baa.py`
- `results/2026-03-16/10-52-46/Chan2-51baa.pickle`
- `results/2026-03-16/10-52-46/Chan2-51baa.pdf`
- `results/2026-03-16/10-52-46/profile-51baa.yaml`

Profile and run mode from saved profile:

- Profile used: `default`
- `run_type: simulate`
- `include_mc: true`
- `mc_with_is: false`

For results-folder and filename conventions, see [CLI Result Files](../../cli/results-files.md).

Equivalent command shape:

```bash
reliafy simulate <profile>
```

The `simulate` command without `-i` runs plain (crude) Monte Carlo only.

## Profile Customization

This example uses the `default` profile, but simulate behavior is configurable. See [Profile Options Reference](../../profiles/profile-reference.md).

- Monte Carlo controls: `reliability_options.mc_n`, `mc_max_cv`, `mc_seed`, `mc_remove_oob`.
- Report toggles: `reporting_options.save_plots_to_pdf`, `save_plots_to_pickle`, `save_excel_summary`.

## Problem File Used

**Source:** Chan, C. L. and Low, B. K., "Practical second-order reliability analysis applied to foundation engineering," *International Journal for Numerical and Analytical Methods in Geomechanics*, 2012, vol. 36, no. 11, p. 1387–1409, Problem 2, p. 1397. [→](https://onlinelibrary.wiley.com/doi/full/10.1002/nag.1057)

`Chan2Problem.py` defines:

- Stochastic variables: `cp`, `fp`, `g`, `Ph`, `Pv` — all Normal
- Correlation: full 5 × 5 matrix defined using the `cor` key (see note below)
- Deterministic variables: `B = 5.0`, `L = 25.0`, `D = 1.8`, `h = 2.5`
- `LSFreturnsGradient: False`, `LSFreturnsHessian: False`, `LSFreturnsLandR: True`
- Limit state returns load ($P_v / B'$) and resistance (bearing-capacity formula)

!!! note "Using `cor` vs `cor_list`"
    `Chan2Problem.py` specifies the correlation matrix as a full **n × n list of lists** under the `cor` key.
    This is an alternative to `cor_list`, which accepts a flat list of `[var1, var2, value]` pairs.
    If neither `cor` nor `cor_list` is supplied, Reliafy assumes zero correlation for all variables.
    Either key may be used; the full matrix form is convenient when many off-diagonal correlations are non-zero.

```python
"StochasticVariables": {
    "name": ["cp", "fp", "g", "Ph", "Pv"],
    "type": ["normal", "normal", "normal", "normal", "normal"],
    "cor": [
        [1.0, -0.5,  0.0,  0.0, 0.0],
        [-0.5, 1.0,  0.5,  0.0, 0.0],
        [0.0,  0.5,  1.0,  0.0, 0.0],
        [0.0,  0.0,  0.0,  1.0, 0.5],
        [0.0,  0.0,  0.0,  0.5, 1.0],
    ],
    "mean": [15.0, 25.0, 20.0, 400.0, 800.0],
    "std":  [4.5,  5.0,  2.0,  40.0,  80.0],
},
```

Because `LSFreturnsLandR: True`, the CLI generates a **Load and Resistance Histogram** in addition to the per-variable and LSF histograms.

## Extracted Results Worksheet Tables

The tables below are transcribed from the `Results` worksheet in `Chan2-51baa.xlsx`.

#### Header Information

| Field | Value |
|---|---|
| Problem | `Chan2` |
| Request ID | `9614c856e5bb41f4b96bd9b1d4051baa` |
| Run time | `00 min 25.62 sec` |

#### Deterministic Variables

| var_name | value |
|---|---:|
| B | 5 |
| L | 25 |
| D | 1.8 |
| h | 2.5 |

#### Stochastic Variables Definition

| var_name | var_type | mean | std | param1 | param2 |
|---|---|---:|---:|---:|---:|
| cp | Normal | 15 | 4.5 | 15 | 4.5 |
| fp | Normal | 25 | 5 | 25 | 5 |
| g | Normal | 20 | 2 | 20 | 2 |
| Ph | Normal | 400 | 40 | 400 | 40 |
| Pv | Normal | 800 | 80 | 800 | 80 |

#### Monte Carlo Results

| beta | pf | cv | max_cv | size | %_removed | cycles | auto_size | mc_with_is |
|---:|---:|---:|---:|---:|---:|---:|---|---|
| 1.5409 | 0.06167 | 0.002252 | 0.05 | 3,000,000 | 0.000733 | 3 | True | False |

#### Monte Carlo Variable Statistics and Correlations

The sampled statistics confirm the input distributions and correlation structure.

| var_name | mean | std | %_oob | cor(cp) | cor(fp) | cor(g) | cor(Ph) | cor(Pv) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| cp | 14.9993 | 4.4999 | 0 | 1.0000 | −0.4999 | 0.0003 | 0.0003 | 0.0008 |
| fp | 24.9972 | 4.9994 | 0 | −0.4999 | 1.0000 | 0.5003 | −0.0008 | 0.0000 |
| g | 19.9997 | 2.0012 | 0 | 0.0003 | 0.5003 | 1.0000 | 0.0001 | 0.0008 |
| Ph | 400.035 | 39.985 | 0 | 0.0003 | −0.0008 | 0.0001 | 1.0000 | 0.5006 |
| Pv | 799.993 | 79.962 | 0 | 0.0008 | 0.0000 | 0.0008 | 0.5006 | 1.0000 |

#### Notes Reported by Reliafy

1. Validation: Stochastic variables definition and limit state function validation required 1 function call.
2. Monte Carlo: Completed 3 cycles with `1.00e+06` samples per cycle.
3. Monte Carlo: Detected 22 NaN values in the limit state function out of `3.00e+06` samples. Review the list of code warnings and update the limit state function to address their source.

### Interpretation Snapshot

- `beta = 1.541`, `pf = 6.17%` — a relatively low reliability index for a bearing-capacity problem with correlated soil parameters.
- The coefficient of variation (`cv = 0.00225`) is well below `max_cv = 0.05`, indicating high MC precision with 3 million samples.
- The sampled correlation matrix closely matches the targets: `cor(cp, fp) ≈ −0.500`, `cor(fp, g) ≈ 0.500`, `cor(Ph, Pv) ≈ 0.501`.
- A small number of NaN results (22 out of 3,000,000) were detected. These typically arise from geometric degeneration in the bearing-capacity formula (e.g., `B' ≤ 0` due to large eccentricity). They do not invalidate the result at this sample size.

### Generated Figures

The PDF result file for this run is saved as `results/2026-03-16/10-52-46/Chan2-51baa.pdf`.
That PDF is composed of vector-based pages, rendered below at 2× resolution from each page.

#### Figure 1: MC Histogram — `cp`

![Chan2 MC histogram for cp](../images/chan2-51baa-01-cp-histogram.png)

#### Figure 2: MC Histogram — `fp`

![Chan2 MC histogram for fp](../images/chan2-51baa-02-fp-histogram.png)

#### Figure 3: MC Histogram — `g`

![Chan2 MC histogram for g](../images/chan2-51baa-03-g-histogram.png)

#### Figure 4: MC Histogram — `Ph`

![Chan2 MC histogram for Ph](../images/chan2-51baa-04-Ph-histogram.png)

#### Figure 5: MC Histogram — `Pv`

![Chan2 MC histogram for Pv](../images/chan2-51baa-05-Pv-histogram.png)

#### Figure 6: Histogram of Limit State Function Values

![Chan2 limit state function histogram](../images/chan2-51baa-06-lsf-histogram.png)

#### Figure 7: Load and Resistance Histogram

Generated because `LSFreturnsLandR: True` in the problem file.

![Chan2 load and resistance histogram](../images/chan2-51baa-07-load-resistance.png)
