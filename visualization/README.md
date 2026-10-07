# Decision Engine Neural Map

Interactive single-file visualisation of the [master framework](../Residential_Investment_Framework.md) and its SOP layer, built on 7 October 2026 at the user's request. Open [Decision_Engine_Neural_Map.html](Decision_Engine_Neural_Map.html) in a browser. Fonts load from Google Fonts; without a network connection the page falls back to system fonts and still works.

The map lays the framework out as a left-to-right network: evidence and informed judgment, the Evidence–Judgment Divergence check (four-state logic, families A–D, falsifiable hypothesis, flag status, margin of safety), the 35 frozen Core principles, the ordered G0–G9 gates with their divergence watchpoints and stop rules, the SOP steps and diagnostics, the execution supplement's financial tests, the four G9 decisions and investment roles, and the learning loop (miss record, F1–F12, candidates, promotion threshold). It has three modes:

- **Explore**: hover or click a node to see what feeds it and what it feeds, with the source quote and the provenance of every link.
- **Walk the reasoning**: sixteen steps from evidence intake to G9 and the learning loop.
- **Run a path**: set the evidence state at each gate and see which of the four G9 decisions the framework's precedence rules allow, with the rules that fired.

## Status and boundary

This is a reading aid, not a framework document. It does not amend the master, the Core, G0–G9, the SOP or any release; it adds no gate, G10, causal principle, score or investment validation; and it authorises no outreach or purchase. "Run a path" shows decision logic only, not a case or a signal. Area-based underwriting (regional protocols, Cheras and Klang Valley case files) is excluded on purpose. No existing repository file was changed to add this folder, and the root README navigation was not updated.

## Sources and versions

Built against these files at commit `448b231`:

| Source | SHA-256 |
|---|---|
| Residential_Investment_Framework.md | `1fbf607a78111bc007736fe0cc8109ad3967939a2dcc7ff54f017b491172e86b` |
| sop/Approved_Execution_Supplement.md | `2e62521e1b95eeaae3801020d762d9e76b4005ade30065b50a990ce1eb2f5b74` |
| sop/Founder_QA_Approval_Register.md | `d60b617cc6568670df93d7a9d8269d6b1ae8ebcf707e1880c6528367152cce81` |
| execution-release-2026-10-07/Decision_Execution_Standard.md | `ac13a9c14b7b30908e500ec75b0ad3edaf6f234730c40a3f3322312466c17327` |
| execution-release-2026-10-07/Case_Workpaper_Template.md | `8cc826e2ddfa4194a77543342277c59c0aea6ecb05e487255745f5b18f39abc7` |
| execution-release-2026-10-07/financial_config.json | `ddcbfca298e1ee33a55544f8c25750b17c60a531eccddd62ad6ddc124a4a367c` |
| phase-7/Phase_7_SOP_Addendum.md | `7c637ea580058d526f55acc5be57a847dd14d6e00e5ab507e0e6a48fb9203620` |
| Evidence_Judgment_Divergence_Integration_Audit.md | `3c4928fcfff065f450c1200108bdad83d19c53b7f6dd25c19dfeaae500996096` |

If any of these files changes, the map may be out of date; rebuild it rather than editing the sources to match.

## Provenance conventions

- A **solid** link is stated in the source text: the master's routing table, gate text or execution binding, the approval register's execution destinations, the supplement's routing, or the execution standard.
- A **dashed** link is the map's own reading: the grouping of explanation families A–D onto Core principles, the seven Core principles the routing table does not route (5.3, 5.4, 5.9, 5.12, 5.16, 5.19, 5.31), the field packet → ledger and negative alignment → routing links, unit-level terminal value → G4/G7, and some SOP-step and control links. Each link's inspector text says which.
- Where a stated route would need a long link across the whole map (the field packet's G2–G4/G6 routes, flag status reviewed at G9), the node text states it instead of drawing it.
- Line weight on a Core → gate link is the number of routing-table rows citing it. Routing row 2 ("G0–G5, followed by G6–G9") is drawn only as its G0 and G5 links, but it is counted on every existing 5.29/5.30 link it covers.
- The Core cluster headings are a reading aid; the master lists 5.1–5.35 without groups.

## Checks performed before commit

These checks cover the file's fidelity and behaviour only. They are not market or investment validation.

- 164 quoted passages shown in the page (node and step quotations, stop rules, gate conditions and gate-table cells) match the source text verbatim, with whitespace and Markdown formatting normalised.
- Every Core → gate pair in the 13-row routing table is drawn, apart from the disclosed row-2 simplification, and every drawn pair carries the correct row count. No Core → gate link is marked as stated without a source row.
- The "Run a path" logic was evaluated over all 746,496 input combinations with no violation of the precedence invariants: Reject only for an established structural failure; Preserve Capacity only for an allocation constraint; Deploy only when every gate passes, no flag is unresolved, coverage is verified, any shortfall has an evidenced transition record, and a Special Situation has a validated discount; a current shortfall always sits in the lowest research tier. The seven illustrative paths return the outcomes their cited audit scenarios or standard sections require.
- The coverage calculator uses the same instalment formula as `execution-release-2026-10-07/financial_engine.py` (90% of price, 4%, 420 months).
- Interaction smoke test in desktop light, desktop dark and phone widths: no script errors, no horizontal overflow, all modes and controls exercised.
- A four-lens review (link provenance, decision logic, attribution and scope, code behaviour) raised 41 findings. The review was stopped before its own adversarial verifiers finished, to conserve usage, so each finding was checked against the sources by hand. All were addressed: corrected links, provenance labels, row counts and citations; source wording restored where a step had firmed up "ordinarily yields" or "may be a hard Gate"; Run-a-path inputs relabelled so only an established failure can produce Reject; the shortfall, unresolved flags and unverified coverage carried into every decision's rationale; and fixes for keyboard focus, pointer handling, calculator rounding, and a page-scroll defect in the Run-a-path form. A follow-up adversarial recheck against the committed version confirmed 40 of the 41 as fixed; the remaining keyboard-focus case (entering Run a path from the overview) was then fixed and verified.
