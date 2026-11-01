# H8 — Northwind Credit, Lending in Colorado and Hiring in New York — teacher FIRACO reasoning

Unverified model output for legal review. Citations, facts, applications, and obligations may be incorrect. Text and node IDs below are preserved from the saved reference graph.

[Read case](../../../data/cases/H8_northwind_lending_hiring_co_nyc.md) · [Review brief](../../PROF_PHILIPP_REVIEW.md)

Teacher: claude-opus-4-6. Source: data/outputs/graphs/H8_reference.json.

Source SHA-256: `926a19709f80d716c5f56fc65c946fd135a6d7882313c272654fa06bc0f8bd6e`.

The internal audit flags at least one rule below for a suspect NYC §20-875 citation. Other errors may also be present.

## Facts (15)

### F1

Northwind Credit headquartered in Denver, CO, 180 employees, 60 in Brooklyn, NY

- **Polarity:** present
- **Support quote:** consumer lender headquartered in Denver, Colorado, with 180 employees, 60 of whom work in Brooklyn

### F2

Northwind built UnderwriteOne internally and trained it on its own loan performance data

- **Polarity:** present
- **Support quote:** Northwind's data science team built UnderwriteOne... trained it on its own loan performance data

### F3

Sub-$10K loans auto-decided; larger loans go to underwriter who sees UnderwriteOne recommendation

- **Polarity:** present
- **Support quote:** Loans under $10,000 are approved or denied automatically. Larger loans go to an underwriter, who sees UnderwriteOne's recommendation

### F4

March 2026 internal test found 18pp lower approval rate for age 62+ due to years-to-retirement feature

- **Polarity:** present
- **Support quote:** approval rates for applicants aged 62 and older were 18 percentage points lower... cause was a feature measuring years to expected retirement

### F5

Corrected model scheduled for August 2026; current discriminatory model remains in use

- **Polarity:** present
- **Support quote:** A corrected model is scheduled for release in August 2026. Until then the current model remains in use

### F6

No AI risk management program, no impact assessment, no consumer notice, no data correction, no appeal, no website disclosure

- **Polarity:** present
- **Support quote:** Northwind has no AI risk management program, has completed no impact assessment, does not tell loan applicants that an AI system is used

### F7

HireSignal licensed from Praxis Talent ranks applicants; top quarter interviewed for Brooklyn and remote NYC roles

- **Polarity:** present
- **Support quote:** Northwind uses HireSignal, a tool licensed from Praxis Talent that ranks applicants. Only the top quarter are interviewed

### F8

HireSignal audited April 8 2025 by independent Dalloway Audit; Praxis retrained on new data December 2025; no new audit

- **Polarity:** present
- **Support quote:** audited on April 8, 2025 by Dalloway Audit... In December 2025 Praxis retrained HireSignal on new data. No further audit has been performed

### F9

HireSignal used for hiring rounds January 2026, March 2026, and late April 2026 scheduled

- **Polarity:** present
- **Support quote:** Northwind used HireSignal for hiring rounds in January 2026 and March 2026, and has another scheduled for late April 2026

### F10

Careers page has April 2025 audit summary but no distribution date; applicant notice provided 10 days before screening

- **Polarity:** present
- **Support quote:** careers page has a clearly labeled section containing the April 2025 audit summary. It does not state HireSignal's distribution date

### F11

Northwind has 180 employees, exceeding 50-employee threshold

- **Polarity:** present
- **Support quote:** 180 employees

### F12

Northwind used its own data to train UnderwriteOne

- **Polarity:** present
- **Support quote:** trained it on its own loan performance data

### F13

Outside counsel advises breach of reasonable care, notification duties triggered, accelerate correction

- **Polarity:** present
- **Support quote:** Fenwick Laurel LLP advises... continued use after June 30, 2026 would breach the duty of reasonable care

### F14

CFO says pre-effective-date discovery does not count

