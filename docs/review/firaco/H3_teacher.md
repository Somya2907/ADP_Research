# H3 — PathScore Bank, New York and Colorado — teacher FIRACO reasoning

Unverified model output for legal review. Citations, facts, applications, and obligations may be incorrect. Text and node IDs below are preserved from the saved reference graph.

[Read case](../../../data/cases/H3_pathscore_bank_nyc_co.md) · [Review brief](../../PROF_PHILIPP_REVIEW.md)

Teacher: claude-opus-4-6. Source: data/outputs/graphs/H3_reference.json.

Source SHA-256: `1bc72a9e8c339e20d3fdd63fbb8b190825ce5a70f4c2e16a4ef479fcd2f32b3a`.

The internal audit flags at least one rule below for a suspect NYC §20-875 citation. Other errors may also be present.

## Facts (16)

### F1

Veridian (Denver, 140 employees) develops PathScore; First Meridian (Charlotte, 9000 employees) licenses it

- **Polarity:** present
- **Support quote:** Veridian Talent Systems headquartered in Denver, 140 employees; First Meridian Bank headquartered in Charlotte, 9000 employees

### F2

PathScore is ML system scoring applicants 0-100; below 65 excluded with no human review

- **Polarity:** present
- **Support quote:** applicants and employees scoring below 65 do not advance, and no person reviews those outcomes

### F3

First Meridian uses PathScore in NYC branches since 2024 for teller hiring and promotion to assistant branch manager

- **Polarity:** present
- **Support quote:** In its New York City branches, since 2024, to screen external applicants for teller positions and current employees for promotion

### F4

First Meridian uses PathScore in Colorado branches (Denver, Boulder) since October 2025 for teller screening

- **Polarity:** present
- **Support quote:** In its Colorado branches in Denver and Boulder, since October 2025, to screen external applicants for teller positions

### F5

July 2025 audit conducted by Veridian Assurance Group, sister company of Veridian under same parent

- **Polarity:** present
- **Support quote:** audited in July 2025 by Veridian Assurance Group, a sister company of Veridian Talent Systems owned by the same parent

### F6

Audit used pooled historical data from nine customers; First Meridian provided none of its own data despite 1+ year of use

- **Polarity:** present
- **Support quote:** audit used historical data pooled from nine Veridian customers. First Meridian did not provide any of its own data

### F7

PathScore 4.0 released Jan 2026, retrained on 2025 data with new features; no audit on v4.0; Bank uses v4.0 since Feb 2026

- **Polarity:** present
- **Support quote:** January 2026 Veridian released PathScore 4.0, retrained on 2025 data with new scoring features. No audit has been performed on version 4.0

### F8

Audit summary on Veridian website; Bank careers page has link labeled 'Vendor information'; no distribution date on either page

- **Polarity:** present
- **Support quote:** Neither page states the date First Meridian began using PathScore

### F9

NYC teller postings give 10 business days notice of PathScore use and qualifications assessed but no alternative selection process instructions

- **Polarity:** present
- **Support quote:** They give no instructions for requesting an alternative selection process

### F10

NYC promotion candidates receive no notice of any kind about PathScore use

- **Polarity:** present
- **Support quote:** Employees considered for promotion receive no notice of any kind

### F11

Bank uses enterprise model-risk policy based on federal banking guidance; no impact assessment completed; no public AI statement

- **Polarity:** present
- **Support quote:** consistent with federal banking guidance on model risk management. It has completed no impact assessment

### F12

Colorado applicants not told AI screens them; no data correction or appeal process

- **Polarity:** present
- **Support quote:** Colorado applicants are not told that an AI system screens them. There is no process to correct data or to appeal

### F13

Veridian provided only marketing brochure; refused training data summary and limitations as confidential; no public use case inventory

- **Polarity:** present
- **Support quote:** declined to provide a summary of PathScore training data or its known limitations, calling them confidential

### F14

General counsel says vendor audit covers NYC and nothing to do for Colorado until June 30

- **Polarity:** present
- **Support quote:** The vendor audit covers us in New York, and Colorado is not in force until June 30, so there is nothing to do now

### F15

Veridian says LL 144 is not its problem as vendor and Colorado duties fall on deployer

- **Polarity:** present
- **Support quote:** We are a vendor, not an employer, so Local Law 144 is not our problem, and in Colorado the duties fall on whoever deploys

### F16

