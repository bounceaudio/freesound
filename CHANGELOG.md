# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-09

### Added
- Initial release of freesound-python package
- FreesoundClient class for API interaction
- Support for text search, content-based search, and combined search
- Sound, User, and Pack information retrieval
- Sound analysis and similar sounds functionality
- Download support for sound previews and full-quality files
- Token-based and OAuth2 authentication
- Automatic JSON to Python object conversion
- Access to raw JSON data via `.as_dict()` method
- Customizable HTTP session support
- Comprehensive documentation and examples
- Unit tests for core functionality
- Package verification script
- GitHub Actions CI/CD workflow

### Features
- Search sounds using text queries with filters
- Content-based search using audio descriptors
- Combined text and content-based searches
- Retrieve detailed sound information
- Get sound analysis data
- Find similar sounds
- Download sound previews (no authentication required)
- Download full-quality sounds (OAuth2 required)
- Get user profiles and sounds
- Get pack information and contents
- Iterate through paginated results
- Custom request session configuration
- Proxy support
- Rate limiting support

[1.0.0]: https://github.com/bounceaudio/freesound/releases/tag/v1.0.0
