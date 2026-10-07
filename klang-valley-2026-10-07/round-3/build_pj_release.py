"""PJ research release builder. Reads frozen engine and prior cases; writes only B03 outputs."""
import json, importlib.util, itertools
from pathlib import Path
P=Path(__file__).resolve().parent
ROOT=P.parent.parent
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
spec=importlib.util.spec_from_file_location('frozen_finance',ROOT/'execution-release-2026-10-07/financial_engine.py')
e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
new=read(P/'B03_Case_Inputs.json')['cases']
old=read(P.parent/'Case_Inputs.json')['cases']+read(P.parent/'round-2/Case_Inputs.json')['cases']
old=[dict(c) for c in old if c['batch']=='B03']
details={
'KV08':('A22','Rail-oriented two-bedroom utility at a lower quantum is plausible; older mixed-use operation may consume the discount.','Investor-led income plus possible small-household use; compare Eve compact and true two-bedroom on usable space and total cost.','Current operations, bay rights and lending remain unknown.','Fully furnished 864-sf sale and unmatched asking-rent evidence; no collected lease or adjusted clearing set.','A rent above the inherited RM1800 or lower verified charges may change coverage; do not infer this from station proximity.','Confirm exact unit/bays and ordinary whole-unit rent, charges and works, then compare the Eve incremental rent against its incremental price.'),
'R207':('A18','Existing PJ daily routines could support compact demand despite older stock.','Investor-led compact exit; owner use remains a hypothesis. Compare Amcorp only after component clearance, and actual PJ8 two-bedroom alternatives.','Mixed-use component and ageing works require parcel and governance checks.','685-sf sale versus 625/667-sf rental leads; newer 800-sf two-bedroom sale versus 900-sf rent is also not a matched pair.','An apparently passing simplified monthly margin is vulnerable to an RM200 rent reduction and full annual costs.','Identify tower/unit, compare equivalent 685-sf ordinary leases and service bills, and normalise transfers; do not borrow 900-sf rent.'),
'R208':('A19','Outlier headline yield may reflect an office/residential component mix rather than mispricing.','No admitted residential ranking while component/area conflict remains. Investor buyer eligibility depends on actual rights and income.','301/306-sf and furnishing inconsistencies are material; location cannot clear component use.','Identity-quarantined numeric diagnostic. No office transfer may be paired with serviced-residential rent.','12% is an arithmetic artefact until both sides refer to an eligible equivalent unit; keep quarantine even if stress appears affordable.','Resolve exact tower/approved use/area/title and genuine long-term rental model first; then rerun costs and eligible transfers.'),
'R209':('A20','SS2 family routines can support utility without supporting income at the current quantum.','Potential local family and investor demand must be separately demonstrated. Ameera and Sea Park landed are diagnostic alternatives, not pooled comparables.','Study usability, parking, works and privacy can dominate project familiarity.','Sale 2+1 study and rental 3BR descriptions lack approved-plan equivalence; no adjusted price interval.','At the inherited RM2300 rent, entry or sustainable rent must change materially; landed overlap is not a universal price ceiling.','Match original plan, bays and condition; secure ordinary rent and charges; compare all-in landed renovation costs before any family premium.'),
'R210':('A21','Relative youth may help product utility but cannot prove management quality or justify rental shortfall.','Potential family use; compare equal-condition Kelana Mahkota and compact new competitors. Investor exit needs rent supporting total price.','Developer unit/block counts establish configuration only; neither building has independently graded management.','1259-sf sale/rent descriptions differ between 3+1 and four rooms; Bumi and auction discounts excluded from ordinary matching.','Kelana Mahkota lower quantum challenges Sterling as the income choice. Verified stronger net rent or much lower entry could reverse this.','Obtain like-for-like condition, room plan, fees/works and rent in both projects; test Sterling premium against actual buyer and rental evidence.'),
'R211':('A23','Local services may support a small-household rent premium; a study may also be overvalued as a bedroom.','Investor-led income and possible couple use; true two-bedroom Casa and neighbouring products test incremental household utility.','No current operations, noise, retail-interface or management proof.','Same advertised 660-sf size is insufficient when bays, study use and furnishing differ.','Small changes in rent or entry can restore simplified coverage, but annual costs and exit yield still matter.','Validate study/parking and ordinary rent; resolve a true two-bedroom alternative on equal furnishing and all-in cost.'),
'R212':('A24','Surian-area access cannot by itself support studio acquisition cost; larger discounted expressions challenge studio-first screening.','Investor-led studio resale; larger Encorp and Tropicana Gardens are task-dependent alternatives. No young-owner premium assumed.','Conflicting tenure descriptions and balcony/internal-area questions require parcel-level resolution.','640-sf studio sale/rent evidence is conditional; reject the 640-sf cheap two-bedroom header as proof of genuine two-bedroom stock.','RM1800 asking rent still needs costs/price testing; the 1166-sf alternative can reverse preference only after identity and rent match.','Resolve title, approved plan, interior area and fees, then test actual studio versus larger-unit leases at comparable condition.')
}
for c in old:
    a,m,b,p,comp,rev,nxt=details[c['id']]
    c.update(area_id=a,mechanism=m,buyer=b,project=p,comp=comp,reversal=rev,next=nxt,hold=c.get('quarantine') or 'Exact parcel, normalised clearing value and operations unverified',source_note=c.get('match',''),evidence_dates='Inherited 7 October 2026 release; original source dates retained')
