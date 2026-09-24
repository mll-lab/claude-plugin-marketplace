# Shapes for content that survived

**This is not a checklist to fill.** Read that again before using anything below.

A template's failure mode is that its headings look like an obligation. Someone sees
`## Commands` and writes commands — and produces exactly the derivable content test 3 deletes.
The original version of this file did prescribe that; it has been rewritten.

Use these only to shape content you have *already established* earns its place. **Never start
from a template.** Start from the three tests and let the surviving content pick its own
headings.

**A short CLAUDE.md is a good CLAUDE.md.** Three sections that each prevent a real error beat
eight that cover every topic. Most repositories need fewer than five.

---

## Sections worth having, when you have the content

Each is worth including *only* when you have content that passed all three tests. The
anti-pattern under each is what the section usually collects instead.

### Gotchas / traps

The highest-value section in most files, and often the only one needed.

```markdown
## Gotchas

- `config.timeout` is seconds; everything else in that file is milliseconds. Upstream
  API requires seconds.
- Tests share one Postgres schema — `--runInBand` is required or they corrupt each other
  and fail under unrelated names.
- `lib/http.ts` is legacy, webhook handlers only. New calls use `lib/api-client.ts`.
```

**Anti-pattern:** "be careful with X" with no failure mode. If you cannot name what goes
wrong, you do not have a gotcha yet.

### Decisions and their reasons

```markdown
## Why it looks wrong

- The address mapper is duplicated in `UserRepository` and `AccountRepository` on purpose —
  they diverged in v3 and sharing it caused a silent data bug (#812).
- `parseDate` reimplements what date-fns does; date-fns drops the timezone we need.
```

Reasons live nowhere in the code and are the most expensive thing to recover — usually a
closed PR discussion or someone's memory. **Anti-pattern:** a changelog. These are only the
decisions that stop the model "fixing" something.

### Ordering and coupling

```markdown
## Load-bearing order

- `crypto.init()` must precede any `auth` import. Import order in `src/bootstrap.ts` is not
  stylistic.
- Migrations and the zod schemas in `src/schemas/` must change in the same commit;
  they are validated against each other at boot.
```

**Anti-pattern:** a dependency graph. Only the edges that break if you get them wrong.

### External systems

```markdown
## Outside this repo

- Staging Postgres is 13, production is 16. `GENERATED ALWAYS` migrations pass
  staging and fail production.
- The payments sandbox rejects amounts over 100000 with a 200 and an empty body.
```

Unavailable at any price by reading this repo. **Anti-pattern:** environment variables that
`.env.example` already lists.

### Conventions a linter cannot express

```markdown
## Conventions

- Domain errors are thrown, never returned. When ambiguous, match the surrounding module.
- New endpoints follow `routes/users.ts`: zod schema, service call, mapped error.
```

Note the second: pointing at an exemplar file beats describing a pattern in prose, and cannot
go stale in the same way. **Anti-pattern:** style rules a formatter enforces — those are
test-2 moves.

### Commands — usually cut, occasionally not

```markdown
## Commands

- `make reset-db` before integration tests; they assume a clean schema and fail
  confusingly otherwise.
```

Include a command **only** when its necessity is invisible from the manifest. A table of
`install` / `dev` / `build` / `test` is the most common waste in real CLAUDE.md files.

**Anti-pattern:**

```markdown
| `npm install` | Install dependencies |
| `npm test` | Run tests |
```

One read of `package.json`. Cut.

### Architecture — usually cut

Include only what the directory tree does not show:

```markdown
## Structure notes

- `src/legacy/` is dead except `src/legacy/tax.ts`, still imported by billing.
- The service boundary is at `src/modules/*/index.ts`; anything deeper is private
  regardless of what TypeScript allows.
```

**Anti-pattern:** a directory listing with each folder's name restated as its description.

---

## Worked example: a whole file that earns its place

A real project needs less than people expect.

```markdown
# Acme API

## Gotchas
- Tests share one Postgres schema; `--runInBand` is required or they corrupt each other.
- `config.timeout` is seconds, everything else ms (upstream API requires seconds).
- `lib/http.ts` is legacy — webhook handlers only. New calls use `lib/api-client.ts`.

## Why it looks wrong
- Address mapper duplicated in `UserRepository`/`AccountRepository` on purpose: they
  diverged in v3 and sharing caused a silent data bug (#812).

## Load-bearing order
- `crypto.init()` before any `auth` import — see `src/bootstrap.ts`.
- Migrations and `src/schemas/` change together; validated against each other at boot.

## Outside this repo
- Staging Postgres 13, production 16. `GENERATED ALWAYS` passes staging, fails production.

## Conventions
- Domain errors thrown, never returned.
- New endpoints follow `routes/users.ts`.
```

Twelve lines. No commands table, no directory map, no tech stack, no generic advice. Every
line names something the model would otherwise get wrong, and none of it is one grep away.

## Monorepos

Claude composes parent-directory files automatically, so **a package file should contain only
what is untrue of the root**. Duplication between levels is pure cost and a reportable
finding.

```markdown
# packages/billing

- Tax rules are per-jurisdiction in `rules/`. Adding a jurisdiction needs a
  fixture in `tests/fixtures/jurisdictions/` or the suite passes vacuously.
```

Nothing about the monorepo, the shared tooling, or the language — the root file has it.

## Placement

The cheapest fix in an audit is moving a line to the right file:

| Content | File |
|---|---|
| True for the team, about this repo | `./CLAUDE.md` (committed) |
| Personal preference, this repo | `./CLAUDE.local.md` (gitignored) |
| True across all your projects | `~/.claude/CLAUDE.md` |
| Only about one package | that package's `CLAUDE.md` |
| Needed by tooling that reads `AGENTS.md` | the nearest `AGENTS.md` covering the code it is about |

**Scope follows the code, at whatever depth the file sits** - every row above means the file
whose directory covers what the line is about, not the one at the repo root.

A personal preference in a committed root file imposes per-turn cost on the whole team. That
is a `RELOCATE`, and it costs nothing to make.

This table is the same one `/revise-ai-instructions` applies at its Step 4 - the audit moves a
line to the right file, the command puts a new one there. **Keep the two in sync**; if they
disagree, this file is the reference.
