---
description: Stage 4 - implement the plan. Defaults to subagent-driven development; uses inline execution only for trivial changes.
argument-hint: [subagent | inline | auto (default)]
---

Implement the current plan. Mode: **$ARGUMENTS** (default: `auto`).

Run Stage 4 of the `ai-sdlc:feature-pipeline` skill:

1. **Check the plan's risk tags first, before picking a mode.** If any task is tagged
   `**Risk:** architectural`, or any task carries no risk tier at all, inline mode is
   **forbidden** - it would have you implement architectural (or untriaged) work yourself,
   past every model pin. An untagged plan satisfies "no task is architectural" by omission,
   not by review, so triage it first: tag it via `plan-author`, or apply superpowers' own
   Model Selection signals and say which. Only once every task carries a risk tier and none
   is `architectural` can you pick a mode:
   - `auto` (default) - **subagent-driven** unless every task carries a risk tier, none is
     `architectural`, *and* the change is clearly trivial (1-2 tasks, single file, no new
     abstractions, no cross-cutting concerns).
   - `subagent` - force `superpowers:subagent-driven-development`.
   - `inline` - force `superpowers:executing-plans`. Only valid when every task carries a
     risk tier and none is `architectural`.
   State the chosen mode and the one-line reason. If `auto` and it's borderline, ask first.
2. Run the chosen superpowers skill, letting it drive TDD and per-task review. Dispatch by
   tier, per Stage 4 of the `ai-sdlc:feature-pipeline` skill: `architectural` ->
   `impl-high-risk` (**no `model` argument**); `integration` / `mechanical` ->
   `general-purpose` with an explicit standard / cheap model; task reviews of
   `architectural` tasks and the final whole-branch review -> `reviewer-high-risk` (**no
   `model` argument**). A batch takes the highest tag it contains. **Append the tier, agent,
   and model to superpowers' completion line for every dispatch** - never replace that line;
   superpowers keys resume detection on the literal word `complete` - e.g.
   `Task 3: complete (commits a1b2c3d..e4f5a6b, review clean; risk: architectural, agent: impl-high-risk, model: opus)`.
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
