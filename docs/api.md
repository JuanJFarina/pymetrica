# API Reference

This reference is intentionally narrow: it follows the package's public exports
and works best alongside the guide pages.

If you are trying to use Pymetrica from the command line, start with
[CLI Reference](cli.md). If you are trying to understand the analysis model,
read [Architecture](architecture.md) and [Metrics](metrics.md) first.

## Models

The `models` package contains the core data structures and abstract base types
used throughout the project.

::: pymetrica.models

## Codebase Parser

The `codebase_parser` package exposes the main parser entrypoints and diagram
generation helpers.

::: pymetrica.codebase_parser

## Metric Calculators

The `metric_calculators` package re-exports the calculators, result types, and
CLI callables that make up the supported metrics surface.

::: pymetrica.metric_calculators

## Report Generators

The report layer is small today. `REPORTS_MAPPING` is the registry used by the
CLI, and `BasicTerminalReport` is the only bundled implementation.

::: pymetrica.report_generators

### Utilities

The `utils` package exposes configuration loading, logging, and profiler
helpers.

::: pymetrica.utils
