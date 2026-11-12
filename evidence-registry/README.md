# Candidate evidence registry

Updated12November2026. [Approved G0 calibration replay](../klang-valley-2026-10-07/round-3/g0-reference-calibration-2026-11-12/G0_Calibration_Replay_2026-11-12.md) is the latest regional assessment overlay.

[Candidate_Records.json](Candidate_Records.json) retains138 regional baselines and2 separate case packets. It now indexes 180 immutable documents. All original working inputs and source snapshots remain unchanged. The125 October cases were replayed under the user-approved G0 interpretation; three pass G0 for broad product-cohort reference only and122 remain unresolved. Thirteen earlier priority dossiers were not replayed in this pass. No all138 current-market survey or purchase approval is asserted.

## Retrieve and replay

1. Select candidate_id and preserve its exact baseline input.
2. Resolve original workpapers and newer overlays through the immutable document dictionary; each has a path, commit and blob SHA.
3. For the G0 replay, read the case selector in [G0_Calibration_Replay_2026-11-12.json](../klang-valley-2026-10-07/round-3/g0-reference-calibration-2026-11-12/G0_Calibration_Replay_2026-11-12.json), the human-readable [decision record](../klang-valley-2026-10-07/round-3/g0-reference-calibration-2026-11-12/G0_Calibration_Replay_2026-11-12.md) and the [SOP supplement](../sop/G0_Reference_Price_Execution_2026-11-12.md).
4. Continue sequentially at each case's first unresolved gate. A broad cohort G0 pass does not pass selected-unit G4 or G1-G9.
5. Future authorised rule changes start with this retained snapshot, preserve prior assessments and supplement only material missing/stale facts.

Legacy fact-level normalisation remains partial. Unknowns remain unknown; replay date is not a source refresh. Financial inputs and historical results were not changed. [Validation](Validation.json) identifies exactly what was checked.
