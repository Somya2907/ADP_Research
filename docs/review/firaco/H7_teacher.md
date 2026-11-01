# H7 — CredenScore Nurse Staffing, Three States — teacher FIRACO reasoning

Unverified model output for legal review. Citations, facts, applications, and obligations may be incorrect. Text and node IDs below are preserved from the saved reference graph.

[Read case](../../../data/cases/H7_credenscore_nursing_multistate.md) · [Review brief](../../PROF_PHILIPP_REVIEW.md)

Teacher: claude-opus-4-6. Source: data/outputs/graphs/H7_reference.json.

Source SHA-256: `6679a541934d0b3f0362c9ca6275f87ba5d178a03f9d8b410e26530abe96fa38`.

The internal audit flags at least one rule below for a suspect NYC §20-875 citation. Other errors may also be present.

## Facts (12)

### F1

ShiftBridge Health develops CredenScore, an AI nurse-scoring system, headquartered in Chicago with 450 employees

- **Polarity:** present
- **Support quote:** ShiftBridge Health develops CredenScore, a system that scores nurses applying for staff positions

### F2

Empire Mercy operates NYC hospitals, weights CredenScore at 50% (more than any other criterion), uses it for hiring and promotion

- **Polarity:** present
- **Support quote:** Its hiring rubric gives the CredenScore result 50% of the total weight, more than any other criterion

### F3

Rocky Vista Health operates in Colorado with 3,000 FTEs, auto-rejects applicants below CredenScore cutoff, has used it since 2025

- **Polarity:** present
- **Support quote:** Rocky Vista Health operates hospitals in Colorado and has 3,000 full-time employees. Applicants scoring below a cutoff are rejected automatically

### F4

Bexar County Hospital District is a Texas governmental entity using CredenScore to shortlist nurse applicants

- **Polarity:** present
- **Support quote:** Bexar County Hospital District is a public hospital district in Texas, a governmental entity

### F5

February 2025 bias audit by independent Tolland Review Partners using pooled historical data including Empire Mercy data; no audit since

- **Polarity:** present
- **Support quote:** CredenScore was audited in February 2025 by Tolland Review Partners... No audit has been done since

### F6

Empire Mercy posts audit summary and distribution date on careers page; notifies external applicants 10+ business days before screening; no notice to promotion candidates

- **Polarity:** present
- **Support quote:** Nurses considered for promotion receive no notice

### F7

Rocky Vista relies on HIPAA security + ISO 27001; uses generic ShiftBridge impact assessment; no applicant notice, no appeal, no data correction

- **Polarity:** present
- **Support quote:** Rocky Vista describes its AI governance as our HIPAA security program plus ISO/IEC 27001 certification

### F8

ShiftBridge provides limitation docs and training data summary but no intended/inappropriate use docs, no monitoring guidance, no public listing of high-risk systems

- **Polarity:** present
- **Support quote:** It provides nothing on intended or inappropriate uses and nothing on how staff should use or monitor the scores

### F9

No evidence of intent to discriminate or cause harm by Bexar County

- **Polarity:** present
- **Support quote:** Nothing suggests any intent to discriminate or cause harm

### F10

ShiftBridge claims one compliance package satisfies all three states

- **Polarity:** present
- **Support quote:** One compliance package satisfies all three states. Our audit and our impact assessment travel with the product

### F11

Bexar County operates AskBexar AI chatbot for public without AI disclosure and AI discharge-planning tool without patient disclosure

- **Polarity:** present
- **Support quote:** AskBexar, an AI chatbot that answers questions from patients and the public on its website, without stating that it is an AI system

### F12

Operative analysis date is April 16, 2026; CO AIA effective June 30, 2026; NYC LL 144 in force since July 2023; TX TRAIGA in force since Jan 2026

- **Polarity:** present
- **Support quote:** Not specified

## Issues (7)

### I1

Is CredenScore an AEDT under NYC LL 144 at Empire Mercy, and is the February 2025 audit current as of April 2026?

- **Status:** dispositive

### I2

Are Empire Mercy publication and notice practices sufficient for both applicants and promotion candidates under NYC LL 144?

- **Status:** dispositive

### I3

Does Colorado AIA apply to Rocky Vista, on what timeline, and are its governance framework and vendor impact assessment sufficient?

- **Status:** dispositive

### I4

What does ShiftBridge owe as a developer under Colorado AIA and what is missing?

