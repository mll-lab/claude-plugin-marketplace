---
name: feature-pipeline
description: The canonical end-to-end feature-delivery pipeline. Use when the user wants to take a Jira issue (or a described feature) from idea to a reviewed PR - e.g. "look at AI-123 and implement it", "ship this feature", "run the pipeline". Covers spec brainstorming, adversarial spec challenge, an implementation plan, subagent-driven or inline implementation, opening a PR, and a bounded Copilot resolution loop. This skill is the single source of truth that the /feature-ship orchestrator and the per-stage commands all defer to.
---

# Feature Factory pipeline

This skill defines the full pipeline for delivering a feature. It composes the
`superpowers` plugin's skills and adds two things superpowers does not: an
**adversarial spec-challenge** step (a fresh Opus subagent that attacks the spec)
and explicit **human review gates** at the points where the user wants to stay in
the loop.

## Prerequisites

- The **superpowers** plugin must be installed (provides `superpowers:brainstorming`,
  `superpowers:writing-plans`, `superpowers:subagent-driven-development`,
  `superpowers:executing-plans`). If a superpowers skill is missing, say so and stop
  rather than improvising a replacement.
  **Minimum superpowers version: 6.3.0** - Stage 3's risk tags extend `writing-plans`'
  task structure and Stage 4 uses `subagent-driven-development`'s tier vocabulary, so an
  older version may not carry the sections this pipeline depends on.
- The **ai-sdlc agents** this pipeline dispatches (`spec-author`, `spec-challenger`,
  `plan-author`, `impl-high-risk`, `reviewer-high-risk`, `architect`) must be dispatchable.
  If one is missing - a stale plugin cache, usually - **stop and say so.** Do not quietly do
  its work inline: for the pinned agents that would land architectural work on the driver,
  which is the exact failure this pipeline is built to prevent.
- Stage 6 uses the **`ai-sdlc:copilot-loop`** skill, which drives
  Copilot directly via `gh` - no separate Copilot skill needs to be installed.
- Jira access (the Jira MCP tools, `mcp__*atlassian*`) for fetching the issue.
- `gh` CLI authenticated, for opening the PR.

## Operating principles

- **Stop at every GATE.** A gate means: present what you have, then wait for an
  explicit human decision. Never cross a gate on your own initiative.
- **One stage at a time.** Announce which stage you are entering and why.
- **Defer, don't reinvent.** Inside a stage, invoke the named superpowers skill and
  let it run. This skill only adds orchestration, the challenge step, and the gates.
- **Persist artifacts.** Keep the spec and plan as files in the repo (the superpowers
  skills already do this) so each stage has a durable input.
- **Respect repository conventions** when you (or a subagent) write code, honor the
  existing coding standards and practices as documented in the repository.

## Model policy

This pipeline is **driver-agnostic**. Sonnet is the intended driver; Opus works too (the
driver is then simply stronger than it needs to be). What must not vary is that
architectural and high-risk work runs on Opus - so that guarantee lives in agent
frontmatter, not in the driver's judgement.

**How a subagent's model resolves**, in order:

1. A `model` argument passed at dispatch time wins.
2. Otherwise the agent definition's frontmatter `model:` applies.
3. Otherwise the subagent inherits this session's model - unless a default subagent model
   is configured, which then wins.

**So: never pass `model` when dispatching a pinned ai-sdlc agent.** Passing one silently
overrides the pin, which is the entire mechanism. This is a deliberate exception to
`superpowers:subagent-driven-development`'s "always specify the model explicitly" rule, and
it applies *only* to the pinned agents. When you dispatch `general-purpose`, that rule
stands - state the model, because an omitted one inherits the driver.

**Pinned agents** (all `model: opus`): `spec-author`, `spec-challenger`, `plan-author`,
`impl-high-risk`, `reviewer-high-risk`, `architect`.

**What is enforced structurally, and what is not.** The pins cover Stages 1-3, the
architectural implementers, and the high-value reviews. They do **not** cover the
`integration` and `mechanical` implementers, the batching rule, or the untagged-plan rule:
`superpowers:subagent-driven-development` dispatches `general-purpose` with a model argument
there, so those depend on this prose and on your judgement. The asymmetry is deliberate -
pin in the direction of escalation. A mechanical task that accidentally runs on Opus wastes
money; an architectural task that accidentally runs on Sonnet ships bad architecture into a
PR.

