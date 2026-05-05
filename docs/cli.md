# CLI Reference

Pymetrica installs the main `pymetrica` command-line entrypoint and a small set
of standalone helper scripts for common metric runs.

## Main Entrypoint

```bash
pymetrica [OPTIONS] COMMAND [ARGS]...
```

Available commands:

- `status`
- `run-all`
- `base-stats`
- `aloc`
- `cc`
- `hv`
- `po`
- `mc`
- `li`

## Shared Conventions

- `DIR_PATH` is the directory Pymetrica will analyze.
- `-rt` / `--report-type` supports `BASIC_TERMINAL` and `BASIC_HOOK`.
- All parsing commands honor `[tool.pymetrica].exclude` patterns from the
  current repository configuration.
- `run-all` combines multiple thresholds into one exit code. Individual metric
  commands exit with `1` when their own threshold fails.
- Only `run-all` supports `--long-report`. Single-metric commands always print
  the descriptive report format.
- `li` reports instability, but it is not threshold-gated.
- `BASIC_HOOK` is intended for pre-commit hooks and reports only failed metrics.

## `status`

Checks that the CLI is installed and runnable.

```bash
pymetrica status
```

Expected output:

```text
Pymetrica health check passed. All systems operational.
```

## `run-all`

Runs the full metrics pipeline across the target codebase.

```bash
pymetrica run-all [--long-report] [-rt BASIC_TERMINAL|BASIC_HOOK] DIR_PATH
```

What it does:

- Parses the codebase.
- Computes `ALOC`, `CC`, `HV`, `Primitive Obsession`,
  `Maintainability Cost`, and `Instability`.
- Prints a short summary by default, or a longer descriptive report when
  `--long-report` is set.
- Returns a composite non-zero exit code if any configured thresholds fail.

Examples:

```bash
pymetrica run-all .
pymetrica run-all --long-report path/to/project
pymetrica run-all -rt BASIC_TERMINAL path/to/project
```

### `run-all` Exit Codes

Threshold failures are additive:

- `1`: ALOC threshold exceeded
- `2`: CC threshold failed
- `4`: HV threshold exceeded
- `8`: Primitive Obsession threshold exceeded
- `16`: Maintainability Cost threshold exceeded

For example, an exit code of `5` means both the ALOC and HV thresholds were
exceeded. An exit code of `24` means Primitive Obsession and Maintainability
Cost failed. The maximum composite failure code is `31`. Instability is always
included in the report, but it does not contribute to the exit code.

## `base-stats`

Parses the target codebase and prints parser-level statistics.

```bash
pymetrica base-stats [--diagram] DIR_PATH [DIAGRAM_FILENAME]
```

The output includes:

- `root_folder_path`
- `root_folder_name`
- `folders_number`
- `files_number`
- `lloc_number`
- `lloc_file_ratio`
- `comments_number`
- `comment_lloc_ratio`
- `classes_number`
- `functions_number`

Examples:

```bash
pymetrica base-stats .
pymetrica base-stats --diagram .
pymetrica base-stats --diagram path/to/project architecture.mmd
```

When `--diagram` is enabled without `DIAGRAM_FILENAME`, Pymetrica writes a file
named `architecture_diagram_<UTC timestamp>.mmd`.

## Single-Metric Commands

Use these commands when you want one metric at a time instead of the full
pipeline.

These commands always emit the descriptive report format. There is no
single-metric equivalent of `run-all --long-report`.

### `aloc`

```bash
pymetrica aloc [-rt BASIC_TERMINAL|BASIC_HOOK] DIR_PATH
```

Reports the `Abstract Lines Of Code` metric. Exits with `1` when
`aloc_fail_threshold` is configured and exceeded.

### `cc`

```bash
pymetrica cc [-rt BASIC_TERMINAL|BASIC_HOOK] DIR_PATH
```

Reports `Cyclomatic Complexity`. Exits with `1` when `cc_fail_threshold` is
configured and `lloc_per_cc` falls below it.

### `hv`

```bash
pymetrica hv [-rt BASIC_TERMINAL|BASIC_HOOK] DIR_PATH
```

Reports `Halstead Volume`. Exits with `1` when `hv_fail_threshold` is
configured and exceeded.

### `po`

```bash
pymetrica po [-rt BASIC_TERMINAL|BASIC_HOOK] DIR_PATH
```

Reports `Primitive Obsession`. Exits with `1` when either
`po_all_fail_threshold` or `po_targeted_fail_threshold` is configured and
exceeded.

### `mc`

```bash
pymetrica mc [-rt BASIC_TERMINAL|BASIC_HOOK] DIR_PATH
```

Reports `Maintainability Cost`. Exits with `1` when `mc_fail_threshold` is
configured and exceeded.

### `li`

```bash
pymetrica li [-rt BASIC_TERMINAL|BASIC_HOOK] DIR_PATH
```

Reports layer instability values. This command does not currently enforce a
threshold-based failure status.

## Standalone Console Scripts

`pyproject.toml` also exposes a few convenience entrypoints:

- `pymetrica-run-all`
- `pymetrica-aloc`
- `pymetrica-cc`
- `pymetrica-hv`
- `pymetrica-po`
- `pymetrica-mc`

These map directly to the same implementations used by the main `pymetrica`
subcommands. There are no separate standalone scripts for `status`,
`base-stats`, or `li`.