- **Status:** dispositive

### I5

Does Texas TRAIGA require anything of Bexar County for its hiring use of CredenScore?

- **Status:** dispositive

### I6

Do AskBexar chatbot and discharge-planning tool create Texas disclosure obligations for Bexar County?

- **Status:** dispositive

### I7

Is ShiftBridge one compliance package claim legally correct?

- **Status:** dispositive

## Rules (21)

### R1

AEDT definition: computational process from ML/AI issuing simplified output used to substantially assist or replace discretionary decision making for employment decisions

- **Citation:** NYC LL 144 Section 20-870; DCWP Rules Section 5-300
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R2

Bias audit must be conducted no more than one year prior to use of AEDT; AEDT may not be used if more than one year since most recent audit

- **Citation:** NYC LL 144 Section 20-871(a)(1); DCWP Rules Section 5-301(a)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R3

Bias audit must be by independent auditor, calculate selection rates and impact ratios for EEO-1 categories; employer using pooled data must contribute own data

- **Citation:** NYC LL 144 Section 20-871(b); DCWP Rules Section 5-302
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R4

Notice to candidates and employees at least 10 business days before AEDT use, covering both hiring and promotion, including alternative process instructions

- **Citation:** NYC LL 144 Section 20-872; DCWP Rules Section 5-304(a)-(c)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R5

Bias audit summary and distribution date must be posted on employment section of website, retained 6 months after latest use

- **Citation:** NYC LL 144 Section 20-873; DCWP Rules Section 5-303
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R6

High-risk AI system: makes or is substantial factor in consequential decisions including employment; human review based primarily on AI output does not negate

- **Citation:** Colorado AIA Section 6-1-1701(3)(b), (7), (9)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R7

Deployer risk management program must be consistent with NIST AI RMF 1.0 or substantially equivalent AI framework like ISO/IEC 42001; HIPAA and ISO 27001 are insufficient

- **Citation:** Colorado AIA Section 6-1-1703(2)(a)(III)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R8

Deployer must complete deployer-specific impact assessment before deployment or within 90 days of effective date for pre-existing systems, annually thereafter

- **Citation:** Colorado AIA Section 6-1-1703(2)(b); Section 6-1-1701(8)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R9

Deployer must notify consumers before AI-assisted consequential decision, provide data correction opportunity, and meaningful appeal opportunity

- **Citation:** Colorado AIA Section 6-1-1703(2)(e)-(g)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R10

Developer must provide deployers documentation on limitations, training data, intended/inappropriate uses, use/monitoring guidance, and impact assessment support

- **Citation:** Colorado AIA Section 6-1-1702(2)(a)-(e)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R11

Developer must publish on website a summary of high-risk AI systems developed or substantially modified

- **Citation:** Colorado AIA Section 6-1-1702(3)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R12

Small deployer exception: fewer than 50 FTEs AND does not use own data to train; both conditions required

- **Citation:** Colorado AIA Section 6-1-1703(6)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R13

Prohibition on deploying AI with intent to unlawfully discriminate; requires proof of intent, disparate impact alone insufficient

- **Citation:** Texas TRAIGA Section 551.051(a)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R14

Government entity deploying AI to interact with consumers must disclose AI interaction before or at time of interaction

- **Citation:** Texas TRAIGA Section 551.101
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R15

Healthcare provider using AI in patient service or treatment must disclose to patient on date of service

- **Citation:** Texas TRAIGA Section 551.102
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R16

Consumer excludes individuals acting in employment context; job applicants are not consumers under TRAIGA

- **Citation:** Texas TRAIGA Section 551.001(2)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R17

Safe harbor for substantial compliance with NIST AI RMF or other recognized AI governance standards

- **Citation:** Texas TRAIGA Section 551.301(d)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R18

> Flagged for review: the internal audit reports that the cited NYC §20-875 does not exist. Please verify both citation and proposition.

Each instance of using non-compliant AEDT to screen a single candidate may be a separate violation; penalties $500-$1,500 per violation

- **Citation:** NYC LL 144 Section 20-875(b)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R19

Violations are deceptive trade practices; AG exclusive enforcement; up to $20,000 per violation; rebuttable presumption for self-discovery and 60-day cure

- **Citation:** Colorado AIA Section 6-1-1706
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R20

AG exclusive enforcement; $10,000-$200,000 per violation accruing daily; safe harbor for internal discovery and cure; 60-day cure notice

