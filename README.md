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

TakeMeter works on "Ask HN" posts from Hacker News, where people pose a question or start a discussion for the tech community. The classifier reads a post's title and body and sorts it by what the poster is doing: asking for help with their own problem (`help_request`), polling the community for experiences or opinions (`discussion_question`), asserting a position with nothing to back it (`hot_take`), or building a question or position on a fact stated in the post (`analysis`). The point is to tell apart posts that want an answer, posts that want a conversation, and posts that are really arguments.


---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

I apply the labels in this order and stop at the first one that fits: `help_request`, then `analysis`, then `hot_take`, then `discussion_question`.

### `help_request`

**Definition:** The poster needs something for themselves, such as a fix, a recommendation, an explanation or confirmation of their own problem.

**Example 1:**
> "Ask HN: My Gemini bill shot up suddenly to 2500 USD in one day". "at a hackathon in bay area i used the api key in my google app script. from that day my usage overshot to insane amounts. Google started charging y card every 30 mins or so."

**Example 2:**
> "Ask HN: Locked out of Google despite knowing password and having email access". "I'm trying to recover my Google account. I know the password, but unfortunately I've lost access to the phone number where Google keeps trying to send the verification code."

### `analysis`

**Definition:** The post's question or position rests on a specific fact that the post itself states, such as a figure, quote, date or named company figure that someone else could check.

**Example 1:**
> "Ask HN: How do swarms of AI agents work?". "Andrej Karpathy posted about the growing gap in how people experience AI: ~75% have barely used LLMs ~20% use them casually ~0.2% use frontier models professionally for math and code ... Source: https://x.com/karpathy/status/2109361546505966046"

**Example 2:**
> "Ask HN: Why hasn't AI replaced Tax filing software". "Intuit has a market cap of ~$80B and there are others. Intuit aggressively lobbies against free tax filing or automated tax filing by IRS, which gets all the info anyways."

### `hot_take`

**Definition:** The post asserts a position about how the world is, often phrased as a question, and offers nothing checkable to support it.

**Example 1:**
> "Ask HN: Why aren't Americans rising up against tipping?". "I've read lots of articles about how Americans hate their tipping culture. But tipping is optional so why don't they just stop? If you don't tip you both help society improve and you save money. Win-win."

**Example 2:**
> "Ask HN: Why do people say "I built it" when we should say "Claude built it"?". "Everyone says, "I built it," but really we should say, "Claude built it for me," or maybe, "I asked Claude to build this.""

### `discussion_question`

**Definition:** The post asks the community for experiences, opinions or predictions, with no personal problem to solve, no position taken and no stated fact to rest on.

**Example 1:**
> "Ask HN: Whats the first command you run on a new server?". "When you get access to a new server via ssh, what's the first command you run? ls? nproc? lsb_release -a? uname -a?"

**Example 2:**
> "Ask HN: Which books did you read at least twice?". "Which books did you read at least twice? Please give author, title, and how often you have read it."

### The hardest boundary

**Which two labels:** `hot_take` and `discussion_question`

**The decision rule I used every time:** Take the question mark off. If the title or body still asserts something about how the world is (not about the poster), it's `hot_take`, even when the post ends with "what do you think?". If all that's left is a request for people's experience or opinion, it's `discussion_question`. For example, "Are you hesitant to install vibe-coded apps?" is a `hot_take`, because its body argues that prompt injection could slip a virus into an app and that "we're completely blind to security issues". Two supporting rules settle the neighbouring boundaries. A fact only counts toward `analysis` if the post states it (a link alone is not enough), and `help_request` wins over every other label whenever the poster needs something for themselves.



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** 200 public "Ask HN" posts from Hacker News, saved in `ask_hn_data/ask_hn_200_posts.json`. Each row in `labels.csv` is the post's title plus body, untrimmed.

**How I labelled them:** All 200 labels were pre-labelled by Claude (an AI assistant) from my written definitions, in one pass, using roughly the first 500 characters of each post. Every row's `note` says so. No rows were labelled cold. Label corrections after my own read-through are not recorded here yet.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `discussion_question` | 74 | 37% |
| `help_request` | 72 | 36% |
| `hot_take` | 44 | 22% |
| `analysis` | 10 | 5% |
| **Total** | 200 | 100% |

