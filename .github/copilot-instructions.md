# GitHub Copilot Instructions for freesound

## Project Overview

This is a Python client library for the Freesound.org API (version 2). The project provides a simple and Pythonic interface for searching and retrieving audio samples from the Freesound database.

## Code Style and Conventions

### Python Version
- This project uses Python 3.14+ (`requires-python = ">=3.14"`)
- Always use modern Python features available in Python 3.14

### Code Quality Tools
- **Ruff**: For linting and code formatting
- **MyPy**: For static type checking
- **Pylint**: For additional code quality checks
- **Pytest**: For testing

### Type Hints
- Always include type hints for function parameters and return values
- Use modern typing syntax (e.g., `list[str]` instead of `List[str]`)
- Follow the type checking configuration in `mypy.ini`

### Code Style
- Use `ruff format` for code formatting
- Follow PEP 8 conventions
- Use dataclasses with `frozen=True` and `slots=True` for immutable data structures
- Keep functions focused and small

### Naming Conventions
- Use `snake_case` for variables, functions, and module names
- Use `PascalCase` for class names
- Use `UPPER_CASE` for constants
- Private attributes should start with underscore `_`

## Project Structure

### Key Files
- `client.py`: Main FreesoundClient class and API interaction logic
- `test_client.py`: Tests for the client
- `tasks.py`: Invoke tasks for building, testing, and linting
- `pyproject.toml`: Project configuration and dependencies

### Important Classes
- `FreesoundClient`: Main client for interacting with the Freesound API
- `Paginator`: Handles pagination of API results
- `Result`: Base dataclass for API results
- `TextSearchResult`: Dataclass for text search results

## Development Workflow

### Building and Testing
Run the full build process (linting, type checking, and tests):
```bash
uv run invoke build
```

### Individual Tasks
- Format code: `uv run ruff format .`
- Check formatting: `uv run invoke code-style`
- Run linters: `uv run invoke linters`
- Run type checker: `uv run invoke mypy`
- Run tests: `uv run invoke pytest`
- Run tests with coverage: `uv run invoke coverage`
- Run pylint: `uv run invoke pylint`
- Validate pyproject.toml: `uv run invoke validate-pyproject-toml`

### Dependencies
- Use `uv` for dependency management
- Dependencies are managed in `pyproject.toml`
- Lock file is `uv.lock`

## API Integration

### Authentication
- The client requires a `FREESOUND_APIV2_TOKEN` environment variable
- The token is used for authenticating API requests

### API Endpoints
- Base URL: `https://freesound.org/apiv2`
- Currently implemented: Text search endpoint (`/search/text`)

### Error Handling
- API responses expect status code 200
- Assertions are used to validate response status

## Testing Guidelines

- Tests are in `test_client.py`
- Use pytest fixtures for common setup
- Mock external API calls in tests
- Aim for high code coverage

## Best Practices

1. **Immutability**: Use `frozen=True` dataclasses for data objects
2. **Type Safety**: Always add type hints and run mypy
3. **Small Functions**: Keep functions focused on a single responsibility
4. **Documentation**: Add docstrings for public APIs
5. **Error Messages**: Make error messages clear and actionable
6. **Testing**: Write tests for new functionality
7. **Linting**: Run all linters before committing

## Common Patterns

### Dataclass Pattern
```python
@dataclass(frozen=True, slots=True)
class MyResult(Result):
    field1: str
    field2: int
    field3: list[str]
```

### API Request Pattern
```python
resp = requests.get(url, params={**params, "token": self._token})
assert resp.status_code == 200, resp.text
json_dict = resp.json()
```

### Generator Pattern
```python
def my_method(self) -> Iterable[MyResult]:
    yield from Paginator(...).paginate()
```

## When Making Changes

1. Understand the existing code patterns before adding new code
2. Run linters and type checkers frequently during development
3. Ensure all tests pass before finalizing changes
4. Follow the existing architecture and patterns in the codebase
5. Update this file if you make architectural changes that affect future development
