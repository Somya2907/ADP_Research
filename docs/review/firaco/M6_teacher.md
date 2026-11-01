# M6 — VoiceMetric and the AEDT Threshold — teacher FIRACO reasoning

Unverified model output for legal review. Citations, facts, applications, and obligations may be incorrect. Text and node IDs below are preserved from the saved reference graph.

[Read case](../../../data/cases/M6_voicemetric_threshold_nyc.md) · [Review brief](../../PROF_PHILIPP_REVIEW.md)

Teacher: claude-opus-4-6. Source: data/outputs/graphs/M6_reference.json.

Source SHA-256: `3764e246b88ac5ccbcf9928143e52f9cc2c94f4a4302e708e45a94ab8ffd4653`.

The internal audit flags at least one rule below for a suspect NYC §20-875 citation. Other errors may also be present.

## Facts (14)

### F1

Brightwater Media is a Manhattan publisher with 1,100 employees hiring editorial assistants for its NYC office

- **Polarity:** present
- **Support quote:** Brightwater Media is a publisher in Manhattan with 1,100 employees

### F2

ScriptEase converts audio interviews to written transcripts with no score, ranking, or recommendation

- **Polarity:** present
- **Support quote:** ScriptEase converts the audio of recorded interviews into written transcripts. It produces no score, ranking, or recommendation

### F3

VoiceMetric scores candidates 1-10 on communication and role alignment

- **Polarity:** present
- **Support quote:** VoiceMetric analyzes the same recordings and gives each candidate a score from 1 to 10 for communication and role alignment

### F4

VoiceMetric is weighted at 40% in hiring rubric, the highest single weight among four criteria

- **Polarity:** present
- **Support quote:** the VoiceMetric score (40%), a writing test (30%), resume review (20%), and reference checks (10%)

### F5

A human hiring manager makes the final decision

- **Polarity:** present
- **Support quote:** A hiring manager makes the final decision

### F6

Brightwater contends VoiceMetric is not an AEDT because a human decides and the score is only one of four factors

- **Polarity:** present
- **Support quote:** A human makes every hiring decision, and the score is only one of four factors

### F7

Bias audit conducted by Meridian Audit Group, independent of Sonara Labs and Brightwater

- **Polarity:** present
- **Support quote:** a firm with no financial or employment ties to Sonara or Brightwater and no role in building the tool

### F8

Bias audit completed August 2025 using historical data from twelve other employers only

- **Polarity:** present
- **Support quote:** completed in August 2025 and used historical data pooled from twelve other employers that use VoiceMetric

### F9

Brightwater did not contribute its own data to the audit despite having used VoiceMetric since June 2025

- **Polarity:** present
- **Support quote:** Brightwater did not give the auditor any data from its own use of the tool

### F10

By April 2026 Brightwater has ten months of its own VoiceMetric historical data

- **Polarity:** present
- **Support quote:** by April 2026 it has ten months of such data

### F11

Brightwater posted audit summary and distribution date on careers page

- **Polarity:** present
- **Support quote:** Brightwater posted a summary of that audit and VoiceMetric distribution date in a clearly labeled section of its careers page

### F12

Job postings provide 10 business days notice of VoiceMetric use, qualifications assessed, and alternative process instructions

- **Polarity:** present
- **Support quote:** Each job posting states, at least ten business days before screening, that VoiceMetric will be used and which qualifications it assesses

### F13

Brightwater has been using VoiceMetric since June 2025

- **Polarity:** present
- **Support quote:** Since June 2025 it has used two tools when hiring editorial assistants

### F14

No indication Brightwater operates in Texas or Colorado

- **Polarity:** absent
- **Support quote:** Not specified

## Issues (6)

### I1

Is VoiceMetric an AEDT under NYC LL 144, applying the three-prong substantially assist test?

- **Status:** dispositive

### I2

Is ScriptEase covered as an AEDT under NYC LL 144?

- **Status:** dispositive

### I3

May Brightwater rely on a bias audit built from other employers historical data without contributing its own?

- **Status:** dispositive

### I4

Is the August 2025 bias audit still current as of April 2026 and when is a new one needed?

- **Status:** collateral

### I5

Are Brightwater publication and notice practices sufficient under LL 144?

- **Status:** collateral

### I6

Does Texas TRAIGA or Colorado AIA impose additional obligations?

- **Status:** collateral

## Rules (15)

### R1

AEDT means computational process from ML/AI issuing simplified output used to substantially assist or replace discretionary decision making for employment decisions

- **Citation:** NYC LL 144 Section 20-870 (AEDT definition)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R2

Substantially assist means: (i) rely solely on simplified output; (ii) simplified output weighted more than any other criterion; or (iii) simplified output overrules other factors

