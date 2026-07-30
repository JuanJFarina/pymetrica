# Metrics

Pymetrica reports seven metrics today: `Base Stats`, `ALOC`, `CC`, `HV`,
`Primitive Obsession`, `Maintainability Cost`, and `Instability`.

In the default short report, Pymetrica prints only the top-level values returned
by each metric. The long report adds descriptive summaries and, where
implemented, per-layer breakdowns.

## Base Stats

Base Stats exposes parser-level information about the resolved analysis root:

- root folder path and name
- folder and Python file counts
- logical lines of code and logical lines per file
- comment count and comment-to-LLOC ratio
- class and function counts

It is included in `run-all` and is also available through the dedicated
`base-stats` command. Base Stats is informational, has an exit code of `0`, and
never fails a threshold.

## Abstract Lines Of Code (ALOC)

ALOC highlights abstraction-heavy lines rather than concrete operations.

The current implementation counts:

- import statements
- `__all__` assignments
- function definitions and their decorators
- class definitions and their decorators
- the logical body size of concrete classes that are never instantiated in the
  analyzed codebase

For the unused-class body adjustment, Pymetrica currently inspects top-level
class definitions. Classes inheriting from `ABC`, `ABCMeta`, `Protocol`, or
`Enum` are treated as abstract bases and do not receive the concrete-class body
penalty. A class is considered used when it appears in a direct call, a class
method call, or as a positional call argument.

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

The visitor currently increments complexity for `if` and ternary expressions,
`match` statements and cases, boolean `and`/`or` chains, `for`/`async for` and
`while` loops, loop `else` blocks, `try` handlers and `else` blocks,
`with`/`async with` items, `assert` statements, and comprehensions.

When `cc_fail_threshold` is configured, lower `lloc_per_cc` values fail the
threshold because they indicate more decision points per logical line.

## Halstead Volume (HV)

Halstead Volume estimates cognitive load from the number of operators and
operands in the codebase.

Pymetrica collects operator and operand counts from the AST and reports:

- `hv_number`
- `hv_per_lloc`

The long report also includes per-layer Halstead values.

The visitor counts operators for assignments, augmented assignments, binary,
unary, boolean, and comparison operations, `if`/`for`/`while`, and function and
class definitions. It counts operands from function names, class names, names,
attributes, and constants.

## Primitive Obsession (PO)

Primitive Obsession highlights type annotations that rely heavily on primitive
types instead of domain-specific abstractions.

The current implementation counts annotations for:

- primitive scalar types: `int`, `float`, `bool`, `str`, and `Any`
- targeted container types: `dict`, `list`, `tuple`, and `set`
- containers whose arguments are also primitive or targeted types
- `Any` as both primitive and targeted

The parser is intentionally narrow today. It recognizes simple names and
attributes such as `typing.Any`, subscripted built-in containers such as
`list[int]` or `dict[str, Any]`, and PEP 604 `|` unions when every member is a
supported primitive or targeted container form. Unsupported annotations,
including many custom types and uppercase typing aliases such as `typing.List`,
are ignored for this metric.

Short-report fields:

- `all_primitives_percent`
- `targeted_primitives_percent`

The percentages normalize annotation counts against total logical lines of code.
The long report summary includes the raw primitive counts and per-layer
primitive counts. Failure messages track whether the all-primitive or targeted
primitive threshold failed.

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

The implemented formula is:

```text
hv_density = hv_number / lloc_number
cc_density = cc_number / lloc_number
raw_line_cost = (hv_density * ((cc_density * 100) or 1)) / 20
maintainability_cost = raw_line_cost + (lloc_number * 0.001)
```

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

The short report is optimized for compact terminal output. It prints only the
values returned by each metric's `dict_` property when report content is
rendered. Use `-rt BASIC_HOOK` when you want threshold failures to affect the
process exit status in CI or hooks.

That means:

- Base Stats short output includes all parser-level fields
- ALOC, CC, HV, PO, and MC short reports omit their per-layer lists
- PO short reports also omit raw counts and failure flags, leaving only the two
  percentage fields
- instability short output already includes the layer map, because its result is
  itself a dictionary of layer names to scores

Use `pymetrica run-all --long-report [DIR_PATH]` when you want the descriptive
summaries and per-layer breakdowns. If omitted, `DIR_PATH` defaults to the
current directory.

The individual `aloc`, `cc`, `hv`, `po`, and `mc` commands already use the
descriptive report format because they operate on one metric at a time. They do
not expose a separate `--long-report` switch.
