# M4 — TalentLens Developer Duties — teacher FIRACO reasoning

Unverified model output for legal review. Citations, facts, applications, and obligations may be incorrect. Text and node IDs below are preserved from the saved reference graph.

[Read case](../../../data/cases/M4_talentlens_developer_co.md) · [Review brief](../../PROF_PHILIPP_REVIEW.md)

Teacher: claude-opus-4-6. Source: data/outputs/graphs/M4_reference.json.

Source SHA-256: `2409e5a82008942d523b1083b13cc19e194b126872a5838a2c96a2a812bee423`.

## Facts (14)

### F1

HireLattice is a software company in Boulder, CO with 85 employees, doing business in the state

- **Polarity:** present
- **Support quote:** HireLattice Inc. is a software company in Boulder, Colorado, with 85 employees

### F2

HireLattice sells TalentLens, a model that scores job applicants resumes and online assessments

- **Polarity:** present
- **Support quote:** It sells 'TalentLens,' a model that scores job applicants resumes and online assessments

### F3

HireLattice built TalentLens by fine-tuning a third-party foundation model on two million historical hiring records

- **Polarity:** present
- **Support quote:** HireLattice built TalentLens by taking a general-purpose foundation model and fine-tuning it on two million historical hiring records

### F4

Forty Colorado employers use TalentLens scores to decide which applicants receive an interview

- **Polarity:** present
- **Support quote:** Forty Colorado employers use TalentLens scores to decide which applicants receive an interview

### F5

HireLattice provides only a two-page model card describing architecture and benchmark accuracy

- **Polarity:** present
- **Support quote:** HireLattice gives each customer a two-page model card that describes the models architecture and its accuracy on benchmark tests

### F6

No documentation of known discrimination limitations, training data summary, biases, intended/inappropriate uses, or monitoring guidance is provided

- **Polarity:** present
- **Support quote:** It provides no description of known limitations relating to discrimination, no summary of the training data or of known biases

### F7

HireLattice refused deployer requests for impact assessment information citing trade secrets

- **Polarity:** present
- **Support quote:** When customers have asked for information to complete their own impact assessments, HireLattice has refused, citing trade secrets

### F8

HireLattice website does not list TalentLens or describe risk management

- **Polarity:** present
- **Support quote:** HireLattice's website does not list TalentLens or describe how its risks are managed

### F9

December 2025 internal testing found TalentLens scores applicants over 55 materially lower than equally qualified younger applicants

- **Polarity:** present
- **Support quote:** internal testing found that TalentLens scores applicants older than 55 materially lower than younger applicants with the same qualifications

### F10

Engineers changed the model in January 2026 believing the age gap is closed

- **Polarity:** present
- **Support quote:** Engineers changed the model in January 2026 and believe the gap is closed

### F11

HireLattice did not notify customers, affected applicants, or any regulator of the discovered discrimination

- **Polarity:** present
- **Support quote:** HireLattice did not tell its customers, the applicants who had been scored, or any regulator

### F12

CEO claims HireLattice is not a developer because it only fine-tuned someone elses model

- **Polarity:** present
- **Support quote:** We only fine-tuned someone elses model, so we are not the developer

### F13

CEO claims compliance is deployers responsibility not HireLattices

- **Polarity:** present
- **Support quote:** Employers decide how to use the scores, so compliance is their responsibility, not ours

### F14

CEO believes finding and fixing the problem itself automatically protects from enforcement

- **Polarity:** present
- **Support quote:** because the company found and fixed the problem itself, it is automatically protected from enforcement

## Issues (5)

### I1

Whether HireLattice qualifies as a developer under CO AIA given it fine-tuned a third-party model

- **Status:** dispositive

### I2

Whether the two-page model card satisfies each documentation duty under section 6-1-1702(2)

- **Status:** dispositive

### I3

Whether HireLattice complies with the public statement requirement under section 6-1-1702(3)

