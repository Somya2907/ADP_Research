# H4 — AuthStream Prior Authorization, Colorado and Texas — teacher FIRACO reasoning

Unverified model output for legal review. Citations, facts, applications, and obligations may be incorrect. Text and node IDs below are preserved from the saved reference graph.

[Read case](../../../data/cases/H4_authstream_insurer_co_tx.md) · [Review brief](../../PROF_PHILIPP_REVIEW.md)

Teacher: claude-opus-4-6. Source: data/outputs/graphs/H4_reference.json.

Source SHA-256: `575896a7c265c29116741b8198d18151faf5d6d7b82952f5ff64b93797c94d9e`.

## Facts (24)

### F1

Sagebrush is a private health insurer HQ in Dallas TX with 2300 employees, insuring individuals in TX and CO

- **Polarity:** present
- **Support quote:** Sagebrush Health Plan is a health insurer headquartered in Dallas, Texas, with 2,300 employees

### F2

AuthStream is an AI system licensed from Calyx Decision Systems processing prior-auth requests since 2024

- **Polarity:** present
- **Support quote:** Since 2024 Sagebrush has used AuthStream to process prior-authorization requests

### F3

AuthStream auto-approves 62% of requests and flags 38% as recommend deny for nurse review

- **Polarity:** present
- **Support quote:** AuthStream approves 62% of requests automatically. It marks the remaining 38% recommend deny

### F4

Nurse reviewers spend average 90 seconds per flagged request and agree with recommendation 94% of the time

- **Polarity:** present
- **Support quote:** nurse reviewers spend an average of 90 seconds on each flagged request and agree with the recommendation in 94% of cases

### F5

In-house counsel memo concludes AuthStream is not high-risk citing nurse review and preparatory task exception

- **Polarity:** present
- **Support quote:** in-house counsel memo concludes that AuthStream is not high-risk because a licensed nurse makes every denial

### F6

Outside counsel Halvorsen & Reyes memo concludes AuthStream is high-risk as substantial factor

- **Polarity:** present
- **Support quote:** outside counsel concludes that AuthStream is a substantial factor in consequential decisions and is high-risk

### F7

Trade association bulletin states utilization-management software is outside the Act

- **Polarity:** present
- **Support quote:** Western Health Plans Association states that utilization-management software is outside the Act

### F8

No AG final rule on whether AuthStream is covered

- **Polarity:** present
- **Support quote:** The Attorney General has issued no final rule on the question

### F9

Sagebrush has NIST AI RMF-aligned risk management program since 2025

- **Polarity:** present
- **Support quote:** a risk management program aligned with the NIST AI Risk Management Framework, in place since 2025

### F10

No impact assessment has been completed

- **Polarity:** present
- **Support quote:** no impact assessment

### F11

Denial letters state request was reviewed by clinical staff with no mention of AI

- **Polarity:** present
- **Support quote:** denial letters stating that the request was reviewed by clinical staff with no mention of AI

### F12

No website statement about high-risk AI systems

- **Polarity:** present
- **Support quote:** no statement on its website

### F13

No process for consumers to correct data used by AuthStream

- **Polarity:** present
- **Support quote:** no process to correct data

### F14

Standard insurance appeal exists but reviewing physician not shown AuthStream output

- **Polarity:** present
- **Support quote:** physician reviews the file but is not shown AuthStream output

### F15

Red-team testing in Feb 2026 found 1.4x higher denial rate for Spanish-preferred-language members

- **Polarity:** present
- **Support quote:** denial recommendations were 1.4 times more frequent for members whose preferred language is Spanish

### F16

No evidence of intentional discrimination

- **Polarity:** present
- **Support quote:** No document or testimony suggests anyone intended this

### F17

Model retrained March 2026 and Sagebrush believes gap is closed

- **Polarity:** present
- **Support quote:** Sagebrush retrained the model in March 2026 and believes the gap is closed

### F18

Texas AG not notified of disparity or retraining

- **Polarity:** present
- **Support quote:** It has not notified the Texas Attorney General

### F19

Colorado AG not notified and no affected members notified

- **Polarity:** present
- **Support quote:** Sagebrush has not notified the Colorado Attorney General or any member

### F20

Same language disparity appeared in Colorado data

- **Polarity:** present
- **Support quote:** The same disparity appeared in the Colorado data

### F21

San Antonio has ordinance requiring annual algorithmic transparency reports from insurers

