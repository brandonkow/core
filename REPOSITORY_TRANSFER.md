# Repository transfer and retention

Date: 7 October 2026. Repository: [brandonkow/core](https://github.com/brandonkow/core).

The user requested transfer of every project-generated file and all framework Markdown to this repository, followed by deletion of this project's local research directory and local checkout only after safe remote verification. Future project outputs belong here; temporary workspaces should be removed after their completed work has been pushed and verified.

## Superseding retention instruction

On 7 October 2026, after the verified transfer and blocked cleanup attempts, the user instructed: leave the old local files alone and send all future project files to GitHub. This suspends the earlier deletion requirement and removes cleanup as a research prerequisite. Historical transfer and cleanup observations below remain historical evidence. No further local deletion or permission changes are authorised by the current workflow. See [CURRENT_WORKFLOW.md](CURRENT_WORKFLOW.md).

## Included

The complete former Residential Investment Decision Engine directory contributes533files, including145Markdown documents, Core, SOP, handoff, validation and failures, historical/forward registers, Cheras, all Klang Valley rounds, raw sources, PDFs/images, inputs, calculations, scripts and three existing generated Python cache files. Nothing from that project directory was omitted. The original407Q&A attachment adds one unmodified source file under source-inputs, giving534preserved source files and146source Markdown files. Administrative repository files and this report are additional.

The single master remains Residential_Investment_Framework.md, SHA2561fbf607a78111bc007736fe0cc8109ad3967939a2dcc7ff54f017b491172e86b. The handoff already exists in phase-7. No second master or Core rewrite is created.

MIGRATION_MANIFEST.json records each preserved source path, byte length and SHA256. Git attributes disable automatic text conversion so historical byte hashes survive checkout and transfer. Some historical documents contain obsolete local paths or conclusions; they remain historical records, interpreted through current navigation/status overrides.

## Current research

[B05 synthesis](klang-valley-2026-10-07/round-3/B05_Regional_Synthesis.md) and [checkpoint](klang-valley-2026-10-07/round-3/B05_RESUME_CHECKPOINT.md) are the current handoff. Seven B05 catchments and16expressions have a bounded desk-complete Defer; zero Deploy.1091release checks include212financial replays and384prior file comparisons. The full61-catchment programme is incomplete. B06 A41-A45 is next.

## Verification before removal

1. Copy each source file and verify its SHA256 against the source.
2. Commit/push to this repository without text transformation.
3. Download the GitHub archive for the exact pushed commit, not a local archive.
4. Verify the complete archive file set and every Git blob against that commit, then all534source SHA256values, the frozen master and prior research manifests.
5. Save REMOTE_TRANSFER_VERIFICATION.json and push the receipt.
6. Download/verify the final commit again, including the receipt, before removing local project copies.

verify_repository_transfer.py performs the archive checks. The receipt identifies the earlier full verified snapshot; the final post-receipt verification is performed before local deletion and reported to the user. The receipt is not a market or investment validation.

Deletion scope is only the former outputs/residential-investment-engine directory and the temporary core checkout under the shared workspace, plus the temporary downloaded verification archive created for this transfer. Original user-supplied attachments/downloads and unrelated repositories remain outside scope. No GitHub repository deletion is authorised.

## Verification method update - 8 October 2026

At the user's request, `verify_repository_transfer.py` lets the three current navigation and status registers advance, as AGENTS.md permits: `README.md`, `klang-valley-2026-10-07/round-3/README.md` and `klang-valley-2026-10-07/round-3/Coverage_Audit.md`. They must still exist, and the result lists which of them now differ from the manifest. Every other manifest file stays byte-checked (531 today), together with the archive blobs, the frozen master, the round-3 preservation audit and the B03-B05 release manifests. Adding a file to the exemption list is a deliberate code change, not an automatic rule.

`MIGRATION_MANIFEST.json` and `REMOTE_TRANSFER_VERIFICATION.json` are unchanged historical records. The method version is now `CORE-REMOTE-VERIFICATION-2026-10-08`. It no longer reports local deletion as authorised, because local cleanup is suspended. Write any new receipt to a new file rather than overwriting the 7 October receipt.
