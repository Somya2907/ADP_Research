# H2 — AutoApprove Lending — teacher FIRACO reasoning

Unverified model output for legal review. Citations, facts, applications, and obligations may be incorrect. Text and node IDs below are preserved from the saved reference graph.

[Read case](../../../data/cases/H2_autoapprove_lending.md) · [Review brief](../../PROF_PHILIPP_REVIEW.md)

Teacher: claude-opus-4-6. Source: data/outputs/graphs/H2_reference.json.

Source SHA-256: `c905ceef4efdda9817d811b6859a968a8f9f8b47d6744f06842392316159df87`.

## Facts (18)

### F1

Helix Credit is a Colorado-based fintech lender headquartered in Denver with 310 employees, operating exclusively in Colorado

- **Polarity:** present
- **Support quote:** Colorado-based fintech lender headquartered in Denver with 310 employees

### F2

Helix deployed AutoApprove, an AI-powered underwriting system developed by FinLogic AI

- **Polarity:** present
- **Support quote:** Helix has deployed AutoApprove, an AI-powered underwriting system developed by FinLogic AI

### F3

Stage 1: 62% of applications are auto-approved or auto-denied with no human review

- **Polarity:** present
- **Support quote:** 62% of all applications are decided at Stage 1 (automated, no human involvement)

### F4

Stage 2: 38% of applications routed to human underwriter who receives AI score, AI risk narrative, and raw data

- **Polarity:** present
- **Support quote:** 38% of applications reach Stage 2 (human review)

### F5

Human underwriters agree with AutoApprove direction in 71% of Stage 2 cases

- **Polarity:** present
- **Support quote:** human underwriters agree with the direction implied by AutoApprove score in 71% of cases

### F6

GC memo argues AutoApprove is not a substantial factor due to independent human analysis

- **Polarity:** disputed
- **Support quote:** the 71% agreement rate simply reflects that the AI and our underwriters reach similar conclusions

### F7

Morrison & Partners memo concludes AutoApprove is a substantial factor requiring full deployer obligations

- **Polarity:** present
- **Support quote:** AutoApprove should be considered a substantial factor in making consequential decisions under 6-1-1703

### F8

Helix has NIST AI 100-1 aligned risk management program documented January 2026

- **Polarity:** present
- **Support quote:** AI risk management program aligned with the NIST AI Risk Management Framework (NIST AI 100-1)

### F9

Helix completed impact assessment of AutoApprove in February 2026

- **Polarity:** present
- **Support quote:** Helix completed an impact assessment of AutoApprove in February 2026

### F10

FinLogic AI provided model card and training data summary

- **Polarity:** present
- **Support quote:** FinLogic AI has provided Helix with a model card and training data summary

### F11

Helix has NOT issued consumer notices to loan applicants regarding AI involvement

- **Polarity:** present
- **Support quote:** Helix has NOT issued consumer notices to any loan applicants regarding AI involvement

### F12

Helix has NOT established a data correction process for applicants

- **Polarity:** present
- **Support quote:** Helix has NOT established a documented process for applicants to correct personal data

### F13

Helix has NOT established an appeal process for AI-involved adverse decisions

- **Polarity:** present
- **Support quote:** Helix has NOT established an appeal process that accounts for AI involvement

### F14

AutoApprove is used for lending decisions - financial or lending services

- **Polarity:** present
- **Support quote:** AI-powered underwriting system... $2.1 billion in annual loan originations

### F15

Helix has 310 employees, far exceeding the 50-employee small deployer threshold

- **Polarity:** present
- **Support quote:** 310 employees

### F16

FinLogic AI is San Francisco-based but sells AutoApprove for use in Colorado

- **Polarity:** present
- **Support quote:** FinLogic AI, a San Francisco-based AI developer

### F17

Colorado AI Act effective date is June 30, 2026; analysis date is April 16, 2026

- **Polarity:** present
- **Support quote:** Not specified

### F18

Stage 1 auto-approves above 70th percentile and auto-denies below 40th percentile with no human review

- **Polarity:** present
- **Support quote:** Applications scoring above the 70th percentile are auto-approved; below the 40th percentile are auto-denied. These automated decisions are final

