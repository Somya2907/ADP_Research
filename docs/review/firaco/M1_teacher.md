# M1 — LoanScore Denver — teacher FIRACO reasoning

Unverified model output for legal review. Citations, facts, applications, and obligations may be incorrect. Text and node IDs below are preserved from the saved reference graph.

[Read case](../../../data/cases/M1_loanscore_denver.md) · [Review brief](../../PROF_PHILIPP_REVIEW.md)

Teacher: claude-opus-4-6. Source: data/outputs/graphs/M1_reference.json.

Source SHA-256: `82a3a2fc32ee642241f5854c3b2ec2d3b25148743db70080d3c001936f8551b6`.

## Facts (15)

### F1

FinSpark is Colorado-chartered, headquartered in Denver, with 240 FTEs

- **Polarity:** present
- **Support quote:** Colorado-chartered online lender headquartered in Denver with 240 full-time employees

### F2

LoanScore is an AI credit underwriting model producing binary approval/denial and interest rate tier

- **Polarity:** present
- **Support quote:** AI-based credit underwriting model called LoanScore... returns a binary approval/denial decision along with a recommended interest rate tier

### F3

LoanScore is used for financial/lending service decisions

- **Polarity:** present
- **Support quote:** AI-based credit underwriting model

### F4

Sub-$15K loans (73% of applications) are fully automated with no human review

- **Polarity:** present
- **Support quote:** For loan applications under $15,000: LoanScore fully automates the approval/denial decision with no human review

### F5

For $15K+ loans, human officer agrees with AI recommendation 94% of the time

- **Polarity:** present
- **Support quote:** human loan officer approves the AI recommendation without modification in 94% of cases

### F6

FinSpark licensed LoanScore from DataCredit Solutions; did not develop or substantially modify it

- **Polarity:** present
- **Support quote:** FinSpark licensed LoanScore from DataCredit Solutions, a Delaware-based AI developer

### F7

DataCredit has provided no model card, dataset documentation, training data summaries, or impact assessment documentation

- **Polarity:** present
- **Support quote:** DataCredit has not provided FinSpark with any model card, dataset documentation, training data summaries, or impact assessment documentation

### F8

FinSpark has never conducted an impact assessment of LoanScore

- **Polarity:** present
- **Support quote:** FinSpark has never conducted its own impact assessment of LoanScore

### F9

FinSpark has no written risk management policy or program for AI deployment

- **Polarity:** present
- **Support quote:** FinSpark does not have a written risk management policy or program governing AI deployment

### F10

FinSpark does not notify loan applicants that AI is used in underwriting

- **Polarity:** present
- **Support quote:** FinSpark does not notify loan applicants that an AI system is used in the underwriting decision

### F11

No mechanism exists for applicants to correct personal data processed by AI

- **Polarity:** present
- **Support quote:** There is no mechanism for applicants to correct personal data processed by the AI

### F12

No mechanism exists for applicants to appeal AI-involved adverse decisions

- **Polarity:** present
- **Support quote:** no mechanism for applicants to... appeal an adverse lending decision through a process that accounts for AI involvement

### F13

CEO memo (Oct 2025) defers compliance to Q2 2026; no action taken as of April 2026

- **Polarity:** present
- **Support quote:** Because the Colorado AI Act has been delayed to June 30, 2026, we have time to sort this out. Lets revisit in Q2 2026

### F14

FinSpark has 240 full-time employees, exceeding the 50-employee small deployer threshold

- **Polarity:** present
- **Support quote:** 240 full-time employees

### F15

Current date is April 16, 2026; CO AIA effective June 30, 2026 (75 days away)

- **Polarity:** present
- **Support quote:** Not specified

## Issues (7)

### I1

Is LoanScore a high-risk AI system under CO AIA Section 6-1-1701(7)?

- **Status:** dispositive

### I2

Is FinSpark a developer, deployer, or both under CO AIA?

- **Status:** dispositive

### I3

What specific deployer obligations apply to FinSpark under Section 6-1-1703?

- **Status:** dispositive

### I4

Does the 94% human agreement rate affect the substantial factor analysis under Section 6-1-1701(9)?

- **Status:** dispositive

### I5

Does DataCredits failure to provide documentation relieve FinSpark of deployer obligations?

- **Status:** collateral

### I6

