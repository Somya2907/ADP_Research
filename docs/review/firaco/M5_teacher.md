# M5 — ClaimGuard and the High-Risk Exclusions — teacher FIRACO reasoning

Unverified model output for legal review. Citations, facts, applications, and obligations may be incorrect. Text and node IDs below are preserved from the saved reference graph.

[Read case](../../../data/cases/M5_claimguard_exclusions_co.md) · [Review brief](../../PROF_PHILIPP_REVIEW.md)

Teacher: claude-opus-4-6. Source: data/outputs/graphs/M5_reference.json.

Source SHA-256: `1810f33e5dff1e28aeae5bddc8ef48d30c4d625b433d19bfb8bc2f3ec9588735`.

## Facts (17)

### F1

Cimarron Peak Insurance is a homeowners insurer in Colorado Springs, CO, doing business in the state

- **Polarity:** present
- **Support quote:** Cimarron Peak Insurance is a homeowners insurer in Colorado Springs, Colorado

### F2

Cimarron Peak has 420 full-time employees

- **Polarity:** present
- **Support quote:** with 420 full-time employees

### F3

Three AI tools supplied by Graywolf Analytics: DocParse, PatternWatch, ClaimGuard

- **Polarity:** present
- **Support quote:** It uses three AI tools supplied by Graywolf Analytics

### F4

DocParse reads claim forms and copies names, dates, amounts into claims system; makes no evaluation

- **Polarity:** present
- **Support quote:** DocParse reads submitted claim forms and copies names, dates, and amounts into the claims system. It makes no evaluation of a claim.

### F5

PatternWatch runs quarterly on closed claims, flags adjuster payout pattern deviations, no effect on individual claims

- **Polarity:** present
- **Support quote:** PatternWatch runs once a quarter on claims that are already closed. It has no effect on any individual claim.

### F6

ClaimGuard assigns fraud score 0-100; claims above 80 routed to special handling

- **Polarity:** present
- **Support quote:** ClaimGuard assigns a fraud score from 0 to 100 to every open claim. Claims scoring above 80 are routed to special handling.

### F7

81% of claims in special handling were denied in 2025

- **Polarity:** present
- **Support quote:** 81% of claims in special handling were denied

### F8

37% of denied policyholders were later non-renewed

- **Polarity:** present
- **Support quote:** 37% of those policyholders were later non-renewed

### F9

Adjusters override ClaimGuard routing in only 6% of cases

- **Polarity:** present
- **Support quote:** Adjusters may override the routing, and did so in 6% of cases

### F10

Single AI governance policy covers all three tools, certified to ISO/IEC 27001

- **Polarity:** present
- **Support quote:** One AI governance policy covers all three tools. It is certified to ISO/IEC 27001, an information-security standard.

### F11

Impact assessment completed for DocParse only

- **Polarity:** present
- **Support quote:** An impact assessment was completed for DocParse only

### F12

Website states only: We use technology to process claims efficiently

- **Polarity:** present
- **Support quote:** The website states: We use technology to process claims efficiently.

### F13

Denial and non-renewal letters do not mention any AI system

- **Polarity:** present
- **Support quote:** Denial and non-renewal letters do not mention any AI system

### F14

General claims-appeal process exists; second adjuster reviews file without seeing ClaimGuard score

- **Polarity:** present
- **Support quote:** A policyholder may use the general claims-appeal process, in which a second adjuster reviews the file. That adjuster is not shown the ClaimGuard score.

### F15

No process for correcting data that ClaimGuard used

- **Polarity:** present
- **Support quote:** There is no process for correcting data that ClaimGuard used

### F16

General counsel concluded none of the three tools is high-risk

- **Polarity:** present
- **Support quote:** general counsel has concluded that none of the three tools is high-risk

### F17

Insurance is a consequential-decision domain under CO AIA

- **Polarity:** present
- **Support quote:** Not specified

## Issues (7)

### I1

Is DocParse a high-risk AI system under CO AIA Section 6-1-1701(7)?

- **Status:** dispositive

### I2

Is PatternWatch a high-risk AI system under CO AIA Section 6-1-1701(7)?

- **Status:** dispositive

### I3

Is ClaimGuard a high-risk AI system under CO AIA Section 6-1-1701(7)?

- **Status:** dispositive

### I4

Is ClaimGuard a substantial factor in consequential decisions despite 6% adjuster override rate?