- **Status:** dispositive

### I4

What the December 2025 age-discrimination discovery requires HireLattice to do, to whom, and by when under section 6-1-1704

- **Status:** dispositive

### I5

Whether either rebuttable presumption of reasonable care is available to HireLattice on these facts

- **Status:** dispositive

## Rules (12)

### R1

Developer definition: person doing business in state that develops or substantially modifies an AI system intended or known to be used as high-risk AI system

- **Citation:** CO AIA section 6-1-1701(6)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R2

High-risk AI system: any AI system that when deployed makes or is a substantial factor in making a consequential decision

- **Citation:** CO AIA section 6-1-1701(7)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R3

Consequential decision includes decisions affecting employment or employment opportunity

- **Citation:** CO AIA section 6-1-1701(3)(b)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R4

Substantial factor: factor that materially contributed to a consequential decision; human review based primarily on AI output does not negate

- **Citation:** CO AIA section 6-1-1701(9)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R5

Developer must provide deployers five categories of documentation: limitations, training data, intended/inappropriate uses, usage guidance, and impact assessment support

- **Citation:** CO AIA section 6-1-1702(2)(a)-(e)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R6

Developer must publish on website or public inventory a statement summarizing high-risk AI systems developed or substantially modified for use in state

- **Citation:** CO AIA section 6-1-1702(3)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R7

Developer shall use reasonable care to protect consumers from known or reasonably foreseeable risks of algorithmic discrimination

- **Citation:** CO AIA section 6-1-1702(1)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R8

Algorithmic discrimination: unlawful differential treatment or impact disfavoring individuals on basis of age or other protected classification

- **Citation:** CO AIA section 6-1-1701(1)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R9

Developer discovering algorithmic discrimination must notify AG and affected consumers within 90 days of discovery

- **Citation:** CO AIA section 6-1-1704
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R10

Developer rebuttable presumption of reasonable care requires compliance with all of section 6-1-1702

- **Citation:** CO AIA section 6-1-1702(4)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R11

Enforcement rebuttable presumption requires self-discovery of violation AND cure plus AG notification within 60 days

- **Citation:** CO AIA section 6-1-1706(4)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R12

Violations are deceptive trade practices; AG exclusive enforcement; penalties up to $20,000 per violation

- **Citation:** CO AIA section 6-1-1706(1)-(3)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

## Applications (9)

### A1

HireLattice does business in Colorado and substantially modified a third-party foundation model by fine-tuning it on 2M hiring records. TalentLens is sold to employers for interview screening, an employment consequential decision. HireLattice knew or had reason to know TalentLens would be used as a high-risk AI system. All elements of the developer definition are met. The CEO claim that fine-tuning is not development is legally incorrect because the statute expressly covers substantial modification.

- **Rule ref:** R1
- **Fact refs:** F1, F3, F4, F12
- **Issue ref:** I1
- **Result:** satisfied

### A2

TalentLens scores are used by 40 employers to decide which applicants receive interviews. This makes TalentLens a substantial factor in employment decisions, which are consequential decisions under section 6-1-1701(3)(b). TalentLens is therefore a high-risk AI system.

- **Rule ref:** R2
- **Fact refs:** F2, F4
- **Issue ref:** I1
- **Result:** satisfied

### A3

The model card describes only architecture and benchmark accuracy. It fails all five documentation requirements: (a) no known limitations re discrimination - violated; (b) no training data summary or known biases from the 2M hiring records - violated; (c) no intended or inappropriate uses - violated; (d) no usage, non-use, or monitoring guidance - violated; (e) affirmative refusal to provide impact assessment information citing trade secrets (no trade secret exception exists in the statute) - violated. The model card is wholly insufficient.

- **Rule ref:** R5
- **Fact refs:** F5, F6, F7
- **Issue ref:** I2
- **Result:** violated

### A4

