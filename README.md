# MLL Claude Code Plugin Marketplace

Catalog of available plugins for Claude Code extensions at MLL.

## 📖 About

This repository serves as a [Claude Code Plugin Marketplace](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces).
It is a centralized catalog for discovering and installing Claude Code plugins within MLL.

## 🚀 Quick Start

### Adding This Marketplace to Claude Code

To add this marketplace to your Claude Code installation:

```bash
/plugin marketplace add mll-lab/claude-plugin-marketplace
```

For detailed usage instructions, see [docs/USAGE.md](docs/USAGE.md).

### Installing Plugins

Once the marketplace is added, you can browse and install available plugins:

```bash
# Browse all available plugins
/plugin

# Install a specific plugin
/plugin install <plugin-name>@mll
```

## 📦 Available Plugins

### Example Plugin

A demonstration plugin that shows the structure and usage of plugins in this marketplace.

- **Command**: `/example-hello`
- **Category**: general
- **Description**: Provides a friendly greeting and demonstrates plugin structure

More plugins will be added as they are developed by the MLL team.

## 🔧 Marketplace Structure

This marketplace follows the official Claude Code plugin marketplace specification:

```
.
├── .claude-plugin/
│   └── marketplace.json          # Marketplace metadata and plugin catalog
├── plugins/                       # Individual plugin directories
│   └── (plugin directories)
├── README.md                      # This file
├── LICENSE                        # MIT License
└── .gitignore                     # Git ignore rules
```

### Marketplace Configuration

The `.claude-plugin/marketplace.json` file contains:
- **name**: Unique identifier for this marketplace
- **owner**: Organization information
- **metadata**: Description, version, and homepage
- **plugins**: Array of available plugins with their metadata

## 📝 Adding New Plugins

To add a new plugin to this marketplace:

1. Create a new directory under `plugins/` with your plugin name
2. Add your plugin files (commands, agents, etc.) to the directory
3. Update `.claude-plugin/marketplace.json` to include your plugin metadata:

```json
{
  "name": "your-plugin-name",
  "description": "Brief description of what your plugin does",
  "version": "1.0.0",
  "author": {
    "name": "Your Name",
    "email": "your.email@mll.com"
  },
  "source": "./plugins/your-plugin-name",
  "category": "productivity",
  "keywords": ["keyword1", "keyword2"]
}
```

## 📚 Documentation

For more information about Claude Code plugin marketplaces, see the [official documentation](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces).

## 🤝 Contributing

This marketplace is maintained by MLL for internal use. If you're part of the MLL team and want to contribute a plugin:

1. Fork this repository
2. Add your plugin following the structure above
3. Submit a pull request with your changes

For detailed contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Resources

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [Plugin Marketplace Documentation](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
- [MLL GitHub](https://github.com/mll-lab)
