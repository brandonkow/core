"""Independent Cheras scenario workpaper; never imports or rewrites Phase 7."""
from pathlib import Path
import json, itertools, math

ROOT = Path(__file__).resolve().parent
# Price and area are advertised; all rents/costs are underwriting assumptions.
CASES = [
    ('C01','M Vertica',489000,850,2400,350,150,20000),
    ('C02','Shamelin Star',700000,1054,2600,400,150,25000),
    ('C03','EkoCheras duplex',520000,762,2300,350,150,15000),
    ('C04','Aster Type B',540000,810,2400,350,150,20000),
    ('C05','Maxim Residences',480000,1050,2400,350,150,25000),
    ('C06','Riana South',595000,947,2700,400,150,20000),
    ('C07','Green Residence',540000,1127,2000,400,150,25000),
    ('C08','Windows on the Park large',900000,2497,3500,850,200,45000),
    ('C09','Scot Pine',498000,1743,2200,450,200,40000),
]

def payment(loan, rate=.04, years=30):
    r=rate/12
    return loan*r/(1-(1+r)**(-years*12)) if r else loan/(years*12)

def balance(loan, rate=.04, years=30, months=60):
    r=rate/12
    return loan*(1+r)**months-payment(loan,rate,years)*((1+r)**months-1)/r

def model(row, price=None, ltv=.8, valuation_ratio=1, rate=.04, stress=.055,
          paid_months=11, rent_factor=1, levy=30000, zero_rent=False, hurdle=.08):
    cid,name,p,area,rent,fee,other,refurb=row
    p=p if price is None else price
    loan=ltv*min(p,p*valuation_ratio)
    entry=p-loan+.05*p+refurb
    operating=fee+other
    mort=payment(loan,rate)
    debt=balance(loan,rate)
    cf=paid_months*rent*rent_factor-12*(mort+operating)
    burn=12*(payment(loan,stress)+operating)-(0 if zero_rent else 6*.8*rent)+levy
    # Stress-year hold cannot be funded by assumed disposal proceeds.
    cash=500000-entry-burn
    exits={str(f): .97*p*f-debt+5*cf-entry for f in (.8,1,1.15)}
    annuity=sum(1/(1+hurdle)**t for t in range(1,6))
    target_exit=(debt+(entry-cf*annuity)*(1+hurdle)**5)/.97
    return dict(id=cid,name=name,price=p,area=area,rent_assumed=rent,
        fee_assumed=fee,other_assumed=other,refurb_assumed=refurb,loan=loan,
        entry_cash=entry,base_mortgage=mort,stress_mortgage=payment(loan,stress),
        gross_yield=12*rent/p,net_operating_yield=(paid_months*rent*rent_factor-12*operating)/p,
        annual_cashflow=cf,cash_neutral_rent=12*(mort+operating)/paid_months,
        year5_debt=debt,year5_nominal_breakeven=(entry-5*cf+debt)/.97,
        year5_8pct_exit=target_exit,year5_profit=exits,stress_burn=burn,
        remaining_cash=cash,reserve_pass=cash>=150000,
        debt_service_gross_income=(4000+payment(loan,stress))/20000,
        future_buyer_80_25_payment=payment(.8*((entry-5*cf+debt)/.97),.055,25),
        future_buyer_70_20_payment=payment(.7*((entry-5*cf+debt)/.97),.055,20))

def price_for_target(row, terminal, hurdle=.08):
    lo,hi=10000,2000000
    for _ in range(70):
        mid=(lo+hi)/2
        if model(row,price=mid,hurdle=hurdle)['year5_8pct_exit']>terminal: hi=mid
        else: lo=mid
    return (lo+hi)/2