- **Polarity:** present
- **Support quote:** We found it before the law took effect, so it does not count

### F15

Trade blog says dual developer-deployer only needs deployer section

- **Polarity:** present
- **Support quote:** a company that both builds and uses its own model only needs to comply with the deployer section

## Issues (7)

### I1

Whether Northwind is developer, deployer, or both under CO AIA and whether trade blog is correct

- **Status:** dispositive

### I2

Whether UnderwriteOne is high-risk for both automated and underwriter-reviewed loans

- **Status:** dispositive

### I3

Northwind's CO AIA obligations and deadlines for pre-effective-date deployed system

- **Status:** dispositive

### I4

Whether March 2026 finding is algorithmic discrimination and consequences of pre-effective-date discovery with post-effective-date use

- **Status:** dispositive

### I5

Availability of rebuttable presumption of reasonable care and cure safe harbor

- **Status:** dispositive

### I6

Validity of HireSignal bias audit for Jan, Mar, and Apr 2026 rounds and publication sufficiency

- **Status:** dispositive

### I7

Penalty exposure and enforcement in each jurisdiction

- **Status:** dispositive

## Rules (26)

### R1

Developer definition: person doing business in state that develops or substantially modifies AI system intended or known to be high-risk

- **Citation:** CO AIA §6-1-1701(6)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R2

Deployer definition: person doing business in state that deploys a high-risk AI system

- **Citation:** CO AIA §6-1-1701(5)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R3

High-risk AI system: makes or is substantial factor in making a consequential decision

- **Citation:** CO AIA §6-1-1701(7)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R4

Consequential decision includes financial or lending service decisions

- **Citation:** CO AIA §6-1-1701(3)(c)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R5

Substantial factor: human review does not negate if based primarily on AI output

- **Citation:** CO AIA §6-1-1701(9)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R6

Algorithmic discrimination: unlawful differential treatment or impact on basis of age and other protected classes

- **Citation:** CO AIA §6-1-1701(1)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R7

Developer obligations: reasonable care, documentation, public use case inventory

- **Citation:** CO AIA §6-1-1702
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R8

Deployer obligations: risk management program, impact assessment, annual review, public statement, consumer notice, data correction, appeal

- **Citation:** CO AIA §6-1-1703(2)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R9

Small deployer exception: fewer than 50 employees AND does not use own data to train; both required

- **Citation:** CO AIA §6-1-1703(6)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R10

Notification of algorithmic discrimination to AG and consumers within 90 days of discovery

- **Citation:** CO AIA §6-1-1704
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R11

Enforcement: deceptive trade practice, AG exclusive, up to $20,000 per violation

- **Citation:** CO AIA §6-1-1706
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R12

Rebuttable presumption of reasonable care if developer/deployer complied with respective section

- **Citation:** CO AIA §6-1-1702(4) and §6-1-1703(3)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R13

AEDT definition: computational process issuing simplified output to substantially assist or replace discretionary employment decisions

- **Citation:** NYC LL 144 §20-870 and DCWP Rules §5-300
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R14

Bias audit required no more than one year prior to use of AEDT

- **Citation:** NYC LL 144 §20-871(a)(1) and DCWP Rules §5-301(a)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R15

New bias audit required after substantial modification including retraining on new or updated data

- **Citation:** NYC LL 144 §20-871(d)(2)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R16

Independent auditor must have no employment or financial interest in employer, agency, or developer

- **Citation:** NYC LL 144 §20-870 (independent auditor)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R17

Published results must include distribution date of the AEDT

- **Citation:** DCWP Rules §5-303(a)(2)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R18

Candidate notice at least 10 business days before use identifying AEDT, qualifications assessed, alternative process

- **Citation:** NYC LL 144 §20-872 and DCWP Rules §5-304
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R19

> Flagged for review: the internal audit reports that the cited NYC §20-875 does not exist. Please verify both citation and proposition.

Penalties $500-$1,500 per violation; each candidate screened may be separate violation

