# H10 — Brightline Telehealth, Texas and Colorado — teacher FIRACO reasoning

Unverified model output for legal review. Citations, facts, applications, and obligations may be incorrect. Text and node IDs below are preserved from the saved reference graph.

[Read case](../../../data/cases/H10_brightline_telehealth_tx_co.md) · [Review brief](../../PROF_PHILIPP_REVIEW.md)

Teacher: claude-opus-4-6. Source: data/outputs/graphs/H10_reference.json.

Source SHA-256: `cb5a428807b321c32a1f7f997cb2ee4e07dd59aaf1ee98d78cb4b096f5c4a549`.

## Facts (21)

### F1

Brightline is a private telehealth provider HQ in Austin TX with 700 employees treating patients in TX and CO

- **Polarity:** present
- **Support quote:** private telehealth provider headquartered in Austin, Texas, with 700 employees

### F2

SymptomIQ is an in-house AI system suggesting diagnoses and treatment options during video visits in TX

- **Polarity:** present
- **Support quote:** clinicians use SymptomIQ, an AI system built in-house that suggests diagnoses and treatment options

### F3

AI disclosure exists only in ToS accepted at account creation, not on date of visit

- **Polarity:** present
- **Support quote:** discloses its use of AI in one place: the Terms of Service that a patient accepts when first creating an account

### F4

Many patients created accounts more than a year before most recent visit

- **Polarity:** present
- **Support quote:** Many patients created their accounts more than a year before their most recent visit

### F5

Red team by Ironwood found self-harm bypass vulnerability in SymptomIQ chat in Feb 2026

- **Polarity:** present
- **Support quote:** a sequence of prompts could bypass the chat features safety filter and cause it to produce text encouraging self-harm

### F6

No intent to produce self-harm content; engineers fixed within three weeks

- **Polarity:** present
- **Support quote:** Nothing indicates that anyone at Brightline intended this. Engineers fixed the weakness within three weeks

### F7

Brightline did not notify the Texas AG of the self-harm vulnerability or fix

- **Polarity:** present
- **Support quote:** Brightline did not notify the Texas Attorney General

### F8

TX AG sent written notice of alleged disclosure violation on April 2 2026

- **Polarity:** present
- **Support quote:** the Texas Attorney General sent Brightline a written notice of an alleged violation concerning its patient disclosure

### F9

CoverCheck automatically decides acceptance and price tier for CO subscription care plans

- **Polarity:** present
- **Support quote:** CoverCheck, which decides automatically whether an applicant is accepted into Brightline subscription care plans and which of three price tiers

### F10

Brightline trained CoverCheck on its own patient data

- **Polarity:** present
- **Support quote:** Brightline trained CoverCheck on its own patient data

### F11

NIST AI RMF-based risk management program documented since 2025

- **Polarity:** present
- **Support quote:** An AI risk management program built on the NIST AI Risk Management Framework, documented and in place since 2025

### F12

Impact assessment of CoverCheck completed August 2025

- **Polarity:** present
- **Support quote:** An impact assessment of CoverCheck completed in August 2025

### F13

CoverCheck pricing model replaced in January 2026 with no new impact assessment

- **Polarity:** present
- **Support quote:** In January 2026 Brightline replaced CoverCheck pricing model with a new one. It did not perform a new impact assessment

### F14

Website statement about CoverCheck and risk management exists

- **Polarity:** present
- **Support quote:** A statement about CoverCheck and how its risks are managed appears on Brightline website

### F15

AI banner shown only after decision is displayed, not before

- **Polarity:** present
- **Support quote:** An applicant sees a banner reading This decision was made with the help of AI after the acceptance and pricing decision is displayed

### F16

No data correction process and no appeal mechanism exist

- **Polarity:** present
- **Support quote:** There is no process to correct data and no appeal

### F17

March 2026 internal analysis found women placed in highest price tier more often than men with same health profile

- **Polarity:** present
- **Support quote:** CoverCheck placed women in the highest price tier more often than men with the same health profile

### F18

Model corrected April 2026 but no regulator or patient notified

- **Polarity:** present
- **Support quote:** Brightline corrected the model in April 2026. It has notified no regulator and no patient

### F19

General counsel claims NIST program provides safe harbor in both states and no exposure