cases=old+new
assert len(cases)==14 and len(set(c['id'] for c in cases))==14
results=[];checks=0
for c in cases:
    inputs={'base':{},'rent_low':{'rent_factor':c['rent_low']/c['rent_assumed']},'rent_high':{'rent_factor':c['rent_high']/c['rent_assumed']},'rate_5_5':{'rate':.055},'rent_down20':{'rent_factor':.8},'fee_up20':{'fee_factor':1.2},'zero_rent12':{'initial_vacancy':12},'works30k':{'levy_month':24,'levy':30000},'valuation85pct':{'valuation_ratio':.85},'term25':{'term':25},'exit_delay12':{'months':72},'unquoted_cost_buffer':{'annual_extra_cost':1200,'exit_extra_cost':5000},'combined12':{'months':12,'rate':.055,'rent_factor':.8,'fee_factor':1.2,'first_year_paid':6,'levy_month':1,'levy':30000}}
    rr={}
    for name,kw in inputs.items():
        r=e.evaluate(c,**kw)
        e.check_financial_identities(r,c,kw.get('exit_extra_cost',0));checks+=1
        r['scenario_monthly_balance_before_vacancy_other']=c['rent_assumed']*kw.get('rent_factor',1)-r['actual_instalment']-c['fee_assumed']*kw.get('fee_factor',1)
        rr[name]=r
    factor=e.payment(.9,.04,35);b=rr['base']
    bounds=dict(standard_price=(c['rent_assumed']-c['fee_assumed'])/factor,gross6_price=200*c['rent_assumed'],standard_rent=b['actual_instalment']+c['fee_assumed'],annual_neutral_rent=12*(b['actual_instalment']+c['fee_assumed']+c['other_assumed'])/11)
    terminal=[]
    for y in [.06,.07,.08]:
        price=12*c['rent_assumed']/y
        profit=.97*price-b['terminal_debt']+b['cashflow_total']-b['entry_cash']
        terminal.append(dict(required_gross_yield=y,implied_price=price,total_profit=profit))
    results.append(dict(case=c,scenarios=rr,boundaries=bounds,terminal_yield_scenarios=terminal,
                        future_buyer_90pct_stress_payment=e.payment(.9*b['terminal_nominal_breakeven'],.055,25)))
