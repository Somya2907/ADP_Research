# E10 — TriageAssist Clinic Disclosure — teacher FIRACO reasoning

Unverified model output for legal review. Citations, facts, applications, and obligations may be incorrect. Text and node IDs below are preserved from the saved reference graph.

[Read case](../../../data/cases/E10_triageassist_clinics_tx.md) · [Review brief](../../PROF_PHILIPP_REVIEW.md)

Teacher: claude-opus-4-6. Source: data/outputs/graphs/E10_reference.json.

Source SHA-256: `3fda13da27cbe6fb4766d8e273acad843d3e71f67b7ba5451b3829b6aff35ff3`.

## Facts (12)

### F1

Lone Star is a private health care service provider operating 22 clinics in San Antonio and Austin, Texas

- **Polarity:** present
- **Support quote:** Lone Star Family Clinics operates 22 primary-care clinics in San Antonio and Austin, Texas

### F2

Since February 2026, all clinics use TriageAssist, an AI system built by MedVector

- **Polarity:** present
- **Support quote:** Since February 2026, every clinic has used 'TriageAssist,' an artificial intelligence system built by MedVector

### F3

TriageAssist analyzes patient symptoms and generates recommended visit priority and suggested diagnostic tests

- **Polarity:** present
- **Support quote:** TriageAssist analyzes them and gives the treating physician a recommended visit priority and a list of suggested diagnostic tests

### F4

Physicians adopt TriageAssist suggested tests in most visits

- **Polarity:** present
- **Support quote:** Clinic records show that physicians adopt the suggested tests in most visits

### F5

Patients are not told that TriageAssist is used; no AI disclosure in check-in screen, consent forms, or visit summary

- **Polarity:** present
- **Support quote:** Patients are not told that TriageAssist is used. The check-in screen, the consent forms, and the visit summary say nothing about artificial intelligence

### F6

CMO justifies non-disclosure: disclosure would confuse patients and physician sign-off means AI is not used in relation to treatment

- **Polarity:** present
- **Support quote:** a disclosure 'would only confuse patients,' and that because a physician signs off on every order, the AI system is not really 'used in relation to' a patient's treatment

### F7

Patient advocacy group filed complaint with Texas AG in March 2026

- **Polarity:** present
- **Support quote:** In March 2026 a patient advocacy group filed a complaint about TriageAssist with the Texas Attorney General

### F8

As of mid-April 2026, Texas AG has not sent Lone Star any notice

- **Polarity:** present
- **Support quote:** As of mid-April 2026 the Attorney General has not sent Lone Star any notice

### F9

No evidence of intent to discriminate or cause harm

- **Polarity:** present
- **Support quote:** There is no evidence that TriageAssist was developed or deployed with an intent to discriminate against any group or to cause harm

### F10

Lone Star has no AI governance program and has not adopted NIST AI RMF

- **Polarity:** present
- **Support quote:** Lone Star has no AI governance program and has not adopted the NIST AI Risk Management Framework

### F11

Lone Star operates exclusively in Texas with no NYC or Colorado nexus

- **Polarity:** present
- **Support quote:** Not specified

### F12

TriageAssist is used in healthcare context, not employment context

- **Polarity:** present
- **Support quote:** Not specified

## Issues (7)

### I1

Does Lone Star's failure to disclose TriageAssist use to patients violate TRAIGA Section 551.102 healthcare provider disclosure obligation?

- **Status:** dispositive

### I2

Does physician sign-off negate the 'used in relation to' requirement under Section 551.102?

- **Status:** dispositive

### I3

Does Lone Star violate TRAIGA Section 551.051(a) prohibition on intentional discrimination?

- **Status:** collateral

### I4

Does lack of AI governance program or NIST AI RMF adoption create legal exposure under TRAIGA?

- **Status:** collateral

### I5

Is Lone Star subject to NYC Local Law 144?

- **Status:** collateral

### I6

Is Lone Star subject to Colorado AI Act?

- **Status:** collateral

### I7

What enforcement mechanisms, cure periods, and safe harbors are available under TRAIGA?

