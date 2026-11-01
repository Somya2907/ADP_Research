# E1 — ResumeRank NYC — teacher FIRACO reasoning

Unverified model output for legal review. Citations, facts, applications, and obligations may be incorrect. Text and node IDs below are preserved from the saved reference graph.

[Read case](../../../data/cases/E1_resumerank_nyc.md) · [Review brief](../../PROF_PHILIPP_REVIEW.md)

Teacher: claude-opus-4-6. Source: data/outputs/graphs/E1_reference.json.

Source SHA-256: `392bc7b68de3fcd961d467f940e3a1433182611f67203739445347b533f0cb37`.

The internal audit flags at least one rule below for a suspect NYC §20-875 citation. Other errors may also be present.

## Facts (13)

### F1

HireFlow Inc. is an Austin, TX-based developer of ResumeRank, an ML-based resume screening tool

- **Polarity:** present
- **Support quote:** HireFlow Inc., a Series B talent-acquisition software company based in Austin, Texas, sells 'ResumeRank'

### F2

ResumeRank uses NLP and gradient-boosted model to score candidates 1-100; above 70 forwarded, below 70 auto-rejected

- **Polarity:** present
- **Support quote:** Candidates scoring above 70 are forwarded to hiring managers; those below 70 are automatically rejected

### F3

Greenleaf Foods is a national grocery chain HQ in Chicago with 12,000 employees, the deployer of ResumeRank

- **Polarity:** present
- **Support quote:** Greenleaf Foods, a national grocery chain with its headquarters in Chicago and 12,000 employees nationwide

### F4

Greenleaf uses ResumeRank to screen applicants for six retail locations in Brooklyn and Manhattan, NYC

- **Polarity:** present
- **Support quote:** using it to screen applicants for its six retail locations in Brooklyn and Manhattan

### F5

Greenleaf relies on ResumeRank as the sole initial screen for all hourly retail positions at NYC locations

- **Polarity:** present
- **Support quote:** Greenleaf's HR department relies on ResumeRank as the sole initial screen for all hourly retail positions

### F6

Last bias audit was conducted in November 2023 by TalentMetrics LLC

- **Polarity:** present
- **Support quote:** ResumeRank was last independently audited for bias by TalentMetrics LLC... in November 2023

### F7

TalentMetrics LLC is HireFlow's contracted vendor partner for ongoing model monitoring

- **Polarity:** present
- **Support quote:** a consulting firm that is also HireFlow's contracted vendor partner for ongoing model monitoring

### F8

HireFlow substantially retrained ResumeRank in June 2024 with updated training data; no new bias audit commissioned

- **Polarity:** present
- **Support quote:** HireFlow substantially retrained the ResumeRank model in June 2024 using updated training data, but did not commission a new bias audit

### F9

Greenleaf has not posted any bias audit summary on its website

- **Polarity:** present
- **Support quote:** Greenleaf has not posted any bias audit summary on its website

### F10

No mention of AEDT use in NYC job postings; no notice provided to candidates before or during application

- **Polarity:** present
- **Support quote:** Greenleaf's NYC job postings... include no mention of AEDT use. No notice of any kind regarding automated screening is provided

### F11

Brooklyn cashier applicant rejected in Jan 2026 without interview; filed DCWP complaint alleging undisclosed automated tool use

- **Polarity:** present
- **Support quote:** A candidate who applied for a cashier position at the Brooklyn location in January 2026 was rejected without interview

### F12

Analysis date is April 16, 2026; LL 144 in force since July 5, 2023; TRAIGA since Jan 1, 2026; CO AIA effective June 30, 2026

- **Polarity:** present
- **Support quote:** Not specified

### F13

Greenleaf is a national grocery chain; Colorado operations plausible but not confirmed in facts

- **Polarity:** unknown
- **Support quote:** Not specified

## Issues (8)

### I1

Does ResumeRank qualify as an AEDT under NYC LL 144?

- **Status:** dispositive

### I2

Is the November 2023 bias audit valid as of January 2026 given the June 2024 retrain and passage of time?

- **Status:** dispositive

### I3

Did TalentMetrics LLC qualify as an independent auditor given its financial relationship with HireFlow?

- **Status:** dispositive

### I4

Has Greenleaf violated LL 144 published results requirements?

- **Status:** dispositive

### I5

Has Greenleaf violated LL 144 candidate notice requirements?

- **Status:** dispositive

### I6

What penalty exposure does Greenleaf face under LL 144?

