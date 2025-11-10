# Specs - Requirements from JIRA Story

This command captures user stories and acceptance criteria in structured EARS notation. It does not implement anything, but helps to define the requirements clearly.

## Usage

To create a new requirement, just type:

```
/spec:req <jira_issue_id>
```

## What This Command Does

1. Retrieves the story with the given ID <jira_issue_id> from JIRA.
2. Checks if a folder with a filepath-safe version of <jira_issue_id> already exists under `.specs`, if not it creates it.
3. Checks if a file named `requirements.md` exists in the newly created folder, if not it creates one.
4. Turns the description of the JIRA story into a fully fleshed out `requirements.md` file in the appropriate format.
5. Asks the user for additional details to fill out the requirements. This is a repetitive process until all details are captured.
6. Once finished, it asks the user to review the `requirements.md` file.
7. If the user approves, it determines the changes to the original requirements and posts them as comment to the JIRA issue in the language of the original issue description.

## Appropriate Format

```md
<!-- markdownlint-disable-file MD024 -->
<!-- markdownlint-disable-file MD013 -->
<!-- markdownlint-disable-file MD040 -->

# Requirements Document

## Introduction

Describe the feature in a detailed paragraph.

## Requirements

### Requirement 1

**User Story** Describe the user story for requirement 1.

#### Acceptance Criteria

1. Describe the first acceptance criterion in EARS format.
2. Describe the second acceptance criterion in EARS format.
3. Describe the third acceptance criterion in EARS format.

### Requirement 2

**User Story** Describe the user story for requirement 2.

#### Acceptance Criteria

1. Describe the first acceptance criterion in EARS format.
2. Describe the second acceptance criterion in EARS format.
```

## EARS format

EARS (Easy Approach to Requirements Syntax) notation provides a structured format for writing clear, testable requirements. Each acceptance criterion should be expressed in the following format:

```
WHEN [condition/event]
THE SYSTEM SHALL [expected behavior]
```

```
IF [unwanted condition/event],
THEN THE SYSTEM SHALL [system response/behavior]
```

```
WHILE [system state],
THE SYSTEM SHALL [system response/behavior]
```

```
WHERE [feature],
THE SYSTEM SHALL [system response/behavior]
```

Note these patterns can be combined for more complex scenarios.