- **Polarity:** present
- **Support quote:** City of San Antonio has an ordinance requiring insurers to file annual algorithmic transparency reports

### F22

Sagebrush has not filed San Antonio algorithmic transparency report

- **Polarity:** present
- **Support quote:** Sagebrush has not filed one

### F23

Sagebrush is a private insurer not a governmental entity and does not provide medical treatment

- **Polarity:** present
- **Support quote:** Sagebrush is a private insurer. It does not provide medical treatment and is not a governmental entity

### F24

CEO asks whether NIST program protects Sagebrush in both states

- **Polarity:** present
- **Support quote:** chief executive has asked whether our NIST program protects us in both states

## Issues (9)

### I1

Is AuthStream a high-risk AI system under Colorado AIA, resolving conflict among three advisory sources

- **Status:** dispositive

### I2

Does the 90-second nurse review prevent AuthStream from being a substantial factor under CO AIA

- **Status:** dispositive

### I3

What are Sagebrush Colorado deployer obligations and compliance gaps including timeline

- **Status:** dispositive

### I4

Does the language disparity constitute algorithmic discrimination under CO AIA and what does discovery trigger

- **Status:** dispositive

### I5

Does the language disparity violate Texas TRAIGA

- **Status:** dispositive

### I6

Are either Texas safe harbors available element by element

- **Status:** dispositive

### I7

Can the San Antonio algorithmic transparency ordinance be enforced

- **Status:** dispositive

### I8

Does any Texas disclosure duty apply to Sagebrush

- **Status:** collateral

### I9

What does the NIST program achieve and not achieve in each state

- **Status:** dispositive

## Rules (18)

### R1

High-risk AI system definition: AI system that makes or is substantial factor in consequential decision

- **Citation:** CO AIA 6-1-1701(7)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R2

Substantial factor definition with anti-rubber-stamp provision for human review based primarily on AI output

- **Citation:** CO AIA 6-1-1701(9)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R3

Consequential decision includes provision/denial of health-care services and insurance

- **Citation:** CO AIA 6-1-1701(3)(e),(g)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R4

Algorithmic discrimination: unlawful differential treatment/impact based on protected class including limited English proficiency

- **Citation:** CO AIA 6-1-1701(1)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R5

Deployer obligations: risk mgmt program, impact assessment, annual review, website statement, consumer notice, data correction, appeal

- **Citation:** CO AIA 6-1-1703(2)(a)-(g)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R6

Small deployer exception: fewer than 50 employees AND does not use own data to train

- **Citation:** CO AIA 6-1-1703(6)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R7

Discovery of algorithmic discrimination requires AG and consumer notification within 90 days

- **Citation:** CO AIA 6-1-1704
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R8

Developer obligations: documentation on limitations, training data, uses, monitoring guidance

- **Citation:** CO AIA 6-1-1702
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R9

CO safe harbor: rebuttable presumption if violation discovered through own testing and cured with AG notice within 60 days

- **Citation:** CO AIA 6-1-1706(4)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R10

Prohibits deploying AI with intent to unlawfully discriminate; requires intentional discrimination

- **Citation:** TX TRAIGA 551.051(a)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R11

TX safe harbor: internal testing discovery plus reasonable cure steps plus AG notification

- **Citation:** TX TRAIGA 551.301(c)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R12

TX safe harbor: substantial compliance with NIST AI RMF or recognized AI governance standards

- **Citation:** TX TRAIGA 551.301(d)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R13

TRAIGA expressly preempts all local AI ordinances in Texas

- **Citation:** TX TRAIGA 551.201
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R14

AI disclosure obligation applies only to governmental entities not private entities

- **Citation:** TX TRAIGA 551.101
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R15

Exception for AI performing a preparatory task to an assessment relevant to consequential decision categories

- **Citation:** CO AIA 6-1-1701(7)(d)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R16

Risk management program must be consistent with NIST AI 100-1 or substantially equivalent framework

- **Citation:** CO AIA 6-1-1703(2)(a)(III)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R17

Impact assessment for pre-existing systems due within 90 days after June 30 2026

- **Citation:** CO AIA 6-1-1703(2)(b)(I)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R18

Healthcare provider AI disclosure applies to providers using AI in patient treatment

- **Citation:** TX TRAIGA 551.102
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

## Applications (17)

### A1