## Issues (7)

### I1

Whether AutoApprove Stage 1 (fully automated) constitutes a high-risk AI system under CO AIA 6-1-1701(7)

- **Status:** dispositive

### I2

Whether AutoApprove Stage 2 (human-reviewed) constitutes a high-risk AI system and whether AI is a substantial factor under 6-1-1701(9)

- **Status:** dispositive

### I3

How to resolve the conflict between GC memo and Morrison memo - authority hierarchy relative to statutory text

- **Status:** dispositive

### I4

Whether Helix is a deployer, developer, or both under CO AIA

- **Status:** dispositive

### I5

Complete inventory of compliance gaps and required remedial actions by June 30, 2026

- **Status:** dispositive

### I6

Whether FinLogic AI has separate developer obligations and whether current documentation is sufficient

- **Status:** dispositive

### I7

Whether Helix qualifies for the small deployer exception under 6-1-1703(6)

- **Status:** collateral

## Rules (20)

### R1

Definition of AI system: machine-based system processing inputs to produce outputs such as predictions, recommendations, decisions

- **Citation:** CO AIA 6-1-1701(2)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R2

Consequential decision includes material legal or significant effect on provision or denial of financial or lending services

- **Citation:** CO AIA 6-1-1701(3)(c)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R3

High-risk AI system: AI system that when deployed makes or is a substantial factor in making a consequential decision

- **Citation:** CO AIA 6-1-1701(7)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R4

Substantial factor: materially contributed to consequential decision; human review does not negate if based primarily on AI output

- **Citation:** CO AIA 6-1-1701(9)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R5

Deployer: person doing business in the state that deploys a high-risk AI system

- **Citation:** CO AIA 6-1-1701(5)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R6

Developer: person doing business in the state that develops or substantially modifies an AI system intended or known to be used as high-risk

- **Citation:** CO AIA 6-1-1701(6)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R7

Deployer must implement risk management policy consistent with NIST AI 100-1 or substantially equivalent framework

- **Citation:** CO AIA 6-1-1703(2)(a)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R8

Deployer must complete impact assessment prior to deployment or within 90 days for pre-existing systems, annually thereafter

- **Citation:** CO AIA 6-1-1703(2)(b)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R9

Deployer must review deployment at least annually to ensure no algorithmic discrimination

- **Citation:** CO AIA 6-1-1703(2)(c)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R10

Deployer must publish website statement summarizing high-risk AI systems and discrimination risk management

- **Citation:** CO AIA 6-1-1703(2)(d)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R11

Deployer must provide pre-decision consumer notice of AI use, purpose, contact info, description, and website statement access

- **Citation:** CO AIA 6-1-1703(2)(e)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R12

Deployer must provide consumer opportunity to correct incorrect personal data processed by AI system

- **Citation:** CO AIA 6-1-1703(2)(f)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R13

Deployer must provide consumer meaningful opportunity to appeal consequential decision where AI was substantial factor

- **Citation:** CO AIA 6-1-1703(2)(g)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R14

Small deployer exception: fewer than 50 employees AND does not use own data to train; both conditions required

- **Citation:** CO AIA 6-1-1703(6)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R15

Developer must provide deployer documentation on limitations, training data, intended uses, monitoring guidance, and impact assessment support

- **Citation:** CO AIA 6-1-1702(2)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R16

Developer must publish public statement summarizing high-risk AI systems developed or substantially modified

- **Citation:** CO AIA 6-1-1702(3)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R17

Deployer or developer must notify AG and affected consumers within 90 days of discovering algorithmic discrimination

- **Citation:** CO AIA 6-1-1704
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R18

Violations are deceptive trade practices; AG exclusive enforcement; up to $20,000 per violation; rebuttable presumption for self-discovery and cure within 60 days

- **Citation:** CO AIA 6-1-1706
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R19

Deployer rebuttable presumption of reasonable care if complied with 6-1-1703 and AG requirements

- **Citation:** CO AIA 6-1-1703(3)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R20

Impact assessment must include purpose, discrimination risk analysis, training data categories, output description, known limitations, and oversight processes

