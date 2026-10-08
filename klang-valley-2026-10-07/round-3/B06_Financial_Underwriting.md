# B06 financial underwriting

Cutoff 7 October 2026. Fourteen conditional operating expressions, eight case-specific branches and two threshold-only Kwasa controls. The [inputs](B06_Case_Inputs.json), [full monthly results](B06_Financial_Results.json) and [read-only model](b06_financial_model.py) permit exact replay. All G0 stop/G9 Defer; arithmetic does not clear a purchase.

## Basis and limitations

Common standard: 90% purchase-price LTV, 4%, 35 years; simplified monthly balance = whole-unit rent minus full instalment minus management-fee proxy. 6% gross is preferred. Fee is an unverified service/sinking proxy, except advertiser amounts explicitly noted; true management-only and total invoices remain unverified.

Separate cashflow: 11 paid months/year; other-cost allowances; initial works; 5% acquisition and 3% disposal allowances; five-year hold; no rent/price growth. Pre-tax; unit-specific legal/tax/credit/insurance/letting and capital costs remain unquoted. Unknown is not verified zero. The extra-cost sensitivity adds 1200/year and 5000 at exit, not a tax estimate.

An 8% equity hurdle is illustrative, not user-approved. Monthly discounting and principal conservation avoid counting principal twice. Remaining debt is repaid at exit; required prices below are burdens, not forecasts or supported market ceilings. Actual valuation/term sensitivity is separate from the unchanged common 90/4/35 comparison.

## Base results

All amounts RM. These prices/rents are conditional inputs from advertisements or inherited assumptions, not authenticated effective offers or leases.

| ID | Price | Rent/mo | Fee/mo | Gross | Standard balance/mo | Annual net carry | Entry cash |
|---|---:|---:|---:|---:|---:|---:|---:|
| KV12 | 310, 000 | 1, 600 | 250 | 6.19% | 115 | -2, 384 | 66, 500 |
| R226 | 250, 000 | 1, 450 | 220 | 6.96% | 234 | -445 | 52, 500 |
| R227 | 450, 000 | 2, 100 | 300 | 5.60% | 7 | -4, 419 | 87, 500 |
| R228 | 390, 000 | 1, 500 | 300 | 4.62% | -354 | -8, 150 | 73, 500 |
| R229 | 350, 000 | 1, 500 | 250 | 5.14% | -145 | -5, 397 | 67, 500 |
| R250 | 430, 000 | 1, 800 | 315 | 5.02% | -229 | -6, 942 | 84, 500 |
| R330 | 350, 000 | 1, 500 | 250 | 5.14% | -145 | -5, 637 | 77, 500 |
| R331 | 450, 000 | 2, 100 | 300 | 5.60% | 7 | -4, 179 | 82, 500 |
| R332 | 410, 000 | 1, 700 | 310 | 4.98% | -244 | -6, 786 | 76, 500 |
| R333 | 350, 000 | 1, 800 | 375 | 6.17% | 30 | -3, 840 | 77, 500 |
| R334 | 250, 000 | 1, 200 | 160 | 5.76% | 44 | -2, 835 | 52, 500 |
| R335 | 265, 000 | 1, 500 | 250 | 6.79% | 194 | -1, 332 | 59, 750 |
| R336 | 335, 000 | 1, 500 | 230 | 5.37% | -65 | -4, 680 | 75, 250 |
| R337 | 300, 000 | 1, 500 | 250 | 6.00% | 55 | -2, 766 | 60, 000 |

All 14 base annual cashflows are negative, even where simplified monthly coverage passes. This is a reconciled cost/collection difference, not automatically an Evidence–Judgment Divergence. Current standard-shortfall cases are lowest research priority, not permanent structural Rejects.

