---
description: Stage 4 - implement the plan. Defaults to subagent-driven development; uses inline execution only for trivial changes.
argument-hint: [subagent | inline | auto (default)]
---

Implement the current plan. Mode: **$ARGUMENTS** (default: `auto`).

Run Stage 4 of the `ai-sdlc:feature-pipeline` skill:

1. Pick the execution mode:
   - `auto` (default) - decide from the plan's complexity. Choose **subagent-driven**
     unless the change is clearly trivial (roughly 1-2 tasks, single file / tightly
     scoped, no new abstractions, no cross-cutting concerns).
   - `subagent` - force `superpowers:subagent-driven-development`.
   - `inline` - force `superpowers:executing-plans`.
   State the chosen mode and the one-line reason. If `auto` and it's borderline, ask
   before starting.
2. Run the chosen superpowers skill, letting it drive TDD and per-task review.
3. On completion, sanity-check: tests pass, the diff matches the plan, no stray
   debug code. Honor the conventions of the current repository, e.g. coding style,
   architecture patterns, and testing practices.

Do not open the PR here - that's `/pr-open`.
