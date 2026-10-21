# Candidate evidence registry

Created22October2026 at source commit `be103f4418bbfb3343826a3c4d285eb5fd9c7158`.

The user's requirement is to retain candidate information for later G0-G9 changes, so rule changes normally use saved evidence rather than restarting regional research.

[Candidate_Records.json](Candidate_Records.json) indexes **138 regional expressions and2 separate case packets (Brightwood B/D and Aviera)**. It retains exact baseline working inputs, source limitations and immutable commit/blob references to144 existing files. Shared document references avoid duplication. Historical and latest available assessment overlays remain distinguishable.

This is a retrieval/migration layer, not138 newly researched candidates or fully normalised fact ledgers.126 legacy baseline records contain at least one null source-fact field; their original packets remain accessible and may contain additional information. No null is replaced with a guessed fact. Source dates remain the dates in the original ledgers;22October indexing is not a source refresh.

## Retrieve and replay

1. Find the stable candidate_id in records (or standalone for the two side packets).
2. Read preserved_working_input without mistaking scenarios/asks for facts.
3. Resolve document_id through documents; retrieve its path at the pinned commit and check git_blob_sha where necessary. The selector identifies the relevant case/source IDs.
4. Read historical_packet_files and evidence_and_assessment_overlays, including contrary evidence, package branches and provenance. Per-candidate overlays may share files; use their selectors.
5. Apply the [retention/replay SOP](../sop/Evidence_Retention_and_Rule_Replay_2026-10-22.md). Save a new assessment under the authorised rule version and compare against the old result on identical evidence.
6. Supplement only decision-changing missing/stale facts. Do not silently call a dated replay current executable underwriting.

Future case work adds structured facts using the [record template](../templates/Candidate_Evidence_Record.json), retains the original source record and updates this index. Save the actual observation, not just a URL. A normalised ledger and a full webpage archive are different; full originals are retained only where available and appropriate.

[Validation](Validation.json) covers138 exact input matches, ID coverage and repository pointers. Core/G0-G9/financial presets/map and all historical findings are unchanged.125 regional cases still await substantive reassessment; their presence here does not clear that queue. No background replay or outreach is running.