Analysis date is April 16, 2026; LL 144 in force since July 2023; CO AIA effective June 30, 2026; TRAIGA effective Jan 1, 2026

- **Polarity:** present
- **Support quote:** Not specified

## Issues (7)

### I1

Is the July 2025 bias audit valid for First Meridian NYC use considering auditor independence, data, and retraining?

- **Status:** dispositive

### I2

Are publication and notice practices sufficient under NYC LL 144 for applicants and promotion candidates?

- **Status:** dispositive

### I3

How are NYC LL 144 obligations allocated between First Meridian (employer) and Veridian (vendor)?

- **Status:** collateral

### I4

Does Colorado AIA apply to First Meridian Colorado use, on what timeline, and what must be in place?

- **Status:** dispositive

### I5

What does Veridian owe as a developer under Colorado AIA?

- **Status:** dispositive

### I6

Does banking model-risk policy satisfy Colorado NIST AI RMF requirement?

- **Status:** dispositive

### I7

Are the general counsel and vendor legal positions correct?

- **Status:** dispositive

## Rules (27)

### R1

AEDT definition: ML process issuing simplified output used to substantially assist or replace discretionary employment decisions

- **Citation:** NYC LL 144 Section 20-870; DCWP Rules Section 5-300
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R2

Bias audit required within one year of use; new audit required after substantial modification including retraining

- **Citation:** NYC LL 144 Section 20-871(a),(d); DCWP Rules Section 5-301(a)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R3

Independent auditor must have no financial interest in employer, employment agency, or AEDT developer/vendor

- **Citation:** NYC LL 144 Section 20-870 (independent auditor definition); DCWP Rules Section 5-300
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R4

Employer with historical data must provide it to auditor; may rely on others data only if own data provided or never used AEDT

- **Citation:** DCWP Rules Section 5-302(a)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R5

Scoring AEDT audit must calculate median score, scoring rate per category, impact ratio per category for sex, race/ethnicity, intersectional

- **Citation:** DCWP Rules Section 5-301(c)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R6

Employer must publish audit date, results summary, and distribution date on employment section of website clearly and conspicuously

- **Citation:** DCWP Rules Section 5-303(a),(b)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R7

Candidate notice 10 business days before use: AEDT use, qualifications assessed, alternative selection process instructions

- **Citation:** NYC LL 144 Section 20-871(b)(1); DCWP Rules Section 5-304(a),(b)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R8

Promotion candidate notice required 10 business days before use via written policy, posting, or mail/email

- **Citation:** NYC LL 144 Section 20-871(b)(1); DCWP Rules Section 5-304(c)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R9

> Flagged for review: the internal audit reports that the cited NYC §20-875 does not exist. Please verify both citation and proposition.

Penalties $500-$1500 per violation; each screening of single candidate may be separate violation

- **Citation:** NYC LL 144 Section 20-875
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R10

LL 144 applies based on candidate/employee location not employer HQ; covers hiring and promotion in NYC

- **Citation:** NYC LL 144 Section 20-874
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R11

Colorado AIA effective date June 30, 2026; not yet in force as of April 16, 2026

- **Citation:** CO AIA SB 24-205 as amended by SB 25B-004
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R12

High-risk AI system: makes or is substantial factor in consequential decision including employment; deployer defined as person doing business in state deploying such system

- **Citation:** CO AIA Section 6-1-1701(7),(3)(b),(5)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R13

Substantial factor: materially contributed to decision; human review insufficient if based primarily on AI output

- **Citation:** CO AIA Section 6-1-1701(9)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R14

Risk management program must be consistent with NIST AI RMF (AI 100-1) or substantially equivalent framework like ISO/IEC 42001

- **Citation:** CO AIA Section 6-1-1703(2)(a)(III)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R15

Impact assessment required before deployment or within 90 days of June 30 2026 for pre-existing systems; annually thereafter

- **Citation:** CO AIA Section 6-1-1703(2)(b)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R16

Deployer must notify consumer before consequential decision: AI use, purpose, contact info, plain-language description, public statement access

- **Citation:** CO AIA Section 6-1-1703(2)(e)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R17

Deployer must provide data correction opportunity and meaningful appeal opportunity for consequential decisions

- **Citation:** CO AIA Section 6-1-1703(2)(f)-(g)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R18

Deployer must publish website statement summarizing deployed high-risk AI systems and discrimination risk management

- **Citation:** CO AIA Section 6-1-1703(2)(d)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R19

