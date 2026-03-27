# Profile Configuration Reference

This page provides a complete reference for all options available in YAML profile files. Profiles control configuration for analysis, design, and simulation runs, including plotting options and reporting settings.

## Profile Structure

A profile YAML file contains four main sections:

- reporting_options: Report generation settings
- rfad_plot_options: Reliability-based Failure Assessment Diagram settings
- lsf_plot_options: Limit State Function plot settings
- reliability_options: Reliability analysis, SORM, Monte Carlo, Importance Sampling, and optimization settings

---

## Reporting Options

Options for saving analysis results and visualizations.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `save_plots_to_pdf` | bool | `true` | Whether to save all generated plots in PDF format |
| `save_plots_to_pickle` | bool | `true` | Whether to save figure objects in pickle format for later retrieval and editing |
| `save_excel_summary` | bool | `true` | Whether to save the numerical results summary to an Excel file |

**Example:**
```yaml
reporting_options:
  save_plots_to_pdf: true
  save_plots_to_pickle: true
  save_excel_summary: true
```

---

## RFAD Plot Options

Options for Reliability-based Failure Assessment Diagram (RFAD) visualization.

| Option | Type | Default | Range/Values | Description |
|--------|------|---------|--------------|-------------|
| `n_x_points` | int | `30` | [5, 60] | Number of grid points along the first variable axis |
| `n_y_points` | int | `29` | [5, 60] | Number of grid points along the second variable axis |
| `plot_beta` | bool | `true` | - | Whether to plot the safety index (reliability index beta) contours |
| `plot_alphas` | bool | `true` | - | Whether to plot alpha values (normalized sensitivity factors) for each variable |
| `plot_base_point` | bool | `true` | - | Whether to plot the base point (mean of input variables) on the diagram |
| `with_labels` | bool | `true` | - | Whether to add text labels to the base point on the diagram |
| `ignore_axis_funcs` | bool | `false` | - | Whether to ignore axis transformation functions and plot in original variable space |
| `view` | str or tuple | `"auto"` | `"auto"`, `"default"`, `"XY"`, `"XZ"`, `"YZ"`, `"-XY"`, `"-XZ"`, `"-YZ"` (case-insensitive) or tuple of 3 floats (elevation, azimuth, roll) in degrees | View orientation for 3D perspective |
| `cmap` | str or list | `"plasma"` | Valid matplotlib colormap name or list of shape (n, 4) with RGBA values in [0, 1] where 1 ≤ n ≤ 256 | Colormap specification |
| `type` | str | `"surface"` | `"contour"`, `"surface"` | Plot visualization type |

**Example:**
```yaml
rfad_plot_options:
  n_x_points: 30
  n_y_points: 29
  plot_beta: true
  plot_alphas: true
  plot_base_point: true
  with_labels: true
  ignore_axis_funcs: false
  view: "auto"
  cmap: "plasma"
  type: "surface"
```

---

## LSF Plot Options

Options for Limit State Function (LSF) 3D visualization.

| Option | Type | Default | Range/Values | Description |
|--------|------|---------|--------------|-------------|
| `n_x_points` | int | `30` | [5, 60] | Number of grid points along the first variable axis |
| `n_y_points` | int | `29` | [5, 60] | Number of grid points along the second variable axis |
| `plot_base_point` | bool | `true` | - | Whether to plot the base point (mean of input variables) on the LSF surface |
| `plot_failure_point` | bool | `true` | - | Whether to plot the design point (Most Probable Point of Failure) on the LSF surface |
| `with_labels` | bool | `true` | - | Whether to add text labels to the base and failure points |
| `ignore_axis_funcs` | bool | `false` | - | Whether to ignore axis transformation functions and plot in original variable space |
| `view` | str or tuple | `"auto"` | `"auto"`, `"default"`, `"XY"`, `"XZ"`, `"YZ"`, `"-XY"`, `"-XZ"`, `"-YZ"` (case-insensitive) or tuple of 3 floats (elevation, azimuth, roll) in degrees | View orientation for 3D perspective |
| `cmap` | str or list | `"plasma"` | Valid matplotlib colormap name or list of shape (n, 4) with RGBA values in [0, 1] where 1 ≤ n ≤ 256 | Colormap specification |
| `type` | str | `"surface"` | `"contour"`, `"surface"` | Plot visualization type |

**Example:**
```yaml
lsf_plot_options:
  n_x_points: 30
  n_y_points: 29
  plot_base_point: true
  plot_failure_point: true
  with_labels: true
  ignore_axis_funcs: false
  view: "auto"
  cmap: "plasma"
  type: "surface"
```

---