lookup={r['case']['id']:r for r in results}
pairs=[]
for a,b in itertools.combinations(results,2):
    aa=a['scenarios']['combined12'];bb=b['scenarios']['combined12']
    path=[e.CFG['synthetic_cash']-aa['entry_cash']-bb['entry_cash']]
    for ma,mb in zip(aa['schedule'],bb['schedule']): path.append(path[-1]+ma['cashflow']+mb['cashflow'])
    assert abs(path[-1]-(e.CFG['synthetic_cash']-aa['entry_cash']-bb['entry_cash']+aa['cashflow_total']+bb['cashflow_total']))<.01
    pairs.append(dict(ids=[aa['id'],bb['id']],minimum_cash=min(path),reserve_pass=min(path)>=e.CFG['synthetic_protected_reserve'],path=path))
rank=[]
for ra,rb in itertools.product([1800,2000,2200],[2200,2400,2600]):
    ca=dict(lookup['R306']['case'],rent_assumed=ra);cb=dict(lookup['R308']['case'],rent_assumed=rb)
    va=e.evaluate(ca);vb=e.evaluate(cb)
    rank.append(dict(eve_rent=ra,mahkota_rent=rb,eve_balance=va['standard_monthly_balance'],mahkota_balance=vb['standard_monthly_balance'],coverage_leader='R306' if va['standard_monthly_balance']>vb['standard_monthly_balance'] else 'R308'))
assert set(x['coverage_leader'] for x in rank)=={'R306','R308'}
price_tests=[]
for caseid,price in [('R305',650000),('R308',489999),('R310',550000)]:
    c=dict(lookup[caseid]['case'],price=price);r=e.evaluate(c);e.check_financial_identities(r,c);checks+=1
    price_tests.append(dict(case_id=caseid,price=price,result=r))
