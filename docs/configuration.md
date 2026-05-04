# Configuration

Pymetrica reads optional threshold and exclusion settings from
`[tool.pymetrica]` in `pyproject.toml`.

## Where Configuration Comes From

Configuration is loaded from the current working directory at command startup.
In practice, that means you should run Pymetrica from the repository whose
`pyproject.toml` contains the thresholds you want to enforce.

## Supported Settings

Example:

```toml
[tool.pymetrica]
aloc_fail_threshold = 30
cc_fail_threshold = 10
hv_fail_threshold = 30
po_all_fail_threshold = 10
po_targeted_fail_threshold = 2
mc_fail_threshold = 25
exclude = ["generated/*", "vendor/*"]
```

Each threshold defaults to `0`, which disables failure gating for that metric.
`exclude` defaults to an empty list.

| Setting | Compared against | Used by |
| --- | --- | --- |
| `aloc_fail_threshold` | `aloc_percentage` greater than the threshold | `aloc`, `run-all` |
| `cc_fail_threshold` | `lloc_per_cc` lower than the threshold | `cc`, `run-all` |
| `hv_fail_threshold` | `hv_per_lloc` greater than the threshold | `hv`, `run-all` |
| `po_all_fail_threshold` | `all_primitives_percent` greater than the threshold | `po`, `run-all` |
| `po_targeted_fail_threshold` | `targeted_primitives_percent` greater than the threshold | `po`, `run-all` |
| `mc_fail_threshold` | `maintainability_cost` greater than the threshold | `mc`, `run-all` |
| `exclude` | Relative file paths matched with `fnmatch` | `run-all`, `base-stats`, `aloc`, `cc`, `hv`, `po`, `mc`, `li` |

## Exclude Patterns

`exclude` is evaluated during parsing, before parser statistics, diagrams, or
metrics are produced.

Important details:

- patterns are matched against each analyzed file path relative to the resolved
  analysis root
- paths are normalized to forward slashes before matching
- matching uses Python's `fnmatch`, so entries such as `generated/*` or
  `legacy/test_*.py` are valid

For example, if `pymetrica run-all .` resolves the codebase root to `src/`,
then `exclude = ["generated/*"]` matches files such as
`src/generated/models.py` because the relative path being checked is
`generated/models.py`.

## Exit-Code Behavior

### `run-all`

`run-all` combines failures into a single exit code:

- `1` for ALOC
- `2` for CC
- `10` for HV
- `20` for Primitive Obsession
- `100` for Maintainability Cost

If more than one threshold fails, the exit code is the sum of the matching
values. For example:

- `11` means ALOC and HV failed.
- `120` means Primitive Obsession and Maintainability Cost failed.

Instability is always computed, but it is not threshold-gated.

### Single-Metric Commands

The `aloc`, `cc`, `hv`, `po`, and `mc` commands each exit with `1` when their
own threshold is configured and fails.

The `li` command does not currently support a threshold setting.

## Report Type

Pymetrica currently ships with one report backend:

```text
BASIC_TERMINAL
```

This value is accepted by the `-rt` / `--report-type` option on the reporting
commands.

## CI Usage

A common pattern is to configure thresholds in the repository and run the full
analysis in CI:

```bash
pymetrica run-all .
```

If you only want to gate one metric, use the corresponding single-metric
command instead:

```bash
pymetrica mc .
```

## Pre-commit Hooks

Pymetrica also publishes ready-to-use `pre-commit` hooks for `run-all` and the
threshold-gated single-metric commands:

```yaml
repos:
  - repo: https://github.com/JuanJFarina/pymetrica
    rev: v1.3.2
    hooks:
      - id: pymetrica
      - id: pymetrica-mc
      - id: pymetrica-po
```

Available hook IDs today:

- `pymetrica`
- `pymetrica-aloc`
- `pymetrica-cc`
- `pymetrica-hv`
- `pymetrica-po`
- `pymetrica-mc`

These hooks analyze the repository root (`.`) and ignore the filename list that
`pre-commit` normally passes to hooks. Thresholds and exclusions still come
from the repository's own `pyproject.toml`.

## Practical Notes

- Threshold evaluation uses the metrics as Pymetrica reports them today. For
  example, CC gating is based on `lloc_per_cc`, not the raw `cc_number`, and it
  fails when `lloc_per_cc` is below the configured threshold.
- Because configuration is resolved from the current working directory, running
  `pymetrica path/to/other/project` from outside that project will not use the
  other project's thresholds unless you change into that directory first.
- Exclusion patterns are evaluated relative to the resolved analysis root. When
  `pymetrica run-all .` auto-detects `src/`, `app/`, or a matching package
  directory, patterns are relative to that detected folder.
