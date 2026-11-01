# M8 — PremiumPath Discovery and Cure — teacher FIRACO reasoning

Unverified model output for legal review. Citations, facts, applications, and obligations may be incorrect. Text and node IDs below are preserved from the saved reference graph.

[Read case](../../../data/cases/M8_premiumpath_discovery_co.md) · [Review brief](../../PROF_PHILIPP_REVIEW.md)

Teacher: claude-opus-4-6. Source: data/outputs/graphs/M8_reference.json.

Source SHA-256: `c9c77483b36dab20560db7480ec90d14dccfd510f3042e3ab043f3a21ed6f8cb`.

## Facts (19)

### F1

Clearwater Auto Insurance is based in Lakewood, Colorado

- **Polarity:** present
- **Support quote:** Clearwater Auto Insurance is based in Lakewood, Colorado

### F2

Clearwater has 240 full-time employees

- **Polarity:** present
- **Support quote:** has 240 full-time employees

### F3

Clearwater built PremiumPath, a model that sets auto insurance premiums for Colorado policyholders

- **Polarity:** present
- **Support quote:** Its data science team built 'PremiumPath,' a model that sets auto insurance premiums

### F4

PremiumPath was trained on Clearwater's own policy and claims data

- **Polarity:** present
- **Support quote:** Clearwater trained PremiumPath on its own policy and claims data

### F5

Premiums are set automatically with no human review of individual quotes

- **Polarity:** present
- **Support quote:** Premiums are set automatically, with no human review of individual quotes

### F6

March 2, 2026 internal review found materially higher premiums for Spanish-language policyholders after controlling for driving record and vehicle

- **Polarity:** present
- **Support quote:** PremiumPath charged materially higher premiums to policyholders who had chosen Spanish as their preferred language

### F7

Cause was a preferred language field the model learned to use

- **Polarity:** present
- **Support quote:** The cause was a 'preferred language' field that the model had learned to use

### F8

Engineers removed the field and released corrected model on April 6, 2026

- **Polarity:** present
- **Support quote:** Engineers removed the field and released a corrected model on April 6, 2026

### F9

3,100 policyholders still paying premiums set by the earlier discriminatory model with terms running past June 30, 2026

- **Polarity:** present
- **Support quote:** About 3,100 policyholders are still paying premiums that were set by the earlier model

### F10

Clearwater does not plan to re-rate affected policyholders before renewal

- **Polarity:** present
- **Support quote:** Clearwater does not plan to re-rate them before renewal

### F11

Clearwater has not notified the Attorney General or any policyholder about the finding

- **Polarity:** present
- **Support quote:** Clearwater has not told the Attorney General or any policyholder about the finding

### F12

General counsel argues problem was found and fixed before law takes effect

- **Polarity:** present
- **Support quote:** the problem 'was found and fixed before the law takes effect'

### F13

General counsel argues language preference is not a protected characteristic

- **Polarity:** present
- **Support quote:** language preference 'is not a protected characteristic'

### F14

General counsel argues self-cure creates presumption of reasonable care

- **Polarity:** present
- **Support quote:** having cured the problem itself, Clearwater 'will have a presumption of reasonable care'

### F15

Clearwater has risk management program aligned with NIST AI RMF

- **Polarity:** present
- **Support quote:** Clearwater has a risk management program aligned with the NIST AI Risk Management Framework

### F16

Impact assessment of PremiumPath completed in January 2026

- **Polarity:** present
- **Support quote:** it completed an impact assessment of PremiumPath in January 2026

### F17

No notice to policyholders that AI sets premiums

- **Polarity:** present
- **Support quote:** It gives policyholders no notice that an AI system sets premiums

### F18

No mechanism for policyholders to correct data or appeal a premium

- **Polarity:** present
- **Support quote:** offers no way to correct data or to appeal a premium

### F19

Insurance is a consequential decision category under the Act

- **Polarity:** present
- **Support quote:** Not specified

## Issues (7)

### I1

Whether PremiumPath qualifies as a high-risk AI system under CO AIA

- **Status:** dispositive

### I2

Whether the March 2026 finding constitutes algorithmic discrimination under section 6-1-1701(1)

