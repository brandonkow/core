# Programme release verification

Date: 8 October 2026. Result: **PASS for the staged remote artifacts and deterministic financial replay.** This verifies arithmetic, source preservation and delivery structure; it is not independent market validation or unit admission.

## Scope and evidence

Base main: `fe7fcf9f57a8b3d8fc0e51fa6ea762e3f895919e`. Checked draft tree: `6861dabb0f6c18bf8744dd707ab7a9dd78ce1a37`. The final release adds this report and its manifest to the verified tree before the expected-head main update.

- Rebuilt the remote Inputs.json and Scenario_Builder.py with the unchanged remote financial engine/config; the entire Financial_Results.json object matched exactly.
- Checked all 138 source case objects against the seven pinned final financial packets; exact equality, including legacy/source fields.
- Verified ten source blob hashes and sizes, source snapshot identities and the global status overlay. All current metadata retains G0 STOP / G9 Defer.
- Confirmed the complete ID set, 61 catchment rows, 138 operating-register rows and 122 project groups.
- Confirmed 74 historical alternative evaluations, 14 forward/price-threshold rows and nine distinct control IDs; forward controls are outside the operating universe.
- Frozen functions checked debt recurrence against closed form, principal conservation, economic-cost recovery identity and discounted hurdle identity. Additional entry/annual identities and adverse scenario direction checks passed.
- Independently reconstructed minimum-month cash paths for every study and scenario from the stored per-case monthly cashflows.
- Replayed 2,622 evaluations, 9,453 expression pairs, 7,381 unique project-pair ranges, seven selected portfolios and 180 rent-grid cells.
- Confirmed five nonnegative annual cases all retain material special holds; the sole flat-price nonnegative case is R208 and remains quarantined.
- Checked 372 relative Markdown links in new workpapers and updated navigation against the remote tree, allowing the two final report/manifest paths being added.
- All 664 prior paths remain. Exactly three pre-existing navigation files change; the other 661 blob identities remain unchanged. This includes Core, engine/config, SOP, historical research/validation/failure/backtests/forward/terminal/portfolio and map assets. All seven pre-existing visualization-directory files are preserved.
- The final expected file count is 677: 664 prior plus 13 new programme files. No local clone/output or cleanup operation was used.

## Frozen master

SHA256: `1fbf607a78111bc007736fe0cc8109ad3967939a2dcc7ff54f017b491172e86b`.

The source remains one consolidated framework. No Core promotion, renamed gate, G10, project example insertion or new permanent screening condition occurred.

## Publication acceptance

The [manifest](Release_Manifest.json) records hashes/sizes of the verified artifacts and this report; it does not self-hash recursively. Publish only using the expected base main, without force, then read back main/tree and every manifest artifact hash/size. A mismatched head must be reconciled rather than overwritten.

No browser interaction or map revision is included in this underwriting verification. Map assessment follows programme publication. The live deployment and UI state are not inferred from these JSON/Markdown checks.
