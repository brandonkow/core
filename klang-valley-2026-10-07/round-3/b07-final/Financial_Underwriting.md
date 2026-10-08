# B07 final financial, exit and portfolio diagnostics

Cutoff8October2026. Reproducible [results](Financial_Results.json), [builder](Scenario_Builder.py) and [supplementary inputs](Inputs.json). Historical20 inputs remain unchanged. All22 cases remain G0STOP/G9Defer.

## Common basis and limits

90% of purchase price financed at4% over35years; preferred6% gross. Standard balance is asking monthly rent less standard instalment and the combined fee proxy. Actual management-only charges are not authenticated. Full-year cash uses11paid months,12full instalments,12fee/other allowances; base entry is15% of price plus refurbishment, comprising10% equity and5% acquisition allowance.3% disposal and a five-year holding horizon are illustrative.8% equity hurdle and500000cash/150000protected reserve are inherited synthetic diagnostics, not user finances or approved target returns.

All figures pre-tax; fees, insurance, taxes, repairs and transaction-specific costs are not fully quoted. Unknown costs are not verified zero. The additional1200annual/5000exit buffer is sensitivity, not a bound. No exact offer, lease, lender approval or realised outcome is represented.

## All operating expressions

| ID | Area / expression | Price | Rent/month | Gross | Standard/month | Annual cash | Entry cash | Five-year nominal break-even |8% required exit |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
|KV13|A46 Skypod Residence|380,000|2,000|6.32%|166|-2,411|77,000|418,807|459,191|
|R230|A47 Koi Prima|290,000|1,300|5.38%|-106|-4,728|58,500|334,228|368,080|
|R231|A48 Zeva Equine South|210,000|1,200|6.86%|183|-802|51,500|237,935|264,013|
|R232|A49 Da Men|428,000|2,100|5.89%|64|-3,727|79,200|469,159|512,093|
|R233|A50 Seri Atria|295,000|1,300|5.29%|-106|-4,727|64,250|344,453|381,087|
|R234|A51 Paramount Utropolis|280,000|1,500|6.43%|164|-1,690|67,000|318,725|353,356|
|R235|A52 Trefoil Setia City|260,000|1,000|4.62%|-266|-6,113|54,000|310,914|344,064|
|R236|A53 Gravit8 Nordica|328,000|1,300|4.76%|-237|-6,305|69,200|386,088|426,872|
|R249|A49 Sunway GeoSense|1,198,000|5,000|5.01%|-194|-10,928|199,700|1,293,100|1,402,994|
|R338|A46 Kinrara Mas|328,000|1,500|5.49%|-47|-4,465|74,200|381,758|422,959|
|R339|A47 The Wharf Residence|218,000|1,100|6.06%|31|-2,525|42,700|244,626|268,340|
|R340|A48 Univ 360 compact|230,000|1,350|7.04%|253|-109|49,500|249,508|273,881|
|R341|A48 Univ 360 family|320,000|1,700|6.38%|95|-2,962|68,000|360,737|397,312|
|R342|A49 Subang Avenue|450,000|2,500|6.67%|384|-295|102,500|494,421|544,901|
|R343|A51 Suria Residence Bukit Jelutong|476,000|1,800|4.54%|-405|-9,058|86,400|545,368|597,647|
|R344|A52 Seri Pinang Setia Alam|290,000|1,200|4.97%|-156|-5,228|63,500|341,960|378,765|
|R345|A53 Impiria Residensi|600,000|3,000|6.00%|279|-2,652|105,000|638,224|692,647|
|R346|A50 Nadayu 801 family|405,000|1,800|5.33%|-164|-6,167|90,750|473,853|525,022|
|R347|A52 BBK Condominium|250,000|1,500|7.20%|154|-2,055|72,500|300,463|338,162|
|R348|A51 Suri Puteri family|370,000|1,650|5.35%|-74|-4,943|80,500|426,860|471,676|
|R349|A46 The Cruise Residence two-bedroom|600,000|1,950|3.90%|-771|-13,602|105,000|694,667|761,033|
|R350|A48 East Lake Residence family|350,000|2,000|6.86%|305|-737|72,500|379,720|416,065|

Eleven expressions pass the simple standard under assumed rents and fees; ten reach6%gross; none has nonnegative base annual cash. Neither this arithmetic nor a gross ratio resolves a G0 stop. Base nominal exit break-even exceeds purchase price in all22 cases; required future prices are not forecasts.

## Price and rent thresholds

Constraints hold fee/other/condition assumptions fixed. They are not fair values, executable bids or validated margins of safety.

