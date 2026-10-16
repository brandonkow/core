# Reusable financial execution SOP — v2

Effective: 16 October 2026. Version: **KV-SOP-FIN-2026-10-16-v2**.

The user explicitly authorised transferring all reusable calibrated parameters into current SOP, excluding project-specific information. This is adoption by the framework owner of execution defaults and scenario choices. It is not a claim of empirical validation, a new causal Core mechanism, a new gate or investment approval.

## Authority, scope and precedence

Read with the single frozen [master](../Residential_Investment_Framework.md), [approved execution supplement](Approved_Execution_Supplement.md), [decision execution standard](../execution-release-2026-10-07/Decision_Execution_Standard.md), and existing tenant/privacy and market-judgment addenda. Preserve their valid evidence, execution, terminal and portfolio controls.

This version supersedes conflicting **financial presets for future or materially reopened cases**. It replaces the old blanket acquisition allowance, all-in disposal allowance, annual-average tenancy shortcut, inherited stress magnitudes and synthetic investor balance sheet. Historical configurations, models and reports retain their versions; they have not been rerun. The [parameter register](Financial_Execution_Parameters_v2.json) is the current declarative input source, not a drop-in file for historical engines. A future implementation must map it explicitly and reconcile its financial chain.

Apply the appropriate lifecycle and operating form; mark inapplicable tests rather than inventing a construction period for a completed unit. Current instructions govern standard comparisons. Authentic terms govern separately labelled actual-financing/cost results. Record deviations, source/date, reason and decision effect. Never tune an input silently to manufacture a pass.

Distinguish four roles:

- **Standard:** the common financing and coverage comparison.
- **Planning default:** an estimate used transparently until better case evidence exists.
- **Stress sensitivity:** an agreed numerical test, without a claim of frequency or exhaustive worst-case coverage.
- **Target:** a desired outcome tested for plausibility, not evidence of market value.

A default can be used immediately in a conditional model. Missing actual terms do not become verified through default adoption. Existing G0-G9 and Evidence-Judgment Divergence still determine the capital decision.

## 1. Price, financing and returns

| Parameter | Current reusable treatment |
|---|---|
| Baseline financing | 90% LTV, 4% annual interest, 35-year amortisation. Do not reduce leverage to rescue coverage. |
| New-launch loan basis | Gross contracted price reference; separately show lender valuation, rebate treatment and actual loan offer. |
| Resale loan basis | Agreed acquisition price reference; actual bank valuation/LTV may differ. |
| Yield/economic basis | Effective nett consideration after applicable confirmed incentives. Show gross, nett, incentive conditions and all-in capital separately. |
| Preferred gross yield | 6%; preference and comparison reference, not universal Reject or an achieved net return. |
| Narrow monthly coverage | Parcel rent minus full principal-and-interest instalment minus management charge. Disclose any combined sinking-fund proxy. |
| Complete operating cash | Separately deduct collection losses, letting, repairs, owner charges and debt. Never label narrow coverage net profit. |
| Financing clock | For new-launch planning, construction interest-only, then the 35-year amortisation clock at handover. Check actual lender maturity/first-instalment terms separately. |
| Subsidy | No credit without applicable documented subsidy terms. |
| Rebate/deposit | Use actual rebate and payment mechanics; no universal rebate percentage or zero downpayment. LTV plus genuine usable incentive can offset initial equity, but no automatic cashback or invented bridge. |
| Reporting basis | Pre-personal-income-tax and pre-final-RPGT comparison, explicitly labelled. Applicable invoice taxes remain costs. |

Monthly instalment: `L*r / (1-(1+r)^(-n))`, where `r=annual_rate/12` and `n=12*term_years`; zero-rate branch is `L/n`. Record closing debt, principal and interest separately. Principal repayment is a cash outflow but not a second economic expense when the exit-debt reconciliation already captures it.

For income-led screening, a current narrow-coverage shortfall retains lowest research priority. A falsifiable, funded transition case remains researchable; there is no new permanent veto. Passing a numerical standard does not clear missing evidence or authorise purchase.

