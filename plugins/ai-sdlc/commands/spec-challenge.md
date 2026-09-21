---
description: Run the adversarial spec-challenger (Opus) on a spec on demand, and fold in justified findings.
argument-hint: [path-to-spec | defaults to the current spec]
---

Re-run the adversarial challenge on the spec: **$ARGUMENTS**
(If no path is given, use the spec from the current pipeline / most recent design
document.)

1. Dispatch the `spec-challenger` subagent (Opus) with the spec as input.
2. Triage its findings. **You decide** what is justified; dispatch `spec-author`
   (`MODE: WRITE`, no `model` argument) to apply it, with the finding appended to the
   decision record's `## Revisions`. List rejected findings with a one-line reason.
   **If the spec has no decision record** - it was written outside the pipeline - create one at
   `.local/pipeline/<slug>/decisions.md` (slug from the spec's filename) holding the spec's path
   under `## Intake` plus a line saying the requirements live in the spec itself, then append
   the findings to its `## Revisions` as usual. Never fold a finding in yourself: the spec keeps
   one author.
3. Present the challenger's verdict and a changelog of what changed, then **STOP**
   for my approval.

Use this when you want another adversarial pass after revising a spec, or to
challenge a spec that was written outside the pipeline.
