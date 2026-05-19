# M2 — TenantRank Boulder

## Metadata
- jurisdiction: CO
- doctrinal_area: high-risk AI, consequential decision, small-deployer exception
- statutes: CO AIA (SB 24-205) §6-1-1701 through §6-1-1707
- tier: medium
- role: test

## Facts

GreenRidge Properties is a Boulder-based residential property management company with 45 full-time employees. It manages 1,200 rental units across 18 apartment complexes in Boulder, Fort Collins, and Colorado Springs.

In February 2026, GreenRidge began using "TenantRank," a machine-learning-based housing applicant screening tool that scores prospective tenants on predicted tenancy risk (likelihood of late payment, lease violation, or early termination). TenantRank was developed entirely in-house by GreenRidge's two-person data science team using five years of GreenRidge's own tenant payment history, lease violation records, and eviction data from its property management system.

TenantRank generates a risk score from 0 to 100 for each applicant. GreenRidge's leasing agents are instructed to use TenantRank scores as "one of several factors" in rental application decisions, alongside credit checks, employment verification, and landlord references. However, internal emails from GreenRidge's VP of Operations to the leasing team, dated March 2026, state: "If TenantRank scores an applicant below 40, we should almost never approve them — the data doesn't lie." A review of decisions from February–April 2026 shows that 96% of applicants with scores below 40 were denied, while 88% of applicants with scores above 60 were approved regardless of other factors.

GreenRidge has taken the following compliance steps:
- Implemented a risk management program in January 2026 modeled on the NIST AI Risk Management Framework 1.0, including documented governance procedures and an assigned AI risk officer (the VP of Operations).
- Completed an initial impact assessment in January 2026 that covers TenantRank's intended purpose, data inputs, potential risks of algorithmic discrimination, and mitigation steps.
- Provides a written disclosure to housing applicants at the time of application submission, stating: "GreenRidge Properties uses data analytics tools to assist in evaluating rental applications."

GreenRidge's outside counsel has advised that the company qualifies for the small-deployer exception under the Colorado AI Act because it has fewer than 50 employees.

## Question

Assess GreenRidge's compliance position under the Colorado AI Act (SB 24-205) as of the expected effective date (June 30, 2026). Specifically address: (1) Whether TenantRank is a "high-risk artificial intelligence system"; (2) Whether the small-deployer exception applies to GreenRidge, analyzing ALL elements of the exception; (3) Whether GreenRidge is acting as both developer and deployer; (4) Whether its current compliance measures are sufficient; (5) What additional obligations apply, if any. Use the F-I-R-A-C-O structure.
