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
   When a justified thread's reason is architectural, **dispatch `ai-sdlc:impl-high-risk` to
   make the fix** (no `model` argument), consulting **`ai-sdlc:architect`** (same rule) first
   if the shape of the fix is in question - `architect` cannot edit source, so acting on its
   recommendation yourself would land the architectural fix on the driver. You may also
   dispatch `architect` to annotate a needs-judgment entry; it has no `gh` access, so hand over
   the thread and diff as a file. A needs-judgment thread stays deferred either way.
4. Resolve every actioned thread. **Finish the whole round, then commit and push once** -
   never one thread at a time: a push re-anchors every open comment to a new line, and
   each push re-runs CI and can re-trigger a review mid-round. Then **re-request**
   Copilot's review (a push alone does not reliably re-trigger it - see the skill).
   **If a human has commented on the PR** (the non-Copilot fetch in the skill's
   `github-threads.md` - the Copilot fetch filters them out), ask me to add everything I
   want addressed *before* you push, and handle it with that round's fixes. Absent human
   comments, do not pause.
5. Stop when a round starts with no actionable threads, or after 5 rounds.
6. **Before finalizing, ask me whether I have manual adjustments I want in this PR** - and
   wait. Copilot being done does not mean the PR is. Collect my full list before acting,
   address it as one batch, and push once; dispatch `ai-sdlc:impl-high-risk` (no `model`
   argument) for any of it that is architectural, since `reviewer-high-risk` has already
   run.

Then **STOP at GATE 2** and report: rounds used and why it stopped, what changed
(including anything I asked for at step 6), threads pushed back on (with reasons), any
still-open items, and whether the PR looks ready to merge. Do not merge.
