"""B04 bounded regional scenario release. Frozen financial engine is imported read-only."""
import json,importlib.util,itertools
from pathlib import Path
P=Path(__file__).resolve().parent; ROOT=P.parent.parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
spec=importlib.util.spec_from_file_location('frozen_engine',ROOT/'execution-release-2026-10-07/financial_engine.py')
e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
old=read(P.parent/'Case_Inputs.json')['cases']+read(P.parent/'round-2/Case_Inputs.json')['cases']
meta=read(P/'B04_Inherited_Assessments.json')
cases=[]
for c in old:
 if c['batch']!='B04':continue
 c=dict(c);c.update(meta[c['id']]);c.update(source_note=c.get('match',''),evidence_dates='Inherited cutoff7October2026; original source dates retained',hold=c.get('quarantine') or 'Exact unit, rent/costs and adjusted reference remain unverified')
 cases.append(c)
cases+=read(P/'B04_Case_Inputs.json')['cases']
assert len(cases)==19 and len({c['id'] for c in cases})==19
results=[];checks=0
for c in cases:
 params={'base':{},'rent_low':{'rent_factor':c['rent_low']/c['rent_assumed']},'rent_high':{'rent_factor':c['rent_high']/c['rent_assumed']},'rate_5_5':{'rate':.055},'rent_down20':{'rent_factor':.8},'fee_up20':{'fee_factor':1.2},'vacancy12':{'initial_vacancy':12},'works30k':{'levy_month':24,'levy':30000},'valuation85pct':{'valuation_ratio':.85},'term25':{'term':25},'exit_delay12':{'months':72},'extra_cost_buffer':{'annual_extra_cost':1200,'exit_extra_cost':5000},'combined12':{'months':12,'rate':.055,'rent_factor':.8,'fee_factor':1.2,'first_year_paid':6,'levy_month':1,'levy':30000}}
 if c['id']=='R317':params['existing_lease_no_credit6']={'first_year_paid':6,'initial_vacancy':6}
 sc={}
 for n,kw in params.items():
  r=e.evaluate(c,**kw);e.check_financial_identities(r,c,kw.get('exit_extra_cost',0));checks+=1;sc[n]=r
 b=sc['base'];f=e.payment(.9,.04,35)
 boundaries=dict(standard_price=(c['rent_assumed']-c['fee_assumed'])/f,gross6_price=c['rent_assumed']*200,standard_rent=b['actual_instalment']+c['fee_assumed'],annual_neutral_rent=12*(b['actual_instalment']+c['fee_assumed']+c['other_assumed'])/11)
 exits=[dict(gross_yield=y,price=12*c['rent_assumed']/y,profit=.97*12*c['rent_assumed']/y-b['terminal_debt']+b['cashflow_total']-b['entry_cash']) for y in [.06,.07,.08]]
 results.append(dict(case=c,scenarios=sc,boundaries=boundaries,yield_exits=exits,future_buyer_90_5_5_25=e.payment(.9*b['terminal_nominal_breakeven'],.055,25)))
by={r['case']['id']:r for r in results}
pairs=[]
for a,b in itertools.combinations(results,2):
 aa=a['scenarios']['combined12'];bb=b['scenarios']['combined12']
 path=[e.CFG['synthetic_cash']-aa['entry_cash']-bb['entry_cash']]
 for x,y in zip(aa['schedule'],bb['schedule']):path.append(path[-1]+x['cashflow']+y['cashflow'])
 assert abs(path[-1]-(e.CFG['synthetic_cash']-aa['entry_cash']-bb['entry_cash']+aa['cashflow_total']+bb['cashflow_total']))<.01
 pairs.append(dict(ids=[aa['id'],bb['id']],minimum_cash=min(path),reserve_pass=min(path)>=e.CFG['synthetic_protected_reserve'],cash_path=path))
rank=[]
for a,b in itertools.product([3200,3800,4500],[3300,4000,4200]):
 x=e.evaluate(dict(by['R315']['case'],rent_assumed=a));y=e.evaluate(dict(by['R316']['case'],rent_assumed=b))
 rank.append(dict(pines_rent=a,windsor_rent=b,pines_balance=x['standard_monthly_balance'],windsor_balance=y['standard_monthly_balance'],leader='R315' if x['standard_monthly_balance']>y['standard_monthly_balance'] else 'R316'))
assert {x['leader'] for x in rank}=={'R315','R316'}
alternatives=[]
for cid,p in [('R216',285888),('R313',668000),('R319',470000)]:
 c=dict(by[cid]['case'],price=p);b=e.evaluate(c);e.check_financial_identities(b,c);checks+=1
 alternatives.append(dict(id=cid,price=p,result=b))
