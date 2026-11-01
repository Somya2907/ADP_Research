# H1 — PeopleScore Multi-State — teacher FIRACO reasoning

Unverified model output for legal review. Citations, facts, applications, and obligations may be incorrect. Text and node IDs below are preserved from the saved reference graph.

[Read case](../../../data/cases/H1_peoplescore_multistate.md) · [Review brief](../../PROF_PHILIPP_REVIEW.md)

Teacher: claude-opus-4-6. Source: data/outputs/graphs/H1_reference.json.

Source SHA-256: `8f6494b704cdb1964dab55888fdc134a296c95432caae6d7d07dd5c362bced42`.

The internal audit flags at least one rule below for a suspect NYC §20-875 citation. Other errors may also be present.

## Facts (16)

### F1

TalentMatrix Inc. is developer of PeopleScore, headquartered in Atlanta, 800 employees

- **Polarity:** present
- **Support quote:** TalentMatrix Inc. (headquartered in Atlanta, Georgia; 800 employees) sells 'PeopleScore'

### F2

PeopleScore uses NLP, interview scoring, predictive modeling to generate score 0-100 and hiring recommendation

- **Polarity:** present
- **Support quote:** composite candidate score from 0 to 100 and a hiring recommendation (Strong Hire / Hire / No Hire)

### F3

RetailCo is national retailer headquartered in Dallas TX with 85,000 employees, deployer of PeopleScore

- **Polarity:** present
- **Support quote:** RetailCo, a national big-box retailer headquartered in Dallas, Texas with 85,000 total employees

### F4

PeopleScore used to evaluate candidates for hourly retail associate positions (employment decisions)

- **Polarity:** present
- **Support quote:** RetailCo uses PeopleScore to evaluate candidates for hourly retail associate positions

### F5

PeopleScore deployed in 400 TX stores (since 2024), 80 CO stores (since March 2026), 30 NYC stores (since 2023)

- **Polarity:** present
- **Support quote:** 400 stores across Texas, 80 stores in Colorado, 30 stores in the five boroughs of New York City

### F6

Last bias audit conducted August 2025

- **Polarity:** present
- **Support quote:** PeopleScore was last bias-audited in August 2025

### F7

Audit conducted by TM Analytics LLC, wholly owned subsidiary of TalentMatrix

- **Polarity:** present
- **Support quote:** conducted by TM Analytics, LLC, a wholly owned subsidiary of TalentMatrix Inc.

### F8

Audit used RetailCo 2024-2025 historical data, covered selection rates across sex/race/intersectional categories, impact ratios above 0.80

- **Polarity:** present
- **Support quote:** covered selection rates across sex, race/ethnicity, and intersectional categories using RetailCo 2024-2025 historical hiring data

### F9

Bias audit summary posted on sub-page labeled NYC Applicants, not visible from main careers page or job listings

- **Polarity:** present
- **Support quote:** not visible from the main careers page or from job listings; candidates must navigate to a sub-page

### F10

Boilerplate notice sent at application time says may use technology-assisted tools, no specifics on AEDT, qualifications assessed, or alternative process

- **Polarity:** present
- **Support quote:** does not name PeopleScore, does not specify which job qualifications or characteristics are evaluated, and does not inform candidates of their right to request an alternative selection process

### F11

December 2025 impact assessment references NIST 800-53 and EU AI Act, not Colorado AIA or NIST AI 100-1

- **Polarity:** present
- **Support quote:** references compliance with NIST 800-53 and the EU AI Act as the governing frameworks

### F12

No consumer notification issued to Colorado applicants regarding AI-assisted hiring

- **Polarity:** present
- **Support quote:** RetailCo has not issued any consumer notification to Colorado applicants

### F13

No appeal process or data-correction mechanism exists for Colorado applicants

- **Polarity:** present
- **Support quote:** No appeal process or data-correction mechanism exists for Colorado applicants

### F14

No written AI risk management policy; no alignment with NIST AI 100-1 or ISO/IEC 42001

