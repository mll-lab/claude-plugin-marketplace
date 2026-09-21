---
description: Stage 3 - turn an approved spec into an implementation plan via superpowers:writing-plans.
argument-hint: [path-to-approved-spec | defaults to the current spec]
---

Create the implementation plan for the approved spec: **$ARGUMENTS**
(If no path is given, use the approved spec from the current pipeline.)

Run Stage 3 of the `ai-sdlc:feature-pipeline` skill:

1. Confirm the spec has been approved (GATE 1 passed). If not, stop and say so.
2. Resolve the absolute path to `superpowers:writing-plans`' `SKILL.md` in the plugin cache.
   Dispatch `plan-author` (Opus, **no `model` argument**) with the approved spec, the target
   plan path, and that skill path.
3. **Print its tag table into the transcript** - task, tier, reason, one row each - with the
   task count and the files the plan touches. This is the only place the risk routing is
   visible before Stage 4 runs, and there is no gate between them. Send the plan back if any
   task lacks a tier or a reason.
