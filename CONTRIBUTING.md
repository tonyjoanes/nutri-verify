# Contributing to NutriVerify

First off, thank you for considering contributing to NutriVerify! It's people like you that make NutriVerify such a great tool.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
```bash
git clone https://github.com/yourusername/nutriverify.git
```

3. Create a branch for your changes:
```bash
git checkout -b feature/your-feature-name
```

4. Make your changes locally, following our development guidelines below

## Development Guidelines

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in the present tense (e.g., "Add feature" not "Added feature")
- Reference issue numbers if applicable
- Keep commits focused and atomic

Example:
```
Add paper analysis feature
- Implement PDF text extraction
- Add metadata parsing
- Create basic analysis pipeline
Fixes #42
```

### Code Style

#### C# Guidelines
- Follow Microsoft's C# coding conventions
- Use meaningful names for variables and methods
- Include XML documentation for public APIs
- Write unit tests for new features

#### Python Guidelines
- Follow PEP 8 style guide
- Use type hints where possible
- Include docstrings for functions and classes
- Write unit tests for new features

#### React Guidelines
- Use functional components and hooks
- Follow ESLint configuration
- Write component tests using React Testing Library
- Use Tailwind CSS for styling

### Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the documentation if you're changing functionality
3. Add tests for new features
4. Ensure the test suite passes
5. Make sure your code lints
6. Create a Pull Request with a clear title and description

#### Pull Request Title Format
```
feat: Add new feature
fix: Fix specific issue
docs: Update documentation
test: Add tests
refactor: Refactor code without changing functionality
```

### Running Tests

Before submitting a PR, make sure all tests pass:

```bash
# Backend tests
dotnet test

# Python tests
pytest

# Frontend tests
npm test
```

## Where to Start?

Look for issues labeled with:
- `good first issue`
- `help wanted`
- `documentation`

## Reporting Bugs

When reporting bugs, please include:

1. Your operating system name and version
2. Any relevant details about your local setup
3. Steps to reproduce the bug
4. Expected behavior
5. Actual behavior
6. Screenshots if applicable

## Suggesting Enhancements

Enhancement suggestions are welcome! Please include:

1. A clear description of the enhancement
2. The motivation for the change
3. Any alternatives you've considered
4. Additional context or screenshots

## License

By contributing, you agree that your contributions will be licensed under the MIT License.