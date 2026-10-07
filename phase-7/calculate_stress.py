"""Reproducible Phase 7 scenarios. All financial inputs are assumptions, not offers."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
CASES = [
    dict(id='P7-01', name='Kiara Park high-rise', price=850000, rent=3200, fees=520, other=150, refurb=50000),
    dict(id='P7-02', name='Westside Three', price=1600000, rent=5500, fees=650, other=200, refurb=25000),
    dict(id='P7-03', name='Aster Residence', price=685000, rent=2800, fees=400, other=150, refurb=20000),
    dict(id='P7-04', name='M City residential', price=650000, rent=2700, fees=550, other=150, refurb=20000),
]

def payment(principal, rate, months=360):
    r = rate / 12
    return principal * r / (1 - (1 + r) ** -months)

def balance(principal, rate, months_paid=60, term=360):
    r = rate / 12
    return principal * (1+r)**months_paid - payment(principal, rate, term) * ((1+r)**months_paid-1)/r

def evaluate(c, ltv=.8, valuation_ratio=1, levy=30000):
    p, rent = c['price'], c['rent']
    loan = ltv * min(p, p * valuation_ratio)
    base, stress = payment(loan, .04), payment(loan, .055)
    opex = c['fees'] + c['other']
    entry = p-loan + .05*p + c['refurb']
    burn = 12*(stress+opex) - 6*.8*rent + levy
    no_rent_burn = 12*(stress+opex) + levy
    cashflow = 11*rent - 12*(base+opex)
    terminal_debt = balance(loan, .04)
    break_even = (entry - 5*cashflow + terminal_debt)/.97
    profits = {label: .97*p*multiple-terminal_debt + 5*cashflow-entry
               for label, multiple in [('exit_minus20pct', .8), ('exit_flat', 1), ('exit_plus15pct', 1.15)]}
    cash_remaining = 500000-entry-burn
    return dict(**c, ltv=ltv, valuation_ratio=valuation_ratio, levy=levy,
                loan=loan, monthly_base=base, monthly_stress=stress,
                entry_cash=entry, gross_yield=12*rent/p,
                annual_base_cashflow=cashflow, annual_stress_burn=burn,
                zero_rent_stress_burn=no_rent_burn,
                cash_after_entry_and_stress=cash_remaining,
                protected_reserve_pass=cash_remaining>=150000,
                proxy_dsr_base=(4000+base)/20000,
                proxy_dsr_stress=(4000+stress)/20000,
                five_year_debt=terminal_debt,
                five_year_nominal_break_even=break_even,
                break_even_growth_pa=(break_even/p)**.2-1,
                future_buyer_monthly_25yr_stress=payment(.8*p,.055,300),
                future_buyer_income_at_35pct=payment(.8*p,.055,300)/.35,
                **profits)

rows = [evaluate(c) for c in CASES]
sens = [evaluate(c, **s) for c in CASES for s in [dict(ltv=.7),dict(ltv=.9),dict(valuation_ratio=.85),dict(levy=50000)]]
portfolio = []
for i,a in enumerate(rows):
    for b in rows[i+1:]:
        entry = a['entry_cash']+b['entry_cash']
        burn = a['annual_stress_burn']+b['annual_stress_burn']
        remaining=500000-entry-burn
        portfolio.append(dict(pair=[a['id'], b['id']],entry_cash=entry,stress_burn=burn,
                              remaining_cash=remaining, reserve_pass=remaining>=150000,
                              stress_proxy_dsr=(4000+a['monthly_stress']+b['monthly_stress'])/20000))

# Independent arithmetic checks: amortisation schedule, accounting identity, shock direction.
for c in rows:
    debt=c['loan']; interest=0
    for _ in range(60):
        interest += debt*.04/12
        debt += debt*.04/12-c['monthly_base']
    assert abs(debt-c['five_year_debt'])<.01
    identity=(c['price']*1.05+c['refurb']+interest+60*(c['fees']+c['other'])-55*c['rent'])/.97
    assert abs(identity-c['five_year_nominal_break_even'])<.01
    assert c['monthly_stress']>c['monthly_base']
    assert c['zero_rent_stress_burn']>c['annual_stress_burn']

data=dict(as_of='2026-10-06', timezone='Asia/Kuala_Lumpur', currency='MYR',
          status='synthetic scenarios; not personal underwriting or market valuation',
          base=rows,sensitivities=sens,pairs=portfolio)
(OUT/'Phase_7_Stress_Results.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
def money(v): return f'{v:,.0f}'
lines=['# Phase 7 — Capital and terminal-risk scenarios', '',
       'As of 6 October 2026. These are reproducible conditional scenarios, not approved loans, achieved rents, valuations, or user finances.', '',
       '## Inputs and boundaries', '',
       'Synthetic household: RM500,000 cash including a protected RM150,000 reserve; RM20,000 monthly gross income; RM4,000 existing monthly debt. Thus RM350,000 is available for entry plus the new asset stress buffer. Existing debt is included in the debt-service proxy, but the existing portfolio itself is unknown. Protected reserves have no verified adequacy for household living expenses or existing assets.', '',
       '80% LTV; 30 years; 4.0% base / 5.5% stressed rate. Five-year hold. Entry allowance is 5% of price plus refurbishment, on top of the down payment. Disposal allowance is 3%. These are broad transaction-cost allowances, not statutory tax/fee quotations. Income tax, disposal tax, loan lock-in penalties and opportunity cost of equity are excluded from the numerical profit; they can only reduce the displayed result. Tax residency, disposal anniversary and actual quotes must be resolved before deployment.', '',
       '| Case | Price input | Monthly rent input | Fees / other monthly | Refurbishment |',
       '|---|---:|---:|---:|---:|']
for c in rows:
    lines.append(f"| {c['name']} | {money(c['price'])} | {money(c['rent'])} | {money(c['fees'])} / {money(c['other'])} | {money(c['refurb'])} |")
lines += ['', 'Prices are the selected seller asks, not agreed prices. Rent inputs are research-informed scenarios; no achieved tenancy was verified. Kiara fee is an agent claim; the other fees and all other-cost/refurbishment allowances are assumptions. Fee allowances intend to cover service charge and sinking contribution, but actual statements are missing. Other monthly costs bundle insurance, assessment/quit rent and routine replacements; they are not quotes.', '',
          '## Individual capital and forced-hold test', '',
          'Stress combines the +1.5 percentage-point rate shock, rent down 20%, six rent-free months, twelve months without selling, and a RM30,000 levy. No annual income from the existing portfolio is assumed to offset it. Cash remaining shown below is after entry AND this stress, keeping the protected reserve separate.', '',
          '| Case | Entry cash | Mortgage base / stress per month | Gross-income debt proxy base / stress | 12-month stress burn | Cash remaining | Reserve pass |',
          '|---|---:|---:|---:|---:|---:|---|']
for c in rows:
    lines.append(f"| {c['name']} | {money(c['entry_cash'])} | {money(c['monthly_base'])} / {money(c['monthly_stress'])} | {c['proxy_dsr_base']:.1%} / {c['proxy_dsr_stress']:.1%} | {money(c['annual_stress_burn'])} | {money(c['cash_after_entry_and_stress'])} | {'Yes' if c['protected_reserve_pass'] else 'No'} |")
lines += ['', 'This proxy is not lender DSR: banks use their own recognised income, deductions and credit rules. Passing the synthetic cash test does not pass G0, G3, G4, title, loan approval, or actual portfolio suitability.', '',
          '## Five-year return hurdle, without assumed appreciation', '',
          'Base collection is eleven months each year, with no rent growth; scheduled principal amortisation is included once. The table shows nominal pre-tax equity profit after five years, including operating carry, financing, refurbishment and the stated transaction allowances. No resale forecast is asserted.', '',
          '| Case | Annual base cash flow | Break-even sale | Annual price growth to break even | Profit if exit -20% | Flat exit | Exit +15% |',
          '|---|---:|---:|---:|---:|---:|---:|']
for c in rows:
    lines.append(f"| {c['name']} | {money(c['annual_base_cashflow'])} | {money(c['five_year_nominal_break_even'])} | {c['break_even_growth_pa']:.1%} | {money(c['exit_minus20pct'])} | {money(c['exit_flat'])} | {money(c['exit_plus15pct'])} |")
lines += ['', 'The five-year base model and the one-year forced-hold shock are separate scenarios, not added together. Loss of a tenant, lower achieved rent, higher tax/levy or another year to sell worsens break-even. A sale equal to purchase price is not capital preservation after all costs.', '',
          '## Sensitivities', '',
          '| Case | Change from base | Entry cash | Stress burn | Cash remaining | Reserve pass |',
          '|---|---|---:|---:|---:|---|']
for c in sens:
    label= '70% LTV' if c['ltv']==.7 else '90% LTV' if c['ltv']==.9 else 'Bank valuation -15%' if c['valuation_ratio']==.85 else 'RM50,000 levy'
    lines.append(f"| {c['name']} | {label} | {money(c['entry_cash'])} | {money(c['annual_stress_burn'])} | {money(c['cash_after_entry_and_stress'])} | {'Yes' if c['protected_reserve_pass'] else 'No'} |")
lines += ['', '90% LTV is only a sensitivity, not assumed eligibility. With an 80% loan against a valuation 15% below price, effective loan/price falls to 68%. A lower monthly instalment can therefore coexist with a failed cash gate.', '',
          '## Joint stress: postcode diversification does not create cash capacity', '',
          '| Pair | Combined entry | Combined stress burn | Remaining cash | Reserve pass | Stress debt proxy |',
          '|---|---:|---:|---:|---|---:|']
for p in portfolio:
    lines.append(f"| {' + '.join(p['pair'])} | {money(p['entry_cash'])} | {money(p['stress_burn'])} | {money(p['remaining_cash'])} | {'Yes' if p['reserve_pass'] else 'No'} | {p['stress_proxy_dsr']:.1%} |")
lines += ['', 'Simultaneous rate/rent stress is applied to both acquisitions, with one material levy on each. No assumed correlation coefficient is used. All pairs fail this constrained cash mandate; buying two lower-ticket units does not solve allocation. Existing asset correlation remains unknown.', '',
          '## Marginal buyer and terminal financeability', '',
          '| Case at unchanged price | Future buyer 80% loan, 25 years, 5.5% monthly payment | Gross income if payment capped at illustrative 35% |',
          '|---|---:|---:|']
for c in rows:
    lines.append(f"| {c['name']} | {money(c['future_buyer_monthly_25yr_stress'])} | {money(c['future_buyer_income_at_35pct'])} |")
lines += ['', 'The 35% ratio is a behavioural affordability scenario, not a lending rule; other debt and living costs make requirements higher. At an exit price 20% higher, these payments and income amounts also rise 20%. No remaining lease is calculated from completion age. Aster title expiry and all unit-specific lending terms remain unverified.', '',
          '## Calculation definitions', '',
          'Monthly payment = L r / [1 − (1+r)^(-n)], where r is annual rate / 12 and n = 360. Entry cash = price − loan + 5% price + refurbishment. Stress burn = 12(stressed payment + monthly costs) − 6(80% rent) + levy. Break-even sale = (entry cash − five-year cash flow + remaining debt) / 0.97. All calculations retain full precision internally; displayed RM values are rounded.', '',
          'Validation: each terminal loan balance independently reconciled to a 60-month amortisation schedule; break-even reconciled to purchase plus interest and operating costs less rent. No principal double-counting. See Phase_7_Stress_Results.json for full inputs and results.']
(OUT/'Phase_7_Portfolio_Stress.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps([{k:r[k] for k in ['name','entry_cash','monthly_base','monthly_stress','annual_stress_burn','cash_after_entry_and_stress','five_year_nominal_break_even','exit_flat']} for r in rows],indent=2))
