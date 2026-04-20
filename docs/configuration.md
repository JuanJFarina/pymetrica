# Configuration

Pymetrica reads optional threshold settings from `[tool.pymetrica]` in
`pyproject.toml`.

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
mc_fail_threshold = 25
```

Each setting defaults to `0`, which disables failure gating for that metric.

| Setting | Compared against | Used by |
| --- | --- | --- |
| `aloc_fail_threshold` | `aloc_percentage` | `aloc`, `run-all` |
| `cc_fail_threshold` | `lloc_per_cc` | `cc`, `run-all` |
| `hv_fail_threshold` | `hv_per_lloc` | `hv`, `run-all` |
| `mc_fail_threshold` | `maintainability_cost` | `mc`, `run-all` |

## Exit-Code Behavior

### `run-all`

`run-all` combines failures into a single exit code:

- `1` for ALOC
- `10` for CC
- `100` for HV
- `1000` for Maintainability Cost

If more than one threshold fails, the exit code is the sum of the matching
values. For example:

- `11` means ALOC and CC failed.
- `1100` means HV and Maintainability Cost failed.

Instability is always computed, but it is not threshold-gated.

### Single-Metric Commands

The `aloc`, `cc`, `hv`, and `mc` commands each exit with `1` when their own
threshold is configured and exceeded.

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

## Practical Notes

- Threshold evaluation uses the metrics as Pymetrica reports them today. For
  example, CC gating is based on `lloc_per_cc`, not the raw `cc_number`.
- Because configuration is resolved from the current working directory, running
  `pymetrica path/to/other/project` from outside that project will not use the
  other project's thresholds unless you change into that directory first.
