# pymetrica

Pymetrica is a Python CLI tool for analyzing codebase metrics, including logical lines of code (LLOC), cyclomatic complexity, abstract lines of code (ALOC), Halstead volume, and maintainability index. It parses Python projects, computes metrics, and generates reports.

## Key Components

- **CLI Layer**: Entry point via `pymetrica.main:main`, with commands like `status`, `run_all`, `base_stats`, and metric-specific ones (e.g., cc, aloc).
- **File Parsing Layer**: `pymetrica.codebase_parser` parses directories into a Codebase model, counting files, LLOC, comments, classes, and functions.
- **Metrics Calculators**: Builder-pattern implementations in `pymetrica.metric_calculators`, including:
  - *Cyclomatic Complexity*: CCCalculator
  - *Halstead Volume*: HalsteadVolumeCalculator
  - *Maintainability Index*: MaintainabilityIndexCalculator
  - *Abstract Lines of Code*: AlocCalculator
  - *Report Generators*: Strategy-pattern implementations in `pymetrica.report_generators`, with a basic terminal report.
- **Models**: Pydantic-based classes in `pymetrica.models` for data structures like Metric and Results.
- **Utilities**: Helpers in `pymetrica.utils` for detecting logical lines and comments.

## Architecture Overview

Based on architecture_draft.md, the system follows a layered design:

```
CLI → Directory Reader → Metrics Calculator → Report Generator.
```

Metrics are computed per codebase and output via selectable strategies (e.g., terminal).

## Testing and Configuration

- Tests in tests, using Pytest with fixtures for sample codebases.
- Configured with pyproject.toml for dependencies, linting (Ruff, MyPy, Pylint), and scripts.
- Dev environment via .devcontainer for containerized setup.

For deeper dives, refer to specific files or run commands like pymetrica base-stats <dir\> to explore parsed data.
