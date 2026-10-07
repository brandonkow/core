import json, importlib.util
from pathlib import Path
P=Path(__file__).resolve().parent
ROOT=P.parent.parent
spec=importlib.util.spec_from_file_location('existing_financial_engine', ROOT/'execution-release-2026-10-07/financial_engine.py')
engine=importlib.util.module_from_spec(spec); spec.loader.exec_module(engine)
data=json.loads((P/'Contrasting_Case_Inputs.json').read_text(encoding='utf-8'))
results=[]
papers=['# Additional contrasting expressions - full G0-G9', '', 'Cutoff 7 October 2026. Original gates and Core preserved. All four expressions are conditional diagnostics. Downstream gates are evaluated conditionally after G0 STOP, not falsely marked passed. No Deploy; no current offer or achieved rent certified.', '', 'Financial baseline: 90% purchase-price LTV, 4%, 35 years. Five-year hold; eleven paid months; 5% acquisition and 3% disposal allowances. Combined fee and other operating allowances are unverified and pre-tax. Unknown taxes/charges are not zero. An 8% equity hurdle is illustrative, not a market forecast or a user return mandate.', '']
for c in data['cases']:
    scenarios={
        'base':{}, 'rent_low':{'rent_factor':c['rent_low']/c['rent_assumed']},
        'rent_high':{'rent_factor':c['rent_high']/c['rent_assumed']},
        'rate_5_5':{'rate':.055}, 'rent_down20':{'rent_factor':.8},
        'fee_up20':{'fee_factor':1.2}, 'zero_rent_12m':{'initial_vacancy':12},
        'combined_12m':{'months':12,'rate':.055,'rent_factor':.8,'first_year_paid':6,'levy_month':6,'levy':30000},
        'valuation90pct':{'valuation_ratio':.9}}
    rr={}
    for name, kwargs in scenarios.items():
        rr[name]=engine.evaluate(c,**kwargs)
        engine.check_financial_identities(rr[name],c)
    results.append({'case_id':c['id'],'scenarios':rr})
    b=rr['base']; factor=engine.payment(.9,.04,35)
    papers += [f"## {c['id']} - {c['name']}", '', f"Scope: {c['area_id']} / {c['batch']}; {c['sqft']} sf; {c['layout']}. Identity hold: {c['hold'] or 'No additional component conflict identified; exact parcel is still unverified.'}", '',
               f"Observed source claims: {c['source_note']}", '', f"[Sale source]({c['sale_source']}); [rent source]({c['rent_source']}). Raw retrievals: {', '.join(c['retrievals'])}.", '']
    if c['primary_source']:
        papers += [f"[Developer/source reference]({c['primary_source']}).",'']
    gates=[('G0 Reference-Price Validity','STOP. The advertised expression lacks a normalised rights/condition/incentive-matched clearing interval. '+c['comp']),
           ('G1 Market Mechanism',c['mechanism']),('G2 Buyer Universe',c['buyer']),('G3 Project Quality',c['project']),('G4 Unit Quality',c['unit']),
           ('G5 Price / Mispricing','No undervaluation determination while G0 remains stopped. '+c['counter']),
           ('G6 Exit Architecture',c['comp']+' Income-led buyers must support the required future price from actual sustainable income. Owner use is an additional channel only when evidenced; holding longer is not an exit.'),
           ('G7 Financing / Terminal Risk','Standardised finance is arithmetic, not a lender offer. Identity/title, bank valuation, remaining lease and purchaser eligibility remain checks. The full scenario table below carries debt, reserves and terminal burden; no source establishes a resale floor.'),
           ('G8 Portfolio / Opportunity Cost','Compare with the no-purchase option and stated substitutes. A second KL-strata property may share tenant, financing, supply and management-cost shocks. Synthetic RM500,000 liquidity / RM150,000 reserve is not the user balance sheet and does not approve allocation.'),
           ('G9 Capital Decision','Defer. Reference value, exact unit and operating/rental evidence remain unresolved. Current standard shortfall receives lowest research priority, not an automatic structural Reject.')]
    papers += ['| Gate | Case finding |','|---|---|']+[f'| {gate} | {finding} |' for gate,finding in gates]+['', '### Complete-cost and terminal diagnostics', '',
               '| Scenario | Entry cash | First-year cashflow | Debt at horizon | Nominal recovery sale | Sale for 8% equity hurdle | Minimum synthetic cash |', '|---|---:|---:|---:|---:|---:|---:|']
    for name,r in rr.items():
        papers.append(f"| {name} ({r['months']} months) | {r['entry_cash']:,.0f} | {r['cashflow_by_year'][0]:,.0f} | {r['terminal_debt']:,.0f} | {r['terminal_nominal_breakeven']:,.0f} | {r['terminal_8pct_required']:,.0f} | {r['minimum_cash']:,.0f} |")
    papers += ['',f"Base gross scenario {b['gross_yield']:.2%}; standard monthly balance {b['standard_monthly_balance']:+,.0f}; five-year profit at unchanged sale price {b['profit_by_exit_multiple']['1']:+,.0f}. Principal is included in cashflow and reconciled to terminal debt; it is not charged twice as economic loss.", '',
               f"Mechanical price boundary: standard {(c['rent_assumed']-c['fee_assumed'])/factor:,.0f}; 6% gross {200*c['rent_assumed']:,.0f}. Required annual cash-neutral rent {12*(b['actual_instalment']+c['fee_assumed']+c['other_assumed'])/11:,.0f}. These are not fair values or automatic offers.", '',
               '**Product versus investment:** '+c['mechanism']+' Product usefulness does not settle an investable price.', '', '**Falsification / rank switch:** '+c['reversal'], '',
               '**Finite evidence route:** '+c['next'], '', '**Public boundary:** sources establish the stated advertised product and counterexamples only. No site visit, authenticated lease, lender valuation or MC accounts were inspected. Missing proof is retained as missing; no assumption that the property is healthy or failed.', '']