HireLattice's website does not list TalentLens or describe how its risks are managed. Section 6-1-1702(3) requires a clear and readily accessible public statement summarizing high-risk AI systems. Complete failure to comply.

- **Rule ref:** R6
- **Fact refs:** F8
- **Issue ref:** I3
- **Result:** violated

### A5

TalentLens scoring applicants over 55 materially lower than equally qualified younger applicants constitutes differential impact disfavoring individuals on the basis of age. Age is a protected classification under federal (ADEA) and Colorado law. This meets the definition of algorithmic discrimination under section 6-1-1701(1).

- **Rule ref:** R8
- **Fact refs:** F9
- **Issue ref:** I4
- **Result:** satisfied

### A6

HireLattice discovered algorithmic discrimination in December 2025 but notified neither the AG nor affected consumers. Section 6-1-1704 requires both notifications within 90 days. The statute takes effect June 30, 2026; the 90-day clock will begin on that date for pre-effective-date discoveries. HireLattice must notify by approximately September 28, 2026. As of the analysis date, no steps have been taken toward compliance.

- **Rule ref:** R9
- **Fact refs:** F9, F11
- **Issue ref:** I4
- **Result:** violated

### A7

The section 6-1-1702(4) presumption requires compliance with all of section 6-1-1702. HireLattice has failed the documentation duties (section 6-1-1702(2)) and the public statement requirement (section 6-1-1702(3)). The presumption is therefore unavailable.

- **Rule ref:** R10
- **Fact refs:** F5, F6, F7, F8
- **Issue ref:** I5
- **Result:** violated

### A8

The enforcement presumption under section 6-1-1706(4) requires two conjunctive conditions: (a) self-discovery through own testing - satisfied; AND (b) cure of violation AND notification to AG within 60 days - NOT satisfied. HireLattice cured the technical issue in January 2026 but never notified the AG. The 60-day window from December 2025 discovery expired approximately February 2026. The CEO belief that self-discovery alone provides automatic protection is legally incorrect.

- **Rule ref:** R11
- **Fact refs:** F9, F10, F11, F14
- **Issue ref:** I5
- **Result:** violated

### A9

HireLattice failed to use reasonable care: it withheld documentation from deployers, refused impact assessment assistance, discovered age-based discrimination and concealed it from deployers, consumers, and the AG. This pattern of conduct falls far short of the reasonable care standard in section 6-1-1702(1).

- **Rule ref:** R7
- **Fact refs:** F6, F7, F9, F11
- **Issue ref:** I1
- **Result:** violated

## Conclusions (6)

### C1

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A1, A2

### C2

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A3

### C3

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A4

### C4

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A5, A6

### C5

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A7, A8

### C6

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A9

## Obligations (11)

### O1

Notify the Colorado Attorney General of the December 2025 age-discrimination discovery and the January 2026 cure under section 6-1-1704(a)

- **Required by:** R9
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** Within 90 days of June 30, 2026 (approx. September 28, 2026)

### O2

Notify all affected consumers (applicants over 55 scored by TalentLens) of the algorithmic discrimination under section 6-1-1704(b)

- **Required by:** R9
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** Within 90 days of June 30, 2026 (approx. September 28, 2026)

### O3

Provide deployers documentation of known limitations regarding algorithmic discrimination risks under section 6-1-1702(2)(a)

- **Required by:** R5
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** By June 30, 2026

### O4

Provide deployers documentation describing training data including summary of 2M hiring records and known biases under section 6-1-1702(2)(b)

- **Required by:** R5
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** By June 30, 2026

### O5

Provide deployers documentation of intended uses and known inappropriate uses under section 6-1-1702(2)(c)

- **Required by:** R5
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** By June 30, 2026

### O6

Provide deployers guidance on how to use, not use, and monitor TalentLens scores for consequential decisions under section 6-1-1702(2)(d)

- **Required by:** R5
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** By June 30, 2026

### O7

