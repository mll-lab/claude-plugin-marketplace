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

### Installing Plugins

Once the marketplace is added, you can browse and install available plugins:

```bash
# Browse all available plugins
/plugin

# Install a specific plugin
/plugin install <plugin-name>@mll
```

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

## 📚 Documentation

For more information about Claude Code plugin marketplaces, see the [official documentation](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces).

## 🤝 Contributing

For detailed contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 License

This project is licensed under the [MIT License](LICENSE).
