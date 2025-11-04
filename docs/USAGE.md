# Using the MLL Lab Claude Code Plugin Marketplace

This guide explains how to use the MLL Lab Claude Code Plugin Marketplace to discover and install plugins.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Adding the Marketplace](#adding-the-marketplace)
- [Browsing Plugins](#browsing-plugins)
- [Installing Plugins](#installing-plugins)
- [Using Installed Plugins](#using-installed-plugins)
- [Updating Plugins](#updating-plugins)
- [Removing Plugins](#removing-plugins)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before using this marketplace, ensure you have:

1. **Claude Code** installed on your system
2. Access to the MLL Lab GitHub organization (for private repositories)
3. Basic familiarity with Claude Code commands

## Adding the Marketplace

To add the MLL Lab marketplace to your Claude Code installation:

```bash
/plugin marketplace add mll-lab/claude-plugin-marketplace
```

This command registers the marketplace with your Claude Code instance, allowing you to browse and install plugins.

### Verification

To verify the marketplace was added successfully:

```bash
/plugin marketplace list
```

You should see `mll-lab-marketplace` in the list of available marketplaces.

## Browsing Plugins

### List All Available Plugins

To see all plugins available in all your marketplaces:

```bash
/plugin
```

or

```bash
/plugin list
```

### Filter by Marketplace

To see only plugins from the MLL Lab marketplace:

```bash
/plugin list --marketplace mll-lab-marketplace
```

### View Plugin Details

To get detailed information about a specific plugin:

```bash
/plugin info example-plugin@mll-lab-marketplace
```

## Installing Plugins

### Install a Specific Plugin

To install a plugin from the MLL Lab marketplace:

```bash
/plugin install example-plugin@mll-lab-marketplace
```

### Install Latest Version

By default, the latest version is installed. To explicitly specify a version:

```bash
/plugin install example-plugin@mll-lab-marketplace@1.0.0
```

### Verify Installation

After installation, verify the plugin is available:

```bash
/plugin list --installed
```

## Using Installed Plugins

Once installed, plugins provide new commands or agents you can use in Claude Code.

### Using Commands

If a plugin provides commands, you can use them directly:

```bash
/example-hello
```

### Using Agents

If a plugin provides agents, Claude Code will automatically use them when relevant tasks come up.

### Getting Help

To get help on a specific plugin's usage:

```bash
/help example-plugin
```

## Updating Plugins

### Update a Single Plugin

To update a specific plugin to the latest version:

```bash
/plugin update example-plugin@mll-lab-marketplace
```

### Update All Plugins

To update all installed plugins:

```bash
/plugin update --all
```

### Check for Updates

To see which plugins have available updates:

```bash
/plugin outdated
```

## Removing Plugins

### Uninstall a Plugin

To remove an installed plugin:

```bash
/plugin uninstall example-plugin
```

### Remove Marketplace

To remove the entire marketplace (this doesn't uninstall already installed plugins):

```bash
/plugin marketplace remove mll-lab-marketplace
```

## Troubleshooting

### Marketplace Not Found

If you get an error that the marketplace cannot be found:

1. Verify you have access to the GitHub repository
2. Check your internet connection
3. Ensure the repository name is correct: `mll-lab/claude-plugin-marketplace`

### Plugin Installation Fails

If a plugin fails to install:

1. Check that the plugin exists in the marketplace
2. Verify the plugin name is spelled correctly
3. Try removing and re-adding the marketplace
4. Check the plugin's README for specific requirements

### Command Not Working

If an installed plugin's command doesn't work:

1. Verify the plugin is installed: `/plugin list --installed`
2. Check the plugin's documentation for correct usage
3. Try reinstalling the plugin
4. Restart Claude Code

### Getting Help

For additional support:

1. Check the plugin's README in the `plugins/` directory
2. Review the [CONTRIBUTING.md](../CONTRIBUTING.md) for plugin structure
3. Contact the plugin author (listed in the plugin metadata)
4. Open an issue in the marketplace repository

## Best Practices

### Regular Updates

Keep your plugins updated for the latest features and bug fixes:

```bash
/plugin update --all
```

### Minimal Installation

Only install plugins you actually need to keep Claude Code performant.

### Review Before Installing

Always review a plugin's documentation before installing to understand what it does.

### Report Issues

If you encounter bugs or have feature requests, report them to help improve the marketplace.

## Additional Resources

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [Plugin Development Guide](https://docs.claude.com/en/docs/claude-code/plugins)
- [Marketplace Documentation](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
- [MLL Lab GitHub](https://github.com/mll-lab)

---

For questions or issues specific to the MLL Lab marketplace, please contact the MLL Lab development team.
