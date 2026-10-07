"""Programme scenarios reuse the frozen approved engine; no master/SOP mutation."""
from pathlib import Path
import importlib.util, json, itertools, hashlib
ROOT=Path(__file__).resolve().parent
ENGINE=ROOT.parent/'execution-release-2026-10-07'/'financial_engine.py'
spec=importlib.util.spec_from_file_location('approved_engine',ENGINE)
eng=importlib.util.module_from_spec(spec)
spec.loader.exec_module(eng)
cases=json.loads((ROOT/'Case_Inputs.json').read_text(encoding='utf-8'))['cases']
scenarios={
'rate_5_5pct':dict(rate=.055), 'rent_down20':dict(rent_factor=.8),
'fee_up20':dict(fee_factor=1.2),'zero_rent_first12':dict(initial_vacancy=12),
'works_30k_month24':dict(levy_month=24,levy=30000),
'bank_value_down15':dict(valuation_ratio=.85),'loan_term25':dict(term=25),
'exit_delay12':dict(months=72),'unquoted_cost_buffer':dict(annual_extra_cost=1200,exit_extra_cost=5000)}
base=[]; sensitivities=[]; stress=[]; grid=[]
factor=eng.payment(.9,.04,35)
def slim(r):
    return {k:v for k,v in r.items() if k not in ('schedule','cash_path')}
for c in cases:
    b=eng.evaluate(c); eng.check_financial_identities(b,c)
    b.update(batch=c['batch'],sqft=c['sqft'],layout=c['layout'],
      gross6_price=12*c['rent_assumed']/.06,
      standard_cover_price=(c['rent_assumed']-c['fee_assumed'])/factor,
      standard_required_rent=b['standard_instalment']+c['fee_assumed'],
      annual_carry_neutral_rent=12*(b['standard_instalment']+c['fee_assumed']+c['other_assumed'])/11,
      g9='Defer')
    base.append(b)
    for label,kw in scenarios.items():
        r=eng.evaluate(c,**kw); eng.check_financial_identities(r,c,kw.get('exit_extra_cost',0))
        if label not in ('bank_value_down15','loan_term25','exit_delay12'):
            assert r['terminal_nominal_breakeven']>b['terminal_nominal_breakeven']
        r['scenario']=label; sensitivities.append(slim(r))
    s=eng.evaluate(c,months=12,rate=.055,rent_factor=.8,first_year_paid=6,levy_month=1,levy=30000)
    eng.check_financial_identities(s,c); stress.append(s)
    for rent,fee_factor in itertools.product((c['rent_low'],c['rent_assumed'],c['rent_high']),(.8,1,1.2)):
        cc=dict(c,rent_assumed=rent)
        r=eng.evaluate(cc,fee_factor=fee_factor)
        # The unchanged engine keeps standard coverage at the input fee proxy.
        # For a fee-input rank test explicitly replace that input as well.
        cc['fee_assumed']=c['fee_assumed']*fee_factor
        r=eng.evaluate(cc); eng.check_financial_identities(r,cc)
        grid.append(dict(id=c['id'],rent=rent,fee=cc['fee_assumed'],
          standard_balance=r['standard_monthly_balance'],annual_cf=r['cashflow_by_year'][0],
          gross_yield=r['gross_yield']))
pairs=[]
for a,b in itertools.combinations(stress,2):
    path=[500000-a['entry_cash']-b['entry_cash']]
    for ma,mb in zip(a['schedule'],b['schedule']):
        path.append(path[-1]+ma['cashflow']+mb['cashflow'])
    pairs.append(dict(ids=[a['id'],b['id']],minimum_cash=min(path),reserve_pass=min(path)>=150000,cash_path=path))
assert len(cases)==14 and len({c['id'] for c in cases})==14
assert len(sensitivities)==126 and len(grid)==126 and len(pairs)==91
# Analytic boundaries must independently reproduce the stated financial condition.
for c,b in zip(cases,base):
    pp=dict(c,price=b['standard_cover_price'])
    assert abs(eng.evaluate(pp)['standard_monthly_balance'])<.01
    rr=dict(c,rent_assumed=b['annual_carry_neutral_rent'])
    assert abs(eng.evaluate(rr)['cashflow_by_year'][0])<.01
    assert abs(12*c['rent_assumed']/b['gross6_price']-.06)<1e-10
out=dict(version='KV-REG-2026-10-07-R1',config=eng.CFG,
 engine_sha256=hashlib.sha256(ENGINE.read_bytes()).hexdigest(),
 base=base,sensitivities=sensitivities,combined_stress=stress,pairs=pairs,rank_grid=grid,
 checks='passed: approved amortisation/economic identity/NPV, stress directions, boundary identities and coverage counts')
