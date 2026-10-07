"""Render the authored substantive coverage self-audit; counts alone certify nothing."""
import json
from pathlib import Path

P = Path(__file__).resolve().parent
areas = json.loads((P.parent / 'Coverage_Register.json').read_text(encoding='utf-8-sig'))
dimensions = [
    'Functional tasks and boundaries',
    'Material budget, layout and lifecycle coverage',
    'Dated demand/supply and forward structure',
    'Comparable identity, source quality and G0',
    'Complete financial, terminal and stress diagnostics',
    'Buyer/exit substitution and strongest rival',
    'Divergence, misses and finite remaining evidence',
]
notes = {
25: [
 'Work-linked small households versus family space; Bangsar South, Pantai and Kerinchi are not assigned the same willingness or routes. Household capture remains a hypothesis.',
 'South View compact and KL Gateway 2BR are modelled; Park Residences family asks and Goodwood product are screened. Restricted/low-cost Pantai-Kerinchi parcels remain unmatched, preventing a whole-budget winner.',
 'UOA AR2024 confirms Laurel 1260 units completed end-FY2024; Goodwood 678 is a different family cohort. Delivered stock challenges scarcity but does not measure vacancy or lease absorption.',
 'B4-E01/E02: Residences versus Premium Residences, floor and availability conflicts; South View study/bedroom coding and family package dates remain G0 stops.',
 'R213/R312 full models: standard monthly +68/-547, annual carry -4419/-12767; terminal recovery, lower rent, fees, term, valuation, works and joint stress included.',
 'Investor-led compact exit is permitted; more usable family space is an alternative, not a transferred valuation. Duplicate competing accommodation and fit-out burden challenge office-led optimism.',
 'Specific next evidence is South View plan/ordinary lease/fees, then adjusted effective transfers; B4-D05 keeps delivery/access distinctions. Generic listings cannot establish tenant capture.',
],
26: [
 'Established family routines are separated from Ascencia compact/rail utility and relevant landed total-budget substitution; no route was physically inspected.',
 'Sinaran 2BR and Ascencia compact are active; Mas Kiara 1260-sf family/550k is screened. Sri TTDI restricted-land price is not an unrestricted comparable. Other TTDI stock is a declared gap.',
 'Glomac developer product range is existing competition; sold out is not occupation. No comprehensive future-supply total means no scarcity premium. Ayanna wrong-area lead was excluded.',
 'B4-E03/E04: Ascencia studio/1BR and partial/full package conflict; 668k is a different offer. Sinaran rent/bay match and normalised prices remain unproved.',
 'R214/R313 full models plus 668k alternate sensitivity. Both standard and annual carry deficits persist; compact quantum does not rescue income. Finance and adverse exit tests retained.',
 'Own-use willingness may support product demand without investor carry. Larger/lower-price family and landed alternatives challenge a prime-neighbourhood narrative; no universal price ceiling.',
 'B4-M02 corrects the supply search. Next approved plan, rights, ordinary leases, actual charges and matched effective transfers; current deficits retain lowest priority without permanent Reject.',
],
27: [
 'Prime mixed-use professional/downsizer utility is a hypothesis distinct from luxury-family demand. DC is one product, not a proxy for all Damansara Heights.',
 '904-sf compact and 1152-sf larger control are modelled; developer 1BR-to-penthouse range acknowledged. Other mature condos, landed and unnormalised new packages prevent an area-wide winner.',
 'Guoco AR2025 and developer record establish 370 residences in mixed development. Hotel/office context is not rental capture; no scarcity or current absorption assumption.',
 'B4-E05: 1152-sf index offer and 1/2BR coding; 1194-sf lower offers are different products. Net incentives and resale terms are unresolved at G0.',
 'R215/R314 carry, entry equity, remaining debt and future-buyer burden modelled. Larger control 3.60% gross and -2573 standard monthly; high rent scenario is not base proof.',
 'Additional room utility does not cover the selected price increment. Owner prestige and investor yield are tested separately; future buyer equity and rival prime stock remain decisive.',
 'First replace index with exact net package and plan, then ordinary leases, charges and lender evidence. Do not spend further broad searches manufacturing a prestige premium.',
],
28: [
 'Premium compact convenience versus mature family rooms; schooling/work-route usefulness is a hypothesis, not measured expatriate/owner share. North Kiara supply is not silently Mont Kiara.',
 'OOAK 696-sf 1BR and Pines 1268-sf 3BR active; Allevia larger modern family cohort assessed. Other mature/Arcoris variants not fully paired, limiting best-project claims.',
 'UEM FY2025 confirms Allevia handover, rather than an undelivered 2025 forecast. MRT3 future scheme is not existing Sri Hartamas station access. Absorption is unmeasured.',
 'B4-E06/E07: indexed asks, 1292 versus 1268-sf transfer and heterogeneous 19-record window cannot establish fair value. Renovated 7000-8000 rents cannot price the cheapest sale.',
 'KV10/R315 full models, nine Pines/Windsor rent combinations and shared capital stress. Pines 6.51% gross but annual -74 and flat-exit five-year loss; matched low rent removes standard buffer.',
 'Family-income advantage competes with hidden refurbishment/major works, newer delivered substitutes and practical bay/routes. Investor-led exit allowed, family owner premium unproved.',
 'B4-D02/D05. First sale condition/works and matched ordinary leases/fees, then adjusted transfers. Unresolved advantage lowers conviction; no numerical safety margin from unvalidated value.',
],
29: [
 'Ordinary affordable compact tenancy and family mixed-use living are distinct tasks. Hotel/managed accommodation cannot substitute for whole-unit ordinary leases.',
 'Cliveden studio and Windsor 1230-sf 3BR active; Mayland Dorsett studio/1+1/2BR range screened. Other Hartamas/landed panels are gaps, so no catchment-wide winner.',
 'Developer product/source distinction retained; mixed-use facilities do not prove demand or operating health. No current MRT3 premium and no measured new-stock rental absorption.',
 'B4-E08/E09: Windsor sale date discrepancy and syndicated April rent; Cliveden old 250k redirect and different 285888 September lead; mixed-size/office records not valuation anchors.',
 'R216/R316 and Cliveden alternate entry fully modelled. Windsor 6.40% gross, annual -865; old Cliveden annual -255. Rent-grid ordering reverses and high gross does not clear offers.',
 'Family rents challenge compact-only selection; one bay, dated rent, fees and exceptional fit-out challenge family optimism. Investor-led compact resale remains admissible but unvalidated.',
 'B4-D02/D03 and corrected draft carry wording B4-M04. Verify current ordinary Windsor lease/charges/works, and eligible exact Cliveden parcel/price before ranking.',
],
30: [
 'Local Dutamas-Segambut family task compares more mature space with newer smaller rooms. North Kiara branding and proposed/direct KTM wording do not transfer Mont Kiara or rail benefits.',
 'Prima Duta 1614-sf and United Point 958-sf 3BR active; developer smaller product range noted. No matched standalone compact or full Dutamas panel; no universal size preference.',
 'UOA confirms 2509 United Point residential units, separate from retail area. This is stock, not empty units. Current direct rail connection and absorption remain unverified.',
 'B4-E10: partially fitted sale, tandem bays and undisclosed tenancy rent until March2027 versus separate furnished rental ask. Existing income cannot be replaced with stabilised rent.',
 'R217/R317 full costs/stress and six-month no-income-credit lease sensitivity. 2500 stabilised assumption gives standard -371/-113; actual contract economics remain unresolved.',
 'Lower newer-unit quantum competes with density, tandem parking and lease timing; larger mature space competes with works. Neither requires a mandatory owner exit or future-rail uplift.',
 'B4-D04. Obtain actual lease, collections and transfer/expiry rights first, then fit-out timing and equal-condition costs/transfers. No nonpayment allegation or zero-income forecast.',
],
31: [
 'Desa ParkCity lifestyle and Menjalara local affordability are separate willingness mechanisms; neighbouring locations are functional alternatives, not equivalent valuations.',
 'Westside One compact, Westside Three 2BR and Menjalara18 3+1 active. Park Place/Noora screened; larger/landed ParkCity and lower-cost Menjalara remain gaps with no area-wide winner.',
 'Official Park Place/Noora expected dates and progress do not settle actual VP. No guessed delivered count, opening year or absence-of-supply premium; compact/family competition distinguished.',
 'B4-E11/E12: 749k WestsideThree header contradicts Bukit Jalil body and is quarantined. WestsideOne study/bedroom/package and retained WestsideThree fair value remain unresolved.',
 'R218/R246/R318 full models: all current standard deficits; lower compact quantum does not automatically improve yield. No 749k false-pair model or hypothetical catalyst rent included.',
 'Township appeal can coexist with weak leveraged income; Menjalara cannot inherit the lifestyle premium. Future owner willingness, ordinary rent and financeable exit must be evidenced.',
 'B4-D01/D05. A coherent exact offer could overturn comparison; current contradiction resolves only source admissibility. Reopen on rights-matched transfers/leases and consequential actual supply timing.',
],
32: [
 'Local lower-quantum family use versus smaller newer stock; actual route/bay utility more relevant than Kepong/Jinjang or Kiara Bay labels. No automatic Mont Kiara buyer transfer.',
 'First Residence 1074-sf 3BR and Fortune775-sf 2BR active; AVA family cohort assessed. Tiny room/studio ads do not prove separate parcels; restricted Jinjang/low-cost and new packages remain gaps.',
 'UEM confirms AVA FY2025 handover and identifies 870 units. No township/phase double count or assumed occupancy; recent family competition is not a demand booster by itself.',
 'B4-E13: partial/display-photo sale versus furnished rents and differing bays. 470k/480k are distinct leads; 100% loan marketing neither sets net price nor replaces90% baseline.',
 'KV09/R319 full models and 470k sensitivity; First Residence 6.00% gross but annual -3440, Fortune5.25% and annual -5853. Partial1700rent materially weakens the two-bedroom proposition.',
 'Cheaper third bedroom may earn too little to pay for age/works/bays; newer smaller product may suit another household but lacks yield at selected entry. No universal three-bedroom rule.',
 'Match equal-condition whole-unit rents, actual fee/works and rights first. Further partition ads would not close the separately titled compact gap or establish regional investment failure.',
],
33: [
 'Damansara Perdana compact income and Mutiara residential utility are different tasks; Kota Damansara/Surian station remains A24. Sabah namesake is excluded.',
 'Neo studio and Surian850-sf unresolved1/2/2+1 active; larger1400-1938-sf Surian and DQuince family alternatives screened. Other Perdana/new phases remain unpaired; no universal price spread.',
 'Boustead AR2012 confirms311Surian units completed, overriding portal2016metadata for lifecycle. DQuince project/phase evidence lacks official actual VP here; no cumulative delivered total assumed.',
 'B4-E14-E16: rent-category sale amounts excluded; Neo original price/bays unresolved; Surian original plan and850-sf630kone-room transfer need rights/condition adjustment.',
 'R219/R320 full stress: Neo only positive annual base carry but held; Surian standard -269. Two-bay1800rent cannot silently improve cheapest Neo case; legacy future80%field not used.',
 'Low-entry compact investor exit competes with financeability/fees/works; Mutiara use value competes with cheaper Perdana/new family stock. Historical date alone proves neither deterioration nor value.',
 'B4-D03/D05 and actual wrong-state search miss B4-M01. Resolve exact Neo parcel/use/live price and ordinary lease, and Surian approved plan before any ranking or mispricing claim.',
],
}
rows=[]
for n, assessments in notes.items():
    assert len(assessments)==7
    rows.append(dict(area_id=f'A{n:02}',catchment=areas[n-1]['catchment'],
        dimensions=[dict(dimension=i+1,name=dimensions[i],assessment=t,status='Assessed with explicit limitation and decision consequence') for i,t in enumerate(assessments)],
        desk_complete=True,decision_ready=False,g9='Defer',
        scope_limit='Bounded functional desk coverage, not a project/unit census or realised validation'))