- **Status:** dispositive

### I7

Does HireFlow or Greenleaf have obligations or exposure under Texas TRAIGA?

- **Status:** collateral

### I8

What obligations will Greenleaf and HireFlow face under Colorado AIA effective June 30, 2026?

- **Status:** collateral

## Rules (18)

### R1

AEDT definition: computational process from ML/AI issuing simplified output used to substantially assist or replace discretionary employment decision-making

- **Citation:** NYC LL 144 §20-870; DCWP Rules §5-300
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R2

Bias audit required no more than one year prior to AEDT use; cannot use AEDT if more than one year since most recent audit

- **Citation:** NYC LL 144 §20-871(a)(1); DCWP Rules §5-301(a)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R3

New bias audit required after substantial modification including retraining on new or updated data

- **Citation:** NYC LL 144 §20-871(d)(2)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R4

Independent auditor must not have financial interest in employer, employment agency, or AEDT vendor/developer

- **Citation:** NYC LL 144 §20-870; DCWP Rules §5-300 (Independent Auditor definition)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R5

Published results: bias audit date, summary of results with data source, unknown categories, applicant counts, rates, impact ratios, and distribution date must be on employer website before AEDT use

- **Citation:** NYC LL 144 §20-871(a)(2), §20-873; DCWP Rules §5-303
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R6

Candidate notice at least 10 business days before AEDT use: inform of AEDT use, qualifications assessed, alternative selection process instructions

- **Citation:** NYC LL 144 §20-872; DCWP Rules §5-304(a)-(c)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R7

Data retention/disclosure: employer must post AEDT data retention policy, data types, sources, and request instructions on website

- **Citation:** DCWP Rules §5-304(d)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R8

> Flagged for review: the internal audit reports that the cited NYC §20-875 does not exist. Please verify both citation and proposition.

Penalties: $500-$1,500 per violation; each use of non-compliant AEDT to screen a single candidate may be a separate violation

- **Citation:** NYC LL 144 §20-875
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R9

Geographic scope: applies based on candidate/employee location, not employer HQ; covers NYC positions and NYC-resident candidates

- **Citation:** NYC LL 144 §20-874
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R10

Prohibited conduct: no person may develop or deploy AI with intent to unlawfully discriminate; requires intentional discrimination, not disparate impact

- **Citation:** TX TRAIGA §551.051
- **Authority:** binding
- **Jurisdiction:** TX
- **Effective as of:** 2026-01-01

### R11

No private employer disclosure/audit/impact assessment requirements; consumer definition excludes employment context; disclosure only for government agencies

- **Citation:** TX TRAIGA §551.001(2), §551.101
- **Authority:** binding
- **Jurisdiction:** TX
- **Effective as of:** 2026-01-01

### R12

Safe harbor for substantial compliance with NIST AI RMF or recognized AI governance standards

- **Citation:** TX TRAIGA §551.301(d)
- **Authority:** binding
- **Jurisdiction:** TX
- **Effective as of:** 2026-01-01

### R13

TRAIGA preempts local TX ordinances on AI but does not preempt other states laws

- **Citation:** TX TRAIGA §551.201
- **Authority:** binding
- **Jurisdiction:** TX
- **Effective as of:** 2026-01-01

### R14

Developer obligations: reasonable care, documentation to deployers on limitations/training data/uses/monitoring, public use case inventory

- **Citation:** CO AIA §6-1-1702
- **Authority:** binding
- **Jurisdiction:** CO
- **Effective as of:** 2026-06-30

### R15

Deployer obligations: NIST AI RMF-aligned risk management program, impact assessments, annual reviews, website statement, consumer notice, data correction, appeal rights

- **Citation:** CO AIA §6-1-1703(2)(a)-(g)
- **Authority:** binding
- **Jurisdiction:** CO
- **Effective as of:** 2026-06-30

### R16

High-risk AI system: AI that makes or is substantial factor in consequential decisions including employment

- **Citation:** CO AIA §6-1-1701(7), §6-1-1701(3)(b)
- **Authority:** binding
- **Jurisdiction:** CO
- **Effective as of:** 2026-06-30

### R17

Small deployer exception: fewer than 50 employees AND does not use own data to train; both conditions required

- **Citation:** CO AIA §6-1-1703(6)
- **Authority:** binding
- **Jurisdiction:** CO
- **Effective as of:** 2026-06-30

### R18

Algorithmic discrimination notice: deployer/developer must notify AG and affected consumers within 90 days of discovery

