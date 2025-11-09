# freesound

Python client for the freesound.org API

## Installation

Install the package using pip:

```bash
pip install freesound
```

Or using uv:

```bash
uv add freesound
```

## Development

This project uses [uv](https://github.com/astral-sh/uv) for dependency management and packaging.

### Setup

1. Install uv:
   ```bash
   pip install uv
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

### Building

Build the package:

```bash
uv build
```

This will create distribution files in the `dist/` directory.

## Publishing

This project uses GitHub Actions to automatically publish to PyPI. The workflow is triggered on:

1. **Release**: When a new release is published on GitHub, the package is automatically published to PyPI.
2. **Manual**: You can manually trigger the workflow from the Actions tab and choose to publish to either PyPI or TestPyPI.

### Setup for Publishing

To enable automatic publishing to PyPI:

1. Set up [PyPI trusted publishing](https://docs.pypi.org/trusted-publishers/):
   - Go to your PyPI project settings
   - Add a GitHub Actions publisher with:
     - Owner: `bounceaudio`
     - Repository: `freesound`
     - Workflow: `publish-pypi.yml`
     - Environment: `pypi`

2. (Optional) Set up TestPyPI trusted publishing for testing:
   - Go to your TestPyPI project settings
   - Add a GitHub Actions publisher with the same settings but environment: `testpypi`

## License

MIT License - see [LICENSE](LICENSE) file for details.