## 2. Rent, lease events and operation

| Parameter | Default and scope |
|---|---|
| Rental growth | 0% during construction and operation. Current defensible rent carries to handover without automatic growth; no receipts during construction. A supported new forecast is a separately recorded revision. |
| Initial fit-out / letting | One month, marketing concurrently; first receipt in operating month 2. Do not add another initial letting void on top. Use a distinct actual schedule for tenanted/ready units or longer documented works. |
| Lease duration | 12 paid months per lease. |
| Replacement vacancy | One month after expiry when a new tenant replaces the old. No vacancy imposed during an uninterrupted same-tenant renewal. |
| New tenant commission | One month's rent at move-in, per income stream. |
| Same tenant renewal | Half a month's rent at renewal, replacing—not adding to—the new-tenant fee for that event. |
| Annual repairs | Half the prevailing monthly total parcel rent per year. It is a planning budget, not half actual annual collections or a substitute for known capital defects. |
| Utilities | Ordinary-tenancy default: electricity, water and internet paid by tenant. Bundled products must show the actual owner-paid costs. |
| Unitemised other expenses | Remove the generic RM200/month allowance. Known owner bills are itemised; unknown material costs remain residual U. |
| Parking income | No extra income without evidence. Bay count, rights and allocation are always case inputs. |

Generate lease events, not an annual average multiplied blindly. With one initial fit-out month, 12-month leases and one replacement void, the 60-month example has voids in months 1,14,27,40,53 and lease starts in 2,15,28,41,54: **55 paid months and five new-tenant commissions** per stream. Part-year leases and later sale dates change this calendar.

In split operations reconcile all streams to the purchased parcel. A shared bay or facility cannot be allocated exclusively to two tenants simultaneously. A master suite is not automatically an independent studio. Preserve checks for privacy, entrances, bathrooms, kitchen/laundry, utility allocation, lawful use and actual works approval. A whole-parcel fallback requires its own rent and execution evidence.

Use the repair budget consistently: if treated as a committed monthly outflow, label it a provision. If held in a recoverable reserve account, track and release the unused balance rather than charging both reserve funding and repairs as losses. Include commission invoice tax only when applicable and not already included.

## 3. Fees, fit-out, acquisition and construction

| Parameter | Default and scope |
|---|---|
| Management/sinking charge | Case-specific actual or clearly provisional quoted charge. No universal psf amount. Disclose area and whether sinking is included. |
| New-launch fee planning | Hold the quoted charge unchanged for the first 24 months after handover as the planning convention; it is not a contractual freeze unless evidenced. A known actual revision overrides this assumption. |
| Later base fees | Future charge depends on AGM/governance decisions. Carry the last known charge provisionally where no resolution is available, with separate escalation stress. |
| Fit-out budget | 5% of effective nett price, final buyer-paid budget including required works, furniture/equipment and operating configuration. No extra inflation/contingency silently layered on. |
| Developer-supplied items | Reconcile inventory and exclude double charging. Quotes and scope can demonstrate the 5% budget inadequate; preserve that miss. |
| Furniture resale value | No separate automatic exit premium. |
| Acquisition costs | Itemise purchase/loan legal work, transfer/loan duties, applicable invoice tax, disbursements and later perfection where relevant. No blanket 5% gross allowance. |
| Construction duration | Case-specific contract/programme input; no universal 48-month duration. |
| Construction interest | Interest on drawn balances. Where dated draws are unavailable, 50% average loan utilisation is an explicitly approximate planning proxy. |
| Base special levy | Zero scheduled hypothetical levy; known approved/committed assessments must still be charged. No invented stress levy. |

Planning interest proxy: `loan * 0.50 * annual_rate * construction_months/12`. Prefer actual dated draws when available. A general billing schedule supplies stage percentages, not proof of timing or 50% average utilisation. Rate changes require timing treatment. Do not amortise the full balance during the separate interest-only planning phase and then charge it again.

