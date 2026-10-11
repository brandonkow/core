# Verification and preservation

Release: EVE-MAXIM-PRIVACY-2026-10-12. Baseline: `904574c38b6ecb57ef320f110d3b01bafe85951d`; tree `12a6f66430975ecc726c03bab99a6bc94991540f`. The baseline recursive tree was retrieved completely and contains 688 file blobs.

## Financial verification performed

The unchanged engine source SHA256 is `3ab25fc9d9c100dde0eb7240cada5f53df2b6585be52af9165d8930cd8a64b5a`. The wrapper extracts its three calculation/check functions through Python AST, preserving their code; it does not execute historical file-writing entry points. Sources, inputs and execution stayed in RAM.

Ninety financial evaluations passed the existing closed-form amortisation, principal-conservation, independent interest/cost break-even and monthly-discounted hurdle identities. Coverage includes fourteen explicit scenarios, eighteen stress evaluations, fifty-four evaluations for twenty-seven rank comparisons and four annual-neutral root checks. These are model evaluations, not market observations.

Additional checks establish: both original bases cover the simplified monthly proxy yet have negative annual cash; both lose money at a five-year flat-price exit; cash rank reverses in the stated grid; annual-neutral price/rent roots agree with the frozen engine; common standard instalments remain 90%/4%/35. Actual-credit stresses are labelled separately. Future-buyer illustrations use 90% for both rate/term cases; the engine's legacy separate 80% future-buyer output is not used.

Reproduce from repository root with:

`python klang-valley-2026-10-07/round-3/privacy-validation-2026-10-12/reproduce.py`

The script prints deterministic results to stdout; no output file or external data download is performed. It verifies the frozen engine hash. Financial_Inputs.json retains the two historical source cases unchanged. Alternative prices/rents, recurring paid-month scenarios and costs are separate.

## Publication boundary

Only this new dated packet and the two root navigation files are authorised changes. Release_Manifest.json records payload SHA256 hashes and protected Git blob hashes. The publication procedure verifies new blob hashes, the exact changed-path set, unchanged hashes for every pre-existing file outside the two navigation files, and an expected-head update to main without force. The resulting main commit is the publication receipt; the manifest does not pretend to contain its own future commit hash.

Core, all SOP files, G0-G9, old inputs/results, historical/forward/validation/failure records, terminal/portfolio releases, framework map and Brightwood work are protected. No project counts or Deploy totals advance. No branch, clone, persistent local research output, cleanup, permissions change or scheduler is part of this release.

The decision-map GitHub workflow is path-filtered to framework/map/SOP files; this packet and root navigation do not match those triggers. No new UI, map deployment or live interaction verification is claimed.

## Evidence boundary

Fourteen ledger entries are source references, not fourteen authenticated units. The packet distinguishes direct advertised offers, inferred accommodation mode and search-index transaction summaries. Public calls and body text were inspected; no site visit, photo/plan visual inspection, executed lease, collection audit, management account or lender approval was obtained. Two transaction pages returned 403. No access restriction was bypassed.

The research finding is a bounded public pass and conditional investment thresholds. MJ-P01 remains Unresolved and both cases remain G0 STOP / G9 Defer. The 8 October programme cutoff is preserved separately from this packet's 11-12 October research.
