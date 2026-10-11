"""Reproduce the family-adoption packet with the unchanged frozen financial engine.
Prints JSON to stdout; no network access or output file. Run from any checkout path.
"""
import ast
import copy
import hashlib
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


    scenarios = [calculate(s["label"], s["case_id"], s.get("case_overrides"),
                           paid=s.get("paid_months_per_year")) for s in inputs["scenarios"]]
    stresses = [calculate(cid+"_"+label,cid,kwargs=kw) for cid in cases
                for label,kw in inputs["common_stresses"].items()]
    # A verified fee change would also change simplified coverage.
    for cid,c in cases.items():
        stresses.append(calculate(cid+"_fee_plus100",cid,{"fee_assumed":c["fee_assumed"]+100}))
    k = ns["payment"](.9,.04,35)
    thresholds = {}
    base = {r["case_id"]:r for r in scenarios if r["label"] in {"P_base","S_base","E_base"}}
    for cid,c in cases.items():
        r,f,o,p = (c[x] for x in ("rent_assumed","fee_assumed","other_assumed","price"))
        ap = (11*r/12-f-o)/k
        ar = 12*(k*p+f+o)/11
        thresholds[cid] = {"gross6_price":12*r/.06,"annual_neutral_price":ap,
                          "annual_neutral_rent":ar,"monthly_proxy_coverage_price":(r-f)/k,
                          "one_extra_paid_month_annual_value":r,
                          "required_rent_increment_to_fund30k_over5years_11paid":30000/55,
                          "gross_exit_capitalisation":[{"yield":y,"price":12*r/y} for y in (.06,.07,.08)]}
        a=calculate("price_root",cid,{"price":ap}); b=calculate("rent_root",cid,{"rent_assumed":ar})
        assert abs(a["cashflow_by_year"][0])<.01 and abs(b["cashflow_by_year"][0])<.01
    retention = {"two_year_rent_concession":100*24,
                 "one_avoided_month_at2400":2400,
                 "meaning":"Contractual RM2300 versus RM2400 for 24 paid months costs RM2400; one otherwise lost RM2400 month offsets it before fees/defaults. This is arithmetic, not observed retention or 24-month payment assurance."}
    # Keep all cash outcomes conditional. A stronger family narrative is not a coefficient.
    assert all(b["standard_monthly_balance"]>0 and b["cashflow_by_year"][0]<0 for b in base.values())
    assert all(b["profit_by_exit_multiple"]["1"]<0 for b in base.values())
    assert config["standard_ltv"]==.9 and config["standard_rate"]==.04 and config["standard_term_years"]==35
    assert all(abs(s["standard_instalment"]-k*s["price"])<1e-8 for s in scenarios+stresses)
    return {"packet":inputs["packet"],"baseline_commit":inputs["baseline_commit"],"config":config,
            "limitations":"Pre-tax conditional arithmetic; no family/management premium, actual costs or achieved rent authenticated. Unknown costs not zero. 8% hurdle illustrative.",
            "scenarios":scenarios,"stresses":stresses,"thresholds":thresholds,"retention_tradeoff":retention,
            "checks":{"financial_runs_checked":checks,
                      "financial_identities":"closed amortisation, principal conservation, independent interest-cost exit identity and discounted hurdle passed",
                      "annual_neutral_roots":"passed","common_standard_invariant":"passed",
                      "base_monthly_positive_annual_negative":"passed","base_flat_price_loss":"passed"}}

if __name__ == "__main__":
    here=Path(__file__).resolve().parent
    root=here.parents[2]
    inputs=json.loads((here/"Financial_Inputs.json").read_text(encoding="utf-8"))
    engine=(root/"execution-release-2026-10-07/financial_engine.py").read_text(encoding="utf-8")
    cfg=json.loads((root/"execution-release-2026-10-07/financial_config.json").read_text(encoding="utf-8"))
    print(json.dumps(run(inputs,engine,cfg),indent=2,ensure_ascii=False)+"\n",end="")
