# M2 — TenantRank Boulder — teacher FIRACO reasoning

Unverified model output for legal review. Citations, facts, applications, and obligations may be incorrect. Text and node IDs below are preserved from the saved reference graph.

[Read case](../../../data/cases/M2_tenantrank_boulder.md) · [Review brief](../../PROF_PHILIPP_REVIEW.md)

Teacher: claude-opus-4-6. Source: data/outputs/graphs/M2_reference.json.

Source SHA-256: `02cbd6e6d424d0fde5fddbedf6b718c61473dab5e0b628e0d8c91556822940a5`.

## Facts (18)

### F1

GreenRidge is a Boulder-based property management company doing business in Colorado

- **Polarity:** present
- **Support quote:** GreenRidge Properties is a Boulder-based residential property management company

### F2

GreenRidge has 45 full-time employees (fewer than 50)

- **Polarity:** present
- **Support quote:** with 45 full-time employees

### F3

TenantRank is an ML-based housing applicant screening tool generating risk scores 0-100

- **Polarity:** present
- **Support quote:** TenantRank, a machine-learning-based housing applicant screening tool that scores prospective tenants

### F4

TenantRank was developed entirely in-house by GreenRidge's data science team

- **Polarity:** present
- **Support quote:** developed entirely in-house by GreenRidge's two-person data science team

### F5

TenantRank was trained on five years of GreenRidge's own tenant data

- **Polarity:** present
- **Support quote:** using five years of GreenRidge's own tenant payment history, lease violation records, and eviction data

### F6

TenantRank is used to screen prospective tenants for rental housing

- **Polarity:** present
- **Support quote:** scores prospective tenants on predicted tenancy risk

### F7

VP email directs near-automatic denial for scores below 40

- **Polarity:** present
- **Support quote:** If TenantRank scores an applicant below 40, we should almost never approve them

### F8

96% of applicants below 40 denied; 88% above 60 approved regardless of other factors

- **Polarity:** present
- **Support quote:** 96% of applicants with scores below 40 were denied, while 88% of applicants with scores above 60 were approved

### F9

Risk management program modeled on NIST AI RMF 1.0 implemented January 2026

- **Polarity:** present
- **Support quote:** Implemented a risk management program in January 2026 modeled on the NIST AI Risk Management Framework 1.0

### F10

Initial impact assessment completed January 2026

- **Polarity:** present
- **Support quote:** Completed an initial impact assessment in January 2026

### F11

Applicant disclosure says only 'data analytics tools' without mentioning AI

- **Polarity:** present
- **Support quote:** GreenRidge Properties uses data analytics tools to assist in evaluating rental applications

### F12

Outside counsel advised small-deployer exception applies based on employee count alone

- **Polarity:** present
- **Support quote:** the company qualifies for the small-deployer exception because it has fewer than 50 employees

### F13

TenantRank deployed in February 2026, before CO AIA effective date of June 30, 2026

- **Polarity:** present
- **Support quote:** In February 2026, GreenRidge began using TenantRank

### F14

VP of Operations serves as AI risk officer

- **Polarity:** present
- **Support quote:** an assigned AI risk officer (the VP of Operations)

### F15

No consumer data correction or appeal process mentioned

- **Polarity:** absent
- **Support quote:** Not specified

### F16

No public website statement about high-risk AI systems mentioned

- **Polarity:** absent
- **Support quote:** Not specified

### F17

No developer documentation on limitations, training data biases, or inappropriate uses mentioned

- **Polarity:** absent
- **Support quote:** Not specified

### F18

No bias testing or algorithmic discrimination analysis of TenantRank mentioned

- **Polarity:** absent
- **Support quote:** Not specified

## Issues (5)

### I1

Whether TenantRank is a high-risk AI system under CO AIA Section 6-1-1701(7)

- **Status:** dispositive

### I2

Whether the small-deployer exception under Section 6-1-1703(6) applies to GreenRidge

- **Status:** dispositive

### I3

Whether GreenRidge is both developer and deployer under CO AIA