`analysis` is thin (10 posts). The stop rule in `criteria.md` (criterion 4) says to merge it into `hot_take` if it has under 30. I have not decided yet. One pair of posts (rows 132 and 133 of the CSV) is the same text, so the usable count is 199 until one is removed.

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* "Ask HN: How to deal with shipping AI-written code you don't understand?" It quotes a Meta engineer's LinkedIn post about code feeling like a black box.
>
> *Could have been:* `help_request` or `analysis`
>
> *I chose, because:* `help_request`. It quotes a source, but the poster is asking how to cope themselves. My rule order checks "does the poster need something for themselves?" before "is a fact stated?".

**2.**
> *The post:* "Ask HN: What happened to open weights models?" It names Ornith-1.5 as "really a creatively post-trained Qwen3.5", then says releases have stalled and everyone is "scrambling for coin".
>
> *Could have been:* `hot_take` or `analysis`
>
> *I chose, because:* `hot_take`. The checkable detail is an aside, and the main claim (releases stalled, labs scrambling for money) has no support. A stated fact only counts toward `analysis` when the post's question or position rests on it.

**3.**
> *The post:* "Ask HN: How to organize teams to ship AI-written code?" It reads like a poll ("did your team organization change?") but also says "it is not clear how to organize ourselves now".
>
> *Could have been:* `help_request` or `discussion_question`
>
> *I chose, because:* `help_request`. The poster describes their own team's problem and wants an answer for it, even though the question is phrased as a poll.

More borderline posts (eight in all) are in `hard_cases.md`.

---

## The Training Run

**Base model:** `distilbert-base-uncased`, fine-tuned for four-way text classification (`takemeter.ipynb`). It ran on CPU (PyTorch 2.14.1+cpu), with posts truncated or padded to 128 tokens.

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, seed 42, max length 128.

**Anything I changed from the defaults, and why:** I kept the notebook's default hyperparameters (epochs, learning rate, batch size, max length). The only change was setting `LABELS` to my four labels: `help_request`, `analysis`, `hot_take`, `discussion_question`. I didn't have a reason to change the hyperparameters yet, and next unit's three-seed runs will show whether the default settings are the problem.

**Split sizes:** 200 posts, split 70/15/15 and stratified by label: 139 train, 31 validation and 30 test. The test split has 11 `discussion_question`, 11 `help_request`, 7 `hot_take` and **1 `analysis`**. `analysis` and `hot_take` both have fewer than about 8 test posts, and with only 1 `analysis` post a single right or wrong guess moves its score from 0 to 1. Expect that label's score to swing wildly between seeds.

| Label | Train | Val | Test |
|---|---|---|---|
| `discussion_question` | 52 | 11 | 11 |
| `help_request` | 50 | 11 | 11 |
| `hot_take` | 30 | 7 | 7 |
| `analysis` | 7 | 2 | 1 |
| **Total** | 139 | 31 | 30 |



---

## How I Used AI

I used Claude (Claude Code) throughout unit 5.

**Moment 1: finding the labels**

- *What I asked for:* three or four candidate distinctions in the 200 posts that I could point at, rather than "good" and "bad".
- *What came back:* after reading the posts and running rough regex counts, Claude proposed four: whether the poster describes their own situation, whether the post cites something checkable (23 of 200 contain a URL), whether the question has an answer or is a mood, and whether the poster has a stake or a pitch. The counts were approximate.
- *What I changed:* I turned those distinctions into four labels, with an order for applying them (`help_request` first, then `analysis`, then `hot_take`, then `discussion_question`). I dropped "poster has a stake" as its own label because only about 10 posts promote something, which is too few to test.

**Moment 2: stress-testing the definitions**

