# Sources and method

Checked16October2026. Baseline `645d2174509203208bbc22905dba98102f03c49c`. No new price/rent search is claimed.

## Repository inputs

The frozen [programme inputs](../programme-final/Inputs.json) supply138source expressions,61catchments,122project groups, rent bounds and status overlays. The [historical financial report](../programme-final/Financial_Underwriting.md) and preserved [7October engine](../../../execution-release-2026-10-07/financial_engine.py) establish the90%/4%/35-year old reference. Embedded older calculated fields in raw C-series objects are ignored; they contain older financing conventions.

The [priority replay](../sop-v2-priority-replay-2026-10-16/README.md) supplies ten later-reviewed bases and18held alternatives for parity. Their source price/rent/fee inputs agree with the common source. The [SOPv2](../../../sop/Financial_Execution_SOP_v2.md) and [parameters](../../../sop/Financial_Execution_Parameters_v2.json) remain unchanged.

All important source Git blobs are pinned in Inputs.json. The first10and18held scenarios reproduce unchanged. Old whole-programme annual cash, entry cash and flat-exit profit match all138rounded reference rows.

## Cost references and small adapter correction

[PwC2025/2026Malaysian tax booklet](https://www.pwc.com/my/en/publications/mtb/stamp-duty.html), accessed16October: ordinary transfer scale1%,2%,3%,4%across100k/500k/1m boundaries, charged byRM100or part. This supports extending the prior sub-RM1m helper to the seven higher-price bases. Local-person/no-exemption is an analytical reference, not a verified buyer profile. No foreign-buyer eligibility, exemption or proposed future rule is presumed.

The previous helper rounded transfer consideration byRM1,000. This adapter usesRM100as the reference states. All first10bases/18held alternatives retain identical costs/results because their price increments make that distinction immaterial. Record this technical limitation rather than changing historical code. Loan duty remains5perRM1,000or part for the ordinary reference, with actual instrument treatment unverified.

[SRO2023 official order hosted by Malaysian Bar](https://www.malaysianbar.org.my/cms/upload_files/document/Solicitors%20Remuneration%20Order%202023.pdf), accessed16October: ordinary sale/financing scale1.25%first500k,1%next7m; no discretionary discount presumed. Seller uses400discharge and500minimum filing references. Actual reassignment/other work and disbursements remain U. No HDA discount is imported into resale comparisons.

[Customs MySST background](https://mysst.customs.gov.my/background/), accessed16October:8%general taxable-service reference, subject to listed categories and registration. Apply only to the reference professional invoices, not property prices or rent receipts. A no-additional-invoice-tax diagnostic covers inclusive/not-chargeable comparison without asserting an exemption.

Prior official consolidated Stamp Act/current-guideline URLs failed retrieval. Current official instrument/exemption/profile verification remains unresolved; PwC is a professional secondary cross-check, not a substitute for transaction adjudication. Ordinary assessed value is provisionally set equal to consideration. No verified zero cost for owner bills, insurance, rates, searches, consent, perfection or bank charges.

## Financial boundaries

No rent growth. Standard loan90%price at4%over35years.55paid months,5new commissions, repairs half-month rent/year; tenant utilities default. Fit-out5%nett planning; zero known launch rebate, construction phase or extra parking income imported. Target exit120%nett after60months, flat exit and stressed90%/110%nett separate.

Pre-personal-income-tax/pre-final-RPGT. Commission and professional invoice taxes remain costs when the chargeable reference applies. Repair provision is treated as spent/committed. No terminal furniture premium. All initial cash at month0for comparability; real purchase/tenancy/fee timing may change funding/IRR.

All3330evaluations are conditional cash calculations, not evidence that a target will clear, a household will renew, or an offer is available. The remaining historical alternatives and portfolio studies are preserved but not all replayed. No synthetic investor balance sheet is used.

## Reproduction

Run `node reproduce.cjs` from this packet in a repository checkout. It reads pinned files, verifies source blob hashes, recomputes every result, checks saved batch outputs and prints a verification summary. No packages, network or file mutation is required. The present execution used the same model and validator entirely in memory.

Base monthly ledgers are in the eight batch files. Other ledgers can be reproduced with runCase(...,true). Summary.json contains derived comparisons and region/pair mappings; it is not another market-data source.
