# Verification and preservation

Release INVESTOR-EXIT-2026-10-13. Baseline main `521d680f56b761ca974a0a9010139dd546c85a53`, tree `ac07d840dff01bc09f19f5cf627a6b90ae1b2b34`; complete baseline contains 706 file blobs.

## Financial verification

The wrapper extracts payment, evaluate and check_financial_identities from the unchanged engine using Python AST, without executing its historical file-writing entry point. Engine SHA256: `3ab25fc9d9c100dde0eb7240cada5f53df2b6585be52af9165d8930cd8a64b5a`. Configuration SHA256: `ddcbfca298e1ee33a55544f8c25750b17c60a531eccddd62ad6ddc124a4a367c`.

**45 financial evaluations passed:** 14 explicit scenarios; 20 individual stresses; four annual-neutral price/rent roots; three carry/exit parity checks; and four individual evaluations aggregated into two joint duration stresses. Ten derived investor-capitalisation illustrations are separate, not extra property observations.

Checks cover amortisation, principal conservation, independent interest/cost exit identity, discounted illustrative hurdle, annual-neutral roots, relative carry and exit parity, and the common 90%/4%/35 standard under separately labelled actual-finance shocks. Both future-buyer illustrations use 90%; the legacy 80% field is excluded from the output.

Original case objects match programme-final/Inputs.json exactly. No price/rent growth, arbitrary diversity coefficient, yield compression or verified-zero cost is assumed. The zero-initial-works scenario is explicitly a counterfactual. Both base monthly balances are positive; both annual balances and five-year unchanged-price profits are negative.

Run `python klang-valley-2026-10-07/round-3/investor-exit-validation-2026-10-13/reproduce.py` from a checkout to print deterministic JSON to stdout. It validates the engine hash, downloads nothing and writes no output files. This session's calculation and publication use RAM/GitHub only.

## Evidence and limitations

Seventeen source references include direct text, indexed advertisements, institutional context and extracted university PDF text. This is not seventeen independent units or verified transactions. The prior Zeva sale condition is explicitly retained historical body evidence. The PDF screenshot did not render; no visual plan, photo or route inspection is claimed.

No executed lease, collections panel, representative tenant-source share, current MC accounts, actual site journey or lender approval was obtained. All seven cases across the three public hypothesis passes remain G0 STOP / G9 Defer; no causal outcome is certified.

## Publication and preservation protocol

Allowed changes: the new dated directory, root README.md and CURRENT_WORKFLOW.md only. Expected result: ten new packet files, two modified navigation files, 704 existing blobs unchanged, total 716 blobs.

Hash each payload using SHA256 and Git blob SHA; validate JSON and relative links; compare the complete new tree against every baseline blob outside the two navigation files. Require exactly the expected changed paths and a single-parent commit before advancing main with expected-head CAS and force=false. Read back the remote head, commit parity and exact report content.

The manifest excludes its own self-hash; the Git commit pins the entire release. It records the protocol rather than inventing a future commit hash. The eventual commit and remote checks establish publication.

Core/G0-G9, SOP, all historical inputs and releases, validation/failure/backtest/forward/terminal/portfolio work, map and paused Brightwood task remain byte-for-byte preserved. No branch, persistent clone, local output, cleanup, ACL change or scheduler. The map workflow's source paths are not modified; no new UI/deployment verification is claimed.
