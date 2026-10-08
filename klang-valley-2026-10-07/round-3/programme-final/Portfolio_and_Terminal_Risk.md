# Programme portfolio and terminal risk

Cutoff: 8 October 2026. Inputs are conditional source scenarios, not live offers. [Reproducible results](Financial_Results.json) and [builder](Scenario_Builder.py) use the frozen financial functions. No personal capital allocation is made.

## Common stress and cash timing

Synthetic starting cash is RM500,000 with RM150,000 protected reserve. Neither is the user's financial profile. Each acquired asset incurs its modeled entry costs and refurbishment, followed by monthly operating/debt cashflows. No salary, refinancing, top-up or sale proceeds rescue a no-sale path. A negative path is an unfunded diagnostic, not permission to borrow cash implicitly.

The joint operating shock uses 5.5% interest, 20% lower rent, 20% higher management/sinking proxy, six paid months in year one and RM30,000 immediate works **per asset**. Year two has eleven paid months at the reduced rent, not an invented second six-month vacancy. Actual-credit stress also lends 90% of a bank value 15% below price (76.5% of acquisition price) over 25 years. The user's common comparison remains 90% / 4% / 35; actual-credit sensitivities do not replace it.

Same-project expressions are mutually alternative designs for this study, not independently verified simultaneously available units. Across-project cases are also unverified offers. No empirical covariance or tail probability is estimated.

## Pair counts after project identity reconciliation

| Diagnostic | Count |
|---|---:|
| Operating expressions / project groups | 138 / 122 |
| All expression pairs | 9,453 |
| Same-project pairs excluded from diversification interpretation | 17 |
| Different-project expression pairs | 9,436 |
| **Unique project-pair groups** | **7,381** |
| Expression-pair reserve passes, 12-month joint operating shock | 7,730 |
| Expression-pair reserve passes, 24-month joint operating + actual-credit shock | 1,735 |
| Project pairs where every modeled variant passes, 12 months | 6,052 |
| Project pairs where at least one variant passes, 12 months | 6,221 |
| Project pairs where every modeled variant passes, 24 months + credit | 1,204 |
| Project pairs where at least one variant passes, 24 months + credit | 1,465 |

Thus 169 project-pair groups have variant-sensitive 12-month pass/fail and 261 have variant-sensitive 24-month-plus-credit pass/fail. Do not choose the favourable variant silently. Project-level ranges in the JSON expose both. These counts describe model alternatives, not 7,381 feasible portfolios or independent opportunities.

## Portfolios selected before calculation

| ID / task | Expressions | Entry at base | Annual base cashflow | Minimum cash: 12m joint | Minimum cash: 24m joint | Minimum cash: 24m joint + credit | Starting cash needed for RM150k reserve in final column |
|---|---|---:|---:|---:|---:|---:|---:|
| P0 Cash-only no-purchase control | None | 0 | 0 | 500,000 | 500,000 | 500,000 | 150,000 |
| P1 Three lower-ticket ordinary-income research leads | KV01, R306, R231 | 202,000 | -5,143 | 158,818 | 130,436 | 1,320 | 648,680 |
| P2 Three mature family research leads | R315, R316, R350 | 355,000 | -1,675 | -28,756 | -73,312 | -310,464 | 960,464 |
| P3 One compact plus one family study | R306, R350 | 146,000 | -2,907 | 257,370 | 236,739 | 139,244 | 510,756 |
| P4 Four tempting arithmetic outliers, all specially held | R208, R309, R219, R353 | 207,250 | 7,576 | 132,605 | 116,456 | 9,079 | 640,921 |
| P5 Two high-quantum prime controls | R314, R323 | 632,500 | -63,224 | -377,472 | -510,843 | -1,004,909 | 1,654,909 |
| P6 Three middle-ticket family controls | R201, R308, R350 | 246,350 | -7,854 | 102,891 | 66,932 | -92,355 | 742,355 |

P0 keeps RM500,000 nominal cash with no interest, tax or inflation modeled. It is the no-purchase capacity control, not a risk-free real-return benchmark.

P1 (Maxim/Eve/Zeva) survives the 12-month operating shock with only about RM8,818 above the reserve. At 24 months it breaches the reserve; with actual-credit stress its minimum is roughly RM1,320. Three lower tickets are not automatically a conservative portfolio.

P2 (Pines/Windsor/East Lake) already uses RM355,000 at entry, leaving less than the RM150,000 reserve. Its near-neutral aggregate base income cannot undo entry concentration. The initial reserve failure must not be hidden behind an attractive family-rent narrative.

P3 (Eve/East Lake) survives the 24-month operating shock but breaches the reserve by about RM10,756 with the stated actual-credit stress. The 12-month credit path still passes. This is a duration/funding reversal, not a recommendation to add exactly RM10,756 to a real investor's budget.

P4 (Centrestage/Amcorp/Neo/Arc) is the tempting positive-income portfolio. All four inputs have material admission holds. Even if their arithmetic were available, simultaneous works and operating shocks breach the reserve. Its five-year flat-price aggregate profit remains negative.