- **Polarity:** present
- **Support quote:** Our NIST program gives us a safe harbor in both states, and we fixed both problems ourselves, so there is no exposure

### F20

Brightline has 700 employees exceeding 50-employee threshold

- **Polarity:** present
- **Support quote:** 700 employees

### F21

Colorado AIA effective date is June 30 2026 and is not yet in force as of April 2026

- **Polarity:** present
- **Support quote:** Not specified

## Issues (7)

### I1

Whether ToS-only disclosure satisfies TX TRAIGA healthcare provider AI disclosure timing requirement

- **Status:** dispositive

### I2

Whether self-harm vulnerability violated TRAIGA and whether internal-testing safe harbor elements are met

- **Status:** dispositive

### I3

How TX enforcement proceeds after April 2 AG notice including cure period and penalties

- **Status:** dispositive

### I4

What NIST program achieves under TX vs CO law and whether GC safe harbor claim is correct

- **Status:** dispositive

### I5

Whether CoverCheck is high-risk, Brightline roles, and sufficiency of IA notice correction and appeal measures

- **Status:** dispositive

### I6

Whether March 2026 pricing finding is algorithmic discrimination and availability of rebuttable presumption

- **Status:** dispositive

### I7

How TX and CO cure mechanisms differ in structure timing and conditions

- **Status:** collateral

## Rules (21)

### R1

Healthcare provider must disclose AI use to patient on the date treatment or service is provided

- **Citation:** TX TRAIGA §551.102
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R2

Prohibition on deploying AI with intent to incite or encourage self-harm

- **Citation:** TX TRAIGA §551.051(b)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R3

Internal-testing safe harbor requires discovery through testing, reasonable cure steps, and AG notification

- **Citation:** TX TRAIGA §551.301(c)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R4

Substantial compliance with NIST AI RMF provides safe harbor against TRAIGA violations

- **Citation:** TX TRAIGA §551.301(d)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R5

AG must provide written notice and allow 60 days to cure before enforcement

- **Citation:** TX TRAIGA §551.301(e)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R6

Civil penalties $10,000 to $200,000 per violation with possible daily accrual

- **Citation:** TX TRAIGA §551.301(b)
- **Authority:** binding
- **Jurisdiction:** Texas
- **Effective as of:** 2026-01-01

### R7

High-risk AI system defined as AI that makes or is substantial factor in consequential decision

- **Citation:** CO AIA §6-1-1701(7)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R8

Consequential decision includes provision denial cost or terms of healthcare services and insurance

- **Citation:** CO AIA §6-1-1701(3)(e)(g)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R9

Risk management program must be consistent with NIST AI RMF or substantially equivalent framework

- **Citation:** CO AIA §6-1-1703(2)(a)(III)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R10

New impact assessment required within 90 days of intentional and substantial modification

- **Citation:** CO AIA §6-1-1703(2)(b)(III)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R11

Consumer must be notified before the decision is made with five required content elements

- **Citation:** CO AIA §6-1-1703(2)(e)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R12

Consumer must have opportunity to correct incorrect personal data used in consequential decision

- **Citation:** CO AIA §6-1-1703(2)(f)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R13

Consumer must have meaningful opportunity to appeal consequential decision

- **Citation:** CO AIA §6-1-1703(2)(g)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R14

Algorithmic discrimination is unlawful differential treatment or impact disfavoring group based on protected class

- **Citation:** CO AIA §6-1-1701(1)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R15

Deployer must notify AG and affected consumers within 90 days of discovering algorithmic discrimination

- **Citation:** CO AIA §6-1-1704
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R16

Rebuttable presumption of reasonable care if violation self-discovered and cured with AG notice within 60 days

- **Citation:** CO AIA §6-1-1706(4)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R17

Deployer rebuttable presumption requires compliance with all of section 6-1-1703

- **Citation:** CO AIA §6-1-1703(3)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R18

Small deployer exception requires fewer than 50 employees AND not using own data to train

- **Citation:** CO AIA §6-1-1703(6)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R19

Violations are deceptive trade practices with AG exclusive enforcement and up to $20,000 per violation

- **Citation:** CO AIA §6-1-1706(1)-(3)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R20

Impact assessment required prior to deployment or within 90 days after June 30 2026 for pre-existing systems