Provide deployers all additional documentation reasonably necessary for impact assessments; trade secret claims do not excuse this obligation under section 6-1-1702(2)(e)

- **Required by:** R5
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** By June 30, 2026

### O8

Publish on HireLattice website a clear and readily accessible statement summarizing TalentLens as a high-risk AI system under section 6-1-1702(3)

- **Required by:** R6
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** By June 30, 2026

### O9

Implement reasonable care measures to protect consumers from algorithmic discrimination including ongoing testing and monitoring under section 6-1-1702(1)

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** By June 30, 2026 and ongoing

### O10

Notify all 40 deployer-customers of the age-discrimination finding and January 2026 model change to enable deployer compliance with section 6-1-1703(2)(b)(III)

- **Required by:** R5
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** Immediately; no later than June 30, 2026

### O11

Engage counsel to assess whether voluntary early AG notification can partially preserve enforcement safe harbor under section 6-1-1706(4)

- **Required by:** R11
- **Status:** recommended
- **Jurisdiction:** Colorado
- **Deadline:** Not specified

## Graph connections (42)

### E1

- **Src:** F3
- **Dst:** I1
- **Type:** triggers
- **Justification:** Fine-tuning a foundation model raises the question of whether this constitutes substantial modification under the developer definition

### E2

- **Src:** F12
- **Dst:** I1
- **Type:** triggers
- **Justification:** CEO claim that fine-tuning does not make HireLattice a developer directly raises the developer status issue

### E3

- **Src:** F4
- **Dst:** I1
- **Type:** triggers
- **Justification:** Use by 40 Colorado employers for interview decisions establishes high-risk AI system status

### E4

- **Src:** R1
- **Dst:** A1
- **Type:** applies-to
- **Justification:** Developer definition applied to HireLattice fine-tuning facts

### E5

- **Src:** R2
- **Dst:** A2
- **Type:** applies-to
- **Justification:** High-risk AI system definition applied to TalentLens employment screening use

### E6

- **Src:** A1
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** HireLattice meets all elements of developer definition establishing developer status and obligations

### E7

- **Src:** A2
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** TalentLens meets high-risk AI system definition confirming developer obligations apply

### E8

- **Src:** F5
- **Dst:** I2
- **Type:** triggers
- **Justification:** Model card content raises question of whether it satisfies documentation duties

### E9

- **Src:** F6
- **Dst:** I2
- **Type:** triggers
- **Justification:** Absence of required documentation categories directly raises documentation compliance issue

### E10

- **Src:** F7
- **Dst:** I2
- **Type:** triggers
- **Justification:** Refusal to provide impact assessment information raises documentation duty compliance issue

### E11

- **Src:** R5
- **Dst:** A3
- **Type:** applies-to
- **Justification:** Five-part documentation duty applied to model card and refusal facts

### E12

- **Src:** A3
- **Dst:** C2
- **Type:** fails-element
- **Justification:** Model card fails all five documentation requirements

### E13

- **Src:** F8
- **Dst:** I3
- **Type:** triggers
- **Justification:** Absence of website listing raises public statement compliance issue

### E14

- **Src:** R6
- **Dst:** A4
- **Type:** applies-to
- **Justification:** Public statement requirement applied to website absence facts

### E15

- **Src:** A4
- **Dst:** C3
- **Type:** fails-element
- **Justification:** No public statement on website violates section 6-1-1702(3)

### E16

- **Src:** F9
- **Dst:** I4
- **Type:** triggers
- **Justification:** Discovery of age-based scoring disparity raises notification obligation issue

### E17

- **Src:** F11
- **Dst:** I4
- **Type:** triggers
- **Justification:** Failure to notify anyone raises question of compliance with notification duties

### E18

- **Src:** R8
- **Dst:** A5
- **Type:** applies-to
- **Justification:** Algorithmic discrimination definition applied to age-based scoring disparity

### E19

- **Src:** R9
- **Dst:** A6
- **Type:** applies-to
- **Justification:** Notification obligation applied to discovery and non-notification facts

