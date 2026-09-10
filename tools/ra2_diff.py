"""Diff the reference engine's extracted spec against the Zan port.

Reads tools/ra2_spec/screens.json (produced by tools/ra2_extract.py) and
the Zan source under templates/game/ra2/src, then reports every
divergence between the reference's declared sidebar and the port's.

This is the "自动 diff" step of the round: implementation is written
against the extracted table, and this tool proves the table and the
implementation agree -- a hand-written port silently drifting from the
reference (which is what happened with the retail-RA2 button list) shows
up here as a named mismatch instead of as a screenshot nobody checked.

Exit code 0 = in agreement, 1 = divergence found.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(r"D:\project\zan-lang")
SPEC = ROOT / "tools" / "ra2_spec" / "screens.json"
SCREENS = ROOT / "templates" / "game" / "ra2" / "src" / "game" / "Screens.zan"

# Which reference screen maps to which Zan draw function + label arrays.
# The mapping is explicit so a rename on either side is a visible error
# rather than a silent skip.
BINDINGS = [
    {
        "ref": "GUI:MainMenu",
        "zan_fn": "DrawMainMenu",
        "labels_var": "labels",
        "n": 10,
    },
]


def zan_main_menu_labels(src: str) -> list[str]:
    """Pull labels[i] = ... assignments out of DrawMainMenu."""
    return _zan_array(src, "labels")


def zan_main_menu_tips(src: str) -> list[str]:
    return _zan_array(src, "tips")


def _zan_array(src: str, name: str) -> list[str]:
    m = re.search(r"static int DrawMainMenu\(", src)
    if not m:
        return []
    rest = src[m.end():]
    nxt = re.search(r"\n    static ", rest)
    body = rest[:nxt.start()] if nxt else rest
    out: list[tuple[int, str]] = []
    # An assignment may span lines (string concatenation with '+'), so
    # match from `name[i] =` up to the terminating ';' at statement level.
    for lm in re.finditer(rf"{name}\[(\d+)\]\s*=\s*(.*?);", body, re.DOTALL):
        idx = int(lm.group(1))
        expr = " ".join(lm.group(2).split())
        # ui.Or("KEY", "fallback") -> KEY ; the first string literal
        # otherwise (concatenations join into one logical tooltip).
        om = re.search(r'\.Or\(\s*"([^"]+)"', expr)
        if om:
            out.append((idx, om.group(1)))
        else:
            parts = re.findall(r'"([^"]*)"', expr)
            out.append((idx, "".join(parts)))
    out.sort()
    return [v for _, v in out]


def main() -> int:
    if not SPEC.exists():
        print(f"missing {SPEC}; run tools/ra2_extract.py first")
        return 1
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    by_title = {s["title"]: s for s in spec}
    src = SCREENS.read_text(encoding="utf-8", errors="replace")

    failures = 0
    for b in BINDINGS:
        ref = by_title.get(b["ref"])
        if not ref:
            print(f"MISSING ref screen {b['ref']} in spec")
            failures += 1
            continue
        want = [x["label"] for x in ref["sidebar"]]
        got = zan_main_menu_labels(src)
        print(f"{b['ref']}  reference={len(want)} zan={len(got)}")
        if len(want) != len(got):
            print(f"  COUNT MISMATCH: reference {len(want)} vs zan {len(got)}")
            failures += 1
        for i in range(max(len(want), len(got))):
            w = want[i] if i < len(want) else "<missing>"
            g = got[i] if i < len(got) else "<missing>"
            mark = "  " if w == g else "!!"
            if w != g:
                failures += 1
            print(f"  {mark} [{i}] ref={w!r:34} zan={g!r}")
        # Also compare isBottom flags.
        zw = re.findall(r"bottom\[(\d+)\]\s*=\s*true", src)
        zwant = [i for i, x in enumerate(ref["sidebar"]) if x["isBottom"]]
        if sorted(int(z) for z in zw) != zwant:
            print(f"  BOTTOM MISMATCH: ref={zwant} zan={[int(z) for z in zw]}")
            failures += 1
        else:
            print(f"  bottom-pinned rows agree: {zwant}")

        # Tooltips: the reference declares one per button. The port must
        # carry the same text (a CSF key stays a key on both sides).
        want_t = [x["tooltip"] for x in ref["sidebar"]]
        got_t = zan_main_menu_tips(src)
        if len(want_t) != len(got_t):
            print(f"  TIP COUNT MISMATCH: ref={len(want_t)} zan={len(got_t)}")
            failures += 1
        for i in range(min(len(want_t), len(got_t))):
            w, g = want_t[i], got_t[i]
            # A CSF-keyed tooltip on the reference side may be spelled
            # with its fallback on ours; compare the key when the
            # reference has one, else require the literal.
            same = (w == g) or (w and g and w.split(":")[0] in ("STT", "GUI")
                                and w == g)
            if not same:
                print(f"  !! tip[{i}] ref={w!r}\n            zan={g!r}")
                failures += 1

    print()
    if failures:
        print(f"DIVERGENCE: {failures} mismatch(es)")
        return 1
    print("OK: port agrees with the extracted reference spec")
    return 0


if __name__ == "__main__":
    sys.exit(main())
