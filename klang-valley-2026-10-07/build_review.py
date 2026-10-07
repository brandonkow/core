from pathlib import Path
import json,itertools
ROOT=Path(__file__).resolve().parent
cases=json.loads((ROOT/'Case_Inputs.json').read_text(encoding='utf-8'))['cases']
fin=json.loads((ROOT/'Financial_Results.json').read_text(encoding='utf-8'))
bs={x['id']:x for x in fin['base']}
old=json.loads((ROOT.parent/'execution-release-2026-10-07'/'Financial_Results.json').read_text(encoding='utf-8'))
money=lambda x:f'RM{x:,.0f}'
lines=['# Klang Valley residential investment research — first comparative review','',
'Research cutoff: 7 October 2026. Authorised programme launch; English documents and Mandarin discussion. This is the first comparative release, not completion of the full regional programme.','',
'## Investment conclusion','',
'No Deploy is supported. The next household-oriented investigation should treat **Maxim Residences 825 sqft at the advertised RM380k and Skypod 881 sqft at RM380k as an unresolved pair**, with **First Residence 1074 sqft around RM390k** as the family-layout challenger. **Solstice 450 sqft at RM200k** deserves a separate income-and-exit investigation; its higher gross yield does not make it the best asset. These prices are advertisements, not clean executed or available offers.','',
'This is an investigation ordering, not a capital allocation. Actual unit rights, effective clearing value, achieved rent, management/works and exit depth remain decision-critical unknowns. High confidence in Defer is compatible with low confidence in fair value. No blank gate has been passed by calculation.','',
'## What has actually been completed','',
'- Locked eight batches and 61 functional catchments before drawing regional conclusions.',
'- Added 14 selected marketed expressions with ordered G0–G9 workpapers across 14 catchments; preserved the earlier nine Cheras expressions and their approved replay.',
'- Recorded 65 scoped evidence entries with dates, access method, advertising/transaction lineage and limitations. These are not 65 independent market outcomes.',
'- Applied the unchanged financial engine to 14 bases, 126 sensitivities, 14 forced-hold paths, 91 paired funding shocks and a 126-row rent/fee grid.',
'- Recorded five material divergence investigations and ten source-integrity incidents; none is investment validation.',
'- Four more catchments retain inherited selective work only; **43 catchments are mapped only**. Geography mapping is complete for declared scope; full regional desk underwriting is not.','',
'## First-round comparison','',
'All rent/fee/cost figures below are disclosed scenarios. Standard balance deducts the full 90%/4%/35-year instalment and a combined management/sinking proxy; management-only coverage remains unverified. Annual carry includes eleven collected months and other costs.','',
'| Batch | Selected expression | Advertised price | Rent scenario/month | Gross yield | Standard balance/month | Annual carry | Research consequence |',
'|---|---|---:|---:|---:|---:|---:|---|']
priorities={
'KV01':'Priority household lead; tied with KV13 pending exact evidence',
'KV02':'Conditional standard-positive premium-rent countercase; below 6%',
'KV03':'Lowest tier; no validated same-type discount',
'KV04':'Lowest tier; exact starting-price expression unresolved',
'KV05':'Lowest tier; current rent weak, old transaction reference',
'KV06':'Lowest tier; living quality separate from income',
'KV07':'Lowest tier at conservative base; rent-dependent sign',
'KV08':'Fragile standard surplus; lease/fee/condition evidence',
'KV09':'Priority family-layout challenger; capex and one bay matter',
'KV10':'Lowest tier; high rent does not justify any entry price',
'KV11':'Lowest tier; effective consideration and title unresolved',
'KV12':'Identity/price resolution only; inconsistent advert',
'KV13':'Priority household lead; tied with KV01 pending exact evidence',
'KV14':'Priority income/exit counterexample; no yield-only promotion'}
for c in cases:
 b=bs[c['id']]
 lines.append(f"| {c['batch']} | {c['id']} {c['name']}, {c['sqft']} sf {c['layout']} | {money(c['price'])} | {money(c['rent_assumed'])} | {b['gross_yield']:.2%} | {money(b['standard_monthly_balance'])} | {money(b['cashflow_by_year'][0])} | {priorities[c['id']]} |")
lines+=['','Seven of fourteen bases have a non-negative standard proxy, including KV12 whose price instrument is unresolved. None has non-negative annual carry under these particular allowances. This does not prove actual negative cashflow for every unit: signed rent, collected months and actual fees/costs can change it. Current modeled shortfalls stay at the lowest research tier, not structural Reject.','',
'## What changed relative to the earlier Cheras shortlist','',
'The original three-bedroom preference is no longer a sufficient basis for the sampling order. A genuine two-bedroom can reduce total capital quantum while retaining a small-household use case. Conversely, choosing smaller Windows does not automatically fix its rental economics. Neither observation creates a universal bedroom rule.','',
'The following inherited bases are from the approved 7 October 90/4/35 replay using the older 6 October evidence. They are not freshly revalidated listings, and their original cost allowances differ from the new cases.','',
'| Expression | Evidence vintage | Standard balance | Annual carry | Decision |',
'|---|---|---:|---:|---|']
for b in old['base']:
 if b['id'] in ('C01','C05'):
  lines.append(f"| {b['id']} {b['name']} | 6 October assumptions, 7 October full replay | {money(b['standard_monthly_balance'])} | {money(b['cashflow_by_year'][0])} | Defer |")
