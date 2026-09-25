# Triage guidance — worked examples

What earns a permanent place in context, and what does not.

> Adapted from `claude-md-management:claude-md-improver`'s update guidelines
> (<https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-md-management>,
> Apache License 2.0 © Anthropic — see
> <https://github.com/anthropics/claude-plugins-official/blob/main/plugins/claude-md-management/LICENSE>),
> re-aimed around the three tests: several of its original "what to add" examples are things
> test 3 now cuts, and are corrected here.

**The core principle is unchanged and worth restating:** the context window is precious, and
every line must earn its place. What changed is the standard of proof.

---

## What earns its place

Each of these survives because the model cannot get it cheaply or correctly any other way.

### 1. Ordering and coupling that spans modules

```markdown
`auth` requires `crypto.init()` to have run first. Import order in
`src/bootstrap.ts` is load-bearing, not stylistic.
```

**Why it survives test 3:** deriving this means reading `bootstrap.ts`, following both
modules, and noticing that a re-order breaks at runtime rather than at compile time. That is
not one grep. And the code actively misleads — the imports look reorderable.

### 2. Rationale that exists nowhere in the code

```markdown
`UserRepository` and `AccountRepository` duplicate the address mapper on purpose —
they diverged in v3 and the shared version caused a silent data bug (#812).
Do not refactor them together.
```

**Why it survives:** the code shows duplication and nothing else. Every instinct — and every
code-quality tool — says deduplicate. Without this line the model confidently causes the same
bug. The strongest possible keeper: a real incident, named.

### 3. Facts about systems outside this repository

```markdown
Staging's Postgres is 13; production is 16. Generated migrations using
`GENERATED ALWAYS` pass staging and fail production.
```

**Why it survives:** no amount of reading this repo reveals it. Unavailable at any price
locally.

### 4. Traps that look like bugs

```markdown
`config.timeout` is in seconds. Everything else in that file is milliseconds.
Deliberate — the upstream API specifies seconds.
```

**Why it survives:** the model will "fix" this inconsistency. A comment at the definition
would be better still — suggest that, and if it is added, the line can go.

### 5. Which of several plausible paths is the live one

```markdown
Two HTTP clients exist. `lib/http.ts` is legacy, kept for the webhook
handlers only. All new calls go through `lib/api-client.ts`.
```

**Why it survives:** grep finds both and cannot tell you which is current. Distinguishing
them means reading call sites and git history.

### 6. Judgment calls a check cannot encode

```markdown
Domain errors are thrown, never returned. Match the surrounding module
when it is ambiguous.
```

**Why it survives test 2:** "match the surrounding module" is unmechanisable. The first half
could be linted, the second cannot, and splitting them would lose the point.

---

## What does not earn its place

### 1. Generic engineering advice — test 1

```markdown
Always write tests for new features.
Use meaningful variable names.
Handle errors appropriately.
Keep functions small and focused.
```

The model does all of this by default. **Diagnostic:** these lines would apply unchanged to
any repository in any language, which means they say nothing about this one.

### 2. Commands — test 3

```markdown
## Commands

| Command | Description |
|---------|-------------|
| `npm install` | Install dependencies |
| `npm run dev` | Start dev server |
| `npm test` | Run tests |
```

**One read of `package.json` scripts.** This is the single most common block of waste in real
CLAUDE.md files, and the original guidance actively recommended adding it.

*Note: this corrects the source material.* `claude-md-improver`'s first "What TO Add" example
was exactly this — `npm run build:prod` with the reasoning "saves future sessions from
discovering these again". It does not: discovering it costs one file read, and the line costs
every turn forever, with a staleness risk the manifest does not have.

**The exception that does survive:** a command whose *existence* is not inferable, or whose
necessity is invisible.

```markdown
Tests need `--runInBand`; they share one Postgres schema and corrupt
each other in parallel.
```

`package.json` shows the flag. It does not show that removing it produces flaky failures
attributed to the wrong test. Keep the *why*, cut the *what*.

### 3. Directory structure — test 3

```markdown
## Architecture

- `src/` — source code
- `src/components/` — React components
- `tests/` — test files
```

One `ls`. Directory names already say this. **What would survive** is structure you cannot
see: which directory is dead, which two must change together, where the boundary actually is
versus where the folders imply it.

### 4. Tech stack inventory — test 3

```markdown
Built with React 18, TypeScript, Vite, Tailwind, and Vitest.
```

The lockfile is authoritative and never stale. This line is stale the day a version bumps.

### 5. What a well-named symbol does — test 3

```markdown
The `UserService` class handles user operations.
```

The name said it. Zero information added.

### 6. Enforceable prohibitions — test 2

```markdown
- Never commit .env files
- Always run prettier before committing
- Don't push directly to main
```

Each must be *blocked*, not suggested. See
[enforcement-mechanisms.md](enforcement-mechanisms.md).

### 7. One-off history — test 1

```markdown
Fixed a bug in commit abc123 where the login button didn't work.
```

Will not recur; changes no future decision. Contrast example 2 above, where the incident is
load-bearing *because* it tells the model not to do something it would otherwise do.

### 8. Verbose explanation of standard technology — tests 1 and 3

Instead of a paragraph explaining what JWT is:

```markdown
Auth: JWT, HS256, `Authorization: Bearer <token>`.
```

And if that is all derivable from the auth middleware, cut it entirely. Keep only the part
that surprises:

```markdown
Tokens carry `org_id`, and the tenant middleware trusts it without
re-checking. Never mint a token outside `auth/issue.ts`.
```

---

## Rewriting rather than cutting

A line often contains something real, wrapped in something worthless. `REWRITE` is usually
better than `CUT`.

| Before | After | What changed |
|---|---|---|
| "Be careful with the cache" | "Cache keys include the locale. Changing the key format requires a flush or users see another locale's content." | Vague → the actual failure mode |
| "We use a monorepo with pnpm workspaces" | *(cut — one look at `pnpm-workspace.yaml`)* | Nothing was load-bearing |
| "Follow the existing patterns in the codebase" | "New endpoints follow `routes/users.ts`: zod schema, service call, mapped error." | Unactionable → a named exemplar |
| "Don't break the build" | *(move to CI)* | Enforcement, not prose |
| "The API is versioned" | "API version lives in the path (`/v2/...`), not a header. v1 is still served for two clients — see `LEGACY_CLIENTS` in `config/api.ts`." | True but useless → the non-obvious half |

The pattern: **keep the surprise, cut the summary.** A line earns its place through the part a
competent reader of this codebase would not have predicted.

---

## Validation checklist

Before finalising any proposed change:

- [ ] Every verdict cites a test, or an inverse for a `KEEP`
- [ ] Every `CUT (test 3)` names the grep or file that answers it
- [ ] Every `MOVE (test 2)` carries concrete config, not just a mechanism name
- [ ] Every `RELOCATE` names the destination file
- [ ] Every `GAP` explains why deriving it is *not* affordable
- [ ] No line cut merely for length
- [ ] No line cut that you could not explain the purpose of
- [ ] Claims in surviving lines were actually verified — paths exist, commands run
- [ ] Duplication across root and package files reported
- [ ] Surviving lines keep the user's voice