- **Citation:** CO AIA §6-1-1704
- **Authority:** binding
- **Jurisdiction:** CO
- **Effective as of:** 2026-06-30

## Applications (15)

### A1

ResumeRank is a computational process derived from ML (gradient-boosted model, NLP) issuing simplified output (score 1-100). Greenleaf relies solely on the score with no other factors considered (auto-reject below 70), satisfying DCWP Rules 5-300(i). Used for employment decisions at NYC locations. ResumeRank is an AEDT.

- **Rule ref:** R1
- **Fact refs:** F2, F5
- **Issue ref:** I1
- **Result:** satisfied

### A2

The November 2023 audit is over two years old as of January 2026. Section 20-871(a)(1) requires audit no more than one year prior to use. The audit expired by November 2024 at the latest. Greenleaf has used ResumeRank without a temporally valid audit since at least November 2024.

- **Rule ref:** R2
- **Fact refs:** F6, F12
- **Issue ref:** I2
- **Result:** violated

### A3

HireFlow substantially retrained ResumeRank in June 2024 on updated training data. Section 20-871(d)(2) requires a new bias audit after substantial modification including retraining. No new audit was commissioned. The pre-retrain audit does not satisfy the requirement for the retrained model.

- **Rule ref:** R3
- **Fact refs:** F8
- **Issue ref:** I2
- **Result:** violated

### A4

TalentMetrics LLC is HireFlow's contracted vendor partner for ongoing model monitoring, constituting a direct financial relationship with the AEDT developer. Under 20-870 and DCWP Rules 5-300, an auditor with a financial interest in the vendor that developed the AEDT is not independent. The November 2023 audit was defective from inception.

- **Rule ref:** R4
- **Fact refs:** F7
- **Issue ref:** I3
- **Result:** violated

### A5

Section 20-871(a)(2) and DCWP Rules 5-303 require publication of bias audit date, summary of results, and distribution date on employer website before AEDT use. Greenleaf has posted nothing. Complete violation.

- **Rule ref:** R5
- **Fact refs:** F9
- **Issue ref:** I4
- **Result:** violated

### A6

Section 20-872 and DCWP Rules 5-304 require notice to NYC-resident candidates at least 10 business days before AEDT use. Greenleaf provides no notice of any kind in job postings, on its website, or via email/mail. The January 2026 Brooklyn applicant received no notice. Complete violation.

- **Rule ref:** R6
- **Fact refs:** F10, F11
- **Issue ref:** I5
- **Result:** violated

### A7

DCWP Rules 5-304(d) requires posting of AEDT data retention policy, data types, sources, and request instructions on employer website. Greenleaf has posted no such information. Violated.

- **Rule ref:** R7
- **Fact refs:** F9, F10
- **Issue ref:** I5
- **Result:** violated

### A8

Each use of non-compliant AEDT to screen a single candidate is a separate violation at $500-$1,500. Greenleaf has screened candidates for six NYC locations since March 2025 (13+ months). Multiple independent violation types (no valid audit, no published results, no notice, no data disclosure) compound exposure. Aggregate penalties could be very substantial.

- **Rule ref:** R8
- **Fact refs:** F4, F5, F11
- **Issue ref:** I6
- **Result:** violated

### A9

LL 144 applies based on candidate location. Candidates apply for positions at Brooklyn and Manhattan locations in NYC. Greenleaf's Chicago HQ and HireFlow's Austin location are irrelevant. LL 144 applies.

- **Rule ref:** R9
- **Fact refs:** F4, F11
- **Issue ref:** I1
- **Result:** satisfied

### A10

TRAIGA prohibits only intentional discrimination. No facts suggest HireFlow or Greenleaf developed or deployed ResumeRank with intent to unlawfully discriminate. No TRAIGA violation identified.

- **Rule ref:** R10
- **Fact refs:** F1, F2, F3
- **Issue ref:** I7
- **Result:** satisfied

### A11

TRAIGA imposes no affirmative audit, notice, impact assessment, or disclosure obligations on private employers or developers for employment AI tools. Consumer definition excludes employment context. No obligations triggered.

- **Rule ref:** R11
- **Fact refs:** F1, F3
- **Issue ref:** I7
- **Result:** satisfied

### A12

TRAIGA preempts only local TX ordinances. It does not preempt NYC LL 144 or CO AIA. No preemptive effect on other jurisdictions.