- **Citation:** Texas TRAIGA Section 551.301(a)-(c),(e)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R21

Developer must use reasonable care to protect consumers from known or reasonably foreseeable risks of algorithmic discrimination

- **Citation:** Colorado AIA Section 6-1-1702(1)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

## Applications (19)

### A1

CredenScore is a computational process from ML/AI issuing a simplified output (score). Empire Mercy weights it at 50%, more than any other criterion, satisfying DCWP Rules 5-300(ii) definition of substantially assist. Used for both hiring and promotion (employment decisions). CredenScore is an AEDT.

- **Rule ref:** R1
- **Fact refs:** F2
- **Issue ref:** I1
- **Result:** satisfied

### A2

The most recent bias audit was February 2025. As of April 2026, more than 14 months have elapsed, exceeding the one-year maximum under Section 20-871(a)(1) and DCWP Rules 5-301(a). The audit is expired and Empire Mercy may not use CredenScore.

- **Rule ref:** R2
- **Fact refs:** F5, F12
- **Issue ref:** I1
- **Result:** violated

### A3

Tolland Review Partners has no financial or employment ties to ShiftBridge or hospitals and was not involved in building CredenScore, satisfying independence requirements. Empire Mercy contributed its own historical data to the pooled audit, satisfying DCWP Rules 5-302(a). The February 2025 audit was validly conducted when performed.

- **Rule ref:** R3
- **Fact refs:** F5
- **Issue ref:** I1
- **Result:** satisfied

### A4

External applicant notice satisfies Section 20-872: provided 10+ business days before screening, identifies AEDT use and qualifications assessed, includes alternative process instructions. However, promotion candidates receive no notice whatsoever, violating Section 20-872(a)(1) and DCWP Rules 5-304(c) which explicitly require notice to employees considered for promotion.

- **Rule ref:** R4
- **Fact refs:** F6
- **Issue ref:** I2
- **Result:** partial

### A5

Empire Mercy posts audit summary and distribution date in a clearly labeled section of its careers page, satisfying Section 20-873 and DCWP Rules 5-303 in form. However, the underlying audit is stale, making continued AEDT use unlawful regardless.

- **Rule ref:** R5
- **Fact refs:** F6
- **Issue ref:** I2
- **Result:** satisfied

### A6

CredenScore auto-rejects applicants below a cutoff, making it the decision-maker for employment (a consequential decision under 6-1-1701(3)(b)). It is a high-risk AI system under 6-1-1701(7). Rocky Vista is a deployer under 6-1-1701(5).

- **Rule ref:** R6
- **Fact refs:** F3
- **Issue ref:** I3
- **Result:** satisfied

### A7

Rocky Vista has 3,000 FTEs, far exceeding the 50-employee threshold in 6-1-1703(6)(a). The small deployer exception does not apply; Rocky Vista must comply with all deployer obligations.

- **Rule ref:** R12
- **Fact refs:** F3
- **Issue ref:** I3
- **Result:** satisfied

### A8

Rocky Vista relies on HIPAA security and ISO/IEC 27001. Section 6-1-1703(2)(a)(III) requires consistency with NIST AI RMF 1.0 or substantially equivalent AI risk management framework like ISO/IEC 42001. HIPAA is a healthcare data security framework and ISO 27001 is an information security standard; neither is an AI risk management framework. Both are explicitly identified as insufficient in the authoritative source.

- **Rule ref:** R7
- **Fact refs:** F7
- **Issue ref:** I3
- **Result:** violated

### A9

Rocky Vista uses a generic ShiftBridge document that does not describe Rocky Vista deployment context. Section 6-1-1701(8) requires deployer-specific elements including deployment context, risk analysis, outputs description, limitations, and governance processes. A generic vendor document fails virtually every element. For pre-existing deployments, the impact assessment is due within 90 days of June 30, 2026 (by September 28, 2026).

- **Rule ref:** R8
- **Fact refs:** F7, F3
- **Issue ref:** I3
- **Result:** violated

### A10

Rocky Vista does not notify applicants of AI use (violating 6-1-1703(2)(e)), provides no data correction mechanism (violating 6-1-1703(2)(f)), and provides no appeal process (violating 6-1-1703(2)(g)). All three obligations must be met by June 30, 2026.

- **Rule ref:** R9
- **Fact refs:** F7
- **Issue ref:** I3
- **Result:** violated

### A11

