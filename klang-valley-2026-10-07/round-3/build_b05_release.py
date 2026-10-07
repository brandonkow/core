"""B05 scenario release using the unmodified frozen financial engine."""
import json,importlib.util,itertools,gzip
from pathlib import Path
P=Path(__file__).resolve().parent; ROOT=P.parent.parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(name,value): (P/name).write_text(value+'\n',encoding='utf-8')
spec=importlib.util.spec_from_file_location('frozen_engine',ROOT/'execution-release-2026-10-07/financial_engine.py')
e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
old=read(P.parent/'Case_Inputs.json')['cases']+read(P.parent/'round-2/Case_Inputs.json')['cases']
meta=read(P/'B05_Inherited_Assessments.json')
cases=[]
for c in old:
 if c['batch']!='B05':continue
 c=dict(c);c.update(meta[c['id']]);c.update(source_note=c['match'],evidence_dates='Inherited cutoff7October2026; original source dates and numerical inputs retained')
 cases.append(c)
cases+=read(P/'B05_Case_Inputs.json')['cases']
assert len(cases)==16 and len({c['id'] for c in cases})==16
results=[];checks=0
for c in cases:
 params={'base':{},'rent_low':{'rent_factor':c['rent_low']/c['rent_assumed']},'rent_high':{'rent_factor':c['rent_high']/c['rent_assumed']},'rate_5_5':{'rate':.055},'rent_down20':{'rent_factor':.8},'fee_up20':{'fee_factor':1.2},'vacancy12':{'initial_vacancy':12},'works30k':{'levy_month':24,'levy':30000},'valuation85pct':{'valuation_ratio':.85},'term25':{'term':25},'exit_delay12':{'months':72},'extra_cost_buffer':{'annual_extra_cost':1200,'exit_extra_cost':5000},'combined12':{'months':12,'rate':.055,'rent_factor':.8,'fee_factor':1.2,'first_year_paid':6,'levy_month':1,'levy':30000}}
 if c['id']=='R328':params['existing_lease_no_credit6']={'first_year_paid':6,'initial_vacancy':6}
 sc={}
 for n,kw in params.items():
  r=e.evaluate(c,**kw);e.check_financial_identities(r,c,kw.get('exit_extra_cost',0));checks+=1;sc[n]=r
 b=sc['base'];f=e.payment(.9,.04,35)
 boundaries=dict(standard_price=(c['rent_assumed']-c['fee_assumed'])/f,gross6_price=c['rent_assumed']*200,standard_rent=b['actual_instalment']+c['fee_assumed'],annual_neutral_rent=12*(b['actual_instalment']+c['fee_assumed']+c['other_assumed'])/11)
 exits=[dict(gross_yield=y,price=12*c['rent_assumed']/y,profit=.97*12*c['rent_assumed']/y-b['terminal_debt']+b['cashflow_total']-b['entry_cash']) for y in [.06,.07,.08]]
 results.append(dict(case=c,scenarios=sc,scenario_parameters=params,boundaries=boundaries,yield_exits=exits,future_buyer_90_5_5_25=e.payment(.9*b['terminal_nominal_breakeven'],.055,25)))
by={r['case']['id']:r for r in results}
pairs=[]
for a,b in itertools.combinations(results,2):
 aa=a['scenarios']['combined12'];bb=b['scenarios']['combined12']
 path=[e.CFG['synthetic_cash']-aa['entry_cash']-bb['entry_cash']]
 for x,y in zip(aa['schedule'],bb['schedule']):path.append(path[-1]+x['cashflow']+y['cashflow'])
 pairs.append(dict(ids=[aa['id'],bb['id']],minimum_cash=min(path),reserve_pass=min(path)>=e.CFG['synthetic_protected_reserve'],cash_path=path,coexisting_units_verified=False))