Document package coverage and final buyer-paid costs. Marketing claims of free fees are conditional branches until supported. Current tax/fee schedules, purchaser status, exemptions and actual instruments must be checked when underwriting; this SOP does not freeze statutory rates or transaction quotes. Original acquisition perfection costs remain acquisition-related even when paid later.

## 4. Holding, target exit and seller costs

| Parameter | Reusable treatment |
|---|---|
| Standard operating hold | 60 months from handover, including initial fit-out; for completed acquisitions use completion/possession. Construction is additional calendar time. |
| Year-3 target | 110% of original effective nett price at operating month 36. |
| Year-5 target | 120% of original effective nett price at month 60. The additional ten percentage points are not compounding to 121%. |
| Meaning of target | Owner-selected target scenario, not a forecast validated by the market, guaranteed minimum or pass condition. |
| Exit agency | 3% of sale consideration for the planning comparison; not the entire selling cost. |
| Other seller expenses | Itemise actual seller legal work, discharge OR reassignment, relevant filing, consent/search/disbursements, applicable invoice tax and evidenced lender/closing adjustments. Avoid duplicate alternatives. |
| Tax handling | Retention can be a timing item/credit; do not automatically equate it to final tax. Personal income tax and final RPGT remain explicitly excluded from the default pre-tax comparison. |
| Future investor yield | 6% gross reference; match gross rent to gross yield and distinguish capitalisation sensitivity from a validated clearing price. |

Test flat-price exit as a dependency diagnostic, not a new survival veto. A higher bid must not automatically create an equally higher evidenced resale value: show both the target-scaled scenario and a fixed evidence-supported exit reference when comparing bids. Report break-even exit and required buyer funding. A different planned hold is explicitly versioned; do not turn five years into an immutable market law.

## 5. Reusable stress register

All magnitudes below are adopted user-selected sensitivities. An adverse loss is not automatically Reject; the existing framework assesses evidence, funding, exit and opportunity cost. Removed synthetic tests are not restored through a joint case. Removal of a test is not evidence that its underlying risk is impossible.

| ID | Current treatment |
|---|---|
| S1 | One 0.25 percentage-point move: 4% to 4.25%, remaining until sale. Main new-launch timing is handover, with first-draw timing bound; existing holding starts at the stress event. 3.75% is favourable sensitivity. Do not claim a once-per-decade frequency or universal worst-case ceiling. |
| S2 | Shorter initial amortisation eligibility: 31 and 25 years; do not silently replace the 35-year standard. |
| S3 | Launch gross valuation reference. For resale lending, valuation 10% below sale consideration; apply to lender loan base, not automatically to the seller's receipts as another price fall. |
| S4 | New-launch completion delay of 12 months relative to its stated base. A 48-month base becomes 60; completed properties are not given an artificial construction phase. No early-completion test. |
| S5 | Remove automatic alternative draw-shape stress; keep proxy uncertainty visible. |
| S6 | Remove automatic rebate-failure/deposit-bridge stress; actual adverse package terms still affect actual cash. |
| S7 | Rent 20% lower throughout the operating hold. |
| S8 | Crisis: 12 potential months minus 2 void months = 10 collected, then minus 1 month commission = 9 rent-equivalent months before invoice tax and other costs. One initial crisis is primary; repeated two-month replacement void is a separate duration bound. |
| S9 | Remove one component at zero for the entire hold. |
| S10 | Remove entire first operating year at zero. |
| S11 | Remove first year with only six paid months. |
| S12 | Start from the case's charge: first 24 months flat, then 5% annual increases from year 3. This is a stress path, not an AGM prediction. |
| S13 | Remove arbitrary other-expense shock / RM200 allowance; itemise evidenced costs. |
| S14 | Remove invented special-levy shock; do not hide it in combinations. |
| S15 | Add RM10,000 once to fit-out. No duplicate contingency for the same event. |
| S16 | Exit at 90% or 110% of original effective nett price, not plus/minus 10% of the 120% target. |
| S17 | Sale six months later: standard month 60 becomes 66. Carry rent, costs and debt through the delay, with no automatic extra appreciation. |
| S18 | Itemised seller costs; no arbitrary extra RM10,000 disposal allowance. |
| S19 | Future buyer funding: 85% LTV, 4.5%, 30 years. Separate from original owner's 90%/4%/35-year debt. |
| S20 | Future buyer gross yield reference 6%; no universal exit-buyer hard gate. |
| S21 | J1 delivery/cost = S4 + S15 + S1 upward + S12. J2 demand/exit = S7 + one S8 initial crisis + S16 at 90% nett + S17. J3 = their union, without duplicate shocks. No automatic additional arrears, shorter term or deleted tests. |
| S22 | Remove invented portfolio cash/reserve and unit mix. Actual G8 liquidity, concentration and correlated exposures remain required before allocation. |
| S23 | Test supported whole-parcel fallback where split operation matters. Rent, availability and restoration cost are case-specific. No invented fallback or automatic fit-out saving. |
| S24 | Two months unpaid plus one month to re-let. Test affected streams separately and synchronous bound if relevant. No automatic deposit recovery; record timing and overlap with scheduled vacancy/commission. |