- **Polarity:** present
- **Support quote:** RetailCo does not have a written AI risk management policy

### F15

No Texas-specific compliance measures implemented

- **Polarity:** present
- **Support quote:** No Texas-specific compliance measures have been implemented

### F16

General counsel states TRAIGA does not apply because it only covers intentional discrimination

- **Polarity:** present
- **Support quote:** TRAIGA does not really apply to our hiring process because it only covers intentional discrimination

## Issues (10)

### I1

Does NYC LL 144 apply to RetailCo use of PeopleScore for NYC positions and is RetailCo compliant

- **Status:** dispositive

### I2

Does TM Analytics LLC qualify as independent auditor under NYC LL 144

- **Status:** dispositive

### I3

Is RetailCo public disclosure of bias audit results compliant with LL 144 and DCWP rules

- **Status:** dispositive

### I4

Is RetailCo candidate notice compliant with LL 144 and DCWP rules

- **Status:** dispositive

### I5

Does Colorado AIA apply to RetailCo deployment of PeopleScore and what is compliance timeline

- **Status:** dispositive

### I6

Does NIST 800-53 satisfy Colorado AIA risk management framework requirement

- **Status:** dispositive

### I7

Is RetailCo December 2025 impact assessment compliant with Colorado AIA

- **Status:** dispositive

### I8

What are TalentMatrix developer obligations under Colorado AIA

- **Status:** dispositive

### I9

Does Texas TRAIGA apply to RetailCo hiring use and is general counsel position correct

- **Status:** dispositive

### I10

What are TalentMatrix developer obligations under TRAIGA

- **Status:** collateral

## Rules (27)

### R1

AEDT definition: computational process from ML/AI issuing simplified output used to substantially assist or replace discretionary employment decisions

- **Citation:** NYC LL 144 Section 20-870; DCWP Section 5-300
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R2

Bias audit required no more than one year prior to use of AEDT

- **Citation:** NYC LL 144 Section 20-871(a)(1); DCWP Section 5-301(a)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R3

Independent auditor must not have financial interest in employer or AEDT developer; subsidiary of developer does not qualify

- **Citation:** NYC LL 144 Section 20-870; DCWP Section 5-300 Independent Auditor definition
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R4

Scoring AEDT bias audit must calculate median score, scoring rate per category, and impact ratio per category for sex, race/ethnicity, and intersectional categories

- **Citation:** DCWP Section 5-301(c)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R5

Published results must be on employment section of website in clear and conspicuous manner with audit date, data source, unknowns, applicant counts, rates, impact ratios, and distribution date

- **Citation:** NYC LL 144 Section 20-871(a)(2); DCWP Section 5-303(a)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R6

Candidate notice at least 10 business days before AEDT use identifying AEDT use, qualifications assessed, and right to request alternative process

- **Citation:** NYC LL 144 Section 20-872; DCWP Section 5-304
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R7

> Flagged for review: the internal audit reports that the cited NYC §20-875 does not exist. Please verify both citation and proposition.

Penalties $500-$1500 per violation; each screening of single candidate may be separate violation

- **Citation:** NYC LL 144 Section 20-875
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R8

Colorado AIA effective date June 30, 2026; not yet in force as of April 16, 2026

- **Citation:** Colorado AIA SB 24-205 as amended by SB 25B-004
- **Authority:** binding
- **Jurisdiction:** CO
- **Effective as of:** 2026-06-30

### R9

High-risk AI system: AI system that makes or is substantial factor in consequential decision; employment is consequential decision

- **Citation:** Colorado AIA Section 6-1-1701(7) and Section 6-1-1701(3)(b)
- **Authority:** binding
- **Jurisdiction:** CO
- **Effective as of:** 2026-06-30

### R10

Risk management program must be consistent with NIST AI 100-1 or substantially equivalent framework like ISO/IEC 42001; NIST 800-53 and EU AI Act are NOT sufficient

- **Citation:** Colorado AIA Section 6-1-1703(2)(a)(III)
- **Authority:** binding
- **Jurisdiction:** CO
- **Effective as of:** 2026-06-30

