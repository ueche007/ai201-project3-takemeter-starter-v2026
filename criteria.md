# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Overall accuracy is at least 0.65 on the held-out test split, on every one of the three seeds.

Measured by `accuracy` in `results_three_seeds_before.json`, one value per seed (42, 7, 2024). All three must be ≥ 0.65.

**Why this target:** With four labels, guessing at random scores about 0.25. Always guessing the biggest label scores about 0.27, because the pre-labelled rows are balanced (`claim` is 26.5%). Even at criterion 3's 40% cap, it couldn't score more than 0.40. A tool that sorts r/running posts has to be right about two times in three before it saves a reader anything, which puts 0.65 well clear of both floors. It also isn't a stretch: three of the labels have strong surface markers (question marks and "should I" for `question`, paces and times for `firsthand`, short "lol / this!" replies for `chatter`). The hard part is `firsthand` vs `claim`.

---

## 2. Every label has an F1 of at least 0.45 on the held-out test split, on every one of the three seeds.

Measured by `per_label[<label>].f1` for `question`, `firsthand`, `claim` and `chatter`, all twelve values (4 labels × 3 seeds) ≥ 0.45.

**Why this target:** A good average can hide one label the model never learns, and the likeliest candidate is `chatter`. It is the thinnest label in the pool, so it will have only about 6–8 posts in a ~33-post test split. On 6 posts a single extra miss moves F1 by roughly 0.15, so the per-label floor sits deliberately below criterion 1's 0.65. 0.45 still means the model finds most of a label's posts without flooding it with others. It is not a free pass for `claim`, which loses posts to `firsthand` under the hardest rule.

---

## 3. In `labels.csv`, no label is more than 40% of the rows, and no label is fewer than 12% of them.

Measured by counting the `label` column of `labels.csv` (`python tools/check_labels.py` prints the shares; the notebook's check cell prints the counts).

**Why this target:** The brief's 70% cap would allow a 140-row `firsthand` file and a 15-row `chatter` file, and the model would learn to guess `firsthand`. On r/running, the raw pool leans heavily toward stories and advice in the discussion threads. A 40% ceiling forces collection to keep `question` and `chatter` in. The 12% floor means at least about 26 of ~220 rows, which still leaves the smallest label about 4 posts in the test split under the 70/15/15 split. Below that, criterion 2 can't be measured meaningfully.

---

## 4. My labels agree with the staff labels on at least 21 of the 30 staff posts (70%), as reported by `agreement.py` in unit 6.

Measured by the agreement rate in `agreement_results.json`.

**Why this target:** This is the only check on whether I apply a written rule consistently, rather than in whatever way I happened to label my own 200. The staff set uses its own three labels (`analysis` / `hot_take` / `reaction`). It has an ordered "does the fact carry the argument" rule, the same kind of rule as my `firsthand` vs `claim` boundary, so a low rate there would be evidence about my own labels too. Staff say a rate in the 70s is normal and several posts were chosen to be ambiguous, so 70% is the bottom of "normal", not a stretch.

> **Note added after labelling (not a change to the criterion):** in the end all of `labels.csv` was labelled by Claude, not by me (see the README's pre-labelling disclosure). So this check measures how consistently *I* apply the staff's written rules. It isn't direct evidence about the consistency of `labels.csv`.

---

## 5. On every seed, the model's most-confident third of test predictions is at least 0.15 more accurate than its least-confident third.

Measured by `confidence.accuracy_most_confident_third − confidence.accuracy_least_confident_third` for each of the three seeds; all three gaps ≥ 0.15.

**Why this target:** For TakeMeter to be usable, a reader has to be able to trust its sure calls and double-check its unsure ones. That only works if confidence means something. With about 33 test posts, each third is about 11 posts, so a 0.15 gap is about 2 more correct answers in the confident third. That's small enough to be reachable, and large enough that it isn't noise from one lucky post. I expect `firsthand`-vs-`claim` posts to fill the unsure third, and that's exactly what this criterion should show.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
