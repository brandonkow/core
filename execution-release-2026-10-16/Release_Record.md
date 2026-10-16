# Financial SOP v2 adoption record

Date: 16 October 2026. Baseline main: `53be4a5e72e0663dbf7a2121ea8665481d751bd0`.
Authority: the user explicitly instructed, after the B/D comparison, to update SOP with all parameters that are not Brightwood-specific.

## Delivered authority

[Current SOP](../sop/Financial_Execution_SOP_v2.md) and [declarative parameters](../sop/Financial_Execution_Parameters_v2.json) are effective for new/materially reopened underwriting. This express approval supersedes the earlier conditional-promotion position; the earlier [assessment](../side-investigations/2026-10-16-brightwood-stress-replay/SOP_Promotion_Assessment.md) remains an accurate historical record.

Adoption is by user authority, not an empirical finding that the calibrated figures predict all properties. The prior caveat about narrow rate stress remains visible. No claim of successful out-of-sample validation or realised profitability is made.

## Source and parameter coverage

Read the preserved [P1-P28 inputs](../side-investigations/2026-10-16-brightwood-stress-replay/Inputs.json), [stress dispositions](../side-investigations/2026-10-16-brightwood-stress-replay/Stress_Register.md), and [one-bay overlay](../side-investigations/2026-10-16-brightwood-execution-brief/Case_Overlay.json) for source context. These are provenance, not current reusable configurations.

| Source ID | Disposition | Current reusable treatment / exclusion |
|---|---|---|
| P1 | Case only | Specific rent values excluded; per-stream reconciliation retained. |
| P2 | Method only | Split-operation feasibility and fallback checks retained; specific layout/rents excluded. |
| P3 | Case only | Excluded product type is not a reusable screening ban. |
| P4 | Case only | Excluded product type is not a reusable screening ban. |
| P5 | Promoted | Zero construction-period rental growth; no construction rent. Specific rent/VP date excluded. |
| P6 | Promoted | Zero operating rent growth planning baseline. |
| P7 | Promoted, scoped | One fit-out month with concurrent marketing; adjust for actual ready/tenanted/works condition. |
| P8 | Promoted | 12-month lease plus one replacement void; event calendar, no renewal void. |
| P9 | Method only | Fee/area/sinking scope; project 0.35 psf and specific areas excluded. |
| P10 | Promoted, scoped | New-launch 24-month flat planning convention; actual decisions override; later AGM unknown. |
| P11 | Promoted | Annual repair budget half prevailing monthly parcel rent; disclose provision accounting. |
| P12 | Promoted | One-month new tenancy / half-month same-tenant renewal commission; no overlap. |
| P13 | Promoted | Delete generic RM200; itemise actual costs and disclose U. |
| P14 | Promoted, scoped | Tenant utilities default, no unsupported extra parking income; actual bundled operations separately. |
| P15 | Promoted | Fit-out 5% effective nett; includes operating configuration and equipment. |
| P16 | Promoted | Final buyer-paid budget; developer inventory deduplicated; no automatic furniture exit premium. |
| P17 | Promoted | Itemised acquisition costs; current schedules/profile/package verified per case. |
| P18 | Case only | 48-month build excluded; actual project construction duration required. |
| P19 | Promoted, scoped | 50% average draw planning proxy when dates unavailable, not validated schedule. |
| P20 | Promoted, scoped | Zero subsidy credited unless documented; specific package assertion excluded. |
| P21 | Promoted | 90% gross new-launch / acquisition-price resale, 4%, 35 years; handover amortisation convention separate from actual lender. |
| P22 | Method only | Reconcile rebate/deposit/loan. 10% rebate and zero downpayment excluded as universal values. |
| P23 | Promoted, scoped | 60-month operating comparison from handover/possession; actual hold separately. |
| P24 | Promoted | 3% agency plus itemised seller costs, not all-in 3%; statutory amounts not frozen. |
| P25 | Promoted as target | Nett +10% year3 / +20% year5; no guaranteed appreciation, no auto-cleared exit. |
| P26 | Promoted, scoped | Zero hypothetical base levy; actual committed works/levy retained. |
| P27 | Promoted | Pre-personal-income-tax / pre-final-RPGT; payable invoice taxes remain costs. |
| P28 | Promoted as reference | 6% future investor gross yield; not mandatory clearing yield. |

All **S1-S24** have an explicit disposition in section 5 of the new SOP and the JSON register:
- Retain S1-S3, S7-S8, S12, S15-S21 and S24 as scoped scenarios/methods.
- Translate S4 from project 48-to-60 months to a reusable **12-month delay relative to the actual base**; no universal 60-month delivery promise.
- Remove S5,S6,S9,S10,S11,S13,S14,S22 from the default suite; preserve evidence and actual portfolio/cost obligations.
- S23 transfers fallback methodology only. B rent2,500 and D's particular two-side dependence remain case-only.
- S12 transfers the 24-month/5%-annual stress shape, not 0.35psf.
- The one-bay instruction remains Brightwood-only. No other project is assumed to have one bay.

## Supersession and preserved evidence

| Older preset | Future execution |
|---|---|
| 7 October financial_config.json as current import | New v2 declarative register; explicitly map future model inputs. Old model outputs stay historical. |
| Blanket acquisition5%gross | Itemised actual/quoted/reference costs and U. |
| Disposal3% as all-in | Agency3% plus separate seller costs. |
| Eleven paid months annually without tenancy events | Monthly lease calendar; 12 paid then one replacement void. |
| Inherited5.5% stress interest | Approved4.25% primary sensitivity with stated scope, not a universal ceiling. |
| RM30k stress works/levy | RM10k fit-out overrun; no synthetic levy reinstatement. |
| Twelve-month forced no-sale default | Six-month sale delay, correctly extending cash/debt. |
| Six-paid-month stress first year | Deleted; S8 ten paid less one commission. |
| SyntheticRM500k/RM150k portfolio | Removed as default; real investor liquidity required for allocation. |
| Inherited8% equity hurdle | Not an approved current gate; disclose actual opportunity cost rather than silently importing this old synthetic hurdle. |
| Historical fit-out5% merely unapproved reference | Now expressly adopted5%nett planning budget, with scope/quote reconciliation. |
| Older 'no SOP promotion' status | Superseded by this explicit authority; historical assessment untouched. |

Modified current entry points: README.md, CURRENT_WORKFLOW.md, AGENTS.md, and the entry notice in sop/Approved_Execution_Supplement.md. All their previous content is retained below/after the notice. The single master, integrity manifests, old execution releases, all research/source/calculation files and map are unchanged.

No historical numerical replay is claimed. Brightwood remains under its calibrated case inputs, with the same B conditional research priority and G0 STOP / G4 not cleared / G9 Defer. A new parameter policy is not a case clearance. The completed regional programme is not reopened by this documentation task.

## Verification boundary

See [release checks](Validation_Report.json). Checks cover source-ID disposition completeness, numerical/unit/event consistency, navigation and tree preservation. They are documentation/configuration checks, not a new market backtest, lender verification or hosted-map test.

No local outputs, clones, file deletion or permission changes. Publication is directly to main with an expected-head lease. No outreach, purchase, map change or automation.