- **Status:** dispositive

### I5

Does ISO/IEC 27001 certification satisfy the risk management program requirement under Section 6-1-1703(2)(a)(III)?

- **Status:** dispositive

### I6

Are impact assessment, consumer notice, data correction, and appeal measures sufficient under Section 6-1-1703(2)?

- **Status:** dispositive

### I7

What obligations apply to Cimarron Peak and by what deadlines?

- **Status:** collateral

## Rules (19)

### R1

Definition of artificial intelligence system

- **Citation:** CO AIA Section 6-1-1701(2)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R2

Insurance is a consequential-decision domain

- **Citation:** CO AIA Section 6-1-1701(3)(g)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R3

Definition of high-risk AI system with exclusions (a)-(d)

- **Citation:** CO AIA Section 6-1-1701(7)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R4

Substantial factor definition; human review does not negate if based primarily on AI output

- **Citation:** CO AIA Section 6-1-1701(9)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R5

Risk management program must be consistent with NIST AI 100-1 or equivalent AI framework like ISO/IEC 42001

- **Citation:** CO AIA Section 6-1-1703(2)(a)(III)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R6

Impact assessment required for each high-risk AI system; 90-day grace for pre-existing deployments

- **Citation:** CO AIA Section 6-1-1703(2)(b)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R7

Pre-decision consumer notice with five required elements

- **Citation:** CO AIA Section 6-1-1703(2)(e)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R8

Consumer right to correct incorrect personal data used by high-risk AI system

- **Citation:** CO AIA Section 6-1-1703(2)(f)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R9

Meaningful opportunity to appeal consequential decision involving high-risk AI system

- **Citation:** CO AIA Section 6-1-1703(2)(g)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R10

Website disclosure summarizing high-risk AI systems and algorithmic discrimination risk management

- **Citation:** CO AIA Section 6-1-1703(2)(d)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R11

Small deployer exception: fewer than 50 employees AND does not use own data to train

- **Citation:** CO AIA Section 6-1-1703(6)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R12

Annual review of high-risk AI system deployment for algorithmic discrimination

- **Citation:** CO AIA Section 6-1-1703(2)(c)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R13

Enforcement: deceptive trade practice, AG exclusive authority, up to $20,000 per violation

- **Citation:** CO AIA Section 6-1-1706
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R14

Exclusion: system performs a narrow procedural task

- **Citation:** CO AIA Section 6-1-1701(7)(a)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R15

Exclusion: system detects decision-making patterns without replacing or influencing human assessment

- **Citation:** CO AIA Section 6-1-1701(7)(c)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R16

Exclusion: system performs a preparatory task to an assessment

- **Citation:** CO AIA Section 6-1-1701(7)(d)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R17

Notification to AG and consumers within 90 days if algorithmic discrimination discovered

- **Citation:** CO AIA Section 6-1-1704
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R18

Deployer duty of reasonable care to protect consumers from algorithmic discrimination risks

- **Citation:** CO AIA Section 6-1-1703(1)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R19

Impact assessment must include six specified elements (a)-(f)

- **Citation:** CO AIA Section 6-1-1701(8)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

## Applications (13)

### A1

DocParse copies data fields from claim forms without evaluating claims. It does not make or substantially factor into any consequential decision. It falls within the narrow procedural task exclusion at Section 6-1-1701(7)(a). DocParse is NOT a high-risk AI system.

- **Rule ref:** R3
- **Fact refs:** F4
- **Issue ref:** I1
- **Result:** satisfied

### A2

PatternWatch runs on closed claims, detects adjuster payout pattern deviations, and reports to managers. It has no effect on any individual claim. It falls within the exclusion at Section 6-1-1701(7)(c) for systems that detect decision-making patterns without replacing or influencing human assessment. PatternWatch is NOT a high-risk AI system.

- **Rule ref:** R15
- **Fact refs:** F5
- **Issue ref:** I2
- **Result:** satisfied

### A3

ClaimGuard assigns fraud scores to open insurance claims and routes high-scoring claims to special handling where 81% are denied and 37% are non-renewed. Insurance is a consequential-decision domain under Section 6-1-1701(3)(g). ClaimGuard makes or is a substantial factor in making consequential decisions. No exclusion applies: it is not a narrow procedural task (it performs evaluative scoring), does not merely detect patterns (it actively routes claims), and is not merely preparatory (its output effectively determines outcomes given the 81% denial rate and 6% override rate). ClaimGuard IS a high-risk AI system.

