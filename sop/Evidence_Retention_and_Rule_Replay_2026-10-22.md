# Evidence retention and rule-change replay

Effective22October2026. User authority: preserve information found for every candidate so later G0-G9 changes can reuse saved data without restarting regional research. This is an execution/data-retention rule, not a Core change or authority to alter G0-G9.

## 1. Separate evidence, assumptions and decisions

Maintain three versioned layers:
1. Evidence: dated observations, source identity, structured comparable rows, product/rights/condition/package facts, contrary observations, failed access and missing facts.
2. Assumptions: approved financial defaults, case overrides, analyst estimates and scenario branches, each with basis and applicable scope.
3. Assessment: rule/Core/SOP/model version, evidence snapshot, gate reasoning, contiguous passed prefix, first unresolved gate, G9 decision, financial outputs and unresolved dependencies.

A new rule must not overwrite what the evidence said or what an earlier assessment concluded. No silent conversion of advertised rent into collected rent, reserve into auction sale, user judgement into independent verification, or unknown into zero.

## 2. Save while researching each candidate

Use stable candidate ID, project/component and unit/product scope. Regional expressions and standalone cases remain separately counted. The central [candidate index](../evidence-registry/Candidate_Records.json) points to immutable GitHub commit/blob records; [record template](../templates/Candidate_Evidence_Record.json) defines the fields for new material.

For every decision-relevant observation retain:
- stable fact/source IDs and candidate links;
- concise structured fact or permitted excerpt; original URL/file, publisher, event date, access date, page/section or table row;
- evidence type: transaction/ask/auction reserve/auction sold/achieved rent/collection/user judgement/assumption/inference;
- area/layout, component/use, tenure/rights, bay, condition/furnishing, package, effective/gross price and rental term where relevant; missing fields explicitly null;
- source independence/duplicate group, contradictions, inclusion/exclusion and confidence with reason;
- affected inputs/gates/mechanisms; material freshness or invalidation trigger;
- retained file/checksum where available, and whether only an extract/index/link was accessible.

Preserve useful disconfirming evidence and rejected comparables with rejection reasons. Keep enough structured information to rerun the reasoning if a page later disappears. A URL alone is not the desired evidence record. Save provided source documents and permitted extracts in GitHub as appropriate; do not fabricate missing originals or imply that every webpage is fully archived. Avoid unnecessary personal data and comply with source access/copying limits.

The candidate index is a retrieval layer, not a replacement for existing ledgers. Baseline input copies retain their original evidence limitations. Legacy blanks are backfilled during normal case work; indexing them is not evidence completion.

## 3. Default response to a rule change: replay stored evidence

1. Identify the exact authorised Core/G0-G9/SOP/model version change. No change is inferred merely because a replay is requested.
2. Freeze the evidence snapshot and record its original cutoff. Produce a dependency list of affected gates/inputs/candidates.
3. Retrieve the candidate's existing facts, comparables, negative evidence and scenarios from the index. Evaluate the new rule against that fixed snapshot first.
4. Recompute affected outputs and re-evaluate the actual sequential gate dependencies. A previous pass is not automatically valid under a changed material rule; blocked downstream gates remain conditional.
5. Publish a separate replay release with old/new rule versions, same-data comparison, changed/unchanged gate reasons, cashflow/rank differences, outstanding unknowns and checks. Preserve old outputs.
6. If also using newer evidence, show a separate refreshed-evidence result. Do not attribute a market-data change to the rule change.

Replay may be numerical, qualitative or both. Do not claim automated G0-G9 judgement solely because a calculator ran. The current registry supplies retrieval and provenance; it does not introduce an automatic admission engine.

## 4. Targeted supplementation only where needed

Do not restart all-region research solely because rules changed. Request/fetch only the material missing information:
- a new rule requires a fact never collected;
- a decisive source is unavailable or contradictory and the retained extract is insufficient;
- price/rent/fees/rights/condition or a catalyst may have materially changed for a current capital decision.

Record which fact is needed, why it changes a conclusion and which candidates are affected. Reuse unaffected evidence. Historical-snapshot replay can proceed without a new market sweep, but it remains dated historical analysis; it is not proof of today's executable price or purchase readiness. No automatic expiry period or universal documentation veto is introduced.

## 5. Completion checkpoint

Before finishing a regional batch, update the candidate records and document manifest, save evidence and exclusions, pin input/rule/model versions, publish results/unknowns, validate ID and link integrity, and advance coverage only for work actually performed.

Main/GitHub is the authoritative store. No new local archive/clone or cleanup. This retention update does not complete the125 pending substantive reviews, refresh any market fact, change Core/SOP financial parameters, update the map, authorise outreach or create background monitoring.
