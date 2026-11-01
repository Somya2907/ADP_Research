# H9 — EligiCheck County Assistance — teacher FIRACO reasoning

Unverified model output for legal review. Citations, facts, applications, and obligations may be incorrect. Text and node IDs below are preserved from the saved reference graph.

[Read case](../../../data/cases/H9_eligicheck_county_co.md) · [Review brief](../../PROF_PHILIPP_REVIEW.md)

Teacher: claude-opus-4-6. Source: data/outputs/graphs/H9_reference.json.

Source SHA-256: `cf3d32557cb14a370eeba754ef00831375b3c7748f2fa00ff4d2eaed0b83b53a`.

## Facts (13)

### F1

Juniper County is a Colorado county; CivicSort is in Durango, CO; all activity in Colorado

- **Polarity:** present
- **Support quote:** CivicSort Analytics, a company in Durango, Colorado

### F2

EligiCheck recommends approval/denial of emergency rental and utility assistance

- **Polarity:** present
- **Support quote:** recommends whether each application for assistance should be approved or denied

### F3

CivicSort built EligiCheck by extensively retraining open-source model on County historical case files

- **Polarity:** present
- **Support quote:** taking an open-source model and extensively retraining it on eight years of the County's historical case files

### F4

Caseworkers followed EligiCheck recommendation 97% of the time, spending avg 2 minutes per case

- **Polarity:** present
- **Support quote:** caseworkers entered the recommended outcome in 97% of applications, spending an average of two minutes

### F5

CivicSort has 38 full-time employees; training data supplied by County under contract

- **Polarity:** present
- **Support quote:** 38 full-time employees...the County supplied under the contract

### F6

No impact assessment exists; only a one-page description provided

- **Polarity:** present
- **Support quote:** No impact assessment exists. CivicSort gave the County a one-page description

### F7

CivicSort provided no documentation of training data, limitations, intended/inappropriate uses

- **Polarity:** present
- **Support quote:** no documentation of training data, limitations, or intended and inappropriate uses

### F8

Applicants not told AI is involved; denial letters give generic reason

- **Polarity:** present
- **Support quote:** Applicants are not told that an AI system is involved. Denial letters give a generic reason

### F9

No process for applicants to correct data processed by EligiCheck

- **Polarity:** present
- **Support quote:** There is no process for correcting data

### F10

Hearing officer has no access to EligiCheck recommendation or factors behind it

- **Polarity:** present
- **Support quote:** hearing officer reviews the application file but has no access to EligiCheck's recommendation or the factors behind it

### F11

Jan 2026 audit: Spanish-language apps denied at 1.6x rate of English with similar finances; no notification or changes made

- **Polarity:** present
- **Support quote:** applications submitted in Spanish were denied at 1.6 times the rate of applications submitted in English

### F12

County Attorney says Act does not apply to governments; CivicSort claims contractor status and small-deployer exception

- **Polarity:** disputed
- **Support quote:** The County Attorney's memo concludes that the Act 'regulates businesses, not governments'

### F13

Colorado AIA effective June 30, 2026; analysis date April 16, 2026

- **Polarity:** present
- **Support quote:** Not specified

## Issues (9)

### I1

Which categories of consequential decision does EligiCheck involve

- **Status:** dispositive

### I2

Is EligiCheck a high-risk AI system and substantial factor despite caseworker review

- **Status:** dispositive

### I3

Is CivicSort the developer under the statutory definition

- **Status:** dispositive

### I4

Who is the deployer - County, CivicSort, or both; does Act apply to government entities

- **Status:** dispositive

### I5

Can CivicSort rely on the small-deployer exception under 6-1-1703(6)

- **Status:** dispositive

### I6

Weight of County Attorney memo, Council guidance, and AG FAQ

- **Status:** collateral

### I7

Specific obligations and deadlines for each party

- **Status:** dispositive

### I8

Does Jan 2026 audit finding constitute algorithmic discrimination triggering notification

- **Status:** dispositive

### I9

Does existing administrative hearing satisfy the appeal requirement

- **Status:** dispositive

## Rules (14)

### R1

Consequential decision includes essential government service and housing

- **Citation:** CO AIA 6-1-1701(3)(d),(f)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R2

High-risk AI system: AI that makes or is substantial factor in consequential decision

- **Citation:** CO AIA 6-1-1701(7)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R3

Substantial factor: human review based primarily on AI output does not negate finding

- **Citation:** CO AIA 6-1-1701(9)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R4

Developer: person doing business in state that develops or substantially modifies AI for high-risk use

- **Citation:** CO AIA 6-1-1701(6)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R5

Deployer: person doing business in state that integrates or uses high-risk AI in product or service

- **Citation:** CO AIA 6-1-1701(4),(5)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R6

Developer obligations: reasonable care, documentation to deployer, public statement