Prior-authorization decisions directly affect provision/denial of health-care services (3)(e) and insurance coverage terms (3)(g). AuthStream processes these requests, making consequential decisions.

- **Rule ref:** R3
- **Fact refs:** F2, F3
- **Issue ref:** I1
- **Result:** satisfied

### A2

Nurse reviewers spend only 90 seconds and agree 94% of the time. The statute states human review does not negate substantial factor status if based primarily on AI output. The 90-second review time and 94% agreement rate demonstrate the review is based primarily on AuthStream output.

- **Rule ref:** R2
- **Fact refs:** F3, F4
- **Issue ref:** I2
- **Result:** satisfied

### A3

The preparatory task exception does not apply. AuthStream does not prepare materials for independent human assessment; it generates the substantive recommendation that drives the outcome. The 94% agreement rate shows the nurse ratifies rather than independently assesses. In-house memo incorrectly relies on this exception.

- **Rule ref:** R15
- **Fact refs:** F3, F4, F5
- **Issue ref:** I1
- **Result:** violated

### A4

AuthStream is a substantial factor in consequential decisions (health care and insurance). No exception applies. AuthStream is a high-risk AI system. Outside counsel memo is correct; in-house memo and trade bulletin are wrong.

- **Rule ref:** R1
- **Fact refs:** F2, F3, F4
- **Issue ref:** I1
- **Result:** satisfied

### A5

Sagebrush has 2300 employees, far exceeding the 50-employee threshold. The small deployer exception in 6-1-1703(6) does not apply regardless of whether Sagebrush uses its own data to train.

- **Rule ref:** R6
- **Fact refs:** F1
- **Issue ref:** I3
- **Result:** violated

### A6

Sagebrush satisfies only the NIST framework element (2)(a)(III). It fails: no impact assessment (2)(b); no annual review (2)(c); no website statement (2)(d); denial letters omit AI disclosure (2)(e); no data correction process (2)(f); appeal process does not address AI component (2)(g). Six of seven obligations unmet.

- **Rule ref:** R5
- **Fact refs:** F9, F10, F11, F12, F13, F14
- **Issue ref:** I3
- **Result:** violated

### A7

The 1.4x higher denial rate for Spanish-preferred-language members constitutes differential impact on basis of limited English proficiency and national origin. Whether this rises to algorithmic discrimination depends on whether it violates underlying antidiscrimination law, but the disparity is significant enough to trigger the notification obligation under a reasonable interpretation.

- **Rule ref:** R4
- **Fact refs:** F15, F20
- **Issue ref:** I4
- **Result:** satisfied

### A8

Sagebrush discovered the disparity in February 2026 and has not notified the Colorado AG or affected consumers. Under 6-1-1704, notification is required within 90 days of discovery. While the statute takes effect June 30 2026, the ongoing deployment and historical harm require notification promptly after the effective date.

- **Rule ref:** R7
- **Fact refs:** F15, F19, F20
- **Issue ref:** I4
- **Result:** violated

### A9

TRAIGA 551.051(a) requires intent to unlawfully discriminate. No evidence suggests intentional discrimination. Disparate impact alone does not violate TRAIGA. Sagebrush has not violated the Texas prohibition.

- **Rule ref:** R10
- **Fact refs:** F15, F16
- **Issue ref:** I5
- **Result:** satisfied

### A10

Element 1 (internal testing discovery): satisfied - red-team testing found the disparity. Element 2 (reasonable cure steps): likely satisfied - model retrained March 2026. Element 3 (AG notification): NOT satisfied - Sagebrush has not notified the Texas AG. Safe harbor unavailable due to missing element 3.

- **Rule ref:** R11
- **Fact refs:** F15, F17, F18
- **Issue ref:** I6
- **Result:** partial

### A11

Sagebrush has a NIST AI RMF-aligned program since 2025. If this constitutes substantial compliance with NIST AI 100-1, the NIST safe harbor under 551.301(d) is available. Confidence is medium as depth of compliance is not fully established.

- **Rule ref:** R12
- **Fact refs:** F9
- **Issue ref:** I6
- **Result:** satisfied

### A12

TRAIGA 551.201 expressly preempts all local AI ordinances in Texas. The San Antonio algorithmic transparency ordinance regulates AI systems and is therefore preempted. Sagebrush has no obligation to file the report.

- **Rule ref:** R13
- **Fact refs:** F21, F22
- **Issue ref:** I7
- **Result:** satisfied

