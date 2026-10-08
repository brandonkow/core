# Whole-programme financial underwriting

Version: KV-PROGRAMME-INTEGRATION-2026-10-08. Source cutoff: 8 October 2026; each market observation retains its own original date. **Conditional arithmetic only: all 138 G0 STOP / G9 Defer.** The [inputs](Inputs.json), [pure calculation builder](Scenario_Builder.py) and [results](Financial_Results.json) reproduce this release.

## Financial basis and interpretation

The frozen standard remains 90% of acquisition price, 4% interest and 35 years. Preferred gross yield is 6%. Monthly standard balance is assumed rent less the standard full loan instalment and the case's combined management/sinking proxy. The source proxy is not an authenticated current invoice.

Base annual cashflow uses eleven paid months less twelve instalments, fee and other operating allowances. Base vacancy occurs in month one of each year. Five-year cashflows track amortisation monthly. Entry is 15% of price plus refurbishment: 10% equity and an illustrative 5% acquisition-cost allowance. Disposal allowance is 3%. All costs are pre-tax planning assumptions, not legal/tax/contractor quotations; unknown actual liabilities do not become zero.

The 8% equity hurdle is illustrative, not a new user requirement. Its required exit discounts monthly carry at an effective annual 8%. Break-even and hurdle prices are burdens, not supported market values. Nominal flat-price profit deducts remaining debt, entry and carrying cash once; principal is not counted twice.

Nineteen common scenarios per expression create 2,622 evaluations: base, 5.5% rate, rent -20%, fee +20%, twelve initial unpaid months, RM30k works in month 24, bank value -15%, 25-year actual term, 72-month exit, RM1,200 annual plus RM5,000 exit unquoted-cost buffer, five-year combined stress, combined 12/24-month no-sale, combined actual-credit 12/24/60-month paths, and case-specific low/high rent and low-rent-plus-fee stress.

The combined scenario uses 5.5%, rent -20%, fee +20%, six paid months in year one and RM30k works in month one. Later years return to eleven paid months at the reduced rent. Actual-credit adds a 15% bank-value haircut and 25-year term; the common comparison still uses 90% / 4% / 35. Existing source branches are preserved separately rather than favourable assumptions being selected into base.

## Aggregate results

| Measure | Expressions | Interpretation |
|---|---:|---|
| Monthly standard non-shortfall | 56 / 138 | Meets the user's simplified comparison on assumed inputs |
| Current monthly shortfall | 82 / 138 | Lowest ordinary-income research priority, not permanent Reject |
| Gross scenario yield at least 6% | 40 / 138 | Preferred gross metric, not cost-complete return |
| Nonnegative annual base cashflow | 5 / 138 | All five have material identity/offer/ordinary-lease holds |
| Nonnegative five-year flat-price profit | 1 / 138 | Quarantined R208, about RM431 before tax/unquoted costs |
| Nonnegative annual cashflow at case lower rent plus fee +20% | 0 / 138 | Sensitivity result, not a probability of loss |
| Current Deploy | 0 | No result authenticates an investable parcel or valuation |

The five positive annual scenarios are R208, R309, R219, R321 and R353. The finite sample is purposive and includes deliberately suspicious counterexamples. No prevalence estimate for the entire property market follows.

## Full 138-expression base chain

All amounts RM; yield is gross. Prices and rents are assumptions. Rounding in this table is for display; exact calculations and monthly cashflows are in JSON.

