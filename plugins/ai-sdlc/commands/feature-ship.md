---
description: Run the full feature-delivery pipeline for a Jira issue, pausing at the human review gates (spec approval, review-loop exit).
argument-hint: <jira-issue-id e.g. AI-123>
---

Drive the complete **Feature Factory** pipeline for: **$ARGUMENTS**

Follow the `ai-sdlc:feature-pipeline` skill as the source of truth, running
every stage in order:

0. Intake the Jira issue `$ARGUMENTS`.
1. Spec via `superpowers:brainstorming`.
2. Adversarial challenge via the `spec-challenger` subagent, fold in justified
   findings -> **STOP at GATE 1 for spec approval**.
3. Implementation plan via `superpowers:writing-plans`.
4. Implementation via `superpowers:subagent-driven-development` (or
   `superpowers:executing-plans` only if trivial). State the mode and why.
5. Open the PR with `gh pr create`, linking the issue.
6. Run the `ai-sdlc:copilot-loop` (max 5 rounds) -> **STOP at GATE 2 and
   report**.

Hard rules:
- **Do not cross a GATE without explicit approval from me.** At GATE 1, wait for me
  to approve the spec. At GATE 2, stop and report; do not merge.
- Announce each stage as you enter it. If a required superpowers or copilot skill
  is missing, stop and tell me rather than improvising.
- Honor the conventions when writing code in the repository, e.g. coding style, architecture patterns, and testing practices.

Begin at Stage 0.