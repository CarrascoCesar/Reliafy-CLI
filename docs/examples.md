# Packaged Example Problems

Reliafy CLI includes packaged example problems to help you get started with reliability analysis, design optimization, and Monte Carlo simulation.

## Copying Examples to Working Directory

First, copy the packaged example problems into your current working directory:

```bash
reliafy examples copy
```

Alias:

```bash
reliafy examples cp
```

This creates a local `./problems/` folder in your current directory.

## Listing Available Examples

List the packaged example files available in your installed Reliafy package:

```bash
reliafy examples list
```

Alias:

```bash
reliafy examples ls
```

This displays a table of packaged example problems.

To see files copied into your local working directory, inspect `./problems/` directly.

## Using Example Problems

When you run analysis, design, or simulation, Reliafy opens a file-selection dialog so you can choose a problem file from `./problems/`.

Analysis:

```bash
reliafy analyze default --include-sorm --plot-rfad
```

Design optimization:

```bash
reliafy design default --use-sorm
```

Monte Carlo simulation:

```bash
reliafy simulate default --plot-pdfs
```

The problem file is selected at run time for each command and is not persisted as part of the command options.
