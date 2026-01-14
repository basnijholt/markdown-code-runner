---
icon: lucide/git-pull-request
---

# Contributing

<!-- CODE:START -->
<!-- from docs_gen import readme_section -->
<!-- print(readme_section("contributing")) -->
<!-- CODE:END -->
<!-- OUTPUT:START -->
<!-- PLACEHOLDER --> Output is generated during CI build. We don't commit generated content to keep docs copyable and avoid recursion. See docs/docs_gen.py
<!-- OUTPUT:END -->

## Development Setup

1. Clone the repository:

```bash
git clone https://github.com/basnijholt/markdown-code-runner.git
cd markdown-code-runner
```

2. Create a virtual environment and install dependencies:

```bash
# Using uv (recommended)
uv sync

# Or using pip
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[test]"
```

3. Run the tests:

```bash
pytest
```

4. Run pre-commit hooks:

```bash
pre-commit run --all-files
```

## Code Style

This project uses:

- **Ruff** for linting and formatting
- **MyPy** for type checking
- **pytest** for testing with 100% code coverage requirement

## Pull Request Process

1. Create a new branch for your changes
2. Make your changes and add tests
3. Ensure all tests pass: `pytest`
4. Ensure pre-commit passes: `pre-commit run --all-files`
5. Submit a pull request with a clear description

## Reporting Issues

Please report issues on the [GitHub issue tracker](https://github.com/basnijholt/markdown-code-runner/issues).

Include:

- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your Python version and OS