- **Citation:** CO AIA 6-1-1702(1)-(3)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R7

Deployer obligations: risk mgmt, impact assessment, review, notice, data correction, appeal

- **Citation:** CO AIA 6-1-1703(2)(a)-(g)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R8

Small-deployer exception: fewer than 50 employees AND does not use own data to train

- **Citation:** CO AIA 6-1-1703(6)(a)-(b)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R9

Notification of algorithmic discrimination: 90 days to notify AG and affected consumers

- **Citation:** CO AIA 6-1-1704
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R10

Algorithmic discrimination: unlawful differential treatment on basis of protected class including limited English proficiency

- **Citation:** CO AIA 6-1-1701(1)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R11

Enforcement: AG exclusive authority, no private right of action, up to $20,000 per violation

- **Citation:** CO AIA 6-1-1706
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R12

Rebuttable presumption of reasonable care for compliant deployers

- **Citation:** CO AIA 6-1-1703(3)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R13

Safe harbor: self-discovery and cure within 60 days with AG notification

- **Citation:** CO AIA 6-1-1706(4)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R14

Risk management must be consistent with NIST AI RMF 100-1 or equivalent like ISO/IEC 42001

- **Citation:** CO AIA 6-1-1703(2)(a)(III)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

## Applications (12)

### A1

Emergency rental and utility assistance is an essential government service under 6-1-1701(3)(d). Rental assistance also implicates housing under 6-1-1701(3)(f). The decision to approve or deny has material legal or similarly significant effect on provision of these services.

- **Rule ref:** R1
- **Fact refs:** F2
- **Issue ref:** I1
- **Result:** satisfied

### A2

EligiCheck is an AI system that produces recommendations for consequential decisions. It is not excluded by any of the four exceptions in 6-1-1701(7)(a)-(d): it does not perform a narrow procedural task, does not improve previously completed human activity, does not merely detect patterns without influencing assessment, and is not a preparatory task.

- **Rule ref:** R2
- **Fact refs:** F2, F3, F4
- **Issue ref:** I2
- **Result:** satisfied

### A3

97% concordance rate with 2-minute review establishes caseworker review is based primarily on AI output. Under 6-1-1701(9), human review based primarily on AI output does not negate substantial factor finding. EligiCheck materially contributes to the consequential decision.

- **Rule ref:** R3
- **Fact refs:** F4
- **Issue ref:** I2
- **Result:** satisfied

### A4

CivicSort is doing business in Colorado and substantially modified an open-source model by extensively retraining it. CivicSort knew the system would be used for benefit eligibility decisions (consequential decisions). CivicSort satisfies all elements of the developer definition.

- **Rule ref:** R4
- **Fact refs:** F1, F3
- **Issue ref:** I3
- **Result:** satisfied

### A5

The County integrates EligiCheck into its assistance program and uses it in service delivery. This satisfies 'deploy' meaning 'integrate or use an AI system in a product or service.' The Act does not contain a government exemption. The AG FAQ confirms applicability regardless of sector. The County is the deployer, though textual ambiguity exists regarding 'doing business in the state' for government entities.

- **Rule ref:** R5
- **Fact refs:** F1, F2, F12
- **Issue ref:** I4
- **Result:** satisfied

### A6

CivicSort meets condition (a) with 38 employees. However, condition (b) likely fails: CivicSort had custody and control of the training data and used it to retrain the model, making it functionally its own data. Moreover, CivicSort is primarily a developer, not a deployer, so the deployer exception is inapplicable. Even if both conditions were met, the exception only relieves obligations under (2)(a), (2)(b), and (2)(d), not (2)(c), (2)(e), (2)(f), or (2)(g).

- **Rule ref:** R8
- **Fact refs:** F5, F3
- **Issue ref:** I5
- **Result:** violated

### A7

CivicSort has failed all developer documentation obligations under 6-1-1702(2)(a)-(e): no documentation of limitations, training data, intended/inappropriate uses, monitoring guidance, or impact assessment support materials. CivicSort has also failed the public statement obligation under 6-1-1702(3).

- **Rule ref:** R6
- **Fact refs:** F6, F7
- **Issue ref:** I7
- **Result:** violated

### A8

The County has failed all deployer obligations: no risk management program (2)(a), no impact assessment (2)(b), no annual review (2)(c), no public statement (2)(d), no consumer notice (2)(e), no data correction process (2)(f), and inadequate appeal process (2)(g).

- **Rule ref:** R7
- **Fact refs:** F6, F8, F9, F10
- **Issue ref:** I7
- **Result:** violated

### A9

Spanish-language applications denied at 1.6x rate implicates limited English proficiency and national origin, both protected under 6-1-1701(1). With similar household finances, the disparity is not explained by legitimate factors. This likely violates Title VI and Colorado antidiscrimination law, satisfying the 'in violation of state or federal antidiscrimination laws' element.