### R11

Impact assessment required before deployment or within 90 days of effective date for pre-existing systems; must include six enumerated elements

- **Citation:** Colorado AIA Section 6-1-1703(2)(b); Section 6-1-1701(8)
- **Authority:** binding
- **Jurisdiction:** CO
- **Effective as of:** 2026-06-30

### R12

Pre-decision consumer notice required: AI system use, purpose, decision nature, contact info, plain-language description, link to public statement

- **Citation:** Colorado AIA Section 6-1-1703(2)(e)
- **Authority:** binding
- **Jurisdiction:** CO
- **Effective as of:** 2026-06-30

### R13

Consumer right to correct data and meaningful opportunity to appeal consequential decisions

- **Citation:** Colorado AIA Section 6-1-1703(2)(f)-(g)
- **Authority:** binding
- **Jurisdiction:** CO
- **Effective as of:** 2026-06-30

### R14

Annual review of deployment to ensure no algorithmic discrimination

- **Citation:** Colorado AIA Section 6-1-1703(2)(c)
- **Authority:** binding
- **Jurisdiction:** CO
- **Effective as of:** 2026-06-30

### R15

Public website statement summarizing deployed high-risk AI systems and discrimination risk management

- **Citation:** Colorado AIA Section 6-1-1703(2)(d)
- **Authority:** binding
- **Jurisdiction:** CO
- **Effective as of:** 2026-06-30

### R16

Developer must provide deployer documentation on limitations, training data, intended uses, monitoring guidance, impact assessment support; must publish public use case inventory

- **Citation:** Colorado AIA Section 6-1-1702(2)-(3)
- **Authority:** binding
- **Jurisdiction:** CO
- **Effective as of:** 2026-06-30

### R17

Small deployer exception: fewer than 50 employees AND does not use own data to train; both conditions required

- **Citation:** Colorado AIA Section 6-1-1703(6)
- **Authority:** binding
- **Jurisdiction:** CO
- **Effective as of:** 2026-06-30

### R18

90-day notification to AG and consumers if algorithmic discrimination discovered

- **Citation:** Colorado AIA Section 6-1-1704
- **Authority:** binding
- **Jurisdiction:** CO
- **Effective as of:** 2026-06-30

### R19

AG exclusive enforcement; up to $20,000 per violation; rebuttable presumption if self-discovered and cured within 60 days

- **Citation:** Colorado AIA Section 6-1-1706
- **Authority:** binding
- **Jurisdiction:** CO
- **Effective as of:** 2026-06-30

### R20

TRAIGA effective January 1, 2026; in force as of April 16, 2026

- **Citation:** Texas TRAIGA HB 149 Section 551.001 et seq.
- **Authority:** binding
- **Jurisdiction:** TX
- **Effective as of:** 2026-01-01

### R21

Prohibits deploying AI with intent to unlawfully discriminate; requires intentional discrimination, not disparate impact

- **Citation:** Texas TRAIGA Section 551.051(a)
- **Authority:** binding
- **Jurisdiction:** TX
- **Effective as of:** 2026-01-01

### R22

Consumer excludes individuals acting in employment context; TRAIGA consumer protections do not apply to job applicants

- **Citation:** Texas TRAIGA Section 551.001(2)
- **Authority:** binding
- **Jurisdiction:** TX
- **Effective as of:** 2026-01-01

### R23

AI disclosure obligation applies only to government agencies, not private employers

- **Citation:** Texas TRAIGA Section 551.101
- **Authority:** binding
- **Jurisdiction:** TX
- **Effective as of:** 2026-01-01

### R24

No private employer obligations for bias audits, impact assessments, risk management, candidate notices, or appeals

- **Citation:** Texas TRAIGA HB 149 (enacted text)
- **Authority:** binding
- **Jurisdiction:** TX
- **Effective as of:** 2026-01-01

### R25

TRAIGA preempts local Texas AI ordinances; does not preempt other states laws

