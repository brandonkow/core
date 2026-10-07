from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent
cases=json.loads((ROOT/'Case_Inputs.json').read_text(encoding='utf-8'))['cases']
analyses={x['id']:x for x in json.loads((ROOT/'Case_Analysis.json').read_text(encoding='utf-8'))['cases']}
sources=json.loads((ROOT/'Evidence_Register.json').read_text(encoding='utf-8'))['sources']
source_map={x['id']:x for x in sources}
fin=json.loads((ROOT/'Financial_Results.json').read_text(encoding='utf-8'))
base={x['id']:x for x in fin['base']}
money=lambda v:f'RM{v:,.0f}'
lines=['# Evidence, claims and comparable register — round 1','',
'Cutoff/retrieval: 7 October 2026. The access method below distinguishes opened page text, indexed search text, inherited developer provenance and failed/redirected exact links. Listing text is evidence of an advertisement, not evidence that its terms are true, current, executable or achieved. No imagery/video or site conditions were inspected.','',
'## Lineage and claim discipline','',
'PropertyGuru and iProperty are not independent achieved-market datasets. Different advertisers may publish the same underlying unit; deduplication by parcel remains incomplete. Brickz, list.my and NilaMap may share NAPIC/JPPH origin and cannot count as three independent transfers. Developer and university sources establish only their stated products/channels. None verifies private management accounts, titles, original parcel plans or collected rent.','',
'Each E-ID is a scoped claim about the named expression. E-IDs map to gates via the case papers: price/transaction observations to G0/G5; type/rights to G2/G4/G7; rental/channel evidence to G1/G2/G6; operations/supply to G3; financing/holding to G7/G8. The observation is separated from its permitted inference. Recheck volatile asks, availability, fees and actual lending before any promotion or offer; a fresh crawl does not refresh an old market event.','',
'No empirical fair-value interval is adopted: material stack, rights, condition, consideration and transaction-motive adjustments cannot currently be bounded. No fixed percentage adjustment or zero adjustment is silently applied.','']
for s in sources:
 lines += [f"## {s['id']} — {s['lineage']}",'',
 f"- Source: [{s['access']}]({s['url']}).",
 f"- Event/publication: {s['event_date']}; retrieval: {s['retrieved']}.",
 f"- Observed: {s['observed']}",
 f"- Inference boundary / adjustment missing: {s['limits']}",'']
lines+=['## Comparable-role register','',
'Primary means the intended closest type, not a validated fair-price anchor. Secondary/diagnostic references are leads until actual budget, routine and rights match. Asking stock is distinct from voluntary completed transactions; auction reserves are distinct from both.','',
'| Case | Selected advertised expression | Intended primary cohort | Secondary / diagnostic and rejected cohorts |',
'|---|---|---|---|']
for c in cases:
 a=analyses[c['id']]
 lines.append(f"| {c['id']} | {c['name']} {c['sqft']} sqft; {c['layout']}; {money(c['price'])}; {c['bays'] if c['bays'] is not None else 'unknown'} bays | Same parcel type, component, rights, area and condition; {c['price_source']}/{c['rent_source']} are unpaired asks | {a['comparables']} |")