- **Rule ref:** R10
- **Fact refs:** F11
- **Issue ref:** I8
- **Result:** satisfied

### A10

Both parties have knowledge of ongoing algorithmic discrimination. The 90-day notification clock begins June 30, 2026 (effective date) since discrimination is ongoing and known. Neither party has notified the AG or affected consumers. Deadline: September 28, 2026.

- **Rule ref:** R9
- **Fact refs:** F11, F13
- **Issue ref:** I8
- **Result:** violated

### A11

Section 6-1-1703(2)(g) requires a 'meaningful opportunity to appeal.' The hearing officer cannot access EligiCheck's recommendation or factors, making it impossible to meaningfully review the AI-assisted decision. The appeal is blind to the AI component that substantially drove the outcome.

- **Rule ref:** R7
- **Fact refs:** F10
- **Issue ref:** I9
- **Result:** violated

### A12

Whether CivicSort is also a deployer (in addition to developer) is uncertain. CivicSort operates EligiCheck on its own servers, which could constitute 'using' the system. However, CivicSort does not directly deliver the service to consumers. The statutory text does not clearly resolve whether a hosted-service vendor 'deploys' the system.

- **Rule ref:** R5
- **Fact refs:** F3, F12
- **Issue ref:** I4
- **Result:** requires-fact

## Conclusions (7)

### C1

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A1, A2, A3

### C2

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A4, A7

### C3

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A5, A8

### C4

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A6

### C5

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A9, A10

### C6

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A11

### C7

- **Determination:** conditional
- **Confidence:** medium
- **Support refs:** A12

## Obligations (14)

### O1

Remediate Spanish-language denial rate disparity immediately

- **Required by:** R9
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O2

CivicSort: prepare and deliver all developer documentation per 6-1-1702(2)(a)-(e)

- **Required by:** R6
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O3

CivicSort: publish public use case inventory per 6-1-1702(3)

- **Required by:** R6
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O4

County: implement NIST AI RMF-consistent risk management program per 6-1-1703(2)(a)

- **Required by:** R14
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O5

County: implement consumer notice process for applicants per 6-1-1703(2)(e)

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O6

County: create data correction process for applicants per 6-1-1703(2)(f)

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O7

County: reform appeal process so hearing officer can access EligiCheck output and factors per 6-1-1703(2)(g)

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O8

County: publish website statement on high-risk AI use and discrimination risk management per 6-1-1703(2)(d)

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O9

County: complete impact assessment within 90 days of effective date per 6-1-1703(2)(b)(I)

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-09-28

### O10

Both: notify AG and affected consumers of algorithmic discrimination per 6-1-1704

- **Required by:** R9
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-09-28

### O11

County: conduct annual review of EligiCheck deployment per 6-1-1703(2)(c)

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** Not specified

### O12

County: update impact assessment annually per 6-1-1703(2)(b)(II)

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** Not specified

### O13

CivicSort: exercise ongoing reasonable care per 6-1-1702(1)

- **Required by:** R6
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** Not specified

### O14

Both: pursue self-cure safe harbor by curing violation and notifying AG within 60 days per 6-1-1706(4)

- **Required by:** R13
- **Status:** safe-harbor
- **Jurisdiction:** Colorado
- **Deadline:** Not specified

## Graph connections (46)

### E1

- **Src:** F2
- **Dst:** I1
- **Type:** triggers
- **Justification:** Nature of decision raises consequential decision classification question

### E2

- **Src:** F4
- **Dst:** I2
- **Type:** triggers
- **Justification:** 97% concordance rate raises substantial factor question

### E3

- **Src:** F3
- **Dst:** I3
- **Type:** triggers
- **Justification:** Extensive retraining raises developer classification question

### E4

- **Src:** F12
- **Dst:** I4
- **Type:** triggers
- **Justification:** Competing positions raise deployer identity question

### E5

- **Src:** F5
- **Dst:** I5
- **Type:** triggers
- **Justification:** 38 employees and data source raise small-deployer exception question

### E6

- **Src:** F12
- **Dst:** I6
- **Type:** triggers
- **Justification:** Multiple guidance sources raise authority weight question

### E7

- **Src:** F11
- **Dst:** I8
- **Type:** triggers
- **Justification:** Disparate denial rate raises algorithmic discrimination question

### E8

- **Src:** F10
- **Dst:** I9
- **Type:** triggers
- **Justification:** Hearing officer lack of access raises appeal adequacy question

### E9

- **Src:** R1
- **Dst:** A1
- **Type:** applies-to
- **Justification:** Consequential decision definition applied to emergency assistance

### E10

- **Src:** R2
- **Dst:** A2
- **Type:** applies-to
- **Justification:** High-risk AI definition applied to EligiCheck

### E11