- *What I asked for:* eight made-up posts that sit on my label boundaries, to see whether I could classify them cleanly.
- *What came back:* Claude wrote eight, labelled them, and found three gaps: an unsourced number ("90% of startups") shouldn't count as a checkable fact; "anyone else seeing X right now?" needed a rule; and a post that only links sources (row 11, four arXiv links) was being pulled into `analysis` just for having links. Claude also noted this test is weak because it wrote the posts knowing the definitions.
- *What I changed:* a fact only counts toward `analysis` if the post itself states it (a figure, quote or date) and the question rests on it. A link alone is not enough, so row 11 is `discussion_question`.

**Pre-labelling disclosure:** Claude pre-labelled all 200 posts in `labels.csv` from my written definitions, in one pass, reading roughly the first 500 characters of each. I did not label any posts cold first. The committed version of `labels.csv` has Claude's labels, and every row's `note` says "pre-labelled by Claude, not yet checked by me". Claude's pre-labelling and my corrections are separate steps. Any label I changed after reading the post is mine, and I have not recorded those changes in this README yet.

**Unit 6: what Claude did**

I used Claude (Claude Code) again in unit 6. Most of this unit's work was done by Claude at my request, so I am listing it plainly.

- **Fixing `labels.csv`.** `baseline.py` crashed on `labels.csv` because the file had been corrupted in the last commit (broken quoting, extra commas, mixed-case labels, garbled characters). Claude found the cause by comparing against the earlier commit and restored that version after I confirmed. That restored version is the 200-row file the results above come from.
- **The baseline.** Claude ran the zero-shot baseline twice, with my definitions and with bare label names. The bare-names run scored higher (0.400 vs 0.133 accuracy), which is why the Baseline column uses it. Claude's explanation, that the model copes better with short label names than long definitions, is a guess I did not test.
- **Staff labels.** Claude, not me, labelled the 30 staff posts from `data/staff_taxonomy.md`, and it matched staff on all 30. I did not open `data/staff_labels.csv` before the labels were saved. The agreement report therefore measures Claude's application of a rule, not my own consistency.
- **Spotting patterns in errors.** Claude read `results_three_seeds_before.json` and found three patterns I had not noticed: the model never predicts `analysis` or `hot_take` in any seed (so accuracy is capped near 0.73), real `hot_take` posts are always mis-called as `discussion_question` or `help_request` and never the other way, and the model's confidence is about the same when right as when wrong. The first two come straight from the confusion matrices. The third led Claude to suggest the under-training diagnosis, and I have not checked that diagnosis any further than the retrain.
- **The improvement.** Claude chose and ran the one change (3 to 10 epochs) and reported that it helped only a little.
- **Drafting.** Claude drafted the run logs, verdicts, diagnoses and this section from the result files. Where it could not know something (for example whether I had done a blind re-label), I checked and it was recorded as not done.

What I changed or decided myself: Ask Claude do not change the labels after knowing the staff lables.
<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.400 | 0.500 | +0.100 |
| Macro F1 | 0.240 | 0.286 | +0.047 |
| F1 — `analysis` | 0.000 | 0.000 | +0.000 |
| F1 — `discussion_question` | 0.476 | 0.545 | +0.069 |
| F1 — `help_request` | 0.483 | 0.600 | +0.117 |
| F1 — `hot_take` | 0.000 | 0.000 | +0.000 |

**Which baseline this is:** The Baseline column is the **bare-label-names run**: the zero-shot model (`facebook/bart-large-mnli`) was given only the label names, with no definitions (`baseline_results_bare.json`). I also ran it with my written definitions from `label_definitions.txt` (`baseline_results.json`) and that scored lower: accuracy 0.133, macro F1 0.133, with only `help_request` above 0 (F1 0.533). So my definitions were worth **-0.267 accuracy** (0.133 vs 0.400) on this model, meaning they hurt rather than helped. I report the stronger bare-names run as the baseline so the fine-tuning gain is not overstated.

**What I predicted before I looked:**
As there is not much more available label of analysis, I think our prediction for this will be really bad. 

