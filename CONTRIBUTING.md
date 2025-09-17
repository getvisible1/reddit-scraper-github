# Contributing to Reddit Scraper Pro

Thank you for your interest in contributing to Reddit Scraper Pro! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues
- Use the GitHub issue tracker to report bugs
- Include detailed information about the problem
- Provide steps to reproduce the issue
- Include your environment details (OS, Python version, etc.)

### Suggesting Features
- Open an issue with the "enhancement" label
- Describe the feature and its benefits
- Explain the use case and expected behavior

### Code Contributions

#### Development Setup
1. Fork the repository
2. Clone your fork locally
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pytest flake8 black
   ```

#### Making Changes
1. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Follow the coding standards (see below)
4. Test your changes thoroughly
5. Commit your changes with clear messages
6. Push to your fork and create a pull request

## 📝 Coding Standards

### Python Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Code Formatting
We use `black` for code formatting:
```bash
black src/
```

### Linting
We use `flake8` for linting:
```bash
flake8 src/
```

### Testing
- Write tests for new features
- Ensure existing tests pass
- Aim for good test coverage

Run tests with:
```bash
pytest
```

## 🏗️ Project Structure

```
reddit-scraper-pro/
├── src/
│   ├── main.py              # Flask application entry point
│   ├── routes/
│   │   ├── reddit.py        # Reddit scraping routes
│   │   └── user.py          # User management routes
│   └── static/
│       └── index.html       # Frontend application
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI/CD
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
└── README.md               # Project documentation
```

## 🔧 Development Guidelines

### Adding New Features
1. **Backend Changes**: Add new routes in the appropriate file under `src/routes/`
2. **Frontend Changes**: Update `src/static/index.html` for UI changes
3. **Dependencies**: Update `requirements.txt` if adding new packages
4. **Documentation**: Update README.md for significant changes

### API Design
- Follow RESTful principles
- Use appropriate HTTP status codes
- Return consistent JSON responses
- Include proper error handling

### Security Considerations
- Validate all user inputs
- Use secure defaults
- Avoid exposing sensitive information
- Follow OWASP guidelines

## 🧪 Testing Guidelines

### Test Categories
- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete user workflows

### Test Structure
```python
def test_function_name():
    # Arrange
    setup_test_data()
    
    # Act
    result = function_under_test()
    
    # Assert
    assert result == expected_value
```

### Mock External Services
- Mock Reddit API calls in tests
- Use fixtures for test data
- Avoid making real HTTP requests in tests

## 📋 Pull Request Process

### Before Submitting
1. Ensure your code follows the style guidelines
2. Run all tests and ensure they pass
3. Update documentation if needed
4. Rebase your branch on the latest main branch

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
```

### Review Process
1. Automated checks must pass (CI/CD pipeline)
2. At least one maintainer review required
3. Address review feedback promptly
4. Squash commits before merging

## 🚀 Release Process

### Versioning
We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Steps
1. Update version numbers
2. Update CHANGELOG.md
3. Create release tag
4. Build and publish Docker image
5. Deploy to production

## 🆘 Getting Help

### Communication Channels
- GitHub Issues: Bug reports and feature requests
- GitHub Discussions: General questions and ideas
- Email: For security-related issues

### Documentation
- README.md: Project overview and setup
- Code comments: Inline documentation
- Docstrings: Function and class documentation

## 📜 Code of Conduct

### Our Standards
- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain a professional environment

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or insulting comments
- Publishing private information
- Any form of abuse

### Enforcement
Violations may result in:
1. Warning
2. Temporary ban
3. Permanent ban

Report issues to the maintainers.

## 🙏 Recognition

Contributors will be:
- Listed in the README.md
- Mentioned in release notes
- Given credit for their contributions

Thank you for contributing to Reddit Scraper Pro! 🚀

