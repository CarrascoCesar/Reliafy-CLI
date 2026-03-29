# Reliafy CLI: FORM, SORM, RBDO, and Monte Carlo Simulation in Python

Reliafy CLI is a Python-based command-line interface for reliability analysis, reliability-based design optimization, and simulation workflows with profile-based configuration.

Core capabilities include First-Order Reliability Method (FORM), Second-Order Reliability Method (SORM), Inverse FORM, Inverse SORM, Monte Carlo simulation, and Importance Sampling for rare-event probability estimation. These workflows cover forward reliability evaluation, reliability-constrained design, and post-design simulation using a consistent problem-module interface. Reliafy supports correlated, non-normal random variables through the Nataf transformation, an isoprobabilistic mapping to standard normal space.

Run outputs are designed for practical engineering decisions and reporting workflows. Depending on options, results include reliability metrics and design points, tabulated summaries (Excel/JSON), plot reports (PDF), and pickled Matplotlib figure objects for post-processing.

The documentation is written for practical use rather than theory derivation. It does not include in-depth theoretical derivations or detailed theory-first explanations. Across analysis, design, and simulation workflows, method descriptions are intentionally concise, and most method-specific references are consolidated in the [Profile Options Reference](profiles/profile-reference.md).

!!! info "Pricing and Sustainability Notice"
    Reliafy CLI is **free to use** at this time. The CLI communicates with a hosted API, and the associated computation and infrastructure costs are currently funded by the developer during this early phase of operation.

    To support ongoing maintenance and service delivery as usage grows, a monthly subscription of approximately **$8/month** is planned for a future release. Payment processing will be handled through [Stripe](https://stripe.com).

    Any transition from free access to a paid subscription model will be communicated in advance. Existing users will receive clear notice before any pricing changes take effect.

## Who This Tool Is For

Reliafy CLI was initially developed with academia in mind. The primary audience is students, instructors, and researchers working in risk and reliability, structural reliability, probabilistic failure analysis, and advanced probability and statistics.

Typical use cases include:

- Courses on risk and reliability methods, structural reliability, probabilistic analysis of failure, and advanced probability and statistics.
- Research at universities and research centers focused on reliability methods, failure analysis, code calibration and development, and related uncertainty-quantification workflows.


### Recommended Texts

- Ang, A. H.-S., and Tang, W. H. (2007). *Probability Concepts in Engineering: Emphasis on Applications to Civil and Environmental Engineering* (2nd ed.). John Wiley and Sons.
- Der Kiureghian, A. (2022). *Structural and System Reliability*. Cambridge University Press.
- Robert, Christian P., and Casella, George. (2004). *Monte Carlo Statistical Methods*. Springer New York.
- Sørensen, John Dalsgaard. (2004). *Notes in Structural Reliability Theory and Risk Analysis*. Aalborg, February 2004. [→](https://filelist.tudelft.nl/TBM/Over%20faculteit/Afdelingen/Values%2C%20Technology%20and%20Innovation/People/Full%20Professors/Pieter%20van%20Gelder/Citations/citatie215.pdf)

## Core Workflows

Reliafy CLI provides five core reliability workflows:

### First-Order Reliability Method (FORM)
Fast baseline reliability assessment. Provides reliability index (β), failure probability (Pf), and most probable point (MPP). Ideal for screening and sensitivity analysis.  
→ [Analyze Command](cli/analyze.md) | [FORM Example](problem-authoring/analyze/form-only.md)

### Second-Order Reliability Method (SORM)
Curvature-aware refinement near the most probable point (MPP). Used after FORM for improved approximation at the MPP.  
→ [SORM + Monte Carlo Example](problem-authoring/analyze/sorm-monte-carlo.md)

### Inverse FORM and Inverse SORM
Code calibration and reliability factor derivation. When no objective function is defined, computes partial factors or design point values that satisfy a target reliability index. Useful for load/resistance factor calibration and characteristic-value back-calculation.  
→ [Design Command](cli/design.md) | [Inverse FORM Examples](problem-authoring/design/inverse-form.md)

### Reliability-Based Design Optimization (RBDO)
Optimization under reliability constraints. When an objective function is defined in the problem, computes design variable values that minimize the objective while satisfying reliability constraints.  
→ [Design Command](cli/design.md) | [Optimization Examples](problem-authoring/design/optimization.md)

### Monte Carlo Simulation and Importance Sampling
Distribution-level validation and robustness checks. Provides empirical failure probability and tail behavior analysis.  
→ [Simulate Command](cli/simulate.md) | [Classic Monte Carlo](problem-authoring/simulate/classic-monte-carlo.md) | [Importance Sampling](problem-authoring/simulate/importance-sampling.md)

## Quick Start

1. Install the CLI (and required dependencies) from PyPI:

    ```bash
    pip install reliafy
    ```

2. View available commands:

    ```bash
    reliafy --help
    ```

3. Copy example problems:

    ```bash
    reliafy examples cp
    ```

4. Run an analysis with the default profile:

    ```bash
    reliafy analyze default --include-sorm --plot-rfad
    ```

!!! note "Developer install"
    If you are working from a local clone of the source repository, use an editable install instead:
    ```bash
    pip install -e .
    ```
    This links directly to your source folder so code changes take effect without reinstalling.

## Main Commands

When you run an analysis, design, or simulation command, Reliafy opens a file-picker popup so you can select the problem file to execute. If you are new to problem files, start with [Examples](examples.md) and then see [Problem Definition](problem-authoring/index.md) for how custom files are structured.

### Analyze: Forward Reliability Assessment
Run forward reliability analysis using FORM, SORM, and Monte Carlo methods to estimate failure probability and MPP sensitivity.

Usage: `reliafy analyze <profile> [OPTIONS]`

[Full options and examples →](cli/analyze.md)

### Design: Design Optimization and Factor Calibration
Run design workflows using Inverse FORM and Inverse SORM methods. Supports two modes: (1) code calibration via Inverse FORM when no objective function is present, and (2) reliability-based design optimization when an objective function is defined to minimize cost/weight/performance while meeting reliability constraints.

Usage: `reliafy design <profile> [OPTIONS]`

[Full options and examples →](cli/design.md)

### Simulate: Monte Carlo Simulation with Importance Sampling
Run Monte Carlo simulation with optional importance sampling for rare-event probability validation and robustness verification.

Usage: `reliafy simulate <profile> [OPTIONS]`

[Full options and examples →](cli/simulate.md)

## Configuration

Reliafy CLI uses YAML profile files to configure analysis parameters. Create and manage profiles using:

Create a new profile:

```bash
reliafy profile new myprofile
```

Edit the profile:

```bash
reliafy profile nano myprofile
```

List all profiles:

```bash
reliafy profile ls
```

See the [Profiles](profiles/index.md) page for detailed profile management commands and the [Profile Options Reference](profiles/profile-reference.md) for complete configuration options.

## Authentication

Reliafy CLI authenticates automatically the first time you run any command — if no valid token is found, you will be prompted to log in before the command proceeds. No manual setup is required.

You can also trigger or re-run authentication manually, or check your current login status:

Manually authenticate (or re-authenticate):

```bash
reliafy user auth
```

Check authentication status:

```bash
reliafy user id
```

See the [Auth](auth.md) page for more details.

## Requirements

- Python 3.10+
- Internet connection for API access and authentication
- Valid Reliafy API credentials

## Getting Help

All commands support the `--help` flag for detailed usage information:

```bash
reliafy --help
reliafy analyze --help
reliafy profile --help
```

## Software References

For third-party Python library citation guidance, see [Software and Library References](software-references.md). That section separates:

- CLI dependencies users install in their environment
- API dependencies documented for attribution/credit only

## Citing Reliafy

If you use Reliafy in journal papers, reports, theses, or other scholarly work, cite Reliafy itself in addition to any underlying libraries or method references that are materially relevant to your work.

- Carrasco, C. (2026). *Reliafy CLI*. Zenodo. <https://doi.org/10.5281/zenodo.19267557>

Include the exact Reliafy version used in your work. For version-specific DOI citations, use the corresponding Zenodo release record.

## Contact

For questions, feedback, or support, reach out at [reliafy.app@gmail.com](mailto:reliafy.app@gmail.com).