### E20

- **Src:** A5
- **Dst:** C4
- **Type:** satisfies-element
- **Justification:** Age-based scoring disparity meets algorithmic discrimination definition

### E21

- **Src:** A6
- **Dst:** C4
- **Type:** fails-element
- **Justification:** Failure to notify AG and consumers violates section 6-1-1704

### E22

- **Src:** F14
- **Dst:** I5
- **Type:** triggers
- **Justification:** CEO belief in automatic protection raises rebuttable presumption availability issue

### E23

- **Src:** R10
- **Dst:** A7
- **Type:** applies-to
- **Justification:** Developer presumption requirements applied to documentation compliance facts

### E24

- **Src:** R11
- **Dst:** A8
- **Type:** applies-to
- **Justification:** Enforcement presumption requirements applied to self-discovery and non-notification facts

### E25

- **Src:** A7
- **Dst:** C5
- **Type:** fails-element
- **Justification:** Non-compliance with section 6-1-1702 precludes developer presumption

### E26

- **Src:** A8
- **Dst:** C5
- **Type:** fails-element
- **Justification:** Failure to notify AG within 60 days precludes enforcement presumption

### E27

- **Src:** R7
- **Dst:** A9
- **Type:** applies-to
- **Justification:** Reasonable care standard applied to pattern of withholding and concealment

### E28

- **Src:** A9
- **Dst:** C6
- **Type:** fails-element
- **Justification:** Pattern of conduct falls far short of reasonable care standard

### E29

- **Src:** R9
- **Dst:** O1
- **Type:** triggers
- **Justification:** Section 6-1-1704(a) requires AG notification upon discovery of algorithmic discrimination

### E30

- **Src:** R9
- **Dst:** O2
- **Type:** triggers
- **Justification:** Section 6-1-1704(b) requires consumer notification upon discovery of algorithmic discrimination

### E31

- **Src:** R5
- **Dst:** O3
- **Type:** triggers
- **Justification:** Section 6-1-1702(2)(a) requires documentation of known discrimination limitations

### E32

- **Src:** R5
- **Dst:** O4
- **Type:** triggers
- **Justification:** Section 6-1-1702(2)(b) requires training data documentation

### E33

- **Src:** R5
- **Dst:** O5
- **Type:** triggers
- **Justification:** Section 6-1-1702(2)(c) requires intended and inappropriate use documentation

### E34

- **Src:** R5
- **Dst:** O6
- **Type:** triggers
- **Justification:** Section 6-1-1702(2)(d) requires usage and monitoring guidance

### E35

- **Src:** R5
- **Dst:** O7
- **Type:** triggers
- **Justification:** Section 6-1-1702(2)(e) requires impact assessment support documentation

### E36

- **Src:** R6
- **Dst:** O8
- **Type:** triggers
- **Justification:** Section 6-1-1702(3) requires public website statement

### E37

- **Src:** R7
- **Dst:** O9
- **Type:** triggers
- **Justification:** Section 6-1-1702(1) requires reasonable care measures

### E38

- **Src:** R5
- **Dst:** O10
- **Type:** triggers
- **Justification:** Documentation duties and reasonable care require notifying deployers of model changes and discovered discrimination

### E39

- **Src:** R11
- **Dst:** O11
- **Type:** triggers
- **Justification:** Enforcement safe harbor analysis requires legal counsel assessment

### E40

- **Src:** F13
- **Dst:** I2
- **Type:** triggers
- **Justification:** CEO claim that compliance is deployers responsibility raises question of developer documentation duties

### E41

- **Src:** R3
- **Dst:** A2
- **Type:** applies-to
- **Justification:** Consequential decision definition confirms employment screening is covered

### E42

- **Src:** R12
- **Dst:** C6
- **Type:** applies-to
- **Justification:** Enforcement provisions establish penalties and consequences for violations
