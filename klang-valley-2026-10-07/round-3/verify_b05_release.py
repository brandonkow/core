"""B05 arithmetic, record structure and preservation checks; not market validation."""
import json,hashlib,importlib.util,itertools,gzip,re
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,condition):
 checks.append(dict(name=name,pass_check=bool(condition)))
 assert condition,name
f=read(P/'B05_Financial_Results.json');a=read(P/'B05_Completion_Audit.json')
check('16 unique expressions',len(f['results'])==len({r['case']['id'] for r in f['results']})==16)
check('nine new and seven inherited',len(read(P/'B05_Case_Inputs.json')['cases'])==9 and len(read(P/'B05_Inherited_Assessments.json'))==7)
check('seven catchments', {r['area_id'] for r in a['rows']}=={f'A{i}' for i in range(34,41)})
check('49 authored dimensions',sum(len(r['dimensions']) for r in a['rows'])==49)
check('bounded Defer only',all(r['desk_complete'] and not r['decision_ready'] and r['g9']=='Defer' for r in a['rows']))
for name in a['required_files']:check('output '+name,(P/name).is_file() and (P/name).stat().st_size>100)
spec=importlib.util.spec_from_file_location('frozen',ROOT/'execution-release-2026-10-07/financial_engine.py')
e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
check('frozen configuration',f['config']==e.CFG)
by={};count=0
for row in f['results']:
 c=row['case'];sc={}
 check(c['id']+' parameter/scenario coverage',set(row['scenario_parameters'])==set(row['scenarios']))
 for name,params in row['scenario_parameters'].items():
  b=e.evaluate(c,**params);e.check_financial_identities(b,c,params.get('exit_extra_cost',0));count+=1
  saved={k:v for k,v in b.items() if k not in ['schedule','cash_path']}
  check(c['id']+' saved metrics '+name,saved==row['scenarios'][name])
  sc[name]=b
 b=sc['base'];by[c['id']]=dict(case=c,scenarios=sc)
 check(c['id']+'90/4/35',abs(b['actual_instalment']-e.payment(.9*c['price'],.04,35))<.001)
 check(c['id']+' independent annual carry',abs(b['cashflow_by_year'][0]-(11*c['rent_assumed']-12*(b['actual_instalment']+c['fee_assumed']+c['other_assumed'])))<.001)
 check(c['id']+' standard and6%boundary',abs(row['boundaries']['standard_price']-(c['rent_assumed']-c['fee_assumed'])/e.payment(.9,.04,35))<.001 and row['boundaries']['gross6_price']==200*c['rent_assumed'])
 check(c['id']+' futurebuyer90LTV',abs(row['future_buyer_90_5_5_25']-e.payment(.9*b['terminal_nominal_breakeven'],.055,25))<.001)
for t in f['alternatives']:
 c=dict(by[t['id']]['case'],**t['change']);b=e.evaluate(c);e.check_financial_identities(b,c);count+=1
 check(t['id']+' alternative metrics',c==t['case'] and {k:v for k,v in b.items() if k not in ['schedule','cash_path']}==t['result'])
check('212 financial identity replays',count==f['financial_identity_checks']==212)
check('120 unique pairs',len(f['diagnostic_pairs'])==120 and {tuple(sorted(t['ids'])) for t in f['diagnostic_pairs']}==set(itertools.combinations(sorted(by),2)))
for t in f['diagnostic_pairs']:
 x,y=(by[i]['scenarios']['combined12'] for i in t['ids'])
 path=[e.CFG['synthetic_cash']-x['entry_cash']-y['entry_cash']]
 for u,v in zip(x['schedule'],y['schedule']):path.append(path[-1]+u['cashflow']+v['cashflow'])
 check('pair '+','.join(t['ids']),path==t['cash_path'] and min(path)==t['minimum_cash'] and t['reserve_pass']==(min(path)>=e.CFG['synthetic_protected_reserve']) and not t['coexisting_units_verified'])
check('68 reserve diagnostics',sum(t['reserve_pass'] for t in f['diagnostic_pairs'])==68)
check('nine rentgrid reversals',len(f['rank_grid'])==9 and {t['leader'] for t in f['rank_grid']}=={'R321','R328'})
for t in f['rank_grid']:
 x=e.evaluate(dict(by['R321']['case'],rent_assumed=t['parkview_rent']));y=e.evaluate(dict(by['R328']['case'],rent_assumed=t['titiwangsa_rent']))
 check('rank '+str((t['parkview_rent'],t['titiwangsa_rent'])),t['parkview_balance']==x['standard_monthly_balance'] and t['titiwangsa_balance']==y['standard_monthly_balance'])
