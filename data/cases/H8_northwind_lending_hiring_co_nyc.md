# H8 — Northwind Credit, Lending in Colorado and Hiring in New York

## Metadata
- jurisdiction: CO, NYC
- doctrinal_area: developer and deployer in one entity, discovery before the effective date, conflicting advice, expired and outdated audit
- statutes: CO AIA §6-1-1701–1707, NYC LL 144 §20-870 et seq., DCWP Final Rules
- tier: hard
- role: test
- parties: Northwind Credit, UnderwriteOne, HireSignal, Praxis Talent, Dalloway Audit, Fenwick Laurel

## Facts

Northwind Credit is a consumer lender headquartered in Denver, Colorado, with 180 employees, 60 of whom work in an engineering office in Brooklyn, New York.

Lending in Colorado. Northwind's data science team built "UnderwriteOne," which decides personal-loan applications from Colorado residents. Northwind trained it on its own loan performance data. Loans under $10,000 are approved or denied automatically. Larger loans go to an underwriter, who sees UnderwriteOne's recommendation.

In March 2026 an internal fairness test found that approval rates for applicants aged 62 and older were 18 percentage points lower than for younger applicants with similar credit profiles. The cause was a feature measuring "years to expected retirement." A corrected model is scheduled for release in August 2026. Until then the current model remains in use.

Northwind has received three views on what it must do.
- Its outside counsel, Fenwick Laurel LLP, advises in a written memo that continued use of the model after June 30, 2026 would breach the duty of reasonable care, that the discovery triggers notification duties, and that the correction should be accelerated.
- Its chief financial officer says: "We found it before the law took effect, so it doesn't count."
- A fintech trade blog states that a company that both builds and uses its own model "only needs to comply with the deployer section."

Northwind has no AI risk management program, has completed no impact assessment, does not tell loan applicants that an AI system is used, and offers no data correction or appeal. Its website says nothing about UnderwriteOne.

Hiring in New York. For its Brooklyn office, and for remote engineering roles to which New York City residents apply, Northwind uses "HireSignal," a tool licensed from Praxis Talent that ranks applicants. Only the top quarter are interviewed.

HireSignal was audited on April 8, 2025 by Dalloway Audit, a firm with no ties to Northwind or Praxis and no role in building the tool. In December 2025 Praxis retrained HireSignal on new data. No further audit has been performed. Northwind used HireSignal for hiring rounds in January 2026 and March 2026, and has another scheduled for late April 2026.

Northwind's careers page has a clearly labeled section containing the April 2025 audit summary. It does not state HireSignal's distribution date. Applicants receive a notice at least ten business days before screening that names the tool, lists the qualifications assessed, and explains how to request an alternative process.

## Question

Provide a jurisdiction-by-jurisdiction compliance assessment of Northwind as of April 2026. Address: (i) Northwind's role or roles under the Colorado AI Act with respect to UnderwriteOne, and whether the trade blog's statement is correct; (ii) whether UnderwriteOne is high-risk, for both the automated and the underwriter-reviewed loans; (iii) Northwind's Colorado obligations and their deadlines for a system deployed before the effective date; (iv) whether the March 2026 finding is algorithmic discrimination, what follows from discovering it before the effective date while continuing to use the model after it, and how much weight the outside counsel memo, the CFO's view, and the trade blog each carry; (v) whether the rebuttable presumption of reasonable care could be available; (vi) whether the HireSignal audit was valid for the January and March 2026 rounds and will be for the late April round, and whether publication is sufficient; (vii) penalty exposure and enforcement in each jurisdiction. Conclude with a priority-ordered action list. Use the F-I-R-A-C-O structure.
