"""Versioned scenario arithmetic, not an autonomous valuation or decision service."""
from pathlib import Path
import json
import itertools

ROOT = Path(__file__).resolve().parent
CFG = json.loads((ROOT / 'financial_config.json').read_text(encoding='utf-8'))


def payment(loan, rate, years):
    if not 0 <= rate or years <= 0 or loan < 0:
        raise ValueError('Invalid loan inputs')
    r = rate / 12
    return loan / (years * 12) if r == 0 else loan * r / (1 - (1 + r) ** (-years * 12))


def evaluate(case, months=None, rate=None, term=None, valuation_ratio=1,
             rent_factor=1, fee_factor=1, initial_vacancy=0,
             first_year_paid=None, levy_month=None, levy=0,
             annual_extra_cost=0, exit_extra_cost=0):
    p = case['price']
    rent, fee, other = case['rent_assumed'], case['fee_assumed'], case['other_assumed']
    if p <= 0 or rent < 0 or fee < 0 or other < 0 or not 0 < valuation_ratio <= 1:
        raise ValueError('Invalid property/valuation inputs')
    rate = CFG['standard_rate'] if rate is None else rate
    term = CFG['standard_term_years'] if term is None else term
    months = 12 * CFG['illustrative_hold_years'] if months is None else months
    first_year_paid = CFG['baseline_paid_months_per_year'] if first_year_paid is None else first_year_paid
    if months <= 0 or months > term * 12 or not 0 <= first_year_paid <= 12:
        raise ValueError('Invalid time/collection inputs')
    standard_loan = CFG['standard_ltv'] * p
    loan = standard_loan * valuation_ratio
    standard_payment = payment(standard_loan, CFG['standard_rate'], CFG['standard_term_years'])
    actual_payment = payment(loan, rate, term)
    entry = p - loan + CFG['acquisition_cost_allowance'] * p + case['refurb_assumed']
    debt = loan
    schedule = []
    for month in range(1, months + 1):
        interest = debt * rate / 12
        principal = actual_payment - interest
        debt -= principal
        if month <= initial_vacancy:
            paid = False
        elif month <= 12:
            paid = month > 12 - first_year_paid
        else:
            paid = (month - 1) % 12 + 1 > 12 - CFG['baseline_paid_months_per_year']
        collected = rent * rent_factor if paid else 0
        operating = fee * fee_factor + other + annual_extra_cost / 12
        works = levy if month == levy_month else 0
        cf = collected - actual_payment - operating - works
        schedule.append(dict(month=month, rent=collected, interest=interest,
                             principal=principal, debt=debt, operating=operating,
                             works=works, cashflow=cf))
    cashflows = [x['cashflow'] for x in schedule]
    cash_sum = sum(cashflows)
    retention = 1 - CFG['disposal_cost_allowance']
    break_even = (entry - cash_sum + debt + exit_extra_cost) / retention
    hurdle = CFG['illustrative_equity_hurdle']
    pv_carry = sum(v / (1 + hurdle) ** ((i + 1) / 12) for i, v in enumerate(cashflows))
    required_exit = (debt + exit_extra_cost + (entry - pv_carry) *
                     (1 + hurdle) ** (months / 12)) / retention
    cash_path = [CFG['synthetic_cash'] - entry]
    for v in cashflows:
        cash_path.append(cash_path[-1] + v)
    standard_balance = rent - standard_payment - fee
    return dict(id=case['id'], name=case['name'], price=p, months=months,
                actual_rate=rate, actual_term_years=term, valuation_ratio=valuation_ratio,
                rent_assumed=rent, fee_proxy=fee, other_cost_allowance=other,
                gross_yield=12 * rent / p, standard_loan=standard_loan,
                standard_instalment=standard_payment, standard_monthly_balance=standard_balance,
                current_shortfall=standard_balance < 0, actual_loan=loan,
                actual_instalment=actual_payment, entry_cash=entry,
                cashflow_by_year=[sum(cashflows[i:i + 12]) for i in range(0, months, 12)],
                cashflow_total=cash_sum, terminal_debt=debt,
                terminal_nominal_breakeven=break_even, terminal_8pct_required=required_exit,
                profit_by_exit_multiple={str(v): retention * p * v - exit_extra_cost - debt + cash_sum - entry
                                         for v in (.8, 1, 1.15)},
                cash_path=cash_path, minimum_cash=min(cash_path), remaining_cash=cash_path[-1],
                protected_reserve_pass=min(cash_path) >= CFG['synthetic_protected_reserve'],
                future_buyer_standard_payment_at_breakeven=payment(
                    CFG['standard_ltv'] * break_even, CFG['standard_rate'], CFG['standard_term_years']),
                future_buyer_stress_payment_at_breakeven=payment(.8 * break_even, CFG['stress_rate'], 25),
                schedule=schedule)


