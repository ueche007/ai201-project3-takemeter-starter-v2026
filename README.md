# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

TakeMeter sorts posts and comments from **r/running**, Reddit's general running
community, by what they give a reader. A post either asks the community
something (`question`), reports the writer's own running with a concrete
detail (`firsthand`), tells readers what to do or what's true about running
without that firsthand evidence (`claim`), or says nothing about running at all
(`chatter`). It fine-tunes DistilBERT on 220 labelled r/running posts. The useful split for a reader is `firsthand`
vs `claim`: two posts can give the same advice, and only one shows where it came from.

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

Four labels, sorted by what a post gives the reader: a request, the writer's
own evidence, a general assertion, or nothing about running. The same
definitions are in [label_definitions.txt](label_definitions.txt) for the baseline.

### `question`

**Definition:** The writer asks or requests something from readers (advice,
information, a recommendation or an opinion), and getting answers is the
reason for the post.

**Example 1:**
> Where do you put your keys and phone that's NOT a FlipBelt?
> How do you all carry stuff when running? I've been using a FlipBelt for a few years but I don't find it comfortable as I can never get it to stop riding up, so I'm looking at other options. I've been thinking about getting a vest but the furthest I currently run is half marathon distance, so I'm not sure it's warranted.

**Example 2:**
> Insatiable appetite since I started running?
> Hi all! I (27F) am training for a half-marathon despite never really running before. […] Training has gone well so far, but I am SO hungry all the time. […]
> What should I be doing to curve this appetite? I feel like I'm out-eating whatever weight I would be losing from running lol

### `firsthand`

**Definition:** The writer reports something that happened in their own
running (a race, a run, a training block, an injury, or what happened when
they tried something) with at least one specific detail tying it to a
particular occasion.

**Example 1:**
> Guilty of this. Ran through shin splints for 3 weeks last fall because I was training for my first half marathon and didn't want to "lose progress". Ended up needing 6 weeks off instead of the 1-2 I would have needed if I'd just listened to my body from the start. Now I treat rest days like they're part of the training, not a break from it.

**Example 2:**
> Despite mocking and negativity from my family I just ran my first ever 5k
> Last year I started going to the gym here and there but didn't really commit, and a few months ago I struggled to run for even a few minutes. About a month ago I really started sticking to running at least 2 or 3 times a week with some cross training, and with some real progress I've finally reached my goal of 5k, without stopping, and made it in 28 minutes! […]

### `claim`

**Definition:** The writer tells readers what to do, or states what is true
about running, races, gear or runners, without a firsthand account of their
own behind it.

**Example 1:**
> My guess is it's more about fairness and record keeping than romance. Straight downhill point to point races would be chaos.
> The history is cool but governing bodies really care about comparability.

**Example 2:**
> I concur. Unless you have a specific performance goal, i.e. beating you PB on a given distance, or a specific time in a race, then no need for speed training. Unless this is what motivates you to keep on running, then it's a different thing.

### `chatter`

**Definition:** Social talk that says nothing about running: agreement,
thanks, congratulations, jokes, or talk about Reddit and the subreddit.

**Example 1:**
> Exactly! The dopamine effect from getting up voted!
> BTW, I up voted your comment

**Example 2:**
> Lol how do you get downvoted for such an obvious statement

### The hardest boundary

**Which two labels:** `firsthand` vs `claim`. On r/running the most common
substantial comment is a personal story that turns into advice. This one, from
a thread asking why marathon plans rarely include running 26 miles before
race day, sits right on the line:

> I ran my first maraton at 41. Trained 3-4 days per week (40-60 km) and it took my 1 week to recover. You will feel horrible after but the next day, get out and walk 5-10 km and so on (swim or bike is likely fine as well). The important thing is to get the blow flowing to help healing the body. […]

Half of it is the writer's own marathon and half is instructions to the reader.

**The decision rule I used every time:** If the post contains a firsthand
account of the writer's **own** running with at least one specific detail of
a particular occasion (a time or pace, the distance of a particular run, a
date or month, a named race or place, or a body part that got hurt), it is
`firsthand`, even if it also gives advice or a general opinion. Without that
detail it is `claim`. These don't count as a specific detail:
- vague appeals like "in my experience", "this worked for me" or "took me
  years to learn";
- bare counts like "two marathons";
- details of someone else's running (a spouse, a friend, a pro). Those are
  evidence offered for a claim, not a firsthand account.

The post above is `firsthand`: first marathon at 41, 40–60 km weeks, a week to recover.

