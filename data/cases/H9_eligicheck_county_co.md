# H9 — EligiCheck County Assistance

## Metadata
- jurisdiction: CO
- doctrinal_area: who is the deployer, government user, own-data ambiguity in the small-deployer exception, authority hierarchy, appeal sufficiency
- statutes: CO AIA (SB 24-205) §6-1-1701 through §6-1-1707
- tier: hard
- role: test
- parties: Juniper County, CivicSort Analytics, EligiCheck, Colorado Counties Technology Council

## Facts

The Juniper County Department of Human Services administers the county's emergency rental and utility assistance program for residents in financial hardship.

Since 2025 the County has contracted with CivicSort Analytics, a company in Durango, Colorado, with 38 full-time employees. CivicSort built and operates "EligiCheck," which recommends whether each application for assistance should be approved or denied. CivicSort built EligiCheck by taking an open-source model and extensively retraining it on eight years of the County's historical case files, which the County supplied under the contract. CivicSort runs EligiCheck on its own servers. County caseworkers see the recommendation in their case-management screen and enter the final decision.

In 2025, caseworkers entered the recommended outcome in 97% of applications, spending an average of two minutes on each.

The parties disagree about who is responsible for what.
- The County Attorney's memo (December 2025) concludes that the Act "regulates businesses, not governments," so the County has no obligations; if anyone is the deployer it is CivicSort, which "operates the system."
- CivicSort's position is that it is "only a contractor," that the County is the deployer because the County makes the decisions, and that in any case CivicSort would fall within the small-deployer exception: it has fewer than fifty employees, and the training data "is the County's, not our own."
- Guidance from the Colorado Counties Technology Council, an association of county IT directors, states that counties using AI in benefit decisions "should treat themselves as deployers."
- A page of frequently asked questions on the Attorney General's website, marked "informal guidance, not a rule," states that an entity that "integrates or uses" a high-risk system in a service is a deployer "regardless of sector."

Current practice:
- No impact assessment exists. CivicSort gave the County a one-page description of EligiCheck. It has provided no documentation of training data, limitations, or intended and inappropriate uses, and publishes nothing about the system.
- Applicants are not told that an AI system is involved. Denial letters give a generic reason.
- An applicant may request a county administrative hearing. The hearing officer reviews the application file but has no access to EligiCheck's recommendation or the factors behind it.
- There is no process for correcting data.
- In January 2026 a County audit found that applications submitted in Spanish were denied at 1.6 times the rate of applications submitted in English, with similar household finances. The audit was circulated internally. Neither the County nor CivicSort has notified anyone or changed the system.

## Question

Assess the positions of Juniper County and CivicSort under the Colorado AI Act (SB 24-205) as of the expected effective date (June 30, 2026). Address: (i) which category or categories of consequential decision are involved, and whether EligiCheck is a high-risk AI system and a substantial factor given caseworker review; (ii) who is the developer and who is the deployer, applying the statutory definitions to each party, and identifying where the text leaves real uncertainty; (iii) whether CivicSort could rely on the small-deployer exception, analyzing both conditions and the meaning of "the deployer's own data"; (iv) how much weight the County Attorney's memo, the Council's guidance, and the Attorney General's FAQ each carry, and your confidence in the resulting conclusion; (v) the obligations of each party and their deadlines; (vi) whether the January 2026 audit finding is algorithmic discrimination and what its discovery requires; (vii) whether the existing administrative hearing satisfies the appeal requirement. Conclude with a priority-ordered action list. Use the F-I-R-A-C-O structure.