def main():
    results=[]
    for row in CASES:
        r=model(row)
        r['sensitivities']={
            '70pct_ltv':model(row,ltv=.7),
            '90pct_ltv':model(row,ltv=.9),
            'valuation_15pct_lower':model(row,valuation_ratio=.85),
            'zero_rent_12m':model(row,zero_rent=True),
            'levy_50k':model(row,levy=50000),
            'persistent_5_5pct':model(row,rate=.055),
            'persistent_rent_down20':model(row,rent_factor=.8),
        }
        r['price_cap_if_exit_at_today_ask_8pct']=price_for_target(row,row[2])
        r['price_cap_if_exit_at_today_ask_zero_return']=price_for_target(row,row[2],0)
        results.append(r)
    pairs=[]
    for a,b in itertools.combinations(results,2):
        left=500000-a['entry_cash']-b['entry_cash']-a['stress_burn']-b['stress_burn']
        pairs.append(dict(ids=[a['id'],b['id']],remaining_cash=left,reserve_pass=left>=150000))
    out={'date':'2026-10-06','scope':'Scenario underwriting, not valuation or loan approval',
         'cases':results,'pairs':pairs}
    (ROOT/'Cheras_Financial_Results.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    lines=['# Cheras - Financial underwriting and capital stress','',
      'As of 6 October 2026. RM throughout. Source case IDs refer to Cheras_G0_G9_Cases.md.', '',
      '## Mandate and boundaries','',
      'Synthetic comparison mandate: RM500,000 cash including RM150,000 protected reserve; RM20,000 gross monthly household income and RM4,000 existing debt. These are not the user\'s declared finances. Base: 80% loan, 30 years, 4%; stress: 5.5%; five-year hold; 5% acquisition-cost allowance and 3% disposal-cost allowance. Allowances are not statutory fee or tax quotations. No appreciation is needed to calculate the flat-exit case. All sale prices are asks, not accepted offers.', '',
      'Every rent, service/sinking charge, other cost and refurbishment figure below is an analyst assumption, not an achieved tenancy, verified invoice or contractor quote. Other cost covers a rough allowance for repairs, insurance, assessment/quit rent and administration; letting commissions, turnover, tax and larger replacements can exceed it. These pre-tax figures exclude RPGT, income tax, loan lock-in charges and transaction-specific legal exceptions. The optional 8% equity hurdle is an illustrative decision test, not an approved user return requirement. The zero-return ceiling is not a margin of safety.', '',
      '## Inputs and base income','',
      '| ID | Ask | Area sf | Assumed rent/month | Fee + other/month | Refurbishment | Gross yield | Net operating yield | Base annual cashflow | Cash-neutral rent/month |',
      '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for r in results:
        lines.append(f"| {r['id']} {r['name']} | {r['price']:,.0f} | {r['area']} | {r['rent_assumed']:,.0f} | {r['fee_assumed']+r['other_assumed']:,.0f} | {r['refurb_assumed']:,.0f} | {r['gross_yield']:.1%} | {r['net_operating_yield']:.1%} | {r['annual_cashflow']:,.0f} | {r['cash_neutral_rent']:,.0f} |")
    lines+=['','Net operating yield uses 11 paid months less operating costs, before financing and entry costs. Base annual cashflow includes principal repayment: it is cashflow, not accounting profit. No room aggregation or short-stay income is used.', '',
      '## Exit burden and reverse underwriting','',
      '| ID | Entry cash | Nominal break-even sale in year 5 | Sale needed for 8% equity hurdle | Profit if resale -20% | Profit if resale flat | Profit if resale +15% |',
      '|---|---:|---:|---:|---:|---:|---:|']
    for r in results:
        lines.append(f"| {r['id']} | {r['entry_cash']:,.0f} | {r['year5_nominal_breakeven']:,.0f} | {r['year5_8pct_exit']:,.0f} | {r['year5_profit']['0.8']:,.0f} | {r['year5_profit']['1']:,.0f} | {r['year5_profit']['1.15']:,.0f} |")
    lines+=['','These are required exit prices, not predicted values, floors or proven ceilings. No matched clearing price is established. -20% is a scenario, not a worst-case bound. An unmarketable unit can do worse. +15% is an upside sensitivity, not a forecast.', '',
      '| ID | Maximum entry if year-5 resale equals today\'s ask, zero return | Same fixed terminal price, 8% hurdle | Future buyer payment: 80%/25y/5.5% at nominal break-even | Future buyer payment: 70%/20y/5.5% |',
      '|---|---:|---:|---:|---:|']
    for r in results:
        lines.append(f"| {r['id']} | {r['price_cap_if_exit_at_today_ask_zero_return']:,.0f} | {r['price_cap_if_exit_at_today_ask_8pct']:,.0f} | {r['future_buyer_80_25_payment']:,.0f} | {r['future_buyer_70_20_payment']:,.0f} |")
    lines+=['','Reverse caps hold the nominal terminal sale at the current selected ask while solving purchase price. They are model outputs, not executable offers, fair values or discounts to a validated price. Future buyers additionally need 20% or 30% equity plus costs; a lower loan amount does not establish greater buyer depth. Any tighter lender tenure/valuation or title problem changes the result.', '',
      '## One-year forced-hold stress','',
      'No sale during 12 months; six paid rental months at 80% of base rent, stress mortgage throughout, all annual operating costs and RM30,000 unexpected works. Reserve is checked at the stress-year end and must also be available through interim cash demands. Cash at entry includes acquisition/refurbishment. No household salary surplus, cash-out refinance or capital gain is assumed to rescue a breach.', '',
      '| ID | Stress burn | Cash remaining | Reserve pass | Zero-rent cash remaining | 15% lower valuation cash remaining | RM50k levy cash remaining | Gross-income debt-service proxy |',
      '|---|---:|---:|---|---:|---:|---:|---:|']
    for r in results:
        s=r['sensitivities']
        lines.append(f"| {r['id']} | {r['stress_burn']:,.0f} | {r['remaining_cash']:,.0f} | {'Yes' if r['reserve_pass'] else 'No'} | {s['zero_rent_12m']['remaining_cash']:,.0f} | {s['valuation_15pct_lower']['remaining_cash']:,.0f} | {s['levy_50k']['remaining_cash']:,.0f} | {r['debt_service_gross_income']:.1%} |")
    lines+=['','The debt-service ratio is a gross-income comparison only, not any bank\'s approval method. Valuation stress sizes the loan at 80% of 85% of price. It raises cash equity while reducing instalments. See JSON for 70% and 90% LTV cases; neither financing availability is asserted.', '',
      '## Persistent stress and portfolio','',
      '| ID | Nominal break-even at persistent 5.5% | Nominal break-even with rents 20% lower throughout |',
      '|---|---:|---:|']
    for r in results:
        lines.append(f"| {r['id']} | {r['sensitivities']['persistent_5_5pct']['year5_nominal_breakeven']:,.0f} | {r['sensitivities']['persistent_rent_down20']['year5_nominal_breakeven']:,.0f} |")
    passes=[p for p in pairs if p['reserve_pass']]
    lines+=['',f"All {len(pairs)} two-property pairs were tested with simultaneous stress and one common RM150k reserve. {len(passes)} pairs preserve it. This is not diversification just because two postcodes differ. Regional credit, commuter demand and investor resale behaviour can correlate; two student-exposed assets add operating concentration.", '',
      '## Reproducible formulas','',
      'Mortgage = L*r / [1-(1+r)^(-360)], r=annual rate/12. Year-5 balance uses 60 monthly payments. Entry = P-L+0.05P+refurbishment. Annual cashflow = 11*monthly rent - 12*(mortgage+fee+other). Stress burn = 12*(stress mortgage+fee+other) - 6*0.8*rent + levy. Nominal break-even exit = (entry - 5*annual cashflow + year-5 debt)/0.97. Flat-exit profit = 0.97P - year-5 debt + 5*annual cashflow - entry. The 8% exit solves NPV of entry, five end-year cashflows and net sale equity equal to zero.', '',
      'Validation: amortisation checked against monthly recurrence; terminal profit checked at calculated break-even; NPV checked at the 8% terminal price; reverse-price roots checked; single/pair reserve arithmetic checked. Rounding occurs only in this presentation.']
    (ROOT/'Cheras_Financial_Underwriting.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    for row,r in zip(CASES,results):
        b=r['loan']
        for _ in range(60): b=b*(1+.04/12)-r['base_mortgage']
        assert abs(b-r['year5_debt'])<.01
        assert abs(.97*r['year5_nominal_breakeven']-b+5*r['annual_cashflow']-r['entry_cash'])<.01
        npv=-r['entry_cash']+sum(r['annual_cashflow']/1.08**t for t in range(1,6))+(.97*r['year5_8pct_exit']-b)/1.08**5
        assert abs(npv)<.01
        assert abs(model(row,price=r['price_cap_if_exit_at_today_ask_8pct'])['year5_8pct_exit']-r['price'])<.01
    print(json.dumps({'cases':len(results),'pairs':len(pairs),'pair_passes':len(passes),'checks':'passed','brief':[{k:r[k] for k in ['id','annual_cashflow','year5_nominal_breakeven','year5_8pct_exit','remaining_cash','price_cap_if_exit_at_today_ask_8pct']} for r in results]},indent=2))

if __name__=='__main__': main()
