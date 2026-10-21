"""Build labels.csv from the pool, the cold ids and the pre-label record.

    python tools/assemble_labels.py            # refuses to overwrite labels.csv
    python tools/assemble_labels.py --force    # only before any review has started

- 20 cold rows: the 19 ids in notes/cold_ids.txt, topped up to 20 with a random
  pool post that was never pre-labelled. These get a blank label. They're
  labelled by hand with no AI help.
- 200 pre-labelled rows from notes/prelabels.csv. Low-confidence rows are left
  out (their label depended on thread context the text doesn't have). The rest
  are sampled at random within each label to these targets.

Note column: "cold", or "pre-labelled by Claude (<conf>), not yet reviewed".
The post id goes at the end of the note, so every row can be traced to its permalink.
"""
import sys
from pathlib import Path

import pandas as pd

TARGETS = {"question": 50, "firsthand": 52, "claim": 53, "chatter": 45}   # 200
SEED = 5


def main():
    out = Path("labels.csv")
    if out.exists() and "--force" not in sys.argv:
        sys.exit("labels.csv exists; it may hold your review. Re-run with --force only if not.")

    pool = pd.read_csv("data/candidate_posts.csv").set_index("id")
    pre = pd.read_csv("notes/prelabels.csv")
    cold_ids = [i for i in Path("notes/cold_ids.txt").read_text().split() if i in pool.index]

    spare = pool.index.difference(pre["id"]).difference(cold_ids)
    while len(cold_ids) < 20:
        cold_ids.append(pd.Series(sorted(spare)).sample(1, random_state=SEED + len(cold_ids)).iloc[0])
        spare = spare.difference(cold_ids)

    usable = pre[pre["prelabel_conf"] != "low"]
    picked = pd.concat([
        usable[usable["prelabel"] == lab].sample(n, random_state=SEED)
        for lab, n in TARGETS.items()
    ])

    cold = pd.DataFrame({"text": pool.loc[cold_ids, "text"].values, "label": "",
                         "note": [f"cold · {i}" for i in cold_ids]})
    rest = pd.DataFrame({
        "text": pool.loc[picked["id"], "text"].values,
        "label": picked["prelabel"].values,
        "note": [f"pre-labelled by Claude ({c}), not yet reviewed · {i}"
                 for c, i in zip(picked["prelabel_conf"], picked["id"])],
    }).sample(frac=1, random_state=SEED)

    pd.concat([cold, rest]).to_csv(out, index=False)
    print(f"wrote {out}: {len(cold)} cold + {len(rest)} pre-labelled")
    print(f"left out: {(pre['prelabel_conf'] == 'low').sum()} low-confidence, "
          f"{len(usable) - len(picked)} surplus after balancing")


if __name__ == "__main__":
    main()