ShiftBridge provides limitation docs (satisfying 6-1-1702(2)(a)) and training data summary (satisfying 6-1-1702(2)(b)). But it provides nothing on intended or inappropriate uses (violating 6-1-1702(2)(c)), nothing on use/monitoring guidance (violating 6-1-1702(2)(d)), and its generic impact assessment does not constitute additional documentation reasonably necessary for deployer impact assessments (violating 6-1-1702(2)(e)).

- **Rule ref:** R10
- **Fact refs:** F8
- **Issue ref:** I4
- **Result:** violated

### A12

ShiftBridge website does not list its high-risk AI systems. Section 6-1-1702(3) requires a publicly available statement summarizing high-risk AI systems developed or substantially modified. This is entirely absent.

- **Rule ref:** R11
- **Fact refs:** F8
- **Issue ref:** I4
- **Result:** violated

### A13

Job applicants are acting in an employment context and are excluded from the TRAIGA consumer definition under 551.001(2). TRAIGA consumer-facing disclosure requirements do not apply to hiring. Section 551.051(a) prohibits intentional discrimination, but no evidence of discriminatory intent exists. Bexar County has no TRAIGA obligations for hiring use of CredenScore.

- **Rule ref:** R16
- **Fact refs:** F4, F9
- **Issue ref:** I5
- **Result:** satisfied

### A14

No evidence of intent to discriminate. TRAIGA requires intentional discrimination; disparate impact alone is insufficient. The prohibition in 551.051(a) is not violated.

- **Rule ref:** R13
- **Fact refs:** F9
- **Issue ref:** I5
- **Result:** satisfied

### A15

Bexar County is a governmental entity deploying AskBexar AI chatbot to interact with consumers (patients and public acting in individual capacity). Section 551.101 requires disclosure before or at time of interaction that consumer is interacting with AI. No such disclosure is made. This is a current violation.

- **Rule ref:** R14
- **Fact refs:** F11, F4
- **Issue ref:** I6
- **Result:** violated

### A16

Bexar County is a healthcare service provider using an AI discharge-planning tool in relation to patient service or treatment. Section 551.102 requires disclosure to the patient on the date of service. No such disclosure is made. This is a current violation.

- **Rule ref:** R15
- **Fact refs:** F11, F4
- **Issue ref:** I6
- **Result:** violated

### A17

ShiftBridge claims one compliance package satisfies NYC, Colorado, and Texas. NYC requires independent bias audits with EEO-1 category calculations. Colorado requires deployer-specific impact assessments aligned with NIST AI RMF. Texas imposes no audit or assessment requirements for private employers but has unique government and healthcare disclosure rules. These are fundamentally different obligations that cannot be satisfied by a single package. The claim is legally incorrect.

- **Rule ref:** R1
- **Fact refs:** F10
- **Issue ref:** I7
- **Result:** violated

### A18

Colorado AIA requires deployer-specific impact assessments under 6-1-1701(8). A vendor-provided generic document does not travel with the product as a compliant impact assessment. Each deployer must prepare its own assessment reflecting its deployment context.

- **Rule ref:** R8
- **Fact refs:** F10
- **Issue ref:** I7
- **Result:** violated

### A19

ShiftBridge telling customers one package suffices may itself constitute a failure of reasonable care under 6-1-1702(1) if it leads deployers to believe they need not take independent compliance steps, exposing consumers to foreseeable risks of algorithmic discrimination.

- **Rule ref:** R21
- **Fact refs:** F10, F8
- **Issue ref:** I7
- **Result:** violated

## Conclusions (8)

### C1

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A1, A2, A3

### C2

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A4, A5

### C3

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A6, A7, A8, A9, A10

### C4

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A11, A12

### C5

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A13, A14

### C6

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A15

### C7

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A16

### C8

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A17, A18, A19

## Obligations (18)

### O1

Empire Mercy must commission a new bias audit of CredenScore by an independent auditor and cease AEDT use until audit is obtained

- **Required by:** R2
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Immediate - AEDT use must stop until current audit obtained

### O2

Empire Mercy must implement notice to promotion candidates at least 10 business days before CredenScore use, including AEDT disclosure, qualifications assessed, and alternative process instructions

- **Required by:** R4
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Immediate - before any further promotion screening

### O3

Bexar County must add AI disclosure to AskBexar chatbot informing users they are interacting with an AI system before or at time of interaction

