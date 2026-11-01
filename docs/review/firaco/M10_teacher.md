# M10 — TalentSieve and Texas Intent — teacher FIRACO reasoning

Unverified model output for legal review. Citations, facts, applications, and obligations may be incorrect. Text and node IDs below are preserved from the saved reference graph.

[Read case](../../../data/cases/M10_talentsieve_hospital_tx.md) · [Review brief](../../PROF_PHILIPP_REVIEW.md)

Teacher: claude-opus-4-6. Source: data/outputs/graphs/M10_reference.json.

Source SHA-256: `b1f1c193637e9b1ac01e116d290530c60207b96398df125cff6b309cfce12f8e`.

## Facts (14)

### F1

Gulfstream Regional Medical is a private hospital system in Houston, TX with 6,000 employees

- **Polarity:** present
- **Support quote:** Gulfstream Regional Medical is a private hospital system in Houston, Texas, with 6,000 employees

### F2

Gulfstream uses TalentSieve, an AI resume-screening tool licensed from Pecos Analytics

- **Polarity:** present
- **Support quote:** Gulfstream uses TalentSieve, a resume-screening tool licensed from Pecos Analytics

### F3

TalentSieve advances women at 0.71 times the rate of men per 2025 internal analysis

- **Polarity:** present
- **Support quote:** TalentSieve advances women at 0.71 times the rate of men

### F4

No evidence of discriminatory intent in TalentSieve design or Gulfstream records for gender disparity

- **Polarity:** present
- **Support quote:** Nothing in the tool's design documents or in Gulfstream's records suggests that anyone intended that result

### F5

Hiring manager configured TalentSieve to exclude pre-1995 graduation years with stated intent to screen out over-50s

- **Polarity:** present
- **Support quote:** I want a young team -- screen out the over-50s

### F6

Gulfstream does not tell job applicants that an AI tool screens their applications

- **Polarity:** present
- **Support quote:** Gulfstream does not tell job applicants that an AI tool screens their applications

### F7

City of Houston adopted 2024 ordinance requiring annual bias audit of AI hiring tools and sent demand in Feb 2026

- **Polarity:** present
- **Support quote:** the City of Houston adopted an ordinance requiring employers in the city to obtain an annual bias audit of any AI hiring tool

### F8

Gulfstream uses DischargePredict AI system for patient discharge timing

- **Polarity:** present
- **Support quote:** Gulfstream uses DischargePredict, an AI system that helps plan the timing of each patient's discharge

### F9

Every patient is told in writing on admission form on day care begins that DischargePredict is used

- **Polarity:** present
- **Support quote:** Every patient is told that the system is being used, in writing, on the admission form signed on the day care begins

### F10

Gulfstream has maintained NIST AI RMF-based governance program since 2025

- **Polarity:** present
- **Support quote:** Gulfstream has maintained a documented AI governance program built on the NIST AI Risk Management Framework

### F11

Gulfstream discovered the age filter through internal review in March 2026 and removed it same week

- **Polarity:** present
- **Support quote:** It found the hiring manager's filter itself, during an internal review in March 2026, and removed it the same week

### F12

Gulfstream did not notify the Texas Attorney General of the discovery or cure

- **Polarity:** present
- **Support quote:** It did not notify the Attorney General

### F13

Texas AG sent written notice of alleged violation on March 30, 2026

- **Polarity:** present
- **Support quote:** On March 30, 2026, the Texas Attorney General sent Gulfstream a written notice of an alleged violation concerning the filter

### F14

No indication Gulfstream screens NYC-resident candidates or operates in Colorado

- **Polarity:** present
- **Support quote:** Not specified

## Issues (6)

### I1

Does TalentSieve's 0.71 gender impact ratio violate TRAIGA absent discriminatory intent?

- **Status:** dispositive

### I2

Does the hiring manager's intentional age-based filter violate TRAIGA Section 551.051(a)?

- **Status:** dispositive

### I3

Can the Houston AI hiring audit ordinance be enforced against Gulfstream given TRAIGA preemption?

- **Status:** dispositive

### I4

Does Gulfstream owe any AI disclosure to job applicants under applicable law?

- **Status:** dispositive

### I5

Does Gulfstream's patient disclosure for DischargePredict satisfy TRAIGA Section 551.102?

- **Status:** dispositive

### I6

Who enforces TRAIGA, what are penalties, and are safe harbors available on these facts?

