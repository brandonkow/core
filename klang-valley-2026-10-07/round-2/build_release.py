"""Build the bounded desk release. Import the approved financial engine unchanged."""
from pathlib import Path
import json, re, hashlib, itertools, importlib.util
ROOT=Path(__file__).resolve().parent
P=ROOT.parent; PROJECT=P.parent
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def save(name,obj): (ROOT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def md(name,lines): (ROOT/name).write_text('\n'.join(lines)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def money(n): return f'{n:,.0f}'
def link(p,label=None): return f'[{label or p.name}](<{p.resolve().as_posix()}>)'
MASTER_HASH='1fbf607a78111bc007736fe0cc8109ad3967939a2dcc7ff54f017b491172e86b'
assert sha(PROJECT/'Residential_Investment_Framework.md')==MASTER_HASH
original=read(P/'Coverage_Register.json')
raw={p.name[:3]:p for p in (ROOT/'raw').glob('*.json')}
sources=[]
for k,p in sorted(raw.items()):
    text=read(p)
    for n,m in enumerate(re.finditer(r'(?m)^([^\n]+) \((https?://[^\n]+)\)\n([^\n]+)',text),1):
        header=m.group(3)
        tail=text[m.end():m.end()+9000]
        dates=list(dict.fromkeys(re.findall(r'(?:Listed on|Disenaraikan pada)\s+([^\n|]+)',tail)))[:5]
        sources.append(dict(id=f'S{k}-{n:02}',retrieval=k,title=m.group(1),url=m.group(2),
          header=header,listed_date_strings=dates,retrieved='2026-10-07',
          status='Retrieved search/open extract; inclusion in index does not mean adopted as evidence',
          raw_file=p.name))
save('Source_Index.json',sources)
lines=['# Retrieval and source index','',
 'Cutoff and retrieval: 7 October 2026. The original returned search/open excerpts are archived in raw/. This index includes rejected, duplicate and irrelevant hits; only explicit case claims and the investigation ledger adopt evidence. Search snippets are weaker than an opened exact advertisement. Multiple agents, translations, related portals or duplicated text do not establish independent units or achieved deals. Relative crawl labels and page titles are not transaction dates. Publication/listed dates are kept in raw; missing dates remain unknown. No images, visits, tenancy contracts, titles, lender records or MC accounts were verified.','']
for k,p in sorted(raw.items()):
    lines += [f'## Retrieval {k}: {p.stem[4:]}','',link(p,'Archived retrieval'), '']
    for x in [a for a in sources if a['retrieval']==k]:
        date_meta=re.search(r'(?:Published:|Crawled:).*?(?=; [^;]*#|; Content type:|; Image:|; [A-Z]|$)',x['header'])
        lines.append(f"- {x['id']}: [Original source]({x['url']}). Retrieval date 7 October 2026; source-specific dates retained in the archived extract.")
    lines.append('')
md('Source_Index.md',lines)
areas={}
for line in (ROOT/'Area_Research_Inputs.txt').read_text(encoding='utf-8').splitlines():
    idx,task,comps,counter,gaps=line.split('|')
    i=int(idx); old=original[i-1]
    areas[i]=dict(id=f'A{i:02}',index=i,batch=old['batch'],catchment=old['catchment'],
      demand_hypothesis=task,substitution_test=comps,counter_thesis=counter,
      material_segment_gaps=gaps,inherited=old['inherited'],r1_cases=old['new_cases'],r2_cases=[])
cases=[]
quarantine={'R208':'Component/area/furnishing identity unresolved; 12% headline is not an admitted residential opportunity',
 'R216':'Exact 250k sale URL redirects to the project index on reopening; continued unit availability unconfirmed',
 'R219':'Price freshness unresolved after opening an older index snapshot; do not promote positive arithmetic',
 'R226':'Conflicting effective sale price; higher header/body scenario does not cure G0',
 'R229':'SOVO versus residential component unresolved',
 'R237':'SOHO permitted use/financeability not verified; conditional arithmetic only',
 'R248':'Original studio/1BR parcel and indexed sale/rent identity still need reconciliation'}
for line in (ROOT/'Case_Research_Inputs.txt').read_text(encoding='utf-8').splitlines():
    row=line.split('|')
    assert len(row)==16,(len(row),row)
    num,ai,name,sqft,layout,p,r,lo,hi,f,o,w,refs,match,thesis,risk=row
    a=areas[int(ai)]; cid='R2'+num
    c=dict(id=cid,area_id=a['id'],batch=a['batch'],catchment=a['catchment'],name=name,
      sqft=int(sqft),layout=layout,price=int(p),rent_assumed=int(r),rent_low=int(lo),rent_high=int(hi),
      fee_assumed=int(f),other_assumed=int(o),refurb_assumed=int(w),retrievals=refs.split(','),
      match=match,thesis=thesis,decisive_risk=risk,
      price_status='Advertised/indexed amount for conditional analysis, not confirmed effective consideration',
      rent_status='Working long-term whole-unit scenario informed by asking evidence; not achieved rent',
      fee_status='Unverified combined management/sinking proxy, not a verified management-only bill',
      cost_status='Analyst planning allowances; tax and specific cost quotes missing',
      g0='STOP: no defensible unit-matched normalised clearing interval',
      g9='Defer',quarantine=quarantine.get(cid),unit_identity='Tower/floor/unit/title/plan not obtained')
    if cid in ('R201','R216','R234'): c['retrievals'].append('124')
    if cid=='R216': c['match']+='; direct recheck redirects to project search, so250k remains a historical/indexed lead'
    if cid=='R204':
        c['retrievals'].append('125')
        c['decisive_risk']+='; a social-media retail-anchor closure lead was not established by the official-site search and remains unverified, so no assured anchor continuity or closure is assumed'
    assert all(k in raw for k in c['retrievals'])
    cases.append(c);a['r2_cases'].append(cid)
save('Case_Inputs.json',dict(version='KV-REG-2026-10-07-R2',cutoff='2026-10-07',cases=cases,
 assumptions='Every price/rent is conditional. No unchanged advertisement implies continued availability. All rent endpoints are scenarios, not confidence intervals.'))
save('Coverage_Register.json',list(areas.values()))
engine=PROJECT/'execution-release-2026-10-07'/'financial_engine.py'
spec=importlib.util.spec_from_file_location('frozen_engine',engine)
eng=importlib.util.module_from_spec(spec);spec.loader.exec_module(eng)
scenarios={'rate_5_5pct':dict(rate=.055),'rent_down20':dict(rent_factor=.8),
 'fee_up20':dict(fee_factor=1.2),'zero_rent_first12':dict(initial_vacancy=12),
 'levy30k_month24':dict(levy_month=24,levy=30000),'bank_value_down15':dict(valuation_ratio=.85),
 'loan_term25':dict(term=25),'exit_delay12':dict(months=72),
 'unquoted_cost_buffer':dict(annual_extra_cost=1200,exit_extra_cost=5000)}
factor=eng.payment(.9,.04,35)
base=[];sensitivity=[];stress=[];grid=[]
for c in cases:
    b=eng.evaluate(c);eng.check_financial_identities(b,c)
    b.update(area_id=c['area_id'],g9='Defer',quarantine=c['quarantine'],
       standard_cover_price=(c['rent_assumed']-c['fee_assumed'])/factor,
       gross6_price=c['rent_assumed']*200,
       standard_required_rent=b['standard_instalment']+c['fee_assumed'],
       annual_carry_neutral_rent=12*(b['standard_instalment']+c['fee_assumed']+c['other_assumed'])/11)
    b['priority']='Lowest: current standard shortfall' if b['current_shortfall'] else (
       'Identity/freshness hold' if c['quarantine'] else 'Next evidence: conditional coverage')
    base.append(b)
    assert abs(eng.evaluate(dict(c,price=b['standard_cover_price']))['standard_monthly_balance'])<.01
    assert abs(eng.evaluate(dict(c,rent_assumed=b['annual_carry_neutral_rent']))['cashflow_by_year'][0])<.01
    for label,kw in scenarios.items():
        r=eng.evaluate(c,**kw);eng.check_financial_identities(r,c,kw.get('exit_extra_cost',0))
        if label not in ('bank_value_down15','loan_term25','exit_delay12'):
            assert r['terminal_nominal_breakeven']>b['terminal_nominal_breakeven']
        r={k:v for k,v in r.items() if k not in ('schedule','cash_path')};r['scenario']=label
        sensitivity.append(r)
    sh=eng.evaluate(c,months=12,rate=.055,rent_factor=.8,first_year_paid=6,levy_month=1,levy=30000)
    eng.check_financial_identities(sh,c);stress.append(sh)
    for rent,ff in itertools.product((c['rent_low'],c['rent_assumed'],c['rent_high']),(.8,1,1.2)):
        cc=dict(c,rent_assumed=rent,fee_assumed=c['fee_assumed']*ff)
        rr=eng.evaluate(cc);eng.check_financial_identities(rr,cc)
        grid.append(dict(id=c['id'],rent=rent,fee=cc['fee_assumed'],
          standard_balance=rr['standard_monthly_balance'],annual_cf=rr['cashflow_by_year'][0]))
r1=read(P/'Financial_Results.json')
allstress=r1['combined_stress']+stress
pairs=[]
for a,b in itertools.combinations(allstress,2):
    path=[500000-a['entry_cash']-b['entry_cash']]
    for x,y in zip(a['schedule'],b['schedule']):path.append(path[-1]+x['cashflow']+y['cashflow'])
    pairs.append(dict(ids=[a['id'],b['id']],minimum_cash=min(path),reserve_pass=min(path)>=150000,cash_path=path))
save('Financial_Results.json',dict(version='KV-REG-2026-10-07-R2',config=eng.CFG,
 engine_sha256=sha(engine),base=base,sensitivities=sensitivity,combined_stress=stress,
 rank_grid=grid,pairs_including_r1=pairs,r1_basis='Unchanged 14 cases; not freshly verified in this round'))
B={b['id']:b for b in base};C={c['id']:c for c in cases}
r1c={c['id']:c for c in read(P/'Case_Inputs.json')['cases']}
r1b={b['id']:b for b in r1['base']}
base_note='90% of purchase price, 4% annual interest, 35 years; 5-year hold; 11 collected months/year and no rent or price growth. Full instalments, fee proxy and other operating allowance included. Acquisition allowance5%, disposal3%, initial works as stated. Pre-tax; transaction-specific taxes, duties, finance charges, reliefs, major works and actual invoices remain unquoted. Extra-cost stress is a buffer, not a tax estimate. 8% return hurdle and RM500k cash/RM150k reserve are inherited illustrations, not user targets or actual finances.'
assump='Fees scale by broad size/service intensity only: they are not bills. Other monthly allowances cover a working provision for routine insurance/assessment/repairs/reletting; actual costs and overlap need a unit schedule. Fit-out/refresh is a working upfront allowance, not a contractor quote. Rent-low/high endpoints mix advertised counterexamples and analyst stress bounds as disclosed per case; no probability interpretation.'
lines=['# Financial underwriting — second desk round','',base_note,'',assump,'',
 'Standard balance is full quoted-month rent minus the standard instalment minus combined fee proxy. It is not annual net cashflow. The user standard specifically includes management; sinking is retained as a conservative combined proxy until disaggregated. Every calculation remains conditional and every case G9 Defer.','',
 '| Case | Price | Rent | Fee | Other/mo | Works | Gross | Standard/mo | Annual carry | Priority |',
 '|---|---:|---:|---:|---:|---:|---:|---:|---:|---|']
for c,b in zip(cases,base):
    lines.append(f"| {c['id']} {c['name']} | {money(c['price'])} | {money(c['rent_assumed'])} | {money(c['fee_assumed'])} | {money(c['other_assumed'])} | {money(c['refurb_assumed'])} | {b['gross_yield']:.2%} | {b['standard_monthly_balance']:+,.0f} | {b['cashflow_by_year'][0]:+,.0f} | {b['priority']} |")
lines+=['','## Mechanical thresholds, not valuations, bids or forecasts','',
 '| Case | 6% gross price | Standard-cover price | Rent for standard | Rent for annual neutrality | Entry cash | Year5 debt | Break-even exit | 8% hurdle exit | Flat exit profit | -20% exit profit |',
 '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
for b in base:
    lines.append('| '+b['id']+' | '+' | '.join(money(b[k]) for k in ('gross6_price','standard_cover_price','standard_required_rent','annual_carry_neutral_rent','entry_cash','terminal_debt','terminal_nominal_breakeven','terminal_8pct_required'))+f" | {b['profit_by_exit_multiple']['1']:+,.0f} | {b['profit_by_exit_multiple']['0.8']:+,.0f} |")
lines+=['','Unknown G0 clearing value means no validated margin of safety or recoverable discount. Unresolved divergence requires a larger eventual evidence-supported safety margin; these formulas do not supply it. Lower rent or higher expenses lowers the affordable entry threshold, even if the location thesis survives.','',
 '## Current-shortfall transition records','',
 'Each negative row remains lowest research priority. Its numeric rent hurdle is above; crossing it requires independently evidenced repeatable whole-unit collections, actual fees and funded fit-out, or a confirmed lower effective entry. Catalyst claims need an operational event, a route to this tenant/buyer pool and observed transmission. A planned station, announced mall or rising project average alone cannot reopen the case. No uplift is included in base. See case-specific falsifiers in workpapers.','',
 '## Full sensitivity register','',
 '| Case | Scenario | Entry cash | Break-even exit | Total carry | Flat-price profit |',
 '|---|---|---:|---:|---:|---:|']
for x in sensitivity:lines.append(f"| {x['id']} | {x['scenario']} | {money(x['entry_cash'])} | {money(x['terminal_nominal_breakeven'])} | {x['cashflow_total']:+,.0f} | {x['profit_by_exit_multiple']['1']:+,.0f} |")
lines+=['','## Forced hold, financing and correlation','',
 'Simultaneous rate5.5%, rent-20%, six unpaid months initially, RM30k levy per property immediately, no sale for12months. Minimum cash path is tested without salary, refinance or emergency disposal. Bank valuation-15% separately finances90% of the reduced valuation; it does not change the purchase-price standard.25-year actual-credit sensitivity and72-month exit delay remain separate.',
 '',f"{sum(x['reserve_pass'] for x in pairs)} of {len(pairs)} pairs across the unchanged14 R1 plus50 R2 expressions preserve the synthetic reserve. This is scenario funding capacity only; identity-quarantined assets are included for arithmetic and are not eligible portfolio choices. The9 older Cheras expressions are not included in this64-case pair count.",
 '',
 'Geographic spread is not independence. Compact investor suites share credit, landlord-exit and furnishing risks; campus/airport demand adds anchor concentration; family townships share landed substitution; premium central units share high-equity buyer and new-supply exposure. Real tenant/employer/income and liability overlap are unknown. Repeated units of a project or connected economic anchors cannot be treated as diversification.','',
 'All schedules, future buyer payments at required exits,450 sensitivities,450 rent/fee grid points and pair cash paths are in Financial_Results.json. Required exit prices are burdens, not supported floors or ceilings. Actual buyer equity/DSR, lender appetite and voluntary resale depth remain unverified.']
md('Financial_Underwriting.md',lines)
(ROOT/'cases').mkdir(exist_ok=True)
for c,b in zip(cases,base):
    a=areas[int(c['area_id'][1:])]
    compact=not c['layout'].startswith('3') and c['sqft']<950
    primary='Local working single/couple or small household choosing this exact usable layout' if compact else 'Local family choosing usable rooms, parking and daily routines'
    secondary='A yield-led investor only if independently verified rent and a surviving non-investor exit support the price'
    false='Large school-oriented family demand and all tenants in the broader district' if compact else 'All nearby households regardless of total budget, household size or preference for landed'
    refs='; '.join(link(raw[k],k+' '+raw[k].stem[4:]) for k in c['retrievals'])
    lines=[f"# {c['id']} — {c['name']}",'',f"Cutoff7October2026. {a['id']} {a['catchment']}; {c['sqft']}sf; {c['layout']}. Conditional marketed expression, not a verified executable unit. Tower/unit, approved plan, rights, bays and legal use remain unverified unless a narrower advertisement claim is explicitly stated.",'',
      f"Master SHA256: {MASTER_HASH}. SOP KV-EXEC-2026-10-07; financial KV-FIN-90-4-35-v1. Role tested: ordinary income / practical use; compounding or special-situation recovery not established.",'',
      '## Evidence and comparison boundary','',
      f"Observed advertisement/index amount used: RM{money(c['price'])}; rent scenario RM{money(c['rent_assumed'])}/month. {c['match']}. These are asking/claimed values, not clearing prices or collected rent.",
      '',f"Source path: {refs}. The "+link(ROOT/'Source_Index.md','source index')+" links the original pages and keeps source dates/lineage. Repeated advertisements and translated copies are not independent observations.",
      '',f"Interpretation, not established fact: {c['thesis']}.",
      '',f"Comparison: {a['substitution_test']}. Inclusion is functional/budget diagnosis. No fixed size, furnishing, parking or rights adjustment is invented. No normalised clearing interval is justified. {c['decisive_risk']}.",
      '',f"Identity/freshness hold: {c['quarantine'] or 'No additional quarantine beyond universal G0 and exact-unit gaps; this is not legal/title clearance.'}",'',
      '## G0–G9: original gates, stops retained','',
      '| Gate | Conditional finding and consequence |','|---|---|',
      '| G0 Reference-Price Validity | STOP. Asking/index evidence and unmatched condition cannot bound normalised clearing value. No undervaluation or recoverable-discount claim. |',
      f"| G1 Market Mechanism | Hypothesis: {a['demand_hypothesis']}. Rival: {a['counter_thesis']}. No assumed catalyst uplift. |",
      f"| G2 Buyer Universe | Primary: {primary}. Secondary: {secondary}. False borrowed buyer: {false}. Same-weekend test: {a['substitution_test']}. Buyer-pool transfer remains unproved without actual motive/credit evidence. |",
      f"| G3 Project Quality | {c['decisive_risk']}. Amenity descriptions are marketing, not operating performance. No MC accounts, arrears, lift/service records or competing-stock absorption obtained; cannot score governance healthy or failed. |",
      f"| G4 Unit Quality | {c['match']}. Exact plan, light/noise/privacy, lift/parking circulation, external adjacency and irreversible penalties uninspected; project averages cannot settle unit quality. |",
      '| G5 Price / Mispricing | Not adjudicated: G0–G4 prerequisites do not survive on current evidence. Mechanical rent/price thresholds are diagnostics, not value. |',
      f"| G6 Exit Architecture | Primary eventual buyer: {primary}. Same-weekend substitutes above define a test, not an exit guarantee. Investor exit conditional on genuine cash rent; extending the hold is capital use, not a sale exit. No validated floor, ceiling, sale velocity or independent exit redundancy. Single-point exit risk remains if only another investor/catalyst can pay the required quantum. |",
      f"| G7 Financing / Terminal Risk | Standard90/4/35 calculated; actual title, remaining lease, valuation, buyer eligibility and lender terms unknown. Correlated12-month hold model minimum cash RM{money(next(s['minimum_cash'] for s in stress if s['id']==c['id']))} under syntheticRM500k starting cash. No management-severity grade assigned from absence of records. |",
      '| G8 Portfolio / Opportunity Cost | Actual investor cash, liabilities and DSR not supplied; synthetic capacity is not approval. Compare no purchase, the other conditional candidates and shared tenant/strata/credit exposure. No forced allocation or assumed diversification. |',
      '| G9 Capital Decision | Defer. Price, identity and operating evidence are not decision-ready; current shortfall alone is not a structural Reject. |',
      '', '## Financial chain', '',base_note,'',assump,'',
      f"Inputs: feeRM{money(c['fee_assumed'])}/month; otherRM{money(c['other_assumed'])}/month; worksRM{money(c['refurb_assumed'])}. Standard instalmentRM{money(b['standard_instalment'])}; gross{b['gross_yield']:.2%}; standard balance{b['standard_monthly_balance']:+,.0f}/month; annual carry{b['cashflow_by_year'][0]:+,.0f}.",
      '',f"Entry cashRM{money(b['entry_cash'])}; year5debtRM{money(b['terminal_debt'])}; nominal break-even saleRM{money(b['terminal_nominal_breakeven'])}; illustrative8% hurdle exitRM{money(b['terminal_8pct_required'])}. At a flat sale price total pre-tax profit is RM{b['profit_by_exit_multiple']['1']:+,.0f}; at20%lower exit it is RM{b['profit_by_exit_multiple']['0.8']:+,.0f}.",
      '',f"Future buyer payment at nominal break-even: standardRM{money(b['future_buyer_standard_payment_at_breakeven'])}/month; independent80%/5.5%/25-year stressRM{money(b['future_buyer_stress_payment_at_breakeven'])}/month plus greater equity. Neither establishes buyer ability or willingness to pay.",
      '',f"Mechanical price for6%grossRM{money(b['gross6_price'])}; standard coverageRM{money(b['standard_cover_price'])}. Rent required for standard coverageRM{money(b['standard_required_rent'])}; for11-month annual carry neutralityRM{money(b['annual_carry_neutral_rent'])}. These are burdens, not forecasts or bids.",
      '', '## Four conclusions and falsification','',
      f"- Product quality: ungraded; use hypothesis is {a['demand_hypothesis']}. Exact operations and unit inspection could reverse preference.",
      f"- Investment at stated price: {'current proxy standard shortfall' if b['current_shortfall'] else 'conditional standard coverage only'}; no validated safety margin. Gross yield is not total return.",
      f"- Research priority: {b['priority']}.",
      '- G9: Defer; no matured investment outcome or predictive-validation hit.',
      '',f"Rent/fee grid: rentRM{money(c['rent_low'])}/{money(c['rent_assumed'])}/{money(c['rent_high'])}, fee80/100/120% of proxy. Standard balance ranges from RM{min(x['standard_balance'] for x in grid if x['id']==c['id']):+,.0f} to RM{max(x['standard_balance'] for x in grid if x['id']==c['id']):+,.0f}. These are stress bounds, not likelihoods. Approval cannot be inferred even if all grid points cover.",
      '',f"Strongest rival explanation: {a['counter_thesis']}. Falsify the use/income hypothesis if authenticated whole-unit rents net of recurring concessions cannot meet the stated coverage hurdle at an attainable entry, if real buyers consistently choose the named substitutes, or if the decisive risk proves structurally unfixable. Persistent unknowns do not count as falsification or validation.",
      '', '## Three immediate evidence questions and bounded closeout','',
      f"1. Is this exact parcel, original plan and effective consideration what the advertisement implies? Public attempt: the linked price/rental and component searches. Obtained: the disclosed claims and inconsistencies. Remaining route: authenticated title/SPA/approved plan and independent matched voluntary transfers with incentives/condition. Recheck on any new exact-unit offer; without them retain G0STOP.",
      f"2. Does sustainable ordinary rent cover costs for this condition? Public attempt: listed counterpart and contrary rental evidence. Obtained: asking bounds, not leases. Remaining route: recent comparable signed leases/collection history, dated management/sinking bill and fit-out quote. Before any promotion, repeat the model at those inputs; if belowRM{money(b['standard_required_rent'])} with fee unchanged, keep lowest research tier.",
      f"3. Can the relevant end user live here and exit without a single buyer/catalyst? Public comparison: {a['substitution_test']}. Remaining route: physical routine/parking/lift/noise inspection, MC financials/major-works schedule, actual buyer/lender evidence. On structural failure use existingReject; if merely absent retainDefer.",
      '', 'Work-queue disposition: close this finite public pass; reopen manually on exact evidence above or a material market event. No scheduled monitoring, contact or paid records commissioned. An unresolved divergence raises the proof/safety-margin burden and lowers conviction; no arbitrary extra discount percentage substitutes for evidence.',
      '',link(ROOT/'Divergence_and_Misses.md','Material flags and misses')+'. Unknowns alone are not a material conflicting polarity; apply only the listed relevant flags.']
    md('cases/'+c['id']+'.md',lines)

batch_names={x['id']:x['name'] for x in read(P/'Regional_Analysis.json')}
findings={
'B01':'Compact Shamelin/Emerald/ Landmarks widen the inherited Cheras sample but do not defeat the larger-unit alternatives on verified value. The key unresolved contest is household use versus total-budget landed substitution. No family preference is hard-coded into screening.',
'B02':'Kuchai family and Endah/Aurora compact expressions can cover the standard on assumed rent; OUG and Desa Green sit near the sign boundary. Their thin surpluses disappear on annual-cost treatment. Trion rent is a seller claim. Selection should turn on authenticated rent/operations and practical routine, not lowest PSF.',
'B03':'Established PJ utility does not translate automatically to income coverage. PJ8 is a conditional small-unit challenger; Sterling and Ken have larger gaps at selected prices. Centrestage looks best arithmetically only before its component and price identity are reconciled, so it is quarantined.',
'B04':'Premium owner utility and income value diverge. Sinaran/DC/Westside/Menjalara need better entry or rent evidence; that does not prove poor products. Cliveden and Neo have attractive compact arithmetic but their low-price freshness failed rechecks. R1 First Residence and OOAK retain their original evidence limits.',
'B05':'Central employment, retail and rail can coexist with inadequate income economics at the selected asks. TRX and Vortex cannot rely on tourist income or project prestige to supply an exit. Datum compact substitution remains expensive. Core Ampang Hilir is screening-only: GCB is explicitly a boundary comparator.',
'B06':'Affordable family utility and actual access need project-specific proof. Urban consideration and D\'Sara use remain held; Saville\'s small positive standard balance is especially fragile.222Residency gives Setapak a cleaner alternative to the PV21 labelling problem without creating a buy.',
'B07':'Zeva and Utropolis create legitimate compact research avenues; Kuchai elsewhere remains a family countercase to small-unit bias. Zeva\'s850 rent and Utropolis\'s basic-versus-furnished mismatch substantially weaken conviction. DaMen and GeoSense demonstrate that large rent differences may be absorbed into price. Trefoil, Koi, Gravit and family budget stock remain price/rent constrained.',
'B08':'Outer township quality and small-ticket affordability do not guarantee rent absorption or financeable ownership depth. Alanis/Horizon require whole-parcel discipline; Habitus451 is not silently admitted as residential. GAIA normal asks are separated from auction reserves. Geo and Parque show why a family township\'s reputation cannot be transferred to every layout.'}
(ROOT/'regions').mkdir(exist_ok=True)
coverage=['# All-catchment coverage and underwriting disposition','',
 'Scope is the unchanged61 functional catchments in8 batches, not every administrative locality or every project in Klang Valley. Each catchment now has a written desk disposition with its material gaps. This is a bounded regional desk release; it does not mean61 fully verified investment markets. Exact scope and overlap follow the original pre-research lock.',
 '', '| Area | Catchment | R2 cases | R1 retained | Inherited | Depth / remaining decision limit |','|---|---|---|---|---|---|']
for batch in batch_names:
    lines=[f'# {batch} — {batch_names[batch]}','',findings[batch],'',
      'All demand mechanisms below are analytical hypotheses unless specifically sourced as observations. Ask budgets are the selected expressions, not statistical market ranges. Advertisements prove offers were marketed, not demand, occupancy, completed resale prices or management health. Each linked case preserves the G0 stop and conditional G1–G9 diagnostics.', '']
    for a in [v for v in areas.values() if v['batch']==batch]:
        ids=a['r2_cases'];oldids=a['r1_cases']; cs=[C[i] for i in ids]
        broad_gap='Core catchment screen only; financial boundary comparator does not close core gap' if a['id']=='A39' else (
          'Selected R2 expression diagnostics; material product/subcatchment gaps remain' if ids else (
          'R1 selected expression retained, no fresh unit verification' if oldids else 'Inherited Cheras expression retained, no fresh unit verification'))
        a['depth']=broad_gap
        links='; '.join(link(ROOT/'cases'/f'{i}.md',i) for i in ids) or 'None'
        coverage.append(f"| {a['id']} | {a['catchment']} | {links} | {', '.join(oldids) or 'None'} | {a['inherited']} | {broad_gap} |")
        lines += [f"## {a['id']} — {a['catchment']}",'',f"**Desk disposition:** {broad_gap}.",
          '',f"**Buyer task / mechanism hypothesis:** {a['demand_hypothesis']}.",
          '',f"**True substitution question:** {a['substitution_test']}.",
          '',f"**Strongest counter-thesis:** {a['counter_thesis']}.",
          '',f"**Evidence and candidate choice:** {links}. Retained R1: {', '.join(oldids) or 'none'}. Older Cheras: {a['inherited']}."]
        if cs or oldids:
            lines+=['','| Expression | Selected ask | Layout/area | Rent scenario | Gross | Standard/month | Annual carry |','|---|---:|---|---:|---:|---:|---:|']
            for cc in cs+[r1c[i] for i in oldids]:
                bb=B.get(cc['id'],r1b.get(cc['id']))
                lines.append(f"| {cc['id']} {cc['name']} | {money(cc['price'])} | {cc['layout']}, {cc['sqft']}sf | {money(cc['rent_assumed'])} | {bb['gross_yield']:.2%} | {bb['standard_monthly_balance']:+,.0f} | {bb['cashflow_by_year'][0]:+,.0f} |")
            prices=[c['price'] for c in cs]+[r1c[i]['price'] for i in oldids]
            lines+=['',f"Sample acquisition quantum RM{money(min(prices))}–{money(max(prices))}; this is a sampled budget span only. Higher/lower budgets are not ruled out."]
        lines += ['',f"**Layout / budget / lifecycle coverage:** {a['material_segment_gaps']}. Predominantly marketed secondary expressions. New-launch net packages, near-VP seller composition and completed auction results are not fully bounded. Those omissions prohibit a whole-catchment fair-value or supply-clearance conclusion.",
          '', '**Ordered gate disposition:** G0 unvalidated reference value; G1 use mechanism is the hypothesis above; G2 actual buyer/tenant motive and credit depth unknown; G3 operations and effective competing supply unverified; G4 no exact unit inspection; G5 no validated discount; G6 named substitutes but no validated resale floor/ceiling or exit redundancy; G7 conditional financial/terminal stress only; G8 no actual portfolio or DSR clearance; G9 Defer for the considered expressions. Screen-only segments have no fabricated project decision.',
          '', '**Product versus investment:** no project-quality ranking is proven by asking rent. A negative standard row receives lowest research priority, not a structural Reject. A positive row is a lead for evidence collection, not permission to buy. G0 stops prevent the financial table from becoming a valuation.',
          '', '**What changes the conclusion:** a current exact residential parcel and net consideration; condition-matched achieved rent and actual strata/capex costs; independently financeable end-user choice against the named substitutes. These are the three bounded evidence routes. Further broad advertisement scraping has lower value than resolving those specific items. Core subcatchment/product gaps remain open until a comparable case is worked.',
          '', '**Closeout:** this public desk pass is closed with explicit gaps; current cases Defer. Reopen manually on a verified offer/lease, a documented operating or lending change, or a catalyst with demonstrated demand transmission. No scheduled monitoring or automatic future growth.','']
    lines += ['## Retained and cross-release evidence','',link(P/'Selected_Case_Workpapers.md','R1 gate papers')+'; '+link(P/'Evidence_Register.md','R1 evidence')+'; '+link(PROJECT/'execution-release-2026-10-07'/'Financial_Replay.md','approved Cheras financial replay')+'; '+link(PROJECT/'cheras'/'Cheras_Regional_Underwriting.md','inherited Cheras cases')+'. Retention does not refresh their evidence dates.']
    md(f'regions/{batch}.md',lines)
save('Coverage_Register.json',list(areas.values()))
coverage += ['', '## Scope boundaries and material work still unresolved','',
 'Core Ampang Hilir is only screened; several wide catchments retain unworked submarkets: Tun Razak/Titiwangsa, core Shah Alam, Kajang/Saujana Impian, Rimbayu/Tropicana Aman, mature Rawang/Kundang and others identified in the61 rows. A one-project result never closes those different buyer pools. Studio/1BR, true2BR, family3BR and larger are admitted equally, but missing cells remain gaps rather than unsuitable layouts.',
 '', 'Listings are not a census. No numerical inventory, pipeline absorption rate, owner-occupier share, median achievable rent, days-to-sell or regional growth rate is estimated from duplicate snapshot ads. New-supply quantities and project-specific management/physical/financing evidence remain material uncertainty. No eligible area-wide winner or verified investment recommendation follows from this desk release.',
 '', 'The original43 mapped-only rows now have an explicit research disposition and expression/screen evidence. The release meets the protocol\'s bounded desk documentation criterion, with gaps disclosed; it does not claim complete decision-ready underwriting of all61markets.']
md('All_Catchment_Coverage.md',coverage)

claims=[]
for c in cases:
    for typ,status,claim in [('P','Observed advertisement/index, not verified consideration',f"Price scenarioRM{money(c['price'])}; {c['match']}"),
      ('R','Bounded estimate / asking evidence',f"Rent scenarioRM{money(c['rent_assumed'])}; sensitivityRM{money(c['rent_low'])}–{money(c['rent_high'])}; matching limits as inP"),
      ('M','Interpretation, not measured demand',c['thesis']+'; rival: '+c['decisive_risk'])]:
        claims.append(dict(id=c['id']+'-'+typ,case=c['id'],claim=claim,status=status,retrievals=c['retrievals'],
          event_date='Source-specific advertisement dates in linked raw; achieved event unknown',retrieved='2026-10-07',
          expires_on='New exact offer/lease/rights/operations evidence; no assumed live availability'))
save('Claim_Ledger.json',claims)
cl=['# Adopted claim and assumption ledger','',
 'Each case has separate price, rent and mechanism claims below. Raw paths retain the exact source text and its displayed dates; Source_Index.md provides original URL links. A retrieval may contain rejected hits. None of the quantitative rent/price claims is a completed transaction. Analyst fee/other/works amounts are explicitly assumed in Case_Inputs.json and every case paper, not promoted to observed data.',
 '', '| Claim | Scope | Evidence status | Retrieval lineage |','|---|---|---|---|']
for x in claims:
    cl.append(f"| {x['id']} | {x['claim']} | {x['status']} | "+'; '.join(link(raw[k],k) for k in x['retrievals'])+' |')
md('Claim_Ledger.md',cl)

stats=dict(new_cases=len(cases),standard_nonshortfall=sum(not b['current_shortfall'] for b in base),
 annual_nonnegative=sum(b['cashflow_by_year'][0]>=0 for b in base),gross_at_least6=sum(b['gross_yield']>=.06 for b in base),
 identity_freshness_holds=sum(bool(c['quarantine']) for c in cases),
 new_catchments=len({c['area_id'] for c in cases}),covered_dispositions=len(areas),
 case_sensitivities=len(sensitivity),rank_grid_rows=len(grid),synthetic_pairs=len(pairs),pair_passes=sum(x['reserve_pass'] for x in pairs),
 r1_retained_cases=14,cheras_inherited_cases=9,r2_g9_defer=len(cases),verified_deploy=0)
save('Release_Statistics.json',stats)
summary=['# Klang Valley regional underwriting — consolidated desk review','',
 'Release KV-REG-2026-10-07-R2. Evidence cutoff7October2026. English framework/research files; discussion may be Mandarin. The frozen Core, original G0–G9 and Evidence–Judgment Divergence architecture remain authoritative and unchanged.',
 '', '**Conclusion:** this round closes the bounded public desk pass across the declared61catchments with explicit material gaps. It produces50additional conditional product cases and retains14R1plus9olderCheras expressions. It does not establish61 decision-ready markets, a full project/unit census, a verified undervaluation or any Deploy. Core Ampang Hilir remains screening-only. Broad subcatchments and product cohorts with missing evidence are visible in the coverage register.',
 '', f"Of the50new scenarios, {stats['standard_nonshortfall']} cover the standard instalment/fee proxy, {stats['gross_at_least6']} meet or exceed6%gross, and only{stats['annual_nonnegative']} have nonnegative annual base carry. Those two are Centrestage and Neo, both held for identity/freshness. Every non-quarantined case has negative annual carry under the stated assumptions. This is a model result for selected expressions, not the market-wide prevalence of profitable property.",
 '', '## Read the result','',
 '- '+link(ROOT/'All_Catchment_Coverage.md','61-catchment coverage and gaps'),
 '- '+link(ROOT/'Financial_Underwriting.md','financial chain, price/rent hurdles and stress'),
 '- '+link(ROOT/'Divergence_and_Misses.md','six divergence investigations and18miss records'),
 '- '+link(ROOT/'Claim_Ledger.md','adopted claims and source lineage'),
 '- '+link(ROOT/'Validation_Report.md','integrity and calculation checks'),
 '', '## Eight regional conclusions','', '| Batch | Finding | Detailed catchments |','|---|---|---|']
for batch in batch_names:summary.append(f"| {batch} {batch_names[batch]} | {findings[batch]} | {link(ROOT/'regions'/f'{batch}.md',batch)} |")
summary += ['', '## Evidence queue, not a buy ranking','',
 'The most useful next contest is compact Zeva/Utropolis against an ordinary family expression such as Kuchai Avenue and retained R1 Maxim/Skypod. This deliberately tests small-unit yield against household utility and exit buyer depth. No winner survives all existing gates. Cliveden/Neo stay on a separate freshness/identity queue; Centrestage is a component-risk diagnostic. Premium quality candidates remain lowest income priority at current shortfalls, with quantified reopening conditions.',
 '', '| New expression | Price scenario | Rent scenario | Fee proxy | Gross | Standard/mo | Annual carry | Why evidence matters next |', '|---|---:|---:|---:|---:|---:|---:|---|']
for cid in ('R231','R234','R201','R216','R219','R208'):
    c=C[cid];b=B[cid]
    summary.append(f"| {link(ROOT/'cases'/f'{cid}.md',c['name'])} | {money(c['price'])} | {money(c['rent_assumed'])} | {money(c['fee_assumed'])} | {b['gross_yield']:.2%} | {b['standard_monthly_balance']:+,.0f} | {b['cashflow_by_year'][0]:+,.0f} | {c['quarantine'] or c['decisive_risk']} |")
summary += ['', 'Every row is conditional, pre-tax and based on unverified fee/cost allowances. Positive standard coverage is not a positive annual income return. No arithmetic threshold is an executable bid or a defensible market valuation.',
 '', '## What the small-unit expansion changes','',
 'Studios/1BR cannot be rejected merely for lacking a family buyer. They can serve distinct households and may have better entry-to-rent arithmetic. Conversely, rental intensity, component rights, furnishing replacement, fees and narrow ownership depth can negate that benefit. Trefoil and Parque show that a smaller unit in a good township need not solve the income problem; Centrestage/Horizon show that advertised small-unit identity can be wrong.2/3BR remain genuine alternatives where their useful rooms and ownership exits warrant the price.',
 '', '## Decision control and market change','',
 'No Core change or new market mechanism is proposed. Current shortfall remains the lowest research tier, not an automatic Reject. Future improvement can reopen a case only through a falsifiable transmission hypothesis and new evidence; no catalyst rent escalation is included in base. Unresolved divergence lowers conviction and raises proof/safety-margin requirements. Personal conviction, a portal median and a famous address do not close G0.',
 '', '## The meaningful Senior Market Red Team boundary','',
 'The decision-sensitive judgment is whether the compact examples offer a credible independent ownership exit after their tenancy advantage is stress-tested, or whether buyer willingness to pay primarily favours practical family products at these budgets. The competing expressions, weaker-rent counterexamples and required exits are now concrete enough to challenge. A market-level critique can change the research queue; it cannot replace exact price/rights, signed rent, MC/physical and lender evidence. No request is made for the user to gather these records or guess management quality.',
 '', 'Specific challenges: would a working household choose Zeva450 at the model\'s future budget over a larger local unit; does Utropolis retain enough non-student ownership appeal when campus accommodation competes; and does Kuchai935 have meaningful owner utility after real parking/lift/approach friction? These are falsifiable market interpretations, not requests to approve a purchase or new Core rule.',
 '', '## Completion boundary','',
 'Completed: scope-wide desk dispositions,50conditional G0–G9 papers, case and source ledger,450sensitivities,450rent/fee grid points,64-case pair stress, material divergences and misses, and preservation audit. Retained work is linked with original evidence dates. Still unresolved: normalised clearing intervals, actual net rents/fees/works, management condition, original plans/rights and financeable ownership exit depth; unworked product/subcatchment cells remain coverage gaps. No sale/offer/outreach, paid research, scheduled monitoring or realised validation occurred.','',base_note]
md('All_Catchment_Review.md',summary)
print(json.dumps(stats,indent=2))