out=dict(version='KV-B04-2026-10-07-R3',config=e.CFG,results=results,diagnostic_pairs=pairs,rank_grid=rank,alternative_prices=alternatives,financial_identity_checks=checks,programme_complete=False,deploy=0)
(P/'B04_Financial_Results.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
lines=['# B04 financial underwriting','',
'Cutoff7October2026. All RM. Nineteen conditional expressions across nine catchments; ten inherited and nine new. No normalised clearing value, authenticated ordinary lease, current fee bill or lender offer. All G0 STOP / G9 Defer. Index/identity-held results cannot enter an executable shortlist.','',
'User standard:90%purchase-price loan,4%,35years; full instalment plus unverified combined service/sinking proxy. Five-year hold, eleven collected months per year,5%entry and3%disposal allowances, stated refurbishment and monthly other-cost provisions. No rent/price growth. Pre-tax: actual tax, loan, duties and project-specific costs are unresolved, not zero. Other costs provision routine repair/insurance/assessment/reletting and must be itemised before decision. Initial works are unquoted. The8%equity hurdle and500kstarting cash/150kreserve are illustrations, not personal targets or balances.','',
'Full instalment enters cashflow; principal is reconciled to remaining debt once, not double-counted as economic loss. Standard coverage is distinct from annual carry and total return. Future-buyer stress reported here retains90%LTV; the engine legacy80%field is not used. Valuation stress means90%of a value15%below purchase price, requiring extra equity.','',
'United Point R317 base is a hypothetical stabilised furnished-rent scenario. The sale is advertised with an existing tenancy untilMarch2027 but its rent is undisclosed. Do not present2500as contracted income. A separate no-credit first-six-month sensitivity bounds that income gap conservatively; it is not a claim of actual tenant nonpayment. Works charged upfront are conservative cash timing, not an approved refurbishment schedule.','',
'## Base entry and carry','',
'| Case | Expression | Price / rent | Fee / other / works | Gross | Standard monthly | Annual carry | Entry cash |',
'|---|---|---:|---:|---:|---:|---:|---:|']
for r in results:
 c=r['case'];b=r['scenarios']['base']
 lines.append(f"| {c['id']} | {c['name']} | {c['price']:,.0f} / {c['rent_assumed']:,.0f} | {c['fee_assumed']:,.0f} / {c['other_assumed']:,.0f} / {c['refurb_assumed']:,.0f} | {b['gross_yield']:.2%} | {b['standard_monthly_balance']:+,.0f} | {b['cashflow_by_year'][0]:+,.0f} | {b['entry_cash']:,.0f} |")
lines+=['','Cliveden and Neo retain live-offer/component evidence holds. A positive annual number is not a cleared candidate. Every fee, non-rent cost and works input remains a planning allowance; low/high rent endpoints are scenarios, not confidence intervals.','',
'## Required price and rent conditions','',
'| Case | Standard price | Price at6%gross | Rent for standard | Rent for annual neutrality |','|---|---:|---:|---:|---:|']
for r in results:
 d=r['boundaries'];lines.append(f"| {r['case']['id']} | {d['standard_price']:,.0f} | {d['gross6_price']:,.0f} | {d['standard_rent']:,.0f} | {d['annual_neutral_rent']:,.0f} |")
lines+=['','Price boundaries are constraints, not market values, bids or a margin of safety. Meeting both numeric preferences cannot override identity, quality, lending or exit failures. Current shortfall means lowest investment-research priority, not a structural Reject. Reopen only on evidenced entry/rent/cost change with timing and funded carry; no speculative catalyst uplift.','',
'## Five-year terminal burden','',
'| Case | Debt | Nominal recovery sale | Sale for8%hurdle | Profit at flat exit | Profit at-20%exit | Future payment90/4/35 | Future payment90/5.5/25 |','|---|---:|---:|---:|---:|---:|---:|---:|']
for r in results:
 b=r['scenarios']['base'];lines.append(f"| {b['id']} | {b['terminal_debt']:,.0f} | {b['terminal_nominal_breakeven']:,.0f} | {b['terminal_8pct_required']:,.0f} | {b['profit_by_exit_multiple']['1']:+,.0f} | {b['profit_by_exit_multiple']['0.8']:+,.0f} | {b['future_buyer_standard_payment_at_breakeven']:,.0f} | {r['future_buyer_90_5_5_25']:,.0f} |")
lines+=['','Required exits are recovery burdens, not price forecasts or validated buyer willingness. Missing foreign/local buyer equity, lending and motive evidence is not assumed. Investor-led exits remain admissible; unverified owner adoption provides no base premium.','',
'| Case | Price at6%gross | At7% | At8% | Total profit at7%exit |','|---|---:|---:|---:|---:|']
for r in results:
 t=r['yield_exits'];lines.append(f"| {r['case']['id']} | {t[0]['price']:,.0f} | {t[1]['price']:,.0f} | {t[2]['price']:,.0f} | {t[1]['profit']:+,.0f} |")
lines+=['','Constant assumed rent and gross-yield capitalisation are diagnostics only. A6%to7%required yield change cuts this diagnostic price14.29%; to8%cuts25%. Net-income valuation needs actual costs. Do not capitalise short-stay, room or luxury fitted rents as an ordinary whole-unit lease.','',
'## Different advertised price leads','',
'| Case | Alternate price | Standard monthly | Annual carry | Meaning |','|---|---:|---:|---:|---|']
meanings=['September Cliveden500sf285888index, a different offer; old250knot refreshed.','Ascencia668kAugust index, not same690kunit negotiation.','Fortune470kAugust index versus480kSeptember individual; not same rights/condition proved.']
for t,m in zip(alternatives,meanings):
 b=t['result'];lines.append(f"| {t['id']} | {t['price']:,.0f} | {b['standard_monthly_balance']:+,.0f} | {b['cashflow_by_year'][0]:+,.0f} | {m} |")
lines+=['','WestsideThree749k is deliberately not priced into this table: header/body geography conflicts disqualify it as a supported project-price pair. Neo210k/220kposted in rental categories remains a classification/freshness lead; no such amount is rental income.','',
'## Rent-driven ranking reversal','',
'| Pines rent | Windsor rent | Pines standard monthly | Windsor standard monthly | Coverage leader |','|---:|---:|---:|---:|---|']
for t in rank:lines.append(f"| {t['pines_rent']:,.0f} | {t['windsor_rent']:,.0f} | {t['pines_balance']:+,.0f} | {t['windsor_balance']:+,.0f} | {t['leader']} |")
lines+=['','No probability weights or overall product ranking follow from this grid. A rent/fee/renovation difference can reverse the order; matching those inputs has greater next-step value than a suburb prestige label.','',
'## Correlated twelve-month hold','',
'5.5%rate,20%rent reduction, six paid months,20%fee increase and30kworks per property in month1. Same500kcash pool, protected150kreserve; no salary, refinancing or sale rescue. All171pairs are diagnostic, including held expressions; none is an allocation recommendation.','',
'| Pair | Minimum cash | Reserve pass |','|---|---:|---|']
for ids in [('R315','R316'),('KV09','R319'),('R314','R246'),('R216','R219')]:
 t=next(t for t in pairs if set(t['ids'])==set(ids));lines.append(f"| {' + '.join(ids)} | {t['minimum_cash']:,.0f} | {'Yes, synthetic only' if t['reserve_pass'] else 'No'} |")
lines+=['',f"{sum(t['reserve_pass'] for t in pairs)} of171pairs retain the synthetic reserve. Capital sufficiency cannot clear missing identity/rent/quality or prove risk diversification. Two prime addresses can share the same household, financing, vacancy and strata-cost shock. No purchase retains the starting cash before unmodelled cash returns.",'',
'## Scenario detail','',
'Combined stress has a12-month horizon; other cases generally use60months and delayed exit72. Compare recovery prices only at equivalent horizons. Actual scenario cashflow uses stressed terms, while standard monthly numbers above remain90/4/35.','']
papers=['# B04 full G0-G9 workpapers','',
'Cutoff7October2026. Nineteen conditional expressions. Existing gate names and stops remain authoritative; downstream diagnostics are not passes. Compact investor-led exits do not require a universally surviving non-investor channel. See B04_Evidence_and_Supply.md and B04_Divergence_and_Misses.md.','']
for r in results:
 c=r['case'];b=r['scenarios']['base'];d=r['boundaries']
 lines += [f"### {c['id']} - {c['name']}",'','| Scenario / horizon | Entry cash | Year1 cashflow | Recovery sale | Minimum cash |','|---|---:|---:|---:|---:|']
 for n,v in r['scenarios'].items():lines.append(f"| {n} / {v['months']}m | {v['entry_cash']:,.0f} | {v['cashflow_by_year'][0]:+,.0f} | {v['terminal_nominal_breakeven']:,.0f} | {v['minimum_cash']:,.0f} |")
 lines.append('')
 papers += [f"## {c['id']} - {c['name']}",'',f"{c['area_id']}; {c['sqft']}sf; {c['layout']}. {c['evidence_dates']}.",'',f"Observed-source boundary: {c['source_note']}",'']
 if 'sale_source' in c:papers += [f"[Sale]({c['sale_source']}); [rent]({c['rent_source']}). B04 raw: {', '.join(c['retrievals'])}.",'']
 else:papers += [f"Original source lineage remains in {'round-1 Evidence_Register.md and Selected_Case_Workpapers.md' if c['id'].startswith('KV') else 'round-2/cases/'+c['id']+'.md'}. New evidence is in the B04 ledger; inherited inputs are not silently refreshed.",'']
 gates=[
 ('G0 Reference-Price Validity','STOP. '+c['comp']+' No normalised effective clearing interval or undervaluation conclusion.'),
 ('G1 Market Mechanism',c['mechanism']+' Hypothesis only; no speculative rent/capital uplift.'),
 ('G2 Buyer Universe',c['buyer']+' Actual willingness, ability and depth remain unmeasured.'),
 ('G3 Project Quality',c['project']+' Unknown does not mean healthy or failed.'),
 ('G4 Unit Quality',c['source_note']+' Approved plan, privacy/noise/light, bay/circulation and irreversible externalities not inspected.'),
 ('G5 Price / Mispricing',f"Unadjudicated while G0 is stopped. Standard price boundary {d['standard_price']:,.0f};6%gross boundary {d['gross6_price']:,.0f}; neither is fair value. "+c['reversal']),
 ('G6 Exit Architecture',c['buyer']+f" Five-year recovery requires {b['terminal_nominal_breakeven']:,.0f}; unchanged-price profit {b['profit_by_exit_multiple']['1']:+,.0f}. No proven exit ceiling/floor or sale velocity. Adverse investor yields and competing products are tested; longer holding is capital exposure, not an exit."),
 ('G7 Financing / Terminal Risk',f"Standard90/4/35; actual title, lease, lender valuation and borrower eligibility unresolved. Entry cash {b['entry_cash']:,.0f}; annual conditional carry {b['cashflow_by_year'][0]:+,.0f}. Full debt, term, rate, valuation, works and exit stress is in B04_Financial_Underwriting.md."),
 ('G8 Portfolio / Opportunity Cost','Compare named alternatives and no purchase. Shared tenant/credit/supply/management shocks are tested jointly. Synthetic cash cannot approve the user portfolio or prove diversification.'),
 ('G9 Capital Decision','Defer. '+c['hold']+'. '+('Current standard shortfall receives lowest investment-research priority; require evidenced transition to reopen.' if b['current_shortfall'] else 'A simplified monthly pass cannot clear full costs, evidence gaps or margin of safety.'))]
 papers+=['| Gate | Finding |','|---|---|']+[f"| {g} | {v} |" for g,v in gates]+['',f"**Finance:** gross {b['gross_yield']:.2%};standard monthly {b['standard_monthly_balance']:+,.0f};annual carry {b['cashflow_by_year'][0]:+,.0f};annual-neutral rent {d['annual_neutral_rent']:,.0f}.",'',
 '**Product:** '+c['mechanism']+' This does not award a quality grade.','',
 '**Strongest counter-thesis / falsification:** '+c['reversal']+' If matched ordinary income cannot meet the stated burden at a feasible entry, or a confirmed structural defect prevents the relevant use, the proposed investment mechanism fails. Missing evidence alone proves neither failure nor success.','',
 '**Finite evidence / reopening:** '+c['next']+' Reopen on that decision-changing evidence; another generic listing count does not clear the stop.','',
 '**Validation status:** Pre-outcome research. No purchase, realised return, predictive hit or newly promoted Core mechanism.','']
lines+=['## Verification','',f"{checks}scenario evaluations passed amortisation, principal conservation, independent economic-cost recovery and discounted-hurdle identities.171joint paths reconcile one starting cash pool; nine rent combinations reverse the coverage lead. This validates arithmetic only.",'']
(P/'B04_Financial_Underwriting.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(P/'B04_Cases_G0_G9.md').write_text('\n'.join(papers)+'\n',encoding='utf-8')
print(json.dumps(dict(cases=len(cases),checks=checks,pairs=len(pairs),pair_passes=sum(t['reserve_pass'] for t in pairs),rows=[dict(id=r['case']['id'],gross=round(r['scenarios']['base']['gross_yield']*100,2),standard=round(r['scenarios']['base']['standard_monthly_balance']),annual=round(r['scenarios']['base']['cashflow_by_year'][0])) for r in results]),indent=2))