- **Rule ref:** R13
- **Fact refs:** F12
- **Issue ref:** I7
- **Result:** satisfied

### A13

ResumeRank makes consequential employment decisions (auto-reject below 70), qualifying as high-risk AI under CO AIA 6-1-1701(7). However, applicability depends on whether Greenleaf operates in Colorado, which is plausible for a national chain but unconfirmed. If confirmed, both developer and deployer obligations apply.

- **Rule ref:** R16
- **Fact refs:** F2, F5, F13
- **Issue ref:** I8
- **Result:** requires-fact

### A14

Greenleaf has 12,000 employees, far exceeding the 50-employee threshold in 6-1-1703(6)(a). The small deployer exception does not apply. All deployer obligations under 6-1-1703(2) would be required if CO AIA applies.

- **Rule ref:** R17
- **Fact refs:** F3
- **Issue ref:** I8
- **Result:** violated

### A15

If Greenleaf operates in CO, it currently lacks: NIST AI RMF-aligned risk management program, impact assessments, website statement, consumer notice mechanisms, data correction processes, and appeal mechanisms. All would be required by June 30, 2026 (or within 90 days for impact assessments of pre-existing deployments). Significant readiness gap exists.

- **Rule ref:** R15
- **Fact refs:** F3, F9, F10, F13
- **Issue ref:** I8
- **Result:** requires-fact

## Conclusions (3)

### C1

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A1, A2, A3, A4, A5, A6, A7, A8, A9

### C2

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A10, A11, A12

### C3

- **Determination:** conditional
- **Confidence:** medium
- **Support refs:** A13, A14, A15

## Obligations (14)

### O1

Commission new valid bias audit by truly independent auditor for post-June 2024 retrained model before any further AEDT use in NYC

- **Required by:** R2
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Before any further use of AEDT

### O2

Publish bias audit date, summary of results (data source, unknown categories, applicant counts, selection/scoring rates, impact ratios), and distribution date on employment section of website

- **Required by:** R5
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Before any further use of AEDT

### O3

Provide candidate notice at least 10 business days before AEDT use: inform of AEDT use, qualifications assessed, alternative selection process instructions

- **Required by:** R6
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** At least 10 business days before future AEDT use

### O4

Post AEDT data retention policy, data types collected, data sources, and written request instructions on employment section of website

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Before any further use of AEDT

### O5

Respond to pending DCWP complaint; engage LL 144 counsel; preserve all records of ResumeRank use

- **Required by:** R8
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Not specified

### O6

Ensure future bias auditors have no financial interest in HireFlow, Greenleaf, or ResumeRank vendor; TalentMetrics LLC is disqualified

- **Required by:** R4
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Not specified

### O7

Maintain prohibition on intentional discrimination in AI development and deployment under TRAIGA

- **Required by:** R10
- **Status:** mandatory
- **Jurisdiction:** TX
- **Deadline:** Not specified

### O8

Consider implementing NIST AI RMF for TRAIGA safe harbor protection

- **Required by:** R12
- **Status:** safe-harbor
- **Jurisdiction:** TX
- **Deadline:** Not specified

### O9

HireFlow: prepare developer documentation (limitations, training data, intended/inappropriate uses, monitoring guidance) for deployers under CO AIA

- **Required by:** R14
- **Status:** mandatory
- **Jurisdiction:** CO
- **Deadline:** 2026-06-30

### O10

HireFlow: publish public use case inventory of high-risk AI systems available in Colorado

- **Required by:** R14
- **Status:** mandatory
- **Jurisdiction:** CO
- **Deadline:** 2026-06-30

### O11

Greenleaf: implement risk management program consistent with NIST AI 100-1 or ISO/IEC 42001 (not NIST 800-53 or ISO 27001)

- **Required by:** R15
- **Status:** mandatory
- **Jurisdiction:** CO
- **Deadline:** 2026-06-30

### O12

Greenleaf: complete impact assessment for ResumeRank within 90 days of CO AIA effective date for pre-existing deployments

- **Required by:** R15
- **Status:** mandatory
- **Jurisdiction:** CO
- **Deadline:** 2026-09-28

### O13

Greenleaf: implement consumer notice before consequential decisions, data correction opportunities, and meaningful appeal mechanisms under CO AIA

- **Required by:** R15
- **Status:** mandatory
- **Jurisdiction:** CO
- **Deadline:** 2026-06-30

### O14

Greenleaf: publish website statement summarizing deployed high-risk AI systems and algorithmic discrimination risk management under CO AIA

