# Milestone 1 — community and candidate distinctions

**Community:** r/running (https://www.reddit.com/r/running/), a public subreddit
for runners of every level. No login is needed to read it.

**Why it fits:** lots of text, and real variation in it. Race reports with
splits and paces sit next to one-line replies, beginner questions, advice from
experience, rants and opinions. It isn't built around one show or release.

**Collected:** 965 public items (239 submissions, 726 comments) in
`data/candidate_posts.csv`, pulled from Reddit's public RSS feeds on 2026-10-20
by `tools/fetch_rss.py` and `tools/build_pool.py`. The sources were top of
all time, top of the year, top of the month, hot, new, the latest comments,
and the comment threads of eight discussion posts. Usernames are not kept.

**Reading:** `notes/reading_sample.md`, 40 random items (15 submissions,
25 comments).

## Candidate distinctions I saw in the text

*Drafted by Claude from the 40-item reading sample (item numbers refer to
`notes/reading_sample.md`); disclosed in the README's How I Used AI.*

1. **Some posts report the writer's own running with specifics; others state
   general rules with nothing behind them.** Item 5 ("Ran through shin splints
   for 3 weeks… needed 6 weeks off") and item 26 ("Trained 3-4 days per week
   (40-60 km) and it took me 1 week to recover") carry their own evidence.
   Item 20 ("1 long run (increase by 10% every week)…") and item 28 ("no need
   for speed training") give advice with no account of the writer's running.
2. **Some posts exist to get answers; the rest exist to tell.** Items 31 (where
   to carry keys), 36 (insatiable appetite) and 22 (women's shoes) are written
   so that people reply. The Runna review (item 10) contains a question ("Does
   anyone use this?") but is plainly not asking.
3. **A slice of comments carries no running content at all.** Items 3 ("BTW, I
   up voted your comment"), 12 and 19 are social glue: agreement, jokes, apologies,
   talk about Reddit. They're short, and they make up much of what a reader skims past.
4. **Personal stories often end in advice.** Items 1, 26 and 4 (Boston race report
   with seven "tips") mix the two. This is where distinctions 1 and 2 collide,
   and it's the boundary any taxonomy here has to settle.

Also seen: bot removal notices and link-only posts with no text of the writer's
own. They are filtered out or kept title-only by `tools/build_pool.py`.
