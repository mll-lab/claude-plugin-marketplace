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
- **Say the comment budget out loud in every dispatch.** A subagent loads the
  repository's `CLAUDE.md`, but superpowers' `implementer-prompt.md` says nothing about
  comments and does tell it to "improve code you're touching the way a good developer
  would". Comment density is therefore the convention that reliably gets lost. Put the
  budget in the dispatch itself (Stage 4), not only in the repository's files.

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

Invoke **`superpowers:brainstorming`** with the intake summary as the seed. Let it
run its Socratic process and produce the design document / spec. Do not skip its
questions - answer from the Jira context where you can, and surface to the human
any question you cannot answer confidently.

Output of this stage: a saved spec/design document.

## Stage 2 - Adversarial challenge

1. Dispatch the **`spec-challenger`** subagent (Opus) with the spec document as
   input. It returns a structured critique with severity-tagged findings
   (BLOCKER / MAJOR / MINOR / QUESTION) and an overall verdict.
2. Triage the critique:
   - **Justified findings** -> fold the fix into the spec. Edit the spec document
     in place.
   - **Unjustified or out-of-scope findings** -> note them with a one-line reason
     for not acting, so the human can see what was considered and rejected.
3. Produce a short changelog: what the challenge surfaced and what you changed.

### >>> GATE 1: spec approval <<<

Present: (a) the revised spec, (b) the challenger's verdict, (c) your changelog of
folded-in vs rejected findings. Then **STOP** and ask the user to approve, request
further changes, or re-run the challenge (`/spec-challenge`). Do not proceed to
planning until they approve.

## Stage 3 - Implementation plan

Once the spec is approved, invoke **`superpowers:writing-plans`** on the approved
spec. It breaks the design into small, verifiable tasks with exact file paths and
verification steps.

Output: a saved implementation plan. Briefly report the task count and the files it
expects to touch - this feeds the complexity decision next.

## Stage 4 - Implementation

Decide the execution mode from the plan's complexity:

- **Default - subagent-driven.** Use **`superpowers:subagent-driven-development`**.
  Choose this unless the change is clearly trivial.
- **Inline (rare).** Use **`superpowers:executing-plans`** only when the change is
  genuinely small: roughly 1-2 tasks, a single file or tightly scoped area, no new
  abstractions, no cross-cutting concerns.

State which mode you chose and the one-line reason. If it is a borderline call,
ask before starting. Let the chosen superpowers skill drive TDD and per-task review.

### The comment budget in a dispatch

`superpowers:subagent-driven-development` assembles each implementer prompt from
`implementer-prompt.md`. That template has no comment guidance, and it caps the
subagent's reply at 15 lines. So two things belong in the dispatch you write:

- **In the prompt's `## Context` section**, state the budget: no comments by default. A
  comment earns its place only by stating a constraint a future editor would otherwise
  violate - not by restating the adjacent line, repeating what the name or the raise site
  already says, or recording why it refactored. A docstring only where the signature does
  not already convey the behaviour.
- **In the report file, never the short reply**, ask for every comment it kept with a
  one-line justification. The 15-line cap has no room for a list, and a comment that must
  be defended in writing does not get written reflexively.

**Before a fan-out, write the shared rationale yourself.** Parallel implementers cannot
see each other, so each restates the reason its siblings need too - on one branch a
single 8-line explanation reached nine sites that way. Put it in the shared helper or
error class before dispatching, name that path in every brief, and say not to restate it.
No brief can fix this after the fact.

When implementation completes, run a final sanity check: tests pass, the diff
matches the plan, no stray debug code, comment density inside the budget.

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

**One push per round, and two places the human gets asked.** Each round finishes every
thread before a single push - never one thread at a time. The loop otherwise runs
unattended, with two exceptions: if a *human* has commented on the PR (Copilot's thread
fetch filters those out, so the skill looks for them separately), it asks them to add
everything they want before pushing that round; and before the loop reports, it asks
whether they have manual adjustments they want in before the PR is finalized. Both exist
to collect a batch rather than push a commit per request.

### >>> GATE 2: loop exit <<<

When the loop ends, **STOP** and report: rounds used, what was changed (including
anything the user asked for when the skill offered them the pre-finalize pass), which
threads were pushed back on and why, and any items still open (only possible if the
5-round cap was hit). Let the user decide whether to merge or continue manually.

---

## Quick reference

| Stage | Skill / agent invoked | Gate |
|-------|-----------------------|------|
| 0 Intake | Jira MCP | - |
| 1 Spec | `superpowers:brainstorming` | - |
| 2 Challenge | `spec-challenger` (Opus subagent) | GATE 1: spec approval |
| 3 Plan | `superpowers:writing-plans` | - |
| 4 Implement | `superpowers:subagent-driven-development` (or `:executing-plans`) | - |
| 5 PR | `gh pr create` | - |
| 6 Review loop | `ai-sdlc:copilot-loop` | GATE 2: loop exit |

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
