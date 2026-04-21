# Metrics

Pymetrica reports five metrics today: `ALOC`, `CC`, `HV`, `Maintainability
Cost`, and `Instability`.

In the default short report, Pymetrica prints only the top-level values returned
by each metric. The long report adds descriptive summaries and, where
implemented, per-layer breakdowns.

## Abstract Lines Of Code (ALOC)

ALOC highlights abstraction-heavy lines rather than concrete operations.

The current implementation counts:

- import statements
- `__all__` assignments
- function definitions and their decorators
- class definitions and their decorators
- the logical body size of concrete classes that are never instantiated in the
  analyzed codebase

Reported fields:

- `aloc_number`
- `aloc_percentage`

The long report also includes per-layer ALOC totals.

## Cyclomatic Complexity (CC)

Cyclomatic Complexity measures how many decision paths exist in the analyzed
code.

Pymetrica walks the AST and counts branching and control-flow constructs, then
reports:

- `cc_number`
- `lloc_per_cc`

`lloc_per_cc` normalizes complexity against the amount of logical code. The long
report includes per-layer CC values.

## Halstead Volume (HV)

Halstead Volume estimates cognitive load from the number of operators and
operands in the codebase.

Pymetrica collects operator and operand counts from the AST and reports:

- `hv_number`
- `hv_per_lloc`

The long report also includes per-layer Halstead values.

## Maintainability Cost (MC)

Maintainability Cost is Pymetrica's maintainability score. Lower values are
better.

It is derived from:

- Halstead volume density
- cyclomatic complexity density
- a small size penalty based on logical lines of code

Reported fields:

- `maintainability_cost`
- `raw_line_cost`

`raw_line_cost` is the density-based portion of the score before the additional
size penalty is applied. The long report includes per-layer MC values.

## Instability

Instability measures how much a layer depends on other layers relative to how
much other layers depend on it.

Pymetrica uses the classic ratio:

```text
instability = efferent_coupling / (efferent_coupling + afferent_coupling)
```

Interpretation:

- `0.0` means stable
- values closer to `1.0` mean more outgoing dependency pressure

Important implementation details:

- instability is calculated per layer
- files at the codebase root are reported under a synthetic `root` layer
- the current dependency analysis is driven by `from ... import ...` statements
  between layers

## Short Report vs Long Report

The short report is optimized for automation and CI. It prints only the values
returned by each metric's `get_dict()` method.

That means:

- ALOC, CC, HV, and MC short reports omit their per-layer lists
- instability short output already includes the layer map, because its result is
  itself a dictionary of layer names to scores

Use `pymetrica run-all --long-report DIR_PATH` when you want the descriptive
summaries and per-layer breakdowns.

The individual `aloc`, `cc`, `hv`, `mc`, and `li` commands already use the
descriptive report format because they operate on one metric at a time. They do
not expose a separate `--long-report` switch.
