# Reliafy CLI

Reliafy CLI provides reliability analysis, design, and simulation workflows with simple profile-based configuration.

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
- Methods are domain-independent (engineering, finance, statistics, medicine): see the Unified View section at https://reliafy.pages.dev/#unified-view-across-domains.
- Developer preview: `mkdocs serve` then open the shown URL.

## Requirements

- Python 3.10+
- Internet connection for API access and authentication

## Notes

- Auth0 device flow uses public values (domain, client ID, audience). No client secret is used in the CLI.
