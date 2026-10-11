# Post-underwriting decision map assessment

Assessment date: 11 October 2026. Research evidence cutoff remains **8 October 2026**. Programme release reviewed: `94639fd807c763e4b873a594065da9cad8892e85`. This assessment follows completed regional and programme integration, as the user required.

## Decision

**Keep the existing map HTML, nodes, routing, calculator and decision rules unchanged.** The map is a framework reading aid; its documented scope intentionally excludes regional cases. The completed research does not establish a new causal mechanism or warrant Core promotion. It tests the existing distinctions rather than replacing them.

Maintain the dated research in the [programme comparison](Cross_Region_Comparison.md), [case/area register](Case_and_Area_Register.md), [portfolio/terminal analysis](Portfolio_and_Terminal_Risk.md) and [continuation record](RESUME_AND_COMPLETION.md). Current repository navigation links this assessment. No individual project's Defer, scenario rent, ranking or observed hold is converted into a universal map rule.

## Why no logic change is warranted

| Programme result | Existing map representation | Consequence |
|---|---|---|
| Positive monthly coverage can coexist with annual losses and terminal recovery risk | Standard coverage, full-cost cashflow and actual/stress finance are separate; G7 and execution controls retain them | No calculator result is promoted into a full underwriting decision |
| Attractive outliers have unresolved evidence / identity / offers | G0 and relevant unit/project gates; divergence investigation and explicit residual uncertainty | No high-yield exception bypasses a gate |
| Family and compact rankings can reverse | Buyer Universe, Asset Fit, unit quality, price-dependent attractiveness and separate research priority | No permanent bedroom preference or owner-only exit rule added |
| Different districts and projects share financing / tenant / exit risk | G8 explicitly maps correlation through future buyer, tenant source, financing regime and exit channel | No postcode-based diversification score added |
| Longer carry and lower bank valuation can defeat an apparently fundable portfolio | G7 forced-hold and G8 scarce-capital/portfolio logic | Keep these dated scenario results in research rather than hard-code a universal 24-month rule |
| Desk completion does not mean Deploy or validated forecasting | Reusable safeguard separating research completion from accuracy; four distinct G9 capital outputs | No “research completed” automatic gate pass |

The existing map already includes Evidence-Judgment Divergence, its four-state logic, four explanation families, falsification, routing and unresolved-risk treatment. It has ten existing gates G0-G9 and no G10. The 35 frozen principles and source distinctions remain authoritative.

## Current verification, 11 October 2026

The repository's unmodified `visualization/verify.cjs` was executed through its supported remote-ref mode against the programme-release commit, using Node 24.15.0 and RAM-only stdin execution. It passed:

- eight source-file SHA256 checks;
- 164 quoted passages, 112 nodes, 299 edges, 35 Core principles and ten gates;
- routing-table provenance and sixteen reasoning steps / seven presets;
- all 1,492,992 configured decision-input combinations;
- 9,021 calculator boundary cases and explicit invalid-input / exact-six-percent checks.

The public [map](https://brandonkow.github.io/core/) returned HTTP 200. Its downloaded HTML SHA256 exactly matched the checked repository HTML:

`9dbe821e6c86d52c5f305b8884aab8344fe73619f6f0357cdc5c9a964ea745bf`

That is also the reconciled HTML identified in the [8 October verification](../../../visualization/VERIFICATION_2026-10-08.md). No new interactive-browser, accessibility, physical-device or cross-browser certification is claimed here. The earlier interaction findings retain their dated evidence; current checks prove source/logic parity and identical published HTML, not a fresh manual UI session.

## Programme completion recheck

Main remained at the programme-release commit before this assessment. The 15 manifest-listed artifacts were read back and hashed, and the remote financial results were rebuilt exactly. All 138 source expressions, 61 catchments, 122 project groups and their current stops remain represented. The prior release's 661 non-navigation blobs remain preserved at that commit.

This current-state recheck supports the [completion audit](Programme_Completion_Audit.md): regional desk passes, cross-region comparison, portfolio/terminal integration, counterexamples, misses and reproducible delivery are complete within the original bounded protocol. Zero Deploy; no every-project census or fresh 11 October market-data refresh is claimed.

The accompanying [machine-readable receipt](Post_Completion_Verification_2026-10-11.json) records the checked commit and results. Subsequent navigation changes do not rewrite historical manifests; evaluate those manifests against their pinned release commits.

## Navigation correction and future triggers

The old AGENTS.md continuation paragraph still pointed to B07 even though current workflow and final releases had advanced. Update that current routing paragraph, root README, round-3 README and CURRENT_WORKFLOW to the completed programme and this map decision. Preserve the rest of the working instructions and all framework/research source files.

Reassess the map if an authoritative framework/SOP source changes, a reproducible UI/logic defect appears, or the user asks for a separate research explorer. Any research overlay would need source dates, evidence holds, provenance and an explicit boundary from the framework simulator. None is automatically created by this assessment.

The next investment work is a finite unit-validation or evidence-driven reopening task from the continuation record. New operating IDs start R366. The user's market-level Red Team discussion concerns the interpretation of mature-family utility versus compact-investor economics and evidenced rent-transition mechanisms; it is not a request for routine documents or an approval requirement for this completed desk release.