- **Citation:** Texas TRAIGA Section 551.201
- **Authority:** binding
- **Jurisdiction:** TX
- **Effective as of:** 2026-01-01

### R26

Safe harbor for substantial compliance with NIST AI 100-1 or recognized AI governance standards

- **Citation:** Texas TRAIGA Section 551.301(d)
- **Authority:** binding
- **Jurisdiction:** TX
- **Effective as of:** 2026-01-01

### R27

AG-only enforcement; $10,000-$200,000 per violation; 60-day cure period

- **Citation:** Texas TRAIGA Section 551.301
- **Authority:** binding
- **Jurisdiction:** TX
- **Effective as of:** 2026-01-01

## Applications (19)

### A1

PeopleScore uses ML/AI (NLP, predictive modeling) to generate simplified output (score 0-100, hiring recommendation) used to screen candidates for employment. This satisfies all elements of the AEDT definition under Section 20-870 and DCWP Section 5-300.

- **Rule ref:** R1
- **Fact refs:** F2, F4
- **Issue ref:** I1
- **Result:** satisfied

### A2

PeopleScore deployed in 30 NYC stores since 2023. Last audit August 2025. As of April 2026, the audit is within one year. However, the audit is invalid due to auditor independence failure (see A3), so the one-year timing is moot.

- **Rule ref:** R2
- **Fact refs:** F5, F6
- **Issue ref:** I1
- **Result:** satisfied

### A3

TM Analytics LLC is a wholly owned subsidiary of TalentMatrix, the developer of PeopleScore. Under Section 20-870 and DCWP Section 5-300, an auditor with a financial interest in the AEDT developer is not independent. A wholly owned subsidiary has a direct financial interest in its parent. TM Analytics does not qualify as an independent auditor. The August 2025 audit is therefore invalid.

- **Rule ref:** R3
- **Fact refs:** F7
- **Issue ref:** I2
- **Result:** violated

### A4

PeopleScore generates a composite score (0-100), making it a scoring AEDT under DCWP Section 5-301(c). The audit used selection rate methodology rather than scoring rate methodology (median score, scoring rates, impact ratios). Even if the auditor were independent, the methodology would be deficient for a scoring AEDT.

- **Rule ref:** R4
- **Fact refs:** F2, F8
- **Issue ref:** I1
- **Result:** violated

### A5

The bias audit summary is posted on a sub-page labeled NYC Applicants that is not visible from the main careers page or job listings. DCWP Section 5-303(a) requires posting on the employment section of the website in a clear and conspicuous manner. Requiring candidates to navigate to a hidden sub-page fails the clear and conspicuous standard. Additionally, the published results are based on an invalid audit.

- **Rule ref:** R5
- **Fact refs:** F9
- **Issue ref:** I3
- **Result:** violated

### A6

RetailCo notice fails on three grounds: (1) does not identify PeopleScore as an AEDT or state that an AEDT will be used; (2) does not specify job qualifications or characteristics assessed; (3) does not include instructions for requesting alternative selection process. Additionally, notice is sent at application time rather than 10 business days before AEDT use as required by DCWP Section 5-304.

- **Rule ref:** R6
- **Fact refs:** F10
- **Issue ref:** I4
- **Result:** violated

### A7

Each use of non-compliant AEDT to screen a single candidate is a separate violation at $500-$1500. RetailCo has screened candidates across 30 NYC stores since 2023 with an invalid audit, deficient notice, and deficient disclosure. Aggregate penalty exposure is substantial.

- **Rule ref:** R7
- **Fact refs:** F5
- **Issue ref:** I1
- **Result:** violated

### A8

PeopleScore is an AI system that makes or is a substantial factor in making employment decisions (consequential decisions under Section 6-1-1701(3)(b)). The composite score and hiring recommendation materially contribute to hiring outcomes. PeopleScore is a high-risk AI system under Section 6-1-1701(7).

- **Rule ref:** R9
- **Fact refs:** F2, F4
- **Issue ref:** I5
- **Result:** satisfied

### A9