- **Status:** dispositive

### I3

What notice duties arise from the discovery and to whom and by when given 3,100 policyholders still affected after effective date

- **Status:** dispositive

### I4

Whether Clearwater qualifies for the rebuttable presumption of reasonable care

- **Status:** dispositive

### I5

Whether the small deployer exception under section 6-1-1703(6) applies

- **Status:** collateral

### I6

Clearwater's roles under the Act and corresponding obligations

- **Status:** dispositive

### I7

Who can enforce the Act and what is the enforcement exposure

- **Status:** dispositive

## Rules (15)

### R1

Definition of algorithmic discrimination including limited English proficiency, national origin, ethnicity as protected bases

- **Citation:** CO AIA section 6-1-1701(1)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R2

Insurance is a consequential decision category

- **Citation:** CO AIA section 6-1-1701(3)(g)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R3

High-risk AI system definition: AI system that makes or is substantial factor in consequential decision

- **Citation:** CO AIA section 6-1-1701(7)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R4

Substantial factor definition: human review insufficient if based primarily on AI output

- **Citation:** CO AIA section 6-1-1701(9)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R5

Developer obligations: reasonable care, documentation, public use case inventory

- **Citation:** CO AIA section 6-1-1702
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R6

Deployer obligations: risk management, impact assessment, annual review, public statement, consumer notice, data correction, appeal

- **Citation:** CO AIA section 6-1-1703(2)(a)-(g)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R7

Small deployer exception: fewer than 50 employees AND does not use own data to train

- **Citation:** CO AIA section 6-1-1703(6)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R8

Notice of algorithmic discrimination: notify AG and affected consumers within 90 days of discovery

- **Citation:** CO AIA section 6-1-1704
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R9

Enforcement: AG exclusive authority, deceptive trade practice, up to $20,000 per violation

- **Citation:** CO AIA section 6-1-1706(1)-(3)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R10

Deployer rebuttable presumption of reasonable care requires compliance with section 6-1-1703

- **Citation:** CO AIA section 6-1-1703(3)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R11

Enforcement safe harbor: discovery through own testing AND cure plus AG notification within 60 days

- **Citation:** CO AIA section 6-1-1706(4)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R12

Developer definition: person doing business in state that develops or substantially modifies high-risk AI system

- **Citation:** CO AIA section 6-1-1701(6)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R13

Deployer definition: person doing business in state that deploys high-risk AI system

- **Citation:** CO AIA section 6-1-1701(5)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R14

New impact assessment required within 90 days of intentional and substantial modification

- **Citation:** CO AIA section 6-1-1703(2)(b)(III)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R15

Deployer duty to use reasonable care to protect consumers from known or foreseeable risks of algorithmic discrimination

- **Citation:** CO AIA section 6-1-1703(1)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

## Applications (12)

### A1

PremiumPath is an AI system that makes consequential decisions (insurance premiums) automatically with no human review. Insurance is explicitly listed in section 6-1-1701(3)(g). No exceptions in section 6-1-1701(7)(a)-(d) apply. PremiumPath is a high-risk AI system.

- **Rule ref:** R3
- **Fact refs:** F3, F5, F19
- **Issue ref:** I1
- **Result:** satisfied

### A2

PremiumPath charged materially higher premiums based on Spanish language preference, which directly implicates 'limited English proficiency' explicitly listed in section 6-1-1701(1). Language preference also serves as a proxy for national origin and ethnicity. The differential treatment after controlling for legitimate factors constitutes unlawful discrimination under Colorado insurance law. General counsel's argument that language preference is not protected is incorrect.

- **Rule ref:** R1
- **Fact refs:** F6, F7
- **Issue ref:** I2
- **Result:** violated

### A3

Clearwater discovered algorithmic discrimination on March 2, 2026. 3,100 policyholders remain on discriminatory premiums past June 30, 2026. The discrimination is ongoing as of the effective date. Clearwater has not notified the AG or affected consumers. At minimum, the 90-day clock runs from June 30, 2026 (effective date) requiring notification by September 28, 2026. Clearwater's failure to plan any notification violates section 6-1-1704.

- **Rule ref:** R8
- **Fact refs:** F6, F9, F10, F11
- **Issue ref:** I3
- **Result:** violated