### A13

TRAIGA 551.101 disclosure obligation applies only to governmental entities. Sagebrush is a private insurer. No Texas disclosure duty applies.

- **Rule ref:** R14
- **Fact refs:** F23
- **Issue ref:** I8
- **Result:** satisfied

### A14

TRAIGA 551.102 applies to health care service providers using AI in patient treatment. Sagebrush is an insurer, not a provider, and does not provide medical treatment. This provision does not apply.

- **Rule ref:** R18
- **Fact refs:** F23
- **Issue ref:** I8
- **Result:** satisfied

### A15

The NIST AI RMF program satisfies CO AIA 6-1-1703(2)(a)(III) framework consistency requirement. However, this is only one element of seven deployer obligations.

- **Rule ref:** R16
- **Fact refs:** F9
- **Issue ref:** I9
- **Result:** satisfied

### A16

CO safe harbor requires discovery through own testing (satisfied - red-team testing) AND cure plus AG notification within 60 days (NOT satisfied - no AG notification). Safe harbor unavailable in Colorado.

- **Rule ref:** R9
- **Fact refs:** F15, F17, F19
- **Issue ref:** I4
- **Result:** partial

### A17

AuthStream was deployed before June 30 2026. Impact assessment must be completed within 90 days after June 30 2026 (by September 28 2026). No impact assessment exists. Deadline is approaching.

- **Rule ref:** R17
- **Fact refs:** F2, F10
- **Issue ref:** I3
- **Result:** violated

## Conclusions (9)

### C1

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A1, A2, A3, A4

### C2

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A2

### C3

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A5, A6, A15, A17

### C4

- **Determination:** non-compliant
- **Confidence:** medium
- **Support refs:** A7, A8, A16

### C5

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A9

### C6

- **Determination:** conditional
- **Confidence:** medium
- **Support refs:** A10, A11

### C7

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A12

### C8

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A13, A14

### C9

- **Determination:** conditional
- **Confidence:** high
- **Support refs:** A15, A11

## Obligations (15)

### O1

Formally classify AuthStream as high-risk AI system and adopt outside counsel analysis

- **Required by:** R1
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** Before 2026-06-30

### O2

Complete impact assessment for AuthStream per 6-1-1701(8) requirements

- **Required by:** R17
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-09-28

### O3

Redesign denial letters to disclose AI involvement before consequential decision per 6-1-1703(2)(e)

- **Required by:** R5
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O4

Publish website statement summarizing high-risk AI systems and discrimination risk management per 6-1-1703(2)(d)

- **Required by:** R5
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O5

Implement consumer data correction process for AuthStream per 6-1-1703(2)(f)

- **Required by:** R5
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O6

Redesign appeal process to address AI component and show AuthStream output to reviewer per 6-1-1703(2)(g)

- **Required by:** R5
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O7

Notify Colorado AG of language disparity algorithmic discrimination per 6-1-1704(a)

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 90 days from 2026-06-30

### O8

Notify affected Colorado consumers of language disparity per 6-1-1704(b)

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 90 days from 2026-06-30

### O9

Conduct annual review of AuthStream deployment for algorithmic discrimination per 6-1-1703(2)(c)

- **Required by:** R5
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** Annually from 2026-06-30

### O10

Notify Texas AG of disparity and retraining to preserve internal testing safe harbor per 551.301(c)

- **Required by:** R11
- **Status:** recommended
- **Jurisdiction:** Texas
- **Deadline:** As soon as practicable

### O11

Document TRAIGA preemption of San Antonio ordinance; do not file transparency report

- **Required by:** R13
- **Status:** recommended
- **Jurisdiction:** Texas
- **Deadline:** Not specified

### O12

Request developer documentation from Calyx Decision Systems per 6-1-1702 requirements

- **Required by:** R8
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** Before 2026-06-30

### O13

Audit NIST AI RMF program for completeness against all four core functions and algorithmic discrimination requirements

- **Required by:** R16
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** Before 2026-06-30

### O14

Advise CEO that NIST program alone is insufficient for Colorado compliance - satisfies only one of seven obligations

- **Required by:** R5
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** Immediate

### O15

Verify effectiveness of March 2026 model retraining and document closure of language disparity

- **Required by:** R5
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** Before 2026-06-30

## Graph connections (62)

### E1

