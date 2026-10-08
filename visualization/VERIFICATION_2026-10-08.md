# Neural map reconciliation verification - 2026-10-08

Status: PASS for the reconciled map, prepared on the former `claude/modest-fermi-2wstbv` branch and merged into main on 8 October 2026 (`9b46aa5`). The branch was then deleted at the user's request; its commits stay reachable from main through that merge. This tests the file's fidelity and behaviour only; it is not market or investment validation.

## What was found on main

Main at `77b8ecf` (served at the Pages URL with HTML SHA-256 `923949805bd7136fac1c1ed44a462253615bb1e500c46a46a1d91da58ac12da5`) was built from commit `e0ab750`. It passed `node visualization/verify.cjs`, but five defects that the branch had already fixed in `83ae4a0` and `1882c08` were present. Each was reproduced in headless Chromium:

| Defect | Reproduction on main |
|---|---|
| Calculator floating-point boundary | Price RM300,022 with rent RM1,500.11 is exactly 6% gross, but read "5.999999% · below". Over 3,007 prices, entering the page's own "Rent for 6% gross" read "below" 86 times. Entering its "Rent for zero coverage" showed "RM 0.00 · Positive · surplus" 1,508 times. Price RM102,414 gave a 6% rent of RM512.08; the exact figure is RM512.07. |
| Focus lost entering Run a path from the overview | Run mode has no h2, so focus fell to the document body. |
| Focus lost after arrow keys, Escape and Play | Only click-driven re-renders restored focus. |
| Badge overflow | "CONSTRAINT · SHORTFALL" on G8 ended at x 1192.7, past the gate box edge at 1186. |
| Three-finger pinch jump | Lifting one finger of three moved the zoom from scale 0.851 to 1.873 with no movement. |

## Reconciliation

`45c82e7` merges main with its tree unchanged. The next commit re-applies the five fixes on top of main's map and keeps MAP-V01 to MAP-V04 as they were. The calculator keeps the continuation's input validation and error message. Its arithmetic moves into the pure function `calcStandard`, which works in integer sen and uses BigInt for the 6% comparison and the truncated yield. A price that rounds to zero sen is now rejected.

## Evidence

- `node visualization/verify.cjs`: PASS. 8 source hashes, 164 passages, 299 edges, all 1,492,992 decision-input combinations (105 Deploy, 221,079 Defer, 1,161,216 Reject, 110,592 Preserve Capacity, unchanged from main) and 9,021 new calculator cases. Those cases cover prices RM100,000 to RM1,600,000 with three fee levels. In each, the 6% rent meets the preference and one sen less does not, and the zero-coverage rent gives non-negative coverage and one sen less does not. The exact RM300,022 / RM1,500.11 boundary and the RM102,414 → RM512.07 case are explicit assertions.
- Headless Chromium regression run over the same five defects: all fixed. Focus lands on the verdict in Run mode and stays on the step button after arrow keys. The G8 badge ends at x 1178 inside the box. The three-finger case keeps scale 0.851. The calculator gave 0 of 3,007 failures for each boundary type.
- The continuation's browser assertions, replayed in Playwright because `browser_smoke.py` needs the Python `websockets` package, which this environment lacks. All of them passed: 112 nodes; partial divergence defaults to Defer, the explicit residual pass gives Deploy, and changing the flag resets it; the spine shows 3 passed and 6 conditional links on the default preset; the final form input is reachable under a long result; calculator default, blank and negative inputs for all three fields, zero price, and the 2,499.99/2,500 boundary.
- Smoke run in desktop light, desktop dark and phone widths: standards mode, no script errors, no horizontal overflow, 7 presets returning Defer, Defer, Reject, Preserve Capacity, Defer, Defer, Deploy.
- Reconciled HTML SHA-256: `9dbe821e6c86d52c5f305b8884aab8344fe73619f6f0357cdc5c9a964ea745bf`.

## Limits

The merge into main triggers the existing workflow, which runs `verify.cjs` before publishing the map to Pages; the live receipt is recorded separately after deployment. `browser_smoke.py` itself was not run here. Emulated viewports are not physical-device, assistive-technology or cross-browser certification.
