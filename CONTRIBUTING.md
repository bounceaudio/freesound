# Contributing to freesound-python

Thank you for your interest in contributing to freesound-python!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/bounceaudio/freesound.git
cd freesound
```

2. Install in development mode:
```bash
pip install -e .
```

3. Run the tests:
```bash
python -m unittest test_freesound.py
```

4. Run the verification script:
```bash
python verify.py
```

## Running Examples

To run the examples, you'll need a Freesound API key:

1. Get an API key from: https://freesound.org/apiv2/apply/
2. Set it as an environment variable:
```bash
export FREESOUND_API_KEY="your_api_key_here"
```
3. Run the examples:
```bash
python examples.py
```

## Code Style

This project follows standard Python conventions:
- Use 4 spaces for indentation
- Follow PEP 8 guidelines
- Write clear, descriptive docstrings
- Keep lines under 120 characters when reasonable

## Testing

Before submitting a pull request:
1. Ensure all existing tests pass
2. Add tests for new functionality
3. Run the verification script to check basic functionality

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and verification
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Reporting Issues

When reporting issues, please include:
- A clear description of the problem
- Steps to reproduce
- Expected behavior
- Actual behavior
- Python version
- freesound-python version

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
