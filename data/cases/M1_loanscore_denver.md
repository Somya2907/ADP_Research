# M1 — LoanScore Denver

## Metadata
- jurisdiction: CO
- doctrinal_area: high-risk AI, consequential decision, deployer obligations
- statutes: CO AIA (SB 24-205) §6-1-1701 through §6-1-1707
- tier: medium
- role: training

## Facts

FinSpark, a Colorado-chartered online lender headquartered in Denver with 240 full-time employees, deploys an AI-based credit underwriting model called "LoanScore." LoanScore takes applicant financial data (credit history, income, debt-to-income ratio, employment status, and bank transaction patterns) and returns a binary approval/denial decision along with a recommended interest rate tier.

LoanScore operates in two modes depending on loan size:
- For loan applications under $15,000: LoanScore fully automates the approval/denial decision with no human review. Approximately 73% of FinSpark's loan applications fall into this category.
- For loan applications of $15,000 or above: A human loan officer reviews the AI recommendation alongside the applicant's file. However, an internal six-month audit completed in September 2025 found that the human loan officer approves the AI's recommendation without modification in 94% of cases in this category.

FinSpark licensed LoanScore from DataCredit Solutions, a Delaware-based AI developer. DataCredit has not provided FinSpark with any model card, dataset documentation, training data summaries, or impact assessment documentation. DataCredit's contract with FinSpark includes a clause stating that "all model documentation is proprietary and confidential."

FinSpark has never conducted its own impact assessment of LoanScore. FinSpark does not have a written risk management policy or program governing AI deployment. FinSpark does not notify loan applicants that an AI system is used in the underwriting decision. There is no mechanism for applicants to correct personal data processed by the AI or to appeal an adverse lending decision through a process that accounts for AI involvement.

The CEO's internal compliance memo, dated October 2025, states: "Because the Colorado AI Act has been delayed to June 30, 2026, we have time to sort this out. Let's revisit in Q2 2026." No further compliance action has been taken as of April 2026.

## Question

As of the expected effective date (June 30, 2026), analyze FinSpark's compliance posture under the Colorado AI Act (SB 24-205). Specifically address: (1) Whether LoanScore is a "high-risk artificial intelligence system" under the statute; (2) Whether FinSpark is a "developer," "deployer," or both; (3) What specific obligations apply to FinSpark in each role; (4) Whether the 94% human agreement rate affects the "substantial factor" analysis; (5) Whether the developer's failure to provide documentation affects FinSpark's obligations; (6) What FinSpark must do to achieve compliance by June 30, 2026. Use the F-I-R-A-C-O structure.
