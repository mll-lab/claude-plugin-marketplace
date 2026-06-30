---
description: Stage 6 - run the bounded Copilot resolution loop (max 5 rounds) on a PR, then stop and report.
argument-hint: [pr-number-or-url | defaults to the current branch's PR]
---

Run the Copilot resolution loop for the PR: **$ARGUMENTS**
(If no PR is given, use the PR for the current branch.)

Follow the `ai-sdlc:copilot-loop` skill. For up to **5 rounds**:

1. Pull Copilot's open threads with `gh` (commands in the `copilot-loop`
   skill's `github-threads.md`).
2. Classify each: justified / unjustified / needs-human-judgment.
3. Justified -> fix in code and reply; unjustified -> reply with a respectful
   rationale, no code change; needs-judgment -> defer and flag.
4. Resolve every actioned thread. Commit and push (triggers re-review).
5. Stop when a round starts with no actionable threads, or after 5 rounds.

Then **STOP at GATE 2** and report: rounds used and why it stopped, what changed,
threads pushed back on (with reasons), any still-open items, and whether the PR
looks ready to merge. Do not merge.