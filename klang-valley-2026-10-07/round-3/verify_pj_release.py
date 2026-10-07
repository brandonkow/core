"""Validate the bounded PJ release; file/arithmetical checks are not market validation."""
import hashlib,json,re
from pathlib import Path
P=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
audit=read(P/'B03_Completion_Audit.json');finance=read(P/'B03_Financial_Results.json')
checks=[]
def check(name,condition):
    checks.append(dict(name=name,pass_check=bool(condition)))
    assert condition,name
for f in audit['required_files']:check('output exists: '+f,(P/f).is_file() and (P/f).stat().st_size>100)
check('seven exact PJ catchments',{r['area_id'] for r in audit['rows']}=={f'A{i}' for i in range(18,25)})
check('49 substantive assessments',sum(len(r['dimensions']) for r in audit['rows'])==49)
check('no decision readiness',all(not r['decision_ready'] for r in audit['rows']))
check('fourteen financial expressions',len(finance['results'])==14)
check('unique case ids',len({r['case']['id'] for r in finance['results']})==14)
check('185 verified scenario evaluations',finance['financial_identity_checks']==185)
check('91 pair paths',len(finance['diagnostic_pairs'])==91)
check('rent grid reverses ranking',{r['coverage_leader'] for r in finance['rank_grid']}=={'R306','R308'})
paper=(P/'B03_Cases_G0_G9.md').read_text(encoding='utf-8')
for r in finance['results']:
    cid=r['case']['id']
    section=paper.split('## '+cid+' - ',1)[1].split('\n## ',1)[0]
    for gate in range(10):check(cid+' G'+str(gate),('| G'+str(gate)+' ') in section)
    check(cid+' stop/defer retained','STOP.' in section and '| G9 Capital Decision | Defer.' in section)
for c in read(P/'B03_Case_Inputs.json')['cases']:
    for raw in c['retrievals']:check(c['id']+' source raw'+raw,any((P/'raw').glob(raw+'_*.json')) or any((P/'raw').glob(raw+'*.json')))
for f in P.glob('B03_*.md'):
    text=f.read_text(encoding='utf-8')
    for target in re.findall(r'\]\(([^)]+)\)',text):
        if not target.startswith(('http:','https:')):
            target=target.strip('<>').split('#',1)[0]
            if target:check(f.name+' local link '+target,(f.parent/target).exists())
pres=read(P/'Preservation_Audit.json')
check('prior281checks preserved',pres['preservation_checks']==281 and not pres['failures'])
check('frozen master',pres['master_unchanged'])
cov=read(P/'Coverage_Audit.json')
check('61scope unchanged',len(cov['rows'])==61)
check('only seven desk closures',sum('desk-complete' in r['completion'] for r in cov['rows'])==7)
check('programme incomplete',not cov['programme_complete'])
out=dict(version='KV-PJ-2026-10-07-R3',status='PASS',checks=checks,check_count=len(checks),
         boundary='Structural integrity, arithmetic and authored coverage self-audit only; no input authenticity, legal clearance, investment approval or realised validation.')
files=list(P.glob('B03_*'))+[P/'build_pj_release.py',P/'verify_pj_release.py',P/'PJ_RESUME_CHECKPOINT.md']
files=[p for p in files if p.is_file() and p.name!='B03_Release_Manifest.json']
files += [p for p in (P/'raw').glob('*.json') if 48<=int(p.name[:3])<=78]
files += [P/'sources/PJ_Midtown_Archived_Flyer.pdf',P/'sources/pjmidtown-plan.png']
check('source files exist',all(p.exists() for p in files))
out['check_count']=len(checks)
(P/'B03_Release_Audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
manifest=dict(release='KV-PJ-2026-10-07-R3',boundary='Selected PJ release and evidence; does not overwrite prior manifests.',
              files={p.relative_to(P).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(files))})
(P/'B03_Release_Manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(status='PASS',checks=len(checks),manifest_files=len(manifest['files']),master_unchanged=True,programme_complete=False),indent=2))