For S8, nine rent-equivalent months is not nine months of receipts followed by another commission. Generate the entire tenancy calendar; do not multiply a crisis year by five unless that duration scenario is explicitly selected.

For S24, the three-month no-receipt event can include a vacancy already in the base. Rebuild the schedule and count incremental loss once. The original near-expiry timing is only an example, not a rule that every default happens at expiry. Deposits are not free income.

The selected 25bp rate shock is deliberately narrower than some observed historical rate cycles; its adoption does not certify that all market risk is covered. Where material actual evidence conflicts with a preset, surface that conflict through existing investigation controls and show a justified, labelled additional sensitivity. Do not silently replace the approved suite or reinstate deleted stresses.

## 6. Required cash, return and ranking outputs

Show, at minimum:

1. Gross and nett consideration, incentives, actual versus standard loan and cash downpayment.
2. Narrow monthly coverage, annual and full-hold operating cash, and gross/net yield with denominators.
3. Separate construction period, operating period and total calendar hold.
4. Acquisition, construction interest, fit-out, debt service, fees, repairs, commission, owner bills and rent receipts.
5. Exit price, remaining loan, itemised selling costs, net sale proceeds, full-period profit and annualised money-weighted return.
6. **Peak cumulative net funding before sale**, its month and a category breakdown; distinguish it from initial deposit, total gross expenses, final cumulative contribution and economic loss.
7. Base, single-factor stress, linked combinations, flat-price dependency and alternative operation if applicable.
8. Price/rent thresholds at which coverage or rank reverses; uncertainty and unpriced residual U beside results.

For monthly net owner cash `CF_t` excluding terminal proceeds, peak funding is `max(0, -min_t(sum_{i<=t} CF_i))`. Rent is recycled. Do not include final sale receipts when locating the pre-sale funding peak. Explain intramonth timing limitations, pre-funded reserves and actual payment dates. Borrowing is financing, not income.

Reconcile profits two ways: total owner cash including final proceeds, and an independent economic bridge with principal/remaining debt correctly treated. Use the whole calendar timeline for annualised IRR, including construction; do not describe a nine-year investment as a five-year return. Report absence/ambiguity of an IRR root honestly.

For a materially reopened case, validate debt balances, receipts, event counts, fee/area units, tax inclusion, costs, exit and joint-scenario non-duplication. Validation checks prove arithmetic/implementation consistency, not market truth. Log outcomes against defaults later, without retroactively rewriting the forecast.

## 7. Boundaries and future review

Project names, specific layouts, rents, asking prices, bay counts, package rebates, quoted psf charges, fixed construction dates and current rankings remain in case packets. This SOP and its parameter file contain only reusable rules and scoped defaults.

The current authority supersedes the earlier assessment that numerical SOP promotion had not yet been authorised. It does not change historical case results or grant admission. No Core promotion, map update, regional rerun, deployment, outreach or unattended monitoring is implied.

Review defaults against actual outcomes and representative assets over time. Market changes can justify versioned revisions. Strong conviction without a falsifiable mechanism still increases risk; a favourable model result cannot replace evidence.