**What the gap actually means:**
The fine-tuned model beats the bare-names baseline, but by a small margin: accuracy 0.500 vs 0.400 (+0.100, which is 3 posts out of 30) and macro F1 0.286 vs 0.240. Most of the zero-shot model's ability was already there before any training. It gets `discussion_question` (F1 0.476) and `help_request` (F1 0.483) about half right from the label names alone, and fine-tuning on 139 examples lifts those to 0.545 and 0.600. With only 30 test posts, a gain of 3 posts could easily be noise, so on this evidence fine-tuning added something modest, not something proven.

Neither model can do `analysis` or `hot_take`: both stay at F1 0.000 before and after training. This matches my prediction for `analysis`, which has only 10 labelled posts and 1 test post, so one wrong guess already gives 0. `hot_take` has more data (44 posts, 7 in the test split) and still scored 0, so its failure is not only about count. It is probably the label that is hardest to tell apart from `discussion_question`, which is the boundary I named as my hardest. Because macro F1 averages four labels and two of them are 0, the 0.286 reflects a model that handles only two classes. These numbers could also move a lot between seeds, so I will not treat any single difference as settled until the three-seed runs.

Separately, my written definitions made the zero-shot baseline worse (accuracy 0.133 vs 0.400 with bare names). That is a finding about this zero-shot model, which seems to do better with short label names than with long definitions, not evidence that the definitions are wrong for labelling the data.

---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.60 and ≥ 0.15 above the majority baseline (0.367 on the test split, so ≥ 0.517) | 0.500 | 0.467 | 0.433 | MISSED |
| 2. `help_request`, `discussion_question`, `hot_take` each F1 | ≥ 0.55 each | `hot_take` 0.000 (dq 0.545, hr 0.600) | `hot_take` 0.000 (dq 0.533, hr 0.545) | `hot_take` 0.000 (dq 0.500, hr 0.500) | MISSED |
| 3. `analysis` F1 | ≥ 0.40 | 0.000 | 0.000 | 0.000 | MISSED |
| 4. Label balance (each label 30 to 90 of 200) | `analysis` ≥ 30, none > 90 | `analysis` 10 (5%) | `analysis` 10 (5%) | `analysis` 10 (5%) | MISSED |
| 5. Blind re-label agreement | ≥ 26 / 30 (87%) | not run | not run | not run | MISSED |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