| ID / expression | Price | Rent | Gross | Entry cash | Monthly standard | Annual carry | Five-year nominal recovery sale | Illustrative 8% required sale | Flat-price five-year profit |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| C01 M Vertica | 489,000 | 2,400 | 5.89% | 93,350 | 101 | -2,984 | 532,408 | 581,430 | -42,106 |
| C02 Shamelin Star | 700,000 | 2,600 | 4.46% | 130,000 | -589 | -11,474 | 795,523 | 871,763 | -92,657 |
| C03 EkoCheras duplex | 520,000 | 2,300 | 5.31% | 93,000 | -122 | -5,566 | 572,035 | 623,736 | -50,474 |
| C04 Aster Type B | 540,000 | 2,400 | 5.33% | 101,000 | -102 | -5,423 | 596,752 | 652,187 | -55,050 |
| C05 Maxim Residences | 480,000 | 2,400 | 6.00% | 97,000 | 137 | -2,553 | 526,208 | 576,517 | -44,822 |
| C06 Riana South | 595,000 | 2,700 | 5.45% | 109,250 | -71 | -5,353 | 652,225 | 711,641 | -55,508 |
| C07 Green Residence | 540,000 | 2,000 | 4.44% | 106,000 | -552 | -10,423 | 627,680 | 691,005 | -85,050 |
| C08 Windows on the Park large | 900,000 | 3,500 | 4.67% | 180,000 | -936 | -17,138 | 1,048,367 | 1,155,299 | -143,916 |
| C09 Scot Pine | 498,000 | 2,200 | 5.30% | 114,700 | -235 | -7,414 | 585,000 | 649,234 | -84,390 |
| KV01 Maxim Residences | 380,000 | 2,000 | 6.32% | 77,000 | 186 | -2,171 | 417,569 | 457,687 | -36,442 |
| KV02 Lavile Kuala Lumpur | 699,000 | 3,200 | 5.49% | 119,850 | 115 | -4,826 | 749,931 | 814,002 | -49,403 |
| KV03 Akasa | 410,000 | 1,800 | 5.27% | 81,500 | -64 | -4,726 | 461,192 | 506,283 | -49,656 |
| KV04 You Vista | 450,000 | 2,000 | 5.33% | 87,500 | -73 | -5,279 | 504,647 | 553,301 | -53,008 |
| KV05 Emerald Residence | 390,000 | 1,500 | 4.62% | 78,500 | -374 | -8,150 | 458,536 | 505,916 | -66,480 |
| KV06 Windows on the Park | 480,000 | 1,700 | 4.25% | 92,000 | -513 | -10,493 | 561,981 | 618,544 | -79,522 |
| KV07 Citizen 2 | 430,000 | 1,900 | 5.30% | 79,500 | -64 | -5,062 | 478,074 | 522,594 | -46,632 |
| R201 Kuchai Avenue | 359,999 | 1,800 | 6.00% | 74,000 | 95 | -3,055 | 401,820 | 441,424 | -40,566 |
| R202 OUG Parklane | 312,000 | 1,500 | 5.77% | 66,800 | -23 | -4,180 | 358,891 | 396,195 | -45,484 |
| R203 Desa Green | 345,000 | 1,600 | 5.57% | 66,750 | -15 | -3,938 | 385,989 | 423,022 | -39,760 |
| R204 Endah Promenade | 298,000 | 1,600 | 6.44% | 64,700 | 152 | -1,930 | 333,084 | 366,892 | -34,031 |
| R205 Aurora Suites Bukit Jalil | 350,000 | 1,800 | 6.17% | 72,500 | 175 | -1,857 | 385,493 | 423,039 | -34,428 |
| R206 Trion KL | 579,999 | 2,700 | 5.59% | 107,000 | 109 | -4,035 | 630,206 | 687,068 | -48,701 |
| R243 Shamelin Star | 515,000 | 2,200 | 5.13% | 97,250 | -152 | -6,427 | 576,551 | 631,244 | -59,705 |
| R244 Emerald Hills | 570,000 | 2,100 | 4.42% | 105,500 | -471 | -10,157 | 651,612 | 714,422 | -79,164 |
| R245 Landmark Residence 2 | 268,000 | 1,300 | 5.82% | 60,200 | 2 | -3,196 | 309,152 | 342,123 | -39,917 |
| R301 Desa Green 715-sf two-bedroom control | 430,000 | 1,700 | 4.74% | 79,500 | -314 | -7,622 | 491,270 | 538,592 | -59,432 |
| R302 The Tropika 732-sf two-bedroom control | 650,000 | 2,800 | 5.17% | 122,500 | -130 | -7,003 | 721,719 | 789,403 | -69,567 |
| R303 M Oscar 708-sf two-bedroom control | 528,000 | 2,300 | 5.23% | 99,200 | -84 | -5,709 | 586,045 | 640,905 | -56,304 |
| R304 Silk Sky 484-sf compact control | 250,000 | 1,300 | 6.24% | 52,500 | 104 | -1,855 | 278,813 | 306,568 | -27,949 |
| R362 Astaka Heights 1115-sf older family control | 388,000 | 1,600 | 4.95% | 88,200 | -276 | -7,074 | 461,271 | 512,170 | -71,073 |
| R363 Prima Midah Heights 1460-sf mature family control | 550,000 | 1,800 | 3.93% | 107,500 | -742 | -13,101 | 651,637 | 718,621 | -98,588 |
| R364 Damai Hillpark 1020-sf family index control | 390,000 | 1,700 | 5.23% | 83,500 | -114 | -5,230 | 448,640 | 495,236 | -56,880 |
| R365 Arena Green 730-sf residential two-bedroom control | 268,000 | 1,300 | 5.82% | 65,200 | 72 | -2,596 | 311,214 | 345,937 | -41,917 |
| KV08 Pacific Place | 370,000 | 1,800 | 5.84% | 70,500 | 26 | -3,893 | 411,139 | 449,981 | -39,904 |
| R207 PJ8 | 390,000 | 2,000 | 6.15% | 78,500 | 116 | -3,010 | 432,042 | 473,817 | -40,780 |
| R208 Centrestage Designer Suite | 150,000 | 1,500 | 12.00% | 42,500 | 682 | 4,527 | 149,556 | 165,420 | 431 |
| R209 Ken Damansara | 630,000 | 2,300 | 4.38% | 119,500 | -591 | -12,026 | 727,311 | 799,018 | -94,391 |
| R210 Sterling | 640,000 | 2,000 | 3.75% | 121,000 | -930 | -15,805 | 756,937 | 833,505 | -113,429 |
| R211 Tropicana Avenue | 518,000 | 2,300 | 5.33% | 92,700 | -64 | -5,471 | 569,512 | 620,961 | -49,966 |
| R212 Encorp Strand Residence | 400,000 | 1,600 | 4.80% | 75,000 | -314 | -7,528 | 460,328 | 505,345 | -58,518 |
| R305 PJ Midtown | 690,000 | 3,000 | 5.22% | 133,500 | -110 | -6,956 | 767,236 | 840,235 | -74,919 |
| R306 Eve Suite compact | 390,000 | 2,000 | 6.15% | 73,500 | 166 | -2,170 | 422,557 | 460,979 | -31,580 |
| R307 Eve Suite two-bedroom | 560,000 | 2,700 | 5.79% | 104,000 | 68 | -4,519 | 612,398 | 668,346 | -50,826 |
| R308 Kelana Mahkota | 499,000 | 2,400 | 5.77% | 99,850 | 82 | -4,062 | 553,272 | 606,637 | -52,644 |
| R309 Amcorp compact | 225,000 | 1,600 | 8.53% | 53,750 | 453 | 1,681 | 240,365 | 264,860 | -14,904 |
| R310 Casa Tropicana | 600,000 | 2,400 | 4.80% | 115,000 | -351 | -9,252 | 682,554 | 749,021 | -80,077 |
| R311 Encorp Strand two-bedroom | 499,999 | 2,600 | 6.24% | 95,000 | 108 | -3,950 | 548,553 | 599,492 | -47,098 |
| KV09 First Residence | 389,999 | 1,950 | 6.00% | 83,500 | 96 | -3,440 | 439,411 | 484,073 | -47,930 |
| KV10 OOAK serviced apartments @ Kiara 163 | 850,000 | 3,500 | 4.94% | 147,500 | -307 | -10,787 | 939,099 | 1,023,244 | -86,426 |
| R213 South View | 560,000 | 2,600 | 5.57% | 99,000 | 68 | -4,419 | 606,727 | 660,123 | -45,326 |
| R214 Sinaran TTDI | 948,000 | 3,500 | 4.43% | 167,200 | -728 | -15,233 | 1,066,658 | 1,165,279 | -115,098 |
| R215 DC Residensi | 1,135,000 | 4,000 | 4.23% | 200,250 | -1,173 | -21,675 | 1,294,854 | 1,416,742 | -155,058 |
| R216 Cliveden Plaza Damas 3 | 250,000 | 1,500 | 7.20% | 52,500 | 254 | -255 | 270,566 | 296,586 | -19,949 |
| R217 Prima Duta | 600,000 | 2,500 | 5.00% | 120,000 | -371 | -9,952 | 691,317 | 761,004 | -88,577 |
| R218 Menjalara 18 | 700,000 | 2,500 | 4.29% | 125,000 | -689 | -13,414 | 800,368 | 876,324 | -97,357 |
| R219 Neo Damansara | 220,000 | 1,399 | 7.63% | 53,000 | 312 | 549 | 241,124 | 266,470 | -20,490 |
| R246 Westside Three | 1,250,000 | 5,000 | 4.80% | 212,500 | -481 | -14,375 | 1,368,809 | 1,488,728 | -115,245 |
| R312 KL Gateway Residences | 850,000 | 3,200 | 4.52% | 147,500 | -547 | -12,767 | 949,305 | 1,035,585 | -96,326 |
| R313 TTDI Ascencia | 690,000 | 2,500 | 4.35% | 123,500 | -550 | -11,736 | 781,566 | 854,930 | -88,819 |
| R314 DC Residensi larger control | 1,800,000 | 5,400 | 3.60% | 310,000 | -2,573 | -40,475 | 2,077,147 | 2,273,356 | -268,832 |
| R315 Mont Kiara Pines | 700,000 | 3,800 | 6.51% | 145,000 | 561 | -74 | 752,224 | 823,312 | -50,657 |
| R316 Windsor Tower family | 750,000 | 4,000 | 6.40% | 137,500 | 511 | -865 | 791,595 | 859,978 | -40,347 |
| R317 United Point | 568,000 | 2,500 | 5.28% | 110,200 | -113 | -6,502 | 635,893 | 697,001 | -65,856 |
| R318 The Westside One compact | 840,000 | 3,000 | 4.29% | 146,000 | -767 | -15,209 | 951,741 | 1,039,965 | -108,388 |
| R319 Fortune Centra | 480,000 | 2,100 | 5.25% | 97,000 | -113 | -5,853 | 543,218 | 597,130 | -61,322 |
| R320 Surian Residences Mutiara | 720,000 | 3,000 | 5.00% | 128,000 | -269 | -8,870 | 797,250 | 869,717 | -74,933 |
| KV11 Angkasa Impian 2 | 440,000 | 2,000 | 5.45% | 86,000 | -3 | -4,681 | 491,412 | 538,675 | -49,870 |
| R220 Vortex KLCC | 770,000 | 3,300 | 5.14% | 140,500 | -218 | -8,921 | 853,425 | 932,064 | -80,923 |
| R221 TRX Residences | 1,150,000 | 4,300 | 4.49% | 192,500 | -733 | -16,093 | 1,270,995 | 1,382,992 | -117,365 |
| R222 Sentul Point | 420,000 | 1,800 | 5.14% | 83,000 | -134 | -5,564 | 475,664 | 522,413 | -53,994 |
| R223 Datum Jelatek Residence | 650,000 | 2,500 | 4.62% | 117,500 | -390 | -9,583 | 729,863 | 797,930 | -77,467 |
| R224 GCB Court boundary comparator | 455,000 | 1,950 | 5.14% | 98,250 | -193 | -6,908 | 528,430 | 584,085 | -71,227 |
| R225 28 Boulevard | 380,000 | 1,650 | 5.21% | 72,000 | -114 | -5,181 | 427,930 | 468,898 | -46,492 |
| R321 Parkview compact | 400,000 | 2,400 | 7.20% | 85,000 | 456 | 672 | 428,369 | 469,285 | -27,518 |
| R322 Lucentia studio - monthly-fee interpretation | 600,000 | 3,400 | 6.80% | 110,000 | -156 | -8,032 | 671,111 | 734,025 | -68,977 |
| R323 TRX Residences two-bedroom | 1,950,000 | 7,500 | 4.62% | 322,500 | -971 | -22,748 | 2,127,734 | 2,310,747 | -172,402 |
| R324 The Saffron family | 500,000 | 2,300 | 5.52% | 105,000 | -42 | -5,450 | 566,596 | 623,974 | -64,598 |
| R325 Seri Maya family - higher-price observed lead | 650,000 | 2,650 | 4.89% | 127,500 | -340 | -9,373 | 739,090 | 811,795 | -86,417 |
| R326 Ampang Hilir Tara family | 1,400,000 | 6,800 | 5.83% | 270,000 | 321 | -7,748 | 1,523,004 | 1,663,777 | -119,314 |
| R327 Pandan Mewah Heights family | 265,000 | 1,300 | 5.89% | 64,750 | 44 | -2,572 | 308,047 | 342,527 | -41,756 |
| R328 Titiwangsa Sentral family - stabilised scenario | 500,000 | 2,700 | 6.48% | 100,000 | 378 | -810 | 537,524 | 587,412 | -36,398 |
| R329 28 Boulevard lower-price studio lead | 280,000 | 1,650 | 7.07% | 67,000 | 284 | -400 | 312,075 | 345,305 | -31,113 |
| KV12 Platinum Lake PV21 | 310,000 | 1,600 | 6.19% | 66,500 | 115 | -2,384 | 347,605 | 382,789 | -36,477 |
| R226 Urban 360 | 250,000 | 1,450 | 6.96% | 52,500 | 234 | -445 | 271,545 | 297,766 | -20,899 |
| R227 Saville Melawati | 450,000 | 2,100 | 5.60% | 87,500 | 7 | -4,419 | 500,214 | 547,934 | -48,708 |
| R228 Amara | 390,000 | 1,500 | 4.62% | 73,500 | -354 | -8,150 | 453,382 | 498,342 | -61,480 |
| R229 D'Sara Sentral | 350,000 | 1,500 | 5.14% | 67,500 | -145 | -5,397 | 398,586 | 437,582 | -47,128 |
| R250 222 Residency | 430,000 | 1,800 | 5.02% | 84,500 | -229 | -6,942 | 492,920 | 541,927 | -61,032 |
| R330 Wangsa Metroview 1150-sf marketed three-bedroom | 350,000 | 1,500 | 5.14% | 77,500 | -145 | -5,637 | 410,132 | 454,234 | -58,328 |
| R331 The Ridge KL East 651-sf partly furnished compact | 450,000 | 2,100 | 5.60% | 82,500 | 7 | -4,179 | 493,823 | 538,856 | -42,508 |
| R332 D'Sara Sentral 805-sf marketed two-bedroom voluntary sale | 410,000 | 1,700 | 4.98% | 76,500 | -244 | -6,786 | 466,656 | 511,596 | -54,956 |
| R333 Urban 360 1001-sf family control | 350,000 | 1,800 | 6.17% | 77,500 | 30 | -3,840 | 400,868 | 443,038 | -49,342 |
| R334 Spring Ville 728-sf restricted family control | 250,000 | 1,200 | 5.76% | 52,500 | 44 | -2,835 | 283,865 | 312,687 | -32,849 |
| R335 168 Park Selayang 624-sf altered compact control | 265,000 | 1,500 | 6.79% | 59,750 | 194 | -1,332 | 296,501 | 327,227 | -30,556 |
| R336 Selayang Point 1108-sf family control | 335,000 | 1,500 | 5.37% | 75,250 | -65 | -4,680 | 389,971 | 431,919 | -53,322 |
| R337 Zen Suites Zetapark 677-sf studio/SOHO control | 300,000 | 1,500 | 6.00% | 60,000 | 55 | -2,766 | 334,267 | 366,708 | -33,239 |
| KV13 Skypod Residence | 380,000 | 2,000 | 6.32% | 77,000 | 166 | -2,411 | 418,807 | 459,191 | -37,642 |
| R230 Koi Prima | 290,000 | 1,300 | 5.38% | 58,500 | -106 | -4,728 | 334,228 | 368,080 | -42,901 |
| R231 Zeva Equine South | 210,000 | 1,200 | 6.86% | 51,500 | 183 | -802 | 237,935 | 264,013 | -27,097 |
| R232 Da Men | 428,000 | 2,100 | 5.89% | 79,200 | 64 | -3,727 | 469,159 | 512,093 | -39,925 |
| R233 Seri Atria | 295,000 | 1,300 | 5.29% | 64,250 | -106 | -4,727 | 344,453 | 381,087 | -47,970 |
| R234 Paramount Utropolis | 280,000 | 1,500 | 6.43% | 67,000 | 164 | -1,690 | 318,725 | 353,356 | -37,563 |
| R235 Trefoil Setia City | 260,000 | 1,000 | 4.62% | 54,000 | -266 | -6,113 | 310,914 | 344,064 | -49,387 |
| R236 Gravit8 Nordica | 328,000 | 1,300 | 4.76% | 69,200 | -237 | -6,305 | 386,088 | 426,872 | -56,345 |
| R249 Sunway GeoSense | 1,198,000 | 5,000 | 5.01% | 199,700 | -194 | -10,928 | 1,293,100 | 1,402,994 | -92,247 |
| R338 Kinrara Mas | 328,000 | 1,500 | 5.49% | 74,200 | -47 | -4,465 | 381,758 | 422,959 | -52,145 |
| R339 The Wharf Residence | 218,000 | 1,100 | 6.06% | 42,700 | 31 | -2,525 | 244,626 | 268,340 | -25,827 |
| R340 Univ 360 compact | 230,000 | 1,350 | 7.04% | 49,500 | 253 | -109 | 249,508 | 273,881 | -18,923 |
| R341 Univ 360 family | 320,000 | 1,700 | 6.38% | 68,000 | 95 | -2,962 | 360,737 | 397,312 | -39,515 |
| R342 Subang Avenue | 450,000 | 2,500 | 6.67% | 102,500 | 384 | -295 | 494,421 | 544,901 | -43,088 |
| R343 Suria Residence Bukit Jelutong | 476,000 | 1,800 | 4.54% | 86,400 | -405 | -9,058 | 545,368 | 597,647 | -67,287 |
| R344 Seri Pinang Setia Alam | 290,000 | 1,200 | 4.97% | 63,500 | -156 | -5,228 | 341,960 | 378,765 | -50,401 |
| R345 Impiria Residensi | 600,000 | 3,000 | 6.00% | 105,000 | 279 | -2,652 | 638,224 | 692,647 | -37,077 |
| R346 Nadayu 801 family | 405,000 | 1,800 | 5.33% | 90,750 | -164 | -6,167 | 473,853 | 525,022 | -66,787 |
| R347 BBK Condominium | 250,000 | 1,500 | 7.20% | 72,500 | 154 | -2,055 | 300,463 | 338,162 | -48,949 |
| R348 Suri Puteri family | 370,000 | 1,650 | 5.35% | 80,500 | -74 | -4,943 | 426,860 | 471,676 | -55,154 |
| R349 The Cruise Residence two-bedroom | 600,000 | 1,950 | 3.90% | 105,000 | -771 | -13,602 | 694,667 | 761,033 | -91,827 |
| R350 East Lake Residence family | 350,000 | 2,000 | 6.86% | 72,500 | 305 | -737 | 379,720 | 416,065 | -28,828 |
| R237 Evo SOHO Suite | 248,000 | 1,300 | 6.29% | 52,200 | 82 | -2,239 | 278,764 | 306,802 | -29,841 |
| R238 D'Cerrum | 250,000 | 1,000 | 4.80% | 52,500 | -216 | -5,515 | 297,679 | 329,438 | -46,249 |
| R239 Dwiputra Residences | 520,000 | 2,300 | 5.31% | 103,000 | -72 | -5,806 | 583,581 | 640,388 | -61,674 |
| R240 Geo Bukit Rimau | 500,000 | 1,900 | 4.56% | 100,000 | -372 | -8,770 | 578,554 | 637,116 | -76,198 |
| R241 Habitus Denai Alam | 390,000 | 1,650 | 5.08% | 73,500 | -164 | -5,780 | 441,165 | 483,524 | -49,630 |
| R242 GAIA Residences | 380,000 | 1,500 | 4.74% | 77,000 | -244 | -6,591 | 440,353 | 485,274 | -58,542 |
| R247 The Parque Residences | 470,000 | 1,500 | 3.83% | 90,500 | -673 | -11,735 | 558,231 | 615,404 | -85,584 |
| R248 Alanis Residence | 210,000 | 1,200 | 6.86% | 51,500 | 163 | -1,162 | 239,791 | 266,269 | -28,897 |
| KV14 Solstice @ Pan'gaea | 200,000 | 1,200 | 7.20% | 45,000 | 223 | -324 | 220,164 | 242,565 | -19,559 |
| R351 MKH Boulevard II | 270,000 | 1,500 | 6.67% | 65,500 | 224 | -731 | 303,634 | 336,474 | -32,625 |
| R352 Ascotte Boulevard | 218,000 | 900 | 4.95% | 47,700 | -189 | -5,085 | 262,977 | 291,912 | -43,627 |
| R353 The Arc | 220,000 | 1,500 | 8.18% | 58,000 | 373 | 820 | 244,881 | 272,368 | -24,135 |
| R354 Shaftsbury Putrajaya | 368,000 | 1,800 | 5.87% | 70,200 | 34 | -3,558 | 407,378 | 445,702 | -38,197 |
| R355 Alanis Residence compact | 249,000 | 1,200 | 5.78% | 57,350 | 28 | -2,667 | 287,139 | 318,122 | -36,995 |
| R356 Aman 1 Tropicana Urban Homes | 338,000 | 1,500 | 5.33% | 75,700 | -97 | -4,823 | 393,756 | 436,081 | -54,083 |
| R357 Habitus Denai Alam original compact control | 360,000 | 1,300 | 4.33% | 74,000 | -485 | -9,155 | 433,264 | 479,540 | -71,066 |
| R358 GAIA Residences larger family control | 500,000 | 1,700 | 4.08% | 90,000 | -572 | -10,730 | 578,348 | 634,206 | -75,998 |
| R359 Alanis Residence family control | 365,000 | 1,600 | 5.26% | 79,750 | -135 | -5,374 | 424,006 | 468,926 | -57,235 |
| R360 Savanna Executive Suites family | 350,000 | 1,500 | 5.14% | 67,500 | -155 | -5,517 | 399,205 | 438,334 | -47,728 |
| R361 Amber Residences compact two-bedroom | 430,000 | 1,700 | 4.74% | 89,500 | -254 | -6,902 | 497,868 | 549,228 | -65,832 |