- **Citation:** NYC LL 144 §20-875
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R20

Geographic scope based on candidate location not employer location; covers NYC residents including remote roles

- **Citation:** NYC LL 144 §20-874
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R21

Prohibits AI deployment with intent to unlawfully discriminate; disparate impact alone insufficient

- **Citation:** TX TRAIGA §551.051
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R22

TRAIGA preempts local Texas AI ordinances only; no effect on other states laws

- **Citation:** TX TRAIGA §551.201
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R23

AG-only enforcement, $10K-$200K per violation, safe harbor for internal discovery and NIST compliance

- **Citation:** TX TRAIGA §551.301
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R24

No private employer obligations for AI hiring disclosure, bias audits, impact assessments, or appeals

- **Citation:** TX TRAIGA §551.101 note
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R25

Cure safe harbor: rebuttable presumption if violation discovered internally and cured with AG notice within 60 days

- **Citation:** CO AIA §6-1-1706(4)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R26

Impact assessment for pre-effective-date systems due within 90 days after June 30, 2026

- **Citation:** CO AIA §6-1-1703(2)(b)(I)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

## Applications (22)

### A1

Northwind does business in Colorado and its data science team built UnderwriteOne for lending decisions (a consequential decision), making it a developer of a high-risk AI system under §6-1-1701(6).

- **Rule ref:** R1
- **Fact refs:** F1, F2
- **Issue ref:** I1
- **Result:** satisfied

### A2

Northwind does business in Colorado and deploys UnderwriteOne to process loan applications, making it a deployer under §6-1-1701(5). Northwind is both developer and deployer.

- **Rule ref:** R2
- **Fact refs:** F1, F2, F3
- **Issue ref:** I1
- **Result:** satisfied

### A3

Personal loan approval/denial is a decision on the provision or denial of a financial or lending service under §6-1-1701(3)(c), constituting a consequential decision.

- **Rule ref:** R4
- **Fact refs:** F3
- **Issue ref:** I2
- **Result:** satisfied

### A4

For sub-$10K loans, UnderwriteOne makes the consequential decision directly. It is a high-risk AI system under §6-1-1701(7).

- **Rule ref:** R3
- **Fact refs:** F3
- **Issue ref:** I2
- **Result:** satisfied

### A5

For larger loans, the underwriter sees UnderwriteOne's recommendation as the primary input. Under §6-1-1701(9), human review based primarily on AI output does not negate substantial factor status. UnderwriteOne is high-risk for these loans too.

- **Rule ref:** R5
- **Fact refs:** F3
- **Issue ref:** I2
- **Result:** satisfied

### A6

Northwind has 180 employees (exceeds 50 threshold) and uses its own data to train. Both conditions of the exception fail. The small deployer exception is unavailable.

- **Rule ref:** R9
- **Fact refs:** F11, F12
- **Issue ref:** I3
- **Result:** violated

### A7

Northwind has no risk management program, no impact assessment, no public statement, no consumer notice, no data correction mechanism, and no appeal process. All deployer obligations under §6-1-1703(2) are unmet.

- **Rule ref:** R8
- **Fact refs:** F6
- **Issue ref:** I3
- **Result:** violated

### A8

Northwind has not made developer documentation available and has no public use case inventory. All developer obligations under §6-1-1702 are unmet.

- **Rule ref:** R7
- **Fact refs:** F6
- **Issue ref:** I3
- **Result:** violated

### A9

18pp lower approval rate for age 62+ applicants with similar credit profiles constitutes differential impact disfavoring individuals on basis of age, violating ECOA and state antidiscrimination laws. This meets the definition of algorithmic discrimination under §6-1-1701(1).

- **Rule ref:** R6
- **Fact refs:** F4
- **Issue ref:** I4
- **Result:** satisfied

### A10

Northwind discovered algorithmic discrimination in March 2026. Once §6-1-1704 takes effect June 30, 2026, the 90-day notification clock begins. Northwind must notify the AG and affected consumers by September 28, 2026. No notification has been made.

