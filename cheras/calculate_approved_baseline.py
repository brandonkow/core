"""Append-only comparison bridge; never executes or edits the original model."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def instalment(principal, annual_rate=.04, years=35):
    r = annual_rate / 12
    return principal * r / (1 - (1 + r) ** (-12 * years))


def calculate(case, ltv):
    loan = case['price'] * ltv
    payment = instalment(loan)
    coverage = case['rent_assumed'] - payment - case['fee_assumed']
    complete = 11 * case['rent_assumed'] - 12 * (
        payment + case['fee_assumed'] + case['other_assumed'])
    # Independent principal recurrence validates the 420-payment convention.
    balance = loan
    for _ in range(420):
        balance = balance * (1 + .04 / 12) - payment
    assert abs(balance) < .01
    assert abs(complete - (12 * coverage - case['rent_assumed']
                           - 12 * case['other_assumed'])) < .01
    return {'ltv': ltv, 'loan': loan, 'instalment': payment,
            'monthly_coverage_fee_proxy': coverage,
            'scenario_covers_fee_proxy': coverage >= 0,
            'annual_cashflow_11_paid_months_other_costs': complete,
            'cash_neutral_rent_11_months': 12 * (
                payment + case['fee_assumed'] + case['other_assumed']) / 11}


def main():
    original = json.loads((ROOT / 'Cheras_Financial_Results.json').read_text())
    rows = []
    for case in original['cases']:
        gross = 12 * case['rent_assumed'] / case['price']
        rows.append({'id': case['id'], 'name': case['name'],
                     'price_ask': case['price'], 'rent_assumed': case['rent_assumed'],
                     'fee_proxy': case['fee_assumed'],
                     'other_cost_assumed': case['other_assumed'],
                     'gross_yield': gross, 'meets_preferred_6pct': gross >= .06,
                     'at_80pct': calculate(case, .8),
                     'at_90pct': calculate(case, .9)})
    result = {'date': '2026-10-06', 'standard_ltv': .9, 'rate': .04, 'years': 35,
              'scope': 'Scenario calibration only, not fresh market or loan evidence',
              'fee_boundary': 'Prior service/sinking allowance used as proxy; verified management-only charges unavailable',
              'ltv_boundary': '90% user-mandated standard; 80% historical sensitivity only; no lender eligibility guarantee',
              'cases': rows}
    (ROOT / 'Cheras_Approved_Baseline_Results.json').write_text(
        json.dumps(result, indent=2) + '\n', encoding='utf-8')
    lines = [
        '# Cheras - approved baseline calibration bridge', '',
        'Date: 6 October 2026. Applies the user-approved 90% LTV / 4% / 35-year rent-coverage convention and preferred 6% gross yield to the original nine case inputs. This is a subsequent calibration, not a revision of earlier evidence or a completed new underwriting.', '',
        '## Evidence and comparison boundary', '',
        'Price, rent and costs are carried from [the original financial workpaper](Cheras_Financial_Underwriting.md). Prices are historical selected asks; rent and costs remain assumptions. No fresh availability, achieved rent, fee invoice or normalised G0 price is established. The old fee allowance covers estimated service/sinking charges and is used as a disclosed proxy here. It cannot certify a management-only break-even result. Exact fee inclusion and actual bank terms remain unverified.', '',
        'The user subsequently fixed 90% LTV for every future baseline comparison. Standard principal is 90% of acquisition price; 80% is retained only as a historical sensitivity. Actual lender margin or valuation constraints must be separately tested and cannot be used to relabel the standard result. Personal income is not used to make a failed property screen pass.', '',
        'Standard definition: monthly rent minus full mortgage instalment at 4%/35 years minus management fee. The following calculations substitute the disclosed fee proxy. Gross yield uses twelve monthly rents divided by the selected ask; 6% is a preference, not a hard gate. Complete-cost scenarios remain separate and still exclude tax, transaction-specific expenses and unexpected large works as described in the original workpaper.', '',
        '## Standard monthly coverage scenarios', '',
        '| Case | Rent assumed | Fee proxy | 90% standard instalment | 90% standard monthly balance | 80% historical monthly balance | Gross yield | 6% target reached? |',
        '|---|---:|---:|---:|---:|---:|---:|---|']
    for r in rows:
        lines.append(f"| {r['id']} {r['name']} | {r['rent_assumed']:,.0f} | {r['fee_proxy']:,.0f} | {r['at_90pct']['instalment']:,.0f} | {r['at_90pct']['monthly_coverage_fee_proxy']:+,.0f} | {r['at_80pct']['monthly_coverage_fee_proxy']:+,.0f} | {r['gross_yield']:.2%} | {'Yes, scenario' if r['meets_preferred_6pct'] else 'Below preference'} |")
    lines += ['', 'A positive figure is a pass only within these assumed-input/proxy scenarios. Unknown actual rent/management fee remains unknown. No case is upgraded to Deploy.', '',
              '## Separate complete-cost holding view', '',
              'This retains eleven paid rental months and the original other-cost allowance, in addition to the fee proxy and the new 35-year mortgage. It is not the definition of the user\'s standard monthly shortfall.', '',
              '| Case | Annual cashflow at standard 90% LTV | Annual cashflow at historical 80% LTV | Monthly rent needed at standard 90%, eleven paid months |',
              '|---|---:|---:|---:|']
    for r in rows:
        lines.append(f"| {r['id']} | {r['at_90pct']['annual_cashflow_11_paid_months_other_costs']:+,.0f} | {r['at_80pct']['annual_cashflow_11_paid_months_other_costs']:+,.0f} | {r['at_90pct']['cash_neutral_rent_11_months']:,.0f} |")
    p80 = [r['id'] for r in rows if r['at_80pct']['scenario_covers_fee_proxy']]
    p90 = [r['id'] for r in rows if r['at_90pct']['scenario_covers_fee_proxy']]
    lines += ['', '## Decision consequence', '',
              f"Under the approved 90% LTV standard, {len(p90)} of nine expressions cover the fee proxy: {', '.join(p90)}. The historical 80% sensitivity covers {len(p80)}: {', '.join(p80)}. These are not verified tenancies or lending decisions.", '',
              'The previous statement that all nine have negative annual cashflow referred to the original 30-year, eleven-paid-month, broader-cost model. It must not be restated as all nine failing the newly defined standard monthly coverage test. The two measures answer different questions.', '',
              'Maxim remains the provisional single-choice investigation preference from the subsequent conversation; this bridge does not prove management, buyer adoption, matched clearing or superiority over unresearched two-bedroom alternatives. All original gate stops remain. No ranking is promoted solely because a longer term reduces instalments.', '',
              'The original 30-year exit prices, five-year debt balances, return hurdles and portfolio stresses remain historical scenario results. This bridge does not relabel them as 35-year results. A later executable underwriting must recalculate those quantities, all relevant costs and actual financing before any Deploy decision.', '',
              '## Verification', '',
              'Mortgage amounts were reconciled to a 420-month principal recurrence; complete-cost cashflow was independently reconciled to standard monthly coverage less the unpaid month and annual other costs. Original model/report/result files are not modified. The earlier bridge/code/results are retained in `baseline-history/pre-90pct/` as historical records. Source and approval provenance: [approved SOP](../sop/Approved_Execution_Supplement.md) and [approval register](../sop/Founder_QA_Approval_Register.md).']
    (ROOT / 'Cheras_Approved_Baseline_Bridge.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({'checks': 'passed', 'standard_scenario_passes_80': p80,
                      'standard_scenario_passes_90': p90,
                      'maxim': next(r for r in rows if r['id'] == 'C05')}, indent=2))


if __name__ == '__main__':
    main()
