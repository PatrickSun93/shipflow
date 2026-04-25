# Cofounder lens — Education domain overlay

Loaded by `cofounder-expert` when the discovery `dialogue.md` shows
`_Domain: education_`. Layer these overlays on top of the six generic
founder frameworks. Most learning apps die for domain-specific reasons
the generic frameworks miss.

## 1. Buyer-vs-user split (sharpens Three-person test)

Education usually has two distinct customers — a buyer and a user — and
they don't share interests perfectly. Three-person test isn't enough on
its own: the user wanting to use it doesn't mean the buyer will pay.

**Test:** Name buyer and user separately for each archetype:
- B2C self-paced: buyer = user (Duolingo, Anki)
- B2C parent → child: buyer = parent, user = child (Khan Kids, ABCmouse)
- B2B teacher → student: buyer = school/district, user = student (Quizlet School, Newsela)
- B2B2C admin → teachers → students: 3-tier (Google Classroom, Schoology)

If buyer ≠ user, name the **buying trigger** — the moment that flips a
buyer from "interested" to "paying". Vague triggers ("they want to help
their kids learn") → pause. Concrete triggers ("parent gets a worried
email from teacher about kid's reading level") → strong.

## 2. Engagement-cliff pre-mortem (sharpens Pre-mortem)

The canonical learning-app death is users dropping off at week 2-3.
Generic pre-mortem can miss this because it's not a single-event failure
— it's gradual erosion.

**Test:** What specifically makes someone return on **day 14**?
- "It's habit-forming" / "the streak" → pause; that's the trick that
  works for Duolingo because the underlying experience is good, not the
  cause of the underlying experience being good
- A concrete loop (specific content delivery, social pressure,
  parent reminder, accountability partner, novel challenge) → strong
- "Network effects" without specifying what — pause

Bonus failure modes specific to learning apps to consider in the
2-failure list:
- Content gets stale; team can't author fast enough
- No measurable outcome → users can't tell if it worked → don't refer
- Engagement looks healthy but learning doesn't happen ("DuoLingo doesn't
  teach Spanish" critique)
- Free competitor (Khan, YouTube) at 10x the content depth

## 3. Outcome vs. engagement (sharpens Distribution + Insight)

Learning has a unique split: **time-on-app (engagement)** ≠ **measurable
learning (outcome)**. Most apps default to engagement metrics because
they're easier and they grow VC-friendly numbers.

**Test:** Quote the brief's `## Success` line. Classify:
- Engagement-shaped (DAU, sessions, streaks, completions): flag with
  `pause` + recommendation to add an outcome metric
- Outcome-shaped (test-score delta, skill demonstration, retention of
  content over 30 days): strong
- Hybrid that names both clearly: strongest

Engagement-only Success is a yellow flag for category fit — the founder
might be optimizing for the wrong thing.

## 4. Pedagogy religion (sharpens Contrarian insight)

Learning has long-running ideological battles. A founder without a
declared stance is usually one who hasn't actually committed.

**Common battle lines:**
- Spaced repetition vs. project-based learning
- AI-tutor (1:1 personalization) vs. peer learning (social)
- Mastery progression (don't move forward until 90% on current topic)
  vs. exposure (broad sampling, fluency emerges)
- Drilling/practice vs. exploration/play
- Direct instruction vs. discovery-based

**Test:** Pick a side on at least 2 of these battles. "Mix of all" or
silence on every battle is usually a tell — typically means the team
hasn't committed and will produce a bland average product. Pause and
recommend declaring a stance with reasoning.

## 5. Distribution: education channels are weird (sharpens Distribution test)

Education's distribution channels have very different team requirements
and economics — generic "first 100 users" thinking misses this.

**Channels and what they need:**
- **B2B school/district sales** — slow (6–12 month sales cycles), needs
  a sales team, requires curriculum-alignment work; high LTV per deal
- **Teacher word-of-mouth** — viral within school networks; needs a
  product teachers love AND want to share; tends to be very org-specific
- **Parent communities** (FB groups, WhatsApp, school parent groups) —
  strong consumer growth; needs identifiable parent value prop
- **App stores** (paid acquisition) — paid CAC dominates; needs broad
  appeal and decent conversion economics
- **Curriculum integration** (Common Core alignment, state testing prep)
  — works for specific markets; high effort + market-specific
- **Existing platform integration** (Google Classroom, Canvas, Schoology
  LMS plugin) — leverages existing distribution; product must fit the
  platform's UX assumptions

**Test:** Name **one channel** as the wedge for the first 100 users.
Multi-channel from day one → pause; most early-stage education apps die
trying to do too many channels at once. The wedge channel must match
the buyer-vs-user split (e.g. B2B sales for school buyer; FB groups for
parent buyer).

## How to apply

When you write the verdict block, fold these into the relevant
generic-framework lines and add a single `Domain overlay` bullet:

```markdown
**Domain overlay (education):**
- Buyer/user split: <named separately + trigger>
- Engagement loop on day 14: <concrete or "missing">
- Success metric type: <engagement | outcome | hybrid>
- Pedagogy stance: <declared | "mix of all" → flag>
- Wedge channel: <one channel + economics>
```

Don't run all 5 in isolation — the value is how they sharpen the six
generic frameworks. A `pause` from any single education-specific check
biases the overall verdict toward `pause`.