Does the small deployer exception under Section 6-1-1703(6) apply to FinSpark?

- **Status:** collateral

### I7

What must FinSpark do to achieve compliance by June 30, 2026?

- **Status:** dispositive

## Rules (19)

### R1

Definition of artificial intelligence system

- **Citation:** CO AIA Section 6-1-1701(2)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R2

Consequential decision includes financial or lending service

- **Citation:** CO AIA Section 6-1-1701(3)(c)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R3

High-risk AI system definition: makes or is substantial factor in consequential decision

- **Citation:** CO AIA Section 6-1-1701(7)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R4

Substantial factor definition: human review based primarily on AI output does not negate

- **Citation:** CO AIA Section 6-1-1701(9)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R5

Deployer definition: person doing business in state that deploys high-risk AI system

- **Citation:** CO AIA Section 6-1-1701(5)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R6

Developer definition: person that develops or substantially modifies AI system

- **Citation:** CO AIA Section 6-1-1701(6)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R7

Deployer duty of reasonable care against algorithmic discrimination

- **Citation:** CO AIA Section 6-1-1703(1)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R8

Deployer must implement risk management policy consistent with NIST AI RMF or equivalent

- **Citation:** CO AIA Section 6-1-1703(2)(a)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R9

Deployer must complete impact assessment prior to deployment or within 90 days for pre-existing systems

- **Citation:** CO AIA Section 6-1-1703(2)(b)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R10

Deployer must conduct annual review for algorithmic discrimination

- **Citation:** CO AIA Section 6-1-1703(2)(c)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R11

Deployer must publish website statement on high-risk AI systems and discrimination risk management

- **Citation:** CO AIA Section 6-1-1703(2)(d)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R12

Deployer must notify consumers before AI-assisted consequential decision

- **Citation:** CO AIA Section 6-1-1703(2)(e)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R13

Deployer must provide data correction opportunity to consumers

- **Citation:** CO AIA Section 6-1-1703(2)(f)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R14

Deployer must provide meaningful appeal opportunity for AI-involved consequential decisions

- **Citation:** CO AIA Section 6-1-1703(2)(g)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R15

Small deployer exception: fewer than 50 FTEs AND does not use own data to train

- **Citation:** CO AIA Section 6-1-1703(6)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R16

Developer must provide documentation on limitations, training data, uses, and monitoring guidance

- **Citation:** CO AIA Section 6-1-1702(2)
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

Enforcement: deceptive trade practice, AG exclusive authority, up to $20K per violation

- **Citation:** CO AIA Section 6-1-1706
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R19

Impact assessment must include six specified elements

- **Citation:** CO AIA Section 6-1-1701(8)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

## Applications (17)

### A1

LoanScore is a machine-based system that processes financial inputs and produces outputs (approval/denial, interest rate tier) influencing real environments. Satisfies AI system definition.

- **Rule ref:** R1
- **Fact refs:** F2
- **Issue ref:** I1
- **Result:** satisfied

### A2

Credit underwriting decisions on loan approval/denial and interest rate terms have material legal or similarly significant effect on provision, denial, cost, or terms of a financial or lending service under Section 6-1-1701(3)(c).

- **Rule ref:** R2
- **Fact refs:** F2, F3
- **Issue ref:** I1
- **Result:** satisfied

### A3

For sub-$15K loans (73% of volume), LoanScore makes the consequential decision with zero human review. The system directly makes the decision, satisfying the high-risk threshold.

- **Rule ref:** R3
- **Fact refs:** F4
- **Issue ref:** I1
- **Result:** satisfied

### A4

The 94% agreement rate demonstrates human review is based primarily on AI output. Section 6-1-1701(9) explicitly provides that such human review does not negate substantial factor finding. LoanScore is a substantial factor in $15K+ decisions.

- **Rule ref:** R4
- **Fact refs:** F5
- **Issue ref:** I4
- **Result:** satisfied

### A5

FinSpark does business in Colorado (Colorado-chartered, Denver HQ) and deploys LoanScore, a high-risk AI system. FinSpark is a deployer.

- **Rule ref:** R5
- **Fact refs:** F1, F2, F6
- **Issue ref:** I2
- **Result:** satisfied

### A6

FinSpark licensed LoanScore from DataCredit and did not develop or substantially modify it. FinSpark is NOT a developer. DataCredit is the developer.

