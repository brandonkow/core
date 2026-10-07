"""Build a progress register and verify preservation; does not certify research completion."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROGRAMME = HERE.parent
ROOT = PROGRAMME.parent

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

scope = read_json(PROGRAMME / 'Coverage_Register.json')
cases = read_json(PROGRAMME / 'round-2/Case_Inputs.json')['cases']
contrasts = read_json(HERE / 'Contrasting_Case_Inputs.json')['cases']
pj_audit = read_json(HERE / 'B03_Completion_Audit.json')
contrasts += read_json(HERE / 'B03_Case_Inputs.json')['cases']
pj_closed = {r['area_id'] for r in pj_audit['rows'] if r['desk_complete']}
b04_audit = read_json(HERE / 'B04_Completion_Audit.json')
contrasts += read_json(HERE / 'B04_Case_Inputs.json')['cases']
b04_closed = {r['area_id'] for r in b04_audit['rows'] if r['desk_complete']}
b05_audit = read_json(HERE / 'B05_Completion_Audit.json')
contrasts += read_json(HERE / 'B05_Case_Inputs.json')['cases']
b05_closed = {r['area_id'] for r in b05_audit['rows'] if r['desk_complete']}
prior = {}
for line in (PROGRAMME / 'round-2/Area_Research_Inputs.txt').read_text(encoding='utf-8-sig').splitlines():
    if line.strip():
        index, mechanism, substitutes, counter, gaps = line.split('|')
        prior[int(index)] = dict(mechanism=mechanism, substitutes=substitutes, counter=counter, gaps=gaps)

rows = []
for index, area in enumerate(scope, 1):
    area_id = f'A{index:02}'
    new_work = 'No round 3 regional reassessment yet; inherited work retained.'
    next_action = prior[index]['gaps']
    completion = 'Not certified; material breadth/depth audit remains'
    if 1 <= index <= 10:
        new_work = 'Enhanced B01_Regional_Synthesis.md integrates household tasks, contrasting products, dated supply, exit risks and current financial comparison; final coverage audit remains.'
        next_action = 'Audit the bounded regional synthesis against all seven completion dimensions; resolve only decision-changing remaining public gaps. Exact-unit private proof remains separate from regional desk completion.'
    if 11 <= index <= 17:
        new_work = 'Enhanced B02_Regional_Synthesis.md integrates transfer/identity work, three new residential product controls, dated supply and financial boundaries; final coverage audit remains.'
        next_action = 'Audit the bounded regional synthesis against all seven completion dimensions, including screened family alternatives and standalone compact identity; include new controls in the final portfolio replay.'
    if index == 16:
        next_action = 'Maintain Aurora identity quarantine. Tropika 732-sf two-bedroom control is now documented; reconcile 710-sf transfer coding before any clearing-value claim. Complete final coverage and portfolio audit.'
    if area_id in pj_closed:
        new_work = 'B03 bounded regional desk pass complete: functional map, product contrasts, dated supply/comparables, fourteen G0-G9 expressions, financial/portfolio stress and divergence investigations; see B03_Completion_Audit.md.'
        completion = 'Bounded regional desk-complete Defer; exact-unit decision readiness and outcome validation unresolved'
        next_action = 'No generic public rescan required. Reopen only on the case-specific identity, effective offer, ordinary lease, fee/works, matched transfer or material supply/financing evidence in B03_Cases_G0_G9.md. Continue programme at B05.'
    if area_id in b04_closed:
        new_work = 'B04 bounded regional desk pass complete: nine functional catchments, material product contrasts and explicit gaps, primary supply/access corrections, nineteen G0-G9 expressions, financial/portfolio diagnostics and five divergence investigations; see B04_Completion_Audit.md.'
        completion = 'Bounded regional desk-complete Defer; exact-unit decision readiness and outcome validation unresolved'
        next_action = 'No generic public rescan required. Reopen on the area-specific exact identity/plan/offer, ordinary lease or current tenancy, fees/works, matched transfer or material supply evidence in B04_Cases_G0_G9.md. Pines/Windsor are verification leads only; Neo/Cliveden remain offer/component-held. Continue programme at B05.'
    if area_id in b05_closed:
        new_work = 'B05 bounded regional desk pass complete: seven functional catchments, compact/family contrasts, fifty saved source retrievals, sixteen G0-G9 expressions, full financial/portfolio diagnostics and six material divergence investigations; see B05_Completion_Audit.md.'
        completion = 'Bounded regional desk-complete Defer; exact-unit decision readiness and outcome validation unresolved'
        next_action = 'Reopen on case-specific current offer/plan/use, ordinary or in-place lease, charge period, fees/works or adjusted transfers in B05_Cases_G0_G9.md. Parkview and Titiwangsa are evidence leads; Lucentia fee and Boulevard component remain held. Continue programme at B06; cross-reference Seri Maya once.'
    next_action = next_action.replace('Continue programme at B05.', 'Continue programme at B06.')
    rows.append(dict(area_id=area_id, batch=area['batch'], catchment=area['catchment'],
                     inherited_r1=area['new_cases'], inherited_cheras=area['inherited'],
                     r2_cases=[c['id'] for c in cases if c['area_id'] == area_id],
                     r3_cases=[c['id'] for c in contrasts if c['area_id'] == area_id],
                     prior_gap=prior[index]['gaps'], current_work=new_work,
                     next_public_research=next_action, completion=completion,
                     decision_ready=False, source='Original scope and inherited evidence; B01/B02 enhanced syntheses and B03/B04/B05 substantive self-audits. No completion inference from case count.'))
assert len(rows) == 61 and len({r['area_id'] for r in rows}) == 61
(HERE / 'Coverage_Audit.json').write_text(json.dumps({'version':'KV-REG-2026-10-07-R3-open','programme_complete':False,'rows':rows}, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
lines = ['# Coverage audit - current research remains incomplete', '',
         'Date: 7 October 2026. The 61 rows preserve the original scope. This is a work register, not 61 fresh regional analyses. Twenty-three catchments in B03/B04/B05 are bounded desk-complete Defer on separate substantive self-audits, not this administrative register. No decision-ready unit or realised validation is claimed.', '',
         'Completion requires the seven substantive dimensions in [the continuation audit](Continuation_and_Completion_Audit.md). A future desk-complete Defer is possible; the present generic gap list does not itself close the work.', '',
         'B01/B02 have enhanced syntheses for 17 catchments with final substantive audit pending; B03/B04/B05 have closed bounded desk passes for seven, nine and seven catchments. The remaining 21 catchments in B06-B08 await comparable regional deepening. Cross-region and programme portfolio work remain. These are workflow counts, not programme completion percentages.', '',
         '| Area | Catchment | Retained and added cases | Remaining targeted research |', '|---|---|---|---|']
for r in rows:
    identifiers = ', '.join(r['inherited_r1']+r['r2_cases']+r['r3_cases']) or 'Inherited/screening only'
    lines.append(f"| {r['area_id']} / {r['batch']} | {r['catchment']} | {identifiers} | {r['next_public_research']} |")
lines += ['', '## Immediate sequence', '',
          '1. Retain the enhanced B01/B02 syntheses, supply register and four contrasting cases. Perform the final substantive coverage audit without equating document production with completion.',
          '2. Retain B03-B05 releases and their reopening conditions. B05 adds fee-period, current-tenancy, component/use and lower-offer counterexamples; none clears a purchase.',
          '3. Continue northern and northeastern B06 A41-A45; do not double-count Seri Maya or transfer Sentul conclusions across household/route boundaries.',
          '4. Complete B07/B08 household-form, institutional accommodation and new-delivery comparisons.',
          '5. Compare justified price conditions and rank reversals across regions; audit completion independently of case counts. No forced winner or Deploy.', '',
          'The user authorised continuing after PJ. The next bounded batch is B06, A41-A45; see B05_RESUME_CHECKPOINT.md. No background scheduler or active goal object is implied.']
(HERE / 'Coverage_Audit.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

factor = .9*(.04/12)/(1-(1+.04/12)**(-35*12))
financial = ['# B02 mechanical price boundaries', '',
             'Date: 7 October 2026. Unchanged 90% purchase-price loan, 4%, 35 years. This supplements rather than replaces the existing full financial engine. Inputs are inherited asking/assumed scenarios; no achieved rent, fee bill, transaction valuation or executable price is newly validated.', '',
             'Monthly instalment = purchase price x '+f'{factor:.9f}'+'. Standard boundary = (monthly rent - assumed fee) / factor. Preferred 6% gross boundary = monthly rent x 200. Annual cash-neutral rent = 12 x (instalment + fee + other monthly costs) / 11, using the inherited eleven-paid-month convention. Acquisition, refurbishment, taxes and terminal costs still belong in the full model.', '',
             '| Case | Assumed entry | Rent / fee / other monthly | Standard price boundary | 6% gross price boundary | Annual cash-neutral rent |', '|---|---:|---:|---:|---:|---:|']
for c in cases:
    if c['batch'] != 'B02':
        continue
    price, rent, fee, other = [c[k] for k in ['price','rent_assumed','fee_assumed','other_assumed']]
    label = c['id'] + (' - IDENTITY HOLD' if c['id']=='R205' else '')
    financial.append(f"| {label} | {price:,.0f} | {rent:,.0f} / {fee:,.0f} / {other:,.0f} | {(rent-fee)/factor:,.0f} | {rent*200:,.0f} | {12*(price*factor+fee+other)/11:,.0f} |")
financial += ['', 'These boundaries are financing/yield sensitivities, not offers, supported fair values or minimum safety margins. A price satisfying both numerical tests can still fail identity, quality, reference-price, exit or actual lending tests. The unresolved Aurora row remains a historical mathematical example and is excluded from eligible residential ranking.', '',
              'Kuchai and Endah remain evidence-priority leads at their inherited scenario inputs. OUG and Desa Green are near or below the simplified coverage boundary. Those distinctions are price-dependent research priorities, not proven product rankings. Trion rent remains a seller tenancy claim. Any revised rent or fee must propagate through the full cashflow and exit model before a capital decision.']
(HERE / 'B02_Financial_Boundaries.md').write_text('\n'.join(financial)+'\n',encoding='utf-8')

checks = []
def check_file(path, expected, group):
    actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
    checks.append({'group':group,'path':str(path.relative_to(ROOT)),'pass':actual==expected,'expected':expected,'actual':actual})
for item in read_json(PROGRAMME / 'Baseline_Integrity.json'):
    if item['path'] != 'README.md':
        check_file(ROOT / item['path'], item['sha256'], 'preserved-preprogramme')
for directory in [PROGRAMME, PROGRAMME/'round-2']:
    manifest = read_json(directory / 'Release_Manifest.json')
    for name, expected in manifest['files'].items():
        check_file(directory / name, expected, manifest['release'])
failures = [x for x in checks if not x['pass']]
result = {'scope_rows':len(rows),'programme_complete':False,'master_unchanged':hashlib.sha256((ROOT/'Residential_Investment_Framework.md').read_bytes()).hexdigest()=='1fbf607a78111bc007736fe0cc8109ad3967939a2dcc7ff54f017b491172e86b',
          'preservation_checks':len(checks),'failures':failures,'checks':checks,
          'boundary':'File integrity and scope only; not market validation, completion certification, legal clearance or investment approval.'}
(HERE / 'Preservation_Audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert not failures and result['master_unchanged'], json.dumps(failures)
print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False,indent=2))
