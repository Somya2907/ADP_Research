# How Patches Are Created, and What "Narrow" vs "Broad" Really Means

You asked me three things: how patches get created, what our basis is for calling a
patch narrow or broad, and what problem a patch is actually fixing — since in the
original work that problem was graph edit distance over missing nodes and arcs. You
also made the point that BM25 can only be as good as the patches we mined in
training.

I went back through what we actually built rather than answering from memory. Two of
those questions have clean answers. On the narrow/broad one I have to be straight
with you: we never implemented it. It's language we used in writing, not something we
measure. And your BM25 point turns out to be sharper than I first appreciated — we
have a case where making the patches more precise made them retrieve worse.

---

## 1. How a patch gets created

The mining happens only on training cases, and it works off the difference between
the teacher's graph and the student's graph for the same case.

When we compare those two graphs, we get four kinds of discrepancy:

- **Missing nodes** — the teacher established something the student never mentioned.
- **Hallucinated nodes** — the student asserted something with no teacher counterpart.
- **Edge differences** — the teacher connected two things and the student either
  didn't connect them or connected them with the wrong relation.
- **Misgroundings** — the student got the legal proposition right but attached it to
  the wrong statutory section. Both rule nodes line up, so this is invisible to the
  other three categories.

Patches are mined from **two** of those four: missing nodes and misgroundings. And
missing nodes get filtered further — only Rules that are binding or persuasive, and
only Obligations that are mandatory or recommended. Advisory rules and safe-harbour
obligations are dropped, and a missing node of any other type is discarded outright.

That leaves three families of patch. We currently have 85 in the store: 42 for a
missed rule, 25 for a missed obligation, 18 for a misgrounding.