- **Status:** dispositive

### I4

Whether current compliance measures satisfy CO AIA obligations

- **Status:** dispositive

### I5

What additional obligations apply to GreenRidge by June 30, 2026

- **Status:** collateral

## Rules (16)

### R1

Definition of artificial intelligence system

- **Citation:** CO AIA Section 6-1-1701(2)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R2

Housing as a consequential decision domain

- **Citation:** CO AIA Section 6-1-1701(3)(f)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R3

Definition of high-risk AI system

- **Citation:** CO AIA Section 6-1-1701(7)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R4

Substantial factor definition - human review does not negate if based primarily on AI output

- **Citation:** CO AIA Section 6-1-1701(9)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R5

Definition of developer

- **Citation:** CO AIA Section 6-1-1701(6)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R6

Definition of deployer

- **Citation:** CO AIA Section 6-1-1701(5)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R7

Developer obligations including reasonable care, documentation, and public statement

- **Citation:** CO AIA Section 6-1-1702
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R8

Deployer obligations including risk management, impact assessment, notice, correction, and appeal

- **Citation:** CO AIA Section 6-1-1703(2)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R9

Small-deployer exception requires BOTH fewer than 50 employees AND not using own data to train

- **Citation:** CO AIA Section 6-1-1703(6)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R10

Impact assessment must include six enumerated elements

- **Citation:** CO AIA Section 6-1-1701(8)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R11

Consumer notice must include five specific items before consequential decision

- **Citation:** CO AIA Section 6-1-1703(2)(e)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R12

Consumer rights to data correction and meaningful appeal

- **Citation:** CO AIA Section 6-1-1703(2)(f)-(g)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R13

90-day notification to AG and consumers upon discovery of algorithmic discrimination

- **Citation:** CO AIA Section 6-1-1704
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R14

Enforcement as deceptive trade practice, up to $20,000 per violation, AG exclusive authority

- **Citation:** CO AIA Section 6-1-1706
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R15

Pre-deployment systems have 90 days after effective date for impact assessment

- **Citation:** CO AIA Section 6-1-1703(2)(b)(I)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R16

Risk management program must be consistent with NIST AI RMF 1.0 or equivalent

- **Citation:** CO AIA Section 6-1-1703(2)(a)(III)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

## Applications (14)

### A1

TenantRank is a machine-based system that processes inputs and produces outputs (risk scores 0-100) that are predictions influencing real environments. It satisfies the AI system definition.

- **Rule ref:** R1
- **Fact refs:** F3
- **Issue ref:** I1
- **Result:** satisfied

### A2

TenantRank screens prospective tenants for rental housing. Housing is explicitly enumerated in Section 6-1-1701(3)(f) as a consequential decision domain.

- **Rule ref:** R2
- **Fact refs:** F6
- **Issue ref:** I1
- **Result:** satisfied

### A3

96% denial rate for sub-40 scores and 88% approval for above-60 scores, combined with VP directive to almost never approve low scorers, demonstrates TenantRank materially contributes to decisions. Human review is based primarily on AI output per Section 6-1-1701(9).

- **Rule ref:** R4
- **Fact refs:** F7, F8
- **Issue ref:** I1
- **Result:** satisfied

### A4

TenantRank is an AI system that is a substantial factor in making consequential housing decisions. No exceptions in Section 6-1-1701(7)(a)-(d) apply - it does not perform narrow procedural tasks, improve prior human activity, merely detect patterns, or perform preparatory tasks. TenantRank is a high-risk AI system.

- **Rule ref:** R3
- **Fact refs:** F3, F6, F7, F8
- **Issue ref:** I1
- **Result:** satisfied

### A5

Section 6-1-1703(6) requires BOTH (a) fewer than 50 employees AND (b) not using own data to train. GreenRidge satisfies (a) with 45 employees but fails (b) because it trained TenantRank on its own five years of tenant data. Both conditions must be met. The exception does not apply.

- **Rule ref:** R9
- **Fact refs:** F2, F5
- **Issue ref:** I2
- **Result:** violated