- **Citation:** CO AIA §6-1-1703(2)(b)(I)
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

### R21

Developer obligations including documentation of limitations training data intended uses and monitoring guidance

- **Citation:** CO AIA §6-1-1702
- **Authority:** binding
- **Jurisdiction:** Colorado
- **Effective as of:** 2026-06-30

## Applications (19)

### A1

Section 551.102 requires disclosure on the date treatment or service is provided. Brightline discloses only in ToS at account creation, not on the date of each visit. Many patients created accounts over a year ago. The temporal requirement is not satisfied by a one-time prior ToS acceptance.

- **Rule ref:** R1
- **Fact refs:** F2, F3, F4
- **Issue ref:** I1
- **Result:** violated

### A2

Section 551.051(b) requires intent to incite or encourage self-harm. The facts state nothing indicates anyone at Brightline intended the self-harm output. The vulnerability was unintentional. Without intent, the prohibition is not violated. Brightline is compliant with this provision.

- **Rule ref:** R2
- **Fact refs:** F5, F6
- **Issue ref:** I2
- **Result:** satisfied

### A3

Safe harbor element 1 satisfied: discovery through red-team exercise qualifies as internal testing. Element 2 satisfied: fix within three weeks is reasonable cure. Element 3 NOT satisfied: Brightline did not notify the TX AG. All three elements required; safe harbor unavailable due to missing AG notification.

- **Rule ref:** R3
- **Fact refs:** F5, F6, F7
- **Issue ref:** I2
- **Result:** partial

### A4

NIST AI RMF compliance provides general safe harbor under TX TRAIGA 551.301(d). However, this general governance safe harbor does not override the specific affirmative disclosure obligation in 551.102 which has a clear temporal element. The safe harbor protects against governance-related claims but not specific statutory timing violations.

- **Rule ref:** R4
- **Fact refs:** F11, F19
- **Issue ref:** I4
- **Result:** partial

### A5

AG sent written notice April 2 2026 as required by 551.301(e). Brightline has 60 days (until approximately June 1 2026) to cure the disclosure violation before AG can initiate enforcement proceedings.

- **Rule ref:** R5
- **Fact refs:** F8
- **Issue ref:** I3
- **Result:** satisfied

### A6

CoverCheck automatically decides acceptance and pricing for healthcare subscription plans. This makes consequential decisions about healthcare services under 6-1-1701(3)(e). CoverCheck makes the decision itself, not as a preparatory task. It is a high-risk AI system under 6-1-1701(7).

- **Rule ref:** R7
- **Fact refs:** F9
- **Issue ref:** I5
- **Result:** satisfied

### A7

CoverCheck decisions about acceptance into care plans and price tier assignment are decisions about provision/denial and cost/terms of healthcare services under 6-1-1701(3)(e). These are consequential decisions.

- **Rule ref:** R8
- **Fact refs:** F9
- **Issue ref:** I5
- **Result:** satisfied

### A8

Small deployer exception requires BOTH fewer than 50 employees AND not using own data. Brightline has 700 employees (fails condition a) and uses own patient data to train CoverCheck (fails condition b). Exception does not apply; full deployer obligations attach.

- **Rule ref:** R18
- **Fact refs:** F20, F10
- **Issue ref:** I5
- **Result:** violated

### A9

Brightline has a NIST AI RMF-based risk management program documented since 2025. This satisfies 6-1-1703(2)(a)(III) requirement for consistency with NIST AI RMF. However this is a baseline requirement not a safe harbor under CO law.

- **Rule ref:** R9
- **Fact refs:** F11
- **Issue ref:** I4
- **Result:** satisfied

### A10

Impact assessment completed August 2025 but pricing model replaced January 2026. This is an intentional and substantial modification requiring new IA within 90 days under 6-1-1703(2)(b)(III). No new IA was performed. The 90-day window expired approximately April 2026. Non-compliant.

- **Rule ref:** R10
- **Fact refs:** F12, F13
- **Issue ref:** I5
- **Result:** violated

### A11

Section 6-1-1703(2)(e)(I) requires notice before the decision is made. Brightline shows banner only after the decision is displayed. Additionally the banner lacks required content: purpose, nature of decision, contact info, plain-language description, and instructions to access public statement. Both timing and content fail.

