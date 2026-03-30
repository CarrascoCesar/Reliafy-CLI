# Analyze: Forward Reliability Assessment

Run forward reliability analysis using the First-Order Reliability Method (FORM), Second-Order Reliability Method (SORM), and Monte Carlo simulation to estimate failure probability, reliability index (β), and most probable point (MPP).

!!! info "Before your first run"
	If you want to test this command with packaged sample problems, first run:
	```bash
	reliafy examples copy
	```
	Then select a problem file from `./problems/` when the file picker opens.

## Basic Usage

Usage: `reliafy analyze <profile> [OPTIONS]`

## Command Options

### Reliability Methods

- `--include-sorm`, `-s`: Include second-order reliability method (SORM) analysis

### Monte Carlo Options

- `--include-mc`, `-m`: Include Monte Carlo simulation
- `--mc-with-is`, `-i`: Use importance sampling with Monte Carlo (automatically enables `--include-mc`)

### Plotting Options

- `--plot-rfad`, `-r`: Generate reliability-based failure assessment diagram plots
- `--plot-lsf`, `-l`: Generate limit state function plots
- `--plot-pdfs`, `-p`: Generate probability density function plots

### General Options

- `--open-results`, `-o`: Open result files after completion — including the Excel report, the PDF report, and any Matplotlib figures saved as pickle files

## Examples

### Basic FORM Analysis
```bash
reliafy analyze default
```

### FORM + SORM with Plots
```bash
reliafy analyze default --include-sorm --plot-rfad --plot-lsf
```

### Complete Analysis with MC
```bash
reliafy analyze default -s -m -i -r -l -p
```

### Using Custom Profile
```bash
reliafy analyze myprofile --include-sorm --plot-rfad
```

!!! tip "Combining short flags"
	Short flags can be merged into a single argument. For example:
	```bash
	reliafy analyze default -s -m -i -r -l -p
	```
	is equivalent to:
	```bash
	reliafy analyze default -smirlp
	```
	Both forms are valid. The expanded form is easier to read; the combined form is faster to type.

## Aliases

- `analyse`: British spelling variant
- `an`: Short alias