- **Status:** dispositive

## Rules (11)

### R1

Prohibition on deploying AI with intent to unlawfully discriminate against protected class

- **Citation:** TRAIGA §551.051(a)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R2

Express preemption of all local ordinances regulating AI systems in Texas

- **Citation:** TRAIGA §551.201
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R3

AI disclosure obligation applies only to governmental entities, not private employers

- **Citation:** TRAIGA §551.101
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R4

Healthcare provider must disclose AI use to patient on date treatment or service is provided

- **Citation:** TRAIGA §551.102
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R5

Only TX AG may enforce TRAIGA; no private right of action; penalties $10,000-$200,000 per violation with daily accrual

- **Citation:** TRAIGA §551.301(a)-(b)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R6

Internal discovery safe harbor requires: (1) internal discovery, (2) reasonable cure steps, (3) AG notification

- **Citation:** TRAIGA §551.301(c)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R7

Substantial compliance with NIST AI RMF provides safe harbor against TRAIGA violations

- **Citation:** TRAIGA §551.301(d)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R8

AG must provide written notice and allow 60 days to cure before initiating enforcement

- **Citation:** TRAIGA §551.301(e)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R9

TRAIGA does not require private employers to disclose AI use to job applicants or employees

- **Citation:** TRAIGA §551.001(2) and Key Compliance Notes
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R10

LL 144 applies based on candidate location in NYC; not applicable to Houston-only operations

- **Citation:** NYC LL 144 §20-871 and §20-874
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R11

Colorado AIA deployer obligations apply to persons doing business in Colorado; effective June 30, 2026

- **Citation:** Colorado AIA §6-1-1703
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

## Applications (9)

### A1

TRAIGA §551.051(a) requires intent to unlawfully discriminate. TalentSieve produces a 0.71 gender impact ratio, but F4 establishes no evidence of discriminatory intent exists. Disparate impact alone does not violate TRAIGA. All elements except intent are met; the intent element fails, so the prohibition is not violated and Gulfstream is compliant on this issue.

- **Rule ref:** R1
- **Fact refs:** F2, F3, F4
- **Issue ref:** I1
- **Result:** satisfied

### A2

The hiring manager's email stating 'I want a young team -- screen out the over-50s' is direct evidence of intent to discriminate on the basis of age, a protected class under federal (ADEA) and Texas law. The graduation-year filter was configured within the AI system to effectuate this intent. All three elements of §551.051(a) are satisfied: (1) AI system deployed, (2) intent to discriminate, (3) against a protected class. Gulfstream is liable as deployer for its employee's actions.

- **Rule ref:** R1
- **Fact refs:** F2, F5
- **Issue ref:** I2
- **Result:** violated

### A3

TRAIGA §551.201 expressly preempts any local ordinance regulating AI systems. The Houston 2024 ordinance requiring bias audits of AI hiring tools is a local regulation of AI systems by a political subdivision of Texas. It is preempted as of January 1, 2026. The February 2026 demand is legally void and unenforceable.

- **Rule ref:** R2
- **Fact refs:** F7
- **Issue ref:** I3
- **Result:** satisfied

### A4

TRAIGA §551.101 disclosure obligation applies only to governmental entities. Gulfstream is a private hospital system, not a governmental entity. §551.001(2) excludes employment contexts from the consumer definition. TRAIGA imposes no AI disclosure obligation on private employers regarding job applicants.

- **Rule ref:** R3
- **Fact refs:** F1, F6
- **Issue ref:** I4
- **Result:** satisfied

### A5

TRAIGA Key Compliance Notes confirm private employers need not disclose AI use in hiring. NYC LL 144 does not apply because there is no indication Gulfstream screens NYC-resident candidates. Colorado AIA is not yet in force and Gulfstream has no Colorado nexus. No applicable statute requires applicant AI disclosure.

- **Rule ref:** R9
- **Fact refs:** F6, F14
- **Issue ref:** I4
- **Result:** satisfied

### A6

TRAIGA §551.102 requires healthcare providers to disclose AI use to patients on the date treatment or service is provided. Gulfstream discloses DischargePredict use in writing on the admission form signed on the day care begins. This satisfies both the timing requirement (on the date service is provided) and the content requirement (disclosure that AI is being used in relation to patient service).

- **Rule ref:** R4
- **Fact refs:** F8, F9
- **Issue ref:** I5
- **Result:** satisfied

### A7