Small deployer exception: fewer than 50 employees AND does not use own data to train; both conditions required

- **Citation:** CO AIA Section 6-1-1703(6)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R20

Developer must provide deployers documentation on limitations, training data, intended uses, monitoring guidance, and impact assessment support

- **Citation:** CO AIA Section 6-1-1702(2)(a)-(e)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R21

Developer must publish website statement summarizing high-risk AI systems developed and available in state

- **Citation:** CO AIA Section 6-1-1702(3)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R22

Developer must use reasonable care to protect consumers from known or foreseeable algorithmic discrimination risks

- **Citation:** CO AIA Section 6-1-1702(1)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R23

Violations are deceptive trade practices; AG exclusive enforcement; up to $20,000 per violation

- **Citation:** CO AIA Section 6-1-1706
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R24

Deployer or developer must notify AG and affected consumers within 90 days of discovering algorithmic discrimination

- **Citation:** CO AIA Section 6-1-1704
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R25

Consumer excludes individuals in employment context; TRAIGA consumer requirements do not apply to job applicants

- **Citation:** TX TRAIGA Section 551.001(2)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R26

Prohibits AI deployment with intent to unlawfully discriminate; requires intentional discrimination not mere disparate impact

- **Citation:** TX TRAIGA Section 551.051(a)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R27

TRAIGA preempts local AI regulations within Texas only; no effect on other states laws

- **Citation:** TX TRAIGA Section 551.201
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

## Applications (22)

### A1

PathScore is ML-based, produces a score (simplified output), and is used as sole determinant with no human review. Under DCWP Rules 5-300(i), relying solely on simplified output with no other factors makes it an AEDT.

- **Rule ref:** R1
- **Fact refs:** F2
- **Issue ref:** I1
- **Result:** satisfied

### A2

Veridian Assurance Group is a sister company under common parent with Veridian Talent Systems (the developer). Under Section 20-870 and DCWP Rules 5-300, an auditor with material indirect financial interest in the AEDT vendor is not independent. The audit is invalid on independence grounds.

- **Rule ref:** R3
- **Fact refs:** F5
- **Issue ref:** I1
- **Result:** violated

### A3

First Meridian used PathScore in NYC since 2024 (over a year before audit) but provided no historical data. Under DCWP Rules 5-302(a), an employer that has used the AEDT may rely on others data only if it provided its own data. First Meridian neither provided data nor qualifies as never having used the AEDT.

- **Rule ref:** R4
- **Fact refs:** F3, F6
- **Issue ref:** I1
- **Result:** violated

### A4

PathScore 4.0 was retrained on 2025 data with new features in January 2026. Under Section 20-871(d)(2), retraining on new data is a substantial modification requiring a new bias audit. No audit exists for v4.0. First Meridian has used v4.0 since February 2026 without any valid audit.

- **Rule ref:** R2
- **Fact refs:** F7
- **Issue ref:** I1
- **Result:** violated

### A5

The July 2025 audit fails on three independent grounds: non-independent auditor, missing employer historical data, and post-audit retraining. First Meridian has no valid bias audit for its current NYC use of PathScore 4.0.

- **Rule ref:** R2
- **Fact refs:** F5, F6, F7
- **Issue ref:** I1
- **Result:** violated

### A6

Neither Veridian nor First Meridian website states the distribution date (when First Meridian began using PathScore). DCWP Rules 5-303(a)(2) requires publication of the distribution date. Additionally, a link labeled 'Vendor information' does not clearly identify itself as linking to bias audit results per 5-303(b).

- **Rule ref:** R6
- **Fact refs:** F8
- **Issue ref:** I2
- **Result:** violated

### A7

NYC teller postings identify PathScore and qualifications but omit instructions for requesting an alternative selection process. DCWP Rules 5-304(a) requires such instructions even if no alternative is available.

- **Rule ref:** R7
- **Fact refs:** F9
- **Issue ref:** I2
- **Result:** violated

### A8

Promotion candidates receive no notice whatsoever. Section 20-871(b)(1) and DCWP Rules 5-304(c) require notice to employees considered for promotion at least 10 business days before AEDT use. Complete absence of notice is a clear violation.

- **Rule ref:** R8
- **Fact refs:** F10
- **Issue ref:** I2
- **Result:** violated

### A9

LL 144 applies based on candidate/employee location. NYC-based applicants and employees are covered. First Meridian as employer bears primary compliance obligations. Veridian as vendor has no direct LL 144 obligations but its corporate structure caused the auditor independence failure.