required=['B04_Regional_Synthesis.md','B04_Evidence_and_Supply.md','B04_Cases_G0_G9.md','B04_Case_Inputs.json','B04_Inherited_Assessments.json','B04_Financial_Underwriting.md','B04_Financial_Results.json','B04_Divergence_and_Misses.md']
out=dict(version='KV-B04-2026-10-07-R3',cutoff='2026-10-07',status='Completed bounded desk pass; no Deploy',programme_complete=False,
    review_method='Author substantive self-audit against the existing protocol, not independent third-party validation or completion inferred from counts',
    rows=rows,required_files=required,next_batch='B05',
    limitations=['No authenticated title/lease/fee/works/lender or physical inspection clearance','Declared unworked submarkets restrict best-project, scarcity and liquidity conclusions','Programme portfolio replay and final cross-region audit remain outstanding','No predictive outcome validation; Core unchanged'])
(P/'B04_Completion_Audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
lines=['# B04 substantive completion self-audit','','Cutoff: 7 October 2026. Nine catchments A25-A33 are bounded desk-complete **Defer**; no decision-ready purchase or realised validation. This is an author self-audit of the seven substantive requirements, not an independent reviewer certification. The full programme remains incomplete.','',
       'The [regional synthesis](B04_Regional_Synthesis.md) explains household/budget coverage and its limits. The [evidence ledger](B04_Evidence_and_Supply.md), [G0-G9 papers](B04_Cases_G0_G9.md), [financial report](B04_Financial_Underwriting.md) and [divergence/misses](B04_Divergence_and_Misses.md) support the assessments below. No document count closes a market gap.','']
for row in rows:
    lines += [f"## {row['area_id']} - {row['catchment']}",'','| Dimension | Substantive assessment and consequence |','|---|---|']
    lines += [f"| {d['dimension']}. {d['name']} | {d['assessment']} |" for d in row['dimensions']]
    lines += ['','Disposition: bounded desk-complete Defer. Specific remaining evidence can reopen this conclusion; no generic missing-document list is offered as a substitute for the investigation above.','']
lines += ['## Completion boundary','',
    'Closing this batch means proceeding to B05 with bounded conclusions and explicit gaps. It does not clear exact-unit identity, achieve the 6% preference, validate a safety margin or authorise investment. B01/B02 still need their final substantive audit; B03 and B04 have bounded desk releases; B05-B08 still need comparable regional deepening. Cross-region comparison and programme portfolio stress remain required.','',
    'No Core or SOP amendment is made in this release. Corrections are recorded in case execution and current status only. See [the continuation record](B04_RESUME_CHECKPOINT.md).','']
(P/'B04_Completion_Audit.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps(dict(areas=len(rows),substantive_dimensions=sum(len(r['dimensions']) for r in rows),decision_ready=0,next_batch='B05')))