- **Rule ref:** R3
- **Fact refs:** F6, F7, F8, F17
- **Issue ref:** I3
- **Result:** violated

### A4

ClaimGuard materially contributes to consequential decisions: 94% of its routing decisions stand (only 6% overridden), and 81% of routed claims are denied. Under Section 6-1-1701(9), human review does not negate the substantial-factor finding if based primarily on AI output. A 6% override rate demonstrates near-total reliance on ClaimGuard, meaning human review is based primarily on the AI output. ClaimGuard is a substantial factor.

- **Rule ref:** R4
- **Fact refs:** F6, F7, F9
- **Issue ref:** I4
- **Result:** violated

### A5

ISO/IEC 27001 is an information security standard, not an AI risk management framework. Section 6-1-1703(2)(a)(III) requires consistency with NIST AI 100-1 or a substantially equivalent AI framework such as ISO/IEC 42001. The statute and authoritative notes explicitly state ISO/IEC 27001 is NOT sufficient. The risk management program is non-compliant.

- **Rule ref:** R5
- **Fact refs:** F10
- **Issue ref:** I5
- **Result:** violated

### A6

Impact assessment was completed only for DocParse (not high-risk). No impact assessment exists for ClaimGuard (which IS high-risk). Section 6-1-1703(2)(b) requires an impact assessment for each high-risk AI system. For pre-existing deployments, the assessment must be completed within 90 days of June 30, 2026 (by September 28, 2026). Currently non-compliant.

- **Rule ref:** R6
- **Fact refs:** F11
- **Issue ref:** I6
- **Result:** violated

### A7

Denial and non-renewal letters do not mention any AI system. Section 6-1-1703(2)(e) requires pre-decision notice with five specific elements including that a high-risk AI system is being used, its purpose, contact info, plain-language description, and instructions for accessing the website statement. No such notice is provided. Non-compliant.

- **Rule ref:** R7
- **Fact refs:** F13
- **Issue ref:** I6
- **Result:** violated

### A8

There is no process for correcting data that ClaimGuard used. Section 6-1-1703(2)(f) requires the deployer to provide consumers an opportunity to correct incorrect personal data processed by the high-risk AI system. Non-compliant.

- **Rule ref:** R8
- **Fact refs:** F15
- **Issue ref:** I6
- **Result:** violated

### A9

A general claims-appeal process exists where a second adjuster reviews without seeing the ClaimGuard score, which provides some independent review. However, consumers are not informed of AI involvement (notice failure), so they cannot meaningfully frame an appeal around the AI system. The appeal right is partially but not fully compliant with the meaningful opportunity to appeal requirement.

- **Rule ref:** R9
- **Fact refs:** F14, F13
- **Issue ref:** I6
- **Result:** partial

### A10

The website states only that Cimarron Peak uses technology to process claims efficiently. This does not identify ClaimGuard as a high-risk AI system or describe how algorithmic discrimination risks are managed. Section 6-1-1703(2)(d) requires a clear, readily accessible statement summarizing deployed high-risk AI systems and discrimination risk management. Non-compliant.

- **Rule ref:** R10
- **Fact refs:** F12
- **Issue ref:** I6
- **Result:** violated

### A11

Cimarron Peak has 420 employees, far exceeding the 50-employee threshold in Section 6-1-1703(6)(a). The small deployer exception requires BOTH fewer than 50 employees AND not using own data to train. The first condition alone disqualifies Cimarron Peak. No exception applies.

- **Rule ref:** R11
- **Fact refs:** F2
- **Issue ref:** I6
- **Result:** violated

### A12

General counsel argues ClaimGuard merely routes claims (preparatory task). However, the preparatory task exclusion at Section 6-1-1701(7)(d) does not apply when the system effectively determines outcomes. With 81% denial rate in special handling and only 6% override rate, ClaimGuard is not merely preparatory - it is the primary driver of the consequential decision.

- **Rule ref:** R16
- **Fact refs:** F6, F7, F9
- **Issue ref:** I3
- **Result:** violated

### A13

No evidence of annual review of ClaimGuard deployment for algorithmic discrimination. Section 6-1-1703(2)(c) requires at least annual review. Non-compliant.