### A4

The section 6-1-1703(3) presumption requires compliance with all of section 6-1-1703. Clearwater fails to provide consumer notice (2)(e), data correction (2)(f), and appeal rights (2)(g). The presumption does not attach.

- **Rule ref:** R10
- **Fact refs:** F17, F18, F11
- **Issue ref:** I4
- **Result:** violated

### A5

The section 6-1-1706(4) safe harbor requires both: (a) discovery through own testing (satisfied) AND (b) cure plus AG notification within 60 days. Clearwater has not notified the AG at all. The violation is also not fully cured because 3,100 policyholders remain on discriminatory premiums. Both elements (b) fail.

- **Rule ref:** R11
- **Fact refs:** F6, F8, F9, F11
- **Issue ref:** I4
- **Result:** violated

### A6

The small deployer exception requires BOTH fewer than 50 employees AND not using own data to train. Clearwater has 240 employees (fails condition a) and uses its own data (fails condition b). The exception is doubly inapplicable.

- **Rule ref:** R7
- **Fact refs:** F2, F4
- **Issue ref:** I5
- **Result:** violated

### A7

Clearwater's data science team built PremiumPath. Clearwater does business in Colorado. It developed an AI system it knew would be used as a high-risk AI system for insurance pricing. Clearwater is a developer under section 6-1-1701(6).

- **Rule ref:** R12
- **Fact refs:** F1, F3, F4
- **Issue ref:** I6
- **Result:** satisfied

### A8

Clearwater deploys PremiumPath to set insurance premiums in Colorado. It does business in the state. Clearwater is a deployer under section 6-1-1701(5).

- **Rule ref:** R13
- **Fact refs:** F1, F3, F5
- **Issue ref:** I6
- **Result:** satisfied

### A9

Clearwater satisfies section 6-1-1703(2)(a) (NIST-aligned risk management program) and partially satisfies (2)(b) (impact assessment completed but needs update after April 6 modification). It fails (2)(e) (no consumer notice), (2)(f) (no data correction mechanism), and (2)(g) (no appeal process). Status of (2)(d) public website statement is unknown.

- **Rule ref:** R6
- **Fact refs:** F15, F16, F17, F18
- **Issue ref:** I6
- **Result:** partial

### A10

The corrected model released April 6, 2026 constitutes an intentional and substantial modification. Under section 6-1-1703(2)(b)(III), a new impact assessment is required within 90 days (by July 5, 2026). The January 2026 assessment predates both the discovery and the modification and is insufficient.

- **Rule ref:** R14
- **Fact refs:** F8, F16
- **Issue ref:** I6
- **Result:** violated

### A11

The AG has exclusive enforcement authority. No private right of action. Penalties up to $20,000 per violation. With 3,100 affected policyholders and multiple violation categories, theoretical exposure is in the tens of millions of dollars.

- **Rule ref:** R9
- **Fact refs:** F1, F9
- **Issue ref:** I7
- **Result:** satisfied

### A12

On and after June 30, 2026, Clearwater must use reasonable care to protect consumers from known risks of algorithmic discrimination. Knowingly allowing 3,100 policyholders to continue paying discriminatory premiums without remediation violates the reasonable care standard.

- **Rule ref:** R15
- **Fact refs:** F9, F10, F6
- **Issue ref:** I3
- **Result:** violated

## Conclusions (7)

### C1

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A1

### C2

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A2

### C3

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A3, A12

### C4

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A4, A5

### C5

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A6

### C6

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A7, A8, A9, A10

### C7

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A11

## Obligations (11)

### O1

Notify the Colorado Attorney General of the discovery that PremiumPath caused algorithmic discrimination

- **Required by:** R8
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-09-28

### O2

Notify approximately 3,100 affected policyholders of the algorithmic discrimination

- **Required by:** R8
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-09-28

### O3

Re-rate or remediate premiums for 3,100 affected policyholders to cure ongoing discriminatory pricing

- **Required by:** R15
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O4

Implement consumer notice before PremiumPath makes consequential decisions including purpose, AI description, contact info, and link to public statement

- **Required by:** R6
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O5