**Escalate to `architect`** from any stage when the work turns out to involve: a new
abstraction or module boundary the plan did not anticipate; a cross-cutting change; schema
or migration work; auth, secrets, or data exposure; a public interface or
backward-compatibility question; concurrency or ordering; a performance-critical path; an
irreversible or data-destructive step; or **the plan turning out to be wrong**. `architect`
advises a ruling that you still make and still record - it is never a reason to stall.

**If Opus is unavailable** (not on the plan, or rate-limited), stop and say so. Do not fall
back to a cheaper model for architectural work. This pipeline's founding defect was a
downgrade that produced no error, no warning, and no visible difference in the transcript -
a silent fallback would recreate it exactly.

**Record what actually ran.** For every dispatch, log the risk tier, the agent, and the
model - in the ledger line and in your stage report. A policy with no runtime evidence
cannot be checked on any given run.

---

## Stage 0 - Intake

1. Resolve the Jira issue from the argument (e.g. `AI-123`). Use the Jira MCP
   tools to fetch the issue: title, description, comments, labels, linked
   issues/PRs, and acceptance criteria.
2. Restate the issue in 2-4 sentences: the problem, the desired outcome, and any
   constraints you found. Note open questions explicitly.
3. **Move the issue to In Progress.** Use the Jira MCP to transition the issue to
   the team's started / "in progress" workflow state - pick the state whose *type* is
   `started` (commonly named "In Progress", but the exact name varies per team). If
   it is already in that state, leave it. Note the transition in your intake summary.
4. Confirm you are on (or create) an appropriate feature branch. Prefer a
   git worktree (`superpowers:using-git-worktrees`) when one is available, so the
   pipeline does not disturb the user's working tree.

## Stage 1 - Spec (brainstorm)

Brainstorming is a dialogue with the human, and a subagent cannot have it. So this stage
splits: **you run the conversation, `spec-author` (Opus) makes the architectural calls and
writes the document.**

Invoke **`superpowers:brainstorming`** and follow its process, with two changes.

**First, the decision record.** Create `.local/pipeline/<issue-id>/decisions.md` and append
to it as you go - never truncate it. Sections, in order:

- `## Intake` - the Stage 0 restatement **plus the issue's acceptance criteria verbatim**.
  `spec-author` has no Jira access; if the criteria reach it only as your paraphrase, they
  are one lossy hop from being silently dropped.
- `## Q&A` - one `**Q:** / **A:**` pair per exchange with the human.
- `## Approvals` - which design sections they approved, and any conditions.
- `## Revisions` - each change they ask for after reading a draft.

**Second, two dispatches of `spec-author`** (no `model` argument - see Model policy):

1. **`MODE: APPROACHES`** - it reads the decision record and the repo, and returns 2-3
   approaches with trade-offs, a recommendation, and a section outline.
2. You present those to the human and collect the per-section approval
   `superpowers:brainstorming` requires, appending each to `## Approvals`.
3. **`MODE: WRITE`** - it writes the spec at the path you give it.
4. You present the spec. **Revisions go back to `spec-author`** (`MODE: WRITE` again, with the
   request appended to `## Revisions`) - never patch it yourself. A spec Opus wrote and you
   then edited drifts in architectural assumption, and the drift is invisible in a diff.

**If `superpowers:brainstorming` classifies the request as spike or bounded**, both of which
deliberately produce no spec file, **stop and report that.** A Jira issue that turns out to be
a one-file change does not need Stages 2-4; saying so is a correct outcome, not a failure. Do
not force a spec into existence to keep the pipeline moving.

Output of this stage: a saved spec/design document, and a decision record that explains it.

## Stage 2 - Adversarial challenge

1. Dispatch the **`spec-challenger`** subagent (Opus) with the spec document as
   input. It returns a structured critique with severity-tagged findings
   (BLOCKER / MAJOR / MINOR / QUESTION) and an overall verdict.