- **Required by:** R14
- **Status:** mandatory
- **Jurisdiction:** Texas
- **Deadline:** Immediate - 60-day cure period under 551.301(e)

### O4

Bexar County must disclose to patients on date of service that AI discharge-planning tool is being used in their care

- **Required by:** R15
- **Status:** mandatory
- **Jurisdiction:** Texas
- **Deadline:** Immediate - 60-day cure period under 551.301(e)

### O5

Rocky Vista must develop and implement risk management program consistent with NIST AI RMF 1.0 or ISO/IEC 42001, replacing reliance on HIPAA and ISO 27001

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O6

Rocky Vista must implement pre-decision consumer notice for all applicants screened by CredenScore including AI disclosure, purpose, contact info, plain-language description, and link to public statement

- **Required by:** R9
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O7

Rocky Vista must implement mechanism for applicants to correct incorrect personal data processed by CredenScore

- **Required by:** R9
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O8

Rocky Vista must implement meaningful appeal process for consequential decisions in which CredenScore was a substantial factor

- **Required by:** R9
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O9

Rocky Vista must complete deployer-specific impact assessment covering all elements of Section 6-1-1701(8) for its specific deployment context

- **Required by:** R8
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-09-28

### O10

Rocky Vista must publish on its website a statement summarizing deployed high-risk AI systems and algorithmic discrimination risk management

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O11

ShiftBridge must provide deployers documentation of intended uses and known inappropriate uses of CredenScore

- **Required by:** R10
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O12

ShiftBridge must provide deployers documentation on how CredenScore should be used, not be used, and monitored by individuals for consequential decisions

- **Required by:** R10
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O13

ShiftBridge must publish on its website a statement summarizing CredenScore and any other high-risk AI systems it develops or substantially modifies

- **Required by:** R11
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O14

ShiftBridge must provide deployers additional documentation reasonably necessary to complete deployer-specific impact assessments

- **Required by:** R10
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O15

ShiftBridge must retract or correct its claim that one compliance package satisfies all three jurisdictions to avoid misleading deployers and potential reasonable care liability

- **Required by:** R21
- **Status:** recommended
- **Jurisdiction:** Colorado
- **Deadline:** Immediate

### O16

ShiftBridge and Rocky Vista should align AI governance with NIST AI RMF 1.0 for safe harbor benefits under both Colorado AIA and Texas TRAIGA

- **Required by:** R17
- **Status:** safe-harbor
- **Jurisdiction:** Colorado and Texas
- **Deadline:** Not specified

### O17

Rocky Vista must establish annual review process to ensure CredenScore is not causing algorithmic discrimination

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** First review by 2027-06-30

### O18

Empire Mercy must update published bias audit summary and distribution date on careers page once new audit is obtained; retain for 6 months after latest AEDT use

- **Required by:** R5
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Upon completion of new bias audit

## Graph connections (68)

### E1

- **Src:** F2
- **Dst:** I1
- **Type:** triggers
- **Justification:** Empire Mercy 50% weighting and dual hiring/promotion use raises AEDT classification question

### E2

- **Src:** F5
- **Dst:** I1
- **Type:** triggers
- **Justification:** February 2025 audit date raises currency question as of April 2026

### E3

- **Src:** R1
- **Dst:** A1
- **Type:** applies-to
- **Justification:** AEDT definition applied to CredenScore at Empire Mercy

### E4

- **Src:** R2
- **Dst:** A2
- **Type:** applies-to
- **Justification:** One-year audit currency rule applied to February 2025 audit

### E5

- **Src:** A1
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** CredenScore is confirmed as AEDT

### E6

- **Src:** A2
- **Dst:** C1
- **Type:** fails-element
- **Justification:** Audit expired; continued use violates LL 144

### E7

- **Src:** F6
- **Dst:** I2
- **Type:** triggers
- **Justification:** Absence of promotion notice raises notice sufficiency question

### E8

- **Src:** R4
- **Dst:** A4
- **Type:** applies-to
- **Justification:** Notice requirements applied to both applicant and promotion contexts

### E9

- **Src:** A4
- **Dst:** C2
- **Type:** fails-element
- **Justification:** Promotion candidate notice entirely absent

### E10

- **Src:** R5
- **Dst:** A5
- **Type:** applies-to
- **Justification:** Publication requirements applied to Empire Mercy careers page

### E11

- **Src:** A5
- **Dst:** C2
- **Type:** satisfies-element
- **Justification:** Publication form requirements met but underlying audit stale

