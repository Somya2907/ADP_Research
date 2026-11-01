# E6 — AskTexLicense Agency Chatbot — teacher FIRACO reasoning

Unverified model output for legal review. Citations, facts, applications, and obligations may be incorrect. Text and node IDs below are preserved from the saved reference graph.

[Read case](../../../data/cases/E6_asktexlicense_agency_tx.md) · [Review brief](../../PROF_PHILIPP_REVIEW.md)

Teacher: claude-opus-4-6. Source: data/outputs/graphs/E6_reference.json.

Source SHA-256: `aec1d28633e9257f50946ebc5aa162920516c593bfa084a2d1763d8500f97e4f`.

## Facts (15)

### F1

Texas Department of Licensing Services is a Texas state government agency

- **Polarity:** present
- **Support quote:** The Texas Department of Licensing Services is a state agency that issues and renews occupational licenses

### F2

Agency deployed AskTexLicense AI chatbot in January 2026

- **Polarity:** present
- **Support quote:** In January 2026 the agency deployed 'AskTexLicense,' an artificial intelligence chatbot built by Brazos AI

### F3

Chatbot deployed on website and telephone line

- **Polarity:** present
- **Support quote:** on its website and its telephone line

### F4

Chatbot answers questions from individual Texas residents about licensing

- **Polarity:** present
- **Support quote:** The chatbot answers questions from individual Texas residents about license renewal deadlines, fees, and eligibility requirements

### F5

Chatbot handles approximately 40,000 conversations per month

- **Polarity:** present
- **Support quote:** It handles about 40,000 conversations each month

### F6

Chatbot introduces itself as 'Riley, your licensing assistant' with a human photograph

- **Polarity:** present
- **Support quote:** The chatbot introduces itself as 'Riley, your licensing assistant' and displays a photograph of a person

### F7

No disclosure at any point that Riley is an AI system

- **Polarity:** present
- **Support quote:** At no point before or during a conversation is the resident told that Riley is an artificial intelligence system

### F8

Website terms of use do not mention artificial intelligence

- **Polarity:** present
- **Support quote:** The agency's website terms of use do not mention artificial intelligence

### F9

IT director stated disclosure is unnecessary because answers are accurate

- **Polarity:** present
- **Support quote:** a disclosure is unnecessary because 'the answers are accurate, and people would trust it less if they knew'

### F10

Texas AG sent written notice of alleged violation on March 20, 2026

- **Polarity:** present
- **Support quote:** On March 20, 2026, the Texas Attorney General sent the agency a written notice of an alleged violation

### F11

Agency has not changed chatbot presentation as of mid-April 2026

- **Polarity:** present
- **Support quote:** As of mid-April 2026 the agency has not changed how the chatbot presents itself

### F12

Agency has no AI governance program and no NIST AI RMF alignment

- **Polarity:** present
- **Support quote:** The agency has no AI governance program and has not aligned its practices with the NIST AI Risk Management Framework

### F13

No evidence of intent to discriminate or cause harm

- **Polarity:** present
- **Support quote:** There is no evidence that the chatbot was built or deployed with any intent to discriminate or to cause harm

### F14

Users are Texas residents acting in individual capacity regarding personal licenses

- **Polarity:** present
- **Support quote:** Not specified

### F15

No nexus to New York City or Colorado

- **Polarity:** present
- **Support quote:** Not specified

## Issues (6)

### I1

Does the agency violate TRAIGA 551.101 by failing to disclose AI interaction to consumers?

- **Status:** dispositive

### I2

What is the status and effect of the 60-day cure period under TRAIGA 551.301(e)?

- **Status:** dispositive

### I3

Are any TRAIGA safe harbors available to the agency?

- **Status:** dispositive

### I4

Does the agency violate TRAIGA 551.051 prohibited conduct provisions?

- **Status:** collateral

### I5

Does NYC LL 144 apply to the agency?

- **Status:** collateral

### I6