- **Rule ref:** R11
- **Fact refs:** F15
- **Issue ref:** I5
- **Result:** violated

### A12

Section 6-1-1703(2)(f) requires opportunity to correct incorrect personal data. No data correction process exists. Clear non-compliance.

- **Rule ref:** R12
- **Fact refs:** F16
- **Issue ref:** I5
- **Result:** violated

### A13

Section 6-1-1703(2)(g) requires meaningful opportunity to appeal consequential decisions. No appeal mechanism exists. Clear non-compliance.

- **Rule ref:** R13
- **Fact refs:** F16
- **Issue ref:** I5
- **Result:** violated

### A14

CoverCheck placed women in highest price tier more often than men with same health profile. This is differential impact disfavoring individuals based on sex, a protected class. Absent actuarial justification, this likely violates state antidiscrimination laws, meeting the definition of algorithmic discrimination under 6-1-1701(1).

- **Rule ref:** R14
- **Fact refs:** F17
- **Issue ref:** I6
- **Result:** violated

### A15

Discovery occurred March 2026 but CO AIA not effective until June 30 2026. Notification obligation under 6-1-1704 arguably does not attach to pre-effective-date discoveries. However if discrimination is ongoing or rediscovered after June 30 2026 the 90-day notification clock will start. Brightline has notified no one. Readiness status: at risk.

- **Rule ref:** R15
- **Fact refs:** F17, F18, F21
- **Issue ref:** I6
- **Result:** partial

### A16

Rebuttable presumption requires: (a) self-discovery through internal processes - satisfied; (b) cure AND AG notification within 60 days - model corrected but AG not notified. Element (b) fails. Presumption unavailable.

- **Rule ref:** R16
- **Fact refs:** F17, F18
- **Issue ref:** I6
- **Result:** violated

### A17

Deployer rebuttable presumption under 6-1-1703(3) requires compliance with all of section 6-1-1703. Brightline fails on impact assessment timing, consumer notice timing and content, data correction, and appeal. Multiple failures defeat the presumption.

- **Rule ref:** R17
- **Fact refs:** F13, F15, F16
- **Issue ref:** I5
- **Result:** violated

### A18

General counsel claims NIST provides safe harbor in both states. In TX, NIST safe harbor under 551.301(d) does not excuse specific 551.102 timing violation. In CO, NIST compliance is a baseline requirement under 6-1-1703(2)(a)(III) not a safe harbor. The GC statement is materially incorrect in both jurisdictions.

- **Rule ref:** R4
- **Fact refs:** F11, F19
- **Issue ref:** I4
- **Result:** partial

### A19

If Brightline fails to cure within 60 days, penalties of $10,000-$200,000 per violation apply with possible daily accrual. Each patient visit without proper disclosure could be a separate violation. For a telehealth company with potentially thousands of daily visits, aggregate exposure could be substantial.

- **Rule ref:** R6
- **Fact refs:** F8
- **Issue ref:** I3
- **Result:** requires-fact

## Conclusions (7)

### C1

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A1

### C2

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A2

### C3

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A3

### C4

- **Determination:** conditional
- **Confidence:** medium
- **Support refs:** A4, A18

### C5

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A10, A11, A12, A13, A17

### C6

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A14, A15, A16

### C7

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A18

## Obligations (12)

### O1

Implement same-day AI disclosure for all TX patient visits before cure period expires

- **Required by:** R1
- **Status:** mandatory
- **Jurisdiction:** Texas
- **Deadline:** 2026-06-01

### O2

Notify TX AG of self-harm vulnerability discovery and cure to preserve safe harbor

- **Required by:** R3
- **Status:** recommended
- **Jurisdiction:** Texas
- **Deadline:** Not specified

### O3

Complete new impact assessment for CoverCheck post-January 2026 modification

- **Required by:** R10
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O4

Redesign consumer notice to be pre-decision with all five required content elements

- **Required by:** R11
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O5

Implement data correction process for CoverCheck applicants

- **Required by:** R12
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O6

Implement meaningful appeal process for CoverCheck decisions

- **Required by:** R13
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O7

Notify CO AG and affected consumers of sex-based pricing discrimination

- **Required by:** R15
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-09-28

### O8

Validate April 2026 model correction fully eliminated sex-based pricing disparity

- **Required by:** R14
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O9

