from pathlib import Path
import json,re,hashlib,math
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent
baseline=json.loads((ROOT/'Baseline_Integrity.json').read_text(encoding='utf-8-sig'))
changes=[];missing=[]
for item in baseline:
 p=PARENT/item['path']
 if not p.exists():missing.append(item['path']);continue
 h=hashlib.sha256(p.read_bytes()).hexdigest()
 if h.lower()!=item['sha256'].lower():changes.append(item['path'])
assert not missing,missing
assert changes==['README.md'],changes
assert hashlib.sha256((PARENT/'Residential_Investment_Framework.md').read_bytes()).hexdigest()=='1fbf607a78111bc007736fe0cc8109ad3967939a2dcc7ff54f017b491172e86b'
cases=json.loads((ROOT/'Case_Inputs.json').read_text(encoding='utf-8'))['cases']
src=json.loads((ROOT/'Evidence_Register.json').read_text(encoding='utf-8'))['sources']
coverage=json.loads((ROOT/'Coverage_Register.json').read_text(encoding='utf-8'))
fin=json.loads((ROOT/'Financial_Results.json').read_text(encoding='utf-8'))
ids={x['id'] for x in src}
assert len(ids)==65
assert len(cases)==14 and {c['batch'] for c in cases}=={f'B{i:02}' for i in range(1,9)}
for c,b in zip(cases,fin['base']):
 assert c['g9']==b['g9']=='Defer'
 assert all(c[k] in ids for k in ('price_source','rent_source','diagnostic_source'))
 monthly=.04/12
 instalment=.9*c['price']*monthly/(1-(1+monthly)**(-35*12))
 assert math.isclose(instalment,b['standard_instalment'],abs_tol=.001)
 standard=c['rent_assumed']-instalment-c['fee_assumed']
 annual=11*c['rent_assumed']-12*(instalment+c['fee_assumed']+c['other_assumed'])
 assert abs(standard-b['standard_monthly_balance'])<.001
 assert abs(annual-b['cashflow_by_year'][0])<.001
 assert abs(.15*c['price']+c['refurb_assumed']-b['entry_cash'])<.001
assert sum(not b['current_shortfall'] for b in fin['base'])==7
assert all(b['cashflow_by_year'][0]<0 for b in fin['base'])
assert len(coverage)==61
assert sum(x['status']=='Mapped only' for x in coverage)==43
assert len(fin['sensitivities'])==126 and len(fin['rank_grid'])==126
assert len(fin['pairs'])==91 and sum(x['reserve_pass'] for x in fin['pairs'])==85
papers=(ROOT/'Selected_Case_Workpapers.md').read_text(encoding='utf-8')
for g in range(10):assert len(re.findall(r'^\| G'+str(g)+r' — ',papers,re.M))==14
assert papers.count('### At most three immediate evidence tasks')==14
assert papers.count('### Current-shortfall transition record')==7
div=(ROOT/'Divergence_and_Misses.md').read_text(encoding='utf-8')
assert div.count('**⚠ DIVERGENCE FLAG**')==5
for family in ('A. Data limitation','B. Judgment bias','C. Omitted variable','D. Structural change'):
 assert div.count('| '+family)==5
broken=[]; non_english=[]
for p in ROOT.glob('*.md'):
 s=p.read_text(encoding='utf-8')
 if re.search(r'[\u4e00-\u9fff]',s):non_english.append(p.name)
 for target in re.findall(r'\]\(([^)]+)\)',s):
  if target.startswith(('https://','http://','#')):continue
  target=target.split('#')[0]
  if target and not (p.parent/target).exists() and target!='Validation_Report.md':broken.append((p.name,target))
assert not broken,broken
assert not non_english,non_english
results=dict(date='2026-10-07',master_sha256='1fbf607a78111bc007736fe0cc8109ad3967939a2dcc7ff54f017b491172e86b',
baseline_files=len(baseline),unchanged_baseline_files=len(baseline)-len(changes),intentional_changed_files=changes,
new_cases=14,scope_catchments=61,new_worked_catchments=14,inherited_only_catchments=4,mapped_only_catchments=43,
source_entries=65,gates_per_case=10,divergence_flags=5,current_shortfall_transition_records=7,
sensitivities=126,rank_grid_rows=126,stress_pairs=91,synthetic_pair_passes=85,
numerical_and_structural_checks='passed',investment_evidence_validation='not established',
coverage_completion='first comparative release only; full-area desk underwriting incomplete',
external_actions='none: no outreach, paid data, purchase or automation')
(ROOT/'Validation_Results.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
txt=f"""# Validation and preservation record

Cutoff: 7 October 2026. This validates document consistency and scenario arithmetic, not investment accuracy.

## Preservation

- {len(baseline)} pre-existing files recorded before research.
- {len(baseline)-len(changes)} remain byte-for-byte unchanged, including the master, SOP/release, historical/backtest/forward material, original Cheras work and approved engine.
- Only the existing README changed intentionally to register the authorised launch and new outputs. It does not change framework logic.
- Master SHA256: {results['master_sha256']}.
- No new Core module, G10, causal promotion, renamed gate or second consolidated master.

## Checks completed

- Independent monthly-payment, standard-coverage, eleven-month annual-carry and entry-cash recomputation for 14 cases.
- Approved engine checks: closed-form loan balance, principal conservation, independent economic-cost break-even identity, discounted hurdle and adverse-scenario directions.
- Financial thresholds independently reproduce zero standard balance, annual carry neutrality and 6% gross arithmetic.
- Fourteen ordered ten-gate papers; all G9 Defer; seven current-shortfall transition packets.
- Five material flags each retain A–D tests, falsifiers, routing and unresolved status.
- 65 distinct source IDs with price/rent/diagnostic references resolved; independence and access limitations explicit.
- 61 mapped catchments: 14 with new selected expressions, four with inherited selective work only, 43 mapped only.
- 126 financial sensitivities, 126 rent/fee grid rows and 91 synthetic pairs; 85 pairs preserve the illustrative reserve.
- Local Markdown links checked and all new Markdown text remains English.

## Verification limits

No title/plan instrument, signed rent, fee invoice, MC accounts, actual bank offer or physical unit was verified. External advertisements can change or disappear; lookup dates do not establish execution terms. Sources marked search-indexed were not upgraded to fully inspected pages. Photos/video were not viewed.

No gate clearance, valuation accuracy, forecast hit, realised return or region-wide completeness follows from passing arithmetic/format checks. No claim of executed purchase, contacted counterparty, paid report, background research or monitoring.

## Release disposition

First comparative release ready for review. Full-area regional underwriting remains incomplete. Senior Market Red Team review concerns buyer-mechanism hypotheses in Programme_Review.md; it is not approval to waive evidence or a request that the user supply operational data. The remaining catchments and exact evidence routes are recorded.
"""
(ROOT/'Validation_Report.md').write_text(txt,encoding='utf-8')
manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.iterdir() if p.is_file() and p.name!='Release_Manifest.json'}
(ROOT/'Release_Manifest.json').write_text(json.dumps(dict(release='KV-REG-2026-10-07-R1',files=manifest),indent=2)+'\n',encoding='utf-8')
print(json.dumps(results,indent=2))