Does the Colorado AIA apply to the agency?

- **Status:** collateral

## Rules (11)

### R1

Government agency must disclose to consumer before or at time of interaction that consumer is interacting with an AI system

- **Citation:** TRAIGA §551.101(a)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R2

Definition of artificial intelligence system - machine-based system that infers from inputs how to generate outputs

- **Citation:** TRAIGA §551.001(1)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R3

Definition of consumer - Texas resident acting in individual or household context, excludes commercial or employment context

- **Citation:** TRAIGA §551.001(2)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R4

Only Texas AG may enforce TRAIGA; no private right of action

- **Citation:** TRAIGA §551.301(a)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R5

Civil penalties of $10,000 to $200,000 per violation, may accrue on continuing daily basis

- **Citation:** TRAIGA §551.301(b)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R6

AG must provide written notice and allow 60 days to cure before initiating enforcement

- **Citation:** TRAIGA §551.301(e)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R7

Safe harbor for violations discovered through internal testing with reasonable cure steps and AG notification

- **Citation:** TRAIGA §551.301(c)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R8

Safe harbor for substantial compliance with NIST AI RMF or equivalent AI governance standards

- **Citation:** TRAIGA §551.301(d)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R9

Prohibits deploying AI with intent to unlawfully discriminate, incite harm, or infringe constitutional rights

- **Citation:** TRAIGA §551.051
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R10

Applies to employers/employment agencies using AEDTs for employment screening in NYC

- **Citation:** NYC LL 144 §20-874
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R11

Deployer obligations for high-risk AI systems making consequential decisions in Colorado

- **Citation:** Colorado AIA §6-1-1703
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

## Applications (9)

### A1

The agency is a governmental entity of Texas (F1) that deployed an AI system (F2, F3) that interacts with consumers - Texas residents acting in individual capacity about personal licenses (F4, F14). The statute requires disclosure before or at the time of interaction that the consumer is interacting with an AI system. The chatbot presents as human 'Riley' with a photograph (F6), makes no AI disclosure at any point (F7), and the website terms of use do not mention AI (F8). All elements of the obligation are met; the disclosure requirement is completely unsatisfied.

- **Rule ref:** R1
- **Fact refs:** F1, F2, F3, F4, F6, F7, F8, F14
- **Issue ref:** I1
- **Result:** violated

### A2

AskTexLicense is an AI chatbot that processes natural language inputs and generates responsive content about licensing. It is a machine-based system that infers from inputs how to generate outputs (content and recommendations), satisfying the statutory definition of an AI system.

- **Rule ref:** R2
- **Fact refs:** F2
- **Issue ref:** I1
- **Result:** satisfied

### A3

Texas residents seeking information about their personal occupational license renewals are acting in an individual capacity, not in a commercial or employment context. They qualify as consumers under TRAIGA.

- **Rule ref:** R3
- **Fact refs:** F4, F14
- **Issue ref:** I1
- **Result:** satisfied

### A4

The AG sent written notice on March 20, 2026, triggering the 60-day cure period expiring approximately May 19, 2026. As of mid-April 2026, the agency has not cured. The agency still has approximately one month remaining but has shown no intent to cure. If it fails to cure by the deadline, the AG may initiate enforcement proceedings.

- **Rule ref:** R6
- **Fact refs:** F10, F11
- **Issue ref:** I2
- **Result:** partial

### A5

The internal-discovery safe harbor requires the person to have discovered the violation through internal testing. Here, the AG discovered and notified the agency of the violation (F10). The agency did not self-discover. Additionally, the agency has taken no steps to cure (F11). This safe harbor is unavailable.

- **Rule ref:** R7
- **Fact refs:** F10, F11, F12
- **Issue ref:** I3
- **Result:** violated

### A6

The NIST AI RMF safe harbor requires substantial compliance with NIST AI 100-1 or equivalent standards. The agency has no AI governance program and has not aligned with the NIST AI RMF (F12). This safe harbor is unavailable.

