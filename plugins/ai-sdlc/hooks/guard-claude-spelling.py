#!/usr/bin/env python
"""Block tool calls whose paths contain a misspelling of the .claude config dir.

Reads a PreToolUse hook payload on stdin. If a Write / Edit / MultiEdit /
NotebookEdit / Bash call references a path segment that is a near-miss of
".claude" (e.g. .claire, .cluade, .claud, .calude), exit 2 to block the call and
explain on stderr; the agent then re-issues it with the correct spelling.

Detection is edit-distance based (1-2 edits from "claude"), so it catches typos
without a hard-coded list, while leaving legitimate dot-dirs alone (.clang-format,
.clangd, .clojure, .github, .cache all stay >2 edits away).

For Bash, to avoid blocking a command that merely *mentions* the typo in a string
or comment, a token is only inspected when it is genuinely path-like:
  - it contains a path separator (e.g. `.claire/worktrees/...`), OR
  - it is the bare target of a directory/path-creating command
    (`mkdir .claire`, `cd .claire`, `rmdir`/`pushd`/`touch`/`mkfifo`), OR
  - it is a redirect target (`> .claire`).

Fails OPEN: any malformed input or internal error exits 0 (allow), so a bug here
can never wedge real work. It only ever blocks on a positive misspelling match.
"""
import sys
import json
import re

TARGET = "claude"                 # compared against the segment minus its leading dot
ALLOW = {".claude", ".clause"}    # exact dot-segments that are never flagged

# Commands that create/enter a path given a bare (slash-free) argument.
_DIR_CMDS = r"mkdir|rmdir|cd|pushd|touch|mkfifo"
_NOT_TOKEN = r"""[^\s'"`;|&<>]"""  # chars that can't appear in a shell path token
_DIR_CMD_TARGET = re.compile(
    r"(?:^|[\n;&|])\s*(?:" + _DIR_CMDS + r")\b(?:\s+-{1,2}\S+)*\s+(" + _NOT_TOKEN + r"+)"
)
_REDIRECT_TARGET = re.compile(r"(?:>>?|<)\s*(" + _NOT_TOKEN + r"+)")


def lev(a, b):
    """Levenshtein edit distance between two short strings."""
    if a == b:
        return 0
    lb = len(b)
    prev = list(range(lb + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * lb
        for j, cb in enumerate(b, 1):
            cost = 0 if ca == cb else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
        prev = cur
    return prev[lb]


def is_typo(segment):
    s = segment.lower()
    if not s.startswith(".") or s in ALLOW:
        return False
    core = s[1:]
    if abs(len(core) - len(TARGET)) > 2:   # too different in length to be a typo
        return False
    return 1 <= lev(core, TARGET) <= 2


def path_segments(path):
    return [p for p in re.split(r"[/\\]+", path) if p]


def candidate_paths(tool_name, tool_input):
    paths = []
    for key in ("file_path", "notebook_path"):
        value = tool_input.get(key)
        if isinstance(value, str):
            paths.append(value)
    if tool_name == "Bash":
        cmd = tool_input.get("command")
        if isinstance(cmd, str):
            # path-like tokens: contain a separator
            for tok in re.split(r"""[\s'"`;|&=(){}<>,:]+""", cmd):
                if "/" in tok:
                    paths.append(tok)
            # bare targets of dir-creating commands and redirects
            paths.extend(_DIR_CMD_TARGET.findall(cmd))
            paths.extend(_REDIRECT_TARGET.findall(cmd))
    return paths


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    tool_input = data.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return 0
    tool_name = data.get("tool_name", "")

    bad = []
    for p in candidate_paths(tool_name, tool_input):
        for seg in path_segments(p):
            if is_typo(seg):
                bad.append(seg)

    if bad:
        uniq = ", ".join(sorted(set(bad)))
        sys.stderr.write(
            "Blocked: path contains a likely misspelling of the Claude config "
            'directory ({}). Use exactly ".claude". If this directory name is '
            "genuinely intentional, rename it or adjust the guardrails plugin's "
            "guard-claude-spelling.py hook.\n".format(uniq)
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())