rank=[]
for a,b in itertools.product([1900,2200,2400],[2100,2400,2700]):
 x=e.evaluate(dict(by['R321']['case'],rent_assumed=a));y=e.evaluate(dict(by['R328']['case'],rent_assumed=b))
 rank.append(dict(parkview_rent=a,titiwangsa_rent=b,parkview_balance=x['standard_monthly_balance'],titiwangsa_balance=y['standard_monthly_balance'],leader='R321' if x['standard_monthly_balance']>y['standard_monthly_balance'] else 'R328'))
assert {x['leader'] for x in rank}=={'R321','R328'}
alternatives=[]
for cid,change,label in [
 ('R322',{'fee_assumed':1165/3},'Hypothesis only:1165 is a quarterly invoice; not verified fee period.'),
 ('R323',{'price':1860000},'Different850-sf1860kSeptember index; rights/fit-out unverified, not negotiated1950koffer.'),
 ('R325',{'price':530000},'Historical April1378-sf530kindex, unconfirmed live offer; not identical650kunit.')]:
 c=dict(by[cid]['case'],**change);b=e.evaluate(c);e.check_financial_identities(b,c);checks+=1
 alternatives.append(dict(id=cid,change=change,case=c,result=b,meaning=label))
out=dict(version='KV-B05-2026-10-07-R3',config=e.CFG,results=results,diagnostic_pairs=pairs,rank_grid=rank,alternatives=alternatives,financial_identity_checks=checks,programme_complete=False,deploy=0)
summary=dict(out,results=[dict(r,scenarios={k:{a:b for a,b in v.items() if a not in ['schedule','cash_path']} for k,v in r['scenarios'].items()}) for r in results],alternatives=[{**t,'result':{k:v for k,v in t['result'].items() if k not in ['schedule','cash_path']}} for t in alternatives])
summary['monthly_detail']='Reconstruct from stored cases, scenario_parameters and frozen financial engine; all monthly identity and pair-path checks replayed by verify_b05_release.py. Individual60-month schedules omitted from storage only; no scenario or cashflow aggregation omitted.'
write('B05_Financial_Results.json',json.dumps(summary,separators=(',',':')))
lines=['# B05 financial underwriting','',
'Cutoff:7October2026. All RM. Sixteen conditional expressions across seven catchments: seven inherited and nine new. G0 STOP / G9 Defer throughout. No normalised clearing value, authenticated ordinary lease, current fee invoice or lender offer. Positive scenario arithmetic does not clear an investment.','',
'## Basis and special conditions','',
'90%purchase-price LTV,4%,35years; five-year hold, eleven paid months/year,5%entry and3%disposal allowances, stated initial works and monthly other-cost provisions; zero rent or capital growth. Costs are planning allowances, not quotations. Pre-tax: actual tax, financing/legal/stamp-duty amounts, arrears and project-specific expenses are unresolved, not verified zero. Other-cost provision covers routine repair, insurance, assessments and reletting; itemisation remains necessary. Fee is a combined management/sinking proxy. The8%equity hurdle and500kstarting cash/150kreserve are illustrations, not personal user targets or cash balances.','',
'Full instalment is included in cashflow; debt amortisation/principal is reconciled once. Standard monthly coverage excludes vacancy and other costs. Annual carry includes eleven rent months and12months of instalment, fee and other provision, but entry works/costs are charged separately upfront. Terminal profit includes those entry costs. Current shortfall is lowest investment-research priority, not permanent Reject. A transition thesis needs observed change, timing and funded carry.','',
'R322 Lucentia base is explicitly the unverified monthly interpretation of the advertised1165charge. Quarterly1165/3 is a separate hypothesis; neither is a confirmed charge. No optimistic fee averaging. R328 Titiwangsa uses hypothetical stabilised2700rent from another unit; the advertised sale is tenanted with unknown rent/expiry. No-credit first-six-month sensitivity bounds that income gap, not actual tenant default. Upfront works are a conservative cash assumption, not an approved tenancy renovation schedule.','',
'R329 is a different280k28Boulevard sale lead with25kfit-out/works versus15kfor the old380kR225scenario. The1650rental midpoint is inherited, not newly achieved. Both component identities remain held. R325 uses650knewer offer evidence;530kApril only appears as an explicitly stale alternative. All rent endpoints are scenarios, not statistical confidence bounds.','',
'## Entry and annual carry','',
'| Case | Expression | Price / rent | Fee / other / works | Gross | Standard monthly | Annual carry | Entry cash |',
'|---|---|---:|---:|---:|---:|---:|---:|']
for r in results:
 c=r['case'];b=r['scenarios']['base']
 lines.append(f"| {c['id']} | {c['name']} | {c['price']:,.0f} / {c['rent_assumed']:,.0f} | {c['fee_assumed']:,.0f} / {c['other_assumed']:,.0f} / {c['refurb_assumed']:,.0f} | {b['gross_yield']:.2%} | {b['standard_monthly_balance']:+,.0f} | {b['cashflow_by_year'][0]:+,.0f} | {b['entry_cash']:,.0f} |")