- **Rule ref:** R8
- **Fact refs:** F12
- **Issue ref:** I3
- **Result:** violated

### A7

Section 551.051 requires intent to unlawfully discriminate, incite harm, or infringe constitutional rights. There is no evidence of any such intent (F13). No violation of this provision.

- **Rule ref:** R9
- **Fact refs:** F13
- **Issue ref:** I4
- **Result:** satisfied

### A8

NYC LL 144 applies to employers/employment agencies using AEDTs for employment screening in NYC. The agency is a Texas government entity (F1), the chatbot provides licensing information not employment screening (F4), and there is no NYC nexus (F15). LL 144 is inapplicable.

- **Rule ref:** R10
- **Fact refs:** F1, F4, F15
- **Issue ref:** I5
- **Result:** satisfied

### A9

Colorado AIA applies to deployers doing business in Colorado making consequential decisions. The agency operates only in Texas (F1, F15), the chatbot provides informational responses not consequential decisions (F4), and the Colorado AIA is not yet effective until June 30, 2026. Inapplicable on all grounds.

- **Rule ref:** R11
- **Fact refs:** F1, F4, F15
- **Issue ref:** I6
- **Result:** satisfied

## Conclusions (6)

### C1

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A1, A2, A3

### C2

- **Determination:** conditional
- **Confidence:** high
- **Support refs:** A4

### C3

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A5, A6

### C4

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A7

### C5

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A8

### C6

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A9

## Obligations (5)

### O1

Implement AI disclosure in chatbot: inform consumers before or at time of interaction that they are interacting with an AI system

- **Required by:** R1
- **Status:** mandatory
- **Jurisdiction:** Texas
- **Deadline:** 2026-05-19

### O2

Remove or supplement deceptive human persona elements (human name and photograph without AI disclosure)

- **Required by:** R1
- **Status:** mandatory
- **Jurisdiction:** Texas
- **Deadline:** 2026-05-19

### O3

Notify Texas AG that the violation has been cured once disclosure is implemented

- **Required by:** R6
- **Status:** mandatory
- **Jurisdiction:** Texas
- **Deadline:** 2026-05-19

### O4

Establish AI governance program aligned with NIST AI RMF (NIST AI 100-1) to obtain safe harbor protection

- **Required by:** R8
- **Status:** safe-harbor
- **Jurisdiction:** Texas
- **Deadline:** Not specified

### O5

Audit all current and planned AI deployments for TRAIGA compliance including disclosure and prohibited conduct requirements

- **Required by:** R1
- **Status:** recommended
- **Jurisdiction:** Texas
- **Deadline:** Not specified

## Graph connections (33)

### E1

- **Src:** F1
- **Dst:** I1
- **Type:** triggers
- **Justification:** Agency status as Texas governmental entity triggers applicability of TRAIGA 551.101

### E2

- **Src:** F7
- **Dst:** I1
- **Type:** triggers
- **Justification:** Absence of AI disclosure is the core factual predicate for the violation

### E3

- **Src:** F6
- **Dst:** I1
- **Type:** triggers
- **Justification:** Human persona presentation aggravates the non-disclosure

### E4

- **Src:** F10
- **Dst:** I2
- **Type:** triggers
- **Justification:** AG written notice triggers the 60-day cure period

### E5

- **Src:** F12
- **Dst:** I3
- **Type:** triggers
- **Justification:** Absence of AI governance program raises safe harbor availability question

### E6

- **Src:** F13
- **Dst:** I4
- **Type:** triggers
- **Justification:** Absence of discriminatory intent is relevant to 551.051 analysis

### E7

- **Src:** F15
- **Dst:** I5
- **Type:** triggers
- **Justification:** No NYC nexus raises jurisdictional applicability question

### E8

- **Src:** F15
- **Dst:** I6
- **Type:** triggers
- **Justification:** No Colorado nexus raises jurisdictional applicability question

