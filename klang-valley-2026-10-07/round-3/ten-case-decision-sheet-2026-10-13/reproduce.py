"""Reproduce the ten-case decision sheet from frozen, dated repository inputs.
Run: python path/to/this/reproduce.py
Prints JSON to stdout; no network or output files. No new market evidence.
"""
import ast
import copy
import hashlib
import json
from pathlib import Path

BASELINE = "2e4a1c9d7d1c155456f9601fd217baa4044a075b"
PATHS = {
  "programme": "klang-valley-2026-10-07/round-3/programme-final/Inputs.json",
  "privacy": "klang-valley-2026-10-07/round-3/privacy-validation-2026-10-12/Financial_Results.json",
  "family": "klang-valley-2026-10-07/round-3/family-validation-2026-10-12/Financial_Results.json",
  "investor": "klang-valley-2026-10-07/round-3/investor-exit-validation-2026-10-13/Financial_Results.json",
  "anomaly": "klang-valley-2026-10-07/round-3/input-anomaly-validation-2026-10-13/Financial_Results.json",
  "engine": "execution-release-2026-10-07/financial_engine.py",
  "config": "execution-release-2026-10-07/financial_config.json"
}
BLOB_HASHES = {
  "programme": "c892fe220959f8d74d54d7c6f54cf14bfdd91c43",
  "privacy": "9c5084c4d63307ab1273078893a31af7ab009e34",
  "family": "22c1b6533312aefcaea037b848a01bb22ad7fe10",
  "investor": "b32e2f2d67f08511c909dd3435c66743cdff994c",
  "anomaly": "a6804d2fd69fd4d5fe31ca519b8b4d7009b2e377",
  "engine": "2fa3554d4b1358795d658efefe270ac53f27bbda",
  "config": "3e17c91823b093aa66f0930b2c012510d3b4528f"
}
BASES = [
    ("privacy", "E_base", "R306"), ("privacy", "M_base", "KV01"),
    ("family", "P_base", "R315"), ("family", "E_base", "R350"),
    ("family", "S_base", "R342"), ("investor", "Z_base", "R231"),
    ("investor", "S_base", "KV14"), ("anomaly", "P_base", "R321"),
    ("anomaly", "A_base", "R353"), ("anomaly", "L_base", "R322"),
]
BRANCHES = [
    ("privacy", "E_370k_2000"), ("privacy", "E_370k_2200"),
    ("privacy", "M_2500_two_bay_ad_is_not_base"),
    ("family", "P_rent3500"), ("family", "P_price780_rent3800"),
    ("family", "P_extra30k_refurb"), ("family", "S_rent2400"),
    ("family", "E_price330_rent2000"), ("family", "E_rent2200"),
    ("investor", "Z_rent850"), ("investor", "Z_rent1300"),
    ("investor", "S_rent1300"), ("anomaly", "P_rent_2300"),
    ("anomaly", "A_248k_1500"), ("anomaly", "L_quarterly_3400"),
    ("anomaly", "L_quarterly_3000"), ("anomaly", "L_060psf_3400"),
    ("anomaly", "L_060psf_3000"),
]

def blob_sha(text):
    data = text.encode("utf-8")
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()