- **Rule ref:** R10
- **Fact refs:** F4, F5
- **Issue ref:** I4
- **Result:** violated

### A11

The rebuttable presumption requires compliance with §6-1-1702 (developer) or §6-1-1703 (deployer). Northwind has complied with neither. The presumption is unavailable.

- **Rule ref:** R12
- **Fact refs:** F6
- **Issue ref:** I5
- **Result:** violated

### A12

Northwind discovered the issue through internal testing (prong a satisfied). But it has not cured the violation or notified the AG within 60 days (prong b not yet satisfied). The safe harbor is potentially available if Northwind accelerates the fix and notifies the AG by August 29, 2026.

- **Rule ref:** R25
- **Fact refs:** F4, F5
- **Issue ref:** I5
- **Result:** partial

### A13

Praxis retrained HireSignal on new data in December 2025. Under §20-871(d)(2), retraining on new data is a substantial modification requiring a new bias audit. No new audit was conducted. The January 2026 and March 2026 hiring rounds used a non-compliant AEDT.

- **Rule ref:** R15
- **Fact refs:** F8, F9
- **Issue ref:** I6
- **Result:** violated

### A14

For the late April 2026 round, the April 8, 2025 audit is both invalidated by the December 2025 retraining and expired on its own terms (more than one year old). Double non-compliance.

- **Rule ref:** R14
- **Fact refs:** F8, F9
- **Issue ref:** I6
- **Result:** violated

### A15

Northwind's careers page does not include HireSignal's distribution date as required by DCWP Rules §5-303(a)(2). Publication is insufficient.

- **Rule ref:** R17
- **Fact refs:** F10
- **Issue ref:** I6
- **Result:** violated

### A16

Dalloway Audit has no ties to Northwind or Praxis and no role in building HireSignal. The auditor independence requirement is satisfied.

- **Rule ref:** R16
- **Fact refs:** F8
- **Issue ref:** I6
- **Result:** satisfied

### A17

Notice is provided 10 business days before screening, names the tool, lists qualifications, and explains alternative process. Substantially compliant but unclear whether notice states employer will consider other information beyond AEDT output per §20-872(a)(2).

- **Rule ref:** R18
- **Fact refs:** F10
- **Issue ref:** I6
- **Result:** partial

### A18

Each candidate screened by non-compliant AEDT in January and March 2026 rounds is a potential separate violation at $500-$1,500 each. Significant cumulative exposure.

- **Rule ref:** R19
- **Fact refs:** F9
- **Issue ref:** I7
- **Result:** violated

### A19

Post-June 30, 2026, each loan decision made by known-discriminatory UnderwriteOne without compliance infrastructure is a potential deceptive trade practice violation at up to $20,000 each.

- **Rule ref:** R11
- **Fact refs:** F4, F5, F6
- **Issue ref:** I7
- **Result:** violated

### A20

TRAIGA requires intentional discrimination. The age discrimination in UnderwriteOne was unintentional (caused by a proxy feature, discovered through internal testing). No TRAIGA violation.

- **Rule ref:** R21
- **Fact refs:** F4
- **Issue ref:** I7
- **Result:** satisfied

### A21

HireSignal ranks applicants and only the top quarter are interviewed, meaning the ranking is the determinative factor. This meets the AEDT definition under §20-870 and DCWP Rules §5-300(i) as relying solely on simplified output.

- **Rule ref:** R13
- **Fact refs:** F7
- **Issue ref:** I6
- **Result:** satisfied

### A22

NYC LL 144 applies based on candidate location. Brooklyn office roles and remote roles with NYC-resident applicants are covered under §20-874.

- **Rule ref:** R20
- **Fact refs:** F1, F7
- **Issue ref:** I6
- **Result:** satisfied

## Conclusions (5)

### C1

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A1, A2, A3, A4, A5, A6, A7, A8

