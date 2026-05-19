# H2 — AutoApprove Lending

## Metadata
- jurisdiction: CO
- doctrinal_area: substantial-factor ambiguity, authority hierarchy, deployer obligations
- statutes: CO AIA (SB 24-205) §6-1-1701 through §6-1-1707
- tier: hard
- role: test

## Facts

Helix Credit is a Colorado-based fintech lender headquartered in Denver with 310 employees and approximately $2.1 billion in annual loan originations. Helix operates exclusively in Colorado and serves both consumer and small-business borrowers.

Helix has deployed "AutoApprove," an AI-powered underwriting system developed by FinLogic AI, a San Francisco-based AI developer. AutoApprove operates in a two-stage workflow:

Stage 1 (Automated): AutoApprove scores all incoming loan applications using a proprietary credit-risk model. Applications scoring above the 70th percentile on its risk score are auto-approved; applications scoring below the 40th percentile are auto-denied. These automated decisions are final — no human reviews them before the applicant is notified.

Stage 2 (Human Review): Applications scoring between the 40th and 70th percentiles are routed to a human underwriter. The underwriter receives: (a) the AutoApprove risk score, (b) an AI-generated risk narrative explaining the key factors driving the score, and (c) the underlying applicant financial data.

Internal data from Q4 2025 through Q1 2026 shows:
- 62% of all applications are decided at Stage 1 (automated, no human involvement)
- 38% of applications reach Stage 2 (human review)
- Within Stage 2, human underwriters agree with the direction implied by AutoApprove's score in 71% of cases
- Overall, a human is the final decision-maker in approximately 38% of all lending decisions

Helix's General Counsel has circulated an internal memo (dated February 2026) arguing that AutoApprove is not a "substantial factor" in consequential decisions because "the majority of decisions that involve human judgment reflect independent analysis, not rubber-stamping — the 71% agreement rate simply reflects that the AI and our underwriters reach similar conclusions from the same data."

Separately, Helix commissioned an external compliance analysis from Morrison & Partners LLP, a nationally recognized financial regulation firm. Morrison's memo (dated March 2026) concludes: "Given that 62% of decisions are fully automated and the remaining 38% involve an AI-generated risk narrative that frames the underwriter's analysis, AutoApprove should be considered a 'substantial factor' in making consequential decisions under §6-1-1703 of the Colorado AI Act as of its June 30, 2026 effective date, requiring full deployer obligations."

Current compliance measures:
- Helix has implemented an AI risk management program aligned with the NIST AI Risk Management Framework (NIST AI 100-1), documented in a written policy dated January 2026.
- Helix completed an impact assessment of AutoApprove in February 2026 covering intended purpose, deployment context, data inputs, and algorithmic discrimination risk analysis.
- FinLogic AI has provided Helix with a model card and training data summary.
- Helix has NOT issued consumer notices to any loan applicants regarding AI involvement in underwriting.
- Helix has NOT established a documented process for applicants to correct personal data processed by AutoApprove.
- Helix has NOT established an appeal process that accounts for AI involvement in adverse lending decisions.

## Question

As Helix's compliance counsel, analyze the following as of April 2026 in preparation for the Colorado AI Act's June 30, 2026 effective date:

(1) Whether AutoApprove constitutes a "high-risk artificial intelligence system" under the Colorado AI Act, addressing both the Stage 1 (fully automated) and Stage 2 (human-reviewed) pathways separately.
(2) How to resolve the conflict between the General Counsel's memo and the Morrison & Partners memo. What is the correct hierarchy of authority between an internal legal opinion, an external law firm opinion, and the statute itself?
(3) Whether Helix qualifies as a "deployer," a "developer," or both.
(4) A complete inventory of what Helix must change to achieve compliance by June 30, 2026, distinguishing between what is already done and what remains.
(5) Whether FinLogic AI has separate developer obligations, and whether FinLogic's provision of model documentation is sufficient.

Structure your answer using the F-I-R-A-C-O framework. In your Application section, explicitly address the authority hierarchy — the weight to be given to the GC memo vs. the external memo vs. the statutory text itself.
