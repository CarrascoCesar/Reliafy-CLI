# Simulate

Run Monte Carlo simulation with optional importance sampling and FORM/SORM analysis.

!!! info "Before your first run"
	If you want to test this command with packaged sample problems, first run:
	```bash
	reliafy examples copy
	```
	Then select a problem file from `./problems/` when the file picker opens.

## Basic Usage

Usage: `reliafy simulate <profile> [OPTIONS]`

## Command Options

### Monte Carlo Options

- `--mc-with-is`, `-i`: Use importance sampling with Monte Carlo simulation

### Reliability Methods

- `--include-form`, `-f`: Include first-order reliability method (FORM) analysis
- `--include-sorm`, `-s`: Include second-order reliability method (SORM) analysis (automatically enables FORM)

### Plotting Options

- `--plot-lsf`, `-l`: Generate limit state function plot
- `--plot-pdfs`, `-p`: Generate probability density function plots

### General Options

- `--open-results`, `-o`: Open result files after completion — including the Excel report, the PDF report, and any Matplotlib figures saved as pickle files

## Examples

### Basic Monte Carlo Simulation
```bash
reliafy simulate default
```

### MC with Importance Sampling
```bash
reliafy simulate default --mc-with-is
```

### MC with FORM/SORM and Plots
```bash
reliafy simulate default -f -s -l -p
```

### Complete Simulation with IS
```bash
reliafy simulate default -i -s -p
```

### Using Custom Profile
```bash
reliafy simulate myprofile --include-form --plot-pdfs
```

!!! tip "Combining short flags"
	Short flags can be merged into a single argument. For example:
	```bash
	reliafy simulate default -f -s -l -p
	```
	is equivalent to:
	```bash
	reliafy simulate default -fslp
	```
	Both forms are valid. The expanded form is easier to read; the combined form is faster to type.

## Notes

- If `--include-sorm` is specified without `--include-form`, FORM is automatically enabled
- If importance sampling method is set to `mpp_normal` in the profile, FORM is automatically enabled
- Monte Carlo sample size is configured in the profile file

## Aliases

- `sim`: Short alias