### C2

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A9, A10, A11, A12

### C3

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A13, A14, A15, A18

### C4

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A20

### C5

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A19

## Obligations (15)

### O1

Obtain new bias audit of retrained HireSignal before any further use; suspend late April 2026 hiring round until complete

- **Required by:** R15
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Before next use of HireSignal

### O2

Add HireSignal distribution date to careers page published results

- **Required by:** R17
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Immediately

### O3

Verify candidate notice includes statement that employer considers other information beyond AEDT output

- **Required by:** R18
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Immediately

### O4

Accelerate corrected UnderwriteOne model release to before June 30, 2026 or as close as possible

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O5

Implement AI risk management program consistent with NIST AI RMF 100-1 or ISO/IEC 42001

- **Required by:** R8
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O6

Prepare developer documentation on limitations, training data, intended uses, monitoring guidance

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O7

Publish public use case inventory and deployer website statement about high-risk AI systems

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O8

Implement pre-decision consumer notice for loan applicants about AI system use

- **Required by:** R8
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O9

Implement data correction and meaningful appeal mechanisms for loan applicants

- **Required by:** R8
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O10

Complete impact assessment for UnderwriteOne

- **Required by:** R26
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-09-28

### O11

Notify Colorado AG and affected consumers of algorithmic discrimination discovery

- **Required by:** R10
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-09-28

### O12

Conduct annual reviews of UnderwriteOne for algorithmic discrimination

- **Required by:** R8
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** Annually after 2026-06-30

### O13

Update impact assessment annually and within 90 days of any substantial modification

- **Required by:** R8
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** Annually

### O14

Ensure annual bias audits of HireSignal and new audits after any retraining

- **Required by:** R14
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Annually and after each retraining

### O15

Pursue cure safe harbor: fix discriminatory model and notify CO AG within 60 days of June 30, 2026

- **Required by:** R25
- **Status:** safe-harbor
- **Jurisdiction:** Colorado
- **Deadline:** 2026-08-29

## Graph connections (65)

### E1

- **Src:** F2
- **Dst:** I1
- **Type:** triggers
- **Justification:** Northwind building its own AI system raises the developer vs deployer classification question

### E2

- **Src:** F15
- **Dst:** I1
- **Type:** triggers
- **Justification:** Trade blog claim that dual role only requires deployer compliance raises the issue

### E3

- **Src:** R1
- **Dst:** A1
- **Type:** applies-to
- **Justification:** Developer definition applied to Northwind's development of UnderwriteOne

### E4

- **Src:** R2
- **Dst:** A2
- **Type:** applies-to
- **Justification:** Deployer definition applied to Northwind's deployment of UnderwriteOne

### E5

- **Src:** A1
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** Northwind is a developer, triggering developer obligations

### E6

- **Src:** A2
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** Northwind is also a deployer, triggering deployer obligations

### E7

- **Src:** F3
- **Dst:** I2
- **Type:** triggers
- **Justification:** Two decision pathways raise question of high-risk classification for each

### E8

- **Src:** R4
- **Dst:** A3
- **Type:** applies-to
- **Justification:** Consequential decision definition applied to lending decisions

### E9

- **Src:** R3
- **Dst:** A4
- **Type:** applies-to
- **Justification:** High-risk definition applied to automated sub-$10K loans

### E10

- **Src:** R5
- **Dst:** A5
- **Type:** applies-to
- **Justification:** Substantial factor definition applied to underwriter-reviewed loans

### E11

- **Src:** A3
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** Lending decisions are consequential decisions

### E12

- **Src:** A4
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** Automated loans involve high-risk AI system

### E13

- **Src:** A5
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** Underwriter-reviewed loans also involve high-risk AI system

### E14

- **Src:** F6
- **Dst:** I3
- **Type:** triggers
- **Justification:** Absence of compliance infrastructure raises obligation question

### E15