## Decision thresholds for research controls

These are solutions to the assumed cashflow equations, not recommended bids or a validated margin of safety. Fixing rent, fees and costs while changing purchase price is a sensitivity, not evidence that the seller will transact or the lender will agree.

| ID | Rent for standard coverage | Rent for annual neutrality | Rent for 6% gross | Price for annual neutrality at assumed rent | Price for 6% gross at assumed rent |
|---|---:|---:|---:|---:|---:|
| C01 | 2,299 | 2,671 | 2,445 | 426,603 | 480,000 |
| C05 | 2,263 | 2,632 | 2,400 | 426,603 | 480,000 |
| KV01 | 1,814 | 2,197 | 1,900 | 334,590 | 400,000 |
| R201 | 1,705 | 2,078 | 1,800 | 296,112 | 360,000 |
| R204 | 1,448 | 1,775 | 1,490 | 257,635 | 320,000 |
| R365 | 1,228 | 1,536 | 1,340 | 213,720 | 260,000 |
| R208 | 818 | 1,088 | 750 | 244,669 | 300,000 |
| R306 | 1,834 | 2,197 | 1,950 | 344,628 | 400,000 |
| R308 | 2,319 | 2,769 | 2,495 | 414,056 | 480,000 |
| R309 | 1,147 | 1,447 | 1,125 | 260,144 | 320,000 |
| R219 | 1,087 | 1,349 | 1,100 | 231,474 | 279,800 |
| R315 | 3,239 | 3,807 | 3,500 | 698,457 | 760,000 |
| R316 | 3,489 | 4,079 | 3,750 | 731,916 | 800,000 |
| R321 | 1,944 | 2,339 | 2,000 | 414,056 | 480,000 |
| R328 | 2,322 | 2,774 | 2,500 | 483,065 | 540,000 |
| KV12 | 1,485 | 1,817 | 1,550 | 260,144 | 320,000 |
| R226 | 1,216 | 1,490 | 1,250 | 240,696 | 290,000 |
| KV13 | 1,834 | 2,219 | 1,900 | 329,571 | 400,000 |
| R231 | 1,017 | 1,273 | 1,050 | 193,226 | 240,000 |
| R234 | 1,336 | 1,654 | 1,400 | 244,669 | 300,000 |
| R342 | 2,116 | 2,527 | 2,250 | 443,834 | 500,000 |
| R350 | 1,695 | 2,067 | 1,750 | 334,590 | 400,000 |
| KV14 | 977 | 1,229 | 1,000 | 193,226 | 240,000 |
| R353 | 1,127 | 1,425 | 1,100 | 237,141 | 300,000 |

