"""Label the 30 staff posts under the STAFF taxonomy (data/staff_taxonomy.md).

    python tools/label_staff.py

Shows one post at a time from my_staff_labels.csv. Keys: a = analysis,
h = hot_take, r = reaction, s = skip, x = save and quit. Saves after every
answer, so you can stop and resume. Read data/staff_taxonomy.md first; these
are the staff's rules, not yours.
"""
import textwrap

import pandas as pd

PATH = "my_staff_labels.csv"
KEYS = {"a": "analysis", "h": "hot_take", "r": "reaction"}


def main():
    df = pd.read_csv(PATH, dtype=str, keep_default_na=False)
    todo = [i for i in df.index if not df.at[i, "label"].strip()]
    print(f"{len(todo)} of {len(df)} posts still to label.")
    print("a = analysis (a load-bearing checkable fact)   h = hot_take (confident, unsupported)")
    print("r = reaction (immediate, about the writer)     s = skip   x = save and quit")
    for n, i in enumerate(todo, 1):
        print(f"\n[{n}/{len(todo)}] {df.at[i, 'id']}")
        print(textwrap.fill(df.at[i, "text"], 78))
        while True:
            a = input("label: ").strip().lower()
            if a in KEYS or a in ("s", "x"):
                break
        if a == "x":
            break
        if a == "s":
            continue
        df.at[i, "label"] = KEYS[a]
        df.to_csv(PATH, index=False)
    df.to_csv(PATH, index=False)
    left = (df["label"].str.strip() == "").sum()
    print(f"\nSaved. {left} still blank." + ("" if left else " Ask your TF for data/staff_labels.csv, then run: python agreement.py"))


if __name__ == "__main__":
    main()
