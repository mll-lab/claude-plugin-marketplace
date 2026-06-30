---
description: Stage 3 - turn an approved spec into an implementation plan via superpowers:writing-plans.
argument-hint: [path-to-approved-spec | defaults to the current spec]
---

Create the implementation plan for the approved spec: **$ARGUMENTS**
(If no path is given, use the approved spec from the current pipeline.)

Run Stage 3 of the `ai-sdlc:feature-pipeline` skill:

1. Confirm the spec has been approved (GATE 1 passed). If not, stop and say so.
2. Invoke `superpowers:writing-plans` on the approved spec to break it into small,
   verifiable tasks with exact file paths and verification steps.
3. Report the resulting task count and the files the plan expects to touch - this
   informs the implementation-mode decision (`/implement`).