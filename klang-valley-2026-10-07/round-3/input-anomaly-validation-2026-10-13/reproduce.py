"""Reproduce the input-anomaly packet with the unchanged frozen financial engine.
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
                           s.get("engine_arguments"), s.get("paid_months_per_year")) for s in inputs["scenarios"]]
    stresses = [calculate(cid+"_"+label,cid,kwargs=kw) for cid in cases
                for label,kw in inputs["common_stresses"].items()]
    k = ns["payment"](.9,.04,35)
    thresholds = {}
    for cid,c in cases.items():
        r,f,o,p = (c[x] for x in ("rent_assumed","fee_assumed","other_assumed","price"))
        annual_price=(11*r/12-f-o)/k
        annual_rent=12*(k*p+f+o)/11
        thresholds[cid]={"annual_neutral_price":annual_price,"annual_neutral_rent":annual_rent,
            "annual_neutral_fee":11*r/12-k*p-o,
            "gross6_price":12*r/.06,"monthly_coverage_price":(r-f)/k,
            "annual_neutral_paid_months":12*(k*p+f+o)/r}
        a=calculate("price_root",cid,{"price":annual_price})
        b=calculate("rent_root",cid,{"rent_assumed":annual_rent})
        assert abs(a["cashflow_by_year"][0])<.01 and abs(b["cashflow_by_year"][0])<.01
    lucentia=[]
    for rent in (3000,3400):
        maximum=11*rent/12-k*600000-230
        root=calculate("fee_root","R322",{"rent_assumed":rent,"fee_assumed":maximum})
        assert abs(root["cashflow_by_year"][0])<.01
        lucentia.append({"rent":rent,"annual_neutral_combined_monthly_fee":maximum,
            "standard_monthly_neutral_fee":rent-k*600000,
            "warning":"Cost threshold only, not evidence of actual billed charge."})
    rows={x["label"]:x for x in scenarios}
    reversals={
        "parkview_rent_reduction_eliminating_base_surplus":rows["P_base"]["cashflow_by_year"][0]/11,
        "parkview_extra_monthly_cost_eliminating_base_surplus":rows["P_base"]["cashflow_by_year"][0]/12,
        "arc_max_price_increase_before_annual_deficit":thresholds["R353"]["annual_neutral_price"]-220000,
        "arc_extra_monthly_cost_eliminating_base_surplus":rows["A_base"]["cashflow_by_year"][0]/12,
        "arc_248k_annual_neutral_rent":12*(k*248000+250+180)/11,
        "lucentia_quarterly_vs_monthly_annual_difference":rows["L_quarterly_3400"]["cashflow_by_year"][0]-rows["L_base"]["cashflow_by_year"][0],
        "lucentia_quarterly_annual_neutral_rent":12*(k*600000+1165/3+230)/11,
        "lucentia_060psf_annual_neutral_rent":12*(k*600000+.6*454+230)/11}
    assert rows["P_base"]["cashflow_by_year"][0]>0>rows["P_rent_2300"]["cashflow_by_year"][0]
    assert rows["A_base"]["cashflow_by_year"][0]>0>rows["A_248k_1500"]["cashflow_by_year"][0]
    assert rows["L_base"]["cashflow_by_year"][0]<0<rows["L_quarterly_3400"]["cashflow_by_year"][0]
    assert rows["L_quarterly_3000"]["cashflow_by_year"][0]<0 and rows["L_060psf_3000"]["cashflow_by_year"][0]<0
    assert abs(reversals["lucentia_quarterly_vs_monthly_annual_difference"]-12*(1165-1165/3))<.01
    ns["CFG"]=copy.deepcopy(config)
    joint=[]
    for months in (12,24):
        shock=[ns["evaluate"](c,months=months,rate=.055,rent_factor=.8,first_year_paid=6,levy_month=1,levy=30000) for c in cases.values()]
        for c,row in zip(cases.values(),shock):
            ns["check_financial_identities"](row,c);checks+=1
        cash=config["synthetic_cash"]-sum(b["entry_cash"] for b in shock); minimum=cash
        for m in range(months):
            cash+=sum(b["schedule"][m]["cashflow"] for b in shock);minimum=min(minimum,cash)
        joint.append({"months":months,"entry_cash":sum(b["entry_cash"] for b in shock),"combined_carry":sum(b["cashflow_total"] for b in shock),
            "minimum_cash":minimum,"remaining_cash":cash,"reserve_pass":minimum>=config["synthetic_protected_reserve"],
            "zero_lucentia_fee_ending_cash_upper_bound":cash+months*cases["R322"]["fee_assumed"],
            "zero_lucentia_fee_still_below_reserve":cash+months*cases["R322"]["fee_assumed"]<config["synthetic_protected_reserve"],
            "boundary":"All three historical branches including Lucentia monthly1165; joint correlated stress, not allocation. Year2 has11paid months at stressed rent/rate. Fee alternatives not counted as additional assets."})
    assert config["standard_ltv"]==.9 and config["standard_rate"]==.04 and config["standard_term_years"]==35
    assert all(abs(s["standard_instalment"]-k*s["price"])<1e-8 for s in scenarios+stresses)
    return {"packet":inputs["packet"],"baseline_commit":inputs["baseline_commit"],"config":config,
        "boundary":inputs["cost_boundary"],"scenarios":scenarios,"stresses":stresses,
        "historical_branch_thresholds":thresholds,"lucentia_fee_thresholds":lucentia,"reversals":reversals,"joint_stress":joint,
        "checks":{"financial_runs_checked":checks,"financial_identities":"passed",
            "annual_neutral_roots":"passed","three_case_reversals":"passed","common_standard_invariant":"passed"}}

if __name__ == "__main__":
    here=Path(__file__).resolve().parent
    root=here.parents[2]
    inputs=json.loads((here/"Financial_Inputs.json").read_text(encoding="utf-8"))
    engine=(root/"execution-release-2026-10-07/financial_engine.py").read_text(encoding="utf-8")
    cfg=json.loads((root/"execution-release-2026-10-07/financial_config.json").read_text(encoding="utf-8"))
    print(json.dumps(run(inputs,engine,cfg),indent=2,ensure_ascii=False)+"\n",end="")
