---
name: ai-instructions-improver
description: Use when auditing, reviewing, improving, fixing, checking, updating, shrinking, or tightening a project's AI instruction files - CLAUDE.md, CLAUDE.local.md, ~/.claude/CLAUDE.md, AGENTS.md - including when one has grown long, repetitive, or stale, when sessions seem to ignore what it says, when deciding whether a rule belongs in one at all, or when the user mentions CLAUDE.md maintenance or project memory optimization. This is a subtractive audit: it treats every line as context budget spent on every turn, scores the file against fixed axes, gives every line an explicit verdict (keep / cut / move to enforcement / relocate / rewrite), and always reports before changing anything.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# AI instructions improver

**This skill can write to instruction files** - but only after presenting a report and getting
explicit approval. Never edit before the report.

**Which files this covers.** Anything loaded into context on every turn as standing
instructions: `CLAUDE.md` at any level, `CLAUDE.local.md`, `~/.claude/CLAUDE.md`, and
`AGENTS.md` where a repo uses one. The whole argument below rests on *always-loaded* rather
than on a filename, so it applies unchanged to each of them. A README is not in scope - it
costs a reader once, when they choose to open it.

## Why this is subtractive

A CLAUDE.md is not documentation. It is **context budget spent on every turn, forever**:
every line is re-read on every request, in every session, for as long as it exists. A
README costs a reader once when they choose to open it. A CLAUDE.md line costs every
request whether it was relevant or not.

So the governing question is never *"is this true?"* - most of what accumulates in these
files is perfectly true. It is:

> **Does this line change what the model does, and is this the cheapest place to put it?**

Most lines in a mature CLAUDE.md fail that question. They are true, well-intentioned, and
buying nothing. Your job is to find them and say so.

**Corollary - shorter is not the goal.** Cutting a line the model genuinely needs costs far
more than keeping a line it did not. The tests below are not a licence to trim; each one has
an inverse that *protects* a line, and test 3's inverse actively demands new content. A good
audit of a thin file adds more than it removes.

## The three tests

Apply all three to every line. A line survives only by passing all three inverses.

### Test 1 - Counterfactual

> **If this were not written down, would the model get it wrong?**

If it would get it right anyway, the line buys nothing. Cut it.