### E12

- **Src:** F3
- **Dst:** I3
- **Type:** triggers
- **Justification:** Rocky Vista auto-rejection and Colorado operations raise CO AIA applicability

### E13

- **Src:** R6
- **Dst:** A6
- **Type:** applies-to
- **Justification:** High-risk AI system definition applied to CredenScore at Rocky Vista

### E14

- **Src:** R12
- **Dst:** A7
- **Type:** applies-to
- **Justification:** Small deployer exception tested against Rocky Vista 3,000 FTEs

### E15

- **Src:** R7
- **Dst:** A8
- **Type:** applies-to
- **Justification:** NIST AI RMF requirement applied to HIPAA + ISO 27001 governance

### E16

- **Src:** A8
- **Dst:** C3
- **Type:** fails-element
- **Justification:** HIPAA and ISO 27001 are not AI risk management frameworks

### E17

- **Src:** R8
- **Dst:** A9
- **Type:** applies-to
- **Justification:** Impact assessment requirements applied to generic vendor document

### E18

- **Src:** A9
- **Dst:** C3
- **Type:** fails-element
- **Justification:** Generic vendor document fails deployer-specific requirements

### E19

- **Src:** R9
- **Dst:** A10
- **Type:** applies-to
- **Justification:** Consumer notice, correction, and appeal requirements applied to Rocky Vista

### E20

- **Src:** A10
- **Dst:** C3
- **Type:** fails-element
- **Justification:** No notice, no correction mechanism, no appeal process

### E21

- **Src:** F8
- **Dst:** I4
- **Type:** triggers
- **Justification:** ShiftBridge documentation gaps raise developer obligation question

### E22

- **Src:** R10
- **Dst:** A11
- **Type:** applies-to
- **Justification:** Developer documentation obligations applied to ShiftBridge

### E23

- **Src:** A11
- **Dst:** C4
- **Type:** fails-element
- **Justification:** Missing intended/inappropriate use docs, monitoring guidance, and impact assessment support

### E24

- **Src:** R11
- **Dst:** A12
- **Type:** applies-to
- **Justification:** Developer public disclosure requirement applied to ShiftBridge website

### E25

- **Src:** A12
- **Dst:** C4
- **Type:** fails-element
- **Justification:** No public listing of high-risk AI systems on website

### E26

- **Src:** F4
- **Dst:** I5
- **Type:** triggers
- **Justification:** Bexar County governmental entity status and hiring use raise TRAIGA question

### E27

- **Src:** R16
- **Dst:** A13
- **Type:** applies-to
- **Justification:** Consumer definition exclusion applied to job applicants

### E28

- **Src:** R13
- **Dst:** A14
- **Type:** applies-to
- **Justification:** Intentional discrimination prohibition applied to Bexar County

### E29

- **Src:** A13
- **Dst:** C5
- **Type:** satisfies-element
- **Justification:** Job applicants excluded from consumer definition; no TRAIGA hiring obligations

### E30

- **Src:** A14
- **Dst:** C5
- **Type:** satisfies-element
- **Justification:** No evidence of discriminatory intent

### E31

- **Src:** F11
- **Dst:** I6
- **Type:** triggers
- **Justification:** AskBexar and discharge tool without disclosure raise Texas obligation questions

### E32

- **Src:** R14
- **Dst:** A15
- **Type:** applies-to
- **Justification:** Government AI disclosure requirement applied to AskBexar chatbot

### E33

- **Src:** A15
- **Dst:** C6
- **Type:** fails-element
- **Justification:** No AI disclosure provided to chatbot users

### E34

- **Src:** R15
- **Dst:** A16
- **Type:** applies-to
- **Justification:** Healthcare AI disclosure requirement applied to discharge-planning tool

### E35

- **Src:** A16
- **Dst:** C7
- **Type:** fails-element
- **Justification:** No AI disclosure provided to patients

### E36

- **Src:** F10
- **Dst:** I7
- **Type:** triggers
- **Justification:** One compliance package claim raises cross-jurisdictional accuracy question

### E37

- **Src:** R1
- **Dst:** A17
- **Type:** applies-to
- **Justification:** NYC AEDT requirements compared against single-package claim

### E38

- **Src:** R8
- **Dst:** A18
- **Type:** applies-to
- **Justification:** Colorado deployer-specific impact assessment requirement contradicts portable package claim

### E39

