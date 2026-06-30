---
description: Stage 1+2 - brainstorm a spec from a JIRA issue, then run the adversarial spec-challenger and fold in justified findings. Stops for your approval.
argument-hint: <jira-issue-id e.g. AI-123>
---

Produce a reviewed spec for: **$ARGUMENTS**

Run Stages 0-2 of the `ai-sdlc:feature-pipeline` skill:

1. **Intake** - Fetch JIRA issue `$ARGUMENTS` (Atlassian Rovo MCP) and restate the
   problem, outcome, and constraints. Surface open questions.
2. **Brainstorm** - Invoke `superpowers:brainstorming` to produce the spec / design
   document. Answer its questions from the JIRA context where possible.
3. **Challenge** - Dispatch the `spec-challenger` subagent (Opus) on the spec. Fold
   justified findings into the spec; list rejected ones with a one-line reason.

Then **STOP at GATE 1**: present the revised spec, the challenger's verdict, and your
changelog, and wait for me to approve / revise / re-challenge. Do not start planning.