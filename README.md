# pymetrica

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Pymetrica is a comprehensive Python CLI tool for analyzing codebase metrics. It parses Python projects and computes various software quality metrics including logical lines of code (LLOC), cyclomatic complexity, abstract lines of code (ALOC), Halstead volume, maintainability index, and instability metrics.

## Features

- **Multiple Metrics**: Calculate LLOC, cyclomatic complexity, ALOC, Halstead volume, maintainability index, and instability
- **Architecture Diagrams**: Generate Mermaid diagrams of codebase structure and dependencies
- **CLI Interface**: Easy-to-use command-line interface with multiple commands
- **Extensible Architecture**: Built with builder and strategy patterns for easy extension
- **Comprehensive Parsing**: Parses Python codebases, counting files, classes, functions, comments, and more
- **Report Generation**: Multiple report formats (currently supports basic terminal output)
- **Type-Safe**: Full type annotations and Pydantic models

## Installation

### From Source

```bash
git clone https://github.com/yourusername/pymetrica.git
cd pymetrica
pip install .
```

### Development Setup

```bash
pip install pipenv
pipenv install --dev
pipenv shell
```

## Usage

### Basic Commands

```bash
# Check tool status
pymetrica status

# Parse and display basic codebase statistics
pymetrica base-stats /path/to/your/python/project

# Parse codebase statistics and generate architecture diagram
pymetrica base-stats /path/to/your/python/project --diagram

# Run all metrics on a codebase
pymetrica run-all /path/to/your/python/project
```

### Individual Metrics

```bash
# Cyclomatic complexity
pymetrica cc /path/to/your/python/project

# Abstract lines of code
pymetrica aloc /path/to/your/python/project

# Halstead volume
pymetrica halstead-volume /path/to/your/python/project

# Maintainability index
pymetrica maintainability-index /path/to/your/python/project

# Instability
pymetrica instability /path/to/your/python/project
```

### Report Types

Currently supports basic terminal output. Use the `--report-type` option:

```bash
pymetrica cc /path/to/project --report-type BASIC_TERMINAL
```

## Metrics Explained

### Logical Lines of Code (LLOC)
Counts the number of logical lines of code, excluding comments and blank lines.

### Cyclomatic Complexity
Measures the complexity of code by counting the number of linearly independent paths through a program's source code.

### Abstract Lines of Code (ALOC)
Represents the number of lines that would be left if all comments, blank lines, and unnecessary code were removed.

### Halstead Volume
A software metric introduced by Maurice Howard Halstead. It measures the size of a program based on the number of operators and operands.

### Maintainability Index
A software metric that measures how maintainable (easy to support and change) the source code is.

### Instability
Measures how stable a module is based on its dependencies (afferent and efferent couplings).

## Architecture Diagrams

Pymetrica can generate visual architecture diagrams of your Python codebase using Mermaid.js format. The diagrams show:

- **Layer Structure**: Directory-based layers and their components
- **Dependencies**: Import relationships between different parts of the codebase
- **Component Organization**: How files are organized within layers

To generate a diagram, use the `--diagram` flag with the `base-stats` command:

```bash
pymetrica base-stats --diagram /path/to/project
```

This creates a `.mmd` (Mermaid) file that can be viewed in any Mermaid-compatible viewer or converted to other formats like PNG, SVG, or PDF.

## Architecture

Pymetrica follows a clean, layered architecture:

```
CLI Layer → File Parsing Layer → Metrics Calculator Layer → Report Generator Layer
```

### Key Components

- **CLI Layer**: Entry point via `pymetrica.main:main`, with commands for different operations
- **File Parsing Layer**: `pymetrica.codebase_parser` parses directories into a Codebase model
- **Metrics Calculators**: Builder-pattern implementations in `pymetrica.metric_calculators`
- **Report Generators**: Strategy-pattern implementations in `pymetrica.report_generators`
- **Models**: Pydantic-based classes in `pymetrica.models` for data structures
- **Utilities**: Helpers in `pymetrica.utils` for detecting logical lines and comments

## Development

### Running Tests

```bash
pipenv run test
```

### Linting and Formatting

```bash
pipenv run lint
```

### Installing Pre-commit Hooks

```bash
pipenv run install_hooks
```

## Project Structure

```
pymetrica/
├── __init__.py
├── __main__.py
├── codebase_parser/
│   ├── __init__.py
│   ├── base_stats.py
│   ├── codebase_parser.py
│   ├── diagram_generator.py
│   └── logical_lines_of_code/
├── metric_calculators/
│   ├── __init__.py
│   ├── abstract_lines_of_code/
│   ├── cyclomatic_complexity/
│   ├── halstead_volume/
│   ├── maintainability_index/
│   └── instability/
├── models/
│   ├── __init__.py
│   ├── code.py
│   ├── codebase.py
│   ├── metric.py
│   ├── metric_calculator.py
│   └── report_generator.py
├── report_generators/
│   ├── __init__.py
│   ├── basic_terminal_report.py
│   └── reports_mapping.py
├── utils/
│   ├── __init__.py
│   ├── is_comment.py
│   └── is_lloc.py
└── run_all.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Juan José Farina - [juanjosefarina.jjf@gmail.com](mailto:juanjosefarina.jjf@gmail.com)
