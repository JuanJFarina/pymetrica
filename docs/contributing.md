# Contributing

Pymetrica welcomes contributions to the parser, metrics, reports, tests, and
documentation.

## Local Setup

```bash
git clone https://github.com/JuanJFarina/pymetrica.git
cd pymetrica
pip install -e .
pip install -r docs/requirements.txt
pip install pytest pre-commit
```

## Run Checks

The repository already uses `pytest` and `pre-commit`.

```bash
pytest
pre-commit run --all-files
```

If you are working on the docs site, you can preview it locally with:

```bash
mkdocs serve
```

If you are changing hook behavior, you can exercise the published local hook
definitions directly:

```bash
pre-commit try-repo . pymetrica --all-files
pre-commit try-repo . pymetrica-mc --all-files
```

## Good Contribution Targets

- improve metric explanations and examples
- add new metric calculators
- extend report generators
- improve parsing and architecture analysis
- expand test coverage around edge cases

The repository root `TODO.md` tracks known follow-ups such as `.gitignore`
handling, excluded-layer behavior, and maintainability-cost layer consistency.
Check it before starting cleanup or parser work so docs, code, and roadmap
stay aligned.

## Pull Requests

When opening a pull request:

- describe the motivation for the change
- include any relevant CLI or output examples
- mention documentation updates when behavior changes

For bug reports or feature ideas, open an issue in the
[GitHub repository](https://github.com/JuanJFarina/pymetrica).
