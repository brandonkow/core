"""Batch 02 conditional calculations. Never imports/reruns the frozen Batch 01 script."""
import json
from itertools import combinations
from pathlib import Path

OUT = Path(__file__).resolve().parent
CASES = [
    dict(id='K1', name='Kiara original one bay', price=850000, rent=3200, fees=520, other=150, refurb=50000, liabilities=0),
    dict(id='A1', name='Aster original C', price=685000, rent=2800, fees=400, other=150, refurb=20000, liabilities=0),
    dict(id='S1', name='Sterling two bays', price=608000, rent=2500, fees=350, other=150, refurb=40000, liabilities=0),
    dict(id='V1', name='Venice Hill Tower 10', price=280000, rent=1400, fees=350, other=150, refurb=40000, liabilities=0),
    dict(id='K2', name='Kiara two-bay high-floor ask', price=1350000, rent=3500, fees=520, other=150, refurb=50000, liabilities=0),
    dict(id='KA', name='Kiara past auction plus liability scenario', price=558000, rent=3200, fees=520, other=150, refurb=50000, liabilities=200000),
    dict(id='A2', name='Aster C low-floor west-facing ask', price=650000, rent=2800, fees=400, other=150, refurb=20000, liabilities=0),
    dict(id='AB', name='Aster B 810 sf ask', price=540000, rent=2400, fees=350, other=150, refurb=20000, liabilities=0),
    dict(id='AD', name='Aster duplex asking scenario', price=750000, rent=2800, fees=450, other=150, refurb=20000, liabilities=0),
]

def payment(loan, rate, months=360):
    r=rate/12
    return loan*r/(1-(1+r)**-months)

def evaluate(c, ltv=.8, valuation_ratio=1, levy=30000):
    p=c['price']; loan=ltv*p*min(1,valuation_ratio)
    base=payment(loan,.04); stress=payment(loan,.055)
    costs=c['fees']+c['other']; entry=p-loan+.05*p+c['refurb']+c['liabilities']
    burn=12*(stress+costs)-4.8*c['rent']+levy
    cf=11*c['rent']-12*(base+costs)
    debt=loan; interest=0
    for _ in range(60):
        interest+=debt*.04/12
        debt+=debt*.04/12-base
    analytic=loan*(1+.04/12)**60-base*((1+.04/12)**60-1)/(.04/12)
    assert abs(debt-analytic)<.01
    be=(entry-5*cf+debt)/.97
    assert abs(be-(1.05*p+c['refurb']+c['liabilities']+interest+60*costs-55*c['rent'])/.97)<.01
    # This ceiling passes ONLY the synthetic cash gate; it is not fair value or a buy target.
    coefficient=1-ltv*min(1,valuation_ratio)+.05+12*payment(ltv*min(1,valuation_ratio),.055)
    cash_ceiling=(350000-c['refurb']-c['liabilities']-12*costs+4.8*c['rent']-levy)/coefficient
    return dict(**c,ltv=ltv,valuation_ratio=valuation_ratio,levy=levy,loan=loan,
        monthly_base=base,monthly_stress=stress,entry_cash=entry,stress_burn=burn,
        cash_remaining=500000-entry-burn,reserve_pass=500000-entry-burn>=150000,
        cash_only_price_ceiling=cash_ceiling,annual_cashflow=cf,
        cashflow_neutral_monthly_rent=12*(base+costs)/11,
        nominal_break_even_exit=be,break_even_growth=(be/p)**.2-1,
        flat_exit_profit=.97*p-debt+5*cf-entry,
        downside20_profit=.97*.8*p-debt+5*cf-entry,
        upside15_profit=.97*1.15*p-debt+5*cf-entry,
        zero_rent_stress=12*(stress+costs)+levy,
        gross_yield=12*c['rent']/p,
        stressed_debt_proxy=(4000+stress)/20000,
        future_payment_25yr=payment(.8*p,.055,300),
        future_payment_20yr=payment(.7*p,.055,240),future_equity_70pct=.3*p)