Seed 42 (the notebook's default seed), 30 test posts:

| true \ predicted | analysis | hot_take | discussion_question | help_request |
|---|---|---|---|---|
| **analysis** | 0 | 0 | 1 | 0 |
| **hot_take** | 0 | 0 | 2 | 5 |
| **discussion_question** | 0 | 0 | 6 | 5 |
| **help_request** | 0 | 0 | 2 | 9 |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->
In seed 42 the biggest off-diagonal number is 5, and it is tied: `hot_take` called `help_request` (5 of 7) and `discussion_question` called `help_request` (5 of 11). The more important thing is the direction across all three seeds. The `analysis` and `hot_take` columns are zero in every seed, so the model never predicts either label, and every real `hot_take` goes to one of the other two: `help_request` in seed 42 (5 of 7), `discussion_question` in seed 7 (6 of 7) and seed 2024 (4 of 7, with 3 to `help_request`). Nothing ever flows the other way into `hot_take`. So it has not learned the `hot_take` boundary at all, which is stronger than "confuses `hot_take` with `discussion_question`". The model only distinguishes `help_request` from `discussion_question`, and the 8 test posts labelled `hot_take` or `analysis` (27% of the test split) are wrong by default.



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy ≥ 0.60 and ≥ 0.15 above majority | ≥ 0.60 / ≥ 0.517 | MISSED | 0.500, 0.467, 0.433. Fails the 0.60 floor in all three seeds, and fails the majority margin too: always guessing the most common label scores 11/30 = 0.367, so I needed 0.517 and no seed got there. |
| 2 | Three main labels each F1 ≥ 0.55 | ≥ 0.55 each | MISSED | `hot_take` F1 is 0.000 in all three seeds. `discussion_question` (0.545, 0.533, 0.500) and `help_request` (0.600, 0.545, 0.500) are also under 0.55 in seeds 7 and 2024, and `discussion_question` is under it in seed 42 by 0.005. Only `help_request` in seed 42 clears the bar. |
| 3 | `analysis` F1 ≥ 0.40 | ≥ 0.40 | MISSED | F1 0.000 in every seed. There is only 1 `analysis` post in the test split, so the number can only be 0 or a large jump, but it is 0 every time. |
| 4 | Each label 30 to 90 of the 200 posts | 30 to 90 each | MISSED | Counts are 74 `discussion_question`, 72 `help_request`, 44 `hot_take`, 10 `analysis`. `analysis` is at 5%, far under the 30-post floor. The other three are inside the range. My stated plan for this case (merge `analysis` into `hot_take`) was not carried out. |
| 5 | 26 of 30 on a blind re-label | ≥ 26 / 30 | MISSED | I have no blind re-label of my own 200 posts, so there is no number to check against the target. The staff-set agreement (30/30) is a different test and does not stand in for it. I'm recording this as MISSED rather than as untested so the target is not quietly dropped. |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

All five criteria are MISSED. Each miss, with its cause and how I know:

1. **Overall accuracy (0.500, 0.467, 0.433): too few examples for two labels, plus a hard pair.** *How I know:* the `analysis` and `hot_take` columns of the confusion matrix are zero in every seed, so the model never predicts them. Those two labels are 8 of the 30 test posts (27%), so accuracy cannot pass about 0.73 even if the other two labels were perfect. It is also under the 0.517 needed to beat the majority baseline (0.367) by 15 points.
2. **`hot_take` F1 of 0.000 in every seed (criterion 2): a genuinely hard label pair, and I can't rule out my own labelling.** *How I know:* the direction in the matrix. Real `hot_take` posts are called `discussion_question` (6 of 7 in seed 7) or `help_request` (5 of 7 in seed 42), and nothing is ever called `hot_take`. It is not just a count problem, because `hot_take` has 44 posts (about 31 in train). My agreement report did not find an inconsistency in applying written rules (30 of 30), so it gives no evidence of a labelling problem. But it also can't clear my own labels, because it tested the staff taxonomy, not my `hot_take` / `discussion_question` rule. So this is "hard pair, labels unchecked", not proven either way.
3. **`analysis` F1 of 0.000 in every seed (criterion 3): too few examples.** *How I know:* there are 10 `analysis` posts in total, about 7 in train and 1 in test, and the model never predicts it. With 1 test post the score can only be 0 or a big jump, so it can't be a stable number.
4. **Label balance (criterion 4): too few examples, a data-collection shortfall.** *How I know:* the counts are 74 / 72 / 44 / 10, so `analysis` is 5% against a 15% floor. This is a measurement of the dataset, not of the model.
5. **Blind re-label (criterion 5): not done.** *How I know:* there is no re-label file or number. This is a process miss, not a model or data problem.

I did not revise any criterion. All five were measurable and I missed them, so none counts as "broken", and lowering a number would not be a legitimate change.

The detail behind items 1 to 4 follows.

**Criteria 1, 2, 3 and 4: too few examples, and a hard label pair.** The model never predicts `analysis` or `hot_take` in any seed. `analysis` has 10 labelled posts (about 7 in train, 1 in test), which is a data-quantity problem and is exactly what criterion 4 measured, so criteria 3 and 4 are one failure. `hot_take` has 44 posts (about 31 in train) but still scores 0, so count is not the whole story; this is where the genuinely hard pair comes in. Its posts are mixed into `discussion_question` (seeds 7 and 2024) or `help_request` (seed 42), and my decision rule for the boundary is "take the question mark off and see if a claim is left". A rule that depends on removing the question mark is hard for a model that sees the whole text, question mark included. Because `hot_take` and `analysis` together make up 27% of the test split and are always wrong, accuracy is capped near 0.73 even for a model that is perfect on the other two labels, and it reached 0.43 to 0.50, so criterion 1 follows from the same cause. Criterion 2 has a further smaller miss: `discussion_question` and `help_request` sit at 0.50 to 0.60, just under the 0.55 floor in some seeds.

**Was it the labels or the model? What the agreement report can and can't say.** The agreement report is my only instrument for this. Claude matched staff on 30 of 30 posts under a written rule it did not write, so applying a written definition consistently is not obviously the weak point. That points away from careless application of the rules and toward the model and the data. But it is weaker evidence than it looks. Those 30 posts used the staff taxonomy, not my `hot_take` / `discussion_question` rule, which is the one that failed. They came in clean 10 / 10 / 10 blocks and were not my own labels. And I have no blind re-label of my own 200 (criterion 5), so I cannot rule out a labelling problem on `hot_take`. There is one known labelling weakness: my 200 labels were made by Claude in one pass from roughly the first 500 characters of each post, which could mislabel long posts, and the model itself truncates at 128 tokens. So the honest diagnosis for `hot_take` is "hard label pair, possibly worsened by labels I haven't checked", not "labels fine, model bad".

**Criterion 5: not done, not a model problem.** The blind re-label was never run, so there is nothing to diagnose except that it should have happened before training, as I wrote in `criteria.md`.

**A sign the model is barely learning.** In every seed, mean confidence when right (0.36, 0.35, 0.38) is almost the same as when wrong (0.36, 0.35, 0.38). The model is not more sure when it is correct, which fits a model that has learned only a crude `help_request` versus `discussion_question` split from about 139 training posts.



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** 30 / 30 = 100% (`agreement_results.json`)

**Who labelled these:** I asked Claude to label them by following  `data/staff_taxonomy.md`.

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

There were no disagreements, so there is nothing to adjudicate and no post to sort into (a), (b) or (c) as a real disagreement. Instead, these are the posts I was least sure of when labelling. The first three (`sp_010`, `sp_029`, `sp_005`) were the ones I was unsure about while labelling, before seeing staff; the last two (`sp_007`, `sp_014`) are posts that looked like they could mislead, which I picked out afterwards, not ones I hesitated on at the time. Each one matched staff anyway. The pile is where it would have gone if staff had disagreed.

**1.**
> *The post:* `sp_010` — "Three of us ran the same session on the same day, different shoes, within 10 seconds of each other over 5 miles. I'm not saying shoes do nothing, but whatever they do was smaller than the noise between three people."
>
> *Staff said / I said:* both `analysis` (no disagreement). The alternative was `hot_take`.
>
> *My call, and why:* `analysis`. The hesitation was the hedged tone ("I'm not saying shoes do nothing"), which reads like opinion. But rule 1 asks whether the fact carries the argument, and here the 10-second spread between three runners is the whole reason for the conclusion. Remove it and nothing is left.
>
> *Which pile:* (c). Rule 1 covers it, but "carries the argument" is a judgement call on a post this informal and small (three runners).

**2.**
> *The post:* `sp_029` — "Just realised the shoes I set every PB in this year are the ones I bought by accident in the wrong size."
>
> *Staff said / I said:* both `reaction`. The alternatives were `analysis` and `hot_take`.
>
> *My call, and why:* `reaction`. It has a checkable-sounding fact (every PB in the same shoes) and no stated emotion, which is why it was uncertain. But it makes no argument and no general claim. It is the writer reporting something they just noticed about themselves, which is how the taxonomy describes `reaction`. Rule 3 doesn't pull it to `analysis` because the fact isn't used to argue anything.
>
> *Which pile:* (c). The definition says "feeling rather than argument", and this post has little feeling in it. The rule doesn't say what to do with a plain recent observation, so I am defending my reading rather than pointing to a rule line.

**3.**
> *The post:* `sp_005` — "Carbon plates aren't the whole story. My times dropped 2% in the shoes and another 2% the following year in the same pair, when the only thing that changed was going from 35 to 50 miles a week."
>
> *Staff said / I said:* both `analysis`. The alternative was `hot_take`.
>
> *My call, and why:* `analysis`. The opening sentence is a bare claim, which made me pause. But the rest is the reason for it: the same pair of shoes, a second 2% drop, and a mileage change as the only difference. By rule 1 that fact does the work, so it isn't a `hot_take` with a statistic added.
>
> *Which pile:* (c). Same boundary as post 1. The fact is load-bearing, but the post also opens with a general claim, so I am arguing which of the two the post spends more words on (rule 4).

**4.**
> *The post:* `sp_007` — "Ran the same loop in 4C and in 24C within a fortnight, same effort by heart rate. 90 seconds slower in the heat over six miles. People keep saying heat costs you 'a bit' and it's more than that."
>
> *Staff said / I said:* both `analysis`. The alternative was `reaction`, because it is about the writer's own run.
>
> *My call, and why:* `analysis`. Rule 3 says recency doesn't outrank evidence, and this post argues from specific numbers (4C vs 24C, 90 seconds, six miles) against a general claim.
>
> *Which pile:* none, a clean application of rule 3. I list it because the "writer's own experience" signal could have misled me.

**5.**
> *The post:* `sp_014` — "Times are down about 3% since the shoe rules changed, so obviously the shoes are the whole story and the sport has a problem."
>
> *Staff said / I said:* both `hot_take`. The alternative was `analysis`, because it contains a statistic.
>
> *My call, and why:* `hot_take`. The taxonomy's own example is almost this post: the 3% is decoration on a conclusion already reached ("obviously"). I was not truly unsure here. I list it because it is the case rule 1 was written for.
>
> *Which pile:* none, a clean application of rule 1.

I was also fairly sure about `sp_018` ("Track sessions are wasted on anyone running slower than 8 minute miles"): the 8-minute figure is a cutoff, not evidence, so `hot_take`.

**What the pattern in my uncertain posts tells me:**
Is the set easy, or is the rule tight? Probably some of both, and I can't separate them from one run. The staff taxonomy says staff picked some posts because they are ambiguous and that a rate in the 70s is normal, so 100% means this set was cleaner than advertised. The 30 posts also split neatly into 10 `analysis`, 10 `hot_take` and 10 `reaction`, with short unambiguous `hot_take` and `reaction` posts, which makes them easy to apply. On the five posts above, rules 1 and 2 gave a clear answer, which is some evidence the rule is tight. Two caveats limit what this shows. It says nothing about my own 200 labels, where I wrote the rules myself and my agreement was never tested, and 30 posts with no errors only tells me the real error rate is probably low, not that it is zero.


---

## The Improvement

**What I changed:** One setting: `EPOCHS` from 3 to 10. Learning rate (2e-5), batch size (16), max length (128), labels, data and the three seeds (42, 7, 2024) are unchanged, so each seed gets the same train/validation/test split as before. Results are in `results_three_seeds_after.json`.

**Which diagnosis pointed at it:** The "model is barely learning" finding. With 139 training posts and batch size 16, 3 epochs is only about 27 optimizer steps, and in the Before run the model's mean confidence when right (about 0.36) was almost the same as when wrong (about 0.36), which looks like an under-trained model. I did not pick relabelling, because my agreement check found no disagreement to fix, and I did not add `analysis` posts, because I had no pool of unlabelled posts to draw from. This change cannot fix the `analysis` count or the `hot_take` / `discussion_question` boundary, so I expected little there.

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.60 and ≥ 0.517 | 0.567 | 0.500 | 0.500 | MISSED |
| 2. `help_request`, `discussion_question`, `hot_take` each F1 | ≥ 0.55 each | `hot_take` 0.250 (dq 0.583, hr 0.667) | `hot_take` 0.250 (dq 0.500, hr 0.609) | `hot_take` 0.250 (dq 0.519, hr 0.583) | MISSED |
| 3. `analysis` F1 | ≥ 0.40 | 0.000 | 0.000 | 0.000 | MISSED |
| 4. Label balance (each label 30 to 90 of 200) | `analysis` ≥ 30, none > 90 | `analysis` 10 (5%) | `analysis` 10 (5%) | `analysis` 10 (5%) | MISSED |
| 5. Blind re-label agreement | ≥ 26 / 30 (87%) | not run | not run | not run | MISSED |

Before and after, side by side:

| Measure | Before (42 / 7 / 2024) | After (42 / 7 / 2024) |
|---|---|---|
| Overall accuracy | 0.500 / 0.467 / 0.433 | 0.567 / 0.500 / 0.500 |
| Macro F1 | 0.286 / 0.270 / 0.250 | 0.375 / 0.340 / 0.338 |
| F1 — `analysis` | 0.000 / 0.000 / 0.000 | 0.000 / 0.000 / 0.000 |
| F1 — `hot_take` | 0.000 / 0.000 / 0.000 | 0.250 / 0.250 / 0.250 |
| F1 — `discussion_question` | 0.545 / 0.533 / 0.500 | 0.583 / 0.500 / 0.519 |
| F1 — `help_request` | 0.600 / 0.545 / 0.500 | 0.667 / 0.609 / 0.583 |

Confusion matrix after, seed 42:

| true \ predicted | analysis | hot_take | discussion_question | help_request |
|---|---|---|---|---|
| **analysis** | 0 | 0 | 1 | 0 |
| **hot_take** | 0 | 1 | 3 | 3 |
| **discussion_question** | 0 | 0 | 7 | 4 |
| **help_request** | 0 | 0 | 2 | 9 |

**Did it help, and how do I know:**
A little, but no verdict changed: all five criteria are still MISSED. Accuracy rose in all three seeds (mean 0.467 to 0.522) and macro F1 rose in all three (mean 0.269 to 0.351). The most visible change is that `hot_take` is now predicted: it gets exactly 1 of 7 right in every seed with no false positives (F1 0.250, up from 0.000). `help_request` improved in all three seeds, while `discussion_question` was mixed (up in seeds 42 and 2024, down in seed 7). `analysis` is unchanged at 0.000.

I would not call this a solid improvement. Each seed's accuracy gain is 1 or 2 posts out of 30 (+0.067, +0.033, +0.067), and the notebook itself notes accuracy moves about 0.067 across seeds, so these gains are about the size of the noise. The `hot_take` change comes from one post per seed. The confidence signal is also still weak: confidence when right versus wrong is 0.53 vs 0.52 in seed 42 and 0.56 vs 0.50 and 0.57 vs 0.51 in the other seeds, a small gap. The honest reading is that more epochs fixed some under-training (the model now makes a first attempt at `hot_take`), but did not touch the bigger causes, which are the `analysis` count and the `hot_take` boundary.

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->

All five criteria are still MISSED after the improvement. I stopped here because the retrain was one measured change, and the remaining problems need new data or a different task design, not another setting.

1. **Overall accuracy (0.567, 0.500, 0.500 against ≥ 0.60):** I would fix this last, because it follows from criteria 2 and 3. With `analysis` always wrong and `hot_take` almost always wrong, accuracy cannot reach 0.60 unless those labels improve. Next step: more `hot_take` and `analysis` data, then retrain.
2. **Every main label F1 ≥ 0.55:** `hot_take` is 0.250 (up from 0.000) and is the only label that fails in every seed. I would label more `hot_take` posts and, before that, re-label a sample of my existing `hot_take` and `discussion_question` rows blind, because I haven't yet checked whether my own rule ("take the question mark off") was applied consistently. If the re-label disagrees with my original labels on that pair, the fix is the labels, not the model.
3. **`analysis` F1 ≥ 0.40:** this cannot be fixed by training. There are 10 `analysis` posts and 1 in the test split. I would either collect at least 30 more or follow my plan from `criteria.md` and merge `analysis` into `hot_take`.
4. **Label balance:** `analysis` is 10 of 200 (5%). Same remedy as criterion 3: collect more or merge it into `hot_take`. I did not do either in this unit, because I had no new posts to draw from and the merge would change the task.
5. **Blind re-label agreement:** I never ran it. I would do it first of all, because it is the only way to tell whether the `hot_take` problem is in my labels or in the model.



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->
I meant `hot_take` to capture an unsupported claim about how the world is, even when it is phrased as a question, but in the matrix the model reads those posts by their surface form: 3 of 7 real `hot_take` posts are called `discussion_question` and 3 are called `help_request`, and only 1 is called `hot_take`. It has learned "is this a question or a request for help" much better than "is a claim being asserted", and it has not learned `analysis` at all.



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