- **Src:** R8
- **Dst:** A7
- **Type:** applies-to
- **Justification:** Deployer obligations applied to Northwind's non-compliance

### E16

- **Src:** R7
- **Dst:** A8
- **Type:** applies-to
- **Justification:** Developer obligations applied to Northwind's non-compliance

### E17

- **Src:** R9
- **Dst:** A6
- **Type:** applies-to
- **Justification:** Small deployer exception tested against Northwind's size and data use

### E18

- **Src:** A6
- **Dst:** C1
- **Type:** fails-element
- **Justification:** Exception unavailable; both conditions fail

### E19

- **Src:** A7
- **Dst:** C1
- **Type:** fails-element
- **Justification:** All deployer obligations unmet

### E20

- **Src:** A8
- **Dst:** C1
- **Type:** fails-element
- **Justification:** All developer obligations unmet

### E21

- **Src:** F4
- **Dst:** I4
- **Type:** triggers
- **Justification:** March 2026 discovery raises algorithmic discrimination question

### E22

- **Src:** R6
- **Dst:** A9
- **Type:** applies-to
- **Justification:** Algorithmic discrimination definition applied to age-based disparate impact

### E23

- **Src:** A9
- **Dst:** C2
- **Type:** satisfies-element
- **Justification:** Age-based disparate impact in lending constitutes algorithmic discrimination

### E24

- **Src:** R10
- **Dst:** A10
- **Type:** applies-to
- **Justification:** Notification obligation applied to Northwind's discovery

### E25

- **Src:** A10
- **Dst:** C2
- **Type:** fails-element
- **Justification:** No notification made to AG or affected consumers

### E26

- **Src:** F13
- **Dst:** I4
- **Type:** supports
- **Justification:** Outside counsel correctly identifies breach of reasonable care

### E27

- **Src:** F14
- **Dst:** I4
- **Type:** contradicts
- **Justification:** CFO view is legally incorrect; pre-effective-date discovery does not exempt post-effective-date obligations

### E28

- **Src:** F15
- **Dst:** I1
- **Type:** contradicts
- **Justification:** Trade blog incorrectly states only deployer section applies

### E29

- **Src:** R12
- **Dst:** A11
- **Type:** applies-to
- **Justification:** Rebuttable presumption tested against Northwind's compliance status

### E30

- **Src:** A11
- **Dst:** C2
- **Type:** fails-element
- **Justification:** Presumption unavailable due to non-compliance with both sections

### E31

- **Src:** R25
- **Dst:** A12
- **Type:** applies-to
- **Justification:** Cure safe harbor tested against Northwind's actions

### E32

- **Src:** A12
- **Dst:** C2
- **Type:** satisfies-element
- **Justification:** Safe harbor partially available if Northwind acts within 60 days of effective date

### E33

- **Src:** F8
- **Dst:** I6
- **Type:** triggers
- **Justification:** December 2025 retraining raises audit validity question

### E34

- **Src:** R15
- **Dst:** A13
- **Type:** applies-to
- **Justification:** Substantial modification rule applied to December 2025 retraining

### E35

- **Src:** A13
- **Dst:** C3
- **Type:** fails-element
- **Justification:** No new audit after retraining; January and March 2026 rounds non-compliant

### E36

- **Src:** R14
- **Dst:** A14
- **Type:** applies-to
- **Justification:** One-year expiration rule applied to April 2026 round

### E37

- **Src:** A14
- **Dst:** C3
- **Type:** fails-element
- **Justification:** Audit both invalidated by retraining and expired for April 2026 round

### E38

- **Src:** R17
- **Dst:** A15
- **Type:** applies-to
- **Justification:** Publication requirements applied to missing distribution date

### E39

- **Src:** A15
- **Dst:** C3
- **Type:** fails-element
- **Justification:** Missing distribution date renders publication non-compliant

### E40

- **Src:** R16
- **Dst:** A16
- **Type:** applies-to
- **Justification:** Auditor independence tested for Dalloway Audit

