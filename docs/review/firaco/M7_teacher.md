# M7 — NurseMatch Hospital Hiring — teacher FIRACO reasoning

Unverified model output for legal review. Citations, facts, applications, and obligations may be incorrect. Text and node IDs below are preserved from the saved reference graph.

[Read case](../../../data/cases/M7_nursematch_hospital_co.md) · [Review brief](../../PROF_PHILIPP_REVIEW.md)

Teacher: claude-opus-4-6. Source: data/outputs/graphs/M7_reference.json.

Source SHA-256: `aa58538a7166001b12972bb1eb71caec8e626ccf0dcc2bac10d7e5b86ae15ad8`.

## Facts (15)

### F1

St. Brendan is a hospital system in Denver, CO with 1,900 FTEs, doing business in Colorado

- **Polarity:** present
- **Support quote:** St. Brendan Regional Health is a hospital system in Denver, Colorado, with 1,900 full-time employees

### F2

St. Brendan uses NurseMatch, licensed from Altura Workforce, to hire nurses since early 2025

- **Polarity:** present
- **Support quote:** Since early 2025 St. Brendan has used 'NurseMatch', a system licensed from Altura Workforce, when hiring nurses

### F3

NurseMatch scores every applicant and produces a shortlist of the top 20%; recruiters interview only shortlisted applicants

- **Polarity:** present
- **Support quote:** NurseMatch scores every applicant and produces a shortlist containing the top 20%. Recruiters interview only applicants on the shortlist

### F4

In Q4 2025, 91% of hires came from top 10% of scores; no applicant outside shortlist was hired

- **Polarity:** present
- **Support quote:** 91% of nurses hired came from the top tenth of NurseMatch scores, and no applicant outside the shortlist was hired

### F5

St. Brendan claims NurseMatch performs a preparatory task with humans deciding

- **Polarity:** present
- **Support quote:** It performs a preparatory task. People conduct the interviews and people decide.

### F6

Risk management program modeled on NIST AI RMF 1.0 adopted February 2025 with governance committee

- **Polarity:** present
- **Support quote:** A risk management program modeled on the NIST AI Risk Management Framework 1.0, adopted in February 2025, with a governance committee

### F7

Impact assessment completed February 2025, not updated since

- **Polarity:** present
- **Support quote:** An impact assessment of NurseMatch completed in February 2025. It has not been updated since.

### F8

Altura retrained NurseMatch on new data in November 2025, changed scoring features, released as version 3

- **Polarity:** present
- **Support quote:** In November 2025, Altura retrained NurseMatch on new data and changed several scoring features, releasing it as version 3

### F9

No new impact assessment performed after version 3 release

- **Polarity:** present
- **Support quote:** St. Brendan did not perform a new impact assessment

### F10

No deployment review for discriminatory outcomes since February 2025

- **Polarity:** present
- **Support quote:** No review of the deployment for discriminatory outcomes has been done since February 2025

### F11

Website statement about NurseMatch and risk management posted on careers section

- **Polarity:** present
- **Support quote:** A statement about NurseMatch and how its risks are managed is posted on the careers section of the website

### F12

Applicants first learn of AI use from rejection email sent after the decision

- **Polarity:** present
- **Support quote:** Applicants first learn that an AI system was used from the rejection email, sent after the decision

### F13

Applicants may email HR to correct resume information

- **Polarity:** present
- **Support quote:** An applicant may email HR to correct resume information

### F14

No mechanism exists for applicants to appeal a rejection

- **Polarity:** present
- **Support quote:** There is no way to appeal a rejection

### F15

NurseMatch is used for employment hiring decisions (nurses)

- **Polarity:** present
- **Support quote:** St. Brendan has used NurseMatch when hiring nurses

## Issues (8)

### I1

Whether NurseMatch is a high-risk AI system under CO AIA section 6-1-1701(7)

- **Status:** dispositive

### I2

Whether the preparatory-task exclusion under section 6-1-1701(7)(d) applies to NurseMatch

- **Status:** dispositive

### I3

Whether NurseMatch is a substantial factor under section 6-1-1701(9) despite human interviews and decisions

- **Status:** dispositive

### I4

Whether the February 2025 impact assessment is current given annual requirement and November 2025 retraining

- **Status:** dispositive

### I5

Whether post-decision applicant notice satisfies section 6-1-1703(2)(e) pre-decision requirement

- **Status:** dispositive

### I6

Whether absence of appeal mechanism violates section 6-1-1703(2)(g)

- **Status:** dispositive

### I7

Whether annual deployment review requirement under section 6-1-1703(2)(c) is satisfied

- **Status:** dispositive

### I8

Whether small deployer exception under section 6-1-1703(6) applies to St. Brendan

- **Status:** collateral

## Rules (16)

### R1

Definition of high-risk AI system: AI system that makes or is substantial factor in making a consequential decision