The internal discovery safe harbor under §551.301(c) requires three conjunctive elements: (1) internal discovery -- satisfied, Gulfstream found the filter through internal review; (2) reasonable cure steps -- satisfied, filter removed same week; (3) AG notification -- NOT satisfied, Gulfstream did not notify the AG. Failure on element 3 is fatal. The safe harbor is unavailable.

- **Rule ref:** R6
- **Fact refs:** F11, F12
- **Issue ref:** I6
- **Result:** violated

### A8

TRAIGA §551.301(d) provides a safe harbor for substantial compliance with NIST AI RMF. Gulfstream has maintained a NIST AI RMF-based program since 2025. The safe harbor is facially available. However, whether a governance-framework safe harbor can shield against an employee's intentional discrimination is analytically uncertain and likely contested. The program's detection of the violation supports the defense, but the AG may argue intentional discrimination should not be immunized by process compliance.

- **Rule ref:** R7
- **Fact refs:** F10
- **Issue ref:** I6
- **Result:** requires-fact

### A9

The AG sent written notice on March 30, 2026, triggering the 60-day cure period under §551.301(e). Gulfstream has until approximately May 29, 2026 to cure. The filter was already removed in March 2026, so the technical cure is accomplished. Gulfstream should formally document the cure in response to the AG notice within the 60-day window.

- **Rule ref:** R8
- **Fact refs:** F13
- **Issue ref:** I6
- **Result:** satisfied

## Conclusions (7)

### C1

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A1

### C2

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A2

### C3

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A3

### C4

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A4, A5

### C5

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A6

### C6

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A7

### C7

- **Determination:** conditional
- **Confidence:** medium
- **Support refs:** A8

## Obligations (7)

### O1

Formally respond to AG March 30 notice documenting cure of age-based filter within 60-day cure period

- **Required by:** R8
- **Status:** mandatory
- **Jurisdiction:** Texas
- **Deadline:** 2026-05-29

### O2

Ensure age-based filter remains removed and no similar discriminatory configurations exist

- **Required by:** R1
- **Status:** mandatory
- **Jurisdiction:** Texas
- **Deadline:** Not specified

### O3

Maintain and document NIST AI RMF governance program to preserve safe harbor defense under §551.301(d)

- **Required by:** R7
- **Status:** safe-harbor
- **Jurisdiction:** Texas
- **Deadline:** Not specified

### O4

Take remedial employment action regarding hiring manager who configured discriminatory filter

- **Required by:** R1
- **Status:** recommended
- **Jurisdiction:** Texas
- **Deadline:** Not specified

### O5

Respond to Houston ordinance demand citing TRAIGA §551.201 preemption; no bias audit required

- **Required by:** R2
- **Status:** recommended
- **Jurisdiction:** Texas
- **Deadline:** Not specified

### O6

Conduct validation study of TalentSieve under EEOC Uniform Guidelines to assess federal Title VII exposure from 0.71 gender impact ratio

- **Required by:** R1
- **Status:** recommended
- **Jurisdiction:** Texas
- **Deadline:** Not specified

### O7

If expanding to Colorado, prepare for Colorado AIA compliance including impact assessments, notices, and appeal rights

- **Required by:** R11
- **Status:** recommended
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

## Graph connections (35)

### E1

- **Src:** F3
- **Dst:** I1
- **Type:** triggers
- **Justification:** Gender impact ratio raises question of TRAIGA violation

### E2

- **Src:** F4
- **Dst:** I1
- **Type:** supports
- **Justification:** Absence of intent is dispositive under TRAIGA intent requirement

### E3

- **Src:** R1
- **Dst:** A1
- **Type:** applies-to
- **Justification:** TRAIGA §551.051(a) is the governing rule for gender impact analysis

### E4

- **Src:** A1
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** No intent found; TRAIGA not violated for gender disparity

### E5

- **Src:** F5
- **Dst:** I2
- **Type:** triggers
- **Justification:** Manager email expressing age discrimination intent raises TRAIGA violation issue

### E6

- **Src:** R1
- **Dst:** A2
- **Type:** applies-to
- **Justification:** TRAIGA §551.051(a) governs intentional discrimination analysis

### E7

- **Src:** A2
- **Dst:** C2
- **Type:** fails-element
- **Justification:** All elements of §551.051(a) satisfied; Gulfstream violated TRAIGA

### E8