2. Triage the critique:
   - **Justified findings** -> dispatch **`spec-author`** (`MODE: WRITE`, no `model`
     argument) with the finding appended to the decision record's `## Revisions`. **You
     decide what is justified; it applies the change.** Folding in a BLOCKER is higher-stakes
     architectural editing than any revision request, and Stage 1's single-author rule holds
     here for the same reason: a spec with one author stays internally consistent.
   - **Unjustified or out-of-scope findings** -> note them with a one-line reason
     for not acting, so the human can see what was considered and rejected.
3. Produce a short changelog: what the challenge surfaced and what you changed.

### >>> GATE 1: spec approval <<<

Present: (a) the revised spec, (b) the challenger's verdict, (c) your changelog of
folded-in vs rejected findings. Then **STOP** and ask the user to approve, request
further changes, or re-run the challenge (`/spec-challenge`). Do not proceed to
planning until they approve.

## Stage 3 - Implementation plan

Once the spec is approved, dispatch **`plan-author`** (Opus, no `model` argument - see Model
policy) with three things: the approved spec, the target plan path, and **the absolute path to
`superpowers:writing-plans`' `SKILL.md`**. Resolve that path yourself (the superpowers plugin
cache) and pass it - `plan-author` reads the skill rather than holding the `Skill` tool, which
keeps the plan format tied to the version actually installed.

`plan-author` writes the plan and tags **every task** with a risk tier that Stage 4 routes on:

- **`architectural`** - a new abstraction or module boundary; a public interface or
  backward-compatibility question; schema or migration work; auth, secrets, or data exposure;
  concurrency or ordering; an irreversible or data-destructive step.
- **`integration`** - multiple files whose interaction matters, no new boundary.
- **`mechanical`** - one file or a repeated same-shape edit, with the code already in the plan.

**Risk beats size:** a one-file auth change with verbatim code is `architectural`.

**Print the tag table into the transcript** - task, tier, reason, one row each - before Stage 4
begins. There is no gate between Stage 3 and Stage 4, so this table is the human's only
chance to see the routing on an end-to-end run and interrupt if a tag is wrong. Report the
task count and the files the plan expects to touch alongside it.

If `plan-author` returns any task without a tier or without a reason, send it back. An
untagged task costs you the expensive default in Stage 4.

## Stage 4 - Implementation

