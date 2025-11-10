# Specs - Implementation plan and JIRA Issues

This command provides a detailed implementation plan with discrete, trackable tasks and sub-tasks.
Each task is clearly defined, with a clear description, expected outcome, and any necessary resources or dependencies.

## Usage

To create a new implementation plan with JIRA issues, just type:

```
/spec-impl <jira_story_id>
```

## What This Command Does

1. Checks if the folder with <jira_story_id> already exists under `.specs` and has a `requirements.md` and `design.md` file. If not, it stops and asks the user to create the design first with `/spec-design <feature>`.
2. Checks if a file named `tasks.md` exists in the folder, if not it creates one.
3. Based on the design defined in `design.md`, it generates an implementation plan in `tasks.md` with appropriate format.
4. It creates a subtask in JIRA for each task in the implementation plan under the story with ID <jira_story_id>.
5. It asks the user to review the implementation plan and JIRA issues before proceeding.
6. If the user wants to make changes, it updates the tasks in `tasks.md` and the corresponding JIRA issues.
7. Once the user has confirmed the implementation plan and JIRA issues, it proceeds with the execution one task at a time as long as all tasks are implemented. When starting a task, it transitions the JIRA issue to "In Progress".

## Appropriate format

```md
<!-- markdownlint-disable-file MD024 -->
<!-- markdownlint-disable-file MD013 -->
<!-- markdownlint-disable-file MD040 -->

# Implementation Plan

- [ ] 1. Short description of the task (<jira_issue_id_1>)

  - Relevant sub-tasks or steps to complete the task
  - \_Requirements: 5.1, 1.1, etc. (see requirements.md)

- [ ] 2. Another task description (<jira_issue_id_2>)
  - Relevant sub-tasks or steps to complete the task
  - \_Requirements: 5.2, 4.1, etc. (see requirements.md)
```
