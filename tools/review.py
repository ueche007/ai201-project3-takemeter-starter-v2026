"""Label the cold rows and review the pre-labels in labels.csv, one post at a time.

    python tools/review.py          # cold rows first, then unreviewed pre-labels
    python tools/review.py --cold   # cold rows only

Cold rows show no label and no hint; pick one from your definitions alone.
Pre-labelled rows show Claude's label and its reason (from notes/prelabels.csv).
Press Enter to accept it, or type the right label.

Keys: q/f/c/h = question/firsthand/claim/chatter, Enter = accept,
s = skip for now, x = save and quit. Every answer is saved straight away, so
you can stop and resume whenever you like. Changes you make are counted in
the note ("changed from claim"), so the README can report how many you corrected.
"""
import sys
import textwrap

import pandas as pd

KEYS = {"q": "question", "f": "firsthand", "c": "claim", "h": "chatter"}
PATH = "labels.csv"
DEFS = {
    "question": "asks/requests something from readers; answers are the point",
    "firsthand": "own running + a specific detail of a particular occasion",
    "claim": "what to do / what's true about running, no firsthand account",
    "chatter": "social talk that says nothing about running",
}


def show(text):
    print("─" * 78)
    for line in text.split("\n"):
        print(textwrap.fill(line, 78, subsequent_indent="  ") if line else "")
    print("─" * 78)


def ask(prompt):
    while True:
        a = input(prompt).strip().lower()
        if a in ("", "s", "x") or a in KEYS:
            return a
        print("  q/f/c/h, Enter, s or x")


def main():
    df = pd.read_csv(PATH, dtype=str, keep_default_na=False)
    reasons = pd.read_csv("notes/prelabels.csv").set_index("id")
    cold_only = "--cold" in sys.argv

    def rid(note):
        return note.rsplit("· ", 1)[-1].strip()

    cold = [i for i in df.index if df.at[i, "note"].startswith("cold") and not df.at[i, "label"]]
    todo = [i for i in df.index if "not yet reviewed" in df.at[i, "note"]]
    queue = cold + ([] if cold_only else todo)
    print(f"{len(cold)} cold rows to label, {len(todo)} pre-labels to review.")
    for k, v in DEFS.items():
        print(f"  {k[0]} = {k:<10} {v}")

    for n, i in enumerate(queue, 1):
        is_cold = i in cold
        print(f"\n[{n}/{len(queue)}] {'COLD — no hints' if is_cold else 'review'}")
        show(df.at[i, "text"])
        if is_cold:
            a = ask("label (q/f/c/h, s skip, x quit): ")
            if a in ("", "s"):
                continue
        else:
            pre = df.at[i, "label"]
            r = rid(df.at[i, "note"])
            reason = reasons.at[r, "recheck_reason"] if r in reasons.index else ""
            if not isinstance(reason, str) or not reason:
                reason = reasons.at[r, "pass1_reason"] if r in reasons.index else ""
            print(f"Claude says: {pre}   ({reason})")
            a = ask("Enter = accept, or q/f/c/h, s skip, x quit: ")
            if a == "s":
                continue
        if a == "x":
            break
        if is_cold:
            df.at[i, "label"] = KEYS[a]
        else:
            r = rid(df.at[i, "note"])
            new = pre if a == "" else KEYS[a]
            change = "" if new == pre else f", changed from {pre}"
            df.at[i, "label"] = new
            df.at[i, "note"] = f"pre-labelled by Claude, reviewed{change} · {r}"
        df.to_csv(PATH, index=False)

    df.to_csv(PATH, index=False)
    left = sum(1 for i in df.index if df.at[i, "note"].startswith("cold") and not df.at[i, "label"])
    left += sum("not yet reviewed" in x for x in df["note"])
    changed = df["note"].str.contains("changed from").sum()
    print(f"\nSaved. {left} rows still to do. {changed} pre-labels changed in review so far.")


if __name__ == "__main__":
    main()
