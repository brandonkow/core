"""Verify B04 arithmetic/structure and prior file integrity, not market authenticity."""
import hashlib
import importlib.util
import itertools
import json
import re
from pathlib import Path

P=Path(__file__).resolve().parent
ROOT=P.parent.parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,condition):
    checks.append(dict(name=name,pass_check=bool(condition)))
    assert condition,name

a=read(P/'B04_Completion_Audit.json')
f=read(P/'B04_Financial_Results.json')
for name in a['required_files']:
    check('substantive output exists: '+name,(P/name).is_file() and (P/name).stat().st_size>100)
check('exact nine B04 catchments',{r['area_id'] for r in a['rows']}=={f'A{i}' for i in range(25,34)})
check('63 authored substantive assessments',sum(len(r['dimensions']) for r in a['rows'])==63)
check('no decision-ready area',all(r['desk_complete'] and not r['decision_ready'] and r['g9']=='Defer' for r in a['rows']))
check('19 unique expressions',len(f['results'])==len({r['case']['id'] for r in f['results']})==19)
check('nine new expressions',len(read(P/'B04_Case_Inputs.json')['cases'])==9)
check('ten retained expressions',len(read(P/'B04_Inherited_Assessments.json'))==10)
check('all active B04 areas represented',{r['case']['area_id'] for r in f['results']}=={r['area_id'] for r in a['rows']})

spec=importlib.util.spec_from_file_location('frozen',ROOT/'execution-release-2026-10-07/financial_engine.py')
engine=importlib.util.module_from_spec(spec);spec.loader.exec_module(engine)
check('frozen financial configuration',f['config']==engine.CFG)
count=0
for r in f['results']:
    c=r['case']
    for name,s in r['scenarios'].items():
        engine.check_financial_identities(s,c,5000 if name=='extra_cost_buffer' else 0)
        count+=1
    b=r['scenarios']['base'];d=r['boundaries']
    check(c['id']+' standard90/4/35',abs(b['actual_instalment']-engine.payment(.9*c['price'],.04,35))<.001)
    check(c['id']+' gross yield',abs(b['gross_yield']-12*c['rent_assumed']/c['price'])<1e-10)
    check(c['id']+' standard coverage',abs(b['standard_monthly_balance']-(c['rent_assumed']-c['fee_assumed']-b['actual_instalment']))<.001)
    check(c['id']+' annual carry',abs(b['cashflow_by_year'][0]-(11*c['rent_assumed']-12*(b['actual_instalment']+c['fee_assumed']+c['other_assumed'])))<.001)
    check(c['id']+' future buyer retains90LTV',abs(r['future_buyer_90_5_5_25']-engine.payment(.9*b['terminal_nominal_breakeven'],.055,25))<.001)
    check(c['id']+' boundary is mechanical',abs(d['gross6_price']-200*c['rent_assumed'])<.001)
for r in f['alternative_prices']:
    c=dict(next(x['case'] for x in f['results'] if x['case']['id']==r['id']),price=r['price'])
    engine.check_financial_identities(r['result'],c);count+=1
check('251 independent identity rechecks',count==f['financial_identity_checks']==251)
by={r['case']['id']:r for r in f['results']}
check('171 unique pair paths',len(f['diagnostic_pairs'])==len({tuple(sorted(x['ids'])) for x in f['diagnostic_pairs']})==171)
check('all pairs represented',{tuple(sorted(x['ids'])) for x in f['diagnostic_pairs']}==set(itertools.combinations(sorted(by),2)))
for pair in f['diagnostic_pairs']:
    x,y=(by[i]['scenarios']['combined12'] for i in pair['ids'])
    path=[engine.CFG['synthetic_cash']-x['entry_cash']-y['entry_cash']]
    for u,v in zip(x['schedule'],y['schedule']):path.append(path[-1]+u['cashflow']+v['cashflow'])
    check('pair '+','.join(pair['ids']),len(path)==13 and max(abs(u-v) for u,v in zip(path,pair['cash_path']))<.001 and abs(min(path)-pair['minimum_cash'])<.001 and pair['reserve_pass']==(min(path)>=engine.CFG['synthetic_protected_reserve']))
check('49 synthetic reserve passes',sum(x['reserve_pass'] for x in f['diagnostic_pairs'])==49)
check('nine rent combinations reverse the lead',len(f['rank_grid'])==9 and {r['leader'] for r in f['rank_grid']}=={'R315','R316'})
check('every flat-price full-hold profit negative',all(r['scenarios']['base']['profit_by_exit_multiple']['1']<0 for r in f['results']))
check('only Neo has positive annual base carry',[r['case']['id'] for r in f['results'] if r['scenarios']['base']['cashflow_by_year'][0]>0]==['R219'])
check('United current tenancy uncertainty modelled','existing_lease_no_credit6' in by['R317']['scenarios'])

