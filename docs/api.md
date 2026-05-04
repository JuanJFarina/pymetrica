# API Reference

This reference is intentionally narrow: it follows the package's public exports
and works best alongside the guide pages.

If you are trying to use Pymetrica from the command line, start with
[CLI Reference](cli.md). If you are trying to understand the analysis model,
read [Architecture](architecture.md) and [Metrics](metrics.md) first.

## Using Pymetrica From Python

The CLI and the Python API share the same parser, calculators, and report
registry. A typical programmatic workflow is:

```python
from pymetrica.codebase_parser import create_diagram, parse_codebase
from pymetrica.metric_calculators import (
    AlocCalculator,
    CCCalculator,
    PrimitiveObsessionCalculator,
)
from pymetrica.report_generators import REPORTS_MAPPING

codebase = parse_codebase("path/to/project")

metrics = [
    AlocCalculator().calculate_metric(codebase),
    CCCalculator().calculate_metric(codebase),
    PrimitiveObsessionCalculator().calculate_metric(codebase),
]

report = REPORTS_MAPPING["BASIC_TERMINAL"]().generate_report(metrics)
print(report)

create_diagram(codebase, filename="architecture.mmd")
```

`parse_codebase()` applies the same exclusion rules used by the CLI, so any
configured `[tool.pymetrica].exclude` patterns still matter when you call the
library from Python.

## Extension Points

The most useful public extension points are:

- `MetricCalculator` subclasses for adding new metrics
- `ReportGenerator` subclasses for adding new report backends
- `REPORTS_MAPPING` for registering report backends under `-rt` names

Today the only bundled report backend is `BASIC_TERMINAL`, but the registry is
already part of the public reporting surface.

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