def check_financial_identities(result, case, exit_extra_cost=0):
    s = result['schedule']
    loan = result['actual_loan']; rate = result['actual_rate'] / 12
    n = len(s); term = result['actual_term_years'] * 12
    if rate:
        closed_balance = loan * (1 + rate) ** n - result['actual_instalment'] * ((1 + rate) ** n - 1) / rate
    else:
        closed_balance = loan * (1 - n / term)
    assert abs(closed_balance - result['terminal_debt']) < .01
    assert abs(sum(x['principal'] for x in s) + result['terminal_debt'] - loan) < .01
    retention = 1 - CFG['disposal_cost_allowance']
    break_even = result['terminal_nominal_breakeven']
    profit = retention * break_even - exit_extra_cost - result['terminal_debt'] + result['cashflow_total'] - result['entry_cash']
    assert abs(profit) < .01
    # Independent unlevered cost + interest identity avoids counting principal twice.
    economic_basis = case['price'] * (1 + CFG['acquisition_cost_allowance']) + case['refurb_assumed']
    economic_basis += sum(x['interest'] + x['operating'] + x['works'] - x['rent'] for x in s) + exit_extra_cost
    assert abs(economic_basis / retention - break_even) < .01
    hurdle = CFG['illustrative_equity_hurdle']
    npv = -result['entry_cash'] + sum(x['cashflow'] / (1 + hurdle) ** (x['month'] / 12) for x in s)
    npv += (retention * result['terminal_8pct_required'] - exit_extra_cost - result['terminal_debt']) / (1 + hurdle) ** (n / 12)
    assert abs(npv) < .01