Implement mechanism for consumers to correct incorrect personal data processed by PremiumPath

- **Required by:** R6
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O6

Implement meaningful appeal process for consequential decisions made by PremiumPath

- **Required by:** R6
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O7

Complete new impact assessment of corrected PremiumPath model released April 6, 2026 as an intentional and substantial modification

- **Required by:** R14
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-07-05

### O8

Publish public website statement summarizing deployed high-risk AI systems and algorithmic discrimination risk management

- **Required by:** R6
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O9

Publish public use case inventory of high-risk AI systems developed (developer obligation)

- **Required by:** R5
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O10

Prepare developer documentation on limitations, training data, intended uses, and monitoring guidance

- **Required by:** R5
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O11

To preserve section 6-1-1706(4) safe harbor, notify AG of discovery and cure within 60 days of discovery (deadline was May 1, 2026 from March 2 discovery)

- **Required by:** R11
- **Status:** safe-harbor
- **Jurisdiction:** Colorado
- **Deadline:** 2026-05-01

## Graph connections (48)

### E1

- **Src:** F3
- **Dst:** I1
- **Type:** triggers
- **Justification:** PremiumPath is an AI system used for insurance pricing raising high-risk classification question

### E2

- **Src:** F5
- **Dst:** I1
- **Type:** supports
- **Justification:** No human review means AI makes the decision, not merely assists

### E3

- **Src:** F19
- **Dst:** I1
- **Type:** supports
- **Justification:** Insurance is explicitly listed as a consequential decision category

### E4

- **Src:** F6
- **Dst:** I2
- **Type:** triggers
- **Justification:** Discovery of differential treatment based on language preference raises algorithmic discrimination question

### E5

- **Src:** F7
- **Dst:** I2
- **Type:** supports
- **Justification:** Language field as causal factor links to limited English proficiency protected basis

### E6

- **Src:** F9
- **Dst:** I3
- **Type:** triggers
- **Justification:** 3,100 policyholders on discriminatory premiums past effective date triggers notice duty analysis

### E7

- **Src:** F11
- **Dst:** I3
- **Type:** supports
- **Justification:** Failure to notify anyone raises the notice obligation question

### E8

- **Src:** F11
- **Dst:** I4
- **Type:** triggers
- **Justification:** No AG notification undermines safe harbor claim

### E9

- **Src:** F14
- **Dst:** I4
- **Type:** triggers
- **Justification:** General counsel's safe harbor argument must be evaluated

### E10

- **Src:** F2
- **Dst:** I5
- **Type:** triggers
- **Justification:** Employee count relevant to small deployer exception

### E11

- **Src:** F4
- **Dst:** I5
- **Type:** supports
- **Justification:** Use of own training data relevant to small deployer exception

### E12

- **Src:** R3
- **Dst:** A1
- **Type:** applies-to
- **Justification:** High-risk AI system definition applied to PremiumPath

### E13

- **Src:** R2
- **Dst:** A1
- **Type:** applies-to
- **Justification:** Insurance as consequential decision category applied

### E14

- **Src:** R1
- **Dst:** A2
- **Type:** applies-to
- **Justification:** Algorithmic discrimination definition applied to language-based differential treatment

### E15

- **Src:** R8
- **Dst:** A3
- **Type:** applies-to
- **Justification:** Notice of algorithmic discrimination obligation applied

### E16

- **Src:** R10
- **Dst:** A4
- **Type:** applies-to
- **Justification:** Deployer presumption requirements applied

### E17

- **Src:** R11
- **Dst:** A5
- **Type:** applies-to
- **Justification:** Enforcement safe harbor requirements applied

### E18

- **Src:** R7
- **Dst:** A6
- **Type:** applies-to
- **Justification:** Small deployer exception applied

### E19

- **Src:** R12
- **Dst:** A7
- **Type:** applies-to
- **Justification:** Developer definition applied to Clearwater

### E20

- **Src:** R13
- **Dst:** A8
- **Type:** applies-to
- **Justification:** Deployer definition applied to Clearwater

### E21

- **Src:** R6
- **Dst:** A9
- **Type:** applies-to
- **Justification:** Deployer obligations applied to Clearwater compliance status