- **Status:** dispositive

## Rules (11)

### R1

Healthcare provider must disclose to patient on date of service that AI system is used in relation to patient's service or treatment

- **Citation:** TX TRAIGA Section 551.102
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R2

Definition of artificial intelligence system: machine-based system that infers from inputs how to generate outputs including predictions or recommendations

- **Citation:** TX TRAIGA Section 551.001(1)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R3

Prohibition on developing or deploying AI with intent to unlawfully discriminate against protected class

- **Citation:** TX TRAIGA Section 551.051(a)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R4

Only Texas AG may enforce TRAIGA; no private right of action

- **Citation:** TX TRAIGA Section 551.301(a)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R5

Civil penalties from $10,000 to $200,000 per violation, may accrue daily

- **Citation:** TX TRAIGA Section 551.301(b)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R6

Safe harbor for internal discovery, reasonable cure steps, and AG notification

- **Citation:** TX TRAIGA Section 551.301(c)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R7

Safe harbor for substantial compliance with NIST AI RMF or equivalent recognized AI governance standards

- **Citation:** TX TRAIGA Section 551.301(d)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R8

AG must provide written notice and allow 60 days to cure before enforcement

- **Citation:** TX TRAIGA Section 551.301(e)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R9

Bias audit and notice requirements for AEDTs used in employment decisions in NYC

- **Citation:** NYC LL 144 Section 20-871
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R10

Deployer obligations for high-risk AI systems making consequential decisions in Colorado

- **Citation:** CO AIA Section 6-1-1703
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R11

TRAIGA preempts local Texas ordinances regulating AI systems

- **Citation:** TX TRAIGA Section 551.201
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

## Applications (9)

### A1

Lone Star is a healthcare provider (F1) using an AI system (F2, F3) in relation to patient treatment (F3, F4). Section 551.102 requires disclosure on the date of service. No disclosure is made (F5). The CMO's justifications (F6) are legally insufficient: the statute uses broad 'in relation to' language with no physician-override exception, and patient confusion is not a statutory defense. Violation is clear and ongoing since February 2026.

- **Rule ref:** R1
- **Fact refs:** F1, F2, F3, F4, F5, F6
- **Issue ref:** I1
- **Result:** violated

### A2

TriageAssist is a machine-based system that processes symptom inputs and generates recommendations (visit priority, diagnostic tests) that influence the clinical environment. It squarely meets the Section 551.001(1) definition of an AI system.

- **Rule ref:** R2
- **Fact refs:** F2, F3
- **Issue ref:** I1
- **Result:** satisfied

### A3

The CMO argues physician sign-off means AI is not 'used in relation to' treatment. This fails because: (1) 'in relation to' is broader than 'to determine' or 'to make'; (2) physicians adopt suggestions in most visits (F4), showing material influence; (3) the statute contains no physician-override exception. Human review does not negate the AI system's role.

- **Rule ref:** R1
- **Fact refs:** F4, F6
- **Issue ref:** I2
- **Result:** violated

### A4

Section 551.051(a) requires intent to unlawfully discriminate. No evidence of discriminatory intent exists (F9). TRAIGA does not impose disparate impact liability. No violation.

- **Rule ref:** R3
- **Fact refs:** F9
- **Issue ref:** I3
- **Result:** satisfied

### A5

The NIST AI RMF safe harbor under Section 551.301(d) requires substantial compliance with NIST AI 100-1 or equivalent. Lone Star has no AI governance program and has not adopted NIST AI RMF (F10). The safe harbor is unavailable, leaving Lone Star without this defense against the Section 551.102 violation.

- **Rule ref:** R7
- **Fact refs:** F10
- **Issue ref:** I4
- **Result:** violated

### A6

The internal discovery safe harbor requires: (1) discovery through internal testing, (2) reasonable cure steps, and (3) AG notification. The violation was identified externally by a patient advocacy group (F7), not through internal testing. Lone Star has not cured or notified the AG. This safe harbor is unavailable.

- **Rule ref:** R6
- **Fact refs:** F7, F8
- **Issue ref:** I7
- **Result:** violated