- **Src:** A17
- **Dst:** C8
- **Type:** fails-element
- **Justification:** Three jurisdictions have materially different requirements

### E40

- **Src:** A18
- **Dst:** C8
- **Type:** fails-element
- **Justification:** Impact assessments must be deployer-specific and cannot travel with product

### E41

- **Src:** R21
- **Dst:** A19
- **Type:** applies-to
- **Justification:** Reasonable care duty applied to misleading compliance claim

### E42

- **Src:** A19
- **Dst:** C8
- **Type:** fails-element
- **Justification:** Misleading claim may constitute failure of reasonable care

### E43

- **Src:** R2
- **Dst:** O1
- **Type:** triggers
- **Justification:** Expired audit requires new audit and cessation of AEDT use

### E44

- **Src:** R4
- **Dst:** O2
- **Type:** triggers
- **Justification:** Missing promotion notice requires implementation

### E45

- **Src:** R14
- **Dst:** O3
- **Type:** triggers
- **Justification:** Missing chatbot disclosure requires implementation

### E46

- **Src:** R15
- **Dst:** O4
- **Type:** triggers
- **Justification:** Missing healthcare AI disclosure requires implementation

### E47

- **Src:** R7
- **Dst:** O5
- **Type:** triggers
- **Justification:** Insufficient governance framework requires NIST AI RMF alignment

### E48

- **Src:** R9
- **Dst:** O6
- **Type:** triggers
- **Justification:** Missing consumer notice requires implementation

### E49

- **Src:** R9
- **Dst:** O7
- **Type:** triggers
- **Justification:** Missing data correction mechanism requires implementation

### E50

- **Src:** R9
- **Dst:** O8
- **Type:** triggers
- **Justification:** Missing appeal process requires implementation

### E51

- **Src:** R8
- **Dst:** O9
- **Type:** triggers
- **Justification:** Insufficient impact assessment requires deployer-specific completion

### E52

- **Src:** R7
- **Dst:** O10
- **Type:** triggers
- **Justification:** Missing public statement requires publication

### E53

- **Src:** R10
- **Dst:** O11
- **Type:** triggers
- **Justification:** Missing intended/inappropriate use documentation

### E54

- **Src:** R10
- **Dst:** O12
- **Type:** triggers
- **Justification:** Missing use/monitoring guidance documentation

### E55

- **Src:** R11
- **Dst:** O13
- **Type:** triggers
- **Justification:** Missing public disclosure of high-risk AI systems

### E56

- **Src:** R10
- **Dst:** O14
- **Type:** triggers
- **Justification:** Missing impact assessment support documentation

### E57

- **Src:** R21
- **Dst:** O15
- **Type:** triggers
- **Justification:** Misleading compliance claim should be retracted

### E58

- **Src:** R17
- **Dst:** O16
- **Type:** triggers
- **Justification:** NIST AI RMF alignment provides safe harbor

### E59

- **Src:** R7
- **Dst:** O17
- **Type:** triggers
- **Justification:** Annual review requirement for algorithmic discrimination

### E60

- **Src:** R5
- **Dst:** O18
- **Type:** triggers
- **Justification:** Publication must be updated with new audit results

### E61

- **Src:** R18
- **Dst:** C2
- **Type:** applies-to
- **Justification:** Per-candidate violation penalties apply to promotion screening without notice

### E62

- **Src:** R3
- **Dst:** A3
- **Type:** applies-to
- **Justification:** Audit methodology and independence requirements applied to Tolland Review Partners

### E63

- **Src:** A3
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** Audit was validly conducted when performed but is now expired

### E64

- **Src:** R19
- **Dst:** C3
- **Type:** applies-to
- **Justification:** Colorado enforcement framework applies to Rocky Vista violations

### E65

- **Src:** R20
- **Dst:** C6
- **Type:** applies-to
- **Justification:** Texas enforcement framework applies to Bexar County chatbot violation

### E66

- **Src:** R20
- **Dst:** C7
- **Type:** applies-to
- **Justification:** Texas enforcement framework applies to Bexar County healthcare disclosure violation

### E67

- **Src:** A6
- **Dst:** C3
- **Type:** satisfies-element
- **Justification:** CredenScore confirmed as high-risk AI system at Rocky Vista

### E68

- **Src:** A7
- **Dst:** C3
- **Type:** satisfies-element
- **Justification:** Small deployer exception inapplicable to Rocky Vista
