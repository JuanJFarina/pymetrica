# Pymetrica

[![Tests Status](https://img.shields.io/github/actions/workflow/status/JuanJFarina/pymetrica/build.yml?branch=main)](https://github.com/JuanJFarina/pymetrica/actions)
[![PyPI version](https://img.shields.io/pypi/v/pymetrica)](https://pypi.org/project/pymetrica/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/badge/lint-ruff-ccff00)](https://github.com/astral-sh/ruff)
[![Pylint](https://img.shields.io/badge/lint-pylint-yellowgreen)](https://pylint.pycqa.org/)
[![Type Checked](https://img.shields.io/badge/type%20checked-mypy-blue)](http://mypy-lang.org/)

[![GitHub stars](https://img.shields.io/github/stars/JuanJFarina/pymetrica)](https://github.com/JuanJFarina/pymetrica/stargazers)
[![Downloads](https://img.shields.io/pypi/dm/pymetrica)](https://pypi.org/project/pymetrica/)
[![License](https://img.shields.io/github/license/JuanJFarina/pymetrica)](https://github.com/JuanJFarina/pymetrica/blob/main/LICENSE)

**Pymetrica** is a static analysis tool that computes **software engineering metrics for Python codebases**.

It parses Python source code using the **AST (Abstract Syntax Tree)** and evaluates classical metrics used to assess **complexity, maintainability, and architectural stability**.

The tool provides a modular architecture, a CLI interface, and extensible reporting to help developers understand the structural quality of their Python projects.

Repository:
[https://github.com/JuanJFarina/pymetrica](https://github.com/JuanJFarina/pymetrica)

---

# Example

Analyze a Python project:

```bash
pymetrica run-all path/to/project
```

Example output:

```
Metric: Abstract Lines Of Code
aloc_number: 67
aloc_percentage: 14.89

Metric: Cyclomatic Complexity
cc_number: 156
lloc_per_cc: 2.89

Metric: Halstead Volume
hv_number: 5423.67

Metric: Maintainability Cost
maintainability_cost: 24.67
```

Pymetrica can also analyze **architecture layers and dependencies** within the codebase.

---

# Contents

* Features
* Why Pymetrica
* Metrics
* Installation
* Quick Start
* CLI Commands
* Architecture Overview
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

Install from source:

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

For an initial overview of a codebase:

```bash
pymetrica base-stats path/to/project
```

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

* terminal summaries
* detailed reports

Future formats may include JSON, Markdown, or CI-friendly outputs.

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
