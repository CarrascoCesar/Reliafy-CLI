# Design: Factor Calibration and Reliability-Based Design Optimization

Run design workflows that support two distinct modes depending on the problem definition: code calibration and partial factor derivation using Inverse FORM or Inverse SORM when no objective function is defined, or reliability-based design optimization (RBDO) when an objective function is defined to minimize cost, weight, or performance while satisfying reliability constraints.

!!! info "Before your first run"
	If you want to test this command with packaged sample problems, first run:
	```bash
	reliafy examples copy
	```
	Then select a problem file from `./problems/` when the file picker opens.

## Basic Usage

Usage: `reliafy design <profile> [OPTIONS]`

## Command Options

### Reliability Methods

- `--use-sorm`, `-s`: Use second-order reliability method (SORM) for design optimization

### General Options

- `--open-results`, `-o`: Open result files after completion — including the Excel report, the PDF report, and any Matplotlib figures saved as pickle files

## Examples

### Basic FORM-based Design
```bash
reliafy design default
```

### SORM-based Design
```bash
reliafy design default --use-sorm
```

### Using Custom Profile
```bash
reliafy design myprofile -s
```

!!! tip "Combining short flags"
	Short flags can be merged into a single argument. For example:
	```bash
	reliafy design default -s -o
	```
	is equivalent to:
	```bash
	reliafy design default -so
	```
	Both forms are valid. The expanded form is easier to read; the combined form is faster to type.

## Design Problem Requirements

Design optimization requires design-specific definitions in the selected problem module (the `DesignProblem` dictionary).

Typical required items include:

- Reliability target (`TargetBeta` or `TargetPf`)
- Fractiles and optional design cases
- For objective optimization: objective function, design variables, initial guess, and bounds

See [Design Keys Reference](../problem-authoring/design/design-keys.md) for required problem-module keys.

## Aliases

- `des`: Short alias
