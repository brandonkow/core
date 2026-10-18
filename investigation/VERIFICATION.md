# Core verification — 18 October 2026

Source baseline: 76f018598a8fb8feba518cb3db0b691d42076aa3.
The latest map and research status were read before building. No research, financial SOP or Core amendment is included.

## Verified before publication

- Extracted engine block matches the 18 October map byte-for-byte. New module exports do not alter evaluation.
- Domain checks: structural Reject precedence, independent Preserve Capacity, unknown reference-price stop, contingent downstream gates, shortfall/transition handling, special-situation discount requirement, divergence and gross/nett finance separation.
- Workspace validation rejects malformed versions, invalid gate values, duplicate property IDs and non-finite money. Null money survives validation and produces Unknown in the UI.
- Browser adapter serializes/restores the aggregate. Bad stored JSON fails visibly without overwriting it.
- Actual Node 24 SQLite API: authentication and origin checks, valid writes, validation rejection, required If-Match, stale-write rejection and ETag response.
- SQLite file-backed data and revision survived closing and reopening the API. Test database files were removed afterward.
- Actual UI → HTTP adapter → SQLite round trip saved a note. A competing update produced a visible conflict and preserved the local edit for export.
- Playwright with installed Edge: select/search properties, change scene layers, cutaway, rotation, zoom/pause; evidence status and hypotheses; add/assign/move task; gross/nett recalculation and unknown rent; gate failure → Reject; snapshot and reload persistence; JSON export/import, invalid import rejection and HTML injection escaping.
- Navigation across all six primary screens at 1024, 390 and 320 pixels without document overflow; reduced-motion startup. Desktop and 390-pixel screenshots visually inspected. No page-script errors.

The development preview ran from an in-memory file map; no repository clone or output was written into the research directory. Temporary screenshots were used for visual QA. tests.mjs and browser-smoke.cjs are committed for reproduction against normal checkout files in CI. The preview harness replaced module/filesystem loading only; GitHub Actions executes the actual committed modules.

## Publication checks

The existing workflow retains full neural-map verification and browser checks, adds Core domain/API/browser verification, and stages only frontend runtime assets under /investigation/. The original map remains at the root. The API is not deployed to Pages.

## Limits

Browser automation and emulation are not physical-device or exhaustive cross-browser certification. SQLite and the API were tested locally, not against a deployed database service. No real properties, verified leases, uploaded documents, account system, production authorization, backups or external integrations are asserted. The district and routes are schematic, not a geographic digital twin. Evidence review is an analyst workflow status; it does not authenticate an external source. Full finance remains in the SOP, beyond the narrow standard calculator.

Synthetic scenarios, data adapter boundaries, deployment instructions and production gaps are documented in README.md.