- **Required by:** R15
- **Status:** mandatory
- **Jurisdiction:** CO
- **Deadline:** 2026-06-30

## Graph connections (55)

### E1

- **Src:** F2
- **Dst:** I1
- **Type:** triggers
- **Justification:** ML-based scoring tool raises question of AEDT classification

### E2

- **Src:** F5
- **Dst:** I1
- **Type:** triggers
- **Justification:** Sole reliance on score satisfies DCWP substantially assist/replace threshold

### E3

- **Src:** F4
- **Dst:** I1
- **Type:** triggers
- **Justification:** NYC location establishes geographic jurisdiction

### E4

- **Src:** F6
- **Dst:** I2
- **Type:** triggers
- **Justification:** November 2023 audit date raises temporal validity question

### E5

- **Src:** F8
- **Dst:** I2
- **Type:** triggers
- **Justification:** June 2024 retrain raises substantial modification invalidity

### E6

- **Src:** F7
- **Dst:** I3
- **Type:** triggers
- **Justification:** Vendor partner relationship raises auditor independence question

### E7

- **Src:** F9
- **Dst:** I4
- **Type:** triggers
- **Justification:** No published results on website triggers publication violation

### E8

- **Src:** F10
- **Dst:** I5
- **Type:** triggers
- **Justification:** No candidate notice triggers notice violation

### E9

- **Src:** F11
- **Dst:** I6
- **Type:** triggers
- **Justification:** DCWP complaint triggers penalty exposure analysis

### E10

- **Src:** R1
- **Dst:** A1
- **Type:** applies-to
- **Justification:** AEDT definition applied to ResumeRank characteristics

### E11

- **Src:** R2
- **Dst:** A2
- **Type:** applies-to
- **Justification:** One-year audit requirement applied to November 2023 audit date

### E12

- **Src:** R3
- **Dst:** A3
- **Type:** applies-to
- **Justification:** Substantial modification rule applied to June 2024 retrain

### E13

- **Src:** R4
- **Dst:** A4
- **Type:** applies-to
- **Justification:** Independent auditor definition applied to TalentMetrics vendor relationship

### E14

- **Src:** R5
- **Dst:** A5
- **Type:** applies-to
- **Justification:** Published results requirement applied to absent website disclosures

### E15

- **Src:** R6
- **Dst:** A6
- **Type:** applies-to
- **Justification:** Candidate notice requirement applied to absent notices

### E16

- **Src:** R7
- **Dst:** A7
- **Type:** applies-to
- **Justification:** Data retention disclosure requirement applied to absent website information

### E17

- **Src:** R8
- **Dst:** A8
- **Type:** applies-to
- **Justification:** Per-candidate penalty provision applied to multi-location screening

### E18

- **Src:** R9
- **Dst:** A9
- **Type:** applies-to
- **Justification:** Geographic scope rule confirms NYC jurisdiction based on candidate location

### E19

- **Src:** R10
- **Dst:** A10
- **Type:** applies-to
- **Justification:** TRAIGA intentional discrimination prohibition applied to facts

### E20

- **Src:** R11
- **Dst:** A11
- **Type:** applies-to
- **Justification:** TRAIGA no-employer-obligation provision applied to HireFlow and Greenleaf

### E21

- **Src:** R13
- **Dst:** A12
- **Type:** applies-to
- **Justification:** TRAIGA preemption scope applied to multi-jurisdiction analysis

### E22

- **Src:** A1
- **Dst:** C1
- **Type:** supports
- **Justification:** AEDT classification confirmed, triggering all LL 144 obligations

### E23

- **Src:** A2
- **Dst:** C1
- **Type:** fails-element
- **Justification:** Expired audit establishes non-compliance with bias audit requirement

### E24

- **Src:** A3
- **Dst:** C1
- **Type:** fails-element
- **Justification:** Post-retrain audit absence establishes independent non-compliance ground

### E25

- **Src:** A4
- **Dst:** C1
- **Type:** fails-element
- **Justification:** Non-independent auditor means no valid audit has ever existed for ResumeRank

### E26

- **Src:** A5
- **Dst:** C1
- **Type:** fails-element
- **Justification:** Complete absence of published results violates 20-871(a)(2)

### E27

- **Src:** A6
- **Dst:** C1
- **Type:** fails-element
- **Justification:** Complete absence of candidate notice violates 20-872

### E28

- **Src:** A7
- **Dst:** C1
- **Type:** fails-element
- **Justification:** Absence of data retention disclosure violates DCWP Rules 5-304(d)

