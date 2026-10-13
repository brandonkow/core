# Ten-case synthesis verification

Date: 13 October 2026. Baseline main: `2e4a1c9d7d1c155456f9601fd217baa4044a075b`; baseline tree: `926df19f84d9b8f56694efe5b6b2f862713f95bc`. Publication uses main with an expected-head lease and no force. Work is in memory with direct GitHub delivery; no persistent local clone or research output.

## Calculation and source checks

- Seven source blobs are pinned and byte-hashed: programme inputs, four dated financial-result files, the frozen engine and configuration.
- Ten unmodified historical scenarios and eighteen explicitly held alternatives replayed against the source results.
- Fifty-eight engine evaluations passed closed amortisation, principal conservation, independent interest-plus-cost break-even and monthly discounted-hurdle checks.
- Twenty-eight scenario parity comparisons passed for entry, carry, debt, nominal/illustrative-hurdle exit, flat/lower/higher exit results and monthly status.
- Thirty single-input annual-neutral roots passed through the engine; ten paid-month algebra identities passed. Fractional paid months are a boundary calculation, not an engine occupancy forecast.
- Confirmed nine non-shortfall monthly bases, two annual-positive bases, eight annual-negative bases, ten five-year unchanged-price losses and zero Deploy.
- Displayed rounded tables derive from the machine-readable output. No assumption correction, matched-market claim or numerical qualitative premium was introduced.
- Read-only reproduction prints JSON to stdout; compare parsed JSON with Decision_Sheet.json. It reads exact source bytes and rejects source drift.

The first in-memory run failed a source-byte check because the Windows subprocess decoded non-ASCII stdin without explicit UTF-8. Repository source bytes were rechecked and unchanged. Rerunning with Python `-X utf8` passed all seven source hashes and the financial checks. This was a runtime encoding issue, not a financial or market input correction.

## Scope and preservation

Only five new files in this packet and the two root navigation files are included. All 725 other pre-existing blobs must remain identical against the 727-file baseline. No original case, release manifest, Core, G0-G9, SOP, engine/config, framework map, historical/forward/validation/failure or portfolio/terminal artifact is modified.

Protected source identities:

| Artifact | Git blob |
|---|---|
| Residential_Investment_Framework.md | 43d66d0b22f25a8e4085491ec1db0aa9f2ddac8e |
| execution-release-2026-10-07/financial_engine.py | 2fa3554d4b1358795d658efefe270ac53f27bbda |
| execution-release-2026-10-07/financial_config.json | 3e17c91823b093aa66f0930b2c012510d3b4528f |
| visualization/Decision_Engine_Neural_Map.html | ebc6bd206ee10aa4d6a13eca12aa738b78d0d286 |
| sop/Tenant_Privacy_and_Exit_Demand_Addendum_2026-10-11.md | bb223fcae99fd2247838bdbf51672d0e52e68df2 |

Publication checks: parse new JSON; validate relative Markdown file targets; check exact allowed paths in the prospective tree; compare all baseline blobs; compare the new commit with its parent; update main only if its head still matches; read main and the report back. The manifest pins payload content and the parent baseline. Commit identity and tree are supplied by Git history, avoiding a self-referential hash.

These are calculation, content and preservation checks. There was no new portal research, authenticated transaction/lease/bill, site inspection, lender approval, observed market outcome, map/UI session or investment execution. The four dated packets retain their source and uncertainty boundaries. Programme coverage stays 61 catchments / 122 project groups / 138 expressions / zero Deploy; Brightwood remains paused.