Section 6-1-1703(2)(a)(III) requires consistency with NIST AI 100-1 or substantially equivalent AI risk management framework such as ISO/IEC 42001. NIST 800-53 is a cybersecurity controls framework, not an AI risk management framework. The EU AI Act is foreign law. Neither satisfies the Colorado AIA requirement. RetailCo has no written AI risk management policy and no NIST AI 100-1 alignment.

- **Rule ref:** R10
- **Fact refs:** F11, F14
- **Issue ref:** I6
- **Result:** violated

### A10

RetailCo December 2025 impact assessment references wrong frameworks (NIST 800-53, EU AI Act) and does not address Colorado AIA Section 6-1-1701(8) required elements. PeopleScore was deployed in CO in March 2026 (before June 30, 2026 effective date), so RetailCo has until September 28, 2026 (90 days post-effective date) to complete a compliant assessment. Current assessment is non-compliant and must be substantially revised.

- **Rule ref:** R11
- **Fact refs:** F5, F11
- **Issue ref:** I7
- **Result:** violated

### A11

No consumer notification has been issued to Colorado applicants. Section 6-1-1703(2)(e) requires pre-decision notice with six specified elements. This obligation attaches June 30, 2026. RetailCo has no readiness measures in place.

- **Rule ref:** R12
- **Fact refs:** F12
- **Issue ref:** I5
- **Result:** violated

### A12

No appeal process or data-correction mechanism exists for Colorado applicants. Sections 6-1-1703(2)(f) and (g) require both. Obligation attaches June 30, 2026.

- **Rule ref:** R13
- **Fact refs:** F13
- **Issue ref:** I5
- **Result:** violated

### A13

No public statement exists summarizing deployed high-risk AI systems and algorithmic discrimination risk management for Colorado. Section 6-1-1703(2)(d) requires this. Obligation attaches June 30, 2026.

- **Rule ref:** R15
- **Fact refs:** F14
- **Issue ref:** I5
- **Result:** violated

### A14

TalentMatrix as developer must provide documentation per Section 6-1-1702(2) and publish public use case inventory per Section 6-1-1702(3). Facts do not indicate whether TalentMatrix has prepared any such documentation. Obligation attaches June 30, 2026.

- **Rule ref:** R16
- **Fact refs:** F1, F2
- **Issue ref:** I8
- **Result:** requires-fact

### A15

Small deployer exception requires fewer than 50 employees AND not using own data to train. RetailCo has 85,000 employees, failing the first condition. Exception is inapplicable; all deployer obligations apply.

- **Rule ref:** R17
- **Fact refs:** F3
- **Issue ref:** I5
- **Result:** satisfied

### A16

TRAIGA Section 551.051(a) prohibits deploying AI with intent to unlawfully discriminate. No facts suggest RetailCo has discriminatory intent. RetailCo is not in violation of this prohibition. However, the general counsel position is incomplete because it ignores the available safe harbor and federal law exposure.

- **Rule ref:** R21
- **Fact refs:** F15, F16
- **Issue ref:** I9
- **Result:** satisfied

### A17

TRAIGA Section 551.001(2) excludes individuals acting in employment context from consumer definition. Job applicants are in employment context. TRAIGA consumer-facing requirements do not apply to RetailCo hiring process.

- **Rule ref:** R22
- **Fact refs:** F4
- **Issue ref:** I9
- **Result:** satisfied

### A18

TRAIGA imposes no private employer obligations for bias audits, impact assessments, risk management, candidate notices, or appeals. RetailCo has no affirmative compliance obligations under TRAIGA for its hiring process beyond the prohibition on intentional discrimination.

- **Rule ref:** R24
- **Fact refs:** F15
- **Issue ref:** I9
- **Result:** satisfied

### A19

TRAIGA Section 551.301(d) provides safe harbor for substantial compliance with NIST AI 100-1. RetailCo has not aligned with NIST AI 100-1 and therefore does not benefit from this safe harbor. While not currently required, failing to obtain the safe harbor leaves RetailCo without an affirmative defense if intent is ever alleged.