### E9

- **Src:** R1
- **Dst:** A1
- **Type:** applies-to
- **Justification:** Government disclosure obligation is the primary rule applied

### E10

- **Src:** R2
- **Dst:** A2
- **Type:** applies-to
- **Justification:** AI system definition determines whether chatbot qualifies

### E11

- **Src:** R3
- **Dst:** A3
- **Type:** applies-to
- **Justification:** Consumer definition determines whether users qualify

### E12

- **Src:** R6
- **Dst:** A4
- **Type:** applies-to
- **Justification:** Cure period provision governs enforcement timeline

### E13

- **Src:** R7
- **Dst:** A5
- **Type:** applies-to
- **Justification:** Internal discovery safe harbor analyzed for availability

### E14

- **Src:** R8
- **Dst:** A6
- **Type:** applies-to
- **Justification:** NIST AI RMF safe harbor analyzed for availability

### E15

- **Src:** R9
- **Dst:** A7
- **Type:** applies-to
- **Justification:** Prohibited conduct provision analyzed for violation

### E16

- **Src:** R10
- **Dst:** A8
- **Type:** applies-to
- **Justification:** NYC LL 144 applicability analyzed

### E17

- **Src:** R11
- **Dst:** A9
- **Type:** applies-to
- **Justification:** Colorado AIA applicability analyzed

### E18

- **Src:** A1
- **Dst:** C1
- **Type:** fails-element
- **Justification:** Agency fails disclosure requirement - non-compliant with TRAIGA 551.101

### E19

- **Src:** A2
- **Dst:** C1
- **Type:** supports
- **Justification:** Chatbot meets AI system definition, confirming 551.101 applies

### E20

- **Src:** A3
- **Dst:** C1
- **Type:** supports
- **Justification:** Users meet consumer definition, confirming 551.101 applies

### E21

- **Src:** A4
- **Dst:** C2
- **Type:** supports
- **Justification:** Cure period is running but agency has not yet cured - conditional status

### E22

- **Src:** A5
- **Dst:** C3
- **Type:** fails-element
- **Justification:** Internal discovery safe harbor unavailable - AG discovered violation

### E23

- **Src:** A6
- **Dst:** C3
- **Type:** fails-element
- **Justification:** NIST AI RMF safe harbor unavailable - no governance program exists

### E24

- **Src:** A7
- **Dst:** C4
- **Type:** satisfies-element
- **Justification:** No intent to discriminate - compliant with 551.051

### E25

- **Src:** A8
- **Dst:** C5
- **Type:** satisfies-element
- **Justification:** No NYC nexus - LL 144 inapplicable

### E26

- **Src:** A9
- **Dst:** C6
- **Type:** satisfies-element
- **Justification:** No Colorado nexus and statute not yet effective - CO AIA inapplicable

### E27

- **Src:** R1
- **Dst:** O1
- **Type:** triggers
- **Justification:** Disclosure obligation requires implementation of AI disclosure

### E28

- **Src:** R1
- **Dst:** O2
- **Type:** triggers
- **Justification:** Disclosure obligation requires addressing deceptive human persona

### E29

- **Src:** R6
- **Dst:** O3
- **Type:** triggers
- **Justification:** Cure period requires AG notification upon cure

### E30

- **Src:** R8
- **Dst:** O4
- **Type:** triggers
- **Justification:** NIST AI RMF safe harbor motivates governance program establishment

### E31

- **Src:** R5
- **Dst:** C2
- **Type:** supports
- **Justification:** Penalty provisions of $10,000-$200,000 per violation with daily accrual define enforcement exposure

### E32

- **Src:** C1
- **Dst:** O1
- **Type:** triggers
- **Justification:** Non-compliance determination necessitates remedial disclosure obligation

### E33

- **Src:** C3
- **Dst:** O4
- **Type:** triggers
- **Justification:** Unavailability of safe harbors motivates establishing AI governance program
