"""Check labels.csv before training.

    python tools/check_labels.py [labels.csv]

Reports what still needs a human: blank labels (the cold rows start blank),
pre-labelled rows not yet reviewed, unknown labels, duplicate posts, and each
label's share against criterion 3 (between 12% and 40%).
"""
import sys

import pandas as pd

LABELS = ["question", "firsthand", "claim", "chatter"]
UNREVIEWED = "not yet reviewed"
LOW, HIGH = 0.12, 0.40


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "labels.csv"
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    print(f"{path}: {len(df)} rows")
    todo = 0

    blank = df[df["label"].str.strip() == ""]
    if len(blank):
        todo += len(blank)
        print(f"[TODO] {len(blank)} rows have no label yet "
              f"({(blank['note'].str.startswith('cold')).sum()} of them cold)")

    unrev = df[df["note"].str.contains(UNREVIEWED, regex=False)]
    if len(unrev):
        todo += len(unrev)
        print(f"[TODO] {len(unrev)} pre-labelled rows not yet reviewed. "
              f"Run: python tools/review.py")

    labelled = df[df["label"].str.strip() != ""]
    unknown = sorted(set(labelled["label"]) - set(LABELS))
    if unknown:
        todo += 1
        print(f"[FIX] labels not in LABELS: {unknown}")

    dups = df[df["text"].str.strip().duplicated(keep=False)]
    if len(dups):
        todo += 1
        print(f"[FIX] {len(dups)} rows share their text with another row")

    print(f"\n{'label':<10} {'count':>5} {'share':>6}   criterion 3 ({LOW:.0%}–{HIGH:.0%})")
    for lab in LABELS:
        n = int((labelled["label"] == lab).sum())
        share = n / len(labelled) if len(labelled) else 0
        ok = "ok" if LOW <= share <= HIGH else "OUT OF RANGE"
        print(f"{lab:<10} {n:>5} {share:>6.1%}   {ok}")
    cold = df["note"].str.startswith("cold").sum()
    print(f"\ncold rows: {cold} (brief wants 20)")
    print("\nReady to train." if todo == 0 else "\nNot ready yet: see the lines above.")


if __name__ == "__main__":
    main()