| ID | Rent for standard coverage | Rent for6%gross | Rent for annual neutrality | Price for annual neutrality |
|---|---:|---:|---:|---:|
|KV13|1,834|1,900|2,219|329,571|
|R230|1,406|1,450|1,730|191,135|
|R231|1,017|1,050|1,273|193,226|
|R232|2,036|2,140|2,439|350,065|
|R233|1,406|1,475|1,730|196,154|
|R234|1,336|1,400|1,654|244,669|
|R235|1,266|1,300|1,556|132,163|
|R236|1,537|1,640|1,873|196,154|
|R249|5,194|5,990|5,993|969,475|
|R338|1,547|1,640|1,906|234,631|
|R339|1,069|1,090|1,330|165,204|
|R340|1,097|1,150|1,360|227,731|
|R341|1,605|1,600|1,969|258,053|
|R342|2,116|2,250|2,527|443,834|
|R343|2,205|2,380|2,623|286,577|
|R344|1,356|1,450|1,675|180,679|
|R345|2,721|3,000|3,241|544,546|
|R346|1,964|2,025|2,361|276,037|
|R347|1,346|1,250|1,687|207,028|
|R348|1,724|1,850|2,099|266,627|
|R349|2,721|3,000|3,187|315,561|
|R350|1,695|1,750|2,067|334,590|

## Conditional branches

| Parent / branch | Standard/month | Annual cash year1 | Entry cash | Nominal break-even |
|---|---:|---:|---:|---:|
|R340 / body_price_290k|14|-2,978|58,500|325,207|
|R342 / body_rent_2600|484|805|102,500|488,751|
|R342 / fitout45k_initial3mo|384|-5,295|112,500|509,885|
|R341 / furnishing35k_initial3mo|95|-6,362|83,000|379,706|
|R345 / replacement_rent_2400|-321|-9,252|105,000|672,245|
|R347 / fee_500_majorworks|4|-33,855|72,500|340,669|
|R346 / rent_header_1900|-64|-5,067|90,750|468,183|
|R338 / current_1550_two_bay_rent|3|-3,915|74,200|378,923|
|R339 / fee_300|-69|-3,725|42,700|250,812|
|R348 / lower355k_distinct_ad|-15|-4,226|78,250|407,936|
|R348 / high1800_older_ask|76|-3,293|80,500|418,355|
|R348 / fitout35k_initial3mo|-74|-8,243|90,500|440,572|
|R349 / older2300_FF_with35k_fitout|-421|-14,352|125,000|700,183|
|R349 / older580k_FF_sale_2300_rent|-341|-8,795|102,000|649,589|
|R350 / September2200_same_size_index|505|1,463|72,500|368,380|
|R350 / 1750_larger1116sf_rent_counter|55|-3,487|72,500|393,895|
|R350 / fee450_works30k|155|-32,537|72,500|419,926|
|R339 / October1000_561sf_counter|-69|-3,625|42,700|250,296|

Different-unit price/rent branches are sensitivity combinations, not executable packages. Extra fit-out and initial vacancy test the cost of reaching advertised furnished rents. Works/fee shocks are analyst assumptions, not known building assessments.

## Stress, terminal burden and future buyers

Fourteen scenarios per case cover base,5.5% interest,20% lower rent,20% higher fees,twelve initial vacant months,30000works in month24,15%lower bank value,25-year debt,12-month exit delay,unquoted-cost buffer,combined five-year stress,combined12-month hold,and low/high rent.308 evaluations plus18 input branches give326. Low/base rent coincide for R349; counts are evaluations, not independent forecasts.

Combined stress uses5.5%,20%lower rent,20%higher fees,six paid months in year1 and30000works in month1. No sale or refinancing funds the twelve-month hold. Standard balance stays at the baseline by design; actual cashflow and the separate scenario metric apply stress.

| New case | Base annual cash | Combined year1 cash | Combined five-year exit break-even |12-month delayed exit break-even |
|---|---:|---:|---:|---:|
|R349|-13,602|-62,591|801,533|699,598|
|R350|-737|-47,419|469,612|375,176|

Lower bank valuation raises initial equity while lowering debt service. A shorter loan or delayed sale can lower nominal exit break-even through different amortisation and earned income while worsening cash timing. No blanket monotonicity assumption is applied.

Investor-led exits remain eligible. Operating income is11rents less12fees/other allowances, before finance/tax. Illustrative5/6/7% operating yields are neither observed cap rates nor the preferred6%gross rule. Complete22-case diagnostics are in JSON. Selected contrasts:

