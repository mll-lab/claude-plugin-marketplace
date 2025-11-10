# Spec Plugin

A spec-driven development plugin that provides a structured, sequential workflow for software development from requirements gathering through implementation. This plugin integrates with JIRA to maintain traceability from initial requirements through to implementation tasks.

## Installation

See [README.md](../../README.md#installing-plugins) for instructions.

### Prerequisites

**Important:** Before using this plugin, you must configure the Atlassian Rovo MCP (Model Context Protocol) to enable JIRA integration.

To check the status of your MCP connection and authenticate if necessary, run:

```bash
/mcp
```

This will show you the status of all configured MCPs. If the Atlassian Rovo MCP is not connected or authenticated, follow the prompts to re-authenticate.

## Usage

The spec plugin provides three commands that should be run sequentially to guide your development process. Each command can be run multiple times to iterate and refine at each stage.

### 1. Capture Requirements: `/spec:req <jira_id>`

Start by capturing requirements from a JIRA story:

```claude_code
/spec:req PROJ-123
```

This command:

- Retrieves the JIRA story with the given ID
- Creates a `.specs/<jira_id>/` folder in your project
- Generates a `requirements.md` file using EARS (Easy Approach to Requirements Syntax) notation
- Interactively asks for additional details to complete requirements
- Posts the requirements back to JIRA as a comment upon approval

### 2. Design the Solution: `/spec:design <jira_id>`

Next, create a technical design based on your requirements:

```claude_code
/spec:design PROJ-123
```

This command:

- Checks that requirements exist (will prompt you to run `/spec:req` first if missing)
- Creates a `design.md` file with architecture, component interactions, and implementation considerations
- Includes mermaid diagrams for visualizing architecture
- Documents data models, error handling, and testing strategy

### 3. Plan Implementation: `/spec:impl <jira_id>`

Finally, generate a detailed implementation plan with trackable tasks:

```claude_code
/spec:impl PROJ-123
```

This command:

- Checks that both requirements and design exist (will prompt if missing)
- Creates a `tasks.md` file with discrete, trackable tasks
- Automatically creates JIRA subtasks under the parent story
- Allows iterative refinement of tasks
- Executes tasks one at a time, transitioning JIRA issues to "In Progress"

## Workflow

The plugin enforces a disciplined three-phase workflow:

```plaintext
Requirements → Design → Implementation
```

**Important Notes:**

- Commands must be run in sequence (requirements before design, design before implementation)
- Each command can be run multiple times to iterate and refine documentation
- The plugin maintains traceability from requirements through to implementation tasks
- JIRA integration ensures all work is tracked and documented

## Features

- **JIRA Integration**: Bidirectional sync with JIRA - reads stories, creates subtasks, posts comments, and transitions issues
- **EARS Notation**: Uses industry-standard Easy Approach to Requirements Syntax for clear, testable requirements
- **Enforced Dependencies**: Prevents skipping phases in the development workflow
- **Iterative Refinement**: Each phase can be revisited and refined as understanding evolves
- **Requirements Traceability**: Links implementation tasks back to specific requirements
- **Automated Task Management**: Creates and transitions JIRA issues automatically
- **Structured Documentation**: Organizes all specs in a `.specs/` directory per feature
- **Multi-language Support**: Posts JIRA comments in the original issue language

## Implementation Details

### File Structure

The plugin creates a `.specs/` directory at your project root with the following structure:

```plaintext
.specs/
└── <jira_id>/
    ├── requirements.md
    ├── design.md
    └── tasks.md
```

### Requirements

- JIRA access must be configured
- Requires permissions to:
  - Read JIRA stories
  - Create subtasks
  - Post comments
  - Transition issues

### Documentation Format

- Uses Markdown with mermaid diagram support
- EARS notation for acceptance criteria:
  - `WHEN [condition] THE SYSTEM SHALL [behavior]`
  - `IF <unwanted condition>, THEN the system shall [response]`
  - `WHILE <state>, the system shall [behavior]`
  - `WHERE <feature>, the system shall [behavior]`
- Checklist format for implementation tasks

#### Markdownlint Configuration

Generated documentation files include the markdownlint disable directives at the top:

```markdown
<!-- markdownlint-disable-file MD024 -->
<!-- markdownlint-disable-file MD013 -->
<!-- markdownlint-disable-file MD040 -->
```

These directives prevent linting errors in IDEs with [markdownlint](https://github.com/DavidAnson/markdownlint) enabled.
For a complete list of rules, refer to the [documentation](https://github.com/DavidAnson/markdownlint?tab=readme-ov-file#rules--aliases).

### Design Document Sections

- High-level description
- Architecture and component interaction diagrams
- Infrastructure, frontend, API, and database changes
- Data models and interfaces
- Error handling strategy
- Unit testing approach (targeting 100% coverage)
- Performance, security, and compliance considerations

## Author

- **Name**: MLL Team
- **Email**: <info@mll.com>

## Version History

- **1.0.0** - Initial release

## License

MIT License - See [LICENSE](../../LICENSE) for details.
