# Contributing to Marlin Configurator

Thank you for your interest in contributing to Marlin Configurator! We welcome all contributions, including bug reports, feature requests, documentation improvements, and code contributions.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Making Changes](#making-changes)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)
- [Code Style and Guidelines](#code-style-and-guidelines)
- [Documentation](#documentation)
- [Testing](#testing)
- [Translations](#translations)
- [License](#license)

## Code of Conduct

By participating in this project, you are expected to uphold our [Code of Conduct](CODE_OF_CONDUCT.md). Please report any unacceptable behavior to nsfr750@yandex.com.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/marlin-configurator.git
   cd marlin-configurator
   ```
3. Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Environment

### Prerequisites

- Python 3.8 or higher
- Git
- pip (Python package manager)

### Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

## Making Changes

1. Make your changes following the code style guidelines
2. Add or update tests as needed
3. Update documentation if necessary
4. Run tests and ensure everything passes

## Pull Request Process

1. Ensure your fork is up to date with the main repository
2. Rebase your changes on top of the main branch
3. Submit a pull request with a clear title and description
4. Reference any related issues in your PR description
5. Ensure all CI checks pass
6. Address any code review feedback

## Reporting Issues

When reporting issues, please include:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Screenshots if applicable
- Your system information (OS, Python version, etc.)

## Feature Requests

For feature requests, please:

1. Check if a similar feature request already exists
2. Describe the feature and why it would be useful
3. Include any relevant examples or mockups

## Code Style and Guidelines

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints for all function signatures
- Write docstrings for all public functions and classes
- Keep lines under 88 characters (Black's default)
- Use `snake_case` for variables and functions
- Use `PascalCase` for class names
- Use `UPPER_CASE` for constants
- Format code with Black before committing

## Documentation

- Update relevant documentation when making changes
- Follow Google-style docstrings
- Keep documentation in the `docs` directory up to date
- Update `CHANGELOG.md` for significant changes

## Testing

- Write tests for new features and bug fixes
- Run tests before submitting a PR:
  ```bash
  pytest tests/
  ```
- Ensure test coverage remains high

## Translations

1. Add new strings to both `lang/en.json` and `lang/it.json`
2. Keep translations in sync
3. Use the `tr()` function for all user-facing strings
4. Test UI with different languages

## License

By contributing to this project, you agree that your contributions will be licensed under the GPL-3.0 License.

## Getting Help

If you need help or have questions, please:
- Open an issue on GitHub
- Join our [Discord server](https://discord.gg/BvvkUEP9)
- Email nsfr750@yandex.com

---

Thank you for contributing to Marlin Configurator! Your help is greatly appreciated.