- **Citation:** CO AIA section 6-1-1701(7)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R2

Employment or employment opportunity is a consequential decision

- **Citation:** CO AIA section 6-1-1701(3)(b)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R3

Substantial factor definition: materially contributed; human review based primarily on AI output does not negate

- **Citation:** CO AIA section 6-1-1701(9)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R4

Exclusion for systems performing a preparatory task to an assessment relevant to consequential decisions

- **Citation:** CO AIA section 6-1-1701(7)(d)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R5

Impact assessment required: pre-deployment or 90 days post-effective date; annually; within 90 days of substantial modification

- **Citation:** CO AIA section 6-1-1703(2)(b)(I)-(III)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R6

Annual deployment review to ensure system is not causing algorithmic discrimination

- **Citation:** CO AIA section 6-1-1703(2)(c)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R7

Pre-decision consumer notice with five required elements before consequential decision is made

- **Citation:** CO AIA section 6-1-1703(2)(e)(I)-(V)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R8

Right to correct incorrect personal data processed by high-risk AI system

- **Citation:** CO AIA section 6-1-1703(2)(f)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R9

Meaningful opportunity to appeal a consequential decision in which high-risk AI was substantial factor

- **Citation:** CO AIA section 6-1-1703(2)(g)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R10

Small deployer exception: fewer than 50 FTEs AND does not use own data to train; both conditions required

- **Citation:** CO AIA section 6-1-1703(6)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R11

Risk management program consistent with NIST AI RMF 1.0 or substantially equivalent framework

- **Citation:** CO AIA section 6-1-1703(2)(a)(I)-(III)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R12

Rebuttable presumption of reasonable care if deployer complied with section 6-1-1703

- **Citation:** CO AIA section 6-1-1703(3)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R13

Enforcement: deceptive trade practice, AG exclusive authority, up to $20,000 per violation

- **Citation:** CO AIA section 6-1-1706
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R14

Website statement summarizing high-risk AI systems deployed and risk management

- **Citation:** CO AIA section 6-1-1703(2)(d)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R15

Deployer duty of reasonable care to protect consumers from algorithmic discrimination risks

- **Citation:** CO AIA section 6-1-1703(1)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R16

90-day notification to AG and affected consumers if algorithmic discrimination discovered

- **Citation:** CO AIA section 6-1-1704
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

## Applications (11)

### A1

NurseMatch is a machine-based system processing applicant inputs and producing scores and shortlists (outputs) used in employment hiring (consequential decision under R2). It makes or is a substantial factor in making consequential decisions, meeting the high-risk AI system definition.

- **Rule ref:** R1
- **Fact refs:** F2, F3, F15
- **Issue ref:** I1
- **Result:** satisfied

### A2

The preparatory-task exclusion does not apply. NurseMatch eliminates 80% of candidates from all further consideration. Zero applicants outside the shortlist were hired. The system does not merely prepare information for human assessment; it makes a dispositive gatekeeping determination that controls the entire candidate pool. This goes far beyond a preparatory task.

- **Rule ref:** R4
- **Fact refs:** F3, F4, F5
- **Issue ref:** I2
- **Result:** violated

### A3

NurseMatch materially contributes to hiring decisions: it defines the entire interview pool, no excluded applicant was hired, and 91% of hires came from the top decile. Human review operates only within NurseMatch-defined pool, meaning it is based primarily on AI output. Under section 6-1-1701(9), such human review does not negate substantial factor status.

- **Rule ref:** R3
- **Fact refs:** F3, F4
- **Issue ref:** I3
- **Result:** satisfied

### A4

Impact assessment from February 2025 is non-compliant on two grounds: (1) Annual update was due by February 2026 under subsection (II) but not performed; (2) November 2025 retraining with new data and changed scoring features is an intentional and substantial modification requiring new assessment within 90 days under subsection (III), which was not performed. The 90-day grace period for pre-existing deployments under subsection (I) does not cure these independent violations.

- **Rule ref:** R5
- **Fact refs:** F7, F8, F9
- **Issue ref:** I4
- **Result:** violated

### A5

Section 6-1-1703(2)(e)(I) requires notice 'before the decision is made.' St. Brendan provides notice only in the rejection email, after the consequential decision. Post-decision notice directly violates the pre-decision timing requirement regardless of content.

- **Rule ref:** R7
- **Fact refs:** F12
- **Issue ref:** I5
- **Result:** violated

### A6

Section 6-1-1703(2)(g) requires a meaningful opportunity to appeal a consequential decision. St. Brendan provides no appeal mechanism whatsoever. The data correction process under section 6-1-1703(2)(f) is a separate obligation and does not satisfy the appeal requirement.

- **Rule ref:** R9
- **Fact refs:** F14
- **Issue ref:** I6
- **Result:** violated

