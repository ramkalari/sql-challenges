# Contributing to SQL Challenges

Thank you for your interest in contributing to the SQL Challenges project! This document provides guidelines for contributing to this project.

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 18+
- Git

### Setting Up the Development Environment

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/your-username/sql-challenges.git
   cd sql-challenges
   ```

2. **Set Up Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set Up Frontend**
   ```bash
   cd frontend
   npm install
   ```

4. **Start Development Servers**
   ```bash
   # Terminal 1 - Backend
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   
   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

## Development Workflow

### 1. Create a Feature Branch

Always create a new branch for your changes:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

- Follow the existing code style
- Write tests for new functionality
- Update documentation as needed

### 3. Testing

Run tests before submitting your changes:

```bash
# Backend tests
cd backend
python -m pytest test_main.py -v

# Frontend tests
cd frontend
npm test
```

### 4. Commit Your Changes

Use conventional commit messages:

```bash
git commit -m "feat: add new SQL challenge for joins"
git commit -m "fix: resolve authentication token issue"
git commit -m "docs: update README with new features"
```

### 5. Push and Create a Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Code Style Guidelines

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions small and focused

### TypeScript/JavaScript (Frontend)

- Use TypeScript for type safety
- Follow ESLint configuration
- Use functional components with hooks
- Keep components small and reusable

### General Guidelines

- Write clear, descriptive commit messages
- Add comments for complex logic
- Use meaningful variable and function names
- Keep functions and methods under 50 lines when possible

## Adding New Features

### Adding SQL Challenges

1. Edit `backend/challenges.py`
2. Add new challenge objects to the `CHALLENGES` list
3. Include:
   - Clear description
   - Schema SQL
   - Seed data
   - Expected output
   - Difficulty level

### Adding UI Components

1. Create components in `frontend/src/app/`
2. Add corresponding tests in `frontend/src/app/__tests__/`
3. Update styles using Tailwind CSS

## Testing Guidelines

### Backend Testing

- Test all API endpoints
- Test authentication flows
- Test database operations
- Test error handling

### Frontend Testing

- Test component rendering
- Test user interactions
- Test API integration
- Test responsive design

## Pull Request Guidelines

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation is updated
- [ ] No console errors
- [ ] Responsive design works

### Pull Request Template

Use this template when creating a pull request:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Backend tests pass
- [ ] Frontend tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where necessary
- [ ] I have made corresponding changes to documentation
```

## Reporting Issues

When reporting issues, please include:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Browser/OS information (for frontend issues)
- Error messages or logs

## Getting Help

- Check existing issues and pull requests
- Ask questions in GitHub discussions
- Review the documentation in README.md

## Code of Conduct

- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow the project's coding standards

Thank you for contributing to SQL Challenges! 