- **Rule ref:** R10
- **Fact refs:** F1, F3
- **Issue ref:** I3
- **Result:** satisfied

### A10

PathScore makes employment decisions (consequential decisions per 6-1-1701(3)(b)) for Colorado applicants. Below-65 candidates are excluded with no human review, making PathScore the sole decision-maker. It is a high-risk AI system. First Meridian operates in Colorado and is a deployer.

- **Rule ref:** R12
- **Fact refs:** F2, F4
- **Issue ref:** I4
- **Result:** satisfied

### A11

First Meridian has 9,000 employees, far exceeding the 50-employee threshold in 6-1-1703(6)(a). The small deployer exception is unavailable. All deployer obligations apply.

- **Rule ref:** R19
- **Fact refs:** F1
- **Issue ref:** I4
- **Result:** violated

### A12

PathScore deployed in Colorado since October 2025 (before June 30, 2026). Impact assessment required within 90 days of June 30, 2026 (by Sept 28, 2026). None completed or in progress. While deadline has not passed, no preparation is underway.

- **Rule ref:** R15
- **Fact refs:** F4, F11
- **Issue ref:** I4
- **Result:** violated

### A13

Colorado applicants receive no notice of AI screening. Section 6-1-1703(2)(e) requires pre-decision notice with five specified elements. No notice procedures exist. Will be in violation on June 30, 2026.

- **Rule ref:** R16
- **Fact refs:** F12
- **Issue ref:** I4
- **Result:** violated

### A14

No data correction or appeal process exists for Colorado applicants. Sections 6-1-1703(2)(f) and (g) require both. Will be in violation on June 30, 2026.

- **Rule ref:** R17
- **Fact refs:** F12
- **Issue ref:** I4
- **Result:** violated

### A15

First Meridian has no public statement on its website about deployed high-risk AI systems or discrimination risk management. Section 6-1-1703(2)(d) requires this. Will be in violation on June 30, 2026.

- **Rule ref:** R18
- **Fact refs:** F11
- **Issue ref:** I4
- **Result:** violated

### A16

Veridian refused to provide training data summary and known limitations, citing confidentiality. Section 6-1-1702(2) requires developers to make available documentation on limitations, training data, intended uses, monitoring guidance, and impact assessment support. Confidentiality is not a statutory defense. Will be in violation on June 30, 2026.

- **Rule ref:** R20
- **Fact refs:** F13
- **Issue ref:** I5
- **Result:** violated

### A17

Veridian website does not list high-risk AI systems it sells. Section 6-1-1702(3) requires a public statement summarizing high-risk AI systems developed and available in the state. Will be in violation on June 30, 2026.

- **Rule ref:** R21
- **Fact refs:** F13
- **Issue ref:** I5
- **Result:** violated

### A18

Federal banking model-risk guidance (e.g., SR 11-7) addresses statistical model validation, not AI-specific risks like algorithmic discrimination, fairness, and transparency. Section 6-1-1703(2)(a)(III) requires consistency with NIST AI 100-1 or substantially equivalent AI risk management framework like ISO/IEC 42001. Banking guidance is not an AI risk management framework and does not satisfy this requirement.

- **Rule ref:** R14
- **Fact refs:** F11
- **Issue ref:** I6
- **Result:** violated

### A19

General counsel claim that vendor audit covers NYC is wrong: audit fails independence (sister company auditor), data (no employer data provided), and currency (post-retraining). Employer cannot delegate compliance to vendor.

- **Rule ref:** R2
- **Fact refs:** F14, F5, F6, F7
- **Issue ref:** I7
- **Result:** violated

### A20

General counsel claim nothing to do for Colorado is practically wrong. While CO AIA not yet in force, effective date is 75 days away. Building NIST-aligned risk management program, impact assessment, notice procedures, correction/appeal processes, and public statement requires significant lead time. Current inaction virtually guarantees non-compliance.

- **Rule ref:** R11
- **Fact refs:** F14, F11, F12
- **Issue ref:** I7
- **Result:** violated

### A21

Veridian claim that Colorado duties fall only on deployer is legally incorrect. Section 6-1-1702 imposes independent developer obligations including documentation provision and public use case inventory. Veridian has separate statutory duties it cannot disclaim.

- **Rule ref:** R20
- **Fact refs:** F15, F13
- **Issue ref:** I7
- **Result:** violated

