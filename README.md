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
