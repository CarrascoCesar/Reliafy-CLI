# CLI Command Overview

Reliafy CLI provides three primary run commands:

- `analyze` for forward reliability assessment (FORM, optional SORM and MC)
- `design` for inverse reliability and reliability-based design optimization
- `simulate` for Monte Carlo simulation with optional importance sampling

When you run any of these commands, Reliafy opens a file-picker popup so you can choose the problem file to execute.

If you are new to problem files, start with [Packaged Examples](../examples.md) and then review [Problem Definition](../problem-authoring/index.md).

## Analyze: Forward Reliability Assessment

Run forward reliability analysis using FORM, SORM, and Monte Carlo methods to estimate failure probability and MPP sensitivity.

Usage: `reliafy analyze <profile> [OPTIONS]`

[Full options and examples ->](analyze.md)

## Design: Design Optimization and Factor Calibration

Run design workflows for both inverse reliability calibration and reliability-based design optimization.

Supports two modes:

- Code calibration via Inverse FORM when no objective function is present
- Reliability-based design optimization when an objective function is defined to minimize cost/weight/performance while meeting reliability constraints

Usage: `reliafy design <profile> [OPTIONS]`

[Full options and examples ->](design.md)

## Simulate: Monte Carlo Simulation with Importance Sampling

Run Monte Carlo simulation with optional importance sampling for rare-event probability validation and robustness verification.

Usage: `reliafy simulate <profile> [OPTIONS]`

[Full options and examples ->](simulate.md)
