---
description: Run the adversarial spec-challenger (Opus) on a spec on demand, and fold in justified findings.
argument-hint: [path-to-spec | defaults to the current spec]
---

Re-run the adversarial challenge on the spec: **$ARGUMENTS**
(If no path is given, use the spec from the current pipeline / most recent design
document.)

1. Dispatch the `spec-challenger` subagent (Opus) with the spec as input.
2. Triage its findings: fold justified ones into the spec (edit in place); list
   rejected ones with a one-line reason.
3. Present the challenger's verdict and a changelog of what changed, then **STOP**
   for my approval.

Use this when you want another adversarial pass after revising a spec, or to
challenge a spec that was written outside the pipeline.