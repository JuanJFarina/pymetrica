# Pymetrica

[![Tests Status](https://img.shields.io/github/actions/workflow/status/JuanJFarina/pymetrica/build.yml?branch=main)](https://github.com/JuanJFarina/pymetrica/actions)
[![PyPI version](https://img.shields.io/pypi/v/pymetrica)](https://pypi.org/project/pymetrica/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen)](https://github.com/pre-commit/pre-commit)
[![Dependabot](https://img.shields.io/badge/dependabot-enabled-brightgreen)](https://github.com/JuanJFarina/pymetrica/blob/main/.github/dependabot.yml)
[![Ruff](https://img.shields.io/badge/lint-ruff-ccff00)](https://github.com/astral-sh/ruff)
[![Pylint](https://img.shields.io/badge/lint-pylint-yellowgreen)](https://pylint.pycqa.org/)
[![Type Checked](https://img.shields.io/badge/type%20checked-mypy-blue)](http://mypy-lang.org/)

[![GitHub stars](https://img.shields.io/github/stars/JuanJFarina/pymetrica)](https://github.com/JuanJFarina/pymetrica/stargazers)
[![Downloads](https://img.shields.io/pypi/dm/pymetrica)](https://pypi.org/project/pymetrica/)
[![License](https://img.shields.io/github/license/JuanJFarina/pymetrica)](https://github.com/JuanJFarina/pymetrica/blob/main/LICENSE)

**Pymetrica** is a static analysis tool that computes **software engineering metrics for Python codebases**.

It parses Python source code using the **AST (Abstract Syntax Tree)** and
evaluates classical metrics used to assess **complexity, maintainability, and
architectural stability**.

The tool provides a modular architecture, a CLI interface, a reusable Python
API, and extensible reporting to help developers understand the structural
quality of their Python projects.

Repository:
[https://github.com/JuanJFarina/pymetrica](https://github.com/JuanJFarina/pymetrica)

---

# Example

Analyze a Python project:

```bash
pymetrica run-all path/to/project
```

By default, `run-all` emits a short CI-oriented report. Use `--long-report`
when you want descriptive summaries and per-layer breakdowns.

Example short report:

```
----------------------------------------------------------------------------------------------------
Short Report
----------------------------------------------------------------------------------------------------
Metric: Abstract Lines Of Code
aloc_number: 6
aloc_percentage: 15.0
----------------------------------------------------------------------------------------------------
Metric: Cyclomatic Complexity
cc_number: 23
lloc_per_cc: 1.7391304347826086
----------------------------------------------------------------------------------------------------
Metric: Halstead Volume
hv_number: 704.5342159112735
hv_per_lloc: 17.613355397781838
----------------------------------------------------------------------------------------------------
Metric: Maintainability Cost
maintainability_cost: 50.678396768622775
raw_line_cost: 50.638396768622776
----------------------------------------------------------------------------------------------------
Metric: Instability
root: 0.0
----------------------------------------------------------------------------------------------------
```

Pymetrica can also analyze **architecture layers and dependencies** within the codebase.

If you switch to a single-metric command such as `pymetrica cc path/to/project`,
Pymetrica always prints the descriptive report format instead of this short
layout.

---

# Contents

* Features
* Why Pymetrica
* Metrics
* Installation
* Quick Start
* CLI Commands
* Configuration and Hooks
* Architecture Overview
* Python API
* Architecture Diagram Generation
* Testing
* Contributing
* License

---

# Features

* Static analysis of Python projects using the AST
* Logical Lines of Code (LLOC) analysis
* Comment density statistics
* Layered architecture detection based on directories
* Multiple classical software engineering metrics
* CLI interface for fast inspection of codebases
* Optional Mermaid architecture diagrams
* Configurable thresholds and file exclusion patterns from `pyproject.toml`
* Published `pre-commit` hooks for automated metric checks
* Reusable Python API for parser, calculators, and report generation
* Extensible metric and reporting system

---

# Why Pymetrica?

Several tools compute Python complexity metrics (such as **radon**, **lizard**, or **SonarQube integrations**). Pymetrica focuses on a different goal: **architecture-aware metric analysis**.

Unlike many static analysis tools, Pymetrica:

* groups metrics by **codebase layers** derived from directory structure
* computes **cross-layer coupling and instability metrics**
* produces **architecture diagrams** alongside metric results
* provides a modular framework for implementing new metrics

This makes it useful not only for measuring complexity, but also for analyzing **architectural quality** in Python projects.

---

# Metrics

Pymetrica implements several classical software engineering metrics.

## Abstract Lines of Code (ALOC)

Measures the amount of **abstraction and indirection** in the codebase by counting abstract constructs such as definitions and structural components.

High ALOC ratios may indicate excessive abstraction or over-engineering.

---

## Cyclomatic Complexity (CC)

Measures the **number of independent execution paths** in a program.

Calculated by analyzing control flow structures including:

* conditionals
* loops
* exception handling
* boolean logic

Higher values correspond to more complex and harder-to-maintain code.

---

## Halstead Volume (HV)

Measures implementation complexity based on **operators and operands** used in the program.

Derived from:

* program vocabulary
* program length
* token frequency

---

## Maintainability Cost (MC)

A composite metric derived from:

* Cyclomatic Complexity
* Halstead Volume
* Logical Lines of Code

It estimates the **expected maintenance effort** required for the codebase.

Lower scores indicate better maintainability.

---

## Instability (LI)

Measures **package coupling and architectural stability** based on import dependencies.

Instability is defined as:

```
Instability = Efferent Coupling / (Afferent Coupling + Efferent Coupling)
```

Values range from:

* **0 → Stable**
* **1 → Unstable**

---

# Installation

Requires **Python 3.10 or newer**.

Install the latest published package from PyPI:

```bash
pip install pymetrica
```

Or install from source:

```bash
git clone https://github.com/JuanJFarina/pymetrica
cd pymetrica
pip install -e .
```

After installation the CLI command becomes available:

```
pymetrica
```

---

# Quick Start

Analyze a Python project:

```bash
pymetrica run-all path/to/project
```

Configured `[tool.pymetrica].exclude` patterns are applied before the codebase
is parsed.

For an initial overview of a codebase:

```bash
pymetrica base-stats path/to/project
```

To focus on one metric, run its dedicated command:

```bash
pymetrica cc path/to/project
```

Single-metric commands always use the descriptive report format.

---

# CLI Commands

```
pymetrica status
pymetrica base-stats
pymetrica aloc
pymetrica cc
pymetrica hv
pymetrica mc
pymetrica li
pymetrica run-all
```

Typical usage pattern:

```
pymetrica <command> DIR_PATH
```

Notes:

* `run-all` supports `--long-report` for descriptive summaries and per-layer detail
* `aloc`, `cc`, `hv`, `mc`, and `li` always emit the descriptive report format
* all parsing commands honor `[tool.pymetrica].exclude` patterns

---

# Configuration and Hooks

Pymetrica reads optional thresholds and exclusion patterns from
`[tool.pymetrica]` in `pyproject.toml`:

```toml
[tool.pymetrica]
aloc_fail_threshold = 30
cc_fail_threshold = 10
hv_fail_threshold = 30
mc_fail_threshold = 25
exclude = ["generated/*", "vendor/*"]
```

Thresholds default to `0`, which disables failure gating for that metric.
`exclude` defaults to an empty list.

Important details:

* exclusions are matched against paths relative to the resolved analysis root
* matching uses Python's `fnmatch`
* the same settings apply to `run-all`, `base-stats`, and the single-metric commands

Pymetrica also publishes `pre-commit` hooks:

```yaml
repos:
  - repo: https://github.com/JuanJFarina/pymetrica
    rev: v1.2.0
    hooks:
      - id: pymetrica
      - id: pymetrica-mc
```

Available hook IDs today:

* `pymetrica`
* `pymetrica-aloc`
* `pymetrica-cc`
* `pymetrica-hv`
* `pymetrica-mc`

---

# Architecture Overview

Pymetrica is built around a modular analysis pipeline.

```
Codebase Parsing
        ↓
Code Representation
        ↓
Metric Calculators
        ↓
Results
        ↓
Report Generators
```

Core components include:

### Parser

Recursively scans `.py` files and builds a structured representation of the codebase.

Extracted information includes:

* logical lines of code
* comment lines
* classes and functions
* directory structure

Files containing syntax errors are automatically skipped.

---

### Data Models

Core data structures are implemented using **Pydantic** models.

Main models include:

* `Code` – representation of a Python file
* `Codebase` – full project structure
* `Metric` – container for metric metadata and results
* `Results` – structured metric outputs

---

### Metric Calculators

Each metric is implemented as a subclass of an abstract `MetricCalculator`.

This design makes it easy to extend the system with additional metrics.

---

### Reporting

Metrics are rendered through pluggable report generators.

Currently supported:

* `BASIC_TERMINAL` short terminal summaries
* `BASIC_TERMINAL` detailed metric reports

Future formats may include JSON, Markdown, or CI-friendly outputs.

---

# Python API

The CLI and the Python API share the same parser, calculators, and report
registry. A typical programmatic workflow is:

```python
from pymetrica.codebase_parser import create_diagram, parse_codebase
from pymetrica.metric_calculators import AlocCalculator, CCCalculator
from pymetrica.report_generators import REPORTS_MAPPING

codebase = parse_codebase("path/to/project")

metrics = [
    AlocCalculator().calculate_metric(codebase),
    CCCalculator().calculate_metric(codebase),
]

report = REPORTS_MAPPING["BASIC_TERMINAL"]().generate_report(metrics)
print(report)

create_diagram(codebase, filename="architecture.mmd")
```

`parse_codebase()` uses the same exclusion rules as the CLI, so configured
`[tool.pymetrica].exclude` patterns still apply.

---

# Architecture Diagram Generation

Pymetrica can generate **Mermaid diagrams** representing the layered architecture of a codebase.

```
pymetrica base-stats --diagram path/to/project
```

This creates a `.mmd` file that can be rendered using:

* Mermaid Live Editor
* VSCode Mermaid extensions
* documentation pipelines

---

# Testing

Tests are implemented using **pytest** and mirror the project structure.

Run tests with:

```
pytest
```

---

# Contributing

Contributions are welcome.

If you want to:

* implement a new metric
* improve the parser
* extend reporting capabilities

feel free to open an issue or submit a pull request.

---

# License

MIT License.