- **Citation:** DCWP Rule Section 5-300 (substantially assist definition)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R3

Simplified output includes score, tag, classification, ranking, recommendation; excludes tools that translate or transcribe existing text

- **Citation:** DCWP Rule Section 5-300 (simplified output definition)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R4

Employer may not use AEDT if more than one year has passed since most recent bias audit

- **Citation:** NYC LL 144 Section 20-871(a)(1) and DCWP Rule Section 5-301(a)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R5

Employer may rely on audit using other employers data only if employer provided its own historical data or has never used the AEDT

- **Citation:** DCWP Rule Section 5-302(a)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R6

Independent auditor must not be employed by or have financial interest in employer, agency, or developer

- **Citation:** NYC LL 144 Section 20-870 and DCWP Rule Section 5-300 (independent auditor)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R7

Employer must publish bias audit date, summary with data source, unknown category count, applicant numbers, scoring/selection rates, and impact ratios before AEDT use

- **Citation:** DCWP Rule Section 5-303
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R8

Notice to candidates at least 10 business days before use including AEDT disclosure, qualifications assessed, and alternative process/accommodation instructions

- **Citation:** DCWP Rule Section 5-304 and NYC LL 144 Section 20-872
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R9

> Flagged for review: the internal audit reports that the cited NYC §20-875 does not exist. Please verify both citation and proposition.

Civil penalties of $500-$1,500 per violation; each candidate screened with non-compliant AEDT may be separate violation

- **Citation:** NYC LL 144 Section 20-875
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R10

Employer must post AEDT data retention policy, type of data collected, source of data on employment website section with written request instructions

- **Citation:** DCWP Rule Section 5-304(d)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

### R11

Prohibits deploying AI with intent to unlawfully discriminate; requires intentional discrimination not disparate impact

- **Citation:** Texas TRAIGA Section 551.051
- **Authority:** binding
- **Jurisdiction:** TX
- **Effective as of:** 2026-01-01

### R12

TRAIGA does not require private employers to conduct bias audits, impact assessments, or provide candidate notices for AI hiring tools

- **Citation:** Texas TRAIGA Key Compliance Notes
- **Authority:** binding
- **Jurisdiction:** TX
- **Effective as of:** 2026-01-01

### R13

High-risk AI system makes or is substantial factor in consequential decisions; human review does not negate substantial factor if based primarily on AI output

- **Citation:** Colorado AIA Section 6-1-1701(7) and (9)
- **Authority:** binding
- **Jurisdiction:** CO
- **Effective as of:** 2026-06-30

### R14

Deployer obligations include risk management programs, impact assessments, consumer notices, correction rights, and appeal rights

- **Citation:** Colorado AIA Section 6-1-1703
- **Authority:** binding
- **Jurisdiction:** CO
- **Effective as of:** 2026-06-30

### R15

Employer may rely on bias audit using test data only if insufficient historical data is available for statistically significant audit

- **Citation:** DCWP Rule Section 5-302(b)
- **Authority:** binding
- **Jurisdiction:** NYC
- **Effective as of:** 2023-07-05

## Applications (12)

### A1

VoiceMetric is a computational process derived from AI that issues simplified output (scores 1-10) for employment screening decisions. All definitional elements of AEDT are met.

- **Rule ref:** R1
- **Fact refs:** F3
- **Issue ref:** I1
- **Result:** satisfied

### A2

VoiceMetric score is weighted at 40%, exceeding every other criterion (writing test 30%, resume 20%, references 10%). This triggers prong (ii): simplified output weighted more than any other criterion in the set. Brightwater argument that human makes final decision is irrelevant because prong (ii) is met by the weighting structure alone.

- **Rule ref:** R2
- **Fact refs:** F4, F5, F6
- **Issue ref:** I1
- **Result:** satisfied

### A3

ScriptEase produces transcripts only. The DCWP rule explicitly excludes from simplified output the output from tools that transcribe a video or audio interview. ScriptEase falls squarely within this exclusion and is not an AEDT.

- **Rule ref:** R3
- **Fact refs:** F2
- **Issue ref:** I2
- **Result:** satisfied

### A4

DCWP Rule 5-302(a) permits reliance on other employers data only if the employer provided its own historical data or has never used the AEDT. Brightwater had been using VoiceMetric since June 2025 (two months before the August 2025 audit) and did not contribute its own data. Neither exception is satisfied. The audit is invalid for Brightwater.

- **Rule ref:** R5
- **Fact refs:** F8, F9, F13
- **Issue ref:** I3
- **Result:** violated

### A5

The August 2025 audit is facially within the one-year window (would expire August 2026). However, this temporal compliance is moot because the audit is substantively invalid under the data requirements of Rule 5-302(a). Brightwater effectively has no valid audit.