paper=(P/'B04_Cases_G0_G9.md').read_text(encoding='utf-8')
for r in f['results']:
    cid=r['case']['id'];s=paper.split('## '+cid+' - ',1)[1].split('\n## ',1)[0]
    for gate in range(10):check(cid+' G'+str(gate),('| G'+str(gate)+' ') in s)
    check(cid+' stop/defer retained','STOP.' in s and '| G9 Capital Decision | Defer.' in s)
    check(cid+' explicit counter and reopening','Strongest counter-thesis / falsification:' in s and 'Finite evidence / reopening:' in s)
check('Cliveden false-surplus wording absent','removes the apparent annual surplus' not in paper)
div=(P/'B04_Divergence_and_Misses.md').read_text(encoding='utf-8')
check('five material flags',div.count('**⚠ DIVERGENCE FLAG**')==5)
for k in ['Data limitation','Judgment bias','Omitted variable','Structural change','Falsifiable Hypothesis','Evidence Required','Falsification Conditions','Core Module Routing','Current Status']:
    check('five investigation fields '+k,div.count('**'+k)>=5)
raw=sorted((P/'b04-raw').glob('*.json'))
check('41 raw retrievals',len(raw)==41 and {int(q.name[:3]) for q in raw}==set(range(1,42)))
for q in raw:read(q)
for c in read(P/'B04_Case_Inputs.json')['cases']:
    for rid in c['retrievals']:check(c['id']+' raw'+rid,any((P/'b04-raw').glob(rid+'*.json')))
for md in P.glob('B04_*.md'):
    for target in re.findall(r'\]\(([^)]+)\)',md.read_text(encoding='utf-8')):
        if target.startswith(('https:','http:')):continue
        target=target.strip('<>').split('#',1)[0]
        if not target:continue
        # These two outputs are written below; their links are checked again afterwards.
        if target in ['B04_Release_Audit.json','B04_Release_Manifest.json']:continue
        check(md.name+' local link '+target,(md.parent/target).is_file())

pres=read(P/'Preservation_Audit.json')
check('prior preservation register281',pres['preservation_checks']==281 and not pres['failures'])
preserved=[]
for item in pres['checks']:
    q=ROOT/item['path'];ok=q.exists() and digest(q)==item['expected']
    preserved.append(dict(path=item['path'],group=item['group'],pass_check=ok))
    check('preserved '+item['path'],ok)
pj=read(P/'B03_Release_Manifest.json')
check('B03 manifest47',len(pj['files'])==47)
for name,sha in pj['files'].items():
    q=P/name;ok=q.exists() and digest(q)==sha
    preserved.append(dict(path=str(q.relative_to(ROOT)),group='B03 frozen release',pass_check=ok))
    check('preserved B03 '+name,ok)
check('328 prior file comparisons',len(preserved)==328)
check('single frozen master',digest(ROOT/'Residential_Investment_Framework.md')=='1fbf607a78111bc007736fe0cc8109ad3967939a2dcc7ff54f017b491172e86b')
cov=read(P/'Coverage_Audit.json')
check('61 scope rows',len(cov['rows'])==61)
check('exact16 desk closures',{r['area_id'] for r in cov['rows'] if 'desk-complete' in r['completion']}=={f'A{i}' for i in range(18,34)})
check('programme still incomplete',not cov['programme_complete'] and not a['programme_complete'] and not f['programme_complete'] and f['deploy']==0)
over=read(P/'Case_Status_Overrides.json')
for cid in ['R216','R219']:
    check(cid+' effective eligibility hold',any(x['case_id']==cid and not x['eligible_for_residential_ranking'] for x in over['overrides']))
check('false Westside pair excluded',over['excluded_advertisements'][0]['advertisement_id']=='501228691' and not over['excluded_advertisements'][0]['financial_case_created'])

out=dict(version='KV-B04-2026-10-07-R3',status='PASS',check_count=len(checks),checks=checks,prior_file_comparisons=len(preserved),preservation=preserved,
    boundary='Arithmetical, structural and file-preservation verification; substantive coverage is an authored self-audit. No market-input authentication, investment approval or realised validation.')
(P/'B04_Release_Audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
files=[q for q in P.glob('B04_*') if q.is_file() and q.name!='B04_Release_Manifest.json']
files += [P/'build_b04_release.py',P/'build_b04_completion.py',P/'verify_b04_release.py']+raw
manifest=dict(release='KV-B04-2026-10-07-R3',boundary='B04 selected release and evidence. Current programme navigation and registers intentionally remain mutable. Earlier manifests unchanged.',files={q.relative_to(P).as_posix():digest(q) for q in sorted(set(files))})
(P/'B04_Release_Manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
assert (P/'B04_Release_Audit.json').exists() and (P/'B04_Release_Manifest.json').exists()
assert all(digest(P/name)==sha for name,sha in manifest['files'].items())
print(json.dumps(dict(status='PASS',checks=len(checks),financial_identity_rechecks=count,prior_files=328,manifest_files=len(manifest['files']),master_unchanged=True,desk_complete_areas=9,decision_ready=0,next_batch='B05',programme_complete=False),indent=2))
