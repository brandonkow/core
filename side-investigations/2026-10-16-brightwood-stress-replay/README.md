# Brightwood calibrated stress replay

Date: 16 October 2026. Parent: `3837218874f6293ef85ad12ca7c8b18522913d6f`. This case-only release completes the authorised P1-P28/S1-S24 financial replay and all three analytical stage reviews. It supersedes prior Brightwood numerical conclusions for the revised assumptions, while preserving every historical file.

**Result: B is the stronger conditional investment expression; neither is a robust purchase-cleared recommendation.** B's split operation at RM3,200 is financially stronger than D at RM3,000. Both produce positive reference profits at the user's fifth-year nett +20% target, but costs and weaker exits materially reduce that result. G0 STOP / G4 not cleared / G9 Defer remains the admission state. This does not mean every conditional investment fails or that current shortfall is a permanent rejection.

| Base, before unpriced costs U | D | B |
|---|---:|---:|
| Nett and initial loan | 495,900 | 499,500 |
| Annual operating cash, first two years | -1,095.84 | 512.88 |
| Total nominal profit: self-paid legal reference | 14,744.35 | 22,912.44 |
| Total nominal profit: advertised legal coverage | 24,176.13 | 32,406.32 |
| Annualised equity IRR, respective references | 2.31% / 4.21% | 3.54% / 5.58% |

The profit clock includes four construction years and five post-handover years. IRR includes construction cash timing. These are not five-year annualised returns. Advertised coverage is an unconfirmed marketing branch, not an authenticated developer contract. Unknown bills U are not silently zero.

Read [financial results](Financial_Underwriting.md), [every stress disposition](Stress_Register.md), [three-stage/G0-G9 review and misses](Three_Stage_Review.md), [source boundaries](Sources.md), and [SOP promotion assessment](SOP_Promotion_Assessment.md). [Inputs](Inputs.json) contains all 28 prior base dispositions plus this release's scenarios/provenance. [Results](Results.json) retains all 104 evaluations. [Monthly ledgers](Base_Monthly_Ledgers.json) make the four bases auditable.

Reproduce from a user-held copy with `node run_replay.js`; the runner prints results without writing files. This release executed the same model and validation functions in an in-memory V8 isolate: 333/333 arithmetic checks passed. No local clone/output, private-data acquisition, site visit, outreach, portfolio allocation, purchase or background task occurred.

Core, master, G0-G9, permanent SOP, decision map and historical releases are unchanged. No parameter is promoted merely because one calibrated case turns positive.
