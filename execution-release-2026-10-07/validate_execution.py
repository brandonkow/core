"""Finite synthetic routing checks; never classifies live evidence automatically."""
from pathlib import Path
import json
from financial_engine import CFG, payment

ROOT = Path(__file__).resolve().parent
BASE = dict(gates_sufficient=True, structural_failure=False, allocation_veto=False,
            return_acceptable=True, monthly_balance=100, gross_yield=.06,
            transition_validated=False, transition_carry_funded=False, bedrooms=3)


def route(p):
    # Inputs are stipulated test truths, not an evidence-grading algorithm.
    if p['structural_failure']:
        return 'Reject'
    if p['allocation_veto']:
        return 'Preserve Capacity'
    if not p['gates_sufficient'] or not p['return_acceptable']:
        return 'Defer'
    if p['monthly_balance'] < 0 and not (
            p['transition_validated'] and p['transition_carry_funded']):
        return 'Defer'
    return 'Deploy'


def main():
    definitions = [
        ('V01', {}, 'Deploy', 'Complete supported synthetic packet'),
        ('V02', {'gates_sufficient': False}, 'Defer', 'G0 unknown'),
        ('V03', {'structural_failure': True, 'gross_yield': .09}, 'Reject', 'Critical structural failure despite high yield'),
        ('V04', {'allocation_veto': True}, 'Preserve Capacity', 'Independent allocation mismatch'),
        ('V05', {'monthly_balance': -100}, 'Defer', 'Announced catalyst only'),
        ('V06', {'monthly_balance': -100, 'transition_validated': True,
                 'transition_carry_funded': True}, 'Deploy', 'All transition and other gate requirements stipulated satisfied'),
        ('V07', {'monthly_balance': -100, 'transition_validated': True}, 'Defer', 'Transition carry not funded'),
        ('V08', {'monthly_balance': -100, 'personal_wealth': 10000000}, 'Defer', 'Wealth does not validate rent uplift'),
        ('V09', {'monthly_balance': 0, 'gross_yield': .055}, 'Deploy', 'Zero coverage and below preferred gross target'),
        ('V10', {'gates_sufficient': False, 'gross_yield': .07}, 'Defer', 'Future buyer unsupported'),
        ('V11', {'gates_sufficient': False, 'transfer_credit': 0,
                 'actual_transfer_demand': None}, 'Defer', 'No underwriting credit is not no actual demand'),
        ('V12', {'bedrooms': 2}, 'Deploy', 'Two-bedroom product on equal sufficient evidence'),
        ('V13', {'gates_sufficient': False, 'gross_yield': .08}, 'Defer', 'Inherited liabilities unknown'),
        ('V14', {'structural_failure': True, 'gross_yield': .08}, 'Reject', 'Established title/transfer failure'),
    ]
    rows = []
    for cid, changes, expected, description in definitions:
        packet = dict(BASE, **changes)
        result = route(packet)
        assert result == expected, cid
        priority = 'Lowest: retain/event-watch' if packet['monthly_balance'] < 0 else 'Evaluate evidence value'
        simple = 'Select' if packet['monthly_balance'] >= 0 and packet['gross_yield'] >= .06 else 'Exclude'
        rows.append(dict(id=cid, packet=packet, expected=expected, result=result,
                         research_priority=priority, simple_screen=simple, description=description))
    assert rows[10]['packet']['actual_transfer_demand'] is None
    assert route(dict(BASE, bedrooms=1)) == route(dict(BASE, bedrooms=3))
    assert route(dict(BASE, structural_failure=True, allocation_veto=True)) == 'Reject'
    assert route(dict(BASE, monthly_balance=-100, transition_validated=True,
                      transition_carry_funded=True, gates_sufficient=False)) == 'Defer'
    assert route(dict(BASE, return_acceptable=False)) == 'Defer'
    assert abs(payment(420000, 0, 35) - 1000) < .001
    for args in [(1, -.01, 35), (1, .04, 0), (-1, .04, 35)]:
        try:
            payment(*args)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid loan accepted')
    assert (CFG['standard_ltv'], CFG['standard_rate'], CFG['standard_term_years']) == (.9, .04, 35)
    output = {'scope': 'Synthetic logical consistency, not live or blind investment validation',
              'fixtures': rows, 'checks': 'passed', 'empirical_deploy_reject_validated': False}
    (ROOT / 'Validation_Results.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    lines = ['# Finite execution validation results', '',
             '7 October 2026. Read [pre-lock](Validation_PreLock.md). Fourteen stipulated synthetic packets test routing only. They are not fourteen market outcomes, inspected deals or an accuracy sample. Evidence sufficiency is an input to this test, not a capability proven by it.', '',
             '| Fixture | Stipulated issue | Expected / observed G9 | Current research treatment | Simple coverage + 6% screen |',
             '|---|---|---|---|---|']
    for r in rows:
        lines.append(f"| {r['id']} | {r['description']} | {r['expected']} / {r['result']} | {r['research_priority']} | {r['simple_screen']} |")
    lines += ['', '## What the comparator exposes', '',
              'The simple screen selects V03/V14 despite established structural failure, V02/V10/V13 despite critical unknowns, and V04 despite allocation mismatch. It excludes V09 solely for missing the preferred 6% target. A rigid no-shortfall rule excludes V06 even though the synthetic packet stipulates a fully supported, funded exception. These are constructed diagnostic disagreements, not measured field superiority or observed missed profits.', '',
              '## Financial and interaction checks', '',
              'The financial replay checks nine baseline cases, 81 one-factor/actual-finance/extra-cost scenarios, nine combined monthly stress paths and 36 paired paths. Identities cover amortisation, principal conservation, full economic break-even and discounted terminal return. Additional checks cover zero interest, invalid inputs, structural veto precedence, unresolved gates despite an otherwise validated transition, return insufficiency and bedroom-count neutrality. Rank-grid results demonstrate a C01/C05 reversal under different unverified rent inputs.', '',
              '## What remains unvalidated', '',
              'No new achieved rent, matched clearing price, MC account pack, title verification or physical inspection was obtained. No empirical Deploy or current structural Reject is added. No forward call matured because of this release. The historical Phase 7 gap remains explicit. This finite release validates arithmetic and routing consistency, not the probability of investment success.', '',
              '## Release interpretation', '',
              'The designed checks pass. The work supports moving to a bounded regional research process after the promised user notification. It does not certify a buy-ready shortlist, remove current unknowns or permit automatic investment. Future evidence can require scenario, SOP or interpretation revisions under the existing change discipline.']
    (ROOT / 'Validation_Report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({'routing_fixtures': len(rows), 'checks': 'passed', 'empirical_validation': False}))


if __name__ == '__main__':
    main()
