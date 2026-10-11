"""Reproduce the dated Eve/Maxim sensitivity packet using the frozen engine.
No market-data download, engine edit or file output. From repository root:
python klang-valley-2026-10-07/round-3/privacy-validation-2026-10-12/reproduce.py
Prints deterministic JSON to stdout. Inputs are scenarios, not authenticated leases.
"""
import ast
import copy
import hashlib
import itertools
import json
from pathlib import Path

def run(inputs, engine_source, config):
    assert hashlib.sha256(engine_source.encode("utf-8")).hexdigest() == inputs["frozen_engine_sha256"]
    names = {"payment", "evaluate", "check_financial_identities"}
    tree = ast.parse(engine_source)
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert {f.name for f in functions} == names
    ns = {"CFG": copy.deepcopy(config)}
    exec(compile(ast.Module(body=functions, type_ignores=[]), "<frozen-financial-functions>", "exec"), ns)
    cases = {c["id"]: c for c in inputs["historical_cases"]}
    checks = 0

    def calculate(label, cid, overrides=None, kwargs=None, paid=None):
        nonlocal checks
        c = dict(cases[cid], **(overrides or {}))
        cfg = copy.deepcopy(config)
        kw = dict(kwargs or {})
        if paid is not None:
            cfg["baseline_paid_months_per_year"] = paid
            kw["first_year_paid"] = paid
        ns["CFG"] = cfg
        full = ns["evaluate"](c, **kw)
        ns["check_financial_identities"](full, c, kw.get("exit_extra_cost", 0))
        checks += 1
        keep = ["price", "gross_yield", "rent_assumed", "fee_proxy", "other_cost_allowance",
                "standard_instalment", "standard_monthly_balance", "current_shortfall",
                "actual_loan", "actual_instalment", "actual_rate", "actual_term_years",
                "valuation_ratio", "entry_cash", "months", "cashflow_by_year", "cashflow_total",
                "terminal_debt", "terminal_nominal_breakeven", "terminal_8pct_required",
                "profit_by_exit_multiple", "minimum_cash", "protected_reserve_pass"]
        out = {k: full[k] for k in keep}
        out.update(label=label, case_id=cid, paid_months_per_year=cfg["baseline_paid_months_per_year"],
                   case_overrides=overrides or {}, engine_arguments=kw)
        # Retain 90% for both future-buyer illustrations. Do not use the
        # frozen engine's separate legacy 80% future-buyer stress output.
        be = full["terminal_nominal_breakeven"]
        out["future_buyer_payment_90_4_35_at_breakeven"] = ns["payment"](.9 * be, .04, 35)
        out["future_buyer_payment_90_5_5_25_at_breakeven"] = ns["payment"](.9 * be, .055, 25)
        out["future_buyer_monthly_coverage_rent_at_breakeven"] = out["future_buyer_payment_90_4_35_at_breakeven"] + c["fee_assumed"]
        return out

    scenarios = [calculate(s["label"], s["case_id"], s.get("case_overrides"), paid=s.get("paid_months_per_year"))
                 for s in inputs["scenarios"]]
    stresses = [calculate(cid + "_" + label, cid, kwargs=kw)
                for cid in cases for label, kw in inputs["common_stresses"].items()]
    k = ns["payment"](.9, .04, 35)
    thresholds = {}
    for cid, c in cases.items():
        r, f, o, p = (c[x] for x in ("rent_assumed", "fee_assumed", "other_assumed", "price"))
        annual_price = (11 * r / 12 - f - o) / k
        annual_rent = 12 * (k * p + f + o) / 11
        thresholds[cid] = {
            "gross6_price_at_base_rent": 12 * r / .06,
            "monthly_coverage_price_at_base_rent": (r - f) / k,
            "annual_neutral_price_at_base_rent": annual_price,
            "annual_neutral_rent_at_base_price": annual_rent,
            "one_extra_paid_month_cash_benefit": r,
            "one_extra_paid_month_annual_cash_parity_price_increment": r / (12*k)
        }
        price_check = calculate(cid + "_annual_price_root", cid, {"price": annual_price})
        rent_check = calculate(cid + "_annual_rent_root", cid, {"rent_assumed": annual_rent})
        assert abs(price_check["cashflow_by_year"][0]) < .01
        assert abs(rent_check["cashflow_by_year"][0]) < .01

    eve, maxim = cases["R306"], cases["KV01"]
    cost_delta = eve["fee_assumed"] + eve["other_assumed"] - maxim["fee_assumed"] - maxim["other_assumed"]
    parity = [{"eve_rent_advantage": delta, "annual_cash_parity_price_premium": (11*delta/12-cost_delta)/k}
              for delta in (0,100,200)]
    grid = []
    for ep, er, mr in itertools.product(inputs["grid"]["eve_prices"], inputs["grid"]["eve_rents"], inputs["grid"]["maxim_rents"]):
        e = calculate("gridE", "R306", {"price":ep, "rent_assumed":er})
        m = calculate("gridM", "KV01", {"rent_assumed":mr})
        ec, mc = e["cashflow_by_year"][0], m["cashflow_by_year"][0]
        grid.append({"eve_price":ep,"eve_rent":er,"maxim_price":maxim["price"],"maxim_rent":mr,
                     "eve_annual_cash":ec,"maxim_annual_cash":mc,
                     "cash_leader":"R306" if ec>mc else "KV01" if mc>ec else "tie"})
    assert {g["cash_leader"] for g in grid} == {"R306", "KV01"}
    base = {r["case_id"]:r for r in scenarios if r["label"] in {"E_base", "M_base"}}
    assert all(r["standard_monthly_balance"] > 0 and r["cashflow_by_year"][0] < 0 for r in base.values())
    assert all(r["profit_by_exit_multiple"]["1"] < 0 for r in base.values())
    assert config["standard_ltv"] == .9 and config["standard_rate"] == .04 and config["standard_term_years"] == 35
    assert all(abs(r["standard_instalment"] - k*r["price"]) < 1e-8 for r in scenarios+stresses)
    return {
        "packet":inputs["packet"],"baseline_commit":inputs["baseline_commit"],"config":config,
        "limitations":"Conditional pre-tax arithmetic. Fee proxies, other costs and refurbishment unverified; unknown transaction costs not zero. 8% hurdle is illustrative, not user-approved. No fair value or Deploy.",
        "scenarios":scenarios,"stresses":stresses,"thresholds":thresholds,
        "parity":{"monthly_instalment_per_RM_price":k,"eve_minus_maxim_monthly_operating_cost":cost_delta,
                  "scenarios":parity,"meaning":"Annual-cash parity only, not valuation or permission to pay a premium."},
        "rank_grid":grid,
        "exit_capitalisation":[{"gross_yield":y,"price_if_monthly_rent2000":24000/y} for y in inputs["gross_exit_yields"]],
        "checks":{"financial_runs_checked":checks,"identity_checks":"closed amortisation, principal conservation, zero-profit exit, independent interest-cost identity, discounted hurdle",
                  "annual_neutral_roots":"passed","rank_reversal":"passed","standard_baseline_invariance":"passed",
                  "baseline_monthly_positive_annual_negative":"passed","flat_exit_losses":"passed"}
    }

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    root = here.parents[2]
    inputs = json.loads((here / "Financial_Inputs.json").read_text(encoding="utf-8"))
    engine = (root / "execution-release-2026-10-07/financial_engine.py").read_text(encoding="utf-8")
    cfg = json.loads((root / "execution-release-2026-10-07/financial_config.json").read_text(encoding="utf-8"))
    print(json.dumps(run(inputs, engine, cfg), indent=2, ensure_ascii=False) + "\n", end="")