def main():
    source = ROOT.parent / 'cheras' / 'Cheras_Financial_Results.json'
    cases = json.loads(source.read_text())['cases']
    base = [evaluate(c, months=12 * CFG['illustrative_hold_years']) for c in cases]
    scenarios = {
        'rate_5_5pct': dict(rate=CFG['stress_rate']),
        'rent_down20': dict(rent_factor=.8),
        'fee_up20': dict(fee_factor=1.2),
        'zero_rent_first12': dict(initial_vacancy=12),
        'works_30k_month24': dict(levy_month=24, levy=30000),
        'bank_valuation_down15': dict(valuation_ratio=.85),
        'actual_loan_term25': dict(term=25),
        'exit_delay12': dict(months=72),
        'illustrative_unquoted_cost_buffer': dict(annual_extra_cost=1200, exit_extra_cost=5000),
    }
    sensitivity = []
    stress = []
    for c, b in zip(cases, base):
        check_financial_identities(b, c)
        for name, inputs in scenarios.items():
            row = evaluate(c, **inputs)
            check_financial_identities(row, c, inputs.get('exit_extra_cost', 0))
            row['scenario'] = name
            if name not in ('bank_valuation_down15', 'actual_loan_term25', 'exit_delay12'):
                assert row['terminal_nominal_breakeven'] > b['terminal_nominal_breakeven']
            sensitivity.append(row)
        shock = evaluate(c, months=12, rate=CFG['stress_rate'], rent_factor=CFG['stress_rent_factor'],
                         first_year_paid=CFG['stress_paid_months_first_year'], levy_month=1,
                         levy=CFG['stress_works'])
        check_financial_identities(shock, c)
        stress.append(shock)
    pairs = []
    for a, b in itertools.combinations(stress, 2):
        path = [CFG['synthetic_cash'] - a['entry_cash'] - b['entry_cash']]
        for ma, mb in zip(a['schedule'], b['schedule']):
            path.append(path[-1] + ma['cashflow'] + mb['cashflow'])
        pairs.append(dict(ids=[a['id'], b['id']], cash_path=path, minimum_cash=min(path),
                          reserve_pass=min(path) >= CFG['synthetic_protected_reserve']))
    rank_grid = []
    for r1, r5 in itertools.product((2200, 2400, 2600), repeat=2):
        c1 = dict(cases[0], rent_assumed=r1); c5 = dict(cases[4], rent_assumed=r5)
        a, b = evaluate(c1), evaluate(c5)
        rank_grid.append(dict(mvertica_rent=r1, maxim_rent=r5,
                             coverage_leader='C01' if a['standard_monthly_balance'] > b['standard_monthly_balance'] else 'C05',
                             mvertica_coverage=a['standard_monthly_balance'], maxim_coverage=b['standard_monthly_balance']))
    assert set(x['coverage_leader'] for x in rank_grid) == {'C01', 'C05'}
    output = dict(config=CFG, evidence_cutoff='2026-10-06; original assumed inputs only',
                  base=base, sensitivities=sensitivity, combined_stress=stress, pairs=pairs,
                  rank_grid=rank_grid, checks='passed')
    (ROOT / 'Financial_Results.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    write_report(output)
    print(json.dumps({'base_cases': len(base), 'sensitivities': len(sensitivity), 'combined_stress': len(stress),
                      'pairs': len(pairs), 'pair_passes': sum(x['reserve_pass'] for x in pairs),
                      'standard_non_shortfall': [x['id'] for x in base if not x['current_shortfall']],
                      'checks': 'passed'}, indent=2))


def write_report(out):
    lines = ['# Unified financial chain - existing Cheras case replay', '',
             'Release KV-EXEC-2026-10-07; configuration KV-FIN-90-4-35-v1. Run date 7 October 2026; original evidence cutoff 6 October 2026. No new market research. All price/rent/fee/repair inputs retain their original limitations. This is a scenario replay, not fair value, lender approval or an executable recommendation.', '',
             '## Common basis and cost boundary', '',
             '90% of acquisition price, 4% annual rate, 35 years; five-year illustrative hold. Gross yield preferably 6%. Rent is assumed, fee is a combined service/sinking proxy, and actual management-only coverage remains unverified. The baseline has eleven paid months per year, original other-cost and refurbishment allowances, 5% acquisition and 3% disposal allowances. It is pre-tax and excludes unquoted transaction-specific costs and base-case major works. These allowances are not legal fee/tax quotations. An illustrative extra-cost sensitivity adds RM1,200 annually and RM5,000 at exit; it is not a tax estimate.', '',
             'The 8% equity hurdle is illustrative, not user-approved. Cashflows are discounted monthly at an effective annual 8%, so hurdle results cannot be compared mechanically with the previous end-year approximation. Base first-year vacancy is month 1 and repeats each year. Holding scenarios use month-by-month principal/interest and collections. Standard coverage always retains 90%/4%/35 even in actual-financing stress.', '',
             '## Entry, coverage, carrying cost and exit', '',
             '| Case | Entry cash | Standard monthly balance | Annual base cashflow | Year-5 debt | Nominal break-even sale | Sale required for 8% | Flat-price total profit |',
             '|---|---:|---:|---:|---:|---:|---:|---:|']
    for x in out['base']:
        lines.append(f"| {x['id']} {x['name']} | {x['entry_cash']:,.0f} | {x['standard_monthly_balance']:+,.0f} | {x['cashflow_by_year'][0]:+,.0f} | {x['terminal_debt']:,.0f} | {x['terminal_nominal_breakeven']:,.0f} | {x['terminal_8pct_required']:,.0f} | {x['profit_by_exit_multiple']['1']:+,.0f} |")
    lines += ['', 'Required exits are burdens, not predictions or supported ceilings. Flat-price profit counts principal exactly once; loan proceeds are not returns. Financial inputs and unknown costs cannot be promoted to verified zero. Current-shortfall cases remain lowest research priority under the new SOP, not automatic structural Reject.', '',
              '## Future buyer payment at the required nominal break-even price', '',
              '| Case | Standard 90% / 4% / 35y payment | Actual-credit stress 80% / 5.5% / 25y payment |', '|---|---:|---:|']
    for x in out['base']:
        lines.append(f"| {x['id']} | {x['future_buyer_standard_payment_at_breakeven']:,.0f} | {x['future_buyer_stress_payment_at_breakeven']:,.0f} |")
    lines += ['', 'Lower stressed LTV requires more buyer cash; neither payment establishes buyer depth or loan eligibility. Actual loan terms, title and buyer equity must be resolved.', '',
              '## Twelve-month forced hold and correlated portfolio stress', '',
              'Synthetic RM500k starting cash and RM150k protected reserve, not user finances. Immediate RM30k works per asset, rate 5.5%, rent down 20%, no rent in the first six months and no sale for twelve months. Baseline 90% financing. Check the minimum monthly cash path, not only the ending balance. No salary, refinancing or future sale proceeds rescue the path.', '',
              '| Case | Minimum remaining cash | Reserve pass |', '|---|---:|---|']
    for x in out['combined_stress']:
        lines.append(f"| {x['id']} | {x['minimum_cash']:,.0f} | {'Yes, scenario' if x['protected_reserve_pass'] else 'No'} |")
    passes = sum(x['reserve_pass'] for x in out['pairs'])
    lines += ['', f"{passes} of {len(out['pairs'])} pairs preserve the synthetic reserve under simultaneous asset shocks. This differs from the old 80%/30-year result because entry equity and instalments both change. A pair funding pass does not establish suitable diversification, actual household reserves, debt-service approval or a Deploy. Cash-path details are in Financial_Results.json.", '',
              '## Five-year and delayed-exit sensitivities', '',
              '| Case | Scenario | Entry cash | Total carry cashflow | Terminal debt | Nominal break-even | Flat-price profit |', '|---|---|---:|---:|---:|---:|---:|']
    for x in out['sensitivities']:
        lines.append(f"| {x['id']} | {x['scenario']} | {x['entry_cash']:,.0f} | {x['cashflow_total']:+,.0f} | {x['terminal_debt']:,.0f} | {x['terminal_nominal_breakeven']:,.0f} | {x['profit_by_exit_multiple']['1']:+,.0f} |")
    lines += ['', 'Bank valuation down 15% finances 90% of the reduced value, increasing cash needed; it is a separate actual-finance constraint, not an alternative standard LTV. The delayed exit has 72 months of carry and amortisation. No-uplift is the base; catalysts are not automatic rent growth. No scenario is a worst-case bound.', '',
              '## Rank robustness: C01 versus C05', '',
              'Illustrative rent grid RM2,200/2,400/2,600 for each independently; not observed ranges or probability weights. This tests whether small assumption differences can reverse a cash-coverage preference, not which product has better actual buyer demand.', '',
              '| M Vertica rent | Maxim rent | Coverage leader | M Vertica balance | Maxim balance |', '|---:|---:|---|---:|---:|']
    for x in out['rank_grid']:
        lines.append(f"| {x['mvertica_rent']:,.0f} | {x['maxim_rent']:,.0f} | {x['coverage_leader']} | {x['mvertica_coverage']:+,.0f} | {x['maxim_coverage']:+,.0f} |")
    first, fifth = out['base'][0], out['base'][4]
    switch = fifth['standard_monthly_balance'] - first['standard_monthly_balance']
    lines += ['', f"At equal assumed rents, Maxim's coverage advantage is only RM{switch:.0f}/month. That small difference cannot support strong overall superiority with unverified rents, fees and operations. Independent rent/fee evidence has higher next-step value than another qualitative description of the same amenities.", '',
              '## Verification and status', '',
              'Checked recurrence against closed-form amortisation, principal conservation, independent interest-plus-cost break-even identity, monthly discounted hurdle, shock direction and rank reversal. The original model/report files are unchanged. No case passes missing G0/unit/governance evidence through this calculation. The full model is now on the approved baseline; the earlier bridge remains a historical calibration.']
    (ROOT / 'Financial_Replay.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
