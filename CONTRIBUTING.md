# Contributing to MLL Lab Claude Code Plugin Marketplace

Thank you for your interest in contributing to the MLL Lab Claude Code Plugin Marketplace! This document provides guidelines for adding new plugins to the marketplace.

## 🎯 Overview

This marketplace provides a centralized catalog for Claude Code plugins used within MLL Lab. Each plugin can contain commands, agents, or other Claude Code extensions.

## 📋 Prerequisites

Before contributing, ensure you have:
- Access to the MLL Lab GitHub organization
- Familiarity with [Claude Code plugins](https://docs.claude.com/en/docs/claude-code/plugins)
- Basic Git and GitHub workflow knowledge

## 🚀 Adding a New Plugin

### Step 1: Create Your Plugin

1. **Create a plugin directory** under `plugins/`:
   ```bash
   mkdir -p plugins/my-plugin
   ```

2. **Add your plugin files**:
   - `README.md` - Documentation for your plugin
   - `plugin.md` - Your plugin implementation (commands, agents, etc.)
   - Any additional files needed by your plugin

### Step 2: Document Your Plugin

Create a `README.md` in your plugin directory with:

```markdown
# Plugin Name

Brief description of what your plugin does.

## Installation

\`\`\`bash
/plugin install my-plugin@mll-lab-marketplace
\`\`\`

## Usage

Describe how to use your plugin with examples.

## Features

- Feature 1
- Feature 2

## Author

- **Name**: Your Name
- **Email**: your.email@mll.com
```

### Step 3: Register Your Plugin

Update `.claude-plugin/marketplace.json` to include your plugin:

```json
{
  "name": "my-plugin",
  "description": "Brief description of your plugin",
  "version": "1.0.0",
  "author": {
    "name": "Your Name",
    "email": "your.email@mll.com"
  },
  "source": "./plugins/my-plugin",
  "category": "productivity",
  "keywords": ["keyword1", "keyword2", "keyword3"]
}
```

#### Available Categories:
- `productivity` - Tools to enhance productivity
- `development` - Development-related tools
- `testing` - Testing and QA tools
- `documentation` - Documentation generators
- `code-review` - Code review and quality tools
- `workflow` - Workflow automation
- `agents` - AI agents with specialized capabilities
- `general` - General purpose tools

### Step 4: Test Your Plugin

1. **Validate the JSON**:
   ```bash
   cat .claude-plugin/marketplace.json | python3 -m json.tool
   ```

2. **Test locally** (if possible):
   ```bash
   /plugin marketplace add mll-lab/claude-plugin-marketplace
   /plugin install my-plugin@mll-lab-marketplace
   ```

### Step 5: Submit Your Changes

1. **Fork the repository** (if you haven't already)

2. **Create a feature branch**:
   ```bash
   git checkout -b add-my-plugin
   ```

3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add my-plugin to marketplace"
   ```

4. **Push to your fork**:
   ```bash
   git push origin add-my-plugin
   ```

5. **Create a Pull Request** on GitHub with:
   - A clear title describing your plugin
   - Description of what your plugin does
   - Any special installation or usage notes

## 📝 Plugin Metadata Guidelines

### Required Fields:
- `name` - Unique identifier (lowercase, hyphens only)
- `description` - Clear, concise description
- `version` - Semantic version (e.g., "1.0.0")
- `author` - Your name and email
- `source` - Path to your plugin directory

### Optional Fields:
- `category` - Plugin category (see list above)
- `keywords` - Array of searchable keywords
- `homepage` - URL to documentation or repository
- `tags` - Additional tags for filtering

## ✅ Best Practices

1. **Clear Documentation**: Provide comprehensive usage examples
2. **Version Control**: Use semantic versioning for updates
3. **Testing**: Test your plugin before submitting
4. **Minimal Dependencies**: Keep plugins lightweight
5. **Error Handling**: Include proper error messages
6. **Examples**: Provide real-world usage examples

## 🔄 Updating an Existing Plugin

To update an existing plugin:

1. Increment the version number in `marketplace.json`
2. Update the plugin files as needed
3. Document changes in your plugin's README
4. Submit a pull request with a clear description of changes

## 🐛 Reporting Issues

If you encounter issues with:
- The marketplace itself: Open an issue in this repository
- A specific plugin: Contact the plugin author or open an issue

## 📚 Resources

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [Plugin Development Guide](https://docs.claude.com/en/docs/claude-code/plugins)
- [Plugin Marketplace Docs](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)

## 📧 Contact

For questions or support, reach out to the MLL Lab development team.

---

Thank you for contributing to the MLL Lab Claude Code Plugin Marketplace! 🎉