out=dict(version='KV-PJ-2026-10-07-R3',config=e.CFG,results=results,diagnostic_pairs=pairs,rank_grid=rank,alternative_price_scenarios=price_tests,financial_identity_checks=checks,case_count=14,deploy=0)
(P/'B03_Financial_Results.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
intro=['# PJ integrated financial underwriting','',
'Cutoff 7 October 2026. All RM. Fourteen conditional expressions: seven inherited, seven new. No executable offers, authenticated leases, exact title clearance or adjusted clearing values. Quarantined arithmetic stays visible but cannot enter an eligible shortlist. All remain G0 STOP / G9 Defer.','',
'Common user standard: 90% of purchase price, 4%, 35 years; full instalment plus fee. Fee is an unverified combined management/sinking proxy. Five-year hold, eleven paid months/year, 5% entry and 3% disposal allowances, stated upfront works and monthly other-cost allowances. No base rent or price growth. Figures are pre-tax; unquoted costs are unresolved, not zero. Other costs provision for repairs, insurance, assessments and reletting must be replaced with an itemised schedule. 8% equity hurdle, RM500k cash and RM150k protected reserve are illustrations, not user mandates or personal finances.','',
'Full payment is charged to cashflow; principal is reconciled to exit debt exactly once. A monthly standard pass is not annual cash neutrality. Discounted hurdle exits are required prices, not forecasts. The frozen engine also retains a legacy 80%-LTV future-buyer diagnostic field in JSON; this PJ report uses 90% for both standard and stressed future-buyer comparisons. Valuation stress finances 90% of a value 15% below price, requiring additional equity.','',
'## Base comparison','',
'| Case | Expression | Entry price / rent | Fee / other / works | Gross | Standard monthly | Annual carry | Entry cash |',
'|---|---|---:|---:|---:|---:|---:|---:|']
for r in results:
    c=r['case'];b=r['scenarios']['base']
    intro.append(f"| {c['id']} | {c['name']} | {c['price']:,.0f} / {c['rent_assumed']:,.0f} | {c['fee_assumed']:,.0f} / {c['other_assumed']:,.0f} / {c['refurb_assumed']:,.0f} | {b['gross_yield']:.2%} | {b['standard_monthly_balance']:+,.0f} | {b['cashflow_by_year'][0]:+,.0f} | {b['entry_cash']:,.0f} |")
intro+=['','R208 Centrestage and R309 Amcorp are component-held. R307 is index-only; R311 has title/layout/rental mismatches. Strong numeric results do not remove those holds. Lower/high rents are scenario bounds, not confidence intervals. No current-shortfall case is automatically rejected.','',
'## Price and rent conditions','',
'| Case | Standard price boundary | Price at 6% gross | Rent for standard | Rent for annual neutral carry |',
'|---|---:|---:|---:|---:|']
for r in results:
    d=r['boundaries'];intro.append(f"| {r['case']['id']} | {d['standard_price']:,.0f} | {d['gross6_price']:,.0f} | {d['standard_rent']:,.0f} | {d['annual_neutral_rent']:,.0f} |")
intro+=['','These are constraint calculations, not fair values or proposed offers. The lower of the first two price columns satisfies both numerical preferences at the assumed rent/fee, but still provides no proven margin of safety. A catalyst can reopen a shortfall case only with evidence for timing, sustainable net rent, competing supply and funded carry; no automatic rent uplift.','',
'## Terminal burden and price downside','',
'| Case | Year-5 debt | Nominal recovery sale | Sale for illustrative 8% | Profit at flat exit | Profit at -20% exit | Future-buyer payment 90/4/35 | Future-buyer payment 90/5.5/25 |',
'|---|---:|---:|---:|---:|---:|---:|---:|']
for r in results:
    b=r['scenarios']['base'];intro.append(f"| {b['id']} | {b['terminal_debt']:,.0f} | {b['terminal_nominal_breakeven']:,.0f} | {b['terminal_8pct_required']:,.0f} | {b['profit_by_exit_multiple']['1']:+,.0f} | {b['profit_by_exit_multiple']['0.8']:+,.0f} | {b['future_buyer_standard_payment_at_breakeven']:,.0f} | {r['future_buyer_90pct_stress_payment']:,.0f} |")
intro+=['','No authenticated owner-buyer willingness, turnover speed or bank valuation establishes the required exits. An investor can remain a valid exit buyer; test cash rent and yield repricing rather than invent an owner-buyer prerequisite.','',
'| Case | Investor price at 6% | At 7% | At 8% | Total five-year profit if exit at 7% |',
'|---|---:|---:|---:|---:|']
for r in results:
    t=r['terminal_yield_scenarios'];intro.append(f"| {r['case']['id']} | {t[0]['implied_price']:,.0f} | {t[1]['implied_price']:,.0f} | {t[2]['implied_price']:,.0f} | {t[1]['total_profit']:+,.0f} |")
intro+=['','These gross-yield capitalisations hold assumed rent unchanged and ignore any unsupported owner premium. They are diagnostics, not valuations; net-income capitalisation requires verified net costs. A move from 6% to 7% cuts this price by 14.29%, and to 8% by 25%.','',
'## Changed asking-price leads','',
'| Case | Separate/unresolved price | Standard monthly | Annual carry | Gross |',
'|---|---:|---:|---:|---:|']
for t in price_tests:
    b=t['result'];intro.append(f"| {t['case_id']} | {t['price']:,.0f} | {b['standard_monthly_balance']:+,.0f} | {b['cashflow_by_year'][0]:+,.0f} | {b['gross_yield']:.2%} |")
intro+=['','Midtown RM650k is a different partially furnished offer; Mahkota RM489999 and Casa RM550k reflect unresolved header/body discrepancies. They are not negotiated reductions in the base unit. Reconcile condition and rights before using any rank change.','',
'## Cash-coverage rank reversal','',
'| Eve compact rent | Mahkota rent | Eve monthly | Mahkota monthly | Coverage leader |',
'|---:|---:|---:|---:|---|']
for t in rank:intro.append(f"| {t['eve_rent']:,.0f} | {t['mahkota_rent']:,.0f} | {t['eve_balance']:+,.0f} | {t['mahkota_balance']:+,.0f} | {t['coverage_leader']} |")
intro+=['','Independent rent changes reverse the mechanical preference; this is not a probability distribution or a product-quality ranking. Within Eve, the larger layout must justify extra cash and lower base yield. Within Encorp, high asking rent can reverse the studio/large-unit comparison but needs stronger matching.','',
'## Correlated twelve-month hold','',
'Rate 5.5%, rent down 20%, only six paid months, charges up 20%, RM30k works in month1 per asset. No sale, salary rescue or refinancing. Pair cash deducts both entry amounts once from the same RM500k. Simultaneous exposure is intentional; PJ addresses are not independent risk factors.','',
'| Pair | Minimum synthetic cash | Preserves RM150k | Interpretation |','|---|---:|---|---|']
for ids,comment in [(['R306','R308'],'Different products; shared Klang Valley credit/tenant shocks.'),(['R306','R307'],'Same building: management, lifts and supply concentration.'),(['R305','R310'],'Two higher-quantum family expressions; both carry shortfalls.'),(['R309','R306'],'Diagnostic only: Amcorp is component-held, not an eligible allocation.')]:
    t=next(t for t in pairs if set(t['ids'])==set(ids))
    intro.append(f"| {' + '.join(ids)} | {t['minimum_cash']:,.0f} | {'Yes, scenario only' if t['reserve_pass'] else 'No'} | {comment} |")
intro+=['',f"All {len(pairs)} pair paths are retained for arithmetic audit; {sum(t['reserve_pass'] for t in pairs)} pass the synthetic reserve. This is not a portfolio shortlist or approval. A cash reserve pass cannot clear unit identity, lender eligibility or exit value. The no-purchase comparator preserves the starting cash before any unmodelled cash return.",'',
'## Scenario detail by expression','',
'Every case includes base, low/high rent, rate, rent cut, charge increase, twelve-month vacancy, works, lower bank valuation, 25-year term, six-year exit and an unquoted-cost buffer. Combined stress has a twelve-month horizon and cannot be compared directly with five-year recovery prices. Standard monthly figures above always retain the common 90/4/35 baseline; stressed cashflows below use actual scenario terms.','']
papers=['# PJ full G0-G9 case workpapers','', 'Cutoff 7 October 2026. Fourteen expressions; G0 stops remain binding. G1-G8 findings are conditional diagnostics, not passed gates. These workpapers supersede unsupported owner-first/non-investor-exit wording for inherited compact cases without editing historical papers or Core. See B03_Evidence_and_Supply.md for source ledger and B03_Divergence_and_Misses.md for investigations.','']
for r in results:
    c=r['case'];b=r['scenarios']['base'];d=r['boundaries']
    intro += [f"### {c['id']} - {c['name']}",'','| Scenario / months | Entry cash | Year1 cashflow | Nominal recovery sale | Minimum synthetic cash |','|---|---:|---:|---:|---:|']
    for name,v in r['scenarios'].items():
        intro.append(f"| {name} / {v['months']} | {v['entry_cash']:,.0f} | {v['cashflow_by_year'][0]:+,.0f} | {v['terminal_nominal_breakeven']:,.0f} | {v['minimum_cash']:,.0f} |")
    intro.append('')
    papers += [f"## {c['id']} - {c['name']}",'',f"{c['area_id']}; {c['sqft']} sf; {c['layout']}. Dates: {c['evidence_dates']}.",'',f"Evidence boundary: {c['source_note']}",'']
    if 'sale_source' in c:papers += [f"[Sale]({c['sale_source']}); [rent lead]({c['rent_source']}). R3 raw: {', '.join(c['retrievals'])}.",'']
    else:
        link='../round-2/cases/'+c['id']+'.md' if c['id'].startswith('R2') else '../Case_Workpapers.md'
        papers += [f"Retained inputs: {'round-2/Case_Inputs.json and case paper '+c['id'] if c['id'].startswith('R2') else 'round-1 Case_Inputs.json, E22-E24 source ledger'}. Original retrieval lineage stays in that release; R3 adds the regional ledger.",'']
    gates=[
    ('G0 Reference-Price Validity','STOP. '+c['comp']+' No undervaluation conclusion or executable entry range.'),
    ('G1 Market Mechanism',c['mechanism']+' This is a falsifiable hypothesis; no catalyst rent growth credited.'),
    ('G2 Buyer Universe',c['buyer']+' Actual buyer motives and financing capacity are not measured.'),
    ('G3 Project Quality',c['project']+' Missing evidence is neither a healthy nor a failed rating.'),
    ('G4 Unit Quality',c['source_note']+' Exact approved plan, floor, light/noise/privacy and parking/circulation remain uninspected.'),
    ('G5 Price / Mispricing',f"G0 remains stopped. Mechanical standard price {d['standard_price']:,.0f}; preferred 6% price {d['gross6_price']:,.0f}. These are not fair values. "+c['reversal']),
    ('G6 Exit Architecture',c['buyer']+f" Required five-year nominal recovery sale {b['terminal_nominal_breakeven']:,.0f}; flat-price profit {b['profit_by_exit_multiple']['1']:+,.0f}. Required price is not supported demand. Investor yield expansion, competing stock and unit penalties can constrain exit; longer holding is not an exit."),
    ('G7 Financing / Terminal Risk',f"90/4/35 standard; actual lending unresolved. Entry cash {b['entry_cash']:,.0f}; annual carry {b['cashflow_by_year'][0]:+,.0f}. See full stress and debt reconciliation. Title, lease, charges and valuation can increase equity or lower financeability; no automatic bank rule inferred."),
    ('G8 Portfolio / Opportunity Cost','Compare no purchase and the named substitutes. Correlated hold, works and credit stress is in the financial report. Synthetic liquidity is not the user balance sheet; no allocation inferred.'),
    ('G9 Capital Decision','Defer. '+c['hold']+'. '+('Current standard shortfall: lowest investment-research tier; reopen only on evidenced entry/income/cost transition.' if b['current_shortfall'] else 'Conditional standard coverage does not establish complete-cost carry, a safety margin or readiness.'))]
    papers += ['| Gate | Finding |','|---|---|']+[f"| {g} | {v} |" for g,v in gates]+['',
    f"**Financial result:** gross {b['gross_yield']:.2%}; standard {b['standard_monthly_balance']:+,.0f}/month; annual carry {b['cashflow_by_year'][0]:+,.0f}; annual-neutral rent {d['annual_neutral_rent']:,.0f}.",
    '', '**Product assessment:** '+c['mechanism']+' No project-quality score is warranted before operations and unit verification.',
    '', '**Strongest counter-thesis / falsification:** '+c['reversal']+' Reject the proposed income mechanism if authenticated comparable rents net of concessions fail its stated burden at a feasible price, or a confirmed structural defect makes the relevant buyer task unworkable. Unknowns are not falsification.',
    '', '**Finite next evidence and reopening:** '+c['next']+' Complete that bounded identity/income/exit chain before promotion; do not repeat generic searches if it cannot change the current Defer.',
    '', '**Outcome status:** pre-outcome research only; no purchase, realised return or predictive-validation hit.','']
intro += ['## Verification','',f"{checks} scenario evaluations passed closed-form amortisation, principal conservation, independent economic-cost recovery and discounted-hurdle identities. {len(pairs)} joint cash paths reconcile without double-counting starting cash. A nine-cell rent grid demonstrates rank reversal. These verify arithmetic, not market inputs or realised investment outcomes.",'']
(P/'B03_Financial_Underwriting.md').write_text('\n'.join(intro)+'\n',encoding='utf-8')
(P/'B03_Cases_G0_G9.md').write_text('\n'.join(papers)+'\n',encoding='utf-8')
print(json.dumps(dict(cases=14,checks=checks,pairs=len(pairs),annual_nonnegative=[r['case']['id'] for r in results if r['scenarios']['base']['cashflow_by_year'][0]>=0],base=[dict(id=r['case']['id'],standard=round(r['scenarios']['base']['standard_monthly_balance']),annual=round(r['scenarios']['base']['cashflow_by_year'][0]),gross=round(r['scenarios']['base']['gross_yield']*100,2)) for r in results]),indent=2))

