# GitLab Plugin

A plugin that provides always-available guidance for using the `glab` CLI effectively with GitLab.

## Installation

See [README.md](../../README.md#installing-plugins) for instructions.

## Current Focus: CI/CD Pipelines

This plugin currently focuses on GitLab CI/CD pipeline workflows. Future versions will expand to cover merge requests, repository operations, and other GitLab functionality.

## Usage

This plugin activates automatically when you work with GitLab. You don't need to explicitly invoke it - Claude will reference this guidance whenever you're working with `glab` commands or discussing GitLab operations.

### Automatic Activation

The plugin automatically provides guidance when you:
- Work with `glab` CLI commands
- Check CI/CD pipeline status
- View job logs
- Work with GitLab branches or tags

### Example Interactions

```
User: Check the CI status for the staging branch
Claude: [Uses `glab ci status --branch=staging`]

User: Show me the logs for the failed test job
Claude: [Uses `glab ci trace <job-name> --branch=<branch>`]

User: What's the pipeline status for tag v1.2.3?
Claude: [Uses `glab ci get --branch=v1.2.3`]
```

## Features

- **Correct Command Usage**: Guides Claude to use `--branch` for branches/tags instead of trying to use pipeline IDs
- **Workflow Optimization**: Teaches efficient workflows for checking status and viewing logs
- **Token Efficient**: Concise guidance that helps Claude get it right the first time
- **Always Available**: No need to explicitly invoke - works automatically when relevant

## Common Workflows Covered

1. **Checking Pipeline Status**
   - Current branch or specific ref
   - Compact and detailed views

2. **Getting Pipeline Details**
   - Full pipeline information
   - Job IDs and details

3. **Viewing Job Logs**
   - By job name (recommended)
   - By job ID (when available)

4. **Listing Pipelines**
   - Recent pipelines
   - Filtered by ref or status

## Technical Details

### Plugin Type

This plugin uses a **Skill** to provide always-available guidance. Skills are model-invoked, meaning Claude autonomously uses them based on task context without explicit invocation.

### Activation Triggers

The skill activates when working with:
- GitLab and the `glab` CLI tool
- CI/CD pipelines and jobs
- Pipeline status and logs
- Branches and tags

## Author

- **Name**: MLL Team
- **Email**: info@mll.com

## Version History

- **1.0.0** - Initial release

## License

MIT License - See [LICENSE](../../LICENSE) for details.