| Case | Operating income | Yield at required nominal exit | Value at5% operating yield | Value at6% | Value at7% | Future-buyer cash90% standard | Cash70% stress |
|---|---:|---:|---:|---:|---:|---:|---:|
|R340|10,890|4.36%|217,800|181,500|155,571|52,426|102,328|
|R342|21,224|4.29%|424,480|353,733|303,200|109,163|208,047|
|R347|9,900|3.29%|198,000|165,000|141,429|80,069|140,162|
|R349|15,090|2.17%|301,800|251,500|215,571|119,200|258,134|
|R350|16,000|4.21%|320,000|266,667|228,571|76,958|152,902|

Buyer cash includes5% acquisition plus the same refurbishment proxy.70%/5.5%/25years is a future-credit sensitivity, not law or the user's default LTV. A resident buyer uses a different utility/budget test; neither resident nor investor willingness and ability has been authenticated.

## Ranking reversals and opportunity cost

The126 cells compare14pairs at low/base/high rent. Twelve pairs change their coverage leader. R342 stays ahead of R232 across the selected grid; KV13 stays ahead of R349. These are cash-coverage comparisons only. Component/title quarantine, different routes/layouts and G0 stops override an eligible purchase ranking.

For R342 versus R350,2500/2000 rents give annual cash-295/-737, favouring R342. Holding R342 at2500 and using2200 for R350 changes annual cash to-295/+1463, favouring R350. At2300/2000, R350 again leads. Source age, condition and actual lease replacement can determine rank; a preferred narrative cannot select the favourable cell.

R340's near-neutral base cash is weakened by its230000/290000 price conflict and component hold. R347's7.2%gross is weakened by same-lineage rent/title and major-works exposure. R345's6%gross depends on3000 rent;2400 reverses standard coverage. No single B07 winner is supportable.

## Joint cash paths and correlated exposure

All231 two-case combinations are evaluated month by month using the synthetic500000 pool and150000 protected reserve.210 preserve that reserve in the stated12-month shock;21 breach it. Every failing pair includes R249, reflecting its larger entry/operating burden under this particular pool. This is not a universal asset veto or the user's actual portfolio.

For example R249/R349 falls to47580 and R249/R342 to61520. A passing pair still may have weak economics, common supply exposure, inaccessible credit or uninvestable identity. Simultaneous shocks are scenarios, not empirically estimated correlations or probability-weighted expected losses. More-than-two holdings, real liabilities and the full61-area portfolio remain programme work.

Shared risk groups include campus allocation/academic turnover; southwest rail-corridor competing completions; Shah Alam/Subang employment/road access; and older family-condo works. Different area labels do not establish diversification. Retaining cash or verifying stronger cases in other regions remains a legitimate opportunity-cost comparison.

## Forward price-only controls

No rental income is assigned. Project floors are not selected-unit net contracts. Full-draw no-income carry is a financing scenario, not progressive-interest timing or a worst-case bound.

| Control | Price sensitivity | Fee | Actual rate | Standard rent required |6%gross rent | Annual-neutral rent | Entry allowance |12-month full-draw no-income carry |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|B07-T01|250,000|230|4.00%|1,226|1,250|1,534|57,500|16,875|
|B07-T02|270,000|230|4.00%|1,306|1,350|1,621|60,500|17,831|
|B07-T04|584,000|350|4.00%|2,677|2,920|3,139|107,600|34,527|
|B07-T05|555,000|350|4.00%|2,562|2,775|3,013|108,250|33,140|
|B07-T06|605,000|350|4.00%|2,761|3,025|3,230|110,750|35,531|
|B07-T03|377,000|250|4.00%|1,752|1,885|2,130|76,550|23,428|
|B07-T03|377,000|250|5.50%|1,752|1,885|2,479|76,550|27,265|
|B07-T03|377,000|350|4.00%|1,852|1,885|2,239|76,550|24,628|
|B07-T03|377,000|350|5.50%|1,852|1,885|2,588|76,550|28,465|
|B07-T03|377,000|450|4.00%|1,952|1,885|2,348|76,550|25,828|
|B07-T03|377,000|450|5.50%|1,952|1,885|2,697|76,550|29,665|

T01 NARA,T02 TAMU,T03 Ambang,T04 COVO,T05 Quaver,T06 2Rio are six controls with11sensitivity rows. The restricted Ambang270000 cohort and historical COVO250000 floor are not treated as unrestricted available offers. New supply requires actual phase/rights/delivery/offer matching before rental underwriting.

## Verification boundary

The builder checks unchanged historical inputs, closed-form debt and principal conservation, independent economic basis, discounted exit identity, annual cash reconciliation and appropriate adverse-shock direction. Remote byte hashes and a complete in-memory rebuild are required before publication acceptance. Passing calculations validates model execution; it does not validate market prices, tenant behaviour or investment outcomes.