- **Rule ref:** R4
- **Fact refs:** F8
- **Issue ref:** I4
- **Result:** partial

### A6

Meridian Audit Group has no financial or employment ties to Sonara Labs or Brightwater and had no role in building VoiceMetric. The auditor independence requirement is satisfied.

- **Rule ref:** R6
- **Fact refs:** F7
- **Issue ref:** I3
- **Result:** satisfied

### A7

Brightwater posted audit summary and distribution date on careers page, satisfying placement requirements. However, the underlying audit is invalid per A4, so publishing invalid audit results does not achieve compliance. Additionally, the facts do not confirm whether the summary includes all required granular data (scoring rates, impact ratios, unknown category counts, data source explanation).

- **Rule ref:** R7
- **Fact refs:** F11
- **Issue ref:** I5
- **Result:** partial

### A8

Brightwater provides 10 business days notice in job postings identifying AEDT use and qualifications assessed, and includes alternative selection process instructions. This is largely compliant. However, Section 5-304(a) also requires instructions for requesting reasonable accommodation under other laws if available, which is not confirmed in the facts.

- **Rule ref:** R8
- **Fact refs:** F12
- **Issue ref:** I5
- **Result:** partial

### A9

The facts do not indicate whether Brightwater has posted its AEDT data retention policy, type of data collected, source of data, and written request instructions on its employment website section as required by DCWP Rule 5-304(d). This obligation may be unmet.

- **Rule ref:** R10
- **Fact refs:** F11
- **Issue ref:** I5
- **Result:** requires-fact

### A10

No indication Brightwater operates in Texas. Even if it did, TRAIGA only prohibits intentional discrimination and imposes no audit, notice, or assessment requirements on private employers. No facts suggest intentional discrimination.

- **Rule ref:** R11
- **Fact refs:** F14
- **Issue ref:** I6
- **Result:** satisfied

### A11

Colorado AIA is not yet in force (effective June 30, 2026) and no facts indicate Brightwater operates in Colorado. If it did screen Colorado candidates after June 30, 2026, VoiceMetric would likely be a high-risk AI system given the 40% weighting and the substantial factor definition in Section 6-1-1701(9).

- **Rule ref:** R13
- **Fact refs:** F14, F4
- **Issue ref:** I6
- **Result:** requires-fact

### A12

Each use of VoiceMetric to screen a candidate without a valid bias audit constitutes a separate violation under Section 20-875. Brightwater has been using VoiceMetric for ten months with an invalid audit, potentially exposing it to $500-$1,500 per candidate screened.

- **Rule ref:** R9
- **Fact refs:** F13, F10
- **Issue ref:** I3
- **Result:** violated

## Conclusions (7)

### C1

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A1, A2

### C2

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A3

### C3

- **Determination:** non-compliant
- **Confidence:** high
- **Support refs:** A4, A12

### C4

- **Determination:** conditional
- **Confidence:** medium
- **Support refs:** A5

### C5

- **Determination:** conditional
- **Confidence:** medium
- **Support refs:** A7, A8, A9

### C6

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A10

### C7

- **Determination:** compliant
- **Confidence:** high
- **Support refs:** A11

## Obligations (7)

### O1

Obtain a new bias audit of VoiceMetric using Brightwater own historical data or contributing its data to a pooled audit

- **Required by:** R5
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Immediately; each candidate screened without valid audit is a separate violation

### O2

Suspend use of VoiceMetric for screening candidates until a compliant bias audit is completed

- **Required by:** R4
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Immediately

### O3

Publish updated compliant bias audit summary with all required data points on careers page before resuming VoiceMetric use

- **Required by:** R7
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Before resuming use of VoiceMetric

### O4

Confirm candidate notice includes reasonable accommodation request instructions per DCWP Rule 5-304(a)

- **Required by:** R8
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Not specified

### O5

Post AEDT data retention policy, data type, data source, and written request instructions on employment website section

- **Required by:** R10
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** Not specified

### O6

Schedule next bias audit no more than one year after new compliant audit is completed

- **Required by:** R4
- **Status:** mandatory
- **Jurisdiction:** NYC
- **Deadline:** One year from date of new compliant audit

### O7

If screening Colorado candidates after June 30 2026, prepare CO AIA compliance including impact assessments, risk management program aligned with NIST AI RMF, consumer notices, and appeal rights

- **Required by:** R14
- **Status:** recommended
- **Jurisdiction:** CO
- **Deadline:** 2026-06-30

## Graph connections (32)

### E1

- **Src:** F3
- **Dst:** I1
- **Type:** triggers
- **Justification:** VoiceMetric scoring function raises question of AEDT classification

### E2

- **Src:** F4
- **Dst:** I1
- **Type:** triggers
- **Justification:** 40% weighting is central to substantially assist analysis