Correct general counsel legal analysis - NIST is not a safe harbor in either state for identified violations

- **Required by:** R4
- **Status:** recommended
- **Jurisdiction:** Texas
- **Deadline:** Not specified

### O10

Establish annual impact assessment schedule for CoverCheck going forward

- **Required by:** R10
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** Not specified

### O11

Document developer obligations for CoverCheck including limitations training data and monitoring guidance

- **Required by:** R21
- **Status:** mandatory
- **Jurisdiction:** Colorado
- **Deadline:** 2026-06-30

### O12

Establish protocol for AG notification following internal testing discoveries in TX

- **Required by:** R3
- **Status:** recommended
- **Jurisdiction:** Texas
- **Deadline:** Not specified

## Graph connections (53)

### E1

- **Src:** F3
- **Dst:** I1
- **Type:** triggers
- **Justification:** ToS-only disclosure raises question of compliance with same-day disclosure requirement

### E2

- **Src:** F4
- **Dst:** I1
- **Type:** supports
- **Justification:** Year-plus gap between ToS acceptance and visit underscores timing deficiency

### E3

- **Src:** R1
- **Dst:** A1
- **Type:** applies-to
- **Justification:** Section 551.102 governs healthcare provider AI disclosure timing

### E4

- **Src:** A1
- **Dst:** C1
- **Type:** fails-element
- **Justification:** ToS disclosure fails on-the-date-of-service timing requirement

### E5

- **Src:** F5
- **Dst:** I2
- **Type:** triggers
- **Justification:** Self-harm vulnerability raises question under 551.051(b)

### E6

- **Src:** F6
- **Dst:** I2
- **Type:** supports
- **Justification:** Absence of intent is material to 551.051(b) analysis

### E7

- **Src:** R2
- **Dst:** A2
- **Type:** applies-to
- **Justification:** Section 551.051(b) governs intent-based self-harm prohibition

### E8

- **Src:** A2
- **Dst:** C2
- **Type:** satisfies-element
- **Justification:** No intent found so prohibition not violated

### E9

- **Src:** R3
- **Dst:** A3
- **Type:** applies-to
- **Justification:** Section 551.301(c) governs internal-testing safe harbor elements

### E10

- **Src:** F7
- **Dst:** A3
- **Type:** fails-element
- **Justification:** Failure to notify AG defeats third element of safe harbor

### E11

- **Src:** A3
- **Dst:** C3
- **Type:** fails-element
- **Justification:** Safe harbor unavailable due to missing AG notification

### E12

- **Src:** F8
- **Dst:** I3
- **Type:** triggers
- **Justification:** AG written notice initiates cure period analysis

### E13

- **Src:** R5
- **Dst:** A5
- **Type:** applies-to
- **Justification:** Section 551.301(e) governs 60-day cure period after AG notice

### E14

- **Src:** R6
- **Dst:** A19
- **Type:** applies-to
- **Justification:** Section 551.301(b) governs penalty range if cure fails

### E15

- **Src:** F19
- **Dst:** I4
- **Type:** triggers
- **Justification:** GC safe harbor claim raises question of NIST program legal effect

### E16

- **Src:** R4
- **Dst:** A4
- **Type:** applies-to
- **Justification:** TX NIST safe harbor provision

### E17

- **Src:** R4
- **Dst:** A18
- **Type:** applies-to
- **Justification:** Evaluating GC claim about NIST safe harbor in both states

### E18

- **Src:** R9
- **Dst:** A9
- **Type:** applies-to
- **Justification:** CO NIST requirement as baseline not safe harbor

### E19

- **Src:** A4
- **Dst:** C4
- **Type:** satisfies-element
- **Justification:** NIST provides partial protection in TX but not for specific timing violation

### E20

- **Src:** A18
- **Dst:** C7
- **Type:** fails-element
- **Justification:** GC statement materially incorrect in both jurisdictions

### E21

- **Src:** F9
- **Dst:** I5
- **Type:** triggers
- **Justification:** CoverCheck automated decisions raise high-risk classification question

### E22

- **Src:** R7
- **Dst:** A6
- **Type:** applies-to
- **Justification:** High-risk AI system definition

### E23

- **Src:** R8
- **Dst:** A7
- **Type:** applies-to
- **Justification:** Consequential decision definition for healthcare