### A6

GreenRidge does business in Colorado and developed TenantRank in-house for use as a high-risk AI system. It meets the developer definition under Section 6-1-1701(6).

- **Rule ref:** R5
- **Fact refs:** F1, F4
- **Issue ref:** I3
- **Result:** satisfied

### A7

GreenRidge does business in Colorado and deploys TenantRank, a high-risk AI system, in its property management operations. It meets the deployer definition under Section 6-1-1701(5).

- **Rule ref:** R6
- **Fact refs:** F1, F6
- **Issue ref:** I3
- **Result:** satisfied

### A8

GreenRidge aligned its risk management program with NIST AI RMF 1.0, satisfying the framework requirement of Section 6-1-1703(2)(a)(III). However, the VP of Operations who directed heavy reliance on TenantRank scores also serves as AI risk officer, creating a governance conflict. The program has not identified or addressed the de facto determinative weight given to scores, undermining substantive adequacy under Section 6-1-1703(2)(a)(I).

- **Rule ref:** R16
- **Fact refs:** F9, F14, F7
- **Issue ref:** I4
- **Result:** partial

### A9

An impact assessment was completed in January 2026 covering purpose, data inputs, discrimination risks, and mitigation. However, the facts do not confirm all six elements of Section 6-1-1701(8) are addressed, particularly known limitations analysis, output description, and oversight processes. Under Section 6-1-1703(2)(b)(I), pre-deployment systems have until September 28, 2026 to complete a compliant assessment.

- **Rule ref:** R10
- **Fact refs:** F10
- **Issue ref:** I4
- **Result:** partial

### A10

The disclosure says only 'data analytics tools' without identifying it as a high-risk AI system, stating the purpose and nature of the consequential decision, providing contact information, giving a plain-language description, or directing consumers to a public statement. It fails all five required elements of Section 6-1-1703(2)(e).

- **Rule ref:** R11
- **Fact refs:** F11
- **Issue ref:** I4
- **Result:** violated

### A11

No data correction process or meaningful appeal mechanism has been implemented for housing applicants. Section 6-1-1703(2)(f) and (g) require both. These are absent.

- **Rule ref:** R12
- **Fact refs:** F15
- **Issue ref:** I4
- **Result:** violated

### A12

As developer, GreenRidge has not created documentation on limitations, training data biases, intended/inappropriate uses, or monitoring guidance per Section 6-1-1702(2). No public statement summarizing high-risk AI systems developed has been published per Section 6-1-1702(3). No bias testing has been conducted per Section 6-1-1702(1) reasonable care obligation.

- **Rule ref:** R7
- **Fact refs:** F17, F16, F18
- **Issue ref:** I4
- **Result:** violated

### A13

GreenRidge has not published a website statement summarizing deployed high-risk AI systems and algorithmic discrimination risk management as required by Section 6-1-1703(2)(d).

- **Rule ref:** R8
- **Fact refs:** F16
- **Issue ref:** I4
- **Result:** violated

### A14

If TenantRank produces disparate outcomes on protected characteristics, each non-compliant application decision could constitute a separate violation at up to $20,000 per violation under Section 6-1-1706. With 1,200 rental units, exposure is significant. Actual discrimination outcomes require further factual investigation.

- **Rule ref:** R14
- **Fact refs:** F8, F7
- **Issue ref:** I5
- **Result:** requires-fact

## Conclusions (5)

### C1

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A4

### C2

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A5

### C3

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A6, A7

### C4

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A8, A9, A10, A11, A12, A13

### C5

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A10, A11, A12, A13, A14

## Obligations (12)

### O1

Conduct bias testing of TenantRank across protected classes and implement reasonable care measures as developer

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O2

Create developer documentation on limitations, training data biases, intended/inappropriate uses, and monitoring guidance

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O3

Publish developer public statement on website summarizing TenantRank as high-risk AI system

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O4

Enhance risk management program to address de facto determinative reliance on TenantRank scores and resolve governance conflict with VP of Operations dual role

- **Required by:** R16
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O5