| ID | Year 5 debt | Nominal break-even exit | Exit for illustrative 8% | Flat-price total profit | Buyer standard payment at BE | Buyer stress payment at BE |
|---|---:|---:|---:|---:|---:|---:|
| KV12 | 258, 756 | 347, 605 | 382, 789 | -36, 477 | 1, 385 | 1, 708 |
| R226 | 208, 674 | 271, 545 | 297, 766 | -20, 899 | 1, 082 | 1, 334 |
| R227 | 375, 614 | 500, 214 | 547, 934 | -48, 708 | 1, 993 | 2, 457 |
| R228 | 325, 532 | 453, 382 | 498, 342 | -61, 480 | 1, 807 | 2, 227 |
| R229 | 292, 144 | 398, 586 | 437, 582 | -47, 128 | 1, 588 | 1, 958 |
| R250 | 358, 920 | 492, 920 | 541, 927 | -61, 032 | 1, 964 | 2, 422 |
| R330 | 292, 144 | 410, 132 | 454, 234 | -58, 328 | 1, 634 | 2, 015 |
| R331 | 375, 614 | 493, 823 | 538, 856 | -42, 508 | 1, 968 | 2, 426 |
| R332 | 342, 226 | 466, 656 | 511, 596 | -54, 956 | 1, 860 | 2, 293 |
| R333 | 292, 144 | 400, 868 | 443, 038 | -49, 342 | 1, 597 | 1, 969 |
| R334 | 208, 674 | 283, 865 | 312, 687 | -32, 849 | 1, 131 | 1, 395 |
| R335 | 221, 195 | 296, 501 | 327, 227 | -30, 556 | 1, 182 | 1, 457 |
| R336 | 279, 624 | 389, 971 | 431, 919 | -53, 322 | 1, 554 | 1, 916 |
| R337 | 250, 409 | 334, 267 | 366, 708 | -33, 239 | 1, 332 | 1, 642 |

Buyer stress is 80% LTV/5.5%/25 years: it also requires more equity. It is not the acquisition comparison standard or a credit offer. Future buyer debt-service affordability, deposits, title acceptance and willingness to pay remain unverified. All 14 flat-price five-year profits are negative.

## What must change?

Annual neutrality assumes 11 paid months and current other-cost allowance. Price thresholds hold rent/fee/other constant; they are not buy limits, supported valuations or adequate margins of safety.

| ID | Rent for standard coverage | Rent for 6% gross | Rent for annual neutrality | Price for standard coverage | Price for 6% gross | Price for annual neutrality |
|---|---:|---:|---:|---:|---:|---:|
| KV12 | 1, 485 | 1, 550 | 1, 817 | 338, 773 | 320, 000 | 260, 144 |
| R226 | 1, 216 | 1, 250 | 1, 490 | 308, 660 | 290, 000 | 240, 696 |
| R227 | 2, 093 | 2, 250 | 2, 502 | 451, 697 | 420, 000 | 357, 593 |
| R228 | 1, 854 | 1, 950 | 2, 241 | 301, 131 | 300, 000 | 219, 575 |
| R229 | 1, 645 | 1, 750 | 1, 991 | 313, 678 | 300, 000 | 237, 141 |
| R250 | 2, 029 | 2, 150 | 2, 431 | 372, 650 | 360, 000 | 284, 820 |
| R330 | 1, 645 | 1, 750 | 2, 012 | 313, 678 | 300, 000 | 232, 122 |
| R331 | 2, 093 | 2, 250 | 2, 480 | 451, 697 | 420, 000 | 362, 612 |
| R332 | 1, 944 | 2, 050 | 2, 317 | 348, 810 | 340, 000 | 268, 091 |
| R333 | 1, 770 | 1, 750 | 2, 149 | 357, 536 | 360, 000 | 269, 706 |
| R334 | 1, 156 | 1, 250 | 1, 458 | 260, 980 | 240, 000 | 190, 716 |
| R335 | 1, 306 | 1, 325 | 1, 621 | 313, 678 | 300, 000 | 237, 141 |
| R336 | 1, 565 | 1, 675 | 1, 925 | 318, 697 | 300, 000 | 237, 141 |
| R337 | 1, 445 | 1, 500 | 1, 751 | 313, 678 | 300, 000 | 242, 160 |

A catalyst thesis must explain which rent or price hurdle can be crossed, by whom, after what operational change and on what timetable. Require measured leases/bids and funded downside carry. None of these thresholds demonstrates that the market will deliver the required outcome.

## Costed counterexamples and unresolved price branches

| Branch | Standard monthly balance | Year 1 carry | Entry | Nominal exit BE | Flat exit profit |
|---|---:|---:|---:|---:|---:|
| Urban studio lower-rent counterexample | -16 | -3, 195 | 52, 500 | 285, 721 | -34, 649 |
| Urban studio 220 k header only | 353 | 990 | 48, 000 | 233, 696 | -13, 285 |
| Urban studio 270 k body only | 154 | -1, 401 | 55, 500 | 296, 778 | -25, 975 |
| Spring Ville 220 k marketing-price control | 163 | -1, 400 | 48, 000 | 246, 016 | -25, 235 |
| Spring Ville furnished 1500 | 344 | 465 | 72, 500 | 287, 473 | -36, 349 |
| Urban family furnished 1900 | 130 | -2, 740 | 87, 500 | 405, 508 | -53, 842 |
| The Ridge furnished 2400 | 307 | -5, 679 | 102, 500 | 502, 379 | -50, 808 |
| D'Sara auction reserve illustration | 509 | -16, 453 | 73, 165 | 283, 692 | -60, 714 |

