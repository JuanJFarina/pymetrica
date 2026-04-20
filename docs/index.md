# Pymetrica

Pymetrica is a static analysis tool for Python codebases that combines
classical software metrics with architecture-aware reporting.

It parses source files with the Python AST, groups code by top-level layers,
and produces reports that help you reason about complexity, maintainability,
and coupling.

## What You Can Do

- Run a full metrics sweep with `pymetrica run-all`.
- Inspect parser and codebase statistics with `pymetrica base-stats`.
- Generate Mermaid `.mmd` dependency diagrams for a codebase.
- Fail CI based on configurable thresholds from `pyproject.toml`.
- Drill into individual metrics such as ALOC, CC, HV, MC, and instability.

## Quick Start

```bash
pip install pymetrica
pymetrica run-all path/to/project
```

Pymetrica requires Python 3.10 or newer.

## Read Next

- [Getting Started](usage.md) for installation, first commands, and example
  output.
- [CLI Reference](cli.md) for every public command and supported option.
- [Configuration](configuration.md) for thresholds, exit codes, and CI usage.
- [Metrics](metrics.md) for metric definitions and interpretation guidance.
- [Architecture](architecture.md) for parsing, layering, and diagram behavior.
- [API Reference](api.md) for the package's public Python surface.

## Source

The project source, issue tracker, and release history live in the
[GitHub repository](https://github.com/JuanJFarina/pymetrica).