Complete or update impact assessment to include all six elements of Section 6-1-1701(8)

- **Required by:** R15
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-09-28

### O6

Implement annual review process for TenantRank to assess algorithmic discrimination

- **Required by:** R8
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2027-06-30

### O7

Publish deployer public website statement summarizing deployed high-risk AI systems and discrimination risk management

- **Required by:** R8
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O8

Revise consumer notice to include all five elements: high-risk AI disclosure, purpose/nature of decision, contact info, plain-language description, and link to public statement

- **Required by:** R11
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O9

Implement process for applicants to correct incorrect personal data processed by TenantRank

- **Required by:** R12
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O10

Implement meaningful appeal process for consequential housing decisions involving TenantRank

- **Required by:** R12
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O11

If algorithmic discrimination discovered, notify AG and affected consumers within 90 days

- **Required by:** R13
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** Not specified

### O12

Obtain corrected legal advice regarding inapplicability of small-deployer exception and full dual developer/deployer obligations

- **Required by:** R9
- **Status:** recommended
- **Jurisdiction:** Colorado
- **Deadline:** Not specified

## Graph connections (50)

### E1

- **Src:** F3
- **Dst:** I1
- **Type:** triggers
- **Justification:** ML-based scoring tool raises question of high-risk AI classification

### E2

- **Src:** F6
- **Dst:** I1
- **Type:** triggers
- **Justification:** Housing screening implicates consequential decision domain

### E3

- **Src:** F7
- **Dst:** I1
- **Type:** supports
- **Justification:** VP directive shows TenantRank is substantial factor in decisions

### E4

- **Src:** F8
- **Dst:** I1
- **Type:** supports
- **Justification:** Empirical data confirms near-determinative reliance on scores

### E5

- **Src:** R1
- **Dst:** A1
- **Type:** applies-to
- **Justification:** AI system definition applied to TenantRank

### E6

- **Src:** R2
- **Dst:** A2
- **Type:** applies-to
- **Justification:** Housing consequential decision rule applied to tenant screening

### E7

- **Src:** R4
- **Dst:** A3
- **Type:** applies-to
- **Justification:** Substantial factor definition applied to TenantRank usage patterns

### E8

- **Src:** R3
- **Dst:** A4
- **Type:** applies-to
- **Justification:** High-risk AI definition applied to TenantRank

### E9

- **Src:** A1
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** TenantRank meets AI system definition

### E10

- **Src:** A2
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** Housing screening is a consequential decision

### E11

- **Src:** A3
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** TenantRank is a substantial factor

### E12

- **Src:** A4
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** No exceptions apply; TenantRank is high-risk

### E13

- **Src:** F2
- **Dst:** I2
- **Type:** triggers
- **Justification:** Employee count raises small-deployer exception question

### E14

- **Src:** F5
- **Dst:** I2
- **Type:** triggers
- **Justification:** Use of own training data is critical to exception analysis

### E15

- **Src:** R9
- **Dst:** A5
- **Type:** applies-to
- **Justification:** Small-deployer exception applied to GreenRidge facts

### E16

- **Src:** A5
- **Dst:** C2
- **Type:** fails-element
- **Justification:** Exception fails because GreenRidge uses own data to train TenantRank

### E17

- **Src:** F12
- **Dst:** I2
- **Type:** contradicts
- **Justification:** Outside counsel advice incorrectly analyzed only employee count prong

### E18

- **Src:** F4
- **Dst:** I3
- **Type:** triggers
- **Justification:** In-house development raises dual developer/deployer status question

### E19

- **Src:** R5
- **Dst:** A6
- **Type:** applies-to
- **Justification:** Developer definition applied to GreenRidge

### E20

- **Src:** R6
- **Dst:** A7
- **Type:** applies-to
- **Justification:** Deployer definition applied to GreenRidge

### E21

- **Src:** A6
- **Dst:** C3
- **Type:** satisfies-element
- **Justification:** GreenRidge meets developer definition

### E22