- **Rule ref:** R6
- **Fact refs:** F6
- **Issue ref:** I2
- **Result:** satisfied

### A7

FinSpark has no written risk management policy or program, let alone one consistent with NIST AI RMF 1.0 or ISO/IEC 42001. Complete non-compliance with Section 6-1-1703(2)(a).

- **Rule ref:** R8
- **Fact refs:** F9
- **Issue ref:** I3
- **Result:** violated

### A8

FinSpark has never conducted an impact assessment. For pre-existing deployments, the 90-day grace period runs from June 30, 2026 to September 28, 2026. While not yet technically in violation, no preparatory work has begun.

- **Rule ref:** R9
- **Fact refs:** F8
- **Issue ref:** I3
- **Result:** violated

### A9

FinSpark has no public website statement summarizing its high-risk AI systems or algorithmic discrimination risk management. Complete non-compliance with Section 6-1-1703(2)(d).

- **Rule ref:** R11
- **Fact refs:** F10
- **Issue ref:** I3
- **Result:** violated

### A10

FinSpark provides no notice to loan applicants that AI is used in underwriting decisions. Fails all five sub-requirements of Section 6-1-1703(2)(e).

- **Rule ref:** R12
- **Fact refs:** F10
- **Issue ref:** I3
- **Result:** violated

### A11

No mechanism exists for applicants to correct incorrect personal data processed by LoanScore. Complete non-compliance with Section 6-1-1703(2)(f).

- **Rule ref:** R13
- **Fact refs:** F11
- **Issue ref:** I3
- **Result:** violated

### A12

No mechanism exists for applicants to appeal adverse AI-involved lending decisions. Complete non-compliance with Section 6-1-1703(2)(g).

- **Rule ref:** R14
- **Fact refs:** F12
- **Issue ref:** I3
- **Result:** violated

### A13

The totality of FinSparks failures — no risk management, no impact assessment, no notice, no correction mechanism, no appeal process — demonstrates failure to use reasonable care to protect consumers from algorithmic discrimination risks.

- **Rule ref:** R7
- **Fact refs:** F8, F9, F10, F11, F12
- **Issue ref:** I3
- **Result:** violated

### A14

FinSpark has 240 FTEs, far exceeding the 50-employee threshold. Condition (a) of the small deployer exception is not met. The exception is inapplicable regardless of condition (b).

- **Rule ref:** R15
- **Fact refs:** F14
- **Issue ref:** I6
- **Result:** satisfied

### A15

DataCredit has failed to provide any of the five categories of documentation required by Section 6-1-1702(2). However, this is DataCredits violation, not FinSparks. FinSparks deployer obligations remain independently binding.

- **Rule ref:** R16
- **Fact refs:** F7
- **Issue ref:** I5
- **Result:** violated

### A16

FinSpark has conducted no annual review of LoanScore for algorithmic discrimination. While the first annual review deadline is June 30, 2027, no review infrastructure exists.

- **Rule ref:** R10
- **Fact refs:** F8
- **Issue ref:** I3
- **Result:** violated

### A17

Without developer documentation and having conducted no independent analysis, FinSpark cannot complete the six required elements of an impact assessment, particularly training data categories and known limitations.

- **Rule ref:** R19
- **Fact refs:** F7, F8
- **Issue ref:** I3
- **Result:** violated

## Conclusions (4)

### C1

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A1, A2, A3, A4

### C2

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A7, A8, A9, A10, A11, A12, A13

### C3

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A14

### C4

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A15, A17

## Obligations (11)

### O1

Implement risk management policy and program consistent with NIST AI RMF 1.0 or ISO/IEC 42001

- **Required by:** R8
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O2

Complete impact assessment of LoanScore with all six elements of Section 6-1-1701(8)

- **Required by:** R9
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-09-28

### O3

Conduct annual deployment review for algorithmic discrimination

- **Required by:** R10
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2027-06-30

### O4

Publish website statement summarizing high-risk AI systems and discrimination risk management

- **Required by:** R11
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O5

Implement consumer notice system with all five sub-elements before each AI-assisted lending decision

- **Required by:** R12
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O6

Implement mechanism for applicants to correct incorrect personal data processed by LoanScore

- **Required by:** R13
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O7

