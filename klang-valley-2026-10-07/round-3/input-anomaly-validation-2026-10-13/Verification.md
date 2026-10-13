# Verification and limits

Packet KV-INPUT-ANOMALY-2026-10-13. Baseline `fb72d3aa7b7bb9dddf9f549080002b5562266e59`.

## Financial checks completed

- Executed the unchanged financial functions extracted by Python AST from the frozen engine; checked its SHA256 before evaluation. No engine or config edits.
- 64 evaluated chains: 23 labelled branches, 27 inherited single-case stresses (including each twelve-month combined shock), eight annual-neutral root checks and six individual chains underlying two three-asset duration tests. These are model evaluations, not market observations.
- Closed-form debt agrees with amortisation; principal conservation, independent interest-plus-cost break-even and monthly-discounted illustrative8% hurdle all pass.
- Annual-neutral price/rent/fee roots pass. All three material sign reversals pass. Standard instalments remain90%/4%/35years even when actual credit is stressed.
- Both future-buyer illustrations explicitly use90% LTV. The unchanged historical engine's separate80% future-buyer stress output is not used.
- Each original input object is copied intact from programme-final/Inputs.json. New assumptions are labelled branches. Current inputs/results/reproduction code are captured from the in-memory run.
- The three-asset reserve stress uses the inherited monthly Lucentia branch. A favourable zero-Lucentia-fee ending-cash bound still fails150k at both durations; no actual portfolio recommendation follows.

## Evidence checks

Fourteen references and nine exclusion/miss groups separate direct-page text, search-index text, event/listing dates and refresh failures. No authenticated current bill, signed/paid lease, net consideration, contract release, parcel plan, governance statement, lender approval or funded exit-buyer panel was obtained.

A direct advert is evidence of its own claims, not of achieved market terms. No listing-count liquidity, median fair value, room-rent aggregation, nightly-income annualisation, renewedGRR or source-image/site inspection is claimed. The Lucentia flag remains Unresolved.

## Publication controls

The publication payload adds eleven files in this dated packet and modifies only README.md and CURRENT_WORKFLOW.md at repository root. All other baseline blobs must remain identical; the single master, G0-G9, SOP, financial engine/config, map, old validation/failure/backtest/forward/portfolio/terminal records and manifests are outside the change set.

Release_Manifest.json pins baseline and content hashes. The publishing turn checks complete tree parity and exact changed paths before updating main with expected head and force=false, then checks main SHA, compare parity and report readback. Any mismatch prevents declaring publication verified. The final response reports that remote check; this self-contained file does not invent its own future commit SHA.

No persistent local clone or output was created; computation used RAM and Python stdin. Existing local folders, Recycle Bin and ACLs were untouched. No outreach, paid access or background job.