lines+=['','## Conditions for coverage','',
'| Case | Standard price boundary | Price at6%gross | Rent for standard | Rent for annual neutrality |','|---|---:|---:|---:|---:|']
for r in results:
 d=r['boundaries'];lines.append(f"| {r['case']['id']} | {d['standard_price']:,.0f} | {d['gross6_price']:,.0f} | {d['standard_rent']:,.0f} | {d['annual_neutral_rent']:,.0f} |")
lines+=['','These are numerical constraints, not supported market values, offers or a margin of safety. A required lower price may never be available for an equivalent asset. Unresolved divergence requires more evidence and a larger justified safety margin; no fixed discount can be derived without a valid reference.','',
'## Terminal burden and future buyer','',
'| Case | Year5 debt | Nominal recovery sale | Sale for8%hurdle | Profit at flat exit | Profit at-20%exit | Buyer payment90/4/35 | Buyer payment90/5.5/25 |','|---|---:|---:|---:|---:|---:|---:|---:|']
for r in results:
 b=r['scenarios']['base'];lines.append(f"| {b['id']} | {b['terminal_debt']:,.0f} | {b['terminal_nominal_breakeven']:,.0f} | {b['terminal_8pct_required']:,.0f} | {b['profit_by_exit_multiple']['1']:+,.0f} | {b['profit_by_exit_multiple']['0.8']:+,.0f} | {b['future_buyer_standard_payment_at_breakeven']:,.0f} | {r['future_buyer_90_5_5_25']:,.0f} |")
lines+=['','Required exits are burdens, not predicted values or validated ceilings/floors. Future buyer stress retains90%LTV; the imported engine legacy80%field is not used in decisions or this table. Valuation stress separately finances90%of a valuation15%below price, requiring additional cash. Actual borrower/lender/title eligibility and willingness remain unresolved.','',
'| Case | Diagnostic price at6%gross | At7% | At8% | Total profit at7%exit |','|---|---:|---:|---:|---:|']
for r in results:
 t=r['yield_exits'];lines.append(f"| {r['case']['id']} | {t[0]['price']:,.0f} | {t[1]['price']:,.0f} | {t[2]['price']:,.0f} | {t[1]['profit']:+,.0f} |")
lines+=['','Investor-led exits are admissible. At fixed assumed rent,6%to7%required gross yield reduces diagnostic price14.29%;6%to8%reduces it25%. These are gross-income sensitivities; net-income valuation requires actual costs. No assumed owner-occupier premium rescues a weak investor exit.','',
'## Decision-changing alternative interpretations','',
'| Case | Changed input | Standard monthly | Annual carry | Five-year recovery sale | Meaning |','|---|---|---:|---:|---:|---|']
for t in alternatives:
 b=t['result'];lines.append(f"| {t['id']} | {t['change']} | {b['standard_monthly_balance']:+,.0f} | {b['cashflow_by_year'][0]:+,.0f} | {b['terminal_nominal_breakeven']:,.0f} | {t['meaning']} |")