(P/'Contrasting_Case_Financials.json').write_text(json.dumps({'version':data['version'],'config':engine.CFG,'results':results,'identities_checked':len(results)*9},indent=2)+'\n',encoding='utf-8')
(P/'Contrasting_Cases_G0_G9.md').write_text('\n'.join(papers)+'\n',encoding='utf-8')
# Current-basis comparative table, retaining source identity and without rewriting releases.
allcases=json.loads((P.parent/'Case_Inputs.json').read_text(encoding='utf-8'))['cases']+json.loads((P.parent/'round-2/Case_Inputs.json').read_text(encoding='utf-8'))['cases']+data['cases']
allcases=[c for c in allcases if c['batch'] in ['B01','B02']]
values=[engine.evaluate(c) for c in allcases]
old=json.loads((ROOT/'execution-release-2026-10-07/Financial_Results.json').read_text(encoding='utf-8'))['base']
values=old+values
compare=['# B01-B02 current-basis comparison', '', 'All monetary values RM. Current 90%/4%/35-year calculations only; old 80%/30-year Cheras outputs are not used here. Existing assumptions are not refreshed achieved rents. The table combines dated expressions, not unique verified units. The original gate papers and round 3 status overrides remain binding.', '',
         '| Case | Project/expression | Entry scenario | Rent | Standard/month | Annual cashflow | Five-year recovery sale | Five-year flat-price profit |', '|---|---|---:|---:|---:|---:|---:|---:|']
for b in values:
    compare.append(f"| {b['id']} | {b['name']} | {b['price']:,.0f} | {b['rent_assumed']:,.0f} | {b['standard_monthly_balance']:+,.0f} | {b['cashflow_by_year'][0]:+,.0f} | {b['terminal_nominal_breakeven']:,.0f} | {b['profit_by_exit_multiple']['1']:+,.0f} |")
compare += ['', 'R205 remains quarantined; R303 uses an index-only offer; R304 has a component-use hold. Their numeric rows cannot be ranked as eligible residential candidates. No future young-owner premium or catalyst rent growth is added.', '',
            'At an unchanged buyer rent, a required gross yield moving from 6% to 7% reduces the diagnostic investor price by 14.29%; to 8%, by 25%. This is a scenario identity, not an estimated probability or a fair-value forecast.']
(P/'B01_B02_Financial_Comparison.md').write_text('\n'.join(compare)+'\n',encoding='utf-8')
print(json.dumps({'new_controls':len(results),'scenario_identities_checked':len(results)*9,'comparison_expressions':len(values),'new_deploy':0}))
