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
    HalsteadVolumeCalculator,
    InstabilityCalculator,
    MaintainabilityCostCalculator,
    PrimitiveObsessionCalculator,
)
from pymetrica.report_generators import REPORTS_MAPPING

codebase = parse_codebase("path/to/project")

metrics = [
    AlocCalculator().calculate_metric(codebase),
    CCCalculator().calculate_metric(codebase),
    HalsteadVolumeCalculator().calculate_metric(codebase),
    PrimitiveObsessionCalculator().calculate_metric(codebase),
    MaintainabilityCostCalculator().calculate_metric(codebase),
    InstabilityCalculator().calculate_metric(codebase),
]

report_generator = REPORTS_MAPPING["BASIC_TERMINAL"](metrics)
print(report_generator.long_report().content)

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

Bundled report backends are `BASIC_TERMINAL` for terminal output and
`BASIC_HOOK` for pre-commit style output that only shows failed metrics by
default and returns threshold-based exit statuses. Instantiate a backend with a
metric sequence and then call its `short_report()` or `long_report()` method.

## Models

The `models` package contains the core data structures and abstract base types
used throughout the project.

::: pymetrica.models

## Codebase Parser

The `codebase_parser` package exposes the main parser entrypoints and diagram
generation helpers.

::: pymetrica.codebase_parser

## Metric Calculators

The `metric_calculators` package re-exports the calculator classes and CLI
callables for the supported metrics. It also re-exports selected result types;
more detailed result and layer models live in each metric's submodule.

::: pymetrica.metric_calculators

## Report Generators

The report layer is small today. `REPORTS_MAPPING` is the registry used by the
CLI. It includes the normal terminal backend and the hook-oriented backend used
by the published pre-commit hooks. `BasicTerminalReport` is exported directly
from this package; the hook backend is available through the registry and its
submodule.

::: pymetrica.report_generators

### Utilities

The `utils` package exposes configuration loading, logging, and profiler
helpers.

::: pymetrica.utils
