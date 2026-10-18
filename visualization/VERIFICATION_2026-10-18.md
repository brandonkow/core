# Map verification — 18 October 2026

The user requested a map refresh while pausing investment research/outreach. This supersedes the 11 October keep-map-unchanged assessment for the visualisation only. No Core or permanent SOP amendment.

## Changes

1. Replaced superseded financial stress descriptions with current SOP v2 execution controls; retained original source quotations and historical financial configuration provenance.
2. Added optional gross loan basis for new launches; rent yield stays on effective nett. Existing three-argument standard calculator and integer-sen boundary behaviour remain compatible.
3. Added a contiguous G0-G8 admission trace; later positive inputs are labelled CONDITIONAL when an earlier gate is unpassed. G5 prerequisite and independent Reject / Preserve Capacity precedence remain unchanged.
4. Added a fourth Current SOP & progress tab with current financial, tenant/privacy and post-completion execution controls. A separate dated research snapshot records 138 replays, zero admission/Deploy and paused unsent enquiries. Case details are linked, not inserted into Core nodes.
5. Extended source verification from 8 to 13 documents and added repeatable browser tests before Pages deployment.

## Source review

The initial source guard correctly detected that Approved_Execution_Supplement.md had gained a 16 October precedence notice. Its remaining body was compared with commit 448b231 and is identical. The expected hash was updated only after that comparison. The five additional SOP/reporting sources are pinned by SHA256. Master, all Core nodes, gate definitions, link routing and the decision evaluator are unchanged.

## Logic verification

Native Node 24.19.0 executed the committed verifier content through stdin against parent 956aca7ae42578233d346c80fbbfe5b4be995c85 and candidate HTML blob 7ecf5ca4ef539aba5ec1ce519accbd9ef50a72f7. No local project checkout/output was created.

- 13 source hashes and 164 source quotations matched.
- 112 nodes, 299 edges, 35 Core principles, ten gates, sixteen steps, seven presets.
- All 1,492,992 decision-input combinations checked, including contiguous-prefix reporting; decision evaluator unchanged.
- 9,021 existing calculator boundaries plus gross/net separation, invalid basis and exact-six-percent controls.
- Dated programme counts checked against the source funnel register.

HTML SHA256: `16ca256e9568a35940541645b609b84be56b5251931984966269d224c0550b7d`.

## Interactive verification

Native Node / Playwright with headless Edge 155.0.4283.45 exercised the RAM-only candidate preview:

- Four modes at 1440x900 light/dark, 1024x768, 861x600, 390x844 dark and 320x568 light.
- All seven decision presets; no downstream green PASS after an unresolved earlier gate.
- Gross/net input switch, invalid gross/blank price, resale reset and exact 6% display.
- Reasoning step controls, zoom buttons, panel toggle and mobile details sheet.
- Current progress counts, dates, source links and stress text; no horizontal document overflow or page-script errors.

A desktop screenshot at 1100x760 was visually inspected. These are automated desktop/browser-emulation checks, not physical-phone or exhaustive cross-browser certification. The first browser harness attempt used innerText on an SVG text element; it was corrected to textContent, then all checks passed. This was a test-harness issue, not a suppressed product failure.

The app browser/Node-REPL tools were unavailable due to a kernel-assets path error; verification used the installed native Node and an isolated headless browser instead.

## Reproduction and publication

Run `node visualization/verify.cjs`. For UI checks, install Playwright 1.62.1 with Chromium, serve visualization/, set MAP_TEST_URL to the HTML URL and run `node visualization/browser_smoke.cjs`. Optional MAP_BROWSER_CHANNEL=msedge selects installed Edge. The screenshot option emits an in-memory image only; no output file is written.

GitHub Actions now runs source/logic and browser verification before publishing the map-only site. Deployment and hosted HTML verification are checked after the guarded main update and reported in the completion message; local checks alone do not claim hosted success.

Existing verification reports remain historical. Investment enquiries remain paused; no contact, loan application, booking or purchase occurred.
