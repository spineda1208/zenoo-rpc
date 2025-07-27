# Changelog

All notable changes to Zenoo RPC will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- TBD for next release

### Changed
- TBD for next release

### Fixed
- TBD for next release

## [0.1.0] - 2025-07-28

### Added
- Initial development release of Zenoo RPC
- Basic async Python library for Odoo RPC communication
- Core ZenooClient with authentication and basic operations
- Pydantic models for type-safe Odoo record handling
- Basic query builder with filtering capabilities
- Simple caching system with memory backend
- Basic batch operations for create/update/delete
- Simple retry mechanisms with exponential backoff
- Basic transaction support
- HTTP connection with timeout handling
- Custom exception hierarchy for error handling
- Model registry for dynamic model discovery
- Basic field types (CharField, IntegerField, etc.)
- Simple cache strategies (TTL, LRU)
- Core batch operation implementations
- Basic retry strategies and policies
- Simple transaction context management

### Documentation
- Comprehensive documentation suite (42 files)
- Complete API reference with examples
- User guide and tutorials
- Advanced topics (architecture, performance, security)
- Troubleshooting guide and FAQ
- Contributing guidelines
- Project governance files (CODE_OF_CONDUCT, SECURITY)
- GitHub issue and PR templates

### Core Features

#### ZenooClient
- Async-first design with modern Python patterns
- JSON-RPC communication with Odoo servers
- Session-based authentication
- Basic connection management
- SSL/TLS support
- Configurable timeouts

#### Model System
- `OdooModel` base class with Pydantic integration
- Basic field types for common Odoo fields
- Simple relationship field support
- Model registry for type discovery
- Data validation and serialization

#### Query Builder
- Fluent API for building Odoo domain queries
- Basic filtering with common operators
- Pagination support (limit/offset)
- Field selection capabilities
- Simple relationship handling

#### Caching System
- Basic memory-based caching
- TTL and LRU eviction strategies
- Simple cache invalidation
- Cache statistics tracking

#### Batch Operations
- Basic bulk create, update, delete operations
- Simple chunking for large datasets
- Basic error handling and progress tracking

#### Retry Mechanisms
- Basic exponential backoff strategy
- Simple retry policies
- Configurable retry attempts and delays

#### Transaction Management
- Basic transaction support
- Simple context managers
- Automatic rollback on errors

#### Error Handling
- Custom exception hierarchy
- Basic error categorization
- Network and authentication error handling
- Simple validation error reporting

### Development Status
- **Alpha Release**: Core functionality implemented
- **API Stability**: API may change in future versions
- **Testing**: Basic test coverage, more tests needed
- **Documentation**: Comprehensive documentation complete
- **Performance**: Basic optimizations, more improvements planned

### Compatibility
- Python 3.8+ support
- Odoo 18.0 compatibility (tested)
- Other Odoo versions (12.0-17.0) not yet tested
- Async/await native support
- Type hints for IDE support
- Pydantic v2 integration

### Documentation
- Complete documentation suite (42 files)
- API reference with examples
- User guides and tutorials
- Advanced topics and best practices
- Troubleshooting and FAQ
- Contributing guidelines

### Testing
- Basic test structure in place
- Unit tests for core components
- Integration test framework ready
- More comprehensive testing planned for future releases

### Known Limitations
- Only tested with Odoo 18.0 (other versions compatibility unknown)
- Redis cache backend not yet implemented
- Advanced retry policies need more testing
- Performance optimizations planned for future releases
- Some edge cases in error handling need refinement
- Integration tests with Odoo 12.0-17.0 needed

### Roadmap for v0.2.0
- Odoo version compatibility testing (12.0-17.0)
- Redis cache backend implementation
- Enhanced retry mechanisms with circuit breakers
- Performance optimizations and benchmarks
- Comprehensive integration testing
- API stability improvements
- Advanced query features

### Roadmap for v1.0.0
- Production-ready stability
- Full test coverage (95%+)
- Performance benchmarks and optimizations
- Complete Odoo version compatibility testing
- API freeze and backward compatibility guarantees
- Production deployment guides

---

## Release Notes

### Version 0.1.0 - Initial Development Release

This is the first development release of Zenoo RPC, providing a foundation for modern, async-first Python integration with Odoo.

**Key Highlights:**
- **Async-First**: Built from ground up for async/await patterns
- **Type Safety**: Pydantic models with full type hints
- **Developer Experience**: Fluent API design with IDE support
- **Comprehensive Documentation**: 42 files covering all aspects
- **Modern Architecture**: Clean, extensible design patterns

**Development Status:**
This is an alpha release intended for:
- Early adopters and contributors
- Feedback collection and API refinement
- Testing with various Odoo configurations
- Community building and collaboration

**Not Recommended For:**
- Production use (wait for v1.0.0)
- Mission-critical applications
- Large-scale deployments

**Getting Started:**
See our [Getting Started Guide](docs/getting-started/installation.md) for installation and basic usage.

**Documentation:**
Comprehensive documentation is available in the `docs/` directory:
- API Reference: Complete method documentation
- User Guide: Step-by-step usage instructions
- Tutorials: Practical examples and patterns
- Advanced Topics: Architecture, performance, security
- Contributing: Guidelines for contributors

**Community:**
We welcome contributions and feedback:
- GitHub Issues: [Report bugs and request features](https://github.com/tuanle96/zenoo-rpc/issues)
- Discussions: Share ideas and ask questions
- Pull Requests: Contribute code and documentation

**Contributors:**
- @tuanle96 - Project creator and maintainer

**Next Steps:**
Planned for upcoming releases:
- v0.2.0: Redis backend, enhanced retries, performance optimizations
- v0.3.0: Advanced query features, comprehensive testing
- v1.0.0: Production-ready stability, performance benchmarks

---

## Changelog Guidelines

This changelog follows the [Keep a Changelog](https://keepachangelog.com/) format:

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes

Versions follow [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

## Links

- [GitHub Repository](https://github.com/tuanle96/zenoo-rpc)
- [Documentation](https://zenoo-rpc.readthedocs.io/)
- [PyPI Package](https://pypi.org/project/zenoo-rpc/)
- [Issue Tracker](https://github.com/tuanle96/zenoo-rpc/issues)
- [Discussions](https://github.com/tuanle96/zenoo-rpc/discussions)