## Reliability Options

Options for reliability calculations and related numerical settings. This section collects tolerances, algorithm choices, finite-difference settings, plotting flags, Monte Carlo controls and various checks used across FORM, SORM, inverse problems and design optimization routines.

### FORM and Inverse FORM Settings

These settings apply to both FORM and Inverse FORM.

!!! info "Optimization algorithm"
    Reliafy CLI does not use the traditional Hasofer-Lind Rackwitz-Fiessler (HL-RF) algorithm found in many reliability textbooks and commercial tools. Instead, FORM and Inverse FORM rely on [`scipy.optimize.minimize`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html) as the optimizer, using the `method` parameter set to `"trust-constr"` for smooth limit-state functions and `"COBYQA"` for non-smooth ones. This provides access to the full scipy minimizer feature set, including variable bounds and general constraints, which the classical HL-RF cannot handle.

| Option | Type | Default | Range | Description |
|--------|------|---------|-------|-------------|
| `form_xtol` | float | `0.0001` | [1e-8, 1e-2] | Tolerance for FORM termination (variable changes) |
| `form_gtol` | float | `0.0001` | [1e-8, 1e-2] | Tolerance for FORM termination (Lagrangian gradient norm changes) |
| `form_maxiter` | int | `1000` | [1, ∞) | Maximum iterations for FORM |
| `form_random_start` | bool | `false` | - | Use a random starting point for FORM |
| `form_seed` | int or null | `null` | - | Random seed for FORM/Inverse FORM random starts |

### Design Optimization Settings

| Option | Type | Default | Range | Description |
|--------|------|---------|-------|-------------|
| `design_xtol` | float | `0.001` | [1e-8, 1e-2] | Tolerance for design optimization termination (variable changes) |
| `design_gtol` | float | `0.001` | [1e-8, 1e-2] | Tolerance for design optimization termination (Lagrangian gradient norm changes) |
| `design_maxiter` | int | `1000` | [1, ∞) | Maximum iterations for design optimization |
| `design_random_start` | bool | `false` | - | Use a random starting point for design optimization |
| `design_seed` | int or null | `null` | - | Random seed for design optimization random starts |

### General Reliability Settings

| Option | Type | Default | Values | Description |
|--------|------|---------|--------|-------------|
| `alpha_direction` | str | `"outward"` | `"outward"`, `"inward"` | Direction convention for the alpha vector |
| `use_nearest_correlation` | bool | `false` | - | Controls fallback behavior when Cholesky decomposition of the correlation matrix fails. If `false`, the run stops with an error. If `true`, Reliafy attempts to replace the matrix with a nearest positive semidefinite (PSD) correlation matrix using the method in [Higham and Strabić (2011)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1969689). |
| `qn_epsilon` | float | `1e-8` | [1e-8, 1e-2] | Tolerance used by the quasi-Newton SR1 (Symmetric Rank 1) update when `sor_fit_method` is set to `SR1` |

### SORM Settings

| Option | Type | Default | Values | Description |
|--------|------|---------|--------|-------------|
| `sor_method` | str | `"SOSPA_H"` | `"Breitung"`, `"Tvedt3T"`, `"TvedtSI"`, `"TvedtDI"`, `"Hohenbichler"`, `"Koyluoglu"`, `"ZhaoEmpirical"`, `"SOSPA_L"`, `"SOSPA_H"`, `"IFFT"` | SORM method to use |
| `sor_approximation` | str | `"Paraboloid"` | `"Paraboloid"`, `"Taylor2"` | SORM approximation type |
| `sor_fit_method` | str or null | `null` | `"FiniteDiff"`, `"ZhaoPF"`, `"Kiureghian"`, `"SR1"`, `"AnalyticAll"`, `null` (auto) | Method for SORM limit state function fitting |
| `sor_fit_delta_factor` | float | `1.0` | [0.1, 10.0] | Factor used to scale the method-recommended delta when numerically estimating SORM fit parameters for ZhaoPF and Kiureghian methods |
| `sor_fdm` | str | `"forward"` | `"central"`, `"forward"`, `"backward"` | Finite-difference method for gradient and Hessian (used when `sor_fit_method` is `FiniteDiff`) |
| `sor_fdm_hess_form` | str | `"full"` | `"full"`, `"diagonal"` | Hessian form for finite-difference approximation (used when `sor_fit_method` is `FiniteDiff`) |
| `force_curvatures` | bool | `false` | - | Force curvature computations even if not strictly required by selected SORM options |

#### SORM References

Use these references as starting points for method details and derivation nuances. Keep in mind that explanations on this page are intentionally brief and implementation-focused.