Urban 220 k and 270 k are mutually unresolved ad interpretations, not two authenticated opportunities. At 220 k the same 1450 rent yields annual+990; at 270 k it yields-1401. The favourable branch still loses money at a flat exit. The independent 1200 partial-rent control fails simplified coverage. Condition mismatch is explicit rather than silently applying the best rent to the cheapest header.

Spring 220 k is a different financing-promoted ad with unknown rights/net terms. The 1500 furnished branch adds 20000 to works; annual+465 is thin and terminal economics remain adverse. Urban family 1900 also adds 10000 works and stays annual negative. Ridge 2400 adds 20000 works and models 3 months initial vacancy: a furnishing promise is neither immediate nor free.

D'Sara 221100 is an 861-sf auction reserve illustration, not R332's 805-sf ordinary sale. It uses 40000 works, 12 initial no-rent months and 10000 exit buffer. Exact auction terms, loan draw, possession, arrears and costs are unknown; this is not a bid limit, complete auction model or assessed worst case. It is excluded from ordinary rank/pair comparisons.

## Kwasa without invented rent

| Control | Price floor | Fee proxy | Standard rent needed |6% gross rent | Annualneutral rent | Entry allowance | Fully drawn 12 mo no-income carry |
|---|---:|---:|---:|---:|---:|---:|---:|
| B06-T 01 | 494, 000 | 250 | 2, 219 | 2, 470 | 2, 617 | 94, 100 | 28, 783 |
| B06-T 02 | 498, 100 | 302 | 2, 287 | 2, 491 | 2, 691 | 99, 715 | 29, 606 |

T 01 Tujuh uses a published 494 kminimum, not a confirmed 550 sf package. T 02 D'Evia uses agency 498100 and 657 x 0.46 fee. No current achieved rent is available for either. These are post-completion thresholds; no operating gross yield, current cashflow rank or terminal IRR is asserted.

The 12 month fully drawn carry illustration is a timing sensitivity only. It is not actual progressive interest, a forecast, a maximum loss or a replacement for SPA milestones, draw schedule, delayed completion, fitout, taxes and first tenant evidence. Their whole construction-to-exit chain stays unresolved at G7.

## Stress, opportunity cost and rank reversals

Each ordinary expression has 14 evaluations: base, low/high rent, 5.5% rate, rent down 20%, fee up 20%, 12 initial no-income months, 30000 works month 24, bank valuation down 15%, 25 yearactual term, 72 month hold, extra-cost buffer, combined 5 year shock and combined 12 monthfunding test. Eight branches bring total financial evaluations to 204.

All 204 passed independent debt, principal, economic-cost and discounted-exit identities. The frozen engine's rent_factor sensitivity leaves its standard_monthly_balance as the original common reference; adjusted collected income is in cashflows. The explicit rank grid separately recomputes simplified coverage at each tested rent. This convention must not be mistaken for unchanged actual coverage.

Synthetic portfolio: 500000 initial cash, 150000 protected reserve; no salary, refinance or sale. Combined 12 month shock applies 5.5% interest, 80% rent, 120% fee, only 6 paid months, 30000 immediate works per asset. All 91/91 two-asset pairs pass that cash floor. This does not establish suitable concentration, real household funding, lender debt-service acceptance or downside safety. Exact monthly minima are saved.

Nearby pairs share local tenant budgets, road access, management-cost inflation and refinancing conditions. A compact/family pair in the same building remains correlated despite different labels. New-launch Kwasa controls are excluded because their actual draw/timing is unavailable.

The 36 rent-grid cells compare Urban studio/family, PV 21/Zen, 168 Park/Selayang Point andRidge/Saville. Coverage reversals occur; someRidge/Saville combinations tie because equal price/fee produces identical simplified burden. These are scenarios, not probabilities or overall asset ranks. Entry/legal/management uncertainty remains an independent decision constraint.

Without evidenced appreciation, even a funded hold can earn a poor return. Keep cash and alternative acquisitions in the opportunity set. The full programme comparison will use the same basis after B07/B08 and the B01/B02 substantive audits.