- **Src:** R3
- **Dst:** A3
- **Type:** applies-to
- **Justification:** Substantial factor definition applied to 97% concordance

### E12

- **Src:** R4
- **Dst:** A4
- **Type:** applies-to
- **Justification:** Developer definition applied to CivicSort

### E13

- **Src:** R5
- **Dst:** A5
- **Type:** applies-to
- **Justification:** Deployer definition applied to County

### E14

- **Src:** R8
- **Dst:** A6
- **Type:** applies-to
- **Justification:** Small-deployer exception applied to CivicSort

### E15

- **Src:** R6
- **Dst:** A7
- **Type:** applies-to
- **Justification:** Developer obligations applied to CivicSort documentation failures

### E16

- **Src:** R7
- **Dst:** A8
- **Type:** applies-to
- **Justification:** Deployer obligations applied to County compliance failures

### E17

- **Src:** R10
- **Dst:** A9
- **Type:** applies-to
- **Justification:** Algorithmic discrimination definition applied to Spanish-language disparity

### E18

- **Src:** R9
- **Dst:** A10
- **Type:** applies-to
- **Justification:** Notification obligation applied to known ongoing discrimination

### E19

- **Src:** R7
- **Dst:** A11
- **Type:** applies-to
- **Justification:** Appeal requirement applied to existing hearing process

### E20

- **Src:** R5
- **Dst:** A12
- **Type:** applies-to
- **Justification:** Deployer definition applied to CivicSort hosted-service role

### E21

- **Src:** A1
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** EligiCheck involves consequential decisions

### E22

- **Src:** A2
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** EligiCheck is high-risk AI system

### E23

- **Src:** A3
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** EligiCheck is substantial factor despite human review

### E24

- **Src:** A4
- **Dst:** C2
- **Type:** fails-element
- **Justification:** CivicSort is developer and has failed all developer obligations

### E25

- **Src:** A7
- **Dst:** C2
- **Type:** fails-element
- **Justification:** CivicSort has not provided required documentation

### E26

- **Src:** A5
- **Dst:** C3
- **Type:** fails-element
- **Justification:** County is deployer and has failed all deployer obligations

### E27

- **Src:** A8
- **Dst:** C3
- **Type:** fails-element
- **Justification:** County has not implemented any required deployer measures

### E28

- **Src:** A6
- **Dst:** C4
- **Type:** fails-element
- **Justification:** Small-deployer exception unavailable to CivicSort

### E29

- **Src:** A9
- **Dst:** C5
- **Type:** fails-element
- **Justification:** Algorithmic discrimination exists and notification obligations unmet

### E30

- **Src:** A10
- **Dst:** C5
- **Type:** fails-element
- **Justification:** Neither party has notified AG or consumers

### E31

- **Src:** A11
- **Dst:** C6
- **Type:** fails-element
- **Justification:** Appeal process does not meet meaningful standard

### E32

- **Src:** A12
- **Dst:** C7
- **Type:** supports
- **Justification:** CivicSort co-deployer status uncertain but possible

### E33

- **Src:** R6
- **Dst:** O2
- **Type:** triggers
- **Justification:** Developer documentation obligations

### E34

- **Src:** R6
- **Dst:** O3
- **Type:** triggers
- **Justification:** Developer public statement obligation

### E35

- **Src:** R14
- **Dst:** O4
- **Type:** triggers
- **Justification:** NIST AI RMF risk management requirement

### E36

- **Src:** R7
- **Dst:** O5
- **Type:** triggers
- **Justification:** Consumer notice obligation

### E37

- **Src:** R7
- **Dst:** O6
- **Type:** triggers
- **Justification:** Data correction obligation

### E38

- **Src:** R7
- **Dst:** O7
- **Type:** triggers
- **Justification:** Meaningful appeal obligation

### E39

- **Src:** R7
- **Dst:** O8
- **Type:** triggers
- **Justification:** Public website statement obligation

### E40

- **Src:** R7
- **Dst:** O9
- **Type:** triggers
- **Justification:** Impact assessment for pre-existing system

### E41

- **Src:** R9
- **Dst:** O10
- **Type:** triggers
- **Justification:** Algorithmic discrimination notification obligation

### E42

- **Src:** R9
- **Dst:** O1
- **Type:** triggers
- **Justification:** Remediation of known discrimination

### E43

- **Src:** R13
- **Dst:** O14
- **Type:** triggers
- **Justification:** Self-cure safe harbor availability

### E44

- **Src:** R7
- **Dst:** O11
- **Type:** triggers
- **Justification:** Annual review obligation

### E45

- **Src:** R7
- **Dst:** O12
- **Type:** triggers
- **Justification:** Annual impact assessment update

### E46

- **Src:** R6
- **Dst:** O13
- **Type:** triggers
- **Justification:** Ongoing reasonable care obligation
