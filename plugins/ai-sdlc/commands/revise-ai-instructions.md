---
description: Capture what this session taught into the right AI instruction file - redacted first, then gated by the three subtractive tests, so it adds only what earns its place and never writes session secrets into a committed file.
argument-hint: [path-to-instruction-file | defaults to discovering them]
allowed-tools: Read, Edit, Write, Glob, Grep, Bash(git:*), Bash(find:*)
---

Capture the durable learnings from **this session** into the right instruction file.

This is the additive counterpart to the `ai-sdlc:ai-instructions-improver` skill, and it is
held to that skill's standard: **most candidate additions do not earn their place.** A line
added here costs every turn of every future session, forever. Read the skill's "three tests"
section before proposing anything, and apply them as an admission gate rather than as a
post-hoc review.

Target file: **$ARGUMENTS** (if none given, discover the candidates as in Phase 1 of the
skill, and choose per addition).

## Step 1 - Reflect on this session only

What did *this* session surface that a future session would get wrong unprompted? Draw on what
actually happened, not on what would make a tidy document:

- A command, flag, or path that turned out to be wrong, or right in a non-obvious way.
- A convention this repo follows that you initially got wrong.
- An environment or configuration quirk that cost real time to discover.
- A constraint that only became visible when something failed.
- A decision whose rationale is nowhere in the code - the approach abandoned and why.

**If nothing in the session meets that bar, say so and stop.** A session that taught nothing
durable is the normal case, not a failure, and inventing an addition to fill this command is
the single worst outcome it can produce.

## Step 2 - Redact before you propose

A session transcript is not a safe source for a committed file. Everything below came out of a
live session that may have touched real credentials, real data, and real infrastructure, and
what this command writes to `CLAUDE.md` or `AGENTS.md` is **permanent, shared, and in git
history** the moment it lands.

So before a candidate is even eligible for the three tests, strip it of:

- credentials of any kind - tokens, keys, passwords, connection strings, session cookies;
- personal or customer data, and customer or client names;
- internal hostnames, private URLs, IPs, bucket names, account and project ids;
- verbatim session output, which is where these hide. Never paste a log line, a stack trace,
  or a command's output into an instruction file.

**Keep the shape, drop the value.** The durable lesson is almost never the secret itself. "The
staging API needs the `X-Tenant` header or it 403s with a misleading `invalid_grant`" is the
learning; the actual tenant id and token are not, and including them buys nothing. If a
candidate cannot survive having its values removed, it was a session detail rather than a
durable rule - drop it.

**If you are unsure whether a value is sensitive, treat it as sensitive** and either
generalise it or raise it with the user. This gate is not covered by secret scanning: the
repo's `gitleaks` pre-commit hook catches recognised token patterns, not a customer name, an
internal hostname, or a leaked path - and only when pre-commit is actually installed.

Say explicitly in the Step 5 report that you applied this gate, and name anything you
generalised, so the user can check your judgement rather than assume it.

## Step 3 - Put every candidate through the three tests

Each candidate needs all three, and the order matters:

1. **Counterfactual.** If this were not written down, would the model get it wrong? If it
   would get it right anyway, **drop it.** "Run the tests before committing" does not survive
   this. "The integration tests need the docker compose stack up first, and fail with a
   misleading auth error if it is not" does.
2. **Enforcement.** Must this be *blocked* rather than suggested? Then it is a hook, a linter
   rule, CI, or a setting - **not a line here.** Propose the mechanism and its config instead,
   and say plainly that prose would only ask. A `PreToolUse` hook must exit **2** to block;
   any other non-zero exit is a non-blocking error and the call proceeds.
3. **Derivability.** Can one grep or one file read answer it? Then **drop it** and name the
   grep. The inverse is the one that earns additions: knowledge that is *expensive* to
   derive - spread across many files, or absent from the repo entirely (a production
   constraint, an external system's undocumented behaviour, a rationale that lives only in
   someone's head).

State the surviving reason for each addition. An addition with no stated reason does not go in.

## Step 4 - Choose the file

| Content | File |
|---|---|
| True for the team, about this repo | `./CLAUDE.md` (committed) |
| Personal preference, this repo | `./CLAUDE.local.md` (gitignored) |
| True across all your projects | `~/.claude/CLAUDE.md` |
| Only about one package | that package's `CLAUDE.md` |
| Needed by tooling that reads `AGENTS.md` | the nearest `AGENTS.md` covering the code it is about - the package's own if there is one, else the root's |

**Pick by which agent needs the line, not by which file you found first.** Step 1 discovers
`AGENTS.md` as well, so a learning can be about tooling that never reads a `CLAUDE.md`. Confirm
what actually loads the repo's `AGENTS.md` before writing there - if nothing does, that is the
finding, and the file is out of scope rather than a destination. If both readers need the line,
state it once in whichever file they both load rather than copying it into two: a duplicated
line pays its per-turn cost twice and the copies drift apart.

**Scope follows the code, at whatever depth the file sits.** Discovery finds `CLAUDE.md` and
`AGENTS.md` anywhere in the tree, so both columns above mean "the one whose directory covers
what the line is about", not "the one at the repo root". A learning about one package written
into a root file charges every session in every other package for it; the same learning written
into a package nobody touches is invisible. If the right directory has no such file yet, say so
and propose creating it rather than defaulting to the root.

`CLAUDE.local.md` is the filename Claude Code loads for local scope - **not** `.claude.local.md`,
which nothing reads. If you write a personal preference into the dotted spelling it will
silently never apply. Add `CLAUDE.local.md` to `.gitignore` if it is not there already.

Before writing to a committed file, check the line is not already stated at another level: a
parent `CLAUDE.md` composes with this one, so a duplicate is pure cost.

## Step 5 - Report before writing

**Always show the proposal and stop for approval.** Never edit first.

```
## Proposed additions from this session

### <the destination file's actual path, e.g. ./packages/api/CLAUDE.md or ./AGENTS.md>
**Why:** [which test's inverse earns it, in one line]
+ [the line, one concept, as short as it can be while staying unambiguous]

### Better enforced than written
[rule] -> [mechanism + concrete config]

### Considered and dropped
| Candidate | Dropped on |
|---|---|
| ... | test 1 - model gets this right unprompted |

### Redaction
[what was generalised, or "nothing sensitive in scope"]
```

**One section per destination file, headed by its real path** - repeat it as many times as
there are targets, and never merge two files' additions under one heading. Step 4 can route a
single session's learnings to a package `CLAUDE.md`, a root `AGENTS.md`, and `~/.claude/CLAUDE.md`
at once, and the user is approving *where* each line lands as much as what it says.

Show the dropped candidates too. They are evidence you applied the gate rather than
transcribing the session, and they let the user overrule a specific call.

## Step 6 - Apply what is approved

Edit only the approved lines, preserving surrounding structure and the user's voice. Create
the file if it does not exist. Print the enforcement configs for the user to wire up - **do
not** install hooks, edit CI, or touch settings from this command.

Then report what changed, and restate anything approved-in-principle that you could not place.

## If the file is already bloated

This command only adds. If the target file is visibly full of lines that would fail the three
tests, say so and recommend `ai-sdlc:ai-instructions-improver` - adding a good line to a file
nobody reads carefully is a poor trade, and the audit will surface far more budget than this
command can.