**`sor_method`**

- `"Breitung"`: Breitung, K. (1984). "Asymptotic approximations for multinormal integrals." *J. Eng. Mech.*, ASCE, 110(3), 357–366. [→](https://ascelibrary.org/doi/10.1061/%28ASCE%290733-9399%281984%29110%3A3%28357%29)
- `"Tvedt3T"`, `"TvedtSI"`, `"TvedtDI"`: Although not the original reference, Der Kiureghian, A., Lin, H.-Z., and Hwang, S.-J. (1987) provides a thorough description of these methods in Appendix I — "Second-order reliability approximations." *J. Eng. Mech.*, ASCE, 113(8), 1208–1225. [→](https://ascelibrary.org/doi/10.1061/%28ASCE%290733-9399%281987%29113%3A8%281208%29)
- `"Hohenbichler"`: Hohenbichler, M., and Rackwitz, R. (1988). "Improvement of second-order reliability estimates by importance sampling." *J. Eng. Mech.*, ASCE, 114(12), 2195–2199. [→](https://ascelibrary.org/doi/10.1061/%28ASCE%290733-9399%281988%29114%3A12%282195%29)
- `"Koyluoglu"`: Köylüoğlu, H. U., and Nielsen, S. R. K. (1994). "New approximations for SORM integrals." *Structural Safety*, 13(4), 235–246. [→](https://www.sciencedirect.com/science/article/pii/0167473094900310)
- `"ZhaoEmpirical"`: Zhao, Y.-G., and Ono, T. (1999a). "New approximations for SORM: Part 1." *J. Eng. Mech.*, ASCE, 125(1), 79–85. [→](https://ascelibrary.org/doi/10.1061/%28ASCE%290733-9399%281999%29125%3A1%2879%29)
- `"SOSPA_L"`, `"SOSPA_H"`:
    - Hu, Z., and Du, X. (2018). "Saddlepoint approximation reliability method for quadratic functions in normal variables." *Structural Safety*, 71, 24–32. [→](https://www.sciencedirect.com/science/article/pii/S0167473017301169)
    - Du, X., and Sudjianto, A. (2004). "A saddlepoint approximation method for uncertainty analysis." *Proc. ASME IDETC/CIE 2004*, Paper DETC2004-57269, pp. 445–452. [→](https://asmedigitalcollection.asme.org/IDETC-CIE/proceedings-abstract/IDETC-CIE2004/46946/445/308224)
    - [Additional SOSPA reference](https://doi.org/10.1080/03610910701730141)
- `"IFFT"`:
    - Zhao, Y.-G., and Ono, T. (1999b). "New approximations for SORM: Part 2." *J. Eng. Mech.*, ASCE, 125(1), 86–93. [→](https://ascelibrary.org/doi/10.1061/%28ASCE%290733-9399%281999%29125%3A1%2886%29)
    - Tvedt, L. (1990). "Distribution of quadratic forms in normal space—application to structural reliability." *J. Eng. Mech.*, ASCE, 116(6), 1183–1197. [→](https://ascelibrary.org/doi/10.1061/%28ASCE%290733-9399%281990%29116%3A6%281183%29)
    - Der Kiureghian, A., Lin, H.-Z., and Hwang, S.-J. (1987). "Second-order reliability approximations." *J. Eng. Mech.*, ASCE, 113(8), 1208–1225. [→](https://ascelibrary.org/doi/10.1061/%28ASCE%290733-9399%281987%29113%3A8%281208%29)

**`sor_approximation`**

- `Paraboloid`: Local quadratic fit of the failure surface at the design point, using principal curvatures.
- `Taylor2`: Second-order Taylor expansion of the limit-state function at the design point.
- Reference: Tvedt, L. (1990). "Distribution of quadratic forms in normal space-application to structural reliability." *J. Eng. Mech.*, ASCE, 116(6), 1183-1197. [→](https://ascelibrary.org/doi/10.1061/%28ASCE%290733-9399%281990%29116%3A6%281183%29)

**`sor_fit_method`**

- `FiniteDiff`: numerical differentiation tooling — [numdifftools](https://pypi.org/project/numdifftools/)
- `SR1`: quasi-Newton symmetric rank-one update — [Wikipedia: Symmetric rank-one](https://en.wikipedia.org/wiki/Symmetric_rank-one)
- `Kiureghian`: point-fitting procedure following Der Kiureghian, A. (2022). *Structural and System Reliability*. Cambridge University Press.
- `ZhaoPF`: point-fitting procedure — Zhao and Ono (1999a) above.
- `AnalyticAll`: uses user-provided analytic gradient and Hessian from the problem definition.
- `null` (auto): Reliafy selects the most appropriate fit strategy based on available problem information.

**`sor_fit_delta_factor`**

- Applies to `ZhaoPF` and `Kiureghian` fit methods as a scaling factor on the method-recommended point-fitting step size. Keep default unless Reliafy diagnostics suggest adjustment.

### IFFT Settings (for IFFT-based SORM)

| Option | Type | Default | Range | Description |
|--------|------|---------|-------|-------------|
| `ifft_std_domain` | float | `16.0` | [2, 24] | Standard deviations covered when computing IFFT of characteristic functions |
| `ifft_n` | int | `4096` | [2^8, 2^16], powers of 2 | Number of points used in IFFT |
| `plot_ifft_funcs` | bool | `true` | - | Generate diagnostic plots for IFFT operations |

### SOSPA Settings (for SOSPA-based SORM)

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `plot_sospa_funcs` | bool | `true` | Generate diagnostic plots for SOSPA characteristic functions and derivatives |

### Derivative Checking

These options validate user-provided derivatives against numerical finite differences.

| Option | Type | Default | Values | Description |
|--------|------|---------|--------|-------------|
| `check_lsf_diffs_wrtx` | bool | `false` | - | Validate user-provided LSF derivatives against numerical diffs w.r.t. real-space variables |
| `check_lsf_diffs_wrtu` | bool | `true` | - | Validate user-provided LSF derivatives against numerical diffs w.r.t. standard-normal (U-space) variables |
| `lsf_diffs_check_method` | str | `"forward"` | `"central"`, `"forward"`, `"backward"`, `"complex"` | Method for LSF derivative checks |
| `check_varscf_diffs_wrtx` | bool | `false` | - | Validate user-provided stochastic variables constraints (real-space) |
| `check_varscf_diffs_wrtu` | bool | `true` | - | Validate user-provided stochastic variables constraints (U-space) |
| `varscf_diffs_check_method` | str | `"forward"` | `"central"`, `"forward"`, `"backward"`, `"complex"` | Method for stochastic variables constraint derivative checks |
| `check_dof_diffs` | bool | `true` | - | Validate user-provided design objective function derivatives against numerical diffs |
| `dof_diffs_check_method` | str | `"forward"` | `"central"`, `"forward"`, `"backward"`, `"complex"` | Method for design objective function derivative checks |
| `check_dcf_diffs` | bool | `true` | - | Validate user-provided design constraint function derivatives against numerical diffs |
| `dcf_diffs_check_method` | str | `"forward"` | `"central"`, `"forward"`, `"backward"`, `"complex"` | Method for design constraint function derivative checks |

### Monte Carlo Settings

| Option | Type | Default | Range | Description |
|--------|------|---------|-------|-------------|
| `mc_n` | float or null | `null` | [1e3, 1e8] or `null` (auto) | Monte Carlo sample size (null means automatic) |
| `mc_max_cv` | float | `0.05` | [0.01, 1.0] | If `mc_n` is `null`, MC runs in cycles until the estimated failure-probability CV is <= `mc_max_cv` |
| `mc_seed` | int or null | `null` | - | Random seed for Monte Carlo simulations; set a value for repeatable results, or leave as `null` to allow small run-to-run differences |
| `mc_remove_oob` | bool | `true` | - | Remove out-of-bounds samples during MC simulation (bounds or constraint violations) |

### Importance Sampling Settings

| Option | Type | Default | Values/Range | Description |
|--------|------|---------|--------------|-------------|
| `is_method` | str | `"kde"` | `"kde"`, `"mixture"`, `"mcmc"`, `"mpp_normal"` | Importance sampling proposal method |
| `is_kde_bandwidth` | str or float | `"scott"` | `"scott"`, `"silverman"` or positive float | Bandwidth selection method for KDE or numeric value |
| `is_mixture_components` | int | `6` | [1, 16] | Number of mixture components for mixture IS methods |
| `is_mixture_cov_type` | str | `"full"` | `"full"`, `"tied"`, `"diag"`, `"spherical"` | Covariance type for mixture IS methods |
| `is_fit_samples` | int | `2000` | [100, 100000] | Number of samples to collect for fitting the proposal distribution (for KDE and mixture IS) |

### MCMC Importance Sampling Settings

| Option | Type | Default | Range | Description |
|--------|------|---------|-------|-------------|
| `is_mcmc_chains` | int | `5` | [1, 100] | Number of parallel Metropolis chains to run during MCMC proposal fitting; a practical starting point is about 2 times the number of stochastic variables |
| `is_mcmc_chain_length` | int | `500` | [100, 10000] | Length of each MCMC chain during proposal fitting |
| `is_mcmc_thinning` | int | `3` | [1, 100] | Number of samples skipped between retained samples in each MCMC chain during proposal fitting |
| `is_mcmc_burnin` | int | `200` | [100, 1000] | Number of samples to discard as burn-in during MCMC proposal fitting |
| `is_mcmc_fit_method` | str | `"kde"` | `"kde"`, `"mixture"` | Method used to fit the MCMC proposal distribution |

#### IS References

Use these references as starting points for method details and implementation background. Keep in mind that explanations on this page are intentionally brief and implementation-focused.

**`is_method: "kde"`**

- `KernelDensity` from scikit-learn — [sklearn.neighbors.KernelDensity](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KernelDensity.html). Bandwidth selection follows the `is_kde_bandwidth` option (`"scott"` or `"silverman"` rules, or a numeric value).

**`is_method: "mixture"`**

- `BayesianGaussianMixture` from scikit-learn — [sklearn.mixture.BayesianGaussianMixture](https://scikit-learn.org/stable/modules/generated/sklearn.mixture.BayesianGaussianMixture.html). Number of components and covariance type are controlled by `is_mixture_components` and `is_mixture_cov_type`.

**`is_method: "mcmc"`**

- Xiao, S., and Nowak, W. (2022). "Reliability sensitivity analysis based on a two-stage Markov chain Monte Carlo simulation." *Aerospace Science and Technology*, 130, 107938. [→](https://doi.org/10.1016/j.ast.2022.107938)
- Cotter, S. L., Roberts, G. O., Stuart, A. M., and White, D. (2013). "MCMC methods for functions: modifying old algorithms to make them faster." *Statistical Science*, 28(3), 424–446. [→](https://doi.org/10.1214/13-STS421)
- Roberts, G. O., and Rosenthal, J. S. (2007). "Coupling and ergodicity of adaptive Markov chain Monte Carlo algorithms." *Journal of Applied Probability*, 44(2), 458–475. [→](https://www.jstor.org/stable/27595854)

**`is_method: "mpp_normal"`**

- Centers the importance sampling proposal distribution on the Most Probable Point (MPP), also called the design point or failure point. The MPP is the point on the limit-state surface closest to the origin in standard normal space, found by FORM. A Gaussian proposal centered there concentrates samples near the dominant failure region. See the FORM method and the textbooks listed on the [home page](../index.md#recommended-texts).

**Example:**

```yaml
reliability_options:
  # FORM
  form_xtol: 0.0001
  form_gtol: 0.0001
  form_maxiter: 1000
  form_random_start: false
  form_seed: null
  
  # Design
  design_xtol: 0.001
  design_gtol: 0.001
  design_maxiter: 1000
  design_random_start: false
  design_seed: null
  
  # General
  alpha_direction: "outward"
  use_nearest_correlation: false
  qn_epsilon: 1e-8
  
  # SORM
  sor_method: "SOSPA_H"
  sor_approximation: "Paraboloid"
  sor_fit_method: null
  sor_fit_delta_factor: 1.0
  sor_fdm: "forward"
  sor_fdm_hess_form: "full"
  force_curvatures: false
  
  # IFFT
  ifft_std_domain: 16.0
  ifft_n: 4096
  plot_ifft_funcs: true
  
  # SOSPA
  plot_sospa_funcs: true
  
  # Derivative checking
  check_lsf_diffs_wrtx: false
  check_lsf_diffs_wrtu: true
  lsf_diffs_check_method: "forward"
  check_varscf_diffs_wrtx: false
  check_varscf_diffs_wrtu: true
  varscf_diffs_check_method: "forward"
  check_dof_diffs: true
  dof_diffs_check_method: "forward"
  check_dcf_diffs: true
  dcf_diffs_check_method: "forward"
  
  # Monte Carlo
  mc_n: null
  mc_max_cv: 0.05
  mc_seed: null
  mc_remove_oob: true
  
  # Importance Sampling
  is_method: "kde"
  is_kde_bandwidth: "scott"
  is_mixture_components: 6
  is_mixture_cov_type: "full"
  is_fit_samples: 2000
  is_mcmc_chains: 5
  is_mcmc_chain_length: 500
  is_mcmc_thinning: 3
  is_mcmc_burnin: 200
  is_mcmc_fit_method: "kde"
```

---

## Notes

- Enum-style fields accept either the enum member name (case-insensitive) or the enum value
- Out-of-range or invalid values trigger a profile validation error
- Set `form_seed`, `design_seed`, and/or `mc_seed` to a non-null integer for repeatable runs when random number generation is involved
