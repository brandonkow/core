# Verification and continuation

Baseline main: `24b305a7c1ce26b6da116ff0bf23474663150497`.
Model: financial_model.cjs. Config: KV-SOP-FIN-2026-10-16-v2 snapshot in Inputs.json.

## Completed checks

-10unique bases,18unique held alternative expressions; source price/rent/fee values preserved.
-238financial evaluations, including220base/scenario/old-fit-out evaluations and18held alternatives.
-2,048checks: cash/economic conservation, loan-principal identity, independent amortisation, exit break-even roots, peak-funding breakdown, seller-cost totals, base tenancy/commission/repair calendar, arrears overlap, renewal receipts, shock conservation, old-to-new operating bridge and IRR discounted residuals.
-Each base has55paid months and5new-tenant commissions over60months. Same-tenant renewal has59paid months with one initial and four half-month renewal commissions. Persistent crisis has50paid months, initial-only crisis54.
-No synthetic portfolio assets, deleted extreme tests or project-specific rebate/bay defaults inserted.
-All10retain STOP/Defer. 128programme bases remain unreplayed.

## Reproduction

Run `node reproduce.cjs` in this packet in a repository checkout. No packages required. It verifies pinned source Git blob hashes, reads Inputs.json, runs the model and validator, and prints JSON to stdout. It does not fetch market data or modify files. The live checks in this task used the same pure JavaScript model and validator in memory; no local checkout/output was created.

Results.json additionally contains derived comparison rows/counts for reading; the reproduction prints the underlying scenarios/alternatives and validation from which those summary fields are derived. Base monthly ledgers are included in Results.json. Other scenario totals are reproducible using runCase with includeLedger=true.

## Preservation / publication

Build the new tree on the pinned baseline. Only README.md and CURRENT_WORKFLOW.md may change outside this new packet. Verify all other existing blobs, including frozen Core, SOPv2, historical cases, models, manifests and map, remain identical before updatingmain with an expected-head lease. Verify remote main and packet read-back after update.

Checks certify arithmetic and preservation, not present-day market accuracy, full-region replay, legal/tax clearance or investment readiness. No additional Red Team calibration is pending for this completed priority replay.