- **Rule ref:** R26
- **Fact refs:** F14, F15
- **Issue ref:** I9
- **Result:** partial

## Conclusions (3)

### C1

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A3, A4, A5, A6, A7

### C2

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A9, A10, A11, A12, A13

### C3

- **Determination:** conditional
- **Confidence:** medium
- **Support refs:** A16, A17, A18, A19

## Obligations (13)

### O1

Retain truly independent auditor and conduct new bias audit using DCWP Section 5-301(c) scoring methodology before continued NYC use

- **Required by:** R2
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Immediate - before continued use of PeopleScore in NYC

### O2

Repost bias audit results on employment section of website in clear and conspicuous manner with all required elements per DCWP Section 5-303(a)

- **Required by:** R5
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Before continued use of AEDT after new audit completed

### O3

Revise candidate notice to identify AEDT use, specify qualifications assessed, include alternative process instructions, and provide 10 business days advance

- **Required by:** R6
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** At least 10 business days before next AEDT use in NYC

### O4

Develop and implement AI risk management policy aligned with NIST AI 100-1 or ISO/IEC 42001

- **Required by:** R10
- **Status:** mandatory
- **Jurisdiction:** CO
- **Deadline:** 2026-06-30

### O5

Complete Colorado AIA-compliant impact assessment with all Section 6-1-1701(8) elements

- **Required by:** R11
- **Status:** mandatory
- **Jurisdiction:** CO
- **Deadline:** 2026-09-28

### O6

Implement pre-decision consumer notice for Colorado applicants with all Section 6-1-1703(2)(e) elements

- **Required by:** R12
- **Status:** mandatory
- **Jurisdiction:** CO
- **Deadline:** 2026-06-30

### O7

Implement data-correction opportunity and meaningful appeal process for Colorado applicants

- **Required by:** R13
- **Status:** mandatory
- **Jurisdiction:** CO
- **Deadline:** 2026-06-30

### O8

Publish public website statement summarizing deployed high-risk AI systems and discrimination risk management

- **Required by:** R15
- **Status:** mandatory
- **Jurisdiction:** CO
- **Deadline:** 2026-06-30

### O9

TalentMatrix must prepare and deliver developer documentation per Section 6-1-1702(2) and publish public use case inventory per Section 6-1-1702(3)

- **Required by:** R16
- **Status:** mandatory
- **Jurisdiction:** CO
- **Deadline:** 2026-06-30

### O10

Adopt NIST AI 100-1 alignment to qualify for TRAIGA safe harbor under Section 551.301(d)

- **Required by:** R26
- **Status:** safe-harbor
- **Jurisdiction:** TX
- **Deadline:** Not specified

### O11

Document non-discriminatory intent and ongoing monitoring of PeopleScore outcomes in Texas

- **Required by:** R21
- **Status:** recommended
- **Jurisdiction:** TX
- **Deadline:** Not specified

### O12

Ensure federal Title VII disparate impact compliance for AI hiring tools across all jurisdictions

- **Required by:** R21
- **Status:** recommended
- **Jurisdiction:** ALL
- **Deadline:** Not specified

### O13

Implement annual review of PeopleScore deployment in Colorado for algorithmic discrimination

- **Required by:** R14
- **Status:** mandatory
- **Jurisdiction:** CO
- **Deadline:** 2026-06-30

## Graph connections (56)

### E1

- **Src:** F2
- **Dst:** I1
- **Type:** triggers
- **Justification:** PeopleScore characteristics raise question of AEDT classification under LL 144

### E2

- **Src:** F5
- **Dst:** I1
- **Type:** triggers
- **Justification:** NYC deployment establishes jurisdictional nexus for LL 144

### E3

- **Src:** F7
- **Dst:** I2
- **Type:** triggers
- **Justification:** Subsidiary relationship raises auditor independence question

### E4

- **Src:** F9
- **Dst:** I3
- **Type:** triggers
- **Justification:** Hidden sub-page placement raises clear and conspicuous disclosure question

### E5