### E22

- **Src:** R14
- **Dst:** A10
- **Type:** applies-to
- **Justification:** Impact assessment update requirement applied to April 6 model correction

### E23

- **Src:** R9
- **Dst:** A11
- **Type:** applies-to
- **Justification:** Enforcement provisions applied to exposure analysis

### E24

- **Src:** R15
- **Dst:** A12
- **Type:** applies-to
- **Justification:** Reasonable care duty applied to ongoing discriminatory premiums

### E25

- **Src:** A1
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** PremiumPath confirmed as high-risk AI system

### E26

- **Src:** A2
- **Dst:** C2
- **Type:** fails-element
- **Justification:** Finding constitutes algorithmic discrimination; general counsel argument fails

### E27

- **Src:** A3
- **Dst:** C3
- **Type:** fails-element
- **Justification:** Notice obligations not met

### E28

- **Src:** A12
- **Dst:** C3
- **Type:** fails-element
- **Justification:** Reasonable care duty violated by ongoing discriminatory premiums

### E29

- **Src:** A4
- **Dst:** C4
- **Type:** fails-element
- **Justification:** Deployer presumption unavailable due to noncompliance with section 6-1-1703

### E30

- **Src:** A5
- **Dst:** C4
- **Type:** fails-element
- **Justification:** Enforcement safe harbor unavailable due to no AG notification and incomplete cure

### E31

- **Src:** A6
- **Dst:** C5
- **Type:** fails-element
- **Justification:** Small deployer exception inapplicable on both conditions

### E32

- **Src:** A9
- **Dst:** C6
- **Type:** fails-element
- **Justification:** Multiple deployer obligations unmet

### E33

- **Src:** A10
- **Dst:** C6
- **Type:** fails-element
- **Justification:** Impact assessment update required but not completed

### E34

- **Src:** A11
- **Dst:** C7
- **Type:** satisfies-element
- **Justification:** AG enforcement authority confirmed with significant exposure

### E35

- **Src:** R8
- **Dst:** O1
- **Type:** triggers
- **Justification:** Discovery of algorithmic discrimination triggers AG notification duty

### E36

- **Src:** R8
- **Dst:** O2
- **Type:** triggers
- **Justification:** Discovery of algorithmic discrimination triggers consumer notification duty

### E37

- **Src:** R15
- **Dst:** O3
- **Type:** triggers
- **Justification:** Reasonable care duty requires remediation of ongoing discriminatory premiums

### E38

- **Src:** R6
- **Dst:** O4
- **Type:** triggers
- **Justification:** Deployer obligation to provide consumer notice before consequential decisions

### E39

- **Src:** R6
- **Dst:** O5
- **Type:** triggers
- **Justification:** Deployer obligation to provide data correction mechanism

### E40

- **Src:** R6
- **Dst:** O6
- **Type:** triggers
- **Justification:** Deployer obligation to provide appeal process

### E41

- **Src:** R14
- **Dst:** O7
- **Type:** triggers
- **Justification:** Substantial modification triggers new impact assessment within 90 days

### E42

- **Src:** R6
- **Dst:** O8
- **Type:** triggers
- **Justification:** Deployer obligation to publish public website statement

### E43

- **Src:** R5
- **Dst:** O9
- **Type:** triggers
- **Justification:** Developer obligation to publish public use case inventory

### E44

- **Src:** R5
- **Dst:** O10
- **Type:** triggers
- **Justification:** Developer obligation to prepare documentation

### E45

- **Src:** R11
- **Dst:** O11
- **Type:** triggers
- **Justification:** Safe harbor requires AG notification within 60 days of discovery

### E46

- **Src:** F13
- **Dst:** A2
- **Type:** contradicts
- **Justification:** General counsel's claim that language preference is not protected contradicts statutory text listing limited English proficiency

### E47

- **Src:** F12
- **Dst:** A3
- **Type:** contradicts
- **Justification:** Argument that fix before effective date eliminates obligations contradicted by ongoing discriminatory premiums post-effective date

### E48

- **Src:** F14
- **Dst:** A5
- **Type:** contradicts
- **Justification:** Self-cure argument fails because AG was never notified and cure is incomplete
