# Getting Started

## Installation

Install the latest published package from PyPI:

```bash
pip install pymetrica
```

Or install the project from source:

```bash
git clone https://github.com/JuanJFarina/pymetrica.git
cd pymetrica
pip install -e .
```

Pymetrica requires Python 3.10 or newer.

## Confirm the CLI Is Available

```bash
pymetrica status
```

Expected output:

```text
Pymetrica health check passed. All systems operational.
```

## Run Your First Analysis

Analyze a Python project with the full metrics pipeline:

```bash
pymetrica run-all path/to/project
```

The default output is a short terminal report with the top-level values for
every metric. Use `--long-report` when you want the descriptive summaries and
per-layer breakdown.

Thresholds are enforced when you use the hook report backend:

```bash
pymetrica run-all -rt BASIC_HOOK path/to/project
```

You can combine it with `--long-report` if you want the longer failure output.
Any configured `[tool.pymetrica].exclude` patterns are applied before the
codebase is parsed.

### Example Short Report

This example comes from the bundled sample codebase under
`tests/sample_codebases/small_codebase`:

```text
----------------------------------------------------------------------------------------------------
Short Report
----------------------------------------------------------------------------------------------------
Metric: Abstract Lines Of Code
aloc_number: 6
aloc_percentage: 15.0
----------------------------------------------------------------------------------------------------
Metric: Cyclomatic Complexity
cc_number: 23
lloc_per_cc: 1.7391304347826086
----------------------------------------------------------------------------------------------------
Metric: Halstead Volume
hv_number: 704.5342159112735
hv_per_lloc: 17.613355397781838
----------------------------------------------------------------------------------------------------
Metric: Primitive Obsession
all_primitives_percent: 0.0
targeted_primitives_percent: 0.0
----------------------------------------------------------------------------------------------------
Metric: Maintainability Cost
maintainability_cost: 50.678396768622775
raw_line_cost: 50.638396768622776
----------------------------------------------------------------------------------------------------
Metric: Instability
root: 0.0
----------------------------------------------------------------------------------------------------
```

If you switch to a single-metric command such as `pymetrica cc path/to/project`,
Pymetrica always prints the descriptive report format instead of this short
compact layout.

## Inspect Base Stats and Generate a Diagram

If you want a parser-level overview before running the full metrics set, start
with `base-stats`:

```bash
pymetrica base-stats path/to/project
```

To also write a Mermaid diagram file:

```bash
pymetrica base-stats --diagram path/to/project architecture.mmd
```

When `--diagram` is set without a filename, Pymetrica writes
`architecture_diagram_<UTC timestamp>.mmd` in the current working directory.

## Understand the Main Output Areas

Pymetrica currently exposes six metrics:

- `ALOC` for abstraction-heavy lines and unused concrete class bodies.
- `CC` for cyclomatic complexity.
- `HV` for Halstead volume.
- `PO` for primitive obsession in type annotations.
- `MC` for maintainability cost.
- `Instability` for layer-level coupling.

See [Metrics](metrics.md) for the full definitions and reporting details.

## Where to Go Next

- [CLI Reference](cli.md) documents every public command and option.
- [Configuration](configuration.md) covers thresholds, exclusions, hooks, exit
  codes, and CI use.
- [Architecture](architecture.md) explains layer detection and diagram output.
- [API Reference](api.md) covers the exported Python modules.