- **Src:** F10
- **Dst:** I4
- **Type:** triggers
- **Justification:** Boilerplate notice content and timing raise notice compliance question

### E6

- **Src:** F5
- **Dst:** I5
- **Type:** triggers
- **Justification:** Colorado deployment establishes jurisdictional nexus for CO AIA

### E7

- **Src:** F11
- **Dst:** I6
- **Type:** triggers
- **Justification:** NIST 800-53 reference raises framework sufficiency question

### E8

- **Src:** F11
- **Dst:** I7
- **Type:** triggers
- **Justification:** Impact assessment content raises compliance question

### E9

- **Src:** F1
- **Dst:** I8
- **Type:** triggers
- **Justification:** TalentMatrix developer status triggers developer obligation analysis

### E10

- **Src:** F16
- **Dst:** I9
- **Type:** triggers
- **Justification:** General counsel statement raises TRAIGA applicability question

### E11

- **Src:** R1
- **Dst:** A1
- **Type:** applies-to
- **Justification:** AEDT definition applied to PeopleScore characteristics

### E12

- **Src:** R2
- **Dst:** A2
- **Type:** applies-to
- **Justification:** Bias audit timing requirement applied to August 2025 audit

### E13

- **Src:** R3
- **Dst:** A3
- **Type:** applies-to
- **Justification:** Independent auditor definition applied to TM Analytics subsidiary status

### E14

- **Src:** R4
- **Dst:** A4
- **Type:** applies-to
- **Justification:** Scoring AEDT methodology applied to PeopleScore audit approach

### E15

- **Src:** R5
- **Dst:** A5
- **Type:** applies-to
- **Justification:** Published results requirements applied to sub-page disclosure

### E16

- **Src:** R6
- **Dst:** A6
- **Type:** applies-to
- **Justification:** Candidate notice requirements applied to boilerplate notice

### E17

- **Src:** R7
- **Dst:** A7
- **Type:** applies-to
- **Justification:** Penalty provisions applied to aggregate NYC violations

### E18

- **Src:** R9
- **Dst:** A8
- **Type:** applies-to
- **Justification:** High-risk AI definition applied to PeopleScore employment use

### E19

- **Src:** R10
- **Dst:** A9
- **Type:** applies-to
- **Justification:** Risk management framework requirement applied to NIST 800-53 reference

### E20

- **Src:** R11
- **Dst:** A10
- **Type:** applies-to
- **Justification:** Impact assessment requirements applied to December 2025 assessment

### E21

- **Src:** R12
- **Dst:** A11
- **Type:** applies-to
- **Justification:** Consumer notice requirement applied to absent CO notifications

### E22

- **Src:** R13
- **Dst:** A12
- **Type:** applies-to
- **Justification:** Appeal and data correction requirements applied to absent CO mechanisms

### E23

- **Src:** R15
- **Dst:** A13
- **Type:** applies-to
- **Justification:** Public statement requirement applied to absent CO disclosure

### E24

- **Src:** R16
- **Dst:** A14
- **Type:** applies-to
- **Justification:** Developer obligations applied to TalentMatrix documentation status

### E25

- **Src:** R17
- **Dst:** A15
- **Type:** applies-to
- **Justification:** Small deployer exception applied to RetailCo 85,000 employees

### E26

- **Src:** R21
- **Dst:** A16
- **Type:** applies-to
- **Justification:** Intentional discrimination prohibition applied to RetailCo hiring

### E27

- **Src:** R22
- **Dst:** A17
- **Type:** applies-to
- **Justification:** Consumer definition exclusion applied to job applicants

### E28

- **Src:** R24
- **Dst:** A18
- **Type:** applies-to
- **Justification:** Absence of private employer obligations applied to RetailCo

### E29

- **Src:** R26
- **Dst:** A19
- **Type:** applies-to
- **Justification:** Safe harbor provision applied to RetailCo lack of NIST AI 100-1 alignment

### E30

- **Src:** A3
- **Dst:** C1
- **Type:** fails-element
- **Justification:** Invalid auditor renders bias audit non-compliant