### A22

TRAIGA consumer definition excludes employment contexts. TRAIGA imposes no bias audit, impact assessment, notice, or risk management requirements on private employers for hiring tools. Not applicable to these facts.

- **Rule ref:** R25
- **Fact refs:** F1, F16
- **Issue ref:** I4
- **Result:** satisfied

## Conclusions (7)

### C1

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A2, A3, A4, A5

### C2

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A6, A7, A8

### C3

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A10, A11, A12, A13, A14, A15, A18

### C4

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A16, A17

### C5

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A18

### C6

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A19, A20, A21

### C7

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A22

## Obligations (15)

### O1

Commission new independent bias audit of PathScore 4.0 by truly independent auditor with First Meridian historical data

- **Required by:** R2
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Immediately; AEDT use without valid audit is ongoing violation

### O2

Suspend PathScore use in NYC or accept documented ongoing violation risk until valid audit completed

- **Required by:** R2
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Immediately

### O3

Publish compliant bias audit results on employment section of First Meridian website with distribution date and clear audit link label

- **Required by:** R6
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Before resuming AEDT use after new audit

### O4

Add alternative selection process request instructions to all NYC teller job postings

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Immediately

### O5

Implement promotion candidate notice for NYC employees at least 10 business days before PathScore use

- **Required by:** R8
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Immediately; no promotions screened via PathScore until notice given

### O6

Develop NIST AI 100-1 or ISO/IEC 42001 aligned risk management program replacing banking model-risk policy for AI compliance

- **Required by:** R14
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O7

Complete impact assessment of PathScore for Colorado deployment including all elements of Section 6-1-1701(8)

- **Required by:** R15
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-09-28

### O8

Formally demand all required developer documentation from Veridian under Section 6-1-1702(2)

- **Required by:** R20
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** Immediately to enable compliance preparation

### O9

Implement pre-decision consumer notice procedures for all Colorado applicants with five required elements

- **Required by:** R16
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O10

Create data correction mechanism for Colorado applicants whose data PathScore processes

- **Required by:** R17
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O11

Create meaningful appeal process for Colorado applicants rejected based on PathScore scores

- **Required by:** R17
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O12

Publish website statement summarizing PathScore deployment and algorithmic discrimination risk management

- **Required by:** R18
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O13

Veridian must provide all required developer documentation to First Meridian and all deployers per Section 6-1-1702(2)

- **Required by:** R20
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O14

Veridian must publish use case inventory on website summarizing PathScore and other high-risk AI systems

- **Required by:** R21
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O15

Veridian must exercise reasonable care to evaluate PathScore 4.0 for algorithmic discrimination risks

- **Required by:** R22
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

## Graph connections (70)

### E1

- **Src:** F2
- **Dst:** I1
- **Type:** triggers
- **Justification:** PathScore as ML scoring tool triggers AEDT classification analysis

### E2

- **Src:** F5
- **Dst:** I1
- **Type:** triggers
- **Justification:** Sister company auditor raises independence question

### E3

- **Src:** F6
- **Dst:** I1
- **Type:** triggers
- **Justification:** Missing employer historical data raises data requirement question

### E4

- **Src:** F7
- **Dst:** I1
- **Type:** triggers
- **Justification:** Post-audit retraining raises audit currency question

### E5

- **Src:** R1
- **Dst:** A1
- **Type:** applies-to
- **Justification:** AEDT definition applied to PathScore characteristics

### E6

- **Src:** R3
- **Dst:** A2
- **Type:** applies-to
- **Justification:** Independence requirement applied to Veridian Assurance Group

### E7

- **Src:** A2
- **Dst:** C1
- **Type:** fails-element
- **Justification:** Auditor independence failure invalidates audit

### E8

- **Src:** R4
- **Dst:** A3
- **Type:** applies-to
- **Justification:** Historical data requirement applied to First Meridian failure to provide data

### E9

- **Src:** A3
- **Dst:** C1
- **Type:** fails-element
- **Justification:** Data deficiency independently invalidates audit

### E10

- **Src:** R2
- **Dst:** A4
- **Type:** applies-to
- **Justification:** Retraining audit requirement applied to PathScore 4.0

### E11

- **Src:** A4
- **Dst:** C1
- **Type:** fails-element
- **Justification:** Post-retraining use without new audit independently invalidates compliance

### E12

- **Src:** F8
- **Dst:** I2
- **Type:** triggers
- **Justification:** Missing distribution date and unclear link trigger publication analysis

