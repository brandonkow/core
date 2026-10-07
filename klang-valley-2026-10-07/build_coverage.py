from pathlib import Path
import json,re,hashlib
ROOT=Path(__file__).resolve().parent
cases=json.loads((ROOT/'Case_Inputs.json').read_text(encoding='utf-8'))['cases']
regions=json.loads((ROOT/'Regional_Analysis.json').read_text(encoding='utf-8'))
prereg=(ROOT/'Programme_PreResearch_Lock.md').read_text(encoding='utf-8')
mapped=[]
for line in prereg.splitlines():
 if re.match(r'\| B0[1-8] ',line):
  cells=[x.strip() for x in line.split('|')[1:-1]]
  batch=cells[0].split()[0]
  for area in cells[1].split('; '): mapped.append(dict(batch=batch,catchment=area))
assert len(mapped)==61,len(mapped)
inherited={'Maluri–Cochrane':'C01 M Vertica','Shamelin–Pandan fringe':'C02 Shamelin Star','Midah–Mutiara–Taynton':'C03 EkoCheras',
'Connaught–Len Seng':'C04 Aster / C05 Maxim / adjoining C06 Riana',
'Alam Damai–Damai Perdana':'C06 Riana edge; Emerald Hills lifecycle lead',
'Batu 9–Suntex–Cuepacs':'C07 Green','Bandar Tun Hussein Onn':'C08 Windows large',
'Sungai Long':'C09 Scot Pine'}
lines=['# Regional scope, functional market map and coverage','',
'Cutoff: 7 October 2026. Sixty-one declared functional catchments grouped into eight batches. This is the launch map and first comparative sample. It is not a claim of comprehensive regional desk completion. Fourteen selected marketed expressions have conditional G0–G9 papers; many material micro-market and product segments remain unworked.','',
'## What the map means','',
'Catchments organise different possible household routines, not verified demographic shares or formal valuation boundaries. No suburb-wide quality score, aggregate appreciation forecast or median-PSF league table is issued. The two Cheras aliases and cross-boundary demand links stay canonical to B01; commercial and landed assets remain diagnostic, not silently added as investable candidates.','',
'Budget cells below are observed sampled asking-price envelopes, not population income bands or regional market boundaries. Bedroom labels remain advertised until original plans are checked. No observation of a low price establishes a bargain.','',
'## Eight batch assessments','']
for r in regions:
 ids=', '.join(c['id'] for c in cases if c['batch']==r['id'])
 lines += [f"### {r['id']} — {r['name']}",'',r['finding'],'',
 f"- Worked expressions: {ids}.",
 f"- Product/budget coverage: {r['segments']}",
 f"- Other examined leads: {r['screen']}",
 f"- Decision-changing gaps: {r['gaps']}",'',
 'Status: selected-expression conditional desk work; regional segment completion remains open. G9 is Defer for each worked expression. No negative area ranking follows from absent coverage.','']
lines += ['## Sixty-one catchment register','',
'“Mapped only” means geography and a research boundary, not investigated market evidence. Source-scanned batch does not promote each of its catchments to screened. Inherited B01 work is explicitly dated and uses the 7 October financial replay for current baseline; its old capital/financing conclusions are not copied as current.','',
'| Batch | Functional catchment | New G0–G9 expressions | Inherited work | Coverage consequence |',
'|---|---|---|---|---|']
for a in mapped:
 cc=[c for c in cases if c['batch']==a['batch'] and c['catchment']==a['catchment']]
 a['new_cases']=[c['id'] for c in cc]
 a['inherited']=inherited.get(a['catchment'],'None')
 a['status']='Selected expressions only' if cc else 'Inherited selective work only' if a['inherited']!='None' else 'Mapped only'
 implication='Original-plan/current-operations/clearing gaps; other budgets/lifecycles unworked' if cc else 'No fresh complete regional call; retain original evidence limits' if a['inherited']!='None' else 'No underwriting rank or negative quality inference'
 lines.append(f"| {a['batch']} | {a['catchment']} | {', '.join(a['new_cases']) or 'None'} | {a['inherited']} | {a['status']}: {implication} |")
lines += ['','## Lifecycle, role and omission controls','',
'| Dimension | Work actually covered | Important remaining gap / implication |',
'|---|---|---|',
'| Budget | Selected asks RM200k–850k; inherited larger Cheras case remains separately recorded | Not a complete low/middle/premium segmentation of each area; no conclusion about the best unsampled budget tier |',
'| Original bedrooms | One-, two- and three-bedroom marketed expressions; Akasa developer text identifies utility separately | Most approved parcel plans missing; studio partitions cannot be treated as genuine two-bedroom stock |',
'| Lifecycle | Mainly completed secondary stock; inherited Cheras VP/new-supply analysis retained | New launch, first-resale and transition phases outside Cheras largely not evaluated; no universal mature-stock preference |',
'| Distress | Auction leads encountered at Emerald, First Residence, Angkasa and Solstice and kept separate | No full possession/arrears/title/court/incentive diligence; no executable distressed purchase case |',
'| Investment role | Ordinary-income plus defensive household-exit hypotheses; premium and institutional-rental countercases | No validated recoverable mispricing or compounding thesis; no rebranding deficits as special situations |',
'| Operations | Source inconsistency checks and explicit current-management/works unknowns | No MC accounts, invoices, site/lift/noise/parking inspection; project quality not certified |',
'| Exit | Specific possible buyers and competing housing tasks; flat/lower/delayed sale arithmetic | No measured current buyer mix or unit-level time-to-sale; no price floor inferred from rent |',
'| Portfolio | Fourteen single-asset and 91 paired synthetic funding shocks | User mandate/capital and empirical dependence unknown; no actual capital allocation |','',
'## Next coverage tranche — no automatic scheduling','',
'1. Deepen current standard-positive household leads KV01/KV13/KV09 and the income-channel counterexample KV14 using available exact-unit evidence routes. PV21 first needs price-instrument resolution. Missing private/field evidence must remain missing.','',
'2. Fill the strongest sample-bias gaps: mature family stock in Kelana/SS2/PJ; Taman Desa/OUG/Bukit Jalil household alternatives; TTDI/Desa ParkCity/Bangsar South and Mont Kiara family stock at distinct budgets; ordinary Ampang/Wangsa stock. This can proceed independently of Red Team comments on current leads.','',
'3. Fill the broad western and outer coverage: Subang/USJ/Sunway, Shah Alam/Setia Alam/Klang, Kajang/Bangi/Putrajaya and growth corridors. Identify actual high-rise adoption, original household layouts and same-budget landed substitutes before selecting any apparent cheap winner.','',
'4. Complete launch/first-resale/distressed contrasts where they materially alter the actual buyer budget or supply mechanism. No forced case quota; absence of a viable high-rise product is a conclusion only after investigation.','',
'No unattended monitoring or future execution is created. Review dates are future evidence cutoffs when an active research pass actually occurs, not promises of background work.']
(ROOT/'Regional_Coverage.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(ROOT/'Coverage_Register.json').write_text(json.dumps(mapped,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(dict(catchments=len(mapped),new_worked_catchments=sum(bool(x['new_cases']) for x in mapped),
 inherited_only=sum(x['status']=='Inherited selective work only' for x in mapped),mapped_only=sum(x['status']=='Mapped only' for x in mapped)),indent=2))