lines+=['','TRX550k1640-sf advertisement501960003 is excluded from valuation: body says1420-sf three-bedroom duplex5kmfromcentre, conflicting with header geography/rooms. This is an identity hold, not evidence of extreme TRX mispricing.','',
'## Rent-dependent reversal','',
'| Parkview rent | Titiwangsa rent | Parkview standard balance | Titiwangsa standard balance | Coverage leader |','|---:|---:|---:|---:|---|']
for t in rank:lines.append(f"| {t['parkview_rent']:,.0f} | {t['titiwangsa_rent']:,.0f} | {t['parkview_balance']:+,.0f} | {t['titiwangsa_balance']:+,.0f} | {t['leader']} |")
lines+=['','This is a coverage comparison, not an overall product rank or probability forecast. Plan, current-tenancy and fee evidence can reverse research priority.','',
'## Correlated twelve-month capital path','',
'5.5%rate,20%rent reduction,20%fee increase, six collected months and30kworks in month1per property. One synthetic500kcash pool and150kprotected reserve; no salary, refinancing or sale rescue. All120unordered expression pairs are diagnostics, including held and alternative units; coexisting distinct parcels are not verified. R225/R329 must not be treated as two confirmed purchasable units, and shared development risk is not diversification.','',
'| Pair | Minimum cash | Reserve pass |','|---|---:|---|']
for ids in [('R321','R328'),('R329','R327'),('R323','R326'),('R322','KV11')]:
 t=next(t for t in pairs if set(t['ids'])==set(ids));lines.append(f"| {' + '.join(ids)} | {t['minimum_cash']:,.0f} | {'Yes, synthetic only' if t['reserve_pass'] else 'No'} |")