- **Src:** F2
- **Dst:** I1
- **Type:** triggers
- **Justification:** AuthStream deployment raises question of high-risk classification

### E2

- **Src:** F3
- **Dst:** I1
- **Type:** triggers
- **Justification:** Auto-approval and recommend-deny outputs indicate consequential decision-making

### E3

- **Src:** F4
- **Dst:** I2
- **Type:** triggers
- **Justification:** 90-second review and 94% agreement rate raise substantial factor question

### E4

- **Src:** F5
- **Dst:** I1
- **Type:** triggers
- **Justification:** In-house memo creates conflict requiring resolution

### E5

- **Src:** F6
- **Dst:** I1
- **Type:** triggers
- **Justification:** Outside counsel memo creates conflict requiring resolution

### E6

- **Src:** F7
- **Dst:** I1
- **Type:** triggers
- **Justification:** Trade bulletin creates conflict requiring resolution

### E7

- **Src:** R3
- **Dst:** A1
- **Type:** applies-to
- **Justification:** Consequential decision definition applied to prior-auth decisions

### E8

- **Src:** R2
- **Dst:** A2
- **Type:** applies-to
- **Justification:** Substantial factor anti-rubber-stamp provision applied to nurse review

### E9

- **Src:** R15
- **Dst:** A3
- **Type:** applies-to
- **Justification:** Preparatory task exception tested against AuthStream facts

### E10

- **Src:** R1
- **Dst:** A4
- **Type:** applies-to
- **Justification:** High-risk definition applied to AuthStream

### E11

- **Src:** A1
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** Consequential decision element confirmed

### E12

- **Src:** A2
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** Substantial factor element confirmed

### E13

- **Src:** A3
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** No exception applies

### E14

- **Src:** A4
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** High-risk classification confirmed

### E15

- **Src:** A2
- **Dst:** C2
- **Type:** fails-element
- **Justification:** Nurse review does not negate substantial factor status

### E16

- **Src:** R6
- **Dst:** A5
- **Type:** applies-to
- **Justification:** Small deployer exception tested

### E17

- **Src:** A5
- **Dst:** C3
- **Type:** fails-element
- **Justification:** Exception unavailable due to employee count

### E18

- **Src:** R5
- **Dst:** A6
- **Type:** applies-to
- **Justification:** All seven deployer obligations tested against Sagebrush measures

### E19

- **Src:** A6
- **Dst:** C3
- **Type:** fails-element
- **Justification:** Six of seven obligations unmet

### E20

- **Src:** F15
- **Dst:** I4
- **Type:** triggers
- **Justification:** Language disparity discovery raises algorithmic discrimination question

### E21

- **Src:** R4
- **Dst:** A7
- **Type:** applies-to
- **Justification:** Algorithmic discrimination definition applied to language disparity

### E22

- **Src:** R7
- **Dst:** A8
- **Type:** applies-to
- **Justification:** Notification obligation applied to discovered disparity

### E23

- **Src:** A7
- **Dst:** C4
- **Type:** satisfies-element
- **Justification:** Disparity likely constitutes algorithmic discrimination

### E24

- **Src:** A8
- **Dst:** C4
- **Type:** fails-element
- **Justification:** No notification provided to AG or consumers

### E25

- **Src:** F16
- **Dst:** I5
- **Type:** triggers
- **Justification:** Lack of intent raises question under TRAIGA intent requirement

### E26

- **Src:** R10
- **Dst:** A9
- **Type:** applies-to
- **Justification:** TRAIGA intent requirement applied to unintentional disparity

### E27

- **Src:** A9
- **Dst:** C5
- **Type:** satisfies-element
- **Justification:** No intent means no TRAIGA violation

### E28

- **Src:** R11
- **Dst:** A10
- **Type:** applies-to
- **Justification:** TX internal testing safe harbor elements tested

### E29

- **Src:** R12
- **Dst:** A11
- **Type:** applies-to
- **Justification:** TX NIST safe harbor tested against existing program

### E30

- **Src:** A10
- **Dst:** C6
- **Type:** fails-element
- **Justification:** Internal testing safe harbor unavailable - no AG notification

### E31

- **Src:** A11
- **Dst:** C6
- **Type:** satisfies-element
- **Justification:** NIST safe harbor likely available

### E32

- **Src:** R13
- **Dst:** A12
- **Type:** applies-to
- **Justification:** TRAIGA preemption applied to San Antonio ordinance