- **Src:** A7
- **Dst:** C3
- **Type:** satisfies-element
- **Justification:** GreenRidge meets deployer definition

### E23

- **Src:** F9
- **Dst:** I4
- **Type:** triggers
- **Justification:** Existing risk management program requires adequacy assessment

### E24

- **Src:** F11
- **Dst:** I4
- **Type:** triggers
- **Justification:** Vague disclosure requires compliance assessment

### E25

- **Src:** R16
- **Dst:** A8
- **Type:** applies-to
- **Justification:** NIST AI RMF alignment requirement applied to risk management program

### E26

- **Src:** R10
- **Dst:** A9
- **Type:** applies-to
- **Justification:** Impact assessment requirements applied to existing assessment

### E27

- **Src:** R11
- **Dst:** A10
- **Type:** applies-to
- **Justification:** Consumer notice requirements applied to current disclosure

### E28

- **Src:** R12
- **Dst:** A11
- **Type:** applies-to
- **Justification:** Consumer rights requirements applied to absent processes

### E29

- **Src:** R7
- **Dst:** A12
- **Type:** applies-to
- **Justification:** Developer obligations applied to GreenRidge as developer

### E30

- **Src:** R8
- **Dst:** A13
- **Type:** applies-to
- **Justification:** Deployer public statement obligation applied

### E31

- **Src:** A8
- **Dst:** C4
- **Type:** fails-element
- **Justification:** Risk management program substantively inadequate despite correct framework

### E32

- **Src:** A10
- **Dst:** C4
- **Type:** fails-element
- **Justification:** Consumer notice fails all five required elements

### E33

- **Src:** A11
- **Dst:** C4
- **Type:** fails-element
- **Justification:** No data correction or appeal processes exist

### E34

- **Src:** A12
- **Dst:** C4
- **Type:** fails-element
- **Justification:** Developer obligations largely unaddressed

### E35

- **Src:** A13
- **Dst:** C4
- **Type:** fails-element
- **Justification:** No deployer public website statement published

### E36

- **Src:** R14
- **Dst:** A14
- **Type:** applies-to
- **Justification:** Enforcement provisions applied to assess exposure

### E37

- **Src:** A14
- **Dst:** C5
- **Type:** fails-element
- **Justification:** Multiple compliance gaps create significant enforcement exposure

### E38

- **Src:** R7
- **Dst:** O1
- **Type:** triggers
- **Justification:** Developer reasonable care obligation requires bias testing

### E39

- **Src:** R7
- **Dst:** O2
- **Type:** triggers
- **Justification:** Developer documentation obligation

### E40

- **Src:** R7
- **Dst:** O3
- **Type:** triggers
- **Justification:** Developer public statement obligation

### E41

- **Src:** R16
- **Dst:** O4
- **Type:** triggers
- **Justification:** Risk management program enhancement needed

### E42

- **Src:** R15
- **Dst:** O5
- **Type:** triggers
- **Justification:** Impact assessment completion deadline for pre-deployment systems

### E43

- **Src:** R8
- **Dst:** O6
- **Type:** triggers
- **Justification:** Annual review obligation

### E44

- **Src:** R8
- **Dst:** O7
- **Type:** triggers
- **Justification:** Deployer public website statement obligation

### E45

- **Src:** R11
- **Dst:** O8
- **Type:** triggers
- **Justification:** Consumer notice must be revised to meet all five elements

### E46

- **Src:** R12
- **Dst:** O9
- **Type:** triggers
- **Justification:** Data correction right must be implemented

### E47

- **Src:** R12
- **Dst:** O10
- **Type:** triggers
- **Justification:** Appeal process must be implemented

### E48

- **Src:** R13
- **Dst:** O11
- **Type:** triggers
- **Justification:** Ongoing algorithmic discrimination notification obligation

### E49

- **Src:** R9
- **Dst:** O12
- **Type:** triggers
- **Justification:** Incorrect legal advice must be corrected

### E50

- **Src:** A9
- **Dst:** C4
- **Type:** fails-element
- **Justification:** Impact assessment completeness uncertain against six statutory elements