- **Citation:** CO AIA 6-1-1701(8)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

## Applications (16)

### A1

AutoApprove is a machine-based system that processes loan application inputs and produces credit-risk scores, risk narratives, and approval/denial decisions - outputs that influence real environments. Squarely meets the AI system definition.

- **Rule ref:** R1
- **Fact refs:** F2
- **Issue ref:** I1
- **Result:** satisfied

### A2

Loan approval/denial decisions have material legal or similarly significant effect on provision or denial of financial or lending services under 6-1-1701(3)(c). AutoApprove decisions directly determine whether consumers receive loans.

- **Rule ref:** R2
- **Fact refs:** F14, F18
- **Issue ref:** I1
- **Result:** satisfied

### A3

In Stage 1, AutoApprove directly makes the consequential decision - auto-approving or auto-denying with no human review. The AI system makes the decision, not merely contributes to it. No exceptions under 6-1-1701(7)(a)-(d) apply: it is not a narrow procedural task, does not improve prior human activity, does not merely detect patterns, and is not preparatory.

- **Rule ref:** R3
- **Fact refs:** F3, F18
- **Issue ref:** I1
- **Result:** satisfied

### A4

In Stage 2, AutoApprove is a substantial factor: the underwriter receives the AI risk score and AI-generated risk narrative as 2 of 3 inputs. The 71% agreement rate indicates material contribution. Under 6-1-1701(9), human review does not negate substantial factor status when review is based primarily on AI output. The AI narrative frames the analysis by identifying key factors, creating anchoring effects. The anti-rubber-stamping provision directly applies.

- **Rule ref:** R4
- **Fact refs:** F4, F5
- **Issue ref:** I2
- **Result:** satisfied

### A5

Helix is doing business in Colorado (headquartered in Denver, operates exclusively in Colorado) and deploys AutoApprove, a high-risk AI system. Helix is unambiguously a deployer under 6-1-1701(5).

- **Rule ref:** R5
- **Fact refs:** F1, F2
- **Issue ref:** I4
- **Result:** satisfied

### A6

Helix did not develop or substantially modify AutoApprove - FinLogic AI developed it. No facts indicate Helix retrained or substantially modified the model. Helix is not a developer under 6-1-1701(6).

- **Rule ref:** R6
- **Fact refs:** F1, F2
- **Issue ref:** I4
- **Result:** satisfied

### A7

The small deployer exception requires BOTH fewer than 50 employees AND not using own data to train. Helix has 310 employees, failing condition (a). The exception does not apply regardless of condition (b). All deployer obligations apply in full.

- **Rule ref:** R14
- **Fact refs:** F15
- **Issue ref:** I7
- **Result:** violated

### A8

Helix has implemented a risk management program aligned with NIST AI 100-1, documented in January 2026. This satisfies 6-1-1703(2)(a)(III) which requires consistency with NIST AI RMF or substantially equivalent framework.

- **Rule ref:** R7
- **Fact refs:** F8
- **Issue ref:** I5
- **Result:** satisfied

### A9

Helix completed an impact assessment in February 2026. For systems deployed before June 30, 2026, the assessment must be completed within 90 days after the effective date (by September 28, 2026). The February 2026 assessment satisfies this timeline, though content should be verified against 6-1-1701(8) requirements.

- **Rule ref:** R8
- **Fact refs:** F9
- **Issue ref:** I5
- **Result:** satisfied

### A10

Helix has NOT issued consumer notices to loan applicants regarding AI involvement. Section 6-1-1703(2)(e) requires pre-decision notice of AI use, purpose, contact info, plain-language description, and website statement access instructions. This is a critical compliance gap.

- **Rule ref:** R11
- **Fact refs:** F11
- **Issue ref:** I5
- **Result:** violated

### A11

Helix has NOT established a data correction process. Section 6-1-1703(2)(f) requires providing consumers opportunity to correct incorrect personal data processed by the AI system. This is a compliance gap.

- **Rule ref:** R12
- **Fact refs:** F12
- **Issue ref:** I5
- **Result:** violated

### A12

