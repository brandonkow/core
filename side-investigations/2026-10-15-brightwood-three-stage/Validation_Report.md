# Validation report — BW-3S-2026-10-15

Date:15October2026. Baseline main: `42587cd6f7aecfac0060ce9cf3c56adc5fc0d891`. This report distinguishes reproducible checks from market validation.

## Completed checks

- Both supplied PDFs read as bytes and SHA256-hashed; all33pages text-extracted. Price table and relevant source layouts/floor plans visually rendered in RAM. P01 pages6,12,13,24,26,27,29,30 and P02 page1 inspected; page29 rechecked at higher resolution.
- Seven type counts total204; main BUA, accessory PES and variable bay entitlements remain separate.
-53scenario evaluations,14type/price endpoint screens,12annual-neutral roots. Each evaluation checks amortisation recurrence against closed form, principal conservation, equity/debt terminal break-even and an independent economic cost identity.
-45payment comparisons with the frozen engine's payment function, including zero rate and different terms/loan sizes, pass. The engine itself was not executed as a file-writing programme or changed.
- Independent JavaScript checks verify all53payments, gross-based standard debt, nett yield denominator, construction-plus-operation duration and terminal cash identity.
- Historical engine/config are preserved. User-authorised gross financing is isolated in this case model. Numerical results consistently use the corrected basis; no nett-based primary loan results remain.
- Rent advertisements are distinguished from achieved rent; conflicting listings excluded from clean anchors. The gross/nett price explanation is recorded as resolved, not an unresolved contradiction.
- All existing G0–G9 names/order are preserved in the assessment; G0/G4 are not passed; G5 is not admitted; G9 is Defer. No G10, Core, SOP or map change.
- Only README.md, CURRENT_WORKFLOW.md and AGENTS.md are planned existing-file changes, all navigation/authority updates. Every other baseline blob must retain its exact SHA in the publication tree. Historical holds/pause records are not overwritten.

## Reproduction

`python financial_model.py < Financial_Inputs.json`

The model reads stdin, uses Python's standard library and prints JSON to stdout. It does not write files. Standard/cost configuration assertions prevent a changed input file silently being interpreted under unchanged hardcoded assumptions. Explicit scenario overrides are documented. Original PDF text/provenance is in PDF_Source_Extracts.json; original binaries are not claimed transferred.

No persistent local clone, generated local output, permission change, deletion or outreach was used. All generated artifacts are prepared in RAM for GitHub main.

## Not verified

No site visit, executable selected-unit offer, contractual plan/specification, permitted final alterations, fee budget/MC financial audit, paid rent, ordinary transfer clearing interval, bank approval, exact rebate/cost settlement schedule, current construction completion or actual personal portfolio. No independently realised outcome validation. No map UI/browser verification is necessary or claimed because map files do not change.

The programme remains61areas/122project groups/138conditional operating expressions, zero Deploy. This side packet completes analytical passes with an explicit Defer; it is not investment-readiness certification.

## Publication verification boundary

The release manifest pins baseline and artifact content hashes. Publish through a tree based on the current parent, inspect preservation, then update main with expected-head protection and no force. After publication, read back every changed/new text artifact and verify main head. Tool receipts and final response record the resulting commit; this pre-publication report does not pretend those later checks have already happened.
