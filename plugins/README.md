# Plugins Directory

This directory contains individual plugin implementations for the MLL Claude Code Plugin Marketplace.

## Structure

Each plugin should be in its own subdirectory with the following structure:

```
plugins/
└── my-plugin/
    ├── README.md           # Plugin documentation
    ├── plugin.md           # Plugin implementation (commands/agents)
    └── (other files)       # Any additional files needed
```

## Adding a Plugin

1. Create a new directory with your plugin name
2. Add your plugin files
3. Update the marketplace.json file in `.claude-plugin/` to reference your plugin
4. Document your plugin in its README.md

Refer to the [plugin development documentation](https://docs.claude.com/en/docs/claude-code/plugins) for more information.