### A7

Section 551.301(e) requires the AG to provide written notice and allow 60 days to cure before enforcement. The AG has not yet sent notice (F8). Therefore, the 60-day cure period has not been triggered, and enforcement proceedings cannot yet commence. This provides Lone Star a window to remediate proactively.

- **Rule ref:** R8
- **Fact refs:** F8
- **Issue ref:** I7
- **Result:** satisfied

### A8

NYC LL 144 applies to AEDTs used for employment decisions for NYC positions. Lone Star operates only in Texas (F11) and uses TriageAssist in healthcare, not employment (F12). LL 144 is inapplicable on two independent grounds: no NYC nexus and no employment context.

- **Rule ref:** R9
- **Fact refs:** F11, F12
- **Issue ref:** I5
- **Result:** satisfied

### A9

Colorado AIA applies to deployers doing business in Colorado. Lone Star operates only in Texas (F11). Additionally, the Colorado AIA does not take effect until June 30, 2026, and is not yet in force as of April 2026. Inapplicable on two independent grounds.

- **Rule ref:** R10
- **Fact refs:** F11
- **Issue ref:** I6
- **Result:** satisfied

## Conclusions (5)

### C1

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A1, A2, A3

### C2

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A4

### C3

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A5, A6

### C4

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A8

### C5

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A9

## Obligations (6)

### O1

Implement patient-facing AI disclosure on date of service across all 22 clinics, informing patients that TriageAssist AI is used in relation to their treatment

- **Required by:** R1
- **Status:** mandatory
- **Jurisdiction:** Texas
- **Deadline:** Immediate; must be in place before next patient encounter to stop accruing violations

### O2

Cure violation within 60 days of receiving written AG notice under Section 551.301(e)

- **Required by:** R8
- **Status:** mandatory
- **Jurisdiction:** Texas
- **Deadline:** 60 days after AG written notice is received

### O3

Adopt and substantially comply with NIST AI RMF (NIST AI 100-1) or equivalent recognized AI governance standard to obtain safe harbor protection

- **Required by:** R7
- **Status:** safe-harbor
- **Jurisdiction:** Texas
- **Deadline:** Not specified

### O4

Establish comprehensive AI governance program covering disclosure, risk assessment, monitoring, and incident response for all clinical AI systems

- **Required by:** R7
- **Status:** recommended
- **Jurisdiction:** Texas
- **Deadline:** Not specified

### O5

Proactively notify Texas AG of the Section 551.102 violation and remediation steps to strengthen safe harbor position under Section 551.301(c)

- **Required by:** R6
- **Status:** recommended
- **Jurisdiction:** Texas
- **Deadline:** Not specified

### O6

Update check-in screens, consent forms, and visit summaries to include clear AI disclosure language

- **Required by:** R1
- **Status:** mandatory
- **Jurisdiction:** Texas
- **Deadline:** Immediate

## Graph connections (32)

### E1

- **Src:** F1
- **Dst:** I1
- **Type:** triggers
- **Justification:** Healthcare provider status triggers Section 551.102 analysis

### E2

- **Src:** F5
- **Dst:** I1
- **Type:** triggers
- **Justification:** Non-disclosure is the core factual predicate for the disclosure violation

### E3

- **Src:** F6
- **Dst:** I2
- **Type:** triggers
- **Justification:** CMO's physician sign-off argument raises the 'used in relation to' interpretation issue

### E4

- **Src:** R1
- **Dst:** A1
- **Type:** applies-to
- **Justification:** Section 551.102 is the primary rule applied to the disclosure facts

### E5

- **Src:** R2
- **Dst:** A2
- **Type:** applies-to
- **Justification:** AI system definition applied to determine TriageAssist qualifies

### E6

- **Src:** R1
- **Dst:** A3
- **Type:** applies-to
- **Justification:** Section 551.102 'in relation to' language applied to physician sign-off argument

### E7

- **Src:** A1
- **Dst:** C1
- **Type:** fails-element
- **Justification:** Failure to disclose establishes non-compliance with Section 551.102