Implement meaningful appeal process for adverse AI-involved lending decisions

- **Required by:** R14
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O8

Demand and obtain developer documentation from DataCredit per Section 6-1-1702(2) requirements

- **Required by:** R16
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** Not specified

### O9

Establish reasonable care posture through totality of compliance measures to support rebuttable presumption

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O10

Establish internal protocol for detecting and reporting algorithmic discrimination to AG and consumers within 90 days

- **Required by:** R17
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O11

Reassess human review protocols for $15K+ loans to ensure meaningful independent review

- **Required by:** R4
- **Status:** recommended
- **Jurisdiction:** Colorado
- **Deadline:** Not specified

## Graph connections (53)

### E1

- **Src:** F2
- **Dst:** I1
- **Type:** triggers
- **Justification:** LoanScore AI system raises question of high-risk classification

### E2

- **Src:** F3
- **Dst:** I1
- **Type:** triggers
- **Justification:** Lending use case implicates consequential decision definition

### E3

- **Src:** F4
- **Dst:** I1
- **Type:** triggers
- **Justification:** Full automation for 73% of decisions implicates high-risk status

### E4

- **Src:** F5
- **Dst:** I4
- **Type:** triggers
- **Justification:** 94% agreement rate raises substantial factor question

### E5

- **Src:** F6
- **Dst:** I2
- **Type:** triggers
- **Justification:** Licensing relationship raises developer vs deployer classification

### E6

- **Src:** F7
- **Dst:** I5
- **Type:** triggers
- **Justification:** Developer documentation failure raises question of deployer obligation scope

### E7

- **Src:** F14
- **Dst:** I6
- **Type:** triggers
- **Justification:** 240 FTEs raises question of small deployer exception applicability

### E8

- **Src:** R1
- **Dst:** A1
- **Type:** applies-to
- **Justification:** AI system definition applied to LoanScore

### E9

- **Src:** R2
- **Dst:** A2
- **Type:** applies-to
- **Justification:** Consequential decision definition applied to credit underwriting

### E10

- **Src:** R3
- **Dst:** A3
- **Type:** applies-to
- **Justification:** High-risk AI definition applied to fully automated lending decisions

### E11

- **Src:** R4
- **Dst:** A4
- **Type:** applies-to
- **Justification:** Substantial factor definition applied to 94% agreement rate scenario

### E12

- **Src:** R5
- **Dst:** A5
- **Type:** applies-to
- **Justification:** Deployer definition applied to FinSpark

### E13

- **Src:** R6
- **Dst:** A6
- **Type:** applies-to
- **Justification:** Developer definition applied to FinSpark licensing relationship

### E14

- **Src:** R8
- **Dst:** A7
- **Type:** applies-to
- **Justification:** Risk management obligation applied to FinSparks absence of policy

### E15

- **Src:** R9
- **Dst:** A8
- **Type:** applies-to
- **Justification:** Impact assessment obligation applied to FinSparks failure to assess

### E16

- **Src:** R11
- **Dst:** A9
- **Type:** applies-to
- **Justification:** Public statement obligation applied to FinSparks website

### E17

- **Src:** R12
- **Dst:** A10
- **Type:** applies-to
- **Justification:** Consumer notice obligation applied to FinSparks lending process

### E18

- **Src:** R13
- **Dst:** A11
- **Type:** applies-to
- **Justification:** Data correction obligation applied to FinSparks lack of mechanism

### E19

- **Src:** R14
- **Dst:** A12
- **Type:** applies-to
- **Justification:** Appeal right obligation applied to FinSparks lack of process

### E20

- **Src:** R7
- **Dst:** A13
- **Type:** applies-to
- **Justification:** Reasonable care duty applied to totality of FinSparks failures

### E21

- **Src:** R15
- **Dst:** A14
- **Type:** applies-to
- **Justification:** Small deployer exception applied to FinSparks 240 FTEs

### E22

- **Src:** R16
- **Dst:** A15
- **Type:** applies-to
- **Justification:** Developer documentation obligation applied to DataCredits failure

### E23

- **Src:** A1
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** LoanScore meets AI system definition element

### E24

- **Src:** A2
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** Credit underwriting meets consequential decision element

### E25

- **Src:** A3
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** Full automation satisfies makes-decision element for high-risk

### E26