- **Src:** F7
- **Dst:** I3
- **Type:** triggers
- **Justification:** Houston ordinance demand raises preemption question

### E9

- **Src:** R2
- **Dst:** A3
- **Type:** applies-to
- **Justification:** TRAIGA §551.201 preemption applies to Houston ordinance

### E10

- **Src:** A3
- **Dst:** C3
- **Type:** satisfies-element
- **Justification:** Houston ordinance is preempted; Gulfstream need not comply

### E11

- **Src:** R2
- **Dst:** O5
- **Type:** triggers
- **Justification:** Preemption provides basis for responding to Houston demand

### E12

- **Src:** F6
- **Dst:** I4
- **Type:** triggers
- **Justification:** Lack of applicant disclosure raises question of legal obligation

### E13

- **Src:** R3
- **Dst:** A4
- **Type:** applies-to
- **Justification:** TRAIGA §551.101 limits disclosure to government entities

### E14

- **Src:** R9
- **Dst:** A5
- **Type:** applies-to
- **Justification:** TRAIGA confirms no private employer disclosure obligation for hiring

### E15

- **Src:** A4
- **Dst:** C4
- **Type:** satisfies-element
- **Justification:** No disclosure obligation exists under any applicable statute

### E16

- **Src:** A5
- **Dst:** C4
- **Type:** satisfies-element
- **Justification:** Neither LL 144 nor Colorado AIA applies to Gulfstream

### E17

- **Src:** F9
- **Dst:** I5
- **Type:** triggers
- **Justification:** Patient disclosure practice raises sufficiency question under §551.102

### E18

- **Src:** R4
- **Dst:** A6
- **Type:** applies-to
- **Justification:** TRAIGA §551.102 governs healthcare AI disclosure

### E19

- **Src:** A6
- **Dst:** C5
- **Type:** satisfies-element
- **Justification:** Written disclosure on admission form on day care begins satisfies §551.102

### E20

- **Src:** F12
- **Dst:** I6
- **Type:** triggers
- **Justification:** Failure to notify AG raises safe harbor availability question

### E21

- **Src:** R6
- **Dst:** A7
- **Type:** applies-to
- **Justification:** §551.301(c) internal discovery safe harbor analysis

### E22

- **Src:** A7
- **Dst:** C6
- **Type:** fails-element
- **Justification:** Safe harbor unavailable due to missing AG notification

### E23

- **Src:** R7
- **Dst:** A8
- **Type:** applies-to
- **Justification:** §551.301(d) NIST AI RMF safe harbor analysis

### E24

- **Src:** A8
- **Dst:** C7
- **Type:** supports
- **Justification:** NIST safe harbor conditionally available but application to intentional discrimination uncertain

### E25

- **Src:** F13
- **Dst:** I6
- **Type:** triggers
- **Justification:** AG notice triggers 60-day cure period analysis

### E26

- **Src:** R8
- **Dst:** A9
- **Type:** applies-to
- **Justification:** §551.301(e) cure period applies to AG March 30 notice

### E27

- **Src:** R8
- **Dst:** O1
- **Type:** triggers
- **Justification:** 60-day cure period creates mandatory response deadline

### E28

- **Src:** R1
- **Dst:** O2
- **Type:** triggers
- **Justification:** Ongoing compliance requires ensuring no discriminatory configurations

### E29

- **Src:** R7
- **Dst:** O3
- **Type:** triggers
- **Justification:** NIST AI RMF safe harbor requires continued program maintenance

### E30

- **Src:** R1
- **Dst:** O4
- **Type:** triggers
- **Justification:** Remedial action against manager supports good faith and prevents recurrence

### E31

- **Src:** F14
- **Dst:** I4
- **Type:** supports
- **Justification:** No NYC or Colorado nexus means LL 144 and Colorado AIA do not apply

### E32

- **Src:** R10
- **Dst:** A5
- **Type:** applies-to
- **Justification:** LL 144 geographic scope analysis confirms inapplicability

### E33

- **Src:** R11
- **Dst:** O7
- **Type:** triggers
- **Justification:** Colorado AIA readiness obligation if Gulfstream expands to Colorado

### E34

- **Src:** R5
- **Dst:** O1
- **Type:** triggers
- **Justification:** AG exclusive enforcement authority and penalty structure frame response urgency

### E35

- **Src:** A9
- **Dst:** O1
- **Type:** supports
- **Justification:** Cure period analysis confirms deadline for formal AG response