### E8

- **Src:** A2
- **Dst:** C1
- **Type:** supports
- **Justification:** TriageAssist meeting AI definition supports finding of violation

### E9

- **Src:** A3
- **Dst:** C1
- **Type:** fails-element
- **Justification:** Physician sign-off does not negate 'used in relation to' requirement

### E10

- **Src:** R3
- **Dst:** A4
- **Type:** applies-to
- **Justification:** Intentional discrimination prohibition applied to facts

### E11

- **Src:** A4
- **Dst:** C2
- **Type:** satisfies-element
- **Justification:** No evidence of discriminatory intent means no Section 551.051(a) violation

### E12

- **Src:** R7
- **Dst:** A5
- **Type:** applies-to
- **Justification:** NIST safe harbor rule applied to Lone Star's lack of governance program

### E13

- **Src:** A5
- **Dst:** C3
- **Type:** fails-element
- **Justification:** No NIST compliance means safe harbor unavailable

### E14

- **Src:** R6
- **Dst:** A6
- **Type:** applies-to
- **Justification:** Internal discovery safe harbor applied to external complaint facts

### E15

- **Src:** A6
- **Dst:** C3
- **Type:** fails-element
- **Justification:** External discovery and no cure steps means safe harbor unavailable

### E16

- **Src:** R8
- **Dst:** A7
- **Type:** applies-to
- **Justification:** 60-day cure period rule applied to AG notice status

### E17

- **Src:** A7
- **Dst:** O2
- **Type:** triggers
- **Justification:** AG notice will trigger mandatory 60-day cure obligation

### E18

- **Src:** R9
- **Dst:** A8
- **Type:** applies-to
- **Justification:** NYC LL 144 jurisdictional analysis

### E19

- **Src:** A8
- **Dst:** C4
- **Type:** satisfies-element
- **Justification:** No NYC nexus and no employment context means LL 144 inapplicable

### E20

- **Src:** R10
- **Dst:** A9
- **Type:** applies-to
- **Justification:** Colorado AIA jurisdictional and temporal analysis

### E21

- **Src:** A9
- **Dst:** C5
- **Type:** satisfies-element
- **Justification:** No Colorado nexus and statute not yet effective means CO AIA inapplicable

### E22

- **Src:** C1
- **Dst:** O1
- **Type:** triggers
- **Justification:** Non-compliance finding triggers mandatory disclosure obligation

### E23

- **Src:** C1
- **Dst:** O6
- **Type:** triggers
- **Justification:** Non-compliance triggers obligation to update patient-facing materials

### E24

- **Src:** C3
- **Dst:** O3
- **Type:** triggers
- **Justification:** Unavailability of safe harbors triggers recommendation to adopt NIST AI RMF

### E25

- **Src:** C3
- **Dst:** O4
- **Type:** triggers
- **Justification:** Unavailability of safe harbors triggers recommendation for AI governance program

### E26

- **Src:** R5
- **Dst:** C1
- **Type:** supports
- **Justification:** Penalty range of $10,000-$200,000 per violation with daily accrual underscores severity of non-compliance

### E27

- **Src:** F9
- **Dst:** I3
- **Type:** triggers
- **Justification:** Absence of discriminatory intent raises question of Section 551.051(a) compliance

### E28

- **Src:** F10
- **Dst:** I4
- **Type:** triggers
- **Justification:** Lack of governance program raises question of safe harbor availability

### E29

- **Src:** F11
- **Dst:** I5
- **Type:** triggers
- **Justification:** Texas-only operations raise jurisdictional question for NYC LL 144

### E30

- **Src:** F11
- **Dst:** I6
- **Type:** triggers
- **Justification:** Texas-only operations raise jurisdictional question for Colorado AIA

### E31

- **Src:** R4
- **Dst:** O5
- **Type:** triggers
- **Justification:** AG-only enforcement means proactive AG notification is strategically important

### E32

- **Src:** F7
- **Dst:** I7
- **Type:** triggers
- **Justification:** Filed complaint raises enforcement mechanism and cure period questions
