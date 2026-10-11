# Verification and preservation

Release FAMILY-ADOPTION-2026-10-12. Baseline main `67761c77408db4a8f6ed83a5ff762ce9f3428f89`, tree `78704912da2125a346db93c92c84bdcc97125554`. Complete recursive baseline contains 697 file blobs.

## Checks performed

The financial wrapper uses the frozen engine's payment, evaluate and check_financial_identities functions, extracted by Python AST without running its historical file-writing entry point. Engine SHA256:`3ab25fc9d9c100dde0eb7240cada5f53df2b6585be52af9165d8930cd8a64b5a`.

49 evaluations passed: 16 explicit scenarios, 27 stress evaluations and 6 annual-neutral price/rent roots. Checks cover closed-form debt, principal conservation, independent interest/cost nominal exit identity and discounted illustrative hurdle. Standard instalments remain 90% purchase-price LTV / 4% / 35 years under separately labelled actual-finance shocks. Future-buyer illustrations also use 90%; legacy 80% future-buyer output is not used.

All three original scenarios have positive simplified monthly coverage, negative annual cash and a five-year flat-price loss. These assertions passed. No family or management coefficient, additional rent growth or yield compression is introduced. Historical input objects are unchanged.

Run `python klang-valley-2026-10-07/round-3/family-validation-2026-10-12/reproduce.py` from a repository checkout to print deterministic JSON to stdout. The script checks the frozen engine hash. It does not download data or write result files. In this session, sources and execution remained in RAM.

## Publication protocol

Only the new dated packet and root README.md / CURRENT_WORKFLOW.md may change. Verify payload Git blob hashes and exact changed paths; compare every other existing file hash; publish directly to main with expected-head CAS, force=false; verify remote head and published report.

The manifest records payload SHA256 and protected Git blob hashes, excluding its own self-hash; the Git commit pins the complete tree. Publication is evidenced by the resulting main commit and remote verification, not by a fabricated future commit hash in this document.

Core, SOP, G0-G9, old cases/financial inputs/results, validation/failure/forward records, portfolio/terminal work, the prior privacy packet, framework map and paused side task remain unchanged. No persistent local outputs, clone, branch, cleanup, ACL changes or scheduler.

The decision-map workflow does not trigger for this packet/root-navigation change set; no UI or deployment claim is made.

## Evidence boundary

16 new source references and 2 retained historical source records are not 18 independent units. Direct page text, primary institutional context and explicitly labelled search extracts were inspected. No photo/plan visual inspection, executed lease, collection statement, current audited MC account, site visit or lender approval was obtained.

MJ-F01 is Unresolved. Three cases remain G0 STOP / G9 Defer; programme counts and zero Deploy remain unchanged. The historical programme's 8 October cutoff is preserved independently of 12 October research.