### E33

- **Src:** A12
- **Dst:** C7
- **Type:** satisfies-element
- **Justification:** Ordinance preempted - no filing obligation

### E34

- **Src:** R13
- **Dst:** F21
- **Type:** preempts
- **Justification:** TRAIGA 551.201 preempts San Antonio local AI ordinance

### E35

- **Src:** R14
- **Dst:** A13
- **Type:** applies-to
- **Justification:** Government-only disclosure tested against private insurer

### E36

- **Src:** A13
- **Dst:** C8
- **Type:** satisfies-element
- **Justification:** No disclosure duty for private entities

### E37

- **Src:** R16
- **Dst:** A15
- **Type:** applies-to
- **Justification:** NIST framework requirement tested against existing program

### E38

- **Src:** A15
- **Dst:** C9
- **Type:** satisfies-element
- **Justification:** NIST program satisfies framework consistency element only

### E39

- **Src:** A6
- **Dst:** C9
- **Type:** fails-element
- **Justification:** NIST program does not satisfy other six deployer obligations

### E40

- **Src:** R5
- **Dst:** O3
- **Type:** triggers
- **Justification:** Consumer notice obligation requires denial letter redesign

### E41

- **Src:** R5
- **Dst:** O4
- **Type:** triggers
- **Justification:** Website statement obligation

### E42

- **Src:** R5
- **Dst:** O5
- **Type:** triggers
- **Justification:** Data correction obligation

### E43

- **Src:** R5
- **Dst:** O6
- **Type:** triggers
- **Justification:** Appeal process obligation

### E44

- **Src:** R7
- **Dst:** O7
- **Type:** triggers
- **Justification:** AG notification obligation upon discovery of algorithmic discrimination

### E45

- **Src:** R7
- **Dst:** O8
- **Type:** triggers
- **Justification:** Consumer notification obligation upon discovery of algorithmic discrimination

### E46

- **Src:** R17
- **Dst:** O2
- **Type:** triggers
- **Justification:** Impact assessment deadline for pre-existing systems

### E47

- **Src:** R11
- **Dst:** O10
- **Type:** triggers
- **Justification:** TX AG notification recommended to preserve safe harbor

### E48

- **Src:** R13
- **Dst:** O11
- **Type:** triggers
- **Justification:** Preemption analysis should be documented

### E49

- **Src:** R8
- **Dst:** O12
- **Type:** triggers
- **Justification:** Developer documentation needed from Calyx for impact assessment

### E50

- **Src:** R9
- **Dst:** A16
- **Type:** applies-to
- **Justification:** CO safe harbor elements tested

### E51

- **Src:** A16
- **Dst:** C4
- **Type:** fails-element
- **Justification:** CO safe harbor unavailable - no AG notification within 60 days

### E52

- **Src:** F5
- **Dst:** A3
- **Type:** contradicts
- **Justification:** In-house memo incorrectly relies on preparatory task exception

### E53

- **Src:** F6
- **Dst:** A4
- **Type:** supports
- **Justification:** Outside counsel correctly identifies substantial factor status

### E54

- **Src:** F7
- **Dst:** A4
- **Type:** contradicts
- **Justification:** Trade bulletin blanket exclusion is unsupported by statutory text

### E55

- **Src:** R18
- **Dst:** A14
- **Type:** applies-to
- **Justification:** Healthcare provider disclosure tested against insurer status

### E56

- **Src:** A14
- **Dst:** C8
- **Type:** satisfies-element
- **Justification:** Sagebrush is not a healthcare provider

### E57

- **Src:** R1
- **Dst:** O1
- **Type:** triggers
- **Justification:** High-risk classification requires formal adoption

### E58

- **Src:** R5
- **Dst:** O9
- **Type:** triggers
- **Justification:** Annual review obligation

### E59

- **Src:** R16
- **Dst:** O13
- **Type:** triggers
- **Justification:** NIST program must be audited for completeness

### E60

- **Src:** F24
- **Dst:** O14
- **Type:** triggers
- **Justification:** CEO question requires corrective advice on NIST program limitations

### E61

- **Src:** F17
- **Dst:** O15
- **Type:** triggers
- **Justification:** Retraining effectiveness must be verified and documented

### E62

- **Src:** A17
- **Dst:** C3
- **Type:** fails-element
- **Justification:** No impact assessment completed against September 28 2026 deadline