P5 (DC 1152 / TRX 850) cannot be funded from the assumed starting cash even before carry. P6 (Kuchai/Mahkota/East Lake) has less extreme individual tickets but also fails the joint shock. The rejected interpretations are retained rather than removed to produce a passing allocation.

## Exposure ledger

| Shared exposure | Relevant groups / examples | Why distinct names do not diversify it |
|---|---|---|
| Rate, bank valuation and borrower eligibility | Every leveraged case | One credit regime can increase entry equity and future buyer burden across regions. No simultaneous loan approvals are assumed. |
| Ordinary compact investor demand | Eve, Maxim, Skypod, Zeva, Solstice and similar products | Tenant tasks differ, yet a common required-yield repricing can compress exits. Young-owner backup remains unproved. |
| Mature common-asset repairs | Pines, Windsor, East Lake, Mahkota and older-family controls | Separate buildings can experience contemporaneous funding needs; RM30k/asset is a scenario, not a works quotation. |
| Institutional/provider substitution | Cyberjaya, Serdang/UPM, Sunway/Subang, airport/university corridors | Institutions also supply accommodation; access/eligibility and schedules differ. Campus or employment counts are not tenant allocations. |
| Local family / landed alternatives | Outer Cheras, western and outer corridors | Household budgets and routes can cap high-rise demand; landed is a functional substitute, not a pooled PSF comparable. |
| Delivered and future competitive stock | Prime KL, Ara, north/west and growth corridors | Completion dates change the competition set. Unsold, delivered, advertised and occupied are distinct measures. |
| Same project and shared locality | 15 multi-expression project groups; Pines/Windsor locality; different ParkCity phases | Project variants share works/use risk; distinct phases can still share tenant, access, credit and supply exposure. |

There are 15 multi-expression groups plus singletons; the singleton R205 in the design is an identity marker, not an additional duplicate group.

## Terminal recovery is a buyer burden

Five-year break-even and the illustrative 8% equity hurdle are required exit amounts, not forecasts or fair values. Principal is counted once; debt remains payable at exit. Base five-year profit assumes the acquisition price repeats at sale, 3% disposal costs and existing modeled carry. It is pre-tax and excludes unquoted transaction-specific costs.

The investor-exit diagnostic capitalises eleven paid months less fee/other allowances at **5%, 6% and 7% operating yield before finance and tax**. These are hypothetical buyer requirements, not market capitalisation rates and not the user's separate 6% gross preference. Future net income is held at the current scenario to expose dependence on growth/yield compression; this does not forecast unchanged rent.

| Research control | Nominal recovery price | Operating yield at recovery | Income-only value at hypothetical 6% operating yield | Buyer cash at recovery: 90% standard | Buyer cash at recovery: 70% stress |
|---|---:|---:|---:|---:|---:|
| KV01 | 417,569 | 3.83% | 266,667 | 82,635 | 166,149 |
| R306 | 422,557 | 3.90% | 274,667 | 78,384 | 162,895 |
| R231 | 237,935 | 3.88% | 154,000 | 55,690 | 103,277 |
| KV14 | 220,164 | 4.20% | 154,000 | 48,025 | 92,057 |
| R315 | 752,224 | 4.44% | 556,667 | 152,834 | 303,278 |
| R316 | 791,595 | 4.42% | 583,333 | 143,739 | 302,058 |
| R342 | 494,421 | 4.29% | 353,733 | 109,163 | 208,047 |
| R350 | 379,720 | 4.21% | 266,667 | 76,958 | 152,902 |
| R321 | 428,369 | 4.62% | 330,000 | 89,255 | 174,929 |
| R353 | 244,881 | 4.63% | 189,000 | 61,732 | 110,709 |

Buyer cash above includes the same illustrative 5% acquisition allowance and refurbishment amount at the hypothetical recovery price. The additional future-buyer stress uses 70% LTV / 5.5% / 25 years; it is separate from the frozen engine's retained 80% future-buyer diagnostic and from the user's 90% standard. No lender rule or actual eligibility is asserted.

An income investor can be a valid exit buyer, but must have a reason and ability to fund the price. A resident buyer can also be valid where willingness and funding are evidenced. Neither is assumed to pay the seller's break-even. If a new mechanism supports higher net rent or a different household premium, it must pass the existing evidence and falsification process.

## Limits that affect the decision

The fixed stress is deliberately joint, not a probability distribution or maximum conceivable loss. It does not model all personal liabilities, lender portfolio limits, taxes, sale execution delays beyond selected horizons, every possible special assessment or stochastic vacancy. Additional unknown costs are not zero; the common replay includes an explicit extra-cost sensitivity. These limitations preserve Defer and the burden of evidence rather than justify a compensating arbitrary discount.

All 2,622 scenario evaluations and 180 rank-grid cells remain reproducible; exact monthly per-case cashflows and study paths allow minimum-month checks. The regional 74 prior branches remain source-pinned alternatives. No current investment becomes Deploy through programme aggregation.
