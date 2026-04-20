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
- `mc`
- `li`

## Shared Conventions

- `DIR_PATH` is the directory Pymetrica will analyze.
- `-rt` / `--report-type` currently supports `BASIC_TERMINAL`.
- `run-all` combines multiple thresholds into one exit code. Individual metric
  commands exit with `1` when their own threshold fails.
- `li` reports instability, but it is not threshold-gated.

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
pymetrica run-all [--long-report] [-rt BASIC_TERMINAL] DIR_PATH
```

What it does:

- Parses the codebase.
- Computes `ALOC`, `CC`, `HV`, `Maintainability Cost`, and `Instability`.
- Prints either a short summary or a longer descriptive report.
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
- `10`: CC threshold exceeded
- `100`: HV threshold exceeded
- `1000`: Maintainability Cost threshold exceeded

For example, an exit code of `101` means both the ALOC and HV thresholds were
exceeded. Instability is always included in the report, but it does not
contribute to the exit code.

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
- `comment_line_ratio`
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

### `aloc`

```bash
pymetrica aloc [-rt BASIC_TERMINAL] DIR_PATH
```

Reports the `Abstract Lines Of Code` metric. Exits with `1` when
`aloc_fail_threshold` is configured and exceeded.

### `cc`

```bash
pymetrica cc [-rt BASIC_TERMINAL] DIR_PATH
```

Reports `Cyclomatic Complexity`. Exits with `1` when `cc_fail_threshold` is
configured and exceeded.

### `hv`

```bash
pymetrica hv [-rt BASIC_TERMINAL] DIR_PATH
```

Reports `Halstead Volume`. Exits with `1` when `hv_fail_threshold` is
configured and exceeded.

### `mc`

```bash
pymetrica mc [-rt BASIC_TERMINAL] DIR_PATH
```

Reports `Maintainability Cost`. Exits with `1` when `mc_fail_threshold` is
configured and exceeded.

### `li`

```bash
pymetrica li [-rt BASIC_TERMINAL] DIR_PATH
```

Reports layer instability values. This command does not currently enforce a
threshold-based failure status.

## Standalone Console Scripts

`pyproject.toml` also exposes a few convenience entrypoints:

- `pymetrica-run-all`
- `pymetrica-aloc`
- `pymetrica-cc`
- `pymetrica-hv`
- `pymetrica-mc`

These map directly to the same implementations used by the main `pymetrica`
subcommands. There are no separate standalone scripts for `status`,
`base-stats`, or `li`.