### E31

- **Src:** A4
- **Dst:** C1
- **Type:** fails-element
- **Justification:** Wrong audit methodology for scoring AEDT

### E32

- **Src:** A5
- **Dst:** C1
- **Type:** fails-element
- **Justification:** Disclosure not clear and conspicuous

### E33

- **Src:** A6
- **Dst:** C1
- **Type:** fails-element
- **Justification:** Notice fails content and timing requirements

### E34

- **Src:** A7
- **Dst:** C1
- **Type:** fails-element
- **Justification:** Per-candidate penalty exposure from multiple violations

### E35

- **Src:** A9
- **Dst:** C2
- **Type:** fails-element
- **Justification:** NIST 800-53 does not satisfy NIST AI 100-1 requirement

### E36

- **Src:** A10
- **Dst:** C2
- **Type:** fails-element
- **Justification:** Impact assessment references wrong frameworks and likely lacks required elements

### E37

- **Src:** A11
- **Dst:** C2
- **Type:** fails-element
- **Justification:** No consumer notice for Colorado applicants

### E38

- **Src:** A12
- **Dst:** C2
- **Type:** fails-element
- **Justification:** No appeal or data correction mechanisms

### E39

- **Src:** A13
- **Dst:** C2
- **Type:** fails-element
- **Justification:** No public statement on high-risk AI systems

### E40

- **Src:** A16
- **Dst:** C3
- **Type:** satisfies-element
- **Justification:** No intentional discrimination found; prohibition not violated

### E41

- **Src:** A17
- **Dst:** C3
- **Type:** satisfies-element
- **Justification:** Employment context excluded from consumer definition

### E42

- **Src:** A18
- **Dst:** C3
- **Type:** satisfies-element
- **Justification:** No affirmative compliance obligations for private employers

### E43

- **Src:** A19
- **Dst:** C3
- **Type:** fails-element
- **Justification:** Safe harbor not obtained due to lack of NIST AI 100-1 alignment

### E44

- **Src:** R2
- **Dst:** O1
- **Type:** triggers
- **Justification:** Invalid audit requires new independent audit before continued use

### E45

- **Src:** R5
- **Dst:** O2
- **Type:** triggers
- **Justification:** Deficient disclosure requires reposting in compliant manner

### E46

- **Src:** R6
- **Dst:** O3
- **Type:** triggers
- **Justification:** Deficient notice requires revision of content and timing

### E47

- **Src:** R10
- **Dst:** O4
- **Type:** triggers
- **Justification:** Risk management requirement triggers NIST AI 100-1 alignment obligation

### E48

- **Src:** R11
- **Dst:** O5
- **Type:** triggers
- **Justification:** Impact assessment requirement triggers compliant assessment obligation

### E49

- **Src:** R12
- **Dst:** O6
- **Type:** triggers
- **Justification:** Consumer notice requirement triggers CO notification obligation

### E50

- **Src:** R13
- **Dst:** O7
- **Type:** triggers
- **Justification:** Appeal and data correction requirements trigger mechanism implementation

### E51

- **Src:** R15
- **Dst:** O8
- **Type:** triggers
- **Justification:** Public statement requirement triggers website disclosure obligation

### E52

- **Src:** R16
- **Dst:** O9
- **Type:** triggers
- **Justification:** Developer obligations trigger TalentMatrix documentation requirement

### E53

- **Src:** R26
- **Dst:** O10
- **Type:** triggers
- **Justification:** Safe harbor availability triggers recommended NIST AI 100-1 adoption

### E54

- **Src:** R21
- **Dst:** O11
- **Type:** triggers
- **Justification:** Intent prohibition triggers recommended documentation of non-discriminatory purpose

### E55

- **Src:** R14
- **Dst:** O13
- **Type:** triggers
- **Justification:** Annual review requirement triggers ongoing monitoring obligation

### E56

- **Src:** R3
- **Dst:** A3
- **Type:** applies-to
- **Justification:** Independence definition applied to wholly owned subsidiary relationship
