# Design Problem Definition

This section covers problem definition for the `design` command. Design problems extend the base problem dictionary with `DesignProblem` keys and can follow two distinct workflows:

1. Inverse FORM: compute partial factors/design point values that satisfy a target reliability (`TargetBeta` or `TargetPf`).
2. Objective optimization: compute design variable values that minimize an objective while satisfying reliability constraints.

## When To Use Which Design Type

- Use Inverse FORM when code calibration, load/resistance factor calibration, or characteristic-value back-calculation is the goal.
- Use objective optimization when cost/weight/performance minimization is the goal and reliability is one of the constraints.

## Design Documentation Layout

- [Design Keys Reference](design-keys.md): full `DesignProblem` dictionary reference and validation rules.
- [Inverse FORM Examples](inverse-form.md): worked Inverse FORM examples (`AT625` single-case and `AT624` multi-case).
- [Objective Optimization](optimization.md): worked objective optimization example (`Sorensen81Problem.py`) including additional optimization keys.

## Notes On Cases

- A design problem can define a single default case or multiple named cases.
- This applies to both workflows: Inverse FORM and objective optimization.
- If `DesignProblem.cases` is omitted, Reliafy creates a `default` case from the top-level `StochasticVariables` definition.
- Multi-case definitions are useful when target reliability remains fixed but statistical definitions or design context vary per scenario.