### E3

- **Src:** F2
- **Dst:** I2
- **Type:** triggers
- **Justification:** ScriptEase transcription function raises question of AEDT coverage

### E4

- **Src:** F9
- **Dst:** I3
- **Type:** triggers
- **Justification:** Failure to contribute own data raises audit data validity question

### E5

- **Src:** F8
- **Dst:** I4
- **Type:** triggers
- **Justification:** August 2025 audit date raises currency question

### E6

- **Src:** R1
- **Dst:** A1
- **Type:** applies-to
- **Justification:** AEDT definition applied to VoiceMetric

### E7

- **Src:** R2
- **Dst:** A2
- **Type:** applies-to
- **Justification:** Three-prong substantially assist test applied to VoiceMetric weighting

### E8

- **Src:** R3
- **Dst:** A3
- **Type:** applies-to
- **Justification:** Simplified output exclusion applied to ScriptEase transcription

### E9

- **Src:** R5
- **Dst:** A4
- **Type:** applies-to
- **Justification:** Data contribution requirement applied to Brightwater audit reliance

### E10

- **Src:** R4
- **Dst:** A5
- **Type:** applies-to
- **Justification:** One-year audit currency rule applied to August 2025 audit

### E11

- **Src:** R6
- **Dst:** A6
- **Type:** applies-to
- **Justification:** Auditor independence requirement applied to Meridian Audit Group

### E12

- **Src:** A2
- **Dst:** C1
- **Type:** satisfies-element
- **Justification:** VoiceMetric meets prong (ii) of substantially assist test confirming AEDT status

### E13

- **Src:** A3
- **Dst:** C2
- **Type:** satisfies-element
- **Justification:** ScriptEase falls within transcription exclusion and is not an AEDT

### E14

- **Src:** A4
- **Dst:** C3
- **Type:** fails-element
- **Justification:** Brightwater cannot rely on audit without contributing own data

### E15

- **Src:** A5
- **Dst:** C4
- **Type:** fails-element
- **Justification:** Audit temporal validity is moot due to substantive data deficiency

### E16

- **Src:** A7
- **Dst:** C5
- **Type:** fails-element
- **Justification:** Published results based on invalid audit do not achieve compliance

### E17

- **Src:** A8
- **Dst:** C5
- **Type:** satisfies-element
- **Justification:** Candidate notice is largely but not fully compliant

### E18

- **Src:** A10
- **Dst:** C6
- **Type:** satisfies-element
- **Justification:** No Texas nexus and TRAIGA imposes no relevant employer obligations

### E19

- **Src:** A11
- **Dst:** C7
- **Type:** satisfies-element
- **Justification:** Colorado AIA not yet in force and no Colorado nexus established

### E20

- **Src:** R5
- **Dst:** O1
- **Type:** triggers
- **Justification:** Data deficiency requires new compliant audit

### E21

- **Src:** R4
- **Dst:** O2
- **Type:** triggers
- **Justification:** No valid audit requires suspension of AEDT use

### E22

- **Src:** R7
- **Dst:** O3
- **Type:** triggers
- **Justification:** New audit requires updated publication of results

### E23

- **Src:** R8
- **Dst:** O4
- **Type:** triggers
- **Justification:** Notice must include reasonable accommodation instructions

### E24

- **Src:** R10
- **Dst:** O5
- **Type:** triggers
- **Justification:** Data retention policy disclosure required

### E25

- **Src:** R4
- **Dst:** O6
- **Type:** triggers
- **Justification:** Annual audit cycle must be maintained

### E26

- **Src:** R14
- **Dst:** O7
- **Type:** triggers
- **Justification:** Colorado AIA readiness if Colorado nexus exists

### E27

- **Src:** A12
- **Dst:** C3
- **Type:** fails-element
- **Justification:** Per-candidate penalty exposure from continued use without valid audit

### E28

- **Src:** F6
- **Dst:** A2
- **Type:** contradicts
- **Justification:** Brightwater argument that human decides is contradicted by prong (ii) analysis showing 40% weight exceeds all other criteria

### E29

- **Src:** R9
- **Dst:** O2
- **Type:** triggers
- **Justification:** Per-violation penalties create urgency to suspend non-compliant AEDT use

### E30

- **Src:** A6
- **Dst:** C3
- **Type:** supports
- **Justification:** Auditor independence is satisfied but does not cure the data contribution deficiency

### E31

- **Src:** F13
- **Dst:** A4
- **Type:** supports
- **Justification:** Brightwater had been using VoiceMetric for two months before audit, negating never-used exception

### E32

- **Src:** A9
- **Dst:** C5
- **Type:** fails-element
- **Justification:** Data retention policy disclosure status unknown, potential additional gap