lines += ['','For every selected expression, exact floor/stack, title instrument, seller motive, effective consideration and signed rent remain unknown unless specifically noted. Listing-specific dates, advertised furnishing/bays and source links are retained above and in Case_Inputs.json. Unknowns prevent G0 clearance; these are not omitted zero-value adjustments.','',
'## Programme source-scan boundary','',
'Public regional transaction searches were attempted across Old Klang Road, Petaling Jaya, Mont Kiara/Kepong, Ampang, Setapak, Puchong and Cyberjaya. Their administrative/property-type/date filters differ. No district median, regional transaction count, macro overhang number or automatic portal summary is used to rank regions. Official NAPIC H1 2026 source retrieval did not yield a sufficiently verified adopted table; macro numerical conclusions are withheld. No absence-of-search-result is called zero transactions.']
(ROOT/'Evidence_Register.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
lines=['# Selected-case G0–G9 workpapers — round 1','',
'Decision cutoff: 7 October 2026; prospective research, no realised outcomes. Master SHA256: 1fbf607a78111bc007736fe0cc8109ad3967939a2dcc7ff54f017b491172e86b. SOP KV-EXEC-2026-10-07; financial configuration KV-FIN-90-4-35-v1. The frozen master, original gates, earlier calls and prior financial outputs remain authoritative/preserved.','',
'Fourteen marketed expressions across eight batches. These are desk gate applications with explicit stops, not fourteen cleared investments or complete coverage of sixty-one catchments. Evidence status: advertisement observations are Supported only as published claims; modeled costs/rents are Bounded estimate for sensitivity, not an empirical confidence band; unit/management/clearing facts remain Unknown; inconsistent adverts are Contrary evidence to a clean-price inference.','',
'All G1–G8 work below is conditional because G0 is not cleared. No exact original unit has been physically inspected. Source and comparable details: [evidence register](Evidence_Register.md); cash schedules and sensitivities: [financial report](Financial_Underwriting.md); material flags: [divergence register](Divergence_and_Misses.md).','']
for c in cases:
 a=analyses[c['id']]; b=base[c['id']]
 flags={'KV01':'D01','KV02':'D04','KV03':'D02','KV13':'D03','KV14':'D05'}.get(c['id'],'None currently; evidence gaps alone do not establish divergence. Source-integrity issues remain binding.')
 links=', '.join(f"[{sid}]({source_map[sid]['url']})" for sid in (c['price_source'],c['rent_source'],c['diagnostic_source']))
 lines += [f"## {c['id']} — {c['name']}, {c['sqft']} sqft ({c['batch']})",'',
 f"Catchment: {c['catchment']}. Advertised {c['layout']}; bays: {c['bays'] if c['bays'] is not None else 'unverified'}. Entry {money(c['price'])}; ordinary whole-unit rent scenario {money(c['rent_assumed'])}/month. {c['match']}. Selection purpose: {c['selection_reason']}. Evidence: {links}.",'',
 '| Gate | Evidence / conditional interpretation | Conclusion / unresolved burden |',
 '|---|---|---|',
 f"| G0 — Reference-Price Validity | {c['price_source']} is asking consideration, {c['rent_source']} is rental advertising/proxy, not a paired completed transaction. {a['comparables']} | STOP. Effective unit price, material comparability and justified clearing interval unvalidated. No discount claim. |",
 f"| G1 — Market Mechanism | {a['mechanism']} | Mechanism hypothesis; no automatic catalyst, rent growth or appreciation credit. |",
 f"| G2 — Buyer Universe | {a['buyers']} | Buyer tasks are analyst hypotheses, not observed proportions or additive independent pools. |",
 f"| G3 — Project Quality | {a['project']} | Operations/supply sufficiency not cleared. Unknown management is not assumed bad or good. |",
 f"| G4 — Unit Quality | {a['unit']} | Marketed expression only. No plan/condition/rights clearance. |",
 f"| G5 — Price / Mispricing | At assumed rent and fees: {b['gross_yield']:.2%} gross; standard balance {money(b['standard_monthly_balance'])}/month. Mechanical 6% price: {money(b['gross6_price'])}. | G0–G4 prerequisites unresolved. Mechanical price is not fair value, a bid or proven mispricing. |",
 f"| G6 — Exit Architecture | {a['exit']} Five-year nominal break-even sale {money(b['terminal_nominal_breakeven'])}; future standard buyer instalment {money(b['future_buyer_standard_payment_at_breakeven'])}/month before fees. | Required sale is not forecast. Actual buyer cash/income, substitutes and sale time unproven. Flat/-20% exits and 12-month delay are modeled. |",
 f"| G7 — Financing / Terminal Risk | {a['finance']} | Standard 90/4/35; separate actual-credit 15% valuation shortfall, 25-year loan, 5.5% rate and works/forced-hold sensitivities. No bank approval. |",
 "| G8 — Portfolio / Opportunity Cost | Synthetic RM500k cash/RM150k reserve and correlated asset shocks; compare all opportunities against keeping capital available. | User capital, debts and real correlation unknown. Synthetic pass is not allocation approval. No assumed salary/refinance rescue. |",
 "| G9 — Capital Decision | Upstream evidence, rights, costs and exit gaps remain material. | **Defer.** No independently proven structural failure justifies Reject; no demonstrated personal allocation constraint justifies Preserve Capacity. |",'',
 '### Financial chain and sensitivity','',
 f"Entry cash {money(b['entry_cash'])}; loan {money(b['standard_loan'])}; instalment {money(b['standard_instalment'])}/month. Fee proxy {money(c['fee_assumed'])}; other allowance {money(c['other_assumed'])}/month; initial works {money(c['refurb_assumed'])}. Eleven collected months produce annual carry {money(b['cashflow_by_year'][0])}. Year-5 debt {money(b['terminal_debt'])}; flat-price whole-investment result {money(b['profit_by_exit_multiple']['1'])}; 20%-lower exit result {money(b['profit_by_exit_multiple']['0.8'])}. Taxes/unquoted transaction costs remain unverified, not assumed known zero.",'',
 f"Rent sensitivity {money(c['rent_low'])}–{money(c['rent_high'])}, plus fee +/-20%, is a stress grid, not an achieved-rent confidence interval. Standard coverage requires {money(b['standard_required_rent'])}/month; annual carry neutrality requires {money(b['annual_carry_neutral_rent'])}/month under these cost/collection assumptions. Neither is a rent forecast. Exact financing and fee evidence can change the result.",'',
 '### Four separate conclusions','',
 f"- Product / living quality: conditional buyer-task fit described at G2/G4; comparative current operating quality is unverified. {a['unit'].split('. ')[0]}.",
 f"- Investment attractiveness at stated price: {b['gross_yield']:.2%} scenario gross yield and {money(b['standard_monthly_balance'])} standard balance; negative annual carry, no validated G0 margin. No executable investment ranking.",
 f"- Research priority: {a['conclusion']}",
 "- G9: **Defer**. Confidence is high that a Deploy is presently unsupported; confidence in fair value and actual performance is low.",'',
 f"Material divergence status: {flags}. Unresolved material conflict reduces conviction and increases the required evidence/margin; no numerical margin is invented when fair value itself is unbounded.",'',
 '### At most three immediate evidence tasks','']
 tasks=a['next'].rstrip('.').split('; ')
 assert len(tasks)==3,(c['id'],tasks)
 for i,t in enumerate(tasks,1):
  lines.append(f"{i}. {t[0].upper()+t[1:]}.")
 lines += ['',
 'Routes: existing public developer/official/transaction records first; exact signed tenancy, fee/MC accounts, title and condition require a seller/management/lender/field diligence packet. No third-party outreach, paid access or site visit has been performed. Recheck before any rank promotion or offer. At the next active evidence pass, advance only if an available source can change the decision; otherwise retain Defer and the specific unresolved task, without repeatedly counting the same ad.','']
 if b['current_shortfall']:
  lines+=['### Current-shortfall transition record','',
 f"Current achieved rent and management-only fee are Unknown; the disclosed proxies give {money(b['standard_monthly_balance'])}/month. Required standard/annual-neutral rents are {money(b['standard_required_rent'])}/{money(b['annual_carry_neutral_rent'])}. No funded operating change with independently evidenced unit-level rent transmission or credible benefit date has been established. Therefore no transition exception is proposed, no future uplift enters base and research priority remains lowest.",'',
 f"The no-uplift base accumulates {money(b['cashflow_total'])} of five-year carry plus initial costs. Delay/rate/rent/works scenarios are in the financial package; actual ring-fenced capacity is unknown. Reopen only on verified achieved rent, genuine net-price/fee change, or a funded/operating change with competing-supply, timing and incremental-cost evidence. Falsifiers: uplift fails in matched signed/renewed leases, incentives/fit-out explain it, competing inventory absorbs the benefit, or finance/works burden erases it. Preserve the old negative result when recording any later revision. Do not relabel this unvalidated income case as a Special Situation.",'']
 lines += ['Work-queue disposition: '+('price/identity resolution before shortlist promotion' if c['id']=='KV12' else 'bounded event-watch at lowest tier' if b['current_shortfall'] else 'advance decision-changing evidence investigation')+'. Outcome status: no matured investment result; paper calculations and source-error detection are not hits.','']
(ROOT/'Selected_Case_Workpapers.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Evidence and 14 ordered gate papers generated.')

