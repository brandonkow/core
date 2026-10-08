"""B07 Working 02 targeted diagnostics; immutable frozen functions, no file writes."""
import ast
import itertools

def build(inputs, engine_source, cfg, working02):
    module = ast.Module(body=[n for n in ast.parse(engine_source).body
        if isinstance(n, ast.FunctionDef) and n.name in ("payment", "evaluate", "check_financial_identities")], type_ignores=[])
    ns = {"CFG": cfg}
    exec(compile(module, "<frozen-financial-functions>", "exec"), ns)
    ev, check, pay = ns["evaluate"], ns["check_financial_identities"], ns["payment"]
    cases = inputs["inherited_cases"] + inputs["working_01_cases"] + inputs["new_cases"]
    selected = [c for c in cases if c["id"] in ["R235", "R236", "R342", "R345", "R347"]]
    historical = list(selected)
    selected += working02["new_cases"]
    assert len(selected) == 6
    scenarios = {
        "base": {},
        "zero_rent_first12": {"months":12, "initial_vacancy":12},
        "combined12mo": {"months":12, "rate":.055, "rent_factor":.8, "fee_factor":1.2,
                         "first_year_paid":6, "levy_month":1, "levy":30000},
        "exit_delay12": {"months":72},
        "bank_value_down15": {"valuation_ratio":.85},
        "term25": {"term":25},
    }
    evaluations = []
    exit_tests = []
    for c in selected:
        for label, params in scenarios.items():
            row = ev(c, **params)
            check(row, c)
            row["scenario"] = label
            row["parameters"] = params
            # Full monthly schedules remain reproducible; retain twelve-month forced-hold paths here.
            if label not in ("zero_rent_first12", "combined12mo"):
                row.pop("schedule")
                row.pop("cash_path")
            evaluations.append(row)
        b = next(x for x in evaluations if x["id"] == c["id"] and x["scenario"] == "base")
        operating_income = 11*c["rent_assumed"] - 12*(c["fee_assumed"]+c["other_assumed"])
        break_even = b["terminal_nominal_breakeven"]
        current_annual_cash = 11*c["rent_assumed"]-12*(pay(.9*c["price"],.04,35)+c["fee_assumed"]+c["other_assumed"])
        assert abs(current_annual_cash-b["cashflow_by_year"][0])<.01
        exits = []
        for y in (.05,.06,.07):
            value = operating_income/y
            profit = .97*value-b["terminal_debt"]+b["cashflow_total"]-b["entry_cash"]
            exits.append({"illustrative_required_operating_yield":y,
                "income_only_value_at_flat_rent":value,
                "five_year_equity_profit_at_that_exit":profit})
        exit_tests.append({"id":c["id"], "operating_income_before_financing":operating_income,
            "operating_yield_at_nominal_break_even":operating_income/break_even,
            "nominal_break_even":break_even,
            "future_buyer_cash_15pct_plus_same_refurb":.15*break_even+c["refurb_assumed"],
            "future_buyer_cash_35pct_plus_same_refurb":.35*break_even+c["refurb_assumed"],
            "future_buyer_standard_instalment":pay(.9*break_even,.04,35),
            "future_buyer_stress_instalment":pay(.7*break_even,.055,25),
            "income_sensitivities":exits,
            "boundary":"Flat rent and unchanged cost proxies; illustrative 5/6/7% operating yields are not observed cap rates or the user's preferred 6% gross. Buyer costs and refurbishment are proxies, not finance approval. 70% LTV is a stress branch, not a legal claim."})
    extra = []
    c = working02["new_cases"][0]
    for label, params in {
        "rate_5_5pct":{"rate":.055}, "rent_down20":{"rent_factor":.8},
        "fee_up20":{"fee_factor":1.2}, "works30k_month24":{"levy_month":24,"levy":30000},
        "unquoted_cost_buffer":{"annual_extra_cost":1200,"exit_extra_cost":5000},
        "combined5yr":{"rate":.055,"rent_factor":.8,"fee_factor":1.2,"first_year_paid":6,"levy_month":1,"levy":30000},
        "rent_low":{"rent_factor":c["rent_low"]/c["rent_assumed"]},
        "rent_high":{"rent_factor":c["rent_high"]/c["rent_assumed"]},
    }.items():
        row=ev(c, **params); check(row,c,params.get("exit_extra_cost",0))
        row.update(scenario=label,parameters=params)
        row.pop("schedule");row.pop("cash_path");extra.append(row)
    branches=[]
    for branch in working02["branches"]:
        c2=dict(c,**branch["overrides"])
        row=ev(c2,**branch["parameters"]);check(row,c2)
        row.update(scenario=branch["label"],parameters=branch["parameters"],input_overrides=branch["overrides"],boundary=branch["boundary"])
        row.pop("schedule");row.pop("cash_path");branches.append(row)
    thresholds=[]
    for c in selected:
        k=pay(.9,.04,35)
        thresholds.append({"id":c["id"],"standard_rent_required":k*c["price"]+c["fee_assumed"],
            "rent_for_6pct_gross":.005*c["price"],
            "annual_neutral_rent":12*(k*c["price"]+c["fee_assumed"]+c["other_assumed"])/11,
            "price_for_annual_neutral":max(0,(11*c["rent_assumed"]/12-c["fee_assumed"]-c["other_assumed"])/k)})
    allbyid={c["id"]:c for c in cases+working02["new_cases"]}
    ranks=[]
    for aid,bid in [("R234","R348"),("R343","R348")]:
        a,b=allbyid[aid],allbyid[bid]
        for ar,br in itertools.product((a["rent_low"],a["rent_assumed"],a["rent_high"]),(b["rent_low"],b["rent_assumed"],b["rent_high"])):
            ac=ar-pay(.9*a["price"],.04,35)-a["fee_assumed"]
            bc=br-pay(.9*b["price"],.04,35)-b["fee_assumed"]
            ranks.append({"ids":[aid,bid],"rents":[ar,br],"standard_balances":[ac,bc],"coverage_leader":aid if ac>bc else bid if bc>ac else "tie"})
    ambang=[]
    for fee, rate in itertools.product((250,350,450),(.04,.055)):
        p=377000
        payment=pay(.9*p,rate,35)
        standard=pay(.9*p,.04,35)+fee
        ambang.append({"id":"B07-T03", "price_sensitivity_only":p,
            "fee_proxy":fee,"other_monthly_proxy":200,"actual_rate_sensitivity":rate,
            "standard_rent_required":standard,"rent_for_6pct_gross":.005*p,
            "actual_payment_plus_fee":payment+fee,
            "annual_neutral_rent_at_actual_rate":12*(payment+fee+200)/11,
            "full_draw_no_income_carry12":12*(payment+fee+200),
            "illustrative_entry_cash":.15*p+20000,
            "boundary":"Ambang brochure repeats Type A at 270k affordable and 377k; no exact market layout/offer verified. 270k restricted cohort is excluded from this ordinary-market diagnostic. No rent, progressive draw schedule, return or clearance inferred. Fees/refurbishment are unverified, full-draw carry is not a worst-case bound."})
    assert len(evaluations)==36 and len(exit_tests)==6 and len(ambang)==6
    assert len(extra)==8 and len(branches)==3 and len(ranks)==18
    return {"version":"B07-WORKING-02-2026-10-08","source_commit":"77b8ecffde3cec4253be3d6fa1a977944cdd94cd",
        "historical_inputs_unchanged":historical,"new_inputs":working02["new_cases"],"config":cfg,"evaluations":evaluations+extra,"branches":branches,"thresholds":thresholds,"rank_grids":ranks,"evaluation_count":len(evaluations)+len(extra)+len(branches),
        "investor_exit_diagnostics":exit_tests,"forward_threshold_control":ambang,
        "checks":"Amortisation, principal conservation, independent economic basis, discounted exit, and annual cash identities passed.",
        "decision_boundary":"All six cases remain G0 STOP / G9 Defer. These diagnostics supplement Working 01 and do not overwrite inputs or create an investable portfolio."}
