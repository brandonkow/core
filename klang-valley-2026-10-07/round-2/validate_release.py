"""Read-only calculation/provenance checks; writes only this round's audit."""
from pathlib import Path
import json,hashlib,re,importlib.util,math
ROOT=Path(__file__).resolve().parent; P=ROOT.parent; PROJECT=P.parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,condition):
    checks.append(dict(check=name,passed=bool(condition)))
    if not condition:raise AssertionError(name)
baseline=read(P/'Baseline_Integrity.json')
protected=[x for x in baseline if x['path']!='README.md']
check('57 protected pre-programme artifacts unchanged',len(protected)==57 and all(sha(PROJECT/x['path'])==x['sha256'] for x in protected))
r1manifest=read(P/'Release_Manifest.json')
check('21 frozen R1 artifacts unchanged',len(r1manifest['files'])==21 and all(sha(P/k)==v for k,v in r1manifest['files'].items()))
check('single master exact frozen hash',sha(PROJECT/'Residential_Investment_Framework.md')=='1fbf607a78111bc007736fe0cc8109ad3967939a2dcc7ff54f017b491172e86b')
master=(PROJECT/'Residential_Investment_Framework.md').read_text(encoding='utf-8')
check('original ten gate headings retained',len(re.findall(r'^## G[0-9] —',master,re.M))==10)
cases=read(ROOT/'Case_Inputs.json')['cases'];areas=read(ROOT/'Coverage_Register.json')
f=read(ROOT/'Financial_Results.json');b=f['base']
check('50 distinct new conditional cases and papers',len(cases)==50 and len({c['id'] for c in cases})==50 and all((ROOT/'cases'/f"{c['id']}.md").exists() for c in cases))
orig=read(P/'Coverage_Register.json')
check('61 original catchments and eight batches unchanged',len(areas)==61 and [a['catchment'] for a in areas]==[a['catchment'] for a in orig] and len({a['batch'] for a in areas})==8)
check('47 catchments with new expression diagnostics',len({c['area_id'] for c in cases})==47)
check('no silent G0 bypass or Deploy',all(c['g9']=='Defer' and c['g0'].startswith('STOP') for c in cases))
check('all new papers retain G0 to G9',all(all(f'| G{i} ' in (ROOT/'cases'/f"{c['id']}.md").read_text(encoding='utf-8') for i in range(10)) for c in cases))
check('approved financial baseline retained',f['config']['standard_ltv']==.9 and f['config']['standard_rate']==.04 and f['config']['standard_term_years']==35)
check('450 sensitivity and450 rent-fee grid records',len(f['sensitivities'])==450 and len(f['rank_grid'])==450)
check('2016 independent two-expression combinations',len(f['pairs_including_r1'])==math.comb(64,2) and len({tuple(p['ids']) for p in f['pairs_including_r1']})==2016)
check('each synthetic pair min path and reserve flag internally consistent',all(abs(min(p['cash_path'])-p['minimum_cash'])<.01 and p['reserve_pass']==(p['minimum_cash']>=150000) for p in f['pairs_including_r1']))
engine=PROJECT/'execution-release-2026-10-07'/'financial_engine.py'
check('engine checksum agrees with release',f['engine_sha256']==sha(engine))
spec=importlib.util.spec_from_file_location('approved_verify',engine);eng=importlib.util.module_from_spec(spec);spec.loader.exec_module(eng)
for c,x in zip(cases,b):
    eng.check_financial_identities(x,c)
    rr=eng.evaluate(c)
    check(c['id']+' independent replay',all(abs(rr[k]-x[k])<.01 for k in ('standard_instalment','terminal_debt','terminal_nominal_breakeven','terminal_8pct_required','cashflow_total')))
    check(c['id']+' current-shortfall priority respected',not x['current_shortfall'] or x['priority'].startswith('Lowest'))
check('both nonnegative annual scenarios held',{x['id'] for x in b if x['cashflow_by_year'][0]>=0}=={'R208','R219'} and all(x['quarantine'] for x in b if x['cashflow_by_year'][0]>=0))
check('cashflow arithmetic not labelled verified income',all(c['rent_status'].startswith('Working') and 'Unverified' in c['fee_status'] for c in cases))
check('source lineage files exist',all(all(list((ROOT/'raw').glob(k+'_*.json')) for k in c['retrievals']) for c in cases))
check('scope gaps explicitly retained including core Hilir',areas[38]['depth'].startswith('Core catchment screen only') and all(a['material_segment_gaps'] for a in areas))
check('six material flags and18misses',len(re.findall('⚠ DIVERGENCE FLAG',(ROOT/'Divergence_and_Misses.md').read_text(encoding='utf-8')))==6 and len(re.findall(r'\| M\d{2} \|',(ROOT/'Divergence_and_Misses.md').read_text(encoding='utf-8')))==18)
broken=[]
for p in ROOT.rglob('*.md'):
    for dest in re.findall(r'\]\(<([^>]+)>\)',p.read_text(encoding='utf-8')):
        if not Path(dest).exists():broken.append((str(p),dest))
# Validation_Report.md is about to be written; allow only that forward reference.
broken=[x for x in broken if Path(x[1])!=ROOT/'Validation_Report.md']
check('all artifact file links resolve',not broken)
report=dict(version='KV-REG-2026-10-07-R2',checks=checks,all_passed=all(c['passed'] for c in checks),
 market_verification='Not established: no authenticated exact-title, lease, MC/physical, lender or realised-outcome validation',
 core_sha256=sha(PROJECT/'Residential_Investment_Framework.md'),engine_sha256=sha(engine))
(ROOT/'Validation_Results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
(ROOT/'Validation_Report.md').write_text(
 '# Verification and preservation audit\n\nCutoff7October2026. Checks below verify provenance, scope and arithmetic. They do not verify market truth, unit availability, property condition, lender eligibility or predicted investment performance.\n\n'
 +'| Check | Result |\n|---|---|\n'+'\n'.join('| '+x['check']+' | Pass |' for x in checks)
 +'\n\nThe57protected baseline files and21R1manifest members are unchanged. README navigation is the only authorised existing-document update; all new research is in round-2. The financial engine/configuration, master, SOP, Phase7, failure library, historical/forward records, terminal and portfolio work are preserved. This release adds dated cases/misses rather than rewriting historical calls. Market data gaps remain exactly as disclosed.\n',
 encoding='utf-8')
manifest=dict(release='KV-REG-2026-10-07-R2',files={str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and p.name!='Release_Manifest.json' and '__pycache__' not in str(p)})
(ROOT/'Release_Manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(checks=len(checks),all_passed=True,files=len(manifest['files']),core_sha256=report['core_sha256']),indent=2))

