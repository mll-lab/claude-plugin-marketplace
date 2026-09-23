# Test 2 — moving a rule out of prose

When a rule *must not* be violated, prose is the wrong place for it. Prose is advisory: it
competes with everything else in the context window, and its influence decays as a
conversation grows. A mechanism either fires or it does not.

This file is the other half of test 2. Having decided a line should move, you still owe the
user a concrete config — a `MOVE` verdict that says only "this should be a hook" has handed
them the research you were well-placed to do.

## Choosing the mechanism

Work down this list and stop at the first that fits. Earlier options are cheaper, run sooner,
and fail more clearly.

| # | Mechanism | Use when | Fires |
|---|---|---|---|
| 1 | **A setting** | The behaviour is already configurable — a permission, a default, a toggle | Always, invisibly |
| 2 | **A linter / formatter rule** | The rule is about code shape and a tool already parses that language | On save, on lint, in CI |
| 3 | **A pre-commit hook** | The rule is about what may enter a commit, across file types | On `git commit` |
| 4 | **A Claude Code hook** | The rule is about what the *agent* may do, not what the code looks like | On the tool call, before it runs |
| 5 | **A CI check** | Verification needs the full project — a build, the test suite, a cross-file invariant | On push / PR |

Two distinctions people get wrong:

**Linter vs pre-commit hook.** A linter rule is better when the language has a tool for it:
it gives an inline editor error and a precise message. Reach for a pre-commit hook when the
rule spans file types or has no linter (secrets, file naming, "don't commit this directory").

**Pre-commit hook vs Claude Code hook.** These catch different things at different times. A
pre-commit hook catches a bad commit. A Claude Code hook catches a bad *action* — reading a
secret, editing a generated file, running a destructive command — before it happens, which
is the only option when the damage is not a commit at all. If the rule is "the agent must
never do X", it is a Claude Code hook; if it is "X must never land in the repo", it is
pre-commit or CI.

For settings and Claude Code hooks, the **`update-config`** skill owns the file format and
the merge semantics of `settings.json`. Point the user at it rather than hand-writing JSON
you have not verified.

## Config patterns

Adapt these — do not paste blind. Check what the repo already uses first: a repo with
`.pre-commit-config.yaml` should get another hook there, not a new mechanism.

### A setting

```json
// .claude/settings.json
{
  "permissions": {
    "deny": ["Read(./.env)", "Read(./.env.*)", "Read(./secrets/**)"]
  }
}
```

Replaces: *"never read or print the contents of .env"*. A deny rule is unarguable; the line
was not.

### A linter rule

```jsonc
// .eslintrc.json
{
  "rules": {
    "no-restricted-imports": ["error", {
      "patterns": [{
        "group": ["../domain/*"],
        "message": "Import domain types via the barrel at domain/index.ts."
      }]
    }]
  }
}
```

Replaces: *"always import domain types through the barrel"*. The rule now names itself at the
point of violation, with the reason attached.

### A pre-commit hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.30.1
    hooks:
      - id: gitleaks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks:
      - id: end-of-file-fixer
      - id: no-commit-to-branch
        args: [--branch, main, --branch, master]
```

Replaces three lines at once: *"never commit secrets"*, *"files end with a newline"*, *"don't
commit directly to main"*. Formatting rules are the best value here — a formatter hook
deletes every style line in the file.

### A Claude Code hook

```json
// .claude/settings.json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "python3 .claude/hooks/block-generated-edits.py",
        "statusMessage": "Checking for generated files"
      }]
    }]
  }
}
```

Replaces: *"never edit files under `generated/` — regenerate instead"*. The hook exits **2**
with an explanation on stderr, which blocks the call and hands the message to the agent so it
re-issues correctly. Any other non-zero exit is a non-blocking error — the edit proceeds.
Prose could only ask.

See `update-config` for the full hook schema and event list.

### A CI check

```yaml
# .github/workflows/ci.yml
- name: Verify no circular dependencies
  run: npx madge --circular src/
```

Replaces: *"avoid circular imports"* — an invariant only visible with the whole module graph,
so nothing earlier in the list can see it.

## When *not* to move a rule

A mechanism is not free. Someone maintains it, it runs on every commit or every tool call,
and a wrong one blocks legitimate work — the worst outcome in this whole skill, because a
false block is a hard stop rather than an ignored suggestion.

**Leave it as prose when:**

- **It is a judgment call.** "Match the error-handling style of the surrounding module" is
  real guidance and unmechanisable. Anything needing taste stays prose.
- **It has legitimate exceptions.** If the right answer is "usually X, but sometimes Y for a
  good reason", a check that blocks Y will be bypassed, and a habitually bypassed check is
  worse than none — it trains people to add `--no-verify`.
- **The consequence is trivial.** A preference about import ordering that nothing depends on
  does not justify a tool. Cut it under test 1 instead, or leave it.
- **The repo has no such infrastructure and this one rule does not justify starting.** Adding
  pre-commit to a repo that has never had it, for a single low-stakes rule, is a bigger change
  than the audit was asked for. Say so, and note it as a suggestion rather than a `MOVE`.

**A warning is not enforcement.** A linter rule set to `warn` leaves the rule advisory — the
same failure as prose, with added maintenance. If it is worth moving, set it to `error`. If
`error` is too strong, the rule has exceptions, and it belongs in prose.

## Reporting a MOVE

Each one gets:

1. **The line** being removed, quoted.
2. **Which mechanism** and — briefly — why that one rather than an earlier or later option.
3. **The config**, copy-paste ready, matching what the repo already uses.
4. **What the user must do to wire it up** — install the tool, add the workflow step, run
   `pre-commit install`. This skill proposes; it does not install.

Example:

> **Line 31:** `- Never commit .env files`
> **→ pre-commit hook.** A Claude Code hook would only constrain the agent; this must hold
> for every human commit too. The repo already has `.pre-commit-config.yaml`, so this is one
> added entry.
>
> ```yaml
>   - repo: https://github.com/gitleaks/gitleaks
>     rev: v8.30.1
>     hooks:
>       - id: gitleaks
> ```
>
> **To wire up:** add the entry, then `pre-commit install` if hooks are not installed yet.

If a single mechanism absorbs several lines — one formatter hook retiring six style rules —
report it once and list every line it retires. That is the highest-value finding an audit can
produce: several lines of permanent per-turn cost replaced by one deterministic check.