lines += ['','The current additions create a stronger test of the original shortlist; they do not retrospectively change its source dates or claim a realised missed investment. Same-condition cost and rent evidence, not the newer report date, must decide the ordering.','',
'## Four different conclusions','',
'| Question | Current answer | Strongest reversal condition |',
'|---|---|---|',
'| Which is the best place/product to live? | Unresolved across regions. Small-family utility, one/two bays, room usability and actual operations are buyer-specific; no uninspected quality winner. | Actual noise, lift/circulation, parking, room dimensions and family choice evidence |',
'| Which is most attractive at the stated investment price? | No executable winner because G0/operations/unit/exit evidence is incomplete. Solstice leads gross arithmetic; Maxim/Skypod are household-exit hypotheses. | Clean net price, achieved rent, MC/works and matched terminal-buyer evidence |',
'| What should research next? | KV01/KV13 household pair; KV09 family challenge; KV14 income-exit challenge. KV08/KV02 after these; KV12 first requires clean identity. | Verified fee/rent or price change, structural evidence or a stronger omitted substitute |',
'| What is the capital decision? | Defer for all 14. Preserve actual capital while evidence is unresolved, without inventing a personal Preserve Capacity finding. | Gate-sufficient evidence and actual mandate/finance/portfolio capacity |','',
'## Rank fragility and burdens','',
f"Maxim's standard base cushion is {money(bs['KV01']['standard_monthly_balance'])}/month versus Skypod's {money(bs['KV13']['standard_monthly_balance'])}. The {money(bs['KV01']['standard_monthly_balance']-bs['KV13']['standard_monthly_balance'])} gap arises from an unverified fee-proxy difference. A RM20 relative rent or fee change erases it. The two products also have different locations, bays, title claims and current-condition uncertainties, so this is not an equal-quality comparison.",'',
f"At RM1800 rent, Maxim's modeled standard balance falls to {money(next(x['standard_balance'] for x in fin['rank_grid'] if x['id']=='KV01' and x['rent']==1800 and x['fee']==300))}. At RM1700, Skypod falls to {money(next(x['standard_balance'] for x in fin['rank_grid'] if x['id']=='KV13' and x['rent']==1700 and x['fee']==320))}. These downside endpoints have advertising context but are not probability estimates. Product quality cannot excuse unsupported rent.",'',
f"Solstice's RM1200 base needs roughly {money(bs['KV14']['annual_carry_neutral_rent'])}/month to achieve annual carry neutrality under the stated eleven-month collection/cost assumptions. A RM1300 asking lead exists, but no renewed/collected tenancy establishes that outcome. Even an annual cash surplus would not clear title, operations or the exit buyer.",'',
'| Lead | Five-year nominal break-even sale | Increase over entry | What the burden means |',
'|---|---:|---:|---|']
for cid in ('KV01','KV13','KV09','KV14'):
 b=bs[cid]
 lines.append(f"| {cid} | {money(b['terminal_nominal_breakeven'])} | {b['terminal_nominal_breakeven']/b['price']-1:.1%} | Required to recover modeled cash/economic costs; not a forecast, floor or fair value |")
lines+=['','All prices above require a real next buyer with financing and alternatives. Loan amortisation is incorporated once. A low entry quantum may ease funding, but no terminal premium is granted for MRT, a mall, a university or analyst conviction.','',
'## What can invalidate the leading interpretation','',
'1. A clean price/unit pack differs from the advertised expression; the apparent bargain disappears once rights, bays, condition or incentives are reconciled.',
'2. Quoted rent requires additional furnishing, utilities, room letting or weak collection; comparable ordinary tenancy cannot fund the assumed hold.',
'3. Current MC liabilities or major works are much larger than planning allowances, or the use/title/lease limits financing.',
'4. The real resale buyer consistently prefers a competing original layout or landed/larger substitute at the required exit quantum.',
'5. A credible current case in the 43 unworked catchments or missing lifecycle/budget segments dominates these accessible samples.','',
'Current evidence cannot select among all these explanations. The answer is explicit uncertainty and additional evidence, not a compensating subjective score.','',
'## Senior Market Red Team checkpoint','',
'Two market interpretations are now concrete enough to challenge:','',
'- **Skypod versus Maxim:** the two-bay Skypod two-bedroom could have at least as credible a small-household ownership fallback at similar entry quantum. A real local preference, access problem, externality or operating issue could overturn that; freehold and bays alone are not proof.',
'- **Solstice:** ordinary income can merit investigation even where the likely exit buyer is an investor, provided net collection and a financeable resale channel are evidenced. The unresolved issue is whether this is a durable channel or a structural exit trap. University presence and gross yield do not answer it.','',
'These are requests for market-level counter-mechanisms, not for the user to supply rent quotes or collect documents. Agreement would not clear gates. No Core change, automatic rejection of investor exits, or permanent family-size screening rule is proposed. Other geographic work is independent of this checkpoint.','',
'## Files and continuation boundary','',
'- [61-catchment coverage and next tranche](Regional_Coverage.md)',
'- [Fourteen ordered G0–G9 workpapers](Selected_Case_Workpapers.md)',
'- [Evidence and comparable register](Evidence_Register.md)',
'- [Full financial chain, thresholds and stress](Financial_Underwriting.md)',
'- [Divergence investigations and misses](Divergence_and_Misses.md)',
'- [Scope and pre-research propositions](Programme_PreResearch_Lock.md)',
'- [Validation and preservation record](Validation_Report.md)','',
'The remaining work is substantial: forty-three catchments have mapping only, others have selective expressions, and current exact-unit/private/field evidence is absent. This release is a substantive first round of the authorised full-area programme, not a completed comprehensive underwriting. No background monitoring, scheduled continuation, outreach or purchase has been created.']
(ROOT/'Programme_Review.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Programme review written.')