### E29

- **Src:** A8
- **Dst:** C1
- **Type:** fails-element
- **Justification:** Per-candidate penalty exposure is substantial across six locations over 13+ months

### E30

- **Src:** A9
- **Dst:** C1
- **Type:** supports
- **Justification:** Geographic jurisdiction confirmed for NYC candidate locations

### E31

- **Src:** A10
- **Dst:** C2
- **Type:** satisfies-element
- **Justification:** No intentional discrimination found; TRAIGA prohibition not violated

### E32

- **Src:** A11
- **Dst:** C2
- **Type:** satisfies-element
- **Justification:** No affirmative obligations triggered under TRAIGA for private employers

### E33

- **Src:** A12
- **Dst:** C2
- **Type:** supports
- **Justification:** TRAIGA preemption does not affect other jurisdictions

### E34

- **Src:** A13
- **Dst:** C3
- **Type:** supports
- **Justification:** CO AIA applicability conditional on confirmed Colorado operations

### E35

- **Src:** A14
- **Dst:** C3
- **Type:** fails-element
- **Justification:** Small deployer exception inapplicable; full obligations would apply

### E36

- **Src:** A15
- **Dst:** C3
- **Type:** fails-element
- **Justification:** Significant readiness gaps identified across all CO AIA deployer obligations

### E37

- **Src:** R2
- **Dst:** O1
- **Type:** triggers
- **Justification:** Invalid audit requires new compliant audit before further AEDT use

### E38

- **Src:** R4
- **Dst:** O6
- **Type:** triggers
- **Justification:** Non-independent auditor requires engagement of qualified independent auditor

### E39

- **Src:** R5
- **Dst:** O2
- **Type:** triggers
- **Justification:** Absent published results require immediate website publication

### E40

- **Src:** R6
- **Dst:** O3
- **Type:** triggers
- **Justification:** Absent candidate notice requires implementation of notice procedures

### E41

- **Src:** R7
- **Dst:** O4
- **Type:** triggers
- **Justification:** Absent data disclosure requires website posting of retention policy and data info

### E42

- **Src:** R8
- **Dst:** O5
- **Type:** triggers
- **Justification:** DCWP complaint requires legal response and record preservation

### E43

- **Src:** R10
- **Dst:** O7
- **Type:** triggers
- **Justification:** TRAIGA prohibition requires ongoing compliance with non-discrimination mandate

### E44

- **Src:** R12
- **Dst:** O8
- **Type:** triggers
- **Justification:** NIST AI RMF safe harbor available and advisable for TRAIGA protection

### E45

- **Src:** R14
- **Dst:** O9
- **Type:** triggers
- **Justification:** CO AIA developer documentation obligations require preparation by June 30, 2026

### E46

- **Src:** R14
- **Dst:** O10
- **Type:** triggers
- **Justification:** CO AIA public use case inventory obligation requires preparation by June 30, 2026

### E47

- **Src:** R15
- **Dst:** O11
- **Type:** triggers
- **Justification:** CO AIA risk management program obligation requires NIST AI RMF alignment by June 30, 2026

### E48

- **Src:** R15
- **Dst:** O12
- **Type:** triggers
- **Justification:** CO AIA impact assessment for pre-existing deployment due within 90 days of effective date

### E49

- **Src:** R15
- **Dst:** O13
- **Type:** triggers
- **Justification:** CO AIA consumer notice, data correction, and appeal obligations effective June 30, 2026

### E50

- **Src:** R15
- **Dst:** O14
- **Type:** triggers
- **Justification:** CO AIA website statement obligation effective June 30, 2026

### E51

- **Src:** C1
- **Dst:** O1
- **Type:** triggers
- **Justification:** NYC non-compliance determination drives mandatory remediation obligations

### E52

- **Src:** C1
- **Dst:** O2
- **Type:** triggers
- **Justification:** NYC non-compliance determination drives mandatory publication obligation

### E53

- **Src:** C1
- **Dst:** O3
- **Type:** triggers
- **Justification:** NYC non-compliance determination drives mandatory notice obligation

### E54

- **Src:** C3
- **Dst:** O11
- **Type:** triggers
- **Justification:** Conditional CO determination drives readiness obligations if CO operations confirmed

### E55

- **Src:** F13
- **Dst:** I8
- **Type:** triggers
- **Justification:** Unknown CO operations status raises CO AIA applicability question
