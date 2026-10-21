# Taxonomy stress test (Milestone 2), 2026-10-20

Two separate Claude sessions:

1. **Writer.** It was given the first-draft definitions and rules, and asked for
   8 r/running-style posts on the label boundaries, each with the label the
   rules should give.
2. **Blind labeller.** It was given only the definitions, the rules and the 8 texts.

| # | Post (short) | Boundary | Intended | Blind label | Confidence | What it exposed |
|---|---|---|---|---|---|---|
| 1 | Carbon plates hot take, husband's 2:05 half | firsthand/claim | claim | claim | medium | Rules silent on someone else's running |
| 2 | "Stop doing long runs at MP. Took me two marathons…" | firsthand/claim | claim | claim | medium | Does a bare count ("two marathons") count as a detail? |
| 3 | Forefoot advice + "my left one [calf] did for most of March" | firsthand/claim | firsthand | firsthand | medium | One clause of own account flips a mostly-advice post |
| 4 | Philly Half report ending "Anyone else ever blow up a race…?" | question/firsthand | question | question | medium-low | Closing invitation vs "asking is the reason" |
| 5 | 18 miles, right knee, "Was that smart? Probably not." | question/firsthand | firsthand | firsthand | high | — |
| 6 | "Congrats!! … the back half in the heat is a different race" | claim/chatter | claim | claim | medium-high | "praise" in chatter vs rule 3 |
| 7 | Garmin vs Coros threads joke | claim/chatter | chatter | chatter | medium | Does naming gear count as running content? |
| 8 | "Recommend me a daily trainer for wide feet…" | question/firsthand | question | question | medium | Imperative request, no question mark |

**Result:** 8/8 agreement, but 7 of 8 calls were below high confidence, so the
first-draft rules worked only when read generously.

**Changes made:**
- `question` now covers requests ("asks or requests"), not just questions.
- A closing invitation to share after a complete report doesn't count as asking.
  Post 4 is now `firsthand`. This deliberately reverses the writer's intended
  label: the "reason for the post" test beats the position of the question mark.
- A specific detail must belong to a particular occasion. A bare count ("two
  marathons") doesn't count, and neither does someone else's running.
- `chatter` now means "says nothing about running". Naming gear or a race
  inside a subreddit joke is still `chatter`, and praise plus a running opinion is `claim`.

**Known risk kept on purpose:** under rule 2, a single clause of the writer's own
account (post 3) makes a post `firsthand`. That keeps the rule mechanical, at
the cost of some mostly-advice posts landing in `firsthand`. If the model
confuses `firsthand` and `claim` in unit 6, look here first.

## Round 2: what pre-labelling 280 real posts exposed

Four Claude sessions pre-labelled 70 posts each under the rules above, then
reported their hardest calls. They split on four things:

| Question | How the sessions split | Ruling now in the README |
|---|---|---|
| Habitual own training ("usually run 26", "60 km a week") | One session said `claim` (no single occasion); others said `firsthand` | `firsthand`: regular training with a number counts as a training block |
| Asking for an opinion outside a title ("Did they get it right?") | One said `claim` (rule 1 listed only help/info); definition said opinions count | `question`: rule 1 now matches the definition |
| Imperative titles that tell rather than ask ("Please learn about…", "Acknowledge Fat Runners") | Treated as `question` by a literal reading, otherwise not | Not `question`; only requests for an answer count |
| "Yesterday" / "a couple days ago" as the date detail | Counted by one session, untested by others | Counts as a particular occasion |

Also settled: organising, coaching or spectating isn't the writer's own
running, and jokes or quoted remarks with no sincere point are `chatter`. The
moderators' scheduled threads ("Super Moronic Monday", "Miscellaneous Monday
Chit Chat") are boilerplate and were removed from the pool.

The 115 low- and medium-confidence pre-labels were then re-checked against these rulings.