lines += ['',f"{sum(t['reserve_pass'] for t in pairs)} of120diagnostic pairs retain the synthetic reserve. No pair is an allocation recommendation. Shared employment, tenant budgets, credit, costs and vacancy shocks remain correlated; different postcodes do not prove diversification. No purchase preserves starting cash before unmodelled cash returns.",'',
'## Full scenario detail','',
'Combined stress uses12months, base60and delayed exit72. Compare terminal prices only at equivalent horizons. Standard monthly diagnostic remains90/4/35; scenario cashflow uses the actual stressed terms.','']
papers=['# B05 full G0-G9 workpapers','',
'Sixteen conditional expressions; cutoff7October2026. Frozen gate names and stops remain authoritative. Downstream diagnostics do not pass a stopped gate. Read B05_Evidence_and_Supply.md and B05_Divergence_and_Misses.md with these papers. Investor-led resale is eligible; owner adoption is not assumed.','']
for r in results:
 c=r['case'];b=r['scenarios']['base'];d=r['boundaries']
 lines += [f"### {c['id']} - {c['name']}",'','| Scenario / horizon | Entry cash | Year1 cashflow | Recovery sale | Minimum cash |','|---|---:|---:|---:|---:|']
 for n,v in r['scenarios'].items():lines.append(f"| {n} / {v['months']}m | {v['entry_cash']:,.0f} | {v['cashflow_by_year'][0]:+,.0f} | {v['terminal_nominal_breakeven']:,.0f} | {v['minimum_cash']:,.0f} |")
 lines.append('')
 papers += [f"## {c['id']} - {c['name']}",'',f"{c['area_id']}; {c['sqft']}sf; {c['layout']}. {c['evidence_dates']}.",'',f"Observed-source boundary: {c['source_note']}",'']
 if 'sale_source' in c:papers += [f"[Sale lead]({c['sale_source']}); [rent lead]({c['rent_source']}). Saved B05 retrievals: {', '.join(c['retrievals'])}.",'']
 else:papers += [f"Original numerical/source lineage: {'round1 Evidence_Register.md and Selected_Case_Workpapers.md' if c['id'].startswith('KV') else 'round2 cases/'+c['id']+'.md'}. Inherited source IDs belong to that release; new evidence is in B05_Evidence_and_Supply.md. No silent refresh.",'']
 gates=[
 ('G0 Reference-Price Validity','STOP. '+c['comp']+' No normalised effective clearing interval or undervaluation conclusion.'),
 ('G1 Market Mechanism',c['mechanism']+' Hypothesis only; no rent/capital uplift in base.'),
 ('G2 Buyer Universe',c['buyer']+' Actual willingness, financing ability and depth remain unmeasured.'),
 ('G3 Project Quality',c['project']+' Unknown is neither healthy nor failed.'),
 ('G4 Unit Quality',c['source_note']+' Exact approved plan, privacy/noise/light and irreversible externalities not inspected.'),
 ('G5 Price / Mispricing',f"Unadjudicated under G0. Standard price boundary {d['standard_price']:,.0f};6%gross boundary {d['gross6_price']:,.0f}; neither is fair value. "+c['reversal']),
 ('G6 Exit Architecture',c['buyer']+f" Five-year recovery requires {b['terminal_nominal_breakeven']:,.0f}; flat-exit total profit {b['profit_by_exit_multiple']['1']:+,.0f}. No proven ceiling/floor or transaction velocity. Adverse investor yields and household substitution tested; longer holding is capital exposure, not an exit."),
 ('G7 Financing / Terminal Risk',f"90/4/35standard. Actual title/lease/use, lender valuation and eligibility unresolved. Entry cash {b['entry_cash']:,.0f};annual conditional carry {b['cashflow_by_year'][0]:+,.0f}. Full debt, rate, term, valuation, costs, works and exit tests in B05_Financial_Underwriting.md."),
 ('G8 Portfolio / Opportunity Cost','Compare named alternatives and no purchase. Joint paths test correlated shocks without income/refinance rescue. Synthetic cash does not approve the user portfolio, nor prove distinct unit availability or diversification.'),
 ('G9 Capital Decision','Defer. '+c['hold']+'. '+('Current standard shortfall receives lowest investment-research priority; reopen on evidenced transition and funded carry.' if b['current_shortfall'] else 'Simplified monthly pass does not clear full cost, identity, reference price, evidence gaps or safety margin.'))]
 papers+=['| Gate | Finding |','|---|---|']+[f"| {g} | {v} |" for g,v in gates]+['',
 f"**Finance:** gross {b['gross_yield']:.2%}; standard monthly {b['standard_monthly_balance']:+,.0f}; annual carry {b['cashflow_by_year'][0]:+,.0f}; annual-neutral rent {d['annual_neutral_rent']:,.0f}.",'',
 '**Strongest counter-thesis / falsification:** '+c['reversal']+' If matched ordinary income cannot meet the burden at a feasible entry, or confirmed structural limitations prevent the relevant use, the investment mechanism fails. Missing evidence alone establishes neither outcome.','',
 '**Finite evidence / reopening:** '+c['next']+' Further generic listing counts cannot clear that condition.','',
 '**Validation status:** Pre-outcome research; no capital deployed, realised return or predictive hit. No new causal promotion or Core amendment.','']
lines+=['## Verification','',f"{checks}evaluations reconcile amortisation, principal, independent economic-cost recovery and discounted hurdle.120joint paths and a nine-cell ranking grid are separately verified in B05_Release_Audit.json. Arithmetic checks do not authenticate inputs.",'']
write('B05_Financial_Underwriting.md','\n'.join(lines))
write('B05_Cases_G0_G9.md','\n'.join(papers))
print(json.dumps(dict(cases=len(cases),checks=checks,pairs=len(pairs),pair_passes=sum(t['reserve_pass'] for t in pairs),rows=[dict(id=r['case']['id'],gross=round(r['scenarios']['base']['gross_yield']*100,2),standard=round(r['scenarios']['base']['standard_monthly_balance']),annual=round(r['scenarios']['base']['cashflow_by_year'][0]),recovery=round(r['scenarios']['base']['terminal_nominal_breakeven'])) for r in results],alternatives=[dict(id=t['id'],standard=round(t['result']['standard_monthly_balance']),annual=round(t['result']['cashflow_by_year'][0])) for t in alternatives]),indent=2))