### E13

- **Src:** F9
- **Dst:** I2
- **Type:** triggers
- **Justification:** Missing alternative process instructions trigger notice analysis

### E14

- **Src:** F10
- **Dst:** I2
- **Type:** triggers
- **Justification:** Absent promotion notice triggers notice analysis

### E15

- **Src:** R6
- **Dst:** A6
- **Type:** applies-to
- **Justification:** Publication requirements applied to First Meridian website practices

### E16

- **Src:** A6
- **Dst:** C2
- **Type:** fails-element
- **Justification:** Missing distribution date and unclear link label violate publication rules

### E17

- **Src:** R7
- **Dst:** A7
- **Type:** applies-to
- **Justification:** Candidate notice requirements applied to teller postings

### E18

- **Src:** A7
- **Dst:** C2
- **Type:** fails-element
- **Justification:** Missing alternative process instructions violate notice rules

### E19

- **Src:** R8
- **Dst:** A8
- **Type:** applies-to
- **Justification:** Promotion notice requirements applied to absent employee notice

### E20

- **Src:** A8
- **Dst:** C2
- **Type:** fails-element
- **Justification:** Complete absence of promotion notice is clear violation

### E21

- **Src:** R10
- **Dst:** A9
- **Type:** applies-to
- **Justification:** Geographic applicability rule confirms NYC jurisdiction over First Meridian

### E22

- **Src:** F4
- **Dst:** I4
- **Type:** triggers
- **Justification:** Colorado deployment triggers CO AIA applicability analysis

### E23

- **Src:** R12
- **Dst:** A10
- **Type:** applies-to
- **Justification:** High-risk AI system definition applied to PathScore Colorado use

### E24

- **Src:** R19
- **Dst:** A11
- **Type:** applies-to
- **Justification:** Small deployer exception tested against First Meridian 9000 employees

### E25

- **Src:** A11
- **Dst:** C3
- **Type:** fails-element
- **Justification:** 9000 employees exceeds 50-employee threshold; exception unavailable

### E26

- **Src:** R15
- **Dst:** A12
- **Type:** applies-to
- **Justification:** Impact assessment requirement applied to pre-existing Colorado deployment

### E27

- **Src:** A12
- **Dst:** C3
- **Type:** fails-element
- **Justification:** No impact assessment completed or in preparation

### E28

- **Src:** R16
- **Dst:** A13
- **Type:** applies-to
- **Justification:** Consumer notice requirement applied to Colorado applicant screening

### E29

- **Src:** A13
- **Dst:** C3
- **Type:** fails-element
- **Justification:** No notice procedures exist for Colorado applicants

### E30

- **Src:** R17
- **Dst:** A14
- **Type:** applies-to
- **Justification:** Data correction and appeal requirements applied to Colorado deployment

### E31

- **Src:** A14
- **Dst:** C3
- **Type:** fails-element
- **Justification:** No correction or appeal process exists

### E32

- **Src:** R18
- **Dst:** A15
- **Type:** applies-to
- **Justification:** Public statement requirement applied to First Meridian website

### E33

- **Src:** A15
- **Dst:** C3
- **Type:** fails-element
- **Justification:** No public AI statement on website

### E34

- **Src:** F13
- **Dst:** I5
- **Type:** triggers
- **Justification:** Veridian refusal to provide documentation triggers developer obligation analysis

### E35

- **Src:** R20
- **Dst:** A16
- **Type:** applies-to
- **Justification:** Developer documentation requirements applied to Veridian refusal

### E36

- **Src:** A16
- **Dst:** C4
- **Type:** fails-element
- **Justification:** Veridian refusal to provide documentation violates developer duties

### E37

- **Src:** R21
- **Dst:** A17
- **Type:** applies-to
- **Justification:** Developer public inventory requirement applied to Veridian website

### E38

- **Src:** A17
- **Dst:** C4
- **Type:** fails-element
- **Justification:** No public use case inventory on Veridian website

### E39

- **Src:** R14
- **Dst:** A18
- **Type:** applies-to
- **Justification:** NIST AI RMF requirement applied to banking model-risk policy

### E40

- **Src:** A18
- **Dst:** C5
- **Type:** fails-element
- **Justification:** Banking model-risk guidance is not NIST AI 100-1 or equivalent AI framework

### E41

- **Src:** F14
- **Dst:** I7
- **Type:** triggers
- **Justification:** General counsel position triggers legal correctness analysis