### A7

Section 6-1-1703(2)(c) requires at least annual review of deployment to ensure no algorithmic discrimination. No review has been conducted since February 2025. As of June 30, 2026, this will be over 16 months without review, violating the annual requirement.

- **Rule ref:** R6
- **Fact refs:** F10
- **Issue ref:** I7
- **Result:** violated

### A8

Small deployer exception requires fewer than 50 FTEs (condition a). St. Brendan has 1,900 FTEs, failing the first condition. Both conditions must be met; exception is inapplicable.

- **Rule ref:** R10
- **Fact refs:** F1
- **Issue ref:** I8
- **Result:** violated

### A9

St. Brendan adopted a NIST AI RMF 1.0-based program with governance committee, facially satisfying section 6-1-1703(2)(a)(III). However, the program failed to trigger reassessment after the November 2025 substantial modification and has not conducted ongoing monitoring, suggesting operational deficiency in identifying and mitigating algorithmic discrimination risks per subsection (I).

- **Rule ref:** R11
- **Fact refs:** F6, F8, F10
- **Issue ref:** I7
- **Result:** partial

### A10

St. Brendan posts a statement about NurseMatch and risk management on the careers section of its website, facially satisfying section 6-1-1703(2)(d).

- **Rule ref:** R14
- **Fact refs:** F11
- **Issue ref:** I1
- **Result:** satisfied

### A11

Rebuttable presumption of reasonable care under section 6-1-1703(3) requires compliance with section 6-1-1703. Multiple violations (impact assessment, notice, appeal, annual review) preclude the presumption.

- **Rule ref:** R12
- **Fact refs:** F7, F9, F10, F12, F14
- **Issue ref:** I1
- **Result:** violated

## Conclusions (9)

### C1

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A1, A2, A3

### C2

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A4

### C3

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A5

### C4

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A6

### C5

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A7

### C6

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A8

### C7

- **Determination:** conditional
- **Confidence:** medium
- **Support refs:** A9

### C8

- **Determination:** compliant
- **Confidence:** medium
- **Support refs:** A10

### C9

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A11

## Obligations (8)

### O1

Complete updated impact assessment for NurseMatch v3 addressing all elements of section 6-1-1701(8)

- **Required by:** R5
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-09-28

### O2

Redesign applicant notification to provide all five elements of section 6-1-1703(2)(e) before the consequential decision is made

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O3

Establish meaningful appeal mechanism for applicants affected by NurseMatch decisions per section 6-1-1703(2)(g)

- **Required by:** R9
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O4

Conduct annual deployment review of NurseMatch for algorithmic discrimination per section 6-1-1703(2)(c)

- **Required by:** R6
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O5

Operationalize risk management program to ensure reassessment triggers upon substantial modifications and ongoing monitoring

- **Required by:** R11
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O6

Review and expand data correction process to cover all personal data processed by NurseMatch per section 6-1-1703(2)(f)

- **Required by:** R8
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O7

Request from Altura Workforce all developer documentation required under section 6-1-1702(2) including limitations, training data, and monitoring guidance

- **Required by:** R11
- **Status:** recommended
- **Jurisdiction:** Colorado
- **Deadline:** Not specified

### O8

If algorithmic discrimination is discovered, notify AG and affected consumers within 90 days per section 6-1-1704

- **Required by:** R16
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** Not specified

## Graph connections (43)

### E1

- **Src:** F2
- **Dst:** I1
- **Type:** triggers
- **Justification:** Use of NurseMatch raises question of high-risk classification

### E2

- **Src:** F3
- **Dst:** I1
- **Type:** triggers
- **Justification:** Shortlisting function raises high-risk and substantial factor questions

### E3

- **Src:** F5
- **Dst:** I2
- **Type:** triggers
- **Justification:** St. Brendan claims preparatory task exclusion applies

### E4

- **Src:** F4
- **Dst:** I3
- **Type:** triggers
- **Justification:** Hiring outcomes data relevant to substantial factor analysis

### E5

- **Src:** F7
- **Dst:** I4
- **Type:** triggers
- **Justification:** Stale impact assessment raises currency question

### E6

- **Src:** F8
- **Dst:** I4
- **Type:** triggers
- **Justification:** November 2025 retraining triggers substantial modification analysis

### E7

- **Src:** F12
- **Dst:** I5
- **Type:** triggers
- **Justification:** Post-decision notice raises timing compliance question

### E8

- **Src:** F14
- **Dst:** I6
- **Type:** triggers
- **Justification:** Absence of appeal mechanism raises section 6-1-1703(2)(g) question

### E9

- **Src:** F10
- **Dst:** I7
- **Type:** triggers
- **Justification:** No deployment review since February 2025 raises annual review question

### E10

- **Src:** F1
- **Dst:** I8
- **Type:** triggers
- **Justification:** 1,900 FTEs relevant to small deployer exception analysis