Helix has NOT established an appeal process. Section 6-1-1703(2)(g) requires providing consumers a meaningful opportunity to appeal consequential decisions where AI was a substantial factor. Particularly critical for Stage 1 auto-denials. This is a compliance gap.

- **Rule ref:** R13
- **Fact refs:** F13
- **Issue ref:** I5
- **Result:** violated

### A13

No facts indicate Helix has published a website statement summarizing its high-risk AI systems and algorithmic discrimination risk management as required by 6-1-1703(2)(d). This is a compliance gap.

- **Rule ref:** R10
- **Fact refs:** F11
- **Issue ref:** I5
- **Result:** violated

### A14

FinLogic provided a model card and training data summary, likely covering 6-1-1702(2)(b) training data description and possibly (c) intended uses. However, no indication FinLogic provided: (a) algorithmic discrimination limitation documentation, (d) human monitoring guidance for consequential decisions, or (e) additional impact assessment support materials. Documentation is necessary but insufficient.

- **Rule ref:** R15
- **Fact refs:** F10, F16
- **Issue ref:** I6
- **Result:** partial

### A15

No facts indicate whether FinLogic has published a public use case inventory as required by 6-1-1702(3). FinLogic must do so if it is doing business in Colorado. The doing-business-in-state question for a San Francisco company selling to Colorado deployers requires further factual analysis.

- **Rule ref:** R16
- **Fact refs:** F16
- **Issue ref:** I6
- **Result:** requires-fact

### A16

The statutory text of 6-1-1701(9) controls over both memos. The GC memo fails to engage with the anti-rubber-stamping provision and ignores that 62% of decisions are fully automated. The Morrison memo correctly applies the statute. Neither memo is binding authority - the statute is the supreme authority. The GC memo is legally deficient; the Morrison memo is persuasive because it correctly interprets binding statutory text.

- **Rule ref:** R4
- **Fact refs:** F6, F7
- **Issue ref:** I3
- **Result:** satisfied

## Conclusions (6)

### C1

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A3

### C2

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A4

### C3

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A10, A11, A12, A13

### C4

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A8, A9

### C5

- **Determination:** conditional
- **Confidence:** medium
- **Support refs:** A14, A15

### C6

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A16

## Obligations (10)

### O1

Implement pre-decision consumer notice system informing all loan applicants of AI use, purpose, contact info, plain-language description, and website statement access per 6-1-1703(2)(e)(I)-(V)

- **Required by:** R11
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O2

Establish documented process for consumers to correct incorrect personal data processed by AutoApprove per 6-1-1703(2)(f)

- **Required by:** R12
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O3

Establish meaningful appeal process for adverse consequential decisions where AutoApprove was a substantial factor per 6-1-1703(2)(g), including independent human review for Stage 1 auto-denials

- **Required by:** R13
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O4

Publish clear and readily accessible website statement summarizing deployed high-risk AI systems and algorithmic discrimination risk management per 6-1-1703(2)(d)

- **Required by:** R10
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O5

Verify February 2026 impact assessment meets all six content requirements of 6-1-1701(8)(a)-(f); supplement if gaps exist

- **Required by:** R8
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-09-28

### O6

Establish annual review process for AutoApprove deployment to ensure no algorithmic discrimination per 6-1-1703(2)(c)

- **Required by:** R9
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2027-06-30

### O7

Request from FinLogic AI additional developer documentation: algorithmic discrimination limitations (6-1-1702(2)(a)), human monitoring guidance (6-1-1702(2)(d)), and impact assessment support materials (6-1-1702(2)(e))

- **Required by:** R15
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O8

Establish ongoing algorithmic discrimination monitoring with 90-day AG and consumer notification protocol per 6-1-1704

- **Required by:** R17
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O9

Formally adopt Morrison & Partners analysis and reject GC memo conclusion; document decision in board or compliance committee minutes

- **Required by:** R4
- **Status:** recommended
- **Jurisdiction:** Colorado
- **Deadline:** Not specified

### O10

FinLogic AI must publish public use case inventory summarizing high-risk AI systems developed per 6-1-1702(3)

- **Required by:** R16
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