### E41

- **Src:** A16
- **Dst:** C3
- **Type:** satisfies-element
- **Justification:** Dalloway Audit meets independence requirements

### E42

- **Src:** R19
- **Dst:** A18
- **Type:** applies-to
- **Justification:** Penalty calculation applied to non-compliant AEDT use

### E43

- **Src:** A18
- **Dst:** C3
- **Type:** fails-element
- **Justification:** Per-candidate penalties for non-compliant screening rounds

### E44

- **Src:** R11
- **Dst:** A19
- **Type:** applies-to
- **Justification:** Colorado enforcement provisions applied to post-effective-date violations

### E45

- **Src:** A19
- **Dst:** C5
- **Type:** fails-element
- **Justification:** Significant per-violation penalty exposure for continued discriminatory use

### E46

- **Src:** R21
- **Dst:** A20
- **Type:** applies-to
- **Justification:** TRAIGA intent requirement applied to unintentional age discrimination

### E47

- **Src:** A20
- **Dst:** C4
- **Type:** satisfies-element
- **Justification:** No intentional discrimination; TRAIGA not violated

### E48

- **Src:** R13
- **Dst:** A21
- **Type:** applies-to
- **Justification:** AEDT definition applied to HireSignal ranking system

### E49

- **Src:** A21
- **Dst:** C3
- **Type:** satisfies-element
- **Justification:** HireSignal meets AEDT definition

### E50

- **Src:** R20
- **Dst:** A22
- **Type:** applies-to
- **Justification:** Geographic scope applied to Brooklyn and remote NYC-resident applicants

### E51

- **Src:** A22
- **Dst:** C3
- **Type:** satisfies-element
- **Justification:** NYC LL 144 applies to Northwind's hiring of NYC residents

### E52

- **Src:** R8
- **Dst:** O5
- **Type:** triggers
- **Justification:** Deployer obligation triggers risk management program requirement

### E53

- **Src:** R7
- **Dst:** O6
- **Type:** triggers
- **Justification:** Developer obligation triggers documentation requirement

### E54

- **Src:** R7
- **Dst:** O7
- **Type:** triggers
- **Justification:** Developer and deployer obligations trigger public disclosure requirement

### E55

- **Src:** R8
- **Dst:** O8
- **Type:** triggers
- **Justification:** Deployer obligation triggers consumer notice requirement

### E56

- **Src:** R8
- **Dst:** O9
- **Type:** triggers
- **Justification:** Deployer obligation triggers data correction and appeal requirement

### E57

- **Src:** R26
- **Dst:** O10
- **Type:** triggers
- **Justification:** Pre-effective-date deployment triggers 90-day impact assessment deadline

### E58

- **Src:** R10
- **Dst:** O11
- **Type:** triggers
- **Justification:** Discovery of algorithmic discrimination triggers AG and consumer notification

### E59

- **Src:** R15
- **Dst:** O1
- **Type:** triggers
- **Justification:** Retraining triggers new bias audit requirement before further use

### E60

- **Src:** R17
- **Dst:** O2
- **Type:** triggers
- **Justification:** Publication requirement triggers distribution date addition

### E61

- **Src:** R18
- **Dst:** O3
- **Type:** triggers
- **Justification:** Notice requirement triggers verification of completeness

### E62

- **Src:** R25
- **Dst:** O15
- **Type:** triggers
- **Justification:** Cure safe harbor triggers accelerated fix and AG notification

### E63

- **Src:** R8
- **Dst:** O12
- **Type:** triggers
- **Justification:** Deployer obligation triggers annual discrimination review

### E64

- **Src:** R8
- **Dst:** O13
- **Type:** triggers
- **Justification:** Deployer obligation triggers annual and post-modification impact assessment updates

### E65

- **Src:** R14
- **Dst:** O14
- **Type:** triggers
- **Justification:** Annual audit requirement triggers ongoing HireSignal audit obligation
