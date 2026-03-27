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

After copying, list the available local example files:

```bash
reliafy examples list
```

Alias:

```bash
reliafy examples ls
```

This displays a table of the example problems available in `./problems/`.

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

Profiles configure run settings, but they do not store the selected problem file path.