- **Rule ref:** R12
- **Fact refs:** F10
- **Issue ref:** I6
- **Result:** violated

## Conclusions (5)

### C1

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A1

### C2

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A2

### C3

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13

### C4

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A5

### C5

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A6, A7, A8, A9, A10, A13

## Obligations (10)

### O1

Implement risk management program consistent with NIST AI 100-1 or ISO/IEC 42001 for ClaimGuard

- **Required by:** R5
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O2

Complete impact assessment for ClaimGuard with all six elements of Section 6-1-1701(8)

- **Required by:** R6
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-09-28

### O3

Update website with clear statement identifying ClaimGuard as high-risk AI system and describing algorithmic discrimination risk management

- **Required by:** R10
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O4

Implement pre-decision consumer notice with all five elements of Section 6-1-1703(2)(e)(I)-(V) for ClaimGuard-processed claims

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O5

Implement data correction process allowing consumers to correct incorrect personal data used by ClaimGuard

- **Required by:** R8
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O6

Enhance appeal process to inform consumers of ClaimGuard involvement and enable meaningful AI-specific appeal

- **Required by:** R9
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O7

Conduct annual review of ClaimGuard deployment for algorithmic discrimination

- **Required by:** R12
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2027-06-30

### O8

Request developer documentation from Graywolf Analytics per Section 6-1-1702(2)(a)-(e)

- **Required by:** R6
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O9

Establish process to notify AG and consumers within 90 days if algorithmic discrimination is discovered

- **Required by:** R17
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O10

Consider proactive discovery and cure of violations with AG notification within 60 days for rebuttable presumption of reasonable care

- **Required by:** R13
- **Status:** safe-harbor
- **Jurisdiction:** Colorado
- **Deadline:** Not specified

## Graph connections (45)

### E1

- **Src:** F4
- **Dst:** I1
- **Type:** triggers
- **Justification:** DocParse functionality raises question of high-risk classification

### E2

- **Src:** F5
- **Dst:** I2
- **Type:** triggers
- **Justification:** PatternWatch functionality raises question of high-risk classification

### E3

- **Src:** F6
- **Dst:** I3
- **Type:** triggers
- **Justification:** ClaimGuard fraud scoring and routing raises question of high-risk classification

### E4

- **Src:** F9
- **Dst:** I4
- **Type:** triggers
- **Justification:** 6% override rate raises question of whether ClaimGuard is a substantial factor

### E5

- **Src:** F10
- **Dst:** I5
- **Type:** triggers
- **Justification:** ISO/IEC 27001 certification raises question of risk management compliance

### E6

- **Src:** R14
- **Dst:** A1
- **Type:** applies-to
- **Justification:** Narrow procedural task exclusion applied to DocParse

### E7

- **Src:** R15
- **Dst:** A2
- **Type:** applies-to
- **Justification:** Pattern detection exclusion applied to PatternWatch

### E8

- **Src:** R3
- **Dst:** A3
- **Type:** applies-to
- **Justification:** High-risk AI system definition applied to ClaimGuard

### E9

- **Src:** R4
- **Dst:** A4
- **Type:** applies-to
- **Justification:** Substantial factor definition applied to ClaimGuard override rate

### E10

- **Src:** R5
- **Dst:** A5
- **Type:** applies-to
- **Justification:** Risk management framework requirement applied to ISO 27001 certification

### E11

- **Src:** R6
- **Dst:** A6
- **Type:** applies-to
- **Justification:** Impact assessment requirement applied to ClaimGuard

### E12

- **Src:** R7
- **Dst:** A7
- **Type:** applies-to
- **Justification:** Consumer notice requirement applied to denial/non-renewal letters

### E13

- **Src:** R8
- **Dst:** A8
- **Type:** applies-to
- **Justification:** Data correction requirement applied to absence of correction process

### E14

- **Src:** R9
- **Dst:** A9
- **Type:** applies-to
- **Justification:** Appeal requirement applied to existing claims-appeal process

### E15

- **Src:** R10
- **Dst:** A10
- **Type:** applies-to
- **Justification:** Website disclosure requirement applied to current website statement

### E16

- **Src:** R11
- **Dst:** A11
- **Type:** applies-to
- **Justification:** Small deployer exception applied to 420-employee company

### E17

- **Src:** A1
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** DocParse excluded from high-risk classification; compliant

### E18