## Graph connections (52)

### E1

- **Src:** F2
- **Dst:** I1
- **Type:** triggers
- **Justification:** Deployment of AutoApprove raises question of high-risk AI system classification

### E2

- **Src:** F3
- **Dst:** I1
- **Type:** triggers
- **Justification:** Stage 1 fully automated decisions raise high-risk classification question

### E3

- **Src:** F4
- **Dst:** I2
- **Type:** triggers
- **Justification:** Stage 2 human-reviewed pathway raises substantial factor question

### E4

- **Src:** F5
- **Dst:** I2
- **Type:** triggers
- **Justification:** 71% agreement rate is relevant to substantial factor analysis

### E5

- **Src:** F6
- **Dst:** I3
- **Type:** triggers
- **Justification:** GC memo creates conflict requiring authority hierarchy resolution

### E6

- **Src:** F7
- **Dst:** I3
- **Type:** triggers
- **Justification:** Morrison memo contradicts GC memo, requiring resolution

### E7

- **Src:** R1
- **Dst:** A1
- **Type:** applies-to
- **Justification:** AI system definition applied to AutoApprove

### E8

- **Src:** R2
- **Dst:** A2
- **Type:** applies-to
- **Justification:** Consequential decision definition applied to lending decisions

### E9

- **Src:** R3
- **Dst:** A3
- **Type:** applies-to
- **Justification:** High-risk AI system definition applied to Stage 1

### E10

- **Src:** R4
- **Dst:** A4
- **Type:** applies-to
- **Justification:** Substantial factor definition and anti-rubber-stamping provision applied to Stage 2

### E11

- **Src:** A3
- **Dst:** C1
- **Type:** fails-element
- **Justification:** AutoApprove Stage 1 is high-risk; Helix lacks required consumer protections

### E12

- **Src:** A4
- **Dst:** C2
- **Type:** fails-element
- **Justification:** AutoApprove Stage 2 is high-risk as substantial factor; Helix lacks required consumer protections

### E13

- **Src:** R5
- **Dst:** A5
- **Type:** applies-to
- **Justification:** Deployer definition applied to Helix

### E14

- **Src:** R6
- **Dst:** A6
- **Type:** applies-to
- **Justification:** Developer definition applied to Helix - Helix is not a developer

### E15

- **Src:** R14
- **Dst:** A7
- **Type:** applies-to
- **Justification:** Small deployer exception applied to Helix - 310 employees exceeds 50 threshold

### E16

- **Src:** A7
- **Dst:** C3
- **Type:** fails-element
- **Justification:** Small deployer exception does not apply; all deployer obligations are mandatory

### E17

- **Src:** R7
- **Dst:** A8
- **Type:** applies-to
- **Justification:** Risk management program requirement applied to Helix existing program

### E18

- **Src:** A8
- **Dst:** C4
- **Type:** satisfies-element
- **Justification:** NIST AI 100-1 aligned program satisfies risk management requirement

### E19

- **Src:** R8
- **Dst:** A9
- **Type:** applies-to
- **Justification:** Impact assessment requirement applied to Helix existing assessment

### E20

- **Src:** A9
- **Dst:** C4
- **Type:** satisfies-element
- **Justification:** February 2026 assessment satisfies timeline for pre-existing systems

### E21

- **Src:** R11
- **Dst:** A10
- **Type:** applies-to
- **Justification:** Consumer notice requirement applied to Helix missing notices

### E22

- **Src:** A10
- **Dst:** C3
- **Type:** fails-element
- **Justification:** No consumer notices issued - critical compliance gap

### E23

- **Src:** R12
- **Dst:** A11
- **Type:** applies-to
- **Justification:** Data correction requirement applied to Helix missing process

### E24

- **Src:** A11
- **Dst:** C3
- **Type:** fails-element
- **Justification:** No data correction process - compliance gap

### E25

- **Src:** R13
- **Dst:** A12
- **Type:** applies-to
- **Justification:** Appeal process requirement applied to Helix missing process

### E26

- **Src:** A12
- **Dst:** C3
- **Type:** fails-element
- **Justification:** No appeal process - compliance gap