### E24

- **Src:** R18
- **Dst:** A8
- **Type:** applies-to
- **Justification:** Small deployer exception analysis

### E25

- **Src:** R10
- **Dst:** A10
- **Type:** applies-to
- **Justification:** Impact assessment timing after substantial modification

### E26

- **Src:** F13
- **Dst:** A10
- **Type:** fails-element
- **Justification:** No new IA after January 2026 model replacement

### E27

- **Src:** R11
- **Dst:** A11
- **Type:** applies-to
- **Justification:** Pre-decision consumer notice requirement

### E28

- **Src:** F15
- **Dst:** A11
- **Type:** fails-element
- **Justification:** Post-decision banner fails pre-decision timing requirement

### E29

- **Src:** R12
- **Dst:** A12
- **Type:** applies-to
- **Justification:** Data correction requirement

### E30

- **Src:** R13
- **Dst:** A13
- **Type:** applies-to
- **Justification:** Appeal requirement

### E31

- **Src:** A10
- **Dst:** C5
- **Type:** fails-element
- **Justification:** Impact assessment non-compliance

### E32

- **Src:** A11
- **Dst:** C5
- **Type:** fails-element
- **Justification:** Consumer notice non-compliance

### E33

- **Src:** A12
- **Dst:** C5
- **Type:** fails-element
- **Justification:** Data correction non-compliance

### E34

- **Src:** A13
- **Dst:** C5
- **Type:** fails-element
- **Justification:** Appeal non-compliance

### E35

- **Src:** F17
- **Dst:** I6
- **Type:** triggers
- **Justification:** Sex-based pricing disparity raises algorithmic discrimination question

### E36

- **Src:** R14
- **Dst:** A14
- **Type:** applies-to
- **Justification:** Algorithmic discrimination definition

### E37

- **Src:** R15
- **Dst:** A15
- **Type:** applies-to
- **Justification:** Notification obligation upon discovery of algorithmic discrimination

### E38

- **Src:** R16
- **Dst:** A16
- **Type:** applies-to
- **Justification:** Rebuttable presumption cure mechanism

### E39

- **Src:** F18
- **Dst:** A16
- **Type:** fails-element
- **Justification:** No AG notification defeats rebuttable presumption

### E40

- **Src:** A14
- **Dst:** C6
- **Type:** fails-element
- **Justification:** Algorithmic discrimination likely present

### E41

- **Src:** A16
- **Dst:** C6
- **Type:** fails-element
- **Justification:** Rebuttable presumption unavailable

### E42

- **Src:** R17
- **Dst:** A17
- **Type:** applies-to
- **Justification:** Deployer rebuttable presumption requires full 6-1-1703 compliance

### E43

- **Src:** A17
- **Dst:** C5
- **Type:** fails-element
- **Justification:** Multiple failures defeat deployer presumption

### E44

- **Src:** R1
- **Dst:** O1
- **Type:** triggers
- **Justification:** Disclosure violation requires same-day disclosure implementation

### E45

- **Src:** R3
- **Dst:** O2
- **Type:** triggers
- **Justification:** Safe harbor preservation requires AG notification

### E46

- **Src:** R10
- **Dst:** O3
- **Type:** triggers
- **Justification:** Stale impact assessment requires new completion

### E47

- **Src:** R11
- **Dst:** O4
- **Type:** triggers
- **Justification:** Notice deficiency requires redesign

### E48

- **Src:** R12
- **Dst:** O5
- **Type:** triggers
- **Justification:** Missing data correction process must be built

### E49

- **Src:** R13
- **Dst:** O6
- **Type:** triggers
- **Justification:** Missing appeal process must be built

### E50

- **Src:** R15
- **Dst:** O7
- **Type:** triggers
- **Justification:** Algorithmic discrimination discovery triggers notification obligation

### E51

- **Src:** R14
- **Dst:** O8
- **Type:** triggers
- **Justification:** Must validate correction eliminated discriminatory impact

### E52

- **Src:** A18
- **Dst:** O9
- **Type:** triggers
- **Justification:** Incorrect legal analysis must be corrected

### E53

- **Src:** R21
- **Dst:** O11
- **Type:** triggers
- **Justification:** Developer obligations apply since Brightline built CoverCheck