def run(raw):
    for key, expected in BLOB_HASHES.items():
        assert blob_sha(raw[key]) == expected, "Source drift: " + PATHS[key]
    cfg = json.loads(raw["config"])
    assert (cfg["standard_ltv"], cfg["standard_rate"], cfg["standard_term_years"],
            cfg["baseline_paid_months_per_year"]) == (.9, .04, 35, 11)
    tree = ast.parse(raw["engine"])
    names = {"payment", "evaluate", "check_financial_identities"}
    functions = [x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name in names]
    assert {x.name for x in functions} == names
    ns = {"CFG": copy.deepcopy(cfg)}
    exec(compile(ast.Module(body=functions, type_ignores=[]), "<frozen-engine>", "exec"), ns)
    all_cases = {c["id"]: c for c in json.loads(raw["programme"])["source_cases"]}
    prior = {key: json.loads(raw[key]) for key in ("privacy", "family", "investor", "anomaly")}
    run_count = 0
    parity_count = 0
    root_count = 0

    def calculate(case, kwargs=None):
        nonlocal run_count
        result = ns["evaluate"](case, **(kwargs or {}))
        ns["check_financial_identities"](result, case, (kwargs or {}).get("exit_extra_cost", 0))
        run_count += 1
        return result

    def near(a, b):
        assert abs(a - b) < .00001, (a, b)

    def replay(packet, label):
        nonlocal parity_count
        matches = [s for s in prior[packet]["scenarios"] if s["label"] == label]
        assert len(matches) == 1
        old = matches[0]
        case = dict(all_cases[old["case_id"]], **old["case_overrides"])
        ns["CFG"] = copy.deepcopy(cfg)
        ns["CFG"]["baseline_paid_months_per_year"] = old["paid_months_per_year"]
        result = calculate(case, old["engine_arguments"])
        for key in ("price", "gross_yield", "rent_assumed", "fee_proxy", "other_cost_allowance",
                    "standard_instalment", "standard_monthly_balance", "entry_cash",
                    "cashflow_total", "terminal_debt", "terminal_nominal_breakeven",
                    "terminal_8pct_required"):
            near(result[key], old[key])
        for a, b in zip(result["cashflow_by_year"], old["cashflow_by_year"]):
            near(a, b)
        assert len(result["cashflow_by_year"]) == len(old["cashflow_by_year"])
        for key in ("0.8", "1", "1.15"):
            near(result["profit_by_exit_multiple"][key], old["profit_by_exit_multiple"][key])
        assert result["current_shortfall"] == old["current_shortfall"]
        parity_count += 1
        ns["CFG"] = copy.deepcopy(cfg)
        return case, result, old

    def compact(case, result, packet, label):
        return {
            "case_id": case["id"], "name": case["name"], "source_packet": packet,
            "source_results": PATHS[packet], "source_scenario": label,
            "price": case["price"], "monthly_rent": case["rent_assumed"],
            "monthly_fee_proxy": case["fee_assumed"], "monthly_other_allowance": case["other_assumed"],
            "initial_refurb_allowance": case["refurb_assumed"],
            "gross_yield": result["gross_yield"],
            "standard_monthly_balance": result["standard_monthly_balance"],
            "current_shortfall": result["current_shortfall"],
            "annual_cash": result["cashflow_by_year"][0], "entry_cash": result["entry_cash"],
            "five_year_nominal_breakeven_sale": result["terminal_nominal_breakeven"],
            "five_year_illustrative_8pct_required_sale": result["terminal_8pct_required"],
            "five_year_profit_at_own_entry_price": result["profit_by_exit_multiple"]["1"],
            "five_year_required_nominal_sale_uplift_pct": 100 * (result["terminal_nominal_breakeven"] / case["price"] - 1),
            "g0": "STOP", "g9": "Defer", "market_input_status": "Unvalidated conditional scenario",
        }

    rows = []
    k = ns["payment"](.9, .04, 35)
    for packet, label, cid in BASES:
        case, result, old = replay(packet, label)
        assert case["id"] == cid and not old["case_overrides"] and not old["engine_arguments"]
        row = compact(case, result, packet, label)
        p, r, f, o = (case[x] for x in ("price", "rent_assumed", "fee_assumed", "other_assumed"))
        pay = result["standard_instalment"]
        thresholds = {
            "gross6_price_at_base_rent": 12 * r / .06,
            "simplified_monthly_coverage_price_at_base_rent": (r - f) / k,
            "annual_neutral_price_at_base_rent": (11 * r / 12 - f - o) / k,
            "annual_neutral_rent_at_base_price": 12 * (pay + f + o) / 11,
            "annual_neutral_max_monthly_fee_at_base_rent": 11 * r / 12 - pay - o,
            "annual_neutral_paid_months_at_base_rent": 12 * (pay + f + o) / r,
        }
        thresholds["occupancy_alone_can_reach_annual_neutral_within_12_months"] = thresholds["annual_neutral_paid_months_at_base_rent"] <= 12
        for field, value in (
            ("price", thresholds["annual_neutral_price_at_base_rent"]),
            ("rent_assumed", thresholds["annual_neutral_rent_at_base_price"]),
            ("fee_assumed", thresholds["annual_neutral_max_monthly_fee_at_base_rent"]),
        ):
            assert value > 0
            test = calculate(dict(case, **{field: value}))
            near(test["cashflow_by_year"][0], 0)
            root_count += 1
        near(thresholds["annual_neutral_paid_months_at_base_rent"] * r - 12 * (pay + f + o), 0)
        row["thresholds"] = thresholds
        row["incremental_annual_cash_if_fee_plus100"] = -1200
        row["annual_cash_if_one_extra_vacant_month"] = row["annual_cash"] - r
        row["five_year_flat_exit_profit_if_extra_refurb30k"] = row["five_year_profit_at_own_entry_price"] - 30000
        rows.append(row)

    branches = []
    for packet, label in BRANCHES:
        case, result, old = replay(packet, label)
        row = compact(case, result, packet, label)
        row["case_overrides"] = old["case_overrides"]
        row["evidence_state"] = "Held alternative from prior release; not a corrected historical base or verified deal"
        branches.append(row)

    counts = {
        "cases": len(rows), "simplified_monthly_non_shortfall": sum(not r["current_shortfall"] for r in rows),
        "annual_positive": sum(r["annual_cash"] > 0 for r in rows),
        "annual_negative": sum(r["annual_cash"] < 0 for r in rows),
        "five_year_flat_price_loss": sum(r["five_year_profit_at_own_entry_price"] < 0 for r in rows),
        "deploy": 0,
    }
    assert counts == {"cases": 10, "simplified_monthly_non_shortfall": 9, "annual_positive": 2,
                      "annual_negative": 8, "five_year_flat_price_loss": 10, "deploy": 0}
    assert {r["case_id"] for r in rows if r["annual_cash"] > 0} == {"R321", "R353"}
    assert all(r["annual_cash"] - 1200 < 0 for r in rows)
    return {
        "packet": "TEN-CASE-DECISION-SHEET-2026-10-13", "baseline_commit": BASELINE,
        "basis": "Synthesis of four dated public packets, not a fresh market survey",
        "source_git_blobs": {PATHS[key]: sha for key, sha in BLOB_HASHES.items()},
        "config": cfg,
        "limitations": [
            "All ten historical bases stay unchanged; held alternatives are not promoted.",
            "Monthly balance uses an unverified combined service/sinking proxy. Annual cash has eleven paid months and inherited other allowances.",
            "Pre-tax illustration with 5% acquisition, 3% disposal and case-specific refurbishment allowances; actual charges and unquoted costs remain missing.",
            "Cash-neutral thresholds are not fair values, offers or G0 admission. The 8% equity hurdle is illustrative, not user-approved.",
            "Sale burdens are not forecasts. No privacy, family, diversity, rail or catalyst premium is booked.",
            "Single-asset cash comparisons do not establish portfolio allocation, lender approval or realised performance.",
        ],
        "historical_bases": rows, "held_alternatives": branches, "counts": counts,
        "checks": {"financial_evaluations": run_count, "source_scenario_parity": parity_count,
                   "annual_neutral_engine_roots": root_count, "paid_month_algebra_checks": len(rows),
                   "source_blobs": "passed", "financial_identities": "passed",
                   "scope_and_status": "passed"},
    }

if __name__ == "__main__":
    root = next(p for p in Path(__file__).resolve().parents if (p / PATHS["engine"]).exists())
    raw = {key: (root / path).read_bytes().decode("utf-8") for key, path in PATHS.items()}
    print(json.dumps(run(raw), indent=2, ensure_ascii=False) + "\n", end="")