**Inline mode is forbidden when any task is tagged `architectural`, or when any task carries
no risk tier at all.**
`superpowers:executing-plans` means *you* implement, so on a Sonnet driver it routes
architectural work straight past every pin in the Model policy. The inline trigger ("1-2
tasks, a single file") overlaps heavily with single-file `architectural` triggers like an auth
change or a migration, which is exactly when it is most tempting. An **untagged** plan is
exposed the same way by omission: "no task is tagged `architectural`" is literally true of a
plan with no tags at all, so a legacy, hand-written, or directly-invoked-`writing-plans` plan
can walk an untagged single-file auth change or migration straight through the inline door.
Before choosing a mode, tag the plan (see "A plan with no tags anywhere" below) - only once
every task carries a risk tier can inline even be considered. Check the tags first.

Decide the execution mode:

- **Default - subagent-driven.** Use **`superpowers:subagent-driven-development`**. Required
  whenever any task is tagged `architectural`, or whenever any task lacks a risk tier and has
  not yet been given one. Triage clears this only when it ends with a tier written against every
  task; a judgement *about* the plan that leaves the tasks untiered does not.
- **Inline (rare).** Use **`superpowers:executing-plans`** only when **every task carries a
  risk tier and none is `architectural`**, **and** the change is genuinely small: roughly 1-2
  tasks, a single file or tightly scoped area, no new abstractions, no cross-cutting concerns.

State which mode you chose and the one-line reason. If it is a borderline call, ask before
starting.

### Dispatching by risk tier

Let `superpowers:subagent-driven-development` drive TDD and per-task review, and follow its
Model Selection section - with these ai-sdlc overrides:

| Task's tag | Dispatch | Enforcement |
|---|---|---|
| `architectural` | **`impl-high-risk`**, no `model` argument | Structural (frontmatter pin) |
| `integration` | `general-purpose`, `model` = standard | Prose - your judgement |
| `mechanical` | `general-purpose`, `model` = cheap | Prose - your judgement |
| Task review of an `architectural` task | **`reviewer-high-risk`**, no `model` argument | Structural |
| Task review of other tasks | per superpowers, scaled to the diff | Prose |
| Final whole-branch review | **`reviewer-high-risk`**, no `model` argument | Structural |
| Fix wave after the final whole-branch review | **`impl-high-risk`**, no `model` argument, whenever any finding is architectural; otherwise per superpowers | Prose - your judgement |
| Fix-loop rounds 4-5 | per superpowers, one tier above the implementer that stuck. If that was `impl-high-risk`, there is no higher model and `effort` is fixed in its frontmatter - sharpen the brief, split the task, or consult `architect` instead | Prose |

**The final whole-branch review always goes to `reviewer-high-risk` (no `model` argument),
regardless of execution mode** - an inline run still owes the branch this pass; skipping it
because `subagent-driven-development` was never invoked would silently drop the highest-value
review in the whole contract.

**And its findings come back as one fix dispatch** - `superpowers:subagent-driven-development`
sends the complete findings list to a single fix subagent. Route that wave to
**`impl-high-risk`** (no `model` argument) whenever any finding is architectural: it is the
last code on the branch, nothing reviews it again, and a finding only Opus caught is the worst
possible thing to hand to the cheapest model.

**Batches.** Superpowers batches small same-shape work into one dispatch. A batch takes the
**highest** tag it contains, and a batch containing an `architectural` task is not batched at
all - that task gets its own dispatch and its own review.

**A plan with no tags anywhere** predates this contract - hand-written, or from
`superpowers:writing-plans` invoked directly. Do **not** treat it as all-`architectural`; that
would send an entire legacy plan to Opus and invert the point of this pipeline. Either
dispatch `plan-author` to tag it, or - **only once you have read every task and none of them
meets an architectural trigger** - fall back to superpowers' own Model Selection signals, and
**say which, in the transcript.** Superpowers' signals are *size* signals ("1-2 files with a
complete spec"), and **risk beats size**: if any task does meet an architectural trigger, that
fallback is closed - tag the plan, or route that task to `impl-high-risk` (no `model`
argument). A *single* untagged task inside an otherwise tagged plan is different: treat that
one as `architectural`, because there the omission is a mistake.

**Log what actually ran.** Append the tier, agent, and model to superpowers' existing
completion line for each task - never replace it. Superpowers keys resume detection on the
literal word `complete`; a line missing it gets that task silently re-dispatched after a
compaction. In the SDD ledger line for each task, and in your stage report:

```
Task 3: complete (commits a1b2c3d..e4f5a6b, review clean; risk: architectural, agent: impl-high-risk, model: opus)
Task 4: complete (commits e4f5a6b..c9d0e1f, review clean; risk: mechanical, agent: general-purpose, model: haiku)
```

**Non-task dispatches get their own line.** The final-review fix wave and Stage 6's fixes have
no task completion line to attach to, so write one of your own recording the same triple - the
dispatch, the agent, and the model:

```
Final-review fix wave: 3 findings, 1 architectural (agent: impl-high-risk, model: opus)
```

Without it the one dispatch most likely to be silently downgraded is the one dispatch with no
record at all.

The defect this pipeline was built to fix produced no visible difference in the transcript.
These lines are what make it visible, and what lets anyone check afterwards that the policy
actually held.

When implementation completes, run a final sanity check: tests pass, the diff matches the
plan, no stray debug code.

**Never pipe a repository-wide test run or a `git commit` through `tail` or `head`.**
On a large repo the useful lines are in the middle: the failing package's block sits
between hundreds of lines of passing output, so `tail` shows you the closing summary,
`head` shows you the start, and neither shows you the failure. Redirect to a file and
grep the file:

```bash
git commit -F /tmp/msg > /tmp/commit.log 2>&1 || grep -nE "Failed:|FAIL|[0-9]+ failed" /tmp/commit.log
```

This matters most for the run you cannot reproduce on demand. A retry that goes green
usually **overwrites** whatever per-package log the build tool kept, so a failure you
piped away is gone for good. Real case: five recorded sightings of two load-sensitive
flakes each lost the failing test name exactly this way.

Two habits that follow from it:

- If the repository preserves failure evidence of its own, **name the preserved path in
  the task report**. A reviewer who cannot see your terminal can still read the
  artefact.
- If a repo-wide gate fails in a package your change does not touch, **say so
  explicitly** instead of retrying in silence. An unattributed retry is how a flake
  stays undiagnosed for months.

## Stage 5 - Open the PR

1. Ensure all work is committed and the branch is pushed.
2. Create the PR with `gh pr create`. The PR body should:
   - Link the Jira issue (e.g. `Closes AI-123` if your Jira<->GitHub link uses
     that, otherwise reference the URL).
   - Summarize the change, the spec decisions, and how it was tested.
3. Report the PR URL.

## Stage 6 - Copilot resolution loop

Copilot reviews the PR automatically. Hand off to the
**`ai-sdlc:copilot-loop`** skill, which runs a **bounded loop of at most
5 rounds**: pull Copilot's threads, fix and reply to justified ones, push back
politely on unjustified ones, resolve all threads, and let Copilot re-review -
stopping when there are no actionable threads left or after 5 rounds.

### >>> GATE 2: loop exit <<<

When the loop ends, **STOP** and report: rounds used, what was changed, which
threads were pushed back on and why, and any items still open (only possible if the
5-round cap was hit). Let the user decide whether to merge or continue manually.

---

## Quick reference

| Stage | Skill / agent invoked | Model | Gate |
|-------|-----------------------|-------|------|
| 0 Intake | Jira MCP | driver | - |
| 1 Spec | `superpowers:brainstorming` (driver) + `spec-author` | driver + **opus** (pinned) | - |
| 2 Challenge | `spec-challenger`, fold-in via `spec-author` | **opus** (pinned) | GATE 1: spec approval |
| 3 Plan | `plan-author` (reads `superpowers:writing-plans`) | **opus** (pinned) | - |
| 4 Implement | `superpowers:subagent-driven-development`; `impl-high-risk` / `reviewer-high-risk` for `architectural` work, `general-purpose` otherwise | **opus** (pinned) / tiered by risk tag | - |
| 5 PR | `gh pr create` | driver | - |
| 6 Review loop | `ai-sdlc:copilot-loop`, escalating to `architect` | driver + **opus** (pinned) | GATE 2: loop exit |
| any | `architect` (escape hatch) | **opus** (pinned) | - |

"Pinned" means the model is set in the agent's frontmatter - so **do not pass a `model`
argument when dispatching it.** See Model policy.

---

## Post-merge cleanup (run after you merge)

This runs **after GATE 2**, once *you* have merged the PR - merging is always your
decision and is never part of the automated `/feature-ship` run. The `/git-cleanup`
command invokes this. Goal: get your local checkout back onto an up-to-date base
branch and remove the now-merged branch (and any worktree), without ever touching
unmerged work.

1. **Confirm the PR is merged.** Resolve the PR (from the argument, or the current
   branch's PR) and read its state and branches:
   `gh pr view <pr> --json state,mergedAt,baseRefName,headRefName`. If it is **not**
   merged, stop and say so - delete nothing.
2. **Update the base branch.** Check out the PR's base - `baseRefName`, i.e. whatever
   the PR was merged into (`develop`, `main`, a release branch, ...), not a hardcoded
   default - and pull: `git checkout <base> && git pull`. Your local base now includes
   the merged change.
3. **Remove the worktree, if the pipeline used one.** Find it with `git worktree
   list`, then `git worktree remove <path>` and `git worktree prune`. You must not be
   standing inside the worktree when you remove it.
4. **Delete the merged local branch.** `git branch -d <headRefName>`. If the PR was
   squash- or rebase-merged, git won't recognize the branch as merged and `-d` will
   refuse - because Step 1 already confirmed the PR is merged, use
   `git branch -D <headRefName>` in that case. Never force-delete a branch whose PR
   you have not confirmed merged.
5. **Prune stale refs.** `git fetch --prune` to drop remote-tracking refs for branches
   GitHub deleted on merge.
6. **Report** what changed: base updated, worktree removed (if any), branch deleted,
   refs pruned. If other local branches exist whose PRs are *also* merged, list them
   and offer to clean those too - but only after confirming each one is merged.

"Clean up any local branches" means the **merged** ones. Only ever delete a branch
whose PR is confirmed merged; leave branches with unmerged work alone.
