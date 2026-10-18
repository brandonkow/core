# Core — property investigation workspace

Live: https://brandonkow.github.io/core/investigation/

Core is an interactive working demo, not a property database or an automated verification service. Six fictional properties populate a schematic animated district. The existing neural map remains at https://brandonkow.github.io/core/ .

## Experience

Select buildings or searchable property cards; switch illustrative evidence/demand/exit layers, rotate/zoom, pause motion and inspect a schematic floor cutaway. Review evidence provenance and conflicts; record competing explanations and falsifiers. Create and assign tasks, move work through three statuses, retain notes. Compare assets without an invented weighted ranking. Change gross/nett price, rent and management assumptions; calculate the current narrow standard with unknown values preserved. Explicitly assess gates, divergence, coverage, transition and role; view G9 rationale and sequential/conditional labels. Save versioned decision snapshots, inspect historic inputs and export/import the complete workspace.

Evidence status, task completion, scenario economics and reviewer assessments are separate. None claims independent authentication. Demo starting positive assessments are hypothetical. No case is imported from the research programme. Geometry, floor selections and routes are schematic; they are not surveyed plans, measured demand or inspections.

## Source authority

engine.mjs is extracted verbatim from the latest map at source commit `76f018598a8fb8feba518cb3db0b691d42076aa3`, 18 October 2026. FORM, BASE, PRESETS, evaluate, calcStandard and gateTrace retain the map's precedence and gross/nett standard. Tests compare the extracted block against the current map. Source changes fail that check until reconciled.

No frozen Core, G0–G9, SOP parameter or research-admission change. G0 is normalised clearing price, not a catch-all evidence gate. G5 is blocked until G0–G4 survive. Independent structural failure and allocation constraints retain Reject/Preserve Capacity precedence. Full underwriting is not replaced by the narrow calculator.

## Files

- index.html, styles.css, app.mjs: responsive interface.
- scene.mjs: procedural SVG isometric district; no paid 3D assets or external rendering library.
- engine.mjs: source-aligned pure decision/calculation functions.
- data.mjs: fictional fixture provider.
- repository.mjs, contracts.d.ts: runtime validation, browser and HTTP repositories.
- server/server.mjs, server/schema.sql, server/openapi.json: runnable API, SQLite migration and endpoint contract.
- tests.mjs, browser-smoke.cjs: domain, storage, API and UI checks.

## Run

Requires Node 24. UI is buildless: serve the repository root with any static server and open /investigation/. For example: `python -m http.server 8788`. ES modules require HTTP, not file://.

Run `node investigation/tests.mjs`. Browser tests require Playwright 1.62.1 and Chromium or Edge. Set CORE_TEST_URL=http://127.0.0.1:8788/investigation/, optionally CORE_BROWSER_CHANNEL=msedge, then run `node investigation/browser-smoke.cjs`.

## Connect a database

1. Set a random secret of at least 32 characters as CORE_API_TOKEN in the API process environment. Never commit it or embed it in the page.
2. Set CORE_DB_PATH to an absolute path on a persistent volume. SQLite initializes from schema.sql automatically. Default binding is localhost:8792.
3. Set CORE_ALLOWED_ORIGIN to the exact UI origin, e.g. https://brandonkow.github.io, when separate from the API.
4. Run `node investigation/server/server.mjs`. Use a TLS reverse proxy for remote use; configure its body limit, rate limiting and access logs. Pages hosts the static frontend separately.
5. In Core, Data & export → Connect a compatible API. Enter the HTTPS API origin and access token. It loads the remote workspace and never silently uploads browser data.
6. GET/PUT /v1/workspace use Bearer authentication. GET supplies ETag; PUT requires If-Match. Stale writes return 412. Validation failures return 400. Changes retain the previous revision transactionally.
7. Populate through the validated API using schemaVersion 1, kind imported, stable IDs and source provenance. Imported data is not automatically authenticated. Preserve unknown amounts as null.
8. For PostgreSQL or another service, retain the WorkspaceRepository and ETag contract and replace the API persistence implementation. JSON aggregate storage is intentional, not a normalized enterprise database claim.

This is a runnable **single-workspace** backend foundation. GitHub Pages does **not** deploy this API. Before real multi-user use, add identity/tenant authorization, scoped roles, protected audit retention, encryption and backup/restore operations. The shared token supports a trusted pilot; it is not an account system. Uploads/object storage are not implemented; evidence holds references and notes. Tokens stay in browser memory only.

## Storage

localStorage key: core-investigation-v1. Imports validate before replacing the browser workspace and are labelled unverified. Reset affects the browser demo, never connected server data. API connection replaces the displayed workspace only after a successful validated GET. Export before connecting or importing. Save failures remain visible and changes can still be exported. Revision conflicts never silently overwrite remote updates.

Browser snapshots are editable records, not tamper-proof audit logs. The server stores prior aggregate revisions but does not claim authenticated reviewer identity.

## Accessibility

Semantic controls, keyboard scene selection, equivalent property list, visible focus, reduced motion, pause and responsive layouts. Optional Google Fonts have system fallbacks. No analytics, AI API, outreach or paid service. See VERIFICATION.md for tested boundaries.
