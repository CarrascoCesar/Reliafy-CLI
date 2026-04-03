# Result Files

All CLI commands (`analyze`, `design`, and `simulate`) save outputs under a timestamped folder in `results/`.

## Location Pattern

```text
results/<YYYY-MM-DD>/<HH-MM-SS>/
```

`<YYYY-MM-DD>` and `<HH-MM-SS>` are generated at run time.

## File Naming Pattern

Inside each run folder, Reliafy saves files using:

```text
<ProblemName>-<suffix>.<ext>
```

- `<ProblemName>` comes from the problem definition.
- `<suffix>` is the last 5 characters of the server request ID.
- `<ext>` depends on enabled outputs.

Typical outputs:

- `<ProblemName>-<suffix>.xlsx`
- `<ProblemName>-<suffix>.json`
- `<ProblemName>-<suffix>.py`
- `<ProblemName>-<suffix>.pdf` (if `reporting_options.save_plots_to_pdf: true`)
- `<ProblemName>-<suffix>.pickle` (if `reporting_options.save_plots_to_pickle: true`)
- `profile-<suffix>.yaml`

## Design Runs

For `design` runs, Reliafy does not generate plot artifacts as part of the run output.

- No `<ProblemName>-<suffix>.pdf` file is created.
- No `<ProblemName>-<suffix>.pickle` file is created.

This behavior is intentional and matches the design-run notes documented in the Problem Definition design examples.

## Notes

- Every run gets a new request ID, so `<suffix>` changes every run.
- The timestamped directory and filenames are deterministic for a given run ID.
- `design` runs may produce fewer plot files than `analyze` or `simulate`, depending on reporting options and run type.

!!! info "API-side file retention"
	Reliafy does not retain run files on the API side after processing completes. Submitted problem modules and generated artifacts (for example `.xlsx`, `.pdf`, and `.pickle`) are removed using secure deletion (`srm`).