base=[evaluate(c) for c in CASES]
sens=[evaluate(c,**s) for c in CASES for s in [dict(ltv=.7),dict(ltv=.9),dict(valuation_ratio=.85),dict(levy=50000)]]
pairs=[]
for a,b in combinations(base[:4],2):
    rem=500000-a['entry_cash']-b['entry_cash']-a['stress_burn']-b['stress_burn']
    pairs.append(dict(ids=[a['id'],b['id']],cash_remaining=rem,reserve_pass=rem>=150000,stressed_debt_proxy=(4000+a['monthly_stress']+b['monthly_stress'])/20000))
ka=base[5]
liability_capacity=ka['cash_remaining']-150000+ka['liabilities']
data=dict(as_of='2026-10-06',status='Conditional scenarios; no verified achieved rents, title, loan approval or fair values',base=base,sensitivities=sens,pairs=pairs,kiara_auction_max_liability_cash_gate=liability_capacity)
(OUT/'Phase_7_Batch_02_Stress_Results.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
money=lambda v:f'{v:,.0f}'
lines=['# Phase 7 Batch 02 - Financial and switching tests','','As of 6 October 2026. Currency MYR. All results are conditional scenarios, not personal financial advice, bank quotes or valuations. No investment return target was supplied; nominal break-even is a diagnostic, not an adequate investment hurdle.','','## Locked mandate and inputs','','RM500,000 cash including RM150,000 protected reserve; RM20,000 gross monthly household income; RM4,000 existing debt. 80% LTV, 30 years, 4% base and 5.5% stress. Five-year hold; no rent growth; eleven rent-paying months per base year. Entry costs 5% of price plus refurbishment; exit costs 3%. Generic allowances, not statutory quotations. Income/disposal tax, loan lock-in costs, equity opportunity cost and household expenses are excluded. Household reserve adequacy is unverified.','','| ID | Expression | Price | Rent/month | Fees / other per month | Refurb | Extra liabilities |','|---|---|---:|---:|---:|---:|---:|']
for c in base:lines.append(f"| {c['id']} | {c['name']} | {money(c['price'])} | {money(c['rent'])} | {money(c['fees'])} / {money(c['other'])} | {money(c['refurb'])} | {money(c['liabilities'])} |")
lines+=['','K1/A1 retain Batch 01 inputs. K2/KA are comparisons, not substitutes silently replacing K1. KA is a PAST reserve plus a RM200,000 liability assumption drawn from an unverified agent warning of RM200,000-plus; actual debt allocation and auction outcome remain unknown. That liability is extra to generic transaction costs and the future levy. A2 is a separate advertisement, not a proven price reduction of A1. AD uses a dated asking example, not an available verified unit. Source IDs and dates are in the evidence log.','','S1 rent RM2,500 is assumed between imperfect one-bay partial/full and three-bay furnished asking comparators; no automatic parking premium. S1 RM350 fees replaces the stale RM0.18 psf advertising claim with an allowance, informed by a different-unit RM344 claim. V1 RM1,400 rent is assumed below a larger ground-floor Tower 10 ask of RM1,600; it is not a matched rent. A2 uses A1 rent unchanged to isolate price. AB/AD rents and all refurb/other allowances are assumptions. Fees intend to include sinking contributions; actual invoices are absent.','','## Capital survival','','Stress: +1.5 percentage-point rate, rent -20%, six months vacancy, twelve months unable to sell and RM30,000 levy simultaneously. The separate zero-rent sensitivity gives no rent for twelve months.','','| ID | Entry cash | Mortgage base / stress | Stress burn | Cash left | RM150k reserve | Cash-only price ceiling |','|---|---:|---:|---:|---:|---|---:|']
for c in base:lines.append(f"| {c['id']} | {money(c['entry_cash'])} | {money(c['monthly_base'])} / {money(c['monthly_stress'])} | {money(c['stress_burn'])} | {money(c['cash_remaining'])} | {'Pass' if c['reserve_pass'] else 'Fail'} | {money(c['cash_only_price_ceiling'])} |")
lines+=['','A cash-only price ceiling is the solution of entry cash + stress burn = RM350,000 with all other inputs fixed. It is never an entry recommendation or market-value ceiling. Unknown title, management, permanent externalities or valuation can stop a purchase far below it.','','## Return and rent hurdles','','| ID | Annual base cash flow | Neutral monthly rent | Five-year break-even sale | Required annual price growth | Profit: exit -20% / flat / +15% |','|---|---:|---:|---:|---:|---:|']
for c in base:lines.append(f"| {c['id']} | {money(c['annual_cashflow'])} | {money(c['cashflow_neutral_monthly_rent'])} | {money(c['nominal_break_even_exit'])} | {c['break_even_growth']:.1%} | {money(c['downside20_profit'])} / {money(c['flat_exit_profit'])} / {money(c['upside15_profit'])} |")
lines+=['','No exit price is forecast. These amounts distinguish capital survival from return sufficiency. KA losses include the assumed inherited liability; its growth hurdle is relative to the reserve, which is not total acquisition basis. The one-year shock and five-year base return are separate scenarios, not double-counted.','','## Financing and levy sensitivity','','| ID | Scenario | Entry cash | Cash after shock | Reserve |','|---|---|---:|---:|---|']
for c in sens:
    label='70% LTV' if c['ltv']==.7 else '90% LTV' if c['ltv']==.9 else 'Valuation -15%' if c['valuation_ratio']==.85 else 'RM50k levy'
    lines.append(f"| {c['id']} | {label} | {money(c['entry_cash'])} | {money(c['cash_remaining'])} | {'Pass' if c['reserve_pass'] else 'Fail'} |")
lines+=['','## Portfolio pairs: original expressions plus two new candidates','','| Pair | Cash after both entries and shocks | Reserve | Gross-income stress debt proxy |','|---|---:|---|---:|']
for p in pairs:lines.append(f"| {' + '.join(p['ids'])} | {money(p['cash_remaining'])} | {'Pass' if p['reserve_pass'] else 'Fail'} | {p['stressed_debt_proxy']:.1%} |")
lines+=['','A pair passing this cash calculation is not portfolio approval. Cross-market assets share credit/rent risks; two Cheras assets additionally share corridor exposure. Existing assets and liabilities beyond the synthetic debt input are unknown. No correlation coefficient is fabricated.','','## Marginal future buyer','','No remaining lease is inferred from completion dates. Sterling and Aster require title expiry and lender terms. The following are sensitivity assumptions for ALL cases, not predictions that lenders will impose them.','','| ID | 80% LTV / 25 yr / 5.5% payment | 70% LTV / 20 yr / 5.5% payment | Down payment at 70%, before costs | Zero-rent annual shock |','|---|---:|---:|---:|---:|']
for c in base:lines.append(f"| {c['id']} | {money(c['future_payment_25yr'])} | {money(c['future_payment_20yr'])} | {money(c['future_equity_70pct'])} | {money(c['zero_rent_stress'])} |")
lines+=['','## Explicit switching arithmetic','',f"At the RM558,000 past reserve, KA can absorb at most RM{money(liability_capacity)} of extra cash-paid liabilities before violating the reserve under this stress. This is a scenario threshold, not a legal debt determination.",'',f"A1 versus AB: the RM145,000 price difference adds RM{money(payment(.8*145000,.04))} monthly mortgage, plus the assumed RM50 fee difference. A2 versus AB adds RM{money(payment(.8*110000,.04))} mortgage plus RM50. The household must value the extra usable space/balcony/bathroom enough to support this premium; that willingness-to-pay is not proven by the floor plan.",'',f"S1 versus the RM533,000 conflicting-body Kelana Mahkota ask: RM75,000 adds RM{money(payment(.8*75000,.04))} monthly mortgage before fee/condition differences. If the RM513,000 header is correct, the gap is RM95,000 and RM{money(payment(.8*95000,.04))}. Verify actual price and bay geometry before selecting the better deal.",'','Validation: all nine five-year loan balances reconcile to analytic amortisation and all break-even values to a separate purchase/interest/cost/rent identity. Nine base cases, 36 one-factor sensitivities and six joint cases. The model preserves Batch 01 files.']
(OUT/'Phase_7_Batch_02_Financial_Tests.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps([dict(id=c['id'],cash=round(c['cash_remaining']),break_even=round(c['nominal_break_even_exit']),flat=round(c['flat_exit_profit']),cash_ceiling=round(c['cash_only_price_ceiling'])) for c in base],indent=2))
print('pairs',pairs,'auction_liability_limit',liability_capacity)
