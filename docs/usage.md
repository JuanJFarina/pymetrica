# Usage

## Installation

To use Pymetrica, first install it using pip:

```console
$ pip install pymetrica
```

Or install from source:

```console
$ git clone https://github.com/JuanJFarina/pymetrica.git
$ cd pymetrica
$ pip install .
```

## Quick Start

Analyze a Python project to get software engineering metrics:

```console
$ pymetrica run-all path/to/your/project
```

### Example Output

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

## Available Metrics

Pymetrica computes the following software engineering metrics:

- **Abstract Lines Of Code (ALOC)**: Measures the number of non-comment, non-blank lines in the codebase
- **Cyclomatic Complexity (CC)**: Measures code complexity based on the number of decision points
- **Halstead Volume (HV)**: Measures program effort and complexity based on operator and operand count
- **Maintainability Index (MI)**: Combines multiple metrics to produce a single index of maintainability
- **Instability (I)**: Measures the likelihood of a module needing modification when other modules change

## Architecture

Pymetrica uses a modular architecture:

- **Codebase Parser**: Parses Python source code using AST (Abstract Syntax Tree)
- **Metric Calculators**: Individual calculators for each metric
- **Report Generators**: Extensible reporting to visualize results
- **Models**: Core data structures representing code and metrics

## Advanced Usage

For more detailed analysis capabilities and custom reports, see the API Reference.