All 138 threshold rows remain in JSON. For example, Eve at RM2,000 assumed rent needs roughly RM2,197 for annual neutrality, or about RM344,628 entry price holding other inputs fixed. Neither is a rent forecast or purchase recommendation. Arena's annual-neutral rent is roughly RM1,536 despite its positive monthly standard at RM1,300; its plan/bath/fee mismatch remains unresolved.

## Rank robustness

| Preregistered comparison | Annual cash leaders appearing in the nine rent combinations | Interpretation |
|---|---|---|
| KV01 / R306 | KV01, R306 | Ordering reverses within this finite grid |
| R306 / R231 | R231, R306 | Ordering reverses within this finite grid |
| R306 / KV14 | KV14, R306 | Ordering reverses within this finite grid |
| R306 / R365 | R306, R365 | Ordering reverses within this finite grid |
| R201 / R308 | R201, R308 | Ordering reverses within this finite grid |
| R315 / R316 | R315, R316 | Ordering reverses within this finite grid |
| R315 / R350 | R315, R350 | Ordering reverses within this finite grid |
| R342 / R350 | R342, R350 | Ordering reverses within this finite grid |
| R321 / R328 | R321, R328 | Ordering reverses within this finite grid |
| R321 / R306 | R306, R321 | Ordering reverses within this finite grid |
| R353 / KV14 | KV14, R353 | Ordering reverses within this finite grid |
| R339 / R231 | R231, R339 | Ordering reverses within this finite grid |
| R340 / R341 | R340, R341 | Ordering reverses within this finite grid |
| R365 / R302 | R365 | No reversal within this grid only |
| C01 / KV01 | C01, KV01 | Ordering reverses within this finite grid |
| R362 / R243 | R243, R362 | Ordering reverses within this finite grid |
| R317 / R217 | R217, R317 | Ordering reverses within this finite grid |
| R345 / R350 | R345, R350 | Ordering reverses within this finite grid |
| R307 / R308 | R307, R308 | Ordering reverses within this finite grid |
| R327 / R329 | R327, R329 | Ordering reverses within this finite grid |

Nineteen of twenty comparisons reverse. The grid assigns no probabilities and does not treat asks as achieved rents. Different household tasks remain distinct even when their investment cashflows can be compared. Lower/high rents for legacy C01-C09 are explicitly scenario bounds, not fresh evidence.

## Terminal and portfolio consequences

See [Portfolio and terminal risk](Portfolio_and_Terminal_Risk.md) for 9,453 expression pairs, exclusion of 17 same-project alternatives, 7,381 unique project-pair ranges, seven preregistered study portfolios, shared exposures, investor yield and future buyer credit.

Actual purchase admission requires the existing gates, including a valid price reference, product/parcel and lease/operations evidence, actual financing, funded downside and a credible exit. A hypothetical positive branch can reopen research but cannot reduce the burden of proof or erase a source hold.
