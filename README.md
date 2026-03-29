# Reliafy CLI

Reliafy CLI is a Python-based command-line interface for reliability analysis, reliability-based design optimization, and simulation workflows with profile-based configuration.

Core capabilities include First-Order Reliability Method (FORM), Second-Order Reliability Method (SORM), Inverse FORM, Inverse SORM, Monte Carlo simulation, and Importance Sampling for rare-event probability estimation. These workflows cover forward reliability evaluation, reliability-constrained design, and post-design simulation using a consistent problem-module interface. Reliafy supports correlated, non-normal random variables through the Nataf transformation, an isoprobabilistic mapping to standard normal space.

Run outputs are designed for practical engineering decisions and reporting workflows. Depending on options, results include reliability metrics and design points, tabulated summaries (Excel/JSON), plot reports (PDF), and pickled Matplotlib figure objects for post-processing.

## Quick Start

```zsh
# Install from PyPI
pip install reliafy

# Show help
reliafy --help

# Copy packaged example problems
reliafy examples copy

# Run an analysis with the default profile
reliafy analyze default --include-sorm --plot-rfad
```

## Profiles

Profiles are YAML files under `profiles/` that control run options.

```zsh
# Create and edit a custom profile
reliafy profile new custom
reliafy profile nano custom
# or
reliafy profile vim custom

# Validate, list, copy, rename
reliafy profile validate custom
reliafy profile list
reliafy profile copy default mycopy
reliafy profile rename oldname newname
```

## Full Documentation

The complete documentation site is built with MkDocs Material.

- Site navigation mirrors CLI commands and common tasks.
- To preview the docs locally, run `mkdocs serve` from the project root and open the URL printed in the terminal (typically `http://127.0.0.1:8000`).

## Requirements

- Python 3.10+
- Internet connection for API access and authentication

## Notes

- Auth0 device flow uses public values (domain, client ID, audience). No client secret is used in the CLI.
