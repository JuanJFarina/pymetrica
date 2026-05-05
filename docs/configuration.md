# Configuration

Pymetrica reads optional threshold and exclusion settings from
`[tool.pymetrica]` in `pyproject.toml`.

## Where Configuration Comes From

Configuration is loaded from the current working directory at command startup.
In practice, that means you should run Pymetrica from the repository whose
`pyproject.toml` contains the thresholds you want to enforce.

If no `pyproject.toml` or `[tool.pymetrica]` section is found, Pymetrica uses
its built-in defaults.

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
top_findings = 5
```

Thresholds are positive by default. Set a threshold to `0` when you want to
disable failure gating for that metric. `exclude` defaults to an empty list,
and `top_findings` defaults to `5`.

| Setting | Default | Compared against | Used by |
| --- | --- | --- | --- |
| `aloc_fail_threshold` | `30` | `aloc_percentage` greater than the threshold | `aloc`, `run-all` |
| `cc_fail_threshold` | `7` | `lloc_per_cc` lower than the threshold | `cc`, `run-all` |
| `hv_fail_threshold` | `30` | `hv_per_lloc` greater than the threshold | `hv`, `run-all` |
| `po_all_fail_threshold` | `10` | `all_primitives_percent` greater than the threshold | `po`, `run-all` |
| `po_targeted_fail_threshold` | `2` | `targeted_primitives_percent` greater than the threshold | `po`, `run-all` |
| `mc_fail_threshold` | `25` | `maintainability_cost` greater than the threshold | `mc`, `run-all` |
| `exclude` | `[]` | Relative file paths matched with `fnmatch` | `run-all`, `base-stats`, `aloc`, `cc`, `hv`, `po`, `mc`, `li` |
| `top_findings` | `5` | Number of worst files shown in threshold failure messages; `0` disables the lists | `aloc`, `cc`, `hv`, `po`, `mc`, `run-all` |

## Exclude Patterns

`exclude` is evaluated during parsing and skips matching Python files before
metrics are produced.

Important details:

- patterns are matched against each analyzed file path relative to the resolved
  analysis root
- paths are normalized to forward slashes before matching
- matching uses Python's `fnmatch`, so entries such as `generated/*` or
  `legacy/test_*.py` are valid
- layer discovery and folder counts happen separately, so an excluded directory
  can still appear as an empty layer or in `folders_number`

For example, if `pymetrica run-all .` resolves the codebase root to `src/`,
then `exclude = ["generated/*"]` matches files such as
`src/generated/models.py` because the relative path being checked is
`generated/models.py`.

## Exit-Code Behavior

### `run-all`

Threshold exit statuses are enforced by the `BASIC_HOOK` report backend. The
default `BASIC_TERMINAL` backend prints values and exits with `0`.

`run-all -rt BASIC_HOOK` combines failures into a single exit code:

- `1` for ALOC
- `2` for CC
- `4` for HV
- `8` for Maintainability Cost
- `16` for Primitive Obsession

If more than one threshold fails, the exit code is the sum of the matching
values. For example:

- `5` means ALOC and HV failed.
- `24` means Primitive Obsession and Maintainability Cost failed.

Instability is always computed, but it is not threshold-gated.

### Single-Metric Commands

With `BASIC_HOOK`, single-metric commands exit with their metric-specific code
when their own positive threshold fails:

- `aloc`: `1`
- `cc`: `2`
- `hv`: `4`
- `mc`: `8`
- `po`: `16`

The `li` command does not currently support a threshold setting.

## Report Type

Pymetrica currently ships with two report backends:

```text
BASIC_TERMINAL
BASIC_HOOK
```

These values are accepted by the `-rt` / `--report-type` option on the
reporting commands. `BASIC_TERMINAL` is the normal CLI output and exits with
`0`. `BASIC_HOOK` is used by the published pre-commit hooks, reports only
failed metrics, and returns the threshold-based exit status.

## CI Usage

A common pattern is to configure thresholds in the repository and run the full
analysis in CI:

```bash
pymetrica run-all -rt BASIC_HOOK .
```

If you only want to gate one metric, use the corresponding single-metric
command instead:

```bash
pymetrica mc -rt BASIC_HOOK .
```

## Pre-commit Hooks

Pymetrica also publishes ready-to-use `pre-commit` hooks for `run-all` and the
threshold-capable single-metric commands:

```yaml
repos:
  - repo: https://github.com/JuanJFarina/pymetrica
    rev: v1.5.0
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
- `PYMETRICA_LOG_LEVEL` can be set to `DEBUG`, `INFO`, `WARNING`, or `ERROR`.
  Invalid or missing values fall back to `WARNING`.
- Because configuration is resolved from the current working directory, running
  `pymetrica path/to/other/project` from outside that project will not use the
  other project's thresholds unless you change into that directory first.
- Exclusion patterns are evaluated relative to the resolved analysis root. When
  `pymetrica run-all .` auto-detects `src/`, `app/`, or a matching package
  directory, patterns are relative to that detected folder.