Each patch carries the controlling citation, a one-or-two sentence "prevention step"
telling the student what to do, a contraindication (which jurisdiction it applies in,
whether it's even in force yet, and any exceptions the teacher flagged), and a short
list of trigger keywords. Patches that describe the same authority and family get
merged across cases, so one patch can carry evidence from several training cases.

Two things are deliberate here. Patches are always written at the level of a rule or
a duty, never at the level of a case outcome — that's what stops training cases
leaking into test-time inference. And mining refuses to run on a non-training case at
all.

Three real ones, so this isn't abstract:

**A missed rule** — the teacher cited a NYC disclosure rule, the student never did:

> When a matter involves 5-304(d), apply DCWP Rules §5-304(d) (nyc, binding): Data
> retention/disclosure: employer must post AEDT data retention policy, data types,
> sources, and request instructions on website.

**A misgrounding** — the student knew the bias-audit rule but cited the wrong section
for it. This one was merged from two training cases, because the same mistake
happened twice:

> Ground the proposition "Bias audit required no more than one year prior to AEDT
> use; cannot use AEDT if more than one year since most recent audit" in NYC LL 144
> §20-871(a)(1); DCWP Rules §5-301(a), **not** 6 RCNY §5-301.

**A missed obligation** — this is the one at the centre of our results:

> Where 6-1-1703(2)(a)-(g) applies, CO AIA §6-1-1703(2)(a)-(g) imposes a mandatory
> obligation: Greenleaf: complete impact assessment for ResumeRank within 90 days of
> CO AIA effective date for pre-existing deployments (deadline: 2026-09-28).

I want to flag something in that last one rather than let you find it. It names
*Greenleaf* and *ResumeRank* — the company and product from a specific training case.
Our stated rule is that patches name no case facts, and when we route patch text
through the LLM rewriter we explicitly instruct it not to. But this patch used the
deterministic template, which copies the teacher's obligation wording verbatim, and
that wording was case-specific. I checked the whole store: 5 of 85 patches do this.

The injection step already guards against it — before a test prompt is assembled it
drops every patch whose text names a training-case party, and has done since Phase 2.
So these patches are mined and stored, but none of them ever reaches a student.

Two things still worth knowing. The store is not as party-free as the design assumes,
and the real fix is a one-line scrub in the deterministic template rather than a filter
downstream. And the guard has a side effect worth flagging: `p_31804710d2d2` is the
patch our retrieval analysis reports as the top hit for the Colorado duties, yet it is
dropped at injection — so the patch the retrieval tables credit is not the patch the
student actually receives.

---

## 2. Narrow vs. broad — we don't actually measure this

There's no breadth field on a patch, no metric, and no classifier. The words appear
in exactly one of our analysis documents, describing two specific patches after the
fact. So when we've written "broad patch," we've been describing, not measuring.

That said, the distinction is real, and it's obvious once you put the two patches
side by side. The one above cites a **span** — subsections (a) through (g) — and its
keywords cover ten distinct concepts: impact assessment, high-risk, algorithmic
discrimination, risk management, consumer, notice, consequential decision, data
correction, appeal, effective date. It hits our 12-keyword cap.

The patch that replaced it cites a **single subsection** and says only:

> Where 6-1-1703(2)(a) applies, CO AIA Section 6-1-1703(2)(a) imposes a mandatory
> obligation: Implement risk management policy and program consistent with NIST AI
> RMF 1.0 or ISO/IEC 42001 (deadline: 2026-06-30).

Four keywords, two concepts, one duty.

So "breadth" as we've been using it is really **citation span**, and it shows up
mechanically as how many keywords the patch carries — which matters enormously,
because keywords are the only thing retrieval can see. The broad patch is reachable
from ten different concept queries; the narrow one from two.

And breadth is what drove the result. The broad patch's text spelled out four
deployer duties — website statement, consumer notice, data correction, appeal rights
— which correspond to four binding teacher rules worth four points each. One patch,
in one retrieval slot, pulled that whole cluster out of the 3B student. When it was
swapped for the risk-management-only patch, the student stopped producing those rules
and node recovery fell from roughly 28 points to about 8.

Making this a real measurement isn't hard, and we half-have the machinery already —
we compute a "duty key" from a citation for other purposes, we just never attached it
to the patch. The cheap version is to count how many distinct duties a patch's
citation spans, which we can do at mining time for free. The honest version is to
count how many teacher nodes the patch's text actually recovers, which tells us what
we really want to know but needs an injection run to measure. I'd add the cheap one
first, because it lets us make decisions before spending any inference budget.

---

## 3. What the patch is actually fixing

This is where our implementation has drifted from the original framing, and it's the
part I think genuinely needs a decision from us.

Our edit-distance score adds up missing nodes, hallucinated nodes, and edge
differences, each weighted by node type — with Application and Obligation weighted
highest at 2.5, Rule at 2.0, and rules further multiplied by how binding they are.
Misgroundings are computed but left **out** of the score by default, so that older
snapshot numbers stay comparable.

Now compare that to what actually generates patches:

| Discrepancy | Counted in the score | Generates a patch? |
|---|---|---|
| Missing nodes | yes | only Rules and Obligations |
| Hallucinated nodes | yes | never |
| **Edge / arc differences** | yes | **never** |
| Misgroundings | **no** | always |

Three things fall out of that:

**Arcs move the score and have no corrective path at all.** To answer your question
directly — in this work the patch target is missing *nodes* plus misgrounding. Arcs
are diffed and scored, but nothing we mine can ever fix one.

**Misgrounding is the reverse** — we have a corrective path for it but it doesn't
move our headline number, because that flag is off.

**Four of the six node types can never be patched** — Facts, Issues, Applications,
Conclusions — including Application, which carries the joint-highest weight in the
score.

I'd defend part of that. Rules and Obligations are the only node types that are
case-*independent*: a statute and the duty it imposes carry over to a new case, while
a fact or an application is welded to the matter it came from. Turning those into
"reusable" notes is exactly how training-case content would leak into test inference.

But that defence doesn't cover arcs. An edge saying *this statute triggers this duty*
is every bit as case-independent as the two nodes it connects, and we're throwing
those away. That's a real gap rather than a consequence of the firewall, and it's the
first thing I'd change.

---

## 4. On BM25 — you're right, and the ceiling is lower than it looks

Retrieval indexes **only** the trigger keywords. It never sees the prevention text.
Those keywords max out at twelve and come from the citation, the jurisdiction, and a
hand-maintained list of about thirty-six legal concept terms.

That's a hard ceiling. If a case is phrased using vocabulary outside those
thirty-odd terms, the patch simply cannot be retrieved, no matter how good its text
is. Retrieval quality is bounded by a hand-written word list, not by patch content.

Then there's the case that really makes your point. In Phase 3 we re-mined the store
and genuinely improved it: we broke up one kitchen-sink patch covering seven duties
into precise per-subsection patches, all verified, with none of the content lost. The
website-statement duty, the consumer-notice duty, the data-correction and appeal
duties each got their own properly-cited patch.

The patches got better and the retrieval got worse. The evidence for that is the
shape of the k-curve on the rebuilt store — how much patching improves the weak
student's graph, as we let it retrieve more patches:

| Patches retrieved | Improvement in L-GED | Rules recovered |
|---|---|---|
| k=1 | 7.0 | three binding rules |
| k=3 | 4.5 | one |
| k=5 | 11.5 | three |

That curve is not monotonic, and that is the whole point. Retrieving **three** patches
helps less than retrieving **one**, because the two extra patches at k=3 actively
displace the website-statement rule that k=1 had recovered. The three patches k=3
retrieves are three variants of the *same* risk-management duty — near-duplicates
crowding each other out.

So the content is all in the store; k=3 simply retrieves the wrong three patches. A
mining error could not produce that shape. Patch granularity and the retrieval budget
are coupled, and making patches more precise without widening or diversifying the
budget leaves the good ones unreachable.

That's what motivated the duty-diversified retrieval on the current branch — take at
most one patch per distinct duty so the slots don't fill up with near-duplicates. It
does work: on the same query, plain retrieval spends three of five slots on variants
of the same subsection and covers two duties, while diversified retrieval covers
five.

But there's a flaw underneath it that comes straight from not having defined breadth.
When we compute a patch's "duty key" from its citation, a span gets truncated to its
first subsection — so the seven-duty patch covering (a) through (g) and the one-duty
patch covering just (a) look like **the same duty** to the retrieval layer. It books
the broad patch into the (a) slot and then spends the remaining slots on (b), (d) and
(e) — duties the broad patch's text already covers. So diversification is optimising
a proxy rather than actual coverage, because breadth isn't something it can see.

That's where your three questions meet. Because we never defined breadth, retrieval
can't reason about it, and our own fix for the budget problem mishandles precisely
the broad patches that produced the effect in the first place.

One related thing worth knowing: the store now holds 21 patches citing that same
Colorado subsection group. Most of that is legitimate — three families across seven
duties — but not all. A patch citing subsection (f) and another citing the span
(f)–(g) are the same family and overlap in coverage, yet never merge, because our
dedup compares citations as text and a span reads differently from a single
subsection. They compete for the same slots.

---

## 5. What I'd change, in order

1. **Let arcs generate patches.** Statute-triggers-duty edges are case-independent,
   currently produce nothing, and still count against us in the score.
2. **Make breadth a real property of a patch**, starting with the cheap
   count-the-spanned-duties version, so retrieval can aim for actual duty coverage
   instead of counting distinct subsection keys.
3. **Scrub party names from the deterministic patch template.** Three patches leak
   them today, and one of those is our top-retrieved patch.
4. **Decide whether misgrounding belongs in the score.** It's one flag. Leaving it
   off means our headline metric ignores the error type we're calling novel; turning
   it on breaks comparability with our existing numbers. That's a decision, not a bug.
5. **Grow or replace the concept lexicon**, or index the patch prose alongside the
   keywords. Thirty-six hand-written terms is the ceiling on what retrieval can find.
6. **Re-tune k together with breadth.** We found k=3 best for the old broad store;
   there's no reason that carries over to the decomposed one.