check('only Parkview positive annual base',[k for k,v in by.items() if v['scenarios']['base']['cashflow_by_year'][0]>0]==['R321'])
check('all base flat-exit total profits negative',all(v['scenarios']['base']['profit_by_exit_multiple']['1']<0 for v in by.values()))
check('monthlyfee branch and quarterlyhypothesis',by['R322']['case']['fee_assumed']==1165 and next(t for t in f['alternatives'] if t['id']=='R322')['case']['fee_assumed']==1165/3)
check('tenancy uncertainty modelled','existing_lease_no_credit6' in by['R328']['scenarios'])
check('separate lower offer',by['R225']['case']['price']==380000 and by['R329']['case']['price']==280000 and by['R329']['case']['refurb_assumed']==25000)
check('SeriMaya fresh vs historical price separated',by['R325']['case']['price']==650000 and next(t for t in f['alternatives'] if t['id']=='R325')['case']['price']==530000)
paper=(P/'B05_Cases_G0_G9.md').read_text(encoding='utf-8')
for cid in by:
 section=paper.split('## '+cid+' - ',1)[1].split('\n## ',1)[0]
 for gate in range(10):check(cid+' G'+str(gate),('| G'+str(gate)+' ') in section)
 check(cid+' stop/defer/counter','STOP.' in section and '| G9 Capital Decision | Defer.' in section and 'Strongest counter-thesis / falsification:' in section and 'Finite evidence / reopening:' in section)
div=(P/'B05_Divergence_and_Misses.md').read_text(encoding='utf-8')
check('six material flags',div.count('**⚠ DIVERGENCE FLAG**')==6)
for field in ['Data limitation','Judgment bias','Omitted variable','Structural change','Falsifiable Hypothesis','Evidence Required','Falsification Conditions','Core Module Routing','Current Status']:
 check('six fields '+field,div.count('**'+field)==6)
raw=sorted((P/'b05-raw').glob('*.json.gz'));content_hashes={}
check('50 consecutive retained retrievals',len(raw)==50 and {int(q.name[:3]) for q in raw}==set(range(1,51)))
for q in raw:
 b=gzip.decompress(q.read_bytes());json.loads(b)
 content_hashes[q.relative_to(P).as_posix()]=hashlib.sha256(b).hexdigest()
for c in read(P/'B05_Case_Inputs.json')['cases']:
 for rid in c['retrievals']:check(c['id']+' raw'+rid,any((P/'b05-raw').glob(rid+'*.json.gz')))
for md in P.glob('B05_*.md'):
 for target in re.findall(r'\]\(([^)]+)\)',md.read_text(encoding='utf-8')):
  if target.startswith(('https:','http:')):continue
  target=target.strip('<>').split('#',1)[0]
  if not target or target in ['B05_Release_Audit.json','B05_Release_Manifest.json']:continue
  check(md.name+' link '+target,(md.parent/target).is_file())
pres=read(P/'Preservation_Audit.json');preserved=[]
check('prior281register valid',pres['preservation_checks']==281 and not pres['failures'])
for item in pres['checks']:
 ok=digest(ROOT/item['path'])==item['expected']
 check('preserved '+item['path'],ok);preserved.append(dict(path=item['path'],pass_check=ok))
for release,expected in [('B03',47),('B04',56)]:
 m=read(P/(release+'_Release_Manifest.json'));check(release+' expected manifest size',len(m['files'])==expected)
 for name,sha in m['files'].items():
  ok=digest(P/name)==sha;check('preserved '+release+' '+name,ok)
  preserved.append(dict(path=str((P/name).relative_to(ROOT)),pass_check=ok))
check('384 prior comparisons',len(preserved)==384)
check('master frozen',digest(ROOT/'Residential_Investment_Framework.md')=='1fbf607a78111bc007736fe0cc8109ad3967939a2dcc7ff54f017b491172e86b')
cov=read(P/'Coverage_Audit.json')
check('61 scope rows,23 bounded closures',len(cov['rows'])==61 and {r['area_id'] for r in cov['rows'] if 'desk-complete' in r['completion']}=={f'A{i}' for i in range(18,41)})
check('programme incomplete/no deploy',not cov['programme_complete'] and not f['programme_complete'] and not a['programme_complete'] and f['deploy']==0)
over=read(P/'Case_Status_Overrides.json')
for cid in ['R225','R329','R322','R321','R328']:
 check(cid+' current hold',any(t['case_id']==cid and not t['eligible_for_residential_ranking'] for t in over['overrides']))
check('TRX falseidentity excluded',any(t['advertisement_id']=='501960003' and not t['financial_case_created'] for t in over['excluded_advertisements']))
audit=dict(version='KV-B05-2026-10-07-R3',status='PASS',check_count=len(checks),financial_identity_rechecks=count,checks=checks,prior_file_comparisons=len(preserved),preservation=preserved,
 boundary='Arithmetic, recorded structure and prior-content verification; substantive review is an authored self-audit, not authentication of market inputs or investment validation.')
(P/'B05_Release_Audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
files=[q for q in P.glob('B05_*') if q.is_file() and q.name!='B05_Release_Manifest.json']
files += [P/'build_b05_release.py',P/'build_b05_completion.py',P/'verify_b05_release.py']+raw
manifest=dict(release='KV-B05-2026-10-07-R3',boundary='B05 research release; current navigation/registers mutable. Prior releases unchanged. Individual monthly schedules reproducible from stored parameters; raw evidence gzip is lossless.',files={q.relative_to(P).as_posix():digest(q) for q in sorted(set(files))},raw_uncompressed_sha256=content_hashes)
(P/'B05_Release_Manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
assert all(digest(P/name)==sha for name,sha in manifest['files'].items())
print(json.dumps(dict(status='PASS',checks=len(checks),financial_replays=count,prior_files=384,manifest_files=len(manifest['files']),master_unchanged=True,next_batch='B06',programme_complete=False),indent=2))