### E27

- **Src:** R10
- **Dst:** A13
- **Type:** applies-to
- **Justification:** Website statement requirement applied to Helix

### E28

- **Src:** A13
- **Dst:** C3
- **Type:** fails-element
- **Justification:** No public website statement - compliance gap

### E29

- **Src:** R15
- **Dst:** A14
- **Type:** applies-to
- **Justification:** Developer documentation obligations applied to FinLogic AI provision

### E30

- **Src:** A14
- **Dst:** C5
- **Type:** fails-element
- **Justification:** FinLogic documentation is partial - missing discrimination limitations, monitoring guidance, and IA support

### E31

- **Src:** R16
- **Dst:** A15
- **Type:** applies-to
- **Justification:** Developer public inventory requirement applied to FinLogic AI

### E32

- **Src:** A15
- **Dst:** C5
- **Type:** fails-element
- **Justification:** Unknown whether FinLogic has published public use case inventory

### E33

- **Src:** R4
- **Dst:** A16
- **Type:** applies-to
- **Justification:** Statutory text applied to resolve GC vs Morrison memo conflict

### E34

- **Src:** A16
- **Dst:** C6
- **Type:** fails-element
- **Justification:** GC memo is legally deficient; reliance on it creates non-compliance risk

### E35

- **Src:** F6
- **Dst:** A16
- **Type:** contradicts
- **Justification:** GC memo contradicts statutory anti-rubber-stamping provision

### E36

- **Src:** F7
- **Dst:** A16
- **Type:** supports
- **Justification:** Morrison memo correctly interprets statutory substantial factor definition

### E37

- **Src:** R11
- **Dst:** O1
- **Type:** triggers
- **Justification:** Consumer notice requirement triggers obligation to implement notice system

### E38

- **Src:** R12
- **Dst:** O2
- **Type:** triggers
- **Justification:** Data correction requirement triggers obligation to build correction process

### E39

- **Src:** R13
- **Dst:** O3
- **Type:** triggers
- **Justification:** Appeal requirement triggers obligation to establish appeal process

### E40

- **Src:** R10
- **Dst:** O4
- **Type:** triggers
- **Justification:** Website statement requirement triggers obligation to publish statement

### E41

- **Src:** R8
- **Dst:** O5
- **Type:** triggers
- **Justification:** Impact assessment content requirements trigger verification obligation

### E42

- **Src:** R9
- **Dst:** O6
- **Type:** triggers
- **Justification:** Annual review requirement triggers obligation to establish review process

### E43

- **Src:** R15
- **Dst:** O7
- **Type:** triggers
- **Justification:** Developer documentation requirements trigger obligation to request additional docs from FinLogic

### E44

- **Src:** R17
- **Dst:** O8
- **Type:** triggers
- **Justification:** Algorithmic discrimination notification requirement triggers monitoring obligation

### E45

- **Src:** R4
- **Dst:** O9
- **Type:** triggers
- **Justification:** Correct statutory interpretation requires formal adoption of Morrison analysis

### E46

- **Src:** R16
- **Dst:** O10
- **Type:** triggers
- **Justification:** Developer public inventory requirement triggers FinLogic obligation

### E47

- **Src:** F1
- **Dst:** I4
- **Type:** triggers
- **Justification:** Helix Colorado operations raise deployer/developer classification question

### E48

- **Src:** F15
- **Dst:** I7
- **Type:** triggers
- **Justification:** 310 employees raises question of small deployer exception applicability

### E49

- **Src:** F11
- **Dst:** I5
- **Type:** triggers
- **Justification:** Missing consumer notices trigger compliance gap analysis

### E50

- **Src:** F12
- **Dst:** I5
- **Type:** triggers
- **Justification:** Missing data correction process triggers compliance gap analysis

### E51

- **Src:** F13
- **Dst:** I5
- **Type:** triggers
- **Justification:** Missing appeal process triggers compliance gap analysis

### E52

- **Src:** F16
- **Dst:** I6
- **Type:** triggers
- **Justification:** FinLogic as SF-based developer raises question of developer obligations under CO AIA