This catches generic engineering advice ("write tests for new features", "use meaningful
variable names", "handle errors"), restatements of default behaviour ("ask before making
large changes"), politeness and preamble, and anything that reads as a reminder to a
competent colleague rather than a fact about *this* repository.

**Inverse - keep it when:** the model demonstrably would get it wrong. A surprising
constraint, a counter-intuitive convention, a place where the obvious approach is the wrong
one here.

The strongest evidence is a real incident: a line that exists because something actually
went wrong once is usually a keeper. If you cannot construct a plausible way the model errs
without the line, that is your answer.

### Test 2 - Enforcement

> **Must we block this?**

If the rule must *never* be violated, prose is the wrong mechanism. Prose is advisory and
probabilistic - it competes with everything else in the context window and it degrades as
the conversation grows. A hook, a linter rule, a CI check, or a setting is deterministic.

When the answer is yes: **propose the mechanism with concrete config, and remove the line.**
See [references/enforcement-mechanisms.md](references/enforcement-mechanisms.md) for which
mechanism fits which rule, with copy-paste config.

Typical movers: "never commit secrets", "always run the formatter", "don't push to main",
"use pnpm, not npm", "all files end with a newline", "never edit generated files".

**Inverse - keep it as prose when:** it is a judgment call no mechanical check can encode.
"Prefer composition over inheritance in the domain layer" cannot be linted without
absurdity. "Match the error-handling style of the surrounding module" is real guidance and
unmechanisable.

**Do not over-apply this.** Not everything enforceable is worth enforcing. A hook that
blocks a rare, legitimate judgment call is worse than a line of prose, and every mechanism
you add is a thing someone must maintain. `enforcement-mechanisms.md` covers when *not* to
reach for one.

### Test 3 - Derivability

> **Can this be affordably derived by reading the code?**

**Affordable means a grep, or opening a few files.** If the model would find it that
cheaply, cut the line - the code cannot go stale, and the line can.

This catches the bulk of a typical CLAUDE.md: build and test commands (one look at
`package.json`, `Makefile`, `pyproject.toml`, `composer.json`), directory structure (one
`ls`), the tech stack (one look at the lockfile or manifest), which test framework is in use,
what a well-named module does.

**A test-3 cut must name the grep.** Write the actual command or file that answers it -
`package.json scripts`, `grep -r "createClient" src/`. If you cannot name it, you have not
established that it is cheap, and the line stays. This is the discipline that keeps test 3
from becoming "I assume the model will figure it out."

**Inverse - and this half matters more than the cutting.** Knowledge that needs a *thorough*
investigation is **not** affordable, and must be stated explicitly. That means anything
requiring:

- tracing a call chain across several modules to see the actual ordering or coupling,
- reading git history or a PR discussion to learn why something is the way it is,
- running something to find out (which env var is actually required; which of two configs wins),
- knowing about a system *outside* this repository (a staging quirk, an upstream API's
  undocumented behaviour, a deploy-time constraint),
- a decision whose rationale is nowhere in the code - the abandoned approach, the deliberate
  duplication, the thing that looks like a bug and is not.

**This inverse is the only legitimate reason to add content**, and it is why a subtractive
audit still produces additions. Every `GAP` you report comes from here.

## Workflow

### Phase 1 - Discovery

```bash
find . -name "CLAUDE.md" -o -name "CLAUDE.local.md" -o -name "AGENTS.md" 2>/dev/null | head -50
```

Also check `~/.claude/CLAUDE.md` when the audit is about the user's own setup rather than one
repository.

| Type | Location | Purpose |
|------|----------|---------|
| Project root | `./CLAUDE.md` | Primary project context (committed, shared with the team) |
| Local overrides | `./CLAUDE.local.md` | Personal settings (gitignored, not shared) |
| Global defaults | `~/.claude/CLAUDE.md` | User-wide, across all projects |
| Package-specific | `./packages/*/CLAUDE.md` | Module-level context in monorepos |
| Subdirectory | any nested location | Feature or domain-specific context |
| Other agents | `./AGENTS.md` | Standing instructions for non-Claude tooling |

`AGENTS.md` earns one extra check before you cut from it: confirm something in this repo
actually reads it. If nothing does, the whole file is dead weight and that is the finding -
do not triage it line by line.

Claude auto-discovers CLAUDE.md files in parent directories, so monorepo setups compose
automatically - which means **duplication across levels is a real finding**. A line in a
package file that the root file already states is pure cost.

**Read the repository too, not just the file.** You cannot apply test 3 without knowing what
the code makes obvious, and you cannot apply test 1 without knowing the conventions. Look at
the manifest, the directory layout, and the config files before judging a single line.

**And run what the file claims works.** Reading is not enough for the Currency axis: a
documented command can be confidently wrong in a way no amount of reading reveals.

Start with the documented install command — it is a claim in the file too, so if it fails,
that is a stale line to report. Install means the command the file documents, not improvising
toward a working environment: if `npm ci` fails, that is the finding, not a cue to try
`npm install`, then `yarn`, then deleting the lockfile. Where setup needs something you cannot
create, such as real credentials or a running service, skip those commands and say so rather
than scoring the file on failures the missing setup caused.

Then execute the build, test, and lint commands the file asserts, and **read the failure rather
than the exit code**: a command that cannot be found, or whose documented flags are rejected, is
a stale line to cut. A command that runs and reports a failing project is not a currency
finding — the line is right and the repo is red. In testing, running `npm test` was what
revealed a documented `--runInBand` flag that made the test runner crash on startup; an audit
that only read `package.json` recommended keeping it.

Do not run anything destructive, anything that writes outside the working tree, or anything
that touches a real environment. Build, test, lint, typecheck — not deploy, migrate, or seed.

### Phase 2 - Line-by-line triage

Every **claim** gets exactly one verdict. Consecutive lines sharing a verdict may be grouped;
**no line may be skipped.**

Usually one line is one claim. When a single line packs two separable claims that fail
*different* tests, split it and give each its own verdict, citing the line number twice —
"TypeScript project built with React 18. We follow modern best practices." is a test-3 cut and
a test-1 cut in one sentence. Do not force it into one verdict: picking the dominant one
buries a true reason, and the user is reading these to decide whether to trust you.

| Verdict | Meaning |
|---|---|
| `KEEP` | Passes all three inverses. Say which one earns it. |
| `CUT (test 1)` | The model gets this right without being told. |
| `MOVE (test 2)` | Belongs in a hook / linter / CI check / setting. Include the config. |
| `RELOCATE` | Right content, wrong file. Name the destination file. |
| `CUT (test 3)` | One grep answers it. **Name the grep.** |
| `REWRITE` | The content earns its place; the wording does not - too vague, too long, ambiguous, or stale. Give the replacement line. |
| `GAP` | Not a line in the file: expensive-to-derive knowledge that is missing (test 3's inverse). |

Headings and structural lines follow their section: if everything under `## Commands` is cut,
the heading goes too.

When a line fails more than one test, report the **first** it fails, in order 1 → 2 → 3. The
order is deliberate: a line the model would get right anyway does not need a hook built for
it, and there is no point naming a grep for a line that should not exist either way.

### Phase 3 - Report

**Always output the report before making any change.**

```
## CLAUDE.md Audit

### Summary
- Files audited: X
- Lines: X kept · X cut · X moved to enforcement · X relocated · X rewritten · X gaps found
- Estimated reduction: X lines (X%)

### ./CLAUDE.md
**Score: XX/100 (Grade: X)**

| Axis | Score | Notes |
|------|-------|-------|
| Counterfactual value | X/20 | ... |
| Right mechanism | X/20 | ... |
| Derivability | X/20 | ... |
| Expensive knowledge captured | X/15 | ... |
| Currency | X/15 | ... |
| Precision | X/10 | ... |

#### Verdicts

| Line(s) | Content | Verdict | Reason |
|---|---|---|---|
| 12 | "Always write tests for new code" | CUT (test 1) | Model does this by default; no project specifics |
| 18-24 | `## Commands` table | CUT (test 3) | `package.json` scripts - one read |
| 31 | "Never commit .env" | MOVE (test 2) | Must be blocked, not suggested - see config below |
| 40 | "Migrations are irreversible in prod" | KEEP | Model would get this wrong; not in the code |
| 44 | "I prefer terse commit messages" | RELOCATE | Personal preference in a committed file - to `./CLAUDE.local.md` |

#### Proposed enforcement (from `MOVE (test 2)` verdicts)
[concrete config per moved rule]

#### Gaps - expensive knowledge that should be here
[each with why deriving it is not affordable]
```

See [references/quality-criteria.md](references/quality-criteria.md) for the scoring bands
behind each axis.

### Phase 4 - Approval gate

Present the report, then **stop and ask**. Never apply anything before an explicit yes.

If the audit proposes cutting a lot, say so plainly and invite the user to veto individual
lines - a line may be load-bearing for a reason nobody wrote down, and they are the only one
who knows. **A veto is information, not an obstacle:** if they keep a line you cut, ask why,
and consider whether the real answer is a `REWRITE` that makes the reason explicit.

### Phase 5 - Apply

Apply approved changes with Edit, preserving surrounding structure. Enforcement configs from
test 2 are **proposed, not installed** - print them for the user to wire up. Do not create
hook scripts, edit CI workflows, or touch settings as part of an audit.

Report what changed, and restate any gaps the user did not fill so they are not lost.

## Rationalizations - STOP if you catch yourself here

Two opposite failures. Under pressure to show results you over-cut; under discomfort at
deleting someone's work you under-cut. Both are failures.

| Rationalization | Reality |
|---|---|
| "The file is too long, this can go" | Length is not a verdict. Every cut cites a test, or it is not a cut. |
| "The model can probably figure this out" | Then name the grep. If you cannot, you have not shown it is cheap - the line stays. |
| "It's obviously generic advice" | Check it is not this project's *exception* to a general rule. "Write tests" is generic; "write tests even for the generated clients, they drift" is not. |
| "I don't know what this line is for, and it looks useless" | Unexplained lines are often scar tissue from a real incident. That is a question for the user, never a cut. |
| "This is a nice section heading, keep it for structure" | A heading over cut content is cut content. Structure is not value. |
| "I'll just apply the obvious ones and report the rest" | Report before writing. Always. There is no tier of change too obvious for the gate. |
| "They kept a line I cut, so I was wrong to propose it" | A veto is information. Ask why, then consider whether the answer should become a REWRITE that records the reason. |
| "Adding is not my job here, this is a subtractive skill" | Test 3's inverse demands additions. An audit that found no gaps probably did not read the code. |
| "It scored well, so there's nothing to do" | The score follows the verdicts, not the reverse. If you scored before triaging, start again. |

## Guardrails

- **Report before writing. Always.** No exceptions, no "this one is obvious".
- **The reference files' examples are illustrations, not findings.** They are deliberately
  vivid and specific — a `config.timeout` in seconds, a staging/production Postgres mismatch,
  a legacy HTTP client — which makes them easy to recognise and dangerously easy to *import*.
  A repo that superficially resembles one does not thereby contain its facts. Before reusing
  any specific claim from an example, verify it here: is there really a second config field
  with different units, is there really evidence of two database versions? In testing, a
  fixture that happened to resemble these examples produced measurable pull toward asserting a
  version mismatch for which the repo held no evidence at all. **A GAP you cannot point at
  evidence for is invention, which is worse than an omission** - the user cannot tell the
  difference and will act on it.
- **Never cut a line you do not understand.** If you cannot tell what a line is for, that is
  a question for the user, not a cut. Unexplained lines are often scar tissue from a real
  incident.
- **Do not cut for length.** Every cut cites a test. "The file is long" is not a reason.
- **A test-3 cut names its grep.** No named grep, no cut.
- **Preserve the user's voice** in lines that survive. This is their file.
- **One concept per line.** Prefer a dense line to a paragraph, but do not compress two
  unrelated facts into one line to shorten the count.
- **`CLAUDE.local.md` for personal preference**, root `CLAUDE.md` for the team, and
  `~/.claude/CLAUDE.md` for anything true across all the user's projects. A line in the wrong
  one of those three is a `RELOCATE`, and the cheapest fix in the whole audit.

## References

- [references/quality-criteria.md](references/quality-criteria.md) - scoring bands per axis
- [references/enforcement-mechanisms.md](references/enforcement-mechanisms.md) - test 2:
  choosing and configuring a mechanism
- [references/triage-guidance.md](references/triage-guidance.md) - worked examples of what
  earns its place and what does not
- [references/templates.md](references/templates.md) - shapes for content that survived.
  **Not a checklist to fill.**
