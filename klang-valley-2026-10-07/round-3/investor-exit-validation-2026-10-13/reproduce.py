"""Reproduce the investor-exit packet with the unchanged frozen financial engine.
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
    base = {r["case_id"]:r for r in scenarios if r["label"] in {"Z_base","S_base"}}
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
    z, s = base["R231"], base["KV14"]
    annual_gap = s["cashflow_by_year"][0] - z["cashflow_by_year"][0]
    total_gap = s["profit_by_exit_multiple"]["1"] - z["profit_by_exit_multiple"]["1"]
    equal_exit = {cid: .97*220000-b["terminal_debt"]+b["cashflow_total"]-b["entry_cash"] for cid,b in base.items()}
    comparisons = {
        "annual_carry_advantage_solstice":annual_gap,
        "zeva_extra_rent_to_match_annual_carry_11paid":annual_gap/11,
        "zeva_extra_paid_months_to_match_annual_carry_at1200":annual_gap/1200,
        "zeva_initial_cash_extra":z["entry_cash"]-s["entry_cash"],
        "flat_exit_nominal_profit_advantage_solstice":total_gap,
        "zeva_extra_monthly_rent_to_match_flat_exit_profit_55paid":total_gap/55,
        "zeva_additional_sale_receipt_to_match_flat_exit_profit":total_gap/.97,
        "common_220k_exit_profit":equal_exit,
        "zeva_extra_rent_to_match_common_exit_profit_55paid":(equal_exit["KV14"]-equal_exit["R231"])/55,
        "baseline_paid_months_for_annual_neutrality":{cid:12*(b["actual_instalment"]+b["fee_proxy"]+b["other_cost_allowance"])/b["rent_assumed"] for cid,b in base.items()},
        "boundary":"Carry equivalence does not recover extra upfront capital or establish equal total return. Same-percentage exits and equal-absolute exits are separate counterfactuals, not forecasts."
    }
    carry_match=calculate("carry_parity_check","R231",{"rent_assumed":1200+annual_gap/11})
    flat_match=calculate("flat_exit_parity_check","R231",{"rent_assumed":1200+total_gap/55})
    common_match=calculate("common_exit_parity_check","R231",{"rent_assumed":1200+(equal_exit["KV14"]-equal_exit["R231"])/55})
    assert abs(carry_match["cashflow_by_year"][0]-s["cashflow_by_year"][0])<.01
    assert abs(flat_match["profit_by_exit_multiple"]["1"]-s["profit_by_exit_multiple"]["1"])<.01
    assert abs(.97*220000-common_match["terminal_debt"]+common_match["cashflow_total"]-common_match["entry_cash"]-equal_exit["KV14"])<.01
    exit_tests = []
    for cid,c in cases.items():
        b=base[cid]
        noi=11*c["rent_assumed"]-12*(c["fee_assumed"]+c["other_assumed"])
        caps=[("gross",y,12*c["rent_assumed"]/y) for y in inputs["comparison_assumptions"]["gross_exit_yields"]]
        caps += [("net",y,noi/y) for y in inputs["comparison_assumptions"]["net_exit_yields"]]
        for basis,y,price in caps:
            exit_tests.append({"case_id":cid,"income_basis":basis,"required_yield":y,"capitalised_price":price,
                 "annual_noi_before_debt":noi,
                 "seller_nominal_profit":.97*price-b["terminal_debt"]+b["cashflow_total"]-b["entry_cash"],
                 "buyer_equity_plus5pct_cost":.15*price,
                 "buyer_payment_90_4_35":ns["payment"](.9*price,.04,35),
                 "buyer_payment_90_5_5_25":ns["payment"](.9*price,.055,25),
                 "buyer_annual_carry_11paid_at4pct":noi-12*ns["payment"](.9*price,.04,35)})
    ns["CFG"]=copy.deepcopy(config)
    joint=[]
    for months in (12,24):
        rows=[ns["evaluate"](c,months=months,rate=.055,rent_factor=.8,first_year_paid=6,levy_month=1,levy=30000) for c in cases.values()]
        for c,row in zip(cases.values(),rows):
            ns["check_financial_identities"](row,c);checks+=1
        cash=config["synthetic_cash"]-sum(b["entry_cash"] for b in rows)
        minimum=cash
        for m in range(months):
            cash+=sum(b["schedule"][m]["cashflow"] for b in rows);minimum=min(minimum,cash)
        joint.append({"months":months,"entry_cash":sum(b["entry_cash"] for b in rows),"combined_carry":sum(b["cashflow_total"] for b in rows),
                      "minimum_cash":minimum,"remaining_cash":cash,"reserve_pass":minimum>=config["synthetic_protected_reserve"],
                      "boundary":"Correlated shock with no assumed tenant diversification; synthetic reserves, not a recommended allocation. Year two reverts to eleven paid months at stressed rent/rate."})
    # Keep all cash outcomes conditional. Diversity is not an invented coefficient.
    assert all(b["standard_monthly_balance"]>0 and b["cashflow_by_year"][0]<0 for b in base.values())
    assert all(b["profit_by_exit_multiple"]["1"]<0 for b in base.values())
    assert config["standard_ltv"]==.9 and config["standard_rate"]==.04 and config["standard_term_years"]==35
    assert all(abs(s["standard_instalment"]-k*s["price"])<1e-8 for s in scenarios+stresses)
    return {"packet":inputs["packet"],"baseline_commit":inputs["baseline_commit"],"config":config,
            "limitations":"Pre-tax conditional arithmetic; no diversity or rail premium, actual costs or achieved rent authenticated. Unknown costs not zero. 8% hurdle illustrative.",
            "scenarios":scenarios,"stresses":stresses,"thresholds":thresholds,"relative_reversals":comparisons,"investor_exit_sensitivities":exit_tests,"joint_stress":joint,
            "checks":{"financial_runs_checked":checks,
                      "financial_identities":"closed amortisation, principal conservation, independent interest-cost exit identity and discounted hurdle passed",
                      "annual_neutral_roots":"passed","relative_carry_and_exit_parity":"passed","common_standard_invariant":"passed",
                      "base_monthly_positive_annual_negative":"passed","base_flat_price_loss":"passed"}}

if __name__ == "__main__":
    here=Path(__file__).resolve().parent
    root=here.parents[2]
    inputs=json.loads((here/"Financial_Inputs.json").read_text(encoding="utf-8"))
    engine=(root/"execution-release-2026-10-07/financial_engine.py").read_text(encoding="utf-8")
    cfg=json.loads((root/"execution-release-2026-10-07/financial_config.json").read_text(encoding="utf-8"))
    print(json.dumps(run(inputs,engine,cfg),indent=2,ensure_ascii=False)+"\n",end="")