**The other rules, applied in this order** (the order settles the boundaries
that aren't the hardest):

1. **`question` first.** A post whose title asks readers for an answer is
   `question`. That includes imperative requests ("Recommend me a daily
   trainer…", "Lend me your tales"), but not imperatives that tell readers
   something ("Please don't take for granted…", "Go for it"). It stays
   `question` even if the body is a long personal account. Anything else,
   including any comment, is `question` if asking readers for help,
   information, recommendations or opinions is the point of it. A closing
   "any tips for my situation?" counts. These don't count as asking:
   - a rhetorical question;
   - a question the writer answers themselves;
   - a closing invitation to share stories ("Anyone else…?") after a complete report.
2. **`firsthand` vs `claim`**: the rule above. A "particular occasion" also
   covers:
   - the writer's own regular training with a number on it ("50–80 mpw", "I
     usually run 26 before race day");
   - a relative date ("yesterday", "last fall");
   - a named body part that keeps getting hurt.

   Organising, coaching, pacing for or watching someone else's race is not the
   writer's own running.
3. **`claim` vs `chatter`.** If any sentence sincerely says something about
   running, races, gear or runners (a recommendation, a fact, an opinion), it
   is not `chatter`. "Congrats!! The back half of a marathon in the heat is a
   different race" is `claim`. These are still `chatter`:
   - merely naming gear or a race inside a joke;
   - a joke;
   - quoting what someone else said, with no point of the writer's own.

These rulings on how-to-apply were added after pre-labelling showed four
places where the first version was read two ways (see
[notes/stress_test.md](notes/stress_test.md)). The four labels and their
definitions did not change.

**How the rules were tested:** before labelling, an AI wrote 8 posts aimed at
these boundaries and a separate AI session labelled them blind from the
definitions. It matched the intended label on all 8, but only one call was
high-confidence. Its notes produced the "requests count", "closing invitation",
"someone else's running" and "naming gear in a joke" clauses above. The record
is in [notes/stress_test.md](notes/stress_test.md).



---

## The Dataset

**Where the posts came from:** Public posts and comments from
[r/running](https://www.reddit.com/r/running/), collected on 2026-10-20 from
Reddit's public RSS feeds. The JSON API now needs a login. The feeds used were:
- top posts of all time, of the year and of the month;
- hot and new posts;
- the latest comments;
- the full comment threads of eight discussion posts (e.g. "Is it worth doing
  a Major Marathon?", "Should a beginner ditch speed training?", "Why do marathon
  training plans almost never suggest running 26 before race day?").

`tools/fetch_rss.py` downloads the feeds slowly, because Reddit rate-limits
hard. `tools/build_pool.py` turns them into a 938-item pool (227 submissions,
711 comments): it strips HTML, drops usernames, bot and moderator boilerplate,
and deleted posts, and removes duplicates. Posts are kept whole. For a
submission, the first line is its title.

**How I labelled them:** `labels.csv` has 220 rows, built by
`tools/assemble_labels.py`:
- **20 cold rows** (`note` starts `cold`): 19 drawn at random from the pool
  (seed 20, in a scratch script that wasn't kept; the ids are in
  `notes/cold_ids.txt`) plus 1 replacement drawn by `tools/assemble_labels.py`,
  after one original turned out to be a moderator thread. Kept apart from
  everything below and labelled by hand from the definitions alone, before
  any pre-labels were seen. One of them, the women's running shoes post, was
  also item 22 of the Milestone 1 reading sample, so it wasn't unseen.
  <!-- TODO: true only once you've labelled the 20 cold rows yourself
  (`python tools/review.py --cold`). -->
- **200 pre-labelled rows**: Claude pre-labelled 280 random pool items (100
  submissions, 180 comments, with short comments over-sampled so `chatter`
  wasn't starved). 5 of the submissions turned out to be moderator boilerplate
  threads and were dropped, leaving 275 (95 submissions, 180 comments). The 112 uncertain ones were re-checked after the rules were
  clarified (Label Taxonomy, rules 1–3). 16 were still low-confidence: a few
  because their label depended on a parent comment or thread the text doesn't
  contain, the rest because the rules still didn't settle them (a plural
  occasion, an unclear spectator, sarcasm). Those were left out rather than
  guessed. From the rest, 200
  were sampled at random within each label to balance the counts. I then read
  and corrected every one with `tools/review.py`. <!-- TODO: true only once the review
  is finished; check `python tools/check_labels.py` says 0 left. -->

Every row's `note` ends with its Reddit id (`t1_…` comment, `t3_…` post).
The pool file `data/candidate_posts.csv` maps each id to its permalink. Both pre-label passes and their reasons are in
`notes/prelabels.csv`.

**Counts per label:** <!-- TODO: re-run `python tools/check_labels.py` after
the cold labels and the review are done, and paste the final counts here. The
table below is the 200 pre-labelled rows before review. -->

| Label | Count | Share |
|---|---|---|
| `question` | 50 | 25.0% |
| `firsthand` | 52 | 26.0% |
| `claim` | 53 | 26.5% |
| `chatter` | 45 | 22.5% |
| *cold rows, not yet labelled* | 20 | — |
| **Total** | 220 | shares above are of the 200 |

**Three hard cases**

**1.**
> *The post:* "Running with my daughter". A report: a 5 km run yesterday,
> with a seven-year-old on a scooter. It ends: "I'm hoping that we can keep
> this going so if anyone has other tips for running with kids let me know."
>
> *Could have been:* `firsthand` (a complete report with a date and a
> distance) or `question` (it asks for tips).
>
> *I chose, because:* `question`. Rule 1 comes before rule 2, and a closing
> request for help with the writer's own situation counts as asking. A closing
> "Anyone else…?" that only invites stories would not. It's a close call
> because the post reads like a report, but the order of the rules
> is there to stop the reading-like-a-report judgement deciding it.
> <!-- TODO: all three hard-case labels are Claude's re-checked pre-labels.
> Confirm or change each during review, and rewrite the reasons in your own words. -->

**2.**
> *The post:* "Energy was off the charts this year. It was unseasonably warm,
> but that made for great spectator weather." (a comment in the "Is it worth
> doing a Major Marathon?" thread)
>
> *Could have been:* `firsthand` (a particular race, this year, described from
> experience) or `claim`.
>
> *I chose, because:* `claim`. Nothing in the text says the writer ran, and
> "great spectator weather" suggests they watched. Watching someone else's race
> isn't the writer's own running, so there's no firsthand account, just a
> statement about the race.

**3.**
> *The post:* a news post about World Athletics giving USATF extra
> half-marathon spots after three athletes were led off course, with the
> writer's only addition being "Did they get it right?"
>
> *Could have been:* `claim` (the post is mostly reported fact about a race)
> or `question`.
>
> *I chose, because:* `question`. The title is a statement, so it fell to
> the body rule. Asking readers for their opinion counts as asking, and that
> question is the only thing the writer adds. The first draft of rule 1
> listed only help and information, and one pre-label pass called this `claim`.
> That disagreement is why rule 1 now names opinions.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased` (the notebook's default), fine-tuned
for sequence classification with 4 output labels.

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, max length 128
tokens, seed 42. 70/15/15 stratified split.

**Device:** `mps` (Apple Silicon GPU, torch 2.14.1). A practice run of the
notebook on the 60-post practice set took about 2 minutes end to end on this machine.

**Anything I changed from the defaults, and why:** Nothing. One known cost
of keeping `MAX_LENGTH = 128`: r/running submissions are long (median 981
characters, roughly 240 tokens), so the model only sees the first part
of most submissions. Comments (median 243 characters) mostly fit. For a
`firsthand` post whose only specific detail comes late, or a race report whose
request is in the last line, the deciding text can be cut off. That's a likely
unit 6 diagnosis, noted here before any results.

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

I used Claude (Claude Code, Opus 5.5) heavily in this unit. What it did:
- wrote the collection scripts in `tools/`;
- drafted the Milestone 1 distinctions, the taxonomy and the decision rules;
- ran the boundary stress test;
- drafted the five criteria in `criteria.md`;
- pre-labelled the dataset.

**The criteria in `criteria.md` were drafted by Claude at my request.** The
brief asks students to write these themselves, and I'm saying so plainly
rather than presenting them as mine. They were committed before any training on
my data (commit `fb8efed`).

**Moment 1: stress-testing the taxonomy**

- *What I asked for:* One Claude session wrote 8 r/running-style posts aimed at
  the label boundaries. A separate session labelled them blind, from the definitions only.
- *What came back:* It agreed with the intended label on all 8, but only one
  call was high-confidence. It pointed out that rule 1 missed requests phrased as
  commands ("Recommend me a trainer…"), and that the rules were silent on
  details from someone else's running.
- *What I changed:* `question` became "asks or requests". A closing "Anyone
  else…?" after a report stopped counting as asking. Someone else's running
  and bare counts like "two marathons" stopped counting as firsthand detail
  ([notes/stress_test.md](notes/stress_test.md)).

**Moment 2: pre-labelling showed the rules were read two ways**

- *What I asked for:* Four Claude sessions each pre-labelled 70 posts and
  reported their hardest calls.
- *What came back:* They disagreed on four things:
  - habitual training ("I usually run 26") as firsthand;
  - asking for an opinion as a question;
  - imperative titles;
  - "yesterday" as a date.
- *What I changed:* Claude drafted a ruling for each and I adopted them into
  rules 1–3. Then the 112 low- and medium-confidence pre-labels were re-checked
  against them.

**Pre-labelling disclosure:** The 20 rows marked `cold` were labelled by hand,
with no AI help and before seeing any pre-labels. <!-- TODO: true only after
`python tools/review.py --cold`. --> Every other row was
pre-labelled by Claude and then read and corrected by me. Each such row's
`note` column says which. <!-- TODO before submitting: confirm the review
happened, and give the number of labels you changed in review. -->

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
