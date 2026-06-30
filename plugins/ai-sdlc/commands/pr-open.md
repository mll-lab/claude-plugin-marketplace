---
description: Stage 5 - commit, push, and open a PR linked to the Jira issue.
argument-hint: [jira-issue-id e.g. AI-123]
allowed-tools: Bash(git:*), Bash(gh:*)
---

Open the pull request for the current branch. Jira issue: **$ARGUMENTS**

Run Stage 5 of the `ai-sdlc:feature-pipeline` skill:

1. Ensure everything is committed and the branch is pushed.
   - Current status: !`git status --short --branch`
2. Create the PR with `gh pr create`. The body must:
   - Link the Jira issue `$ARGUMENTS` (use your Jira<->GitHub convention, e.g.
     `Closes $ARGUMENTS`, or paste the issue URL).
   - Summarize the change, the key spec decisions, and how it was tested.
3. Report the PR URL. Copilot will review automatically - follow with
   `/code-review-address` once its review lands.