---
description: Stage 4 - implement the plan. Defaults to subagent-driven development; uses inline execution only for trivial changes.
argument-hint: [subagent | inline | auto (default)]
---

Implement the current plan. Mode: **$ARGUMENTS** (default: `auto`).

Run Stage 4 of the `ai-sdlc:feature-pipeline` skill:

1. **Check the plan's risk tags first.** If any task is tagged `**Risk:** architectural`,
   inline mode is **forbidden** - it would have you implement architectural work yourself,
   past every model pin. Reject `/implement inline` in that case and say why.
   Then pick the mode:
   - `auto` (default) - **subagent-driven** unless no task is `architectural` *and* the
     change is clearly trivial (1-2 tasks, single file, no new abstractions, no
     cross-cutting concerns).
   - `subagent` - force `superpowers:subagent-driven-development`.
   - `inline` - force `superpowers:executing-plans`. Only valid with no `architectural` task.
   State the chosen mode and the one-line reason. If `auto` and it's borderline, ask first.
2. Run the chosen superpowers skill, letting it drive TDD and per-task review. Dispatch by
   tier, per Stage 4 of the `ai-sdlc:feature-pipeline` skill: `architectural` ->
   `impl-high-risk` (**no `model` argument**); `integration` / `mechanical` ->
   `general-purpose` with an explicit standard / cheap model; task reviews of
   `architectural` tasks and the final whole-branch review -> `reviewer-high-risk` (**no
   `model` argument**). A batch takes the highest tag it contains. **Log the tier, agent,
   and model for every dispatch** - e.g.
   `Task 3: done (risk: architectural, agent: impl-high-risk, model: opus)`.
3. On completion, sanity-check: tests pass, the diff matches the plan, no stray
   debug code. Honor the conventions of the current repository, e.g. coding style,
   architecture patterns, and testing practices.

Never pipe a repository-wide test run or a `git commit` through `tail` or `head` - the
failing package's block is in the middle, and a retry that goes green typically
overwrites the per-package log, so a piped-away failure is unrecoverable. Redirect to
a file and grep it (`… > /tmp/run.log 2>&1 || grep -nE "Failed:|FAIL|[0-9]+ failed"
/tmp/run.log`). If the repository preserves failure evidence, name the preserved path
in the task report; if a gate fails in a package your change does not touch, say so
rather than retrying in silence. See Stage 4 of the `ai-sdlc:feature-pipeline` skill.

Do not open the PR here - that's `/pr-open`.
