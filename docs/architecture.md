# Architecture

Pymetrica is built as a parsing and reporting pipeline around a small set of
Pydantic models and metric calculators.

## Analysis Pipeline

```text
DIR_PATH
  -> resolve the base directory
  -> parse Python files into Code objects
  -> assemble a Codebase model
  -> calculate metrics
  -> render a report
```

At a high level:

- `codebase_parser` discovers files and builds the `Codebase` model
- `metric_calculators` produce `Metric` objects from that codebase
- `report_generators` turn those metrics into terminal output

## Base-Path Resolution

When you pass an explicit path such as `path/to/project`, Pymetrica analyzes
that directory directly.

When you pass `"."`, Pymetrica first resolves the current directory and then
checks a few common source-layout conventions:

- `src/`
- `app/`
- a package directory matching the current folder name with hyphens converted to
  underscores

If more than one candidate exists, Pymetrica checks them in that order and uses
the last matching candidate. This means a matching package directory wins over
`app/`, and `app/` wins over `src/`.

This makes `pymetrica run-all .` convenient for common Python project layouts,
but explicit paths are best when a repository contains more than one candidate
source directory.

## Layer Model

Pymetrica treats the immediate child directories of the resolved base path as
layers.

Important details:

- files directly under the base path are stored separately as root files
- `__pycache__` is excluded from initial layer discovery
- dot-prefixed directories are still discovered as layers by the parser
- syntax-error files are skipped during parsing
- the parser currently does not honor `.gitignore`
- `[tool.pymetrica].exclude` skips matching Python files after layer discovery,
  so excluded directories can still appear as empty layers or in folder counts

This layer model is what powers both the per-layer metrics and the instability
analysis.

## Data Models

The central models are:

- `Code` for one Python file and its parsed source metadata
- `Codebase` for the analyzed project structure
- `Metric` and `Results` for structured metric output
- `MetricCalculator` and `ReportGenerator` as extension points

See [API Reference](api.md) for the exported Python interfaces.

## Diagram Generation

`base-stats` can generate Mermaid `.mmd` output:

```bash
pymetrica base-stats --diagram path/to/project architecture.mmd
```

The generated diagram groups components by top-level layer and adds edges for
detected cross-layer dependencies.

Current behavior to know about:

- the diagram writer skips root-level files as diagram components
- components are top-level Python files inside each layer, plus immediate
  subdirectories when a layer contains nested code
- files whose names end in `__.py`, including `__init__.py`, are skipped by the
  component-file check
- dependency edges from nested files are collapsed to the immediate
  subdirectory component
- layer and component directory discovery skips `__pycache__` and hidden
  directories
- dependency edges are derived from `from ... import ...` statements
- generated files start with a Mermaid initialization block that adjusts diagram
  label styling
- when no filename is provided, Pymetrica writes
  `architecture_diagram_<UTC timestamp>.mmd`

## Reporting Model

Pymetrica currently ships with two report backends:

```text
BASIC_TERMINAL
BASIC_HOOK
```

The terminal backend supports:

- a short key/value report for compact output
- a longer summary report with descriptions and per-layer detail where
  available
- a zero exit status; it reports metrics but does not enforce thresholds

The hook backend is used by the published pre-commit hooks and reports only
failed metrics, or a success message when all thresholds pass. It is the backend
that returns threshold-based exit statuses for CI and hooks.

## Current Scope and Limits

The current architecture is intentionally small and focused. That means a few
important limits are worth documenting:

- layer analysis is based on top-level folders, not arbitrary architectural
  boundaries
- coupling analysis currently inspects `ImportFrom` relationships
- only the basic terminal and hook report generators are implemented today

Those constraints are useful to keep in mind when interpreting results or
planning future extensions.