### E42

- **Src:** F15
- **Dst:** I7
- **Type:** triggers
- **Justification:** Veridian position triggers legal correctness analysis

### E43

- **Src:** A19
- **Dst:** C6
- **Type:** fails-element
- **Justification:** GC NYC position wrong on three independent grounds

### E44

- **Src:** A20
- **Dst:** C6
- **Type:** fails-element
- **Justification:** GC Colorado position practically wrong given 75-day preparation window

### E45

- **Src:** A21
- **Dst:** C6
- **Type:** fails-element
- **Justification:** Veridian Colorado position legally wrong; developer has independent statutory duties

### E46

- **Src:** R25
- **Dst:** A22
- **Type:** applies-to
- **Justification:** TRAIGA consumer definition excludes employment context

### E47

- **Src:** A22
- **Dst:** C7
- **Type:** satisfies-element
- **Justification:** TRAIGA not applicable to employment screening facts

### E48

- **Src:** R9
- **Dst:** O1
- **Type:** triggers
- **Justification:** Per-candidate violation penalties make immediate audit remediation urgent

### E49

- **Src:** R2
- **Dst:** O1
- **Type:** triggers
- **Justification:** Bias audit requirement mandates new audit for PathScore 4.0

### E50

- **Src:** R6
- **Dst:** O3
- **Type:** triggers
- **Justification:** Publication requirements mandate compliant website disclosure

### E51

- **Src:** R7
- **Dst:** O4
- **Type:** triggers
- **Justification:** Notice requirements mandate alternative process instructions

### E52

- **Src:** R8
- **Dst:** O5
- **Type:** triggers
- **Justification:** Promotion notice requirement mandates employee notification

### E53

- **Src:** R14
- **Dst:** O6
- **Type:** triggers
- **Justification:** NIST AI RMF requirement mandates new risk management program

### E54

- **Src:** R15
- **Dst:** O7
- **Type:** triggers
- **Justification:** Impact assessment requirement mandates completion by Sept 28, 2026

### E55

- **Src:** R20
- **Dst:** O8
- **Type:** triggers
- **Justification:** Developer documentation requirement supports deployer demand for documentation

### E56

- **Src:** R16
- **Dst:** O9
- **Type:** triggers
- **Justification:** Consumer notice requirement mandates Colorado notice procedures

### E57

- **Src:** R17
- **Dst:** O10
- **Type:** triggers
- **Justification:** Data correction requirement mandates correction mechanism

### E58

- **Src:** R17
- **Dst:** O11
- **Type:** triggers
- **Justification:** Appeal requirement mandates appeal process

### E59

- **Src:** R18
- **Dst:** O12
- **Type:** triggers
- **Justification:** Public statement requirement mandates website disclosure

### E60

- **Src:** R20
- **Dst:** O13
- **Type:** triggers
- **Justification:** Developer documentation obligation on Veridian

### E61

- **Src:** R21
- **Dst:** O14
- **Type:** triggers
- **Justification:** Developer public inventory obligation on Veridian

### E62

- **Src:** R22
- **Dst:** O15
- **Type:** triggers
- **Justification:** Developer reasonable care obligation on Veridian

### E63

- **Src:** C1
- **Dst:** O1
- **Type:** triggers
- **Justification:** Audit invalidity conclusion triggers new audit obligation

### E64

- **Src:** C1
- **Dst:** O2
- **Type:** triggers
- **Justification:** Audit invalidity conclusion triggers suspension consideration

### E65

- **Src:** C2
- **Dst:** O3
- **Type:** triggers
- **Justification:** Publication non-compliance triggers publication remediation

### E66

- **Src:** C2
- **Dst:** O4
- **Type:** triggers
- **Justification:** Notice non-compliance triggers notice remediation

### E67

- **Src:** C2
- **Dst:** O5
- **Type:** triggers
- **Justification:** Promotion notice non-compliance triggers promotion notice implementation

### E68

- **Src:** C3
- **Dst:** O6
- **Type:** triggers
- **Justification:** Colorado non-compliance triggers risk management program development

### E69

- **Src:** C4
- **Dst:** O13
- **Type:** triggers
- **Justification:** Veridian non-compliance triggers documentation provision obligation

### E70

- **Src:** C4
- **Dst:** O14
- **Type:** triggers
- **Justification:** Veridian non-compliance triggers public inventory obligation
