# Neural map live verification - 2026-10-07

Result: **PASS** for the published map at https://brandonkow.github.io/core/.

- Published application/release commit: `6d5841e8a0221c88ef16e78fea6f3e64f80277f5`.
- Application fix commit: `c528341ff932a5af720f919ec8691a6f2cb4c760`.
- [GitHub Actions run 37643916468](https://github.com/brandonkow/core/actions/runs/37643916468): verify and deploy jobs both completed successfully.
- Served response: HTTP 200, `text/html; charset=utf-8`, 151,202 bytes.
- Served HTML SHA-256: `923949805bd7136fac1c1ed44a462253615bb1e500c46a46a1d91da58ac12da5`, matching the tested and committed file.
- The full committed browser smoke suite passed against the HTTPS Pages URL in a dedicated headless Edge 154.0.4258.62 instance with extensions disabled. It exercised the live application, not only the localhost preview or static HTTP.
- An earlier live run completed the interaction assertions but failed its all-exceptions assertion on an injected browser-extension script (`chrome-extension://.../activeContent.js`). The clean-instance rerun produced zero exceptions. No application error was suppressed to obtain a pass.
- Source preservation at this release: all 566 pre-existing non-navigation blobs retain their baseline SHA; only the root README changes among the 567 old files. The eight map source hashes, including the frozen master, match the recorded baseline.
- The original Claude branch remains intact at `e0ab750ad989f3da955d41790dc061b8aaf99e94`.
- Browser opening was requested in Codex; the UI returned queued. This receipt does not claim the user's visible tab was manually inspected.

See [verification report](../visualization/VERIFICATION_2026-10-07.md), [source/decision checks](../visualization/verify.cjs), and [browser smoke test](../visualization/browser_smoke.py). The original 41-item Claude review transcript remains unavailable. These checks establish the stated source, arithmetic, decision-path and interface behaviour; they do not validate market predictions or investment performance.

The Pages artifact contains only the interactive map and its alternate HTML entry. Research records and personal workpapers are not copied into that website artifact.