(ROOT/'Financial_Results.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
money=lambda v:f'{v:,.0f}'
lines=['# Cross-region financial diagnostics — round 1','',
'Cutoff: 7 October 2026. Fourteen selected marketed expressions, not executable offers or regional fair values. All results are conditional; every case remains G9 Defer. The existing approved engine and configuration are imported unchanged.','',
'## Assumptions and cost boundary','',
'90% of acquisition price, 4%, 35 years; five-year illustrative hold. Eleven collected months annually; no rent growth, catalyst premium, salary contribution or refinancing. Fee combines management and sinking provision as an unverified proxy. Actual management-only coverage is unverified. Other monthly costs and initial furnishing/refurbishment are analyst allowances, not invoices. Gross yield uses price, not all-in cost.','',
'Entry cash includes 10% equity, a 5% acquisition-cost allowance and the stated initial works. Disposal allowance is 3%. These are planning allowances, not tax/legal quotations. Results are pre-tax; transaction-specific duties, reliefs, tax status, loan costs, repairs and levies remain unresolved. A separate sensitivity adds RM1,200/year and RM5,000 at exit; this is not a tax estimate or worst-case bound. The 8% equity hurdle and RM500k/RM150k cash/reserve are inherited illustrations, not approved investor targets or user finances.','',
'## Price, rent and current coverage','',
'Amounts in RM. Standard balance = full monthly rent minus full instalment minus fee proxy. Annual carry includes one unpaid month and other costs; principal is counted once.','',
'| Case | Price | Monthly rent | Fee proxy | Other/month | Initial works | Gross yield | Standard balance/month | Annual carry |',
'|---|---:|---:|---:|---:|---:|---:|---:|---:|']
for c,b in zip(cases,base):
 lines.append(f"| {c['id']} {c['name']} {c['sqft']} sf | {money(c['price'])} | {money(c['rent_assumed'])} | {money(c['fee_assumed'])} | {money(c['other_assumed'])} | {money(c['refurb_assumed'])} | {b['gross_yield']:.2%} | {b['standard_monthly_balance']:+,.0f} | {b['cashflow_by_year'][0]:+,.0f} |")
lines+=['','An assumed standard surplus is not verified cashflow. A negative standard result places the expression at the lowest research priority; it is not a structural Reject. KV12 additionally has unresolved sale/rent labelling, so its positive arithmetic cannot establish an eligible investment expression.','',
'## Mechanical thresholds — not bids, valuations or forecasts','',
'The 6% price ceiling and coverage price ceiling hold assumed rent/fees fixed. Required rent measures the burden at the input price; it is not an achievable-rent forecast. No unknown price discount is validated by these formulas.','',
'| Case | Price at 6% gross | Price at standard coverage | Rent for standard coverage | Rent for annual carry neutrality |',
'|---|---:|---:|---:|---:|']
for b in base: lines.append(f"| {b['id']} | {money(b['gross6_price'])} | {money(b['standard_cover_price'])} | {money(b['standard_required_rent'])} | {money(b['annual_carry_neutral_rent'])} |")
lines+=['','## Entry, terminal burden and future buyer','',
'| Case | Entry cash | Year-5 debt | Nominal break-even sale | Sale for illustrative 8% | Flat-price total profit | 20%-lower exit total profit | Future buyer 90/4/35 payment at break-even |',
'|---|---:|---:|---:|---:|---:|---:|---:|']
for b in base: lines.append(f"| {b['id']} | {money(b['entry_cash'])} | {money(b['terminal_debt'])} | {money(b['terminal_nominal_breakeven'])} | {money(b['terminal_8pct_required'])} | {b['profit_by_exit_multiple']['1']:+,.0f} | {b['profit_by_exit_multiple']['0.8']:+,.0f} | {money(b['future_buyer_standard_payment_at_breakeven'])} |")
lines+=['','Required exits are cost-recovery/return hurdles, not supported exit values. None is used as G0 evidence. Buyer income, equity, loan acceptance and competing stock at that future budget remain to be proven.','',
'## Simultaneous forced-hold stress','',
'Rate 5.5%, rent down 20%, no collection for first six months, immediate RM30k levy per asset, no sale for twelve months. Loan stays 90%; the separately reported bank-value/term sensitivities do not change the standard.','',
'| Case | Minimum synthetic remaining cash | Protected RM150k reserve survives |',
'|---|---:|---|']
for s in stress: lines.append(f"| {s['id']} | {money(s['minimum_cash'])} | {'Yes, scenario only' if s['protected_reserve_pass'] else 'No'} |")
lines += ['',f"{sum(x['reserve_pass'] for x in pairs)} of {len(pairs)} two-case pairs preserve the synthetic reserve under this shock. This count does not establish diversification or capacity to buy. All are exposed to shared high-rise financing, strata works and tenant-income risks; location distance alone cannot establish low correlation.",'',
'## Full sensitivity register','',
'| Case | Scenario | Entry cash | Nominal break-even sale | Total carry | Flat-price total profit |',
'|---|---|---:|---:|---:|---:|']
for s in sensitivities: lines.append(f"| {s['id']} | {s['scenario']} | {money(s['entry_cash'])} | {money(s['terminal_nominal_breakeven'])} | {s['cashflow_total']:+,.0f} | {s['profit_by_exit_multiple']['1']:+,.0f} |")
lines+=['','The JSON contains monthly schedules, loan balances, stress cash paths and a 126-row rent/fee grid. Fee bands of plus/minus 20% and the stated rent endpoints are sensitivity choices, not statistical confidence intervals. The base-case fee remains unverified.','',
'## Verification','',out['checks'], '',
'No model output clears an unresolved gate. Original master, SOP, replay and historical case records are preserved.']
(ROOT/'Financial_Underwriting.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps(dict(cases=len(base),sensitivities=len(sensitivities),pairs=len(pairs),pair_pass=sum(x['reserve_pass'] for x in pairs),
 summaries=[dict(id=b['id'],std=round(b['standard_monthly_balance']),annual=round(b['cashflow_by_year'][0]),yield_pct=round(b['gross_yield']*100,2),breakeven=round(b['terminal_nominal_breakeven'])) for b in base]),indent=2))