- **Src:** A2
- **Dst:** C2
- **Type:** satisfies-element
- **Justification:** PatternWatch excluded from high-risk classification; compliant

### E19

- **Src:** A3
- **Dst:** C3
- **Type:** fails-element
- **Justification:** ClaimGuard is high-risk; multiple deployer obligations not met

### E20

- **Src:** A4
- **Dst:** C3
- **Type:** fails-element
- **Justification:** ClaimGuard is substantial factor despite override; obligations triggered

### E21

- **Src:** A5
- **Dst:** C4
- **Type:** fails-element
- **Justification:** ISO 27001 does not satisfy AI risk management requirement

### E22

- **Src:** A6
- **Dst:** C5
- **Type:** fails-element
- **Justification:** No impact assessment for ClaimGuard

### E23

- **Src:** A7
- **Dst:** C5
- **Type:** fails-element
- **Justification:** No consumer notice provided

### E24

- **Src:** A8
- **Dst:** C5
- **Type:** fails-element
- **Justification:** No data correction process

### E25

- **Src:** A9
- **Dst:** C5
- **Type:** fails-element
- **Justification:** Appeal process only partially compliant

### E26

- **Src:** A10
- **Dst:** C5
- **Type:** fails-element
- **Justification:** Website disclosure insufficient

### E27

- **Src:** R5
- **Dst:** O1
- **Type:** triggers
- **Justification:** Non-compliant risk management program triggers obligation to implement NIST AI 100-1 or equivalent

### E28

- **Src:** R6
- **Dst:** O2
- **Type:** triggers
- **Justification:** Missing impact assessment triggers obligation with 90-day grace period

### E29

- **Src:** R10
- **Dst:** O3
- **Type:** triggers
- **Justification:** Insufficient website disclosure triggers obligation to update

### E30

- **Src:** R7
- **Dst:** O4
- **Type:** triggers
- **Justification:** Missing consumer notice triggers obligation to implement pre-decision notice

### E31

- **Src:** R8
- **Dst:** O5
- **Type:** triggers
- **Justification:** Missing data correction process triggers obligation to implement

### E32

- **Src:** R9
- **Dst:** O6
- **Type:** triggers
- **Justification:** Partially compliant appeal process triggers obligation to enhance

### E33

- **Src:** R12
- **Dst:** O7
- **Type:** triggers
- **Justification:** Annual review requirement triggers ongoing obligation

### E34

- **Src:** F7
- **Dst:** I3
- **Type:** supports
- **Justification:** 81% denial rate in special handling supports finding that ClaimGuard drives consequential decisions

### E35

- **Src:** F8
- **Dst:** I3
- **Type:** supports
- **Justification:** 37% non-renewal rate supports finding of cascading consequential decisions

### E36

- **Src:** F17
- **Dst:** I3
- **Type:** supports
- **Justification:** Insurance as consequential-decision domain supports high-risk classification

### E37

- **Src:** R16
- **Dst:** A12
- **Type:** applies-to
- **Justification:** Preparatory task exclusion analyzed and rejected for ClaimGuard

### E38

- **Src:** A12
- **Dst:** C3
- **Type:** fails-element
- **Justification:** Preparatory task exclusion does not apply to ClaimGuard

### E39

- **Src:** A11
- **Dst:** C3
- **Type:** fails-element
- **Justification:** Small deployer exception inapplicable; all obligations apply

### E40

- **Src:** A13
- **Dst:** C5
- **Type:** fails-element
- **Justification:** No annual review conducted for ClaimGuard

### E41

- **Src:** F1
- **Dst:** I3
- **Type:** triggers
- **Justification:** Colorado domicile establishes jurisdiction under CO AIA

### E42

- **Src:** F2
- **Dst:** I6
- **Type:** triggers
- **Justification:** 420 employees disqualifies small deployer exception

### E43

- **Src:** R13
- **Dst:** O10
- **Type:** triggers
- **Justification:** Enforcement provisions create safe-harbor opportunity through proactive cure

### E44

- **Src:** R17
- **Dst:** O9
- **Type:** triggers
- **Justification:** Algorithmic discrimination notification obligation triggered by deployment of high-risk system

### E45

- **Src:** F16
- **Dst:** I3
- **Type:** contradicts
- **Justification:** General counsel conclusion that no tool is high-risk contradicts statutory analysis of ClaimGuard
