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

## 1. Overall accuracy of at least 0.60, and at least 15 points above the majority-class baseline

On the held-out set, in every one of the three seeds, overall accuracy is at
least 0.60 **and** at least 0.15 higher than the accuracy of always predicting
my most common label.

**Why this target:** I have four labels (`help_request`, `discussion_question`,
`hot_take`, `analysis`), so random guessing gets about 25%. My largest label
will probably hold 35–45% of the posts, so "always guess the biggest label"
already scores around 0.40 and 0.60 alone is only 20 points above that. The
15-point margin stops me passing on label imbalance alone. 0.60 is where
I'd call it useful for sorting a feed: it would put roughly 6 in 10 posts in
the right bucket, and the `hot_take` / `discussion_question` boundary is subtle
enough that I don't expect much more from a small model on about 200 posts.

---

## 2. The three main labels each have an F1 of at least 0.55

`help_request`, `discussion_question` and `hot_take` each have an F1 of at
least 0.55 on the held-out set in every seed.

**Why this target:** Accuracy can hide a label the model never predicts. These
three should each hold enough posts to score fairly. `help_request` has
concrete cues (a device, a bill, "I've tried"), so I expect it to be easiest.
`hot_take` vs `discussion_question` is my hardest boundary (the rule is: remove
the question mark and see if a claim is left), so 0.55 is a deliberately modest
floor there. It is still well above the 0.25 a random guess would get.

---

## 3. `analysis` has an F1 of at least 0.40

`analysis` has an F1 of at least 0.40 on the held-out set in every seed.

**Why this target:** `analysis` needs a fact stated in the post itself, and that
is rare. Only 23 of the 200 posts contain a link at all, and most of those are
`help_request`. I expect `analysis` to be my smallest label, with maybe 6–8
posts in the test split, so its F1 will swing a lot between seeds, and one
misclassified post moves it by 10 points or more. That's why it gets a looser
floor than criterion 2. If I end up with fewer than 8 test posts for it, I'll
say so in the README rather than relax this number.

---

## 4. No label is smaller than 15% or larger than 45% of the 200 labelled posts

Every label has at least 30 of the 200 labelled posts and no label has more
than 90.

**Why this target:** Criterion 3 only makes sense if `analysis` has enough
examples to train and test on. At 30 posts, about 4–5 land in test, which is the
least I'd trust. A label above 45% would make the majority baseline in
criterion 1 too strong. If `analysis` comes in under 30, my plan is to merge it
into `hot_take` and rename that label, not to keep a label I can't measure.

---

## 5. I agree with my own blind re-label on at least 85% of 30 posts

After at least a day, I re-label 30 random posts without seeing my first label.
At least 26 of 30 (87%) must match, and no single label may match on fewer than
75% of its posts.

**Why this target:** The model can't be more consistent than the labels it's
trained on. Several of my rules rely on judgment calls: whether a fact is stated
in the post or only linked, and whether a claim is left once the question mark
is removed. Posts like #11 (four paper links, no stated fact) and #105 ("Are
you hesitant to install vibe-coded apps?") sit right on those lines. If I can't
reproduce my own labels, no model score is meaningful. If I fall under 85%,
I'll tighten the definitions and re-label before any training.

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
