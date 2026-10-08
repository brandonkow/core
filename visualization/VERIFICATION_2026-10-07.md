# Neural map verification - 2026-10-07

Status: local browser and source/decision checks PASS. Deployment is verified separately against the published commit and served HTML; this report does not pre-claim a live deployment.

## Scope and preservation

Continuation of Claude's map commit `e0ab750ad989f3da955d41790dc061b8aaf99e94` on `claude/modest-fermi-2wstbv`, integrated on top of current main `ca6f5581dfa5ad324b32972b449ff186ca6157d6`. The older branch was not used to replace newer main research. The eight framework/SOP sources retain their recorded SHA-256 values. The master remains `1fbf607a78111bc007736fe0cc8109ad3967939a2dcc7ff54f017b491172e86b`.

The original README reports 41 findings handled by Claude after four review passes. The individual findings, cached review passes and adversarial verifier transcripts were not committed. This verification independently examines the committed artifact; it cannot certify one-for-one closure of those unavailable records. No additional agents were invoked.

## Confirmed findings and fixes

| ID | Reproduction and consequence | Fix | Regression evidence |
|---|---|---|---|
| MAP-V01 | Clear the price field: the calculator treated it as zero and displayed RM1,850 positive coverage with the default rent/fee. Missing rent/fee and negative values were also silently coerced. | Require explicit finite inputs; price must exceed zero, rent and fee must be non-negative. Clear numerical results and show an accessible input message while incomplete/invalid. | Blank/negative inputs for all three fields and zero price suppress results. Valid default remains RM1,992.49 instalment, minus RM142.49 coverage and 5.28% gross. The 6% boundary is tested at RM2,499.99 and RM2,500 rent. |
| MAP-V02 | Select the hypothetical passing preset, then Partially Resolved. Deploy remained possible without any input showing that material residual uncertainty met the master's explicit compatibility and adverse-explanation conditions. A note did not test those conditions. | A conditional residual assessment input defaults to Not demonstrated. Partial divergence remains Defer until the user explicitly represents those existing conditions as evidenced. Changing divergence state resets that assessment. Independent structural Reject and allocation Preserve Capacity retain precedence. | Exhaustive decision matrix and browser tests cover missing/passed/reset residual assessment. This is an input within the existing flag, not a new gate or Core rule. |
| MAP-V03 | At 1440 x 900 with multiple unknowns, the sticky result grew to about 777 px inside a 783 px drawer. Scrolling to the final role control still hit the result overlay. | Let the result scroll normally with the form. | Browser hit-test reaches the actual final role label under the same adverse state. Mobile sheet remains usable. |
| MAP-V04 | The default governance/title-unknown preset still painted green sequential links after an unknown gate. Only STOP/FAIL interrupted the green path. | The sequential trace becomes conditional after the first non-passing gate, including Unknown/Incomplete/Not Assessable/Constraint. | Default preset has three passed spine links and six conditional spine links. G9 precedence is unchanged. |

## Evidence collected

- Reproducible `node visualization/verify.cjs` check: 8 source hashes, 164 source-attributed passages, 35 Core principles, 10 gates, 112 nodes, 299 edges, 16 steps and 7 presets.
- Quotations are checked within their named source document(s). Markdown/whitespace and condensed list punctuation are normalised; this is not a byte-for-byte typography claim or a fresh semantic review of every prose sentence.
- The authoritative master's 13 routing rows are parsed independently. Every required Core-to-gate pair and each stated row count is checked, retaining the documented row-2 drawing simplification.
- All 1,492,992 combinations of the simulator's controls pass the decision invariants. This includes combinations of conditionally hidden inputs; the extra residual input doubles the original raw matrix. Counts: 105 Deploy, 221,079 Defer, 1,161,216 Reject, 110,592 Preserve Capacity. These counts are test states, not properties, probabilities or investment outcomes.
- Actual Edge `154.0.4258.62` rendering and interaction tests: all inspectors, reasoning steps, presets, gate lock, shortfall/transition, residual reset, calculator errors, control reachability, keyboard Enter/ArrowRight, panel/sheet controls, zoom, pointer drag and timed autoplay.
- Layouts: 1440 x 900 light/dark; 1024 x 768 light; 861 x 600 light; 390 x 844 dark; 320 x 568 light. No document-level horizontal overflow or application JavaScript exceptions in those tests.
- Fonts blocked: the map still boots and operates using fallback fonts.
- Desktop dark overview and mobile light divergence-result screenshots were visually inspected in this session. Emulation is not physical-device testing, comprehensive accessibility certification or cross-browser certification.
- HTML SHA-256: `923949805bd7136fac1c1ed44a462253615bb1e500c46a46a1d91da58ac12da5`.

## Reproduction and delivery

`verify.cjs` uses Node built-ins only. Run from any working directory in a checkout with `node visualization/verify.cjs`. For repository-only execution, set `MAP_REMOTE_REF` to an immutable commit with authenticated `gh` available; files are then read directly from GitHub. An optional `MAP_HTML_BLOB` can select an uncommitted blob for pre-publication tests.

`browser_smoke.py` uses Python and `websockets` with a dedicated Chromium/Edge debugging instance, default port 9223. Set `MAP_TEST_URL` to the served map and `MAP_CDP_PORT` if needed. It creates its own test tab; do not point it at a personal browsing session. It changes viewport/theme and exercises the page but writes no project files. The additional timed playback/drag/font-block checks are recorded in the JSON receipt.

The GitHub Actions workflow runs the source/routing/decision checks before publishing only this map to GitHub Pages. Research files are not included in the website artifact. A changed source hash blocks publication until the map is deliberately re-reviewed; never modify the framework merely to satisfy a map test.

Underwriting was paused for this work. Its continuation point remains B07 A46-A53; this map does not change research decisions, close remaining catchments or produce any investment approval.
