# Scoring bands

Six axes, 100 points. The three tests carry 60 of them, so a file cannot score well by being
thorough - only by being *load-bearing*.

Score the file, not your hopes for it. A short file that says four things the model would
otherwise get wrong is an A. A 300-line file covering every section in the template is not.

---

## 1. Counterfactual value - 20 points

*Test 1: would the model get this wrong if it were not written down?*

| Band | Condition |
|---|---|
| **20** | Every line changes behaviour. Nothing generic, nothing restating defaults. You can name the error each line prevents. |
| **15** | One or two lines of generic advice, the rest load-bearing. |
| **10** | A recognisable layer of engineering-platitude content ("write tests", "keep functions small") over a real core. |
| **5** | Mostly advice that would apply unchanged to any repository in any language. |
| **0** | Nothing here is specific to this project. The file could be pasted into an unrelated repo without a single edit. |

**Diagnostic:** try pasting the file into an imagined unrelated project. Every line that
still makes sense there is a line that is not about *this* project.

---

## 2. Right mechanism - 20 points

*Test 2: must we block this? Then it is not prose.*

| Band | Condition |
|---|---|
| **20** | Nothing here should be enforced mechanically. Every rule is a genuine judgment call. |
| **15** | One enforceable rule left as prose, low stakes if violated. |
| **10** | Several enforceable rules as prose, or one with real consequences (secrets, migrations, a protected branch). |
| **5** | The file is largely a list of prohibitions that a hook or linter would enforce deterministically. |
| **0** | It reads as a substitute for CI. The most important rules rely entirely on the model reading and remembering them. |

**Weight by consequence, not count.** One un-enforced "never commit credentials" is a worse
finding than five un-enforced formatting preferences. Score the blast radius.

---

## 3. Derivability - 20 points

*Test 3: can one grep answer it?*

| Band | Condition |
|---|---|
| **20** | Nothing restates what the code plainly shows. No command tables, no directory listings, no tech-stack inventory. |
| **15** | A little overlap - a couple of commands or a short structure note. |
| **10** | A substantial derivable section: a full command table, or a directory map. |
| **5** | Most of the file is a prose rendering of the manifest and the file tree. |
| **0** | It is a worse, staler `ls` and `cat package.json`. |

**Deduct extra for staleness in derivable content.** A restated command is waste; a restated
command that is now *wrong* is actively harmful, because prose in context competes with the
truth in the repo. Weight those cases toward 0 and raise them under Currency as well.

---

## 4. Expensive knowledge captured - 15 points

*Test 3's inverse: is what the code cannot cheaply tell you actually here?*

| Band | Condition |
|---|---|
| **15** | The genuinely costly knowledge is present: cross-module ordering, why-not decisions, external-system quirks, the traps that look like bugs. |
| **10** | Some captured; at least one significant gap you can name. |
| **5** | Gestures at hard-won knowledge but stays too vague to act on ("be careful with the cache"). |
| **0** | None. Everything expensive to learn about this project still lives only in someone's head or in a closed PR. |

This is the axis most files score worst on, and the only axis where the fix is to **add**.
Every point you deduct here should correspond to a `GAP` entry in the report - a deduction
with no gap named is an opinion, not a finding.

---

## 5. Currency - 15 points

| Band | Condition |
|---|---|
| **15** | Everything still true. Paths exist, commands run, described behaviour matches. |
| **10** | Minor drift - a renamed directory, a slightly-off flag. |
| **5** | Several stale references; at least one instruction that would now mislead. |
| **0** | Substantially describes a codebase that no longer exists. |

**Staleness is worse here than in ordinary documentation.** Stale prose in context does not
sit quietly being ignored - it competes with what the model reads in the repo, and can win.
A confidently wrong line is worse than a missing one. Verify by actually checking: does the
path exist, is the script in the manifest, does the module still export that name?

---

## 6. Precision - 10 points

| Band | Condition |
|---|---|
| **10** | Unambiguous. Commands copy-pasteable, paths real, each line saying one thing. |
| **7** | Mostly tight; some wordiness. |
| **4** | Several lines a reader could act on two different ways. |
| **0** | Vague throughout ("follow best practices", "keep things clean"). |

Vagueness is a quiet failure of test 1: a line too vague to act on cannot change behaviour,
so it cannot be preventing an error. If an axis-6 deduction is severe, check whether the line
is really a test-1 cut.

---

## Grades

| Grade | Range | Reading |
|---|---|---|
| **A** | 90-100 | Every line earns its place; expensive knowledge captured |
| **B** | 70-89 | Sound, with identifiable waste or a known gap |
| **C** | 50-69 | Half of it is derivable or generic |
| **D** | 30-49 | Mostly restates the code or lists unenforced rules |
| **F** | 0-29 | Net negative - costs budget every turn and misleads where stale |

**An F is not always a long file.** An empty CLAUDE.md scores 0 on axis 4 and cannot pass
20 for anything else - but it costs nothing per turn and misleads nobody, so it is a cheaper
starting point than a large stale one. Say that explicitly when it is the case: the remedy
for a thin file is additions from test 3's inverse, not a template.

## Assessment procedure

1. Read the CLAUDE.md completely.
2. Read enough of the repo to judge tests 1 and 3 - manifest, directory layout, config files.
   **Scoring without this is guessing.**
3. Verify the checkable claims: paths exist, scripts are in the manifest, names still export.
4. Triage line by line (SKILL.md Phase 2).
5. Score each axis from the verdict distribution - the scores should *follow* the verdicts,
   not precede them.
6. Name every gap behind an axis-4 deduction.

## Red flags

- Command tables and directory maps - the two most common test-3 cuts.
- Advice that would apply to any repository in any language.
- Prohibitions with real consequences left to prose.
- A template's section headings left in place with generic filler underneath.
- The same rule stated in both a root and a package file.
- "TODO" and "TBD" - a line that admits it has no content.
- Rationale-free absolutes ("never use X") - either scar tissue worth keeping and explaining,
  or cargo cult worth cutting. Ask rather than guess.
- A file that has only ever grown. Nothing has been removed because nobody has been asked to.
