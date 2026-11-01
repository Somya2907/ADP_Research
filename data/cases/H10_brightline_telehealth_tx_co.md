# H10 — Brightline Telehealth, Texas and Colorado

## Metadata
- jurisdiction: TX, CO
- doctrinal_area: healthcare disclosure timing, safe harbor elements, framework alignment versus full compliance, comparison of cure mechanisms
- statutes: TX TRAIGA (HB 149), CO AIA §6-1-1701–1707
- tier: hard
- role: test
- parties: Brightline Telehealth, SymptomIQ, CoverCheck, Ironwood Security

## Facts

Brightline Telehealth is a private telehealth provider headquartered in Austin, Texas, with 700 employees. It treats patients in Texas and in Colorado.

Texas. During video visits, Brightline clinicians use "SymptomIQ," an AI system built in-house that suggests diagnoses and treatment options. Brightline discloses its use of AI in one place: the Terms of Service that a patient accepts when first creating an account. Nothing is said on the day of a visit. Many patients created their accounts more than a year before their most recent visit.

SymptomIQ also has a patient-facing chat feature. In February 2026 Brightline hired Ironwood Security to run a red-team exercise. Ironwood found that a sequence of prompts could bypass the chat feature's safety filter and cause it to produce text encouraging self-harm. Nothing indicates that anyone at Brightline intended this. Engineers fixed the weakness within three weeks. Brightline did not notify the Texas Attorney General.

On April 2, 2026, the Texas Attorney General sent Brightline a written notice of an alleged violation concerning its patient disclosure.

Colorado. For Colorado residents, Brightline uses a second system, "CoverCheck," which decides automatically whether an applicant is accepted into Brightline's subscription care plans and which of three price tiers the applicant pays. Brightline trained CoverCheck on its own patient data.

Brightline's Colorado measures:
- An AI risk management program built on the NIST AI Risk Management Framework, documented and in place since 2025.
- An impact assessment of CoverCheck completed in August 2025.
- In January 2026 Brightline replaced CoverCheck's pricing model with a new one. It did not perform a new impact assessment.
- A statement about CoverCheck and how its risks are managed appears on Brightline's website.
- An applicant sees a banner reading "This decision was made with the help of AI" after the acceptance and pricing decision is displayed.
- There is no process to correct data and no appeal.

In March 2026 an internal analysis found that CoverCheck placed women in the highest price tier more often than men with the same health profile. Brightline corrected the model in April 2026. It has notified no regulator and no patient.

Brightline's general counsel has summarized the company's position in one sentence: "Our NIST program gives us a safe harbor in both states, and we fixed both problems ourselves, so there is no exposure."

## Question

Provide a jurisdiction-by-jurisdiction compliance assessment of Brightline as of April 2026. Address: (i) whether a disclosure in the Terms of Service satisfies the Texas requirement for health care service providers, considering when the disclosure must be made; (ii) whether the self-harm weakness found by the red team violated Texas law, and whether each element of the internal-testing safe harbor is met; (iii) how Texas enforcement would proceed following the April 2 notice, including the cure period and penalties; (iv) what the NIST program achieves under Texas law and what it achieves under Colorado law, and whether the general counsel's "safe harbor in both states" statement is correct; (v) whether CoverCheck is high-risk, Brightline's role or roles, and whether the impact assessment, notice, correction, and appeal measures are sufficient; (vi) whether the March 2026 pricing finding is algorithmic discrimination, what its discovery requires in Colorado, and whether the rebuttable presumption of reasonable care is available; (vii) how the Texas and Colorado cure mechanisms differ. Conclude with a priority-ordered action list. Use the F-I-R-A-C-O structure.