- **Src:** A4
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** 94% rate confirms substantial factor for human-reviewed decisions

### E27

- **Src:** A7
- **Dst:** C2
- **Type:** fails-element
- **Justification:** No risk management policy violates deployer obligation

### E28

- **Src:** A8
- **Dst:** C2
- **Type:** fails-element
- **Justification:** No impact assessment violates deployer obligation

### E29

- **Src:** A9
- **Dst:** C2
- **Type:** fails-element
- **Justification:** No public statement violates deployer obligation

### E30

- **Src:** A10
- **Dst:** C2
- **Type:** fails-element
- **Justification:** No consumer notice violates deployer obligation

### E31

- **Src:** A11
- **Dst:** C2
- **Type:** fails-element
- **Justification:** No data correction mechanism violates deployer obligation

### E32

- **Src:** A12
- **Dst:** C2
- **Type:** fails-element
- **Justification:** No appeal process violates deployer obligation

### E33

- **Src:** A13
- **Dst:** C2
- **Type:** fails-element
- **Justification:** Totality of failures demonstrates lack of reasonable care

### E34

- **Src:** A14
- **Dst:** C3
- **Type:** fails-element
- **Justification:** 240 FTEs disqualifies FinSpark from small deployer exception

### E35

- **Src:** A15
- **Dst:** C4
- **Type:** fails-element
- **Justification:** DataCredits documentation failure impairs but does not excuse FinSparks compliance

### E36

- **Src:** R8
- **Dst:** O1
- **Type:** triggers
- **Justification:** Risk management policy obligation flows from Section 6-1-1703(2)(a)

### E37

- **Src:** R9
- **Dst:** O2
- **Type:** triggers
- **Justification:** Impact assessment obligation flows from Section 6-1-1703(2)(b)

### E38

- **Src:** R10
- **Dst:** O3
- **Type:** triggers
- **Justification:** Annual review obligation flows from Section 6-1-1703(2)(c)

### E39

- **Src:** R11
- **Dst:** O4
- **Type:** triggers
- **Justification:** Public statement obligation flows from Section 6-1-1703(2)(d)

### E40

- **Src:** R12
- **Dst:** O5
- **Type:** triggers
- **Justification:** Consumer notice obligation flows from Section 6-1-1703(2)(e)

### E41

- **Src:** R13
- **Dst:** O6
- **Type:** triggers
- **Justification:** Data correction obligation flows from Section 6-1-1703(2)(f)

### E42

- **Src:** R14
- **Dst:** O7
- **Type:** triggers
- **Justification:** Appeal right obligation flows from Section 6-1-1703(2)(g)

### E43

- **Src:** R16
- **Dst:** O8
- **Type:** triggers
- **Justification:** Developer documentation obligation supports deployer compliance needs

### E44

- **Src:** R7
- **Dst:** O9
- **Type:** triggers
- **Justification:** Reasonable care duty requires comprehensive compliance posture

### E45

- **Src:** R17
- **Dst:** O10
- **Type:** triggers
- **Justification:** Discrimination notification obligation requires internal detection protocol

### E46

- **Src:** R4
- **Dst:** O11
- **Type:** triggers
- **Justification:** Substantial factor analysis suggests strengthening human review independence

### E47

- **Src:** F9
- **Dst:** I3
- **Type:** triggers
- **Justification:** Absence of risk management policy raises deployer obligation compliance question

### E48

- **Src:** F8
- **Dst:** I3
- **Type:** triggers
- **Justification:** Absence of impact assessment raises deployer obligation compliance question

### E49

- **Src:** F10
- **Dst:** I3
- **Type:** triggers
- **Justification:** Absence of consumer notice raises deployer obligation compliance question

### E50

- **Src:** F13
- **Dst:** I7
- **Type:** triggers
- **Justification:** CEO deferral memo raises compliance readiness question

### E51

- **Src:** A17
- **Dst:** C4
- **Type:** fails-element
- **Justification:** Lack of documentation prevents completion of impact assessment elements

### E52

- **Src:** R18
- **Dst:** C2
- **Type:** applies-to
- **Justification:** Enforcement provisions apply to all identified violations

### E53

- **Src:** R19
- **Dst:** A17
- **Type:** applies-to
- **Justification:** Impact assessment content requirements applied to FinSparks documentation gap