### E11

- **Src:** R1
- **Dst:** A1
- **Type:** applies-to
- **Justification:** High-risk AI system definition applied to NurseMatch

### E12

- **Src:** R2
- **Dst:** A1
- **Type:** applies-to
- **Justification:** Employment as consequential decision applied to nurse hiring

### E13

- **Src:** R4
- **Dst:** A2
- **Type:** applies-to
- **Justification:** Preparatory task exclusion analyzed against NurseMatch function

### E14

- **Src:** R3
- **Dst:** A3
- **Type:** applies-to
- **Justification:** Substantial factor definition applied to NurseMatch gatekeeping role

### E15

- **Src:** R5
- **Dst:** A4
- **Type:** applies-to
- **Justification:** Impact assessment timing requirements applied to February 2025 assessment

### E16

- **Src:** R6
- **Dst:** A7
- **Type:** applies-to
- **Justification:** Annual review requirement applied to absence of review

### E17

- **Src:** R7
- **Dst:** A5
- **Type:** applies-to
- **Justification:** Pre-decision notice requirement applied to post-decision rejection email

### E18

- **Src:** R9
- **Dst:** A6
- **Type:** applies-to
- **Justification:** Appeal right requirement applied to absence of appeal mechanism

### E19

- **Src:** R10
- **Dst:** A8
- **Type:** applies-to
- **Justification:** Small deployer exception applied to 1,900-FTE hospital system

### E20

- **Src:** R11
- **Dst:** A9
- **Type:** applies-to
- **Justification:** Risk management program requirements applied to NIST-based program

### E21

- **Src:** R14
- **Dst:** A10
- **Type:** applies-to
- **Justification:** Website disclosure requirement applied to careers page statement

### E22

- **Src:** R12
- **Dst:** A11
- **Type:** applies-to
- **Justification:** Rebuttable presumption analyzed against multiple violations

### E23

- **Src:** A1
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** NurseMatch meets high-risk AI system definition

### E24

- **Src:** A2
- **Dst:** C1
- **Type:** fails-element
- **Justification:** Preparatory task exclusion does not apply to NurseMatch

### E25

- **Src:** A3
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** NurseMatch is a substantial factor despite human involvement

### E26

- **Src:** A4
- **Dst:** C2
- **Type:** fails-element
- **Justification:** Impact assessment is stale on two independent grounds

### E27

- **Src:** A5
- **Dst:** C3
- **Type:** fails-element
- **Justification:** Post-decision notice violates pre-decision requirement

### E28

- **Src:** A6
- **Dst:** C4
- **Type:** fails-element
- **Justification:** No appeal mechanism exists

### E29

- **Src:** A7
- **Dst:** C5
- **Type:** fails-element
- **Justification:** No annual deployment review conducted

### E30

- **Src:** A8
- **Dst:** C6
- **Type:** fails-element
- **Justification:** Small deployer exception inapplicable due to 1,900 FTEs

### E31

- **Src:** A9
- **Dst:** C7
- **Type:** satisfies-element
- **Justification:** Framework adopted but operational execution is deficient

### E32

- **Src:** A10
- **Dst:** C8
- **Type:** satisfies-element
- **Justification:** Website disclosure facially compliant

### E33

- **Src:** A11
- **Dst:** C9
- **Type:** fails-element
- **Justification:** Multiple violations preclude rebuttable presumption

### E34

- **Src:** R5
- **Dst:** O1
- **Type:** triggers
- **Justification:** Impact assessment must be updated for NurseMatch v3

### E35

- **Src:** R7
- **Dst:** O2
- **Type:** triggers
- **Justification:** Pre-decision notice process must be redesigned

### E36

- **Src:** R9
- **Dst:** O3
- **Type:** triggers
- **Justification:** Appeal mechanism must be established

### E37

- **Src:** R6
- **Dst:** O4
- **Type:** triggers
- **Justification:** Annual deployment review must be conducted

### E38

- **Src:** R11
- **Dst:** O5
- **Type:** triggers
- **Justification:** Risk management program must be operationalized

### E39

- **Src:** R8
- **Dst:** O6
- **Type:** triggers
- **Justification:** Data correction process must be reviewed and expanded

### E40

- **Src:** R11
- **Dst:** O7
- **Type:** triggers
- **Justification:** Developer documentation needed to support deployer compliance

### E41

- **Src:** R16
- **Dst:** O8
- **Type:** triggers
- **Justification:** AG notification obligation if discrimination discovered

### E42

- **Src:** F15
- **Dst:** I1
- **Type:** triggers
- **Justification:** Nurse hiring is employment, a consequential decision category

### E43

- **Src:** F9
- **Dst:** I4
- **Type:** triggers
- **Justification:** Failure to update assessment after retraining raises compliance question
