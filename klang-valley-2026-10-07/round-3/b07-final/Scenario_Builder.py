"""Deterministic B07 integrated diagnostics. No file writes or market-data calls."""
import ast
import copy
import itertools

def build(working01, working02, supplement, engine_source, cfg):
    module = ast.Module(body=[n for n in ast.parse(engine_source).body
        if isinstance(n, ast.FunctionDef) and n.name in
        ("payment", "evaluate", "check_financial_identities")], type_ignores=[])
    ns = {"CFG": cfg}
    exec(compile(module, "<frozen-financial-functions>", "exec"), ns)
    ev, check, pay = ns["evaluate"], ns["check_financial_identities"], ns["payment"]
    historical = working01["inherited_cases"] + working01["working_01_cases"] + working01["new_cases"]
    cases = copy.deepcopy(historical + working02["new_cases"] + supplement["new_cases"])
    assert len(historical) == 19 and len(cases) == 22
    assert len({c["id"] for c in cases}) == 22
    assert cases[:19] == historical and cases[19] == working02["new_cases"][0]
    scenarios = {
        "base": {},
        "rate_5_5pct": {"rate":.055},
        "rent_down20": {"rent_factor":.8},
        "fee_up20": {"fee_factor":1.2},
        "zero_rent_first12": {"initial_vacancy":12},
        "works30k_month24": {"levy_month":24,"levy":30000},
        "bank_value_down15": {"valuation_ratio":.85},
        "term25": {"term":25},
        "exit_delay12": {"months":72},
        "unquoted_cost_buffer": {"annual_extra_cost":1200,"exit_extra_cost":5000},
        "combined5yr": {"rate":.055,"rent_factor":.8,"fee_factor":1.2,"first_year_paid":6,"levy_month":1,"levy":30000},
        "combined12mo": {"months":12,"rate":.055,"rent_factor":.8,"fee_factor":1.2,"first_year_paid":6,"levy_month":1,"levy":30000}
    }
    full, evaluations, thresholds, exit_tests = {}, [], [], []
    k = pay(.9,.04,35)
    for c in cases:
        local = {}
        for label, params in list(scenarios.items()) + [
            ("rent_low",{"rent_factor":c["rent_low"]/c["rent_assumed"]}),
            ("rent_high",{"rent_factor":c["rent_high"]/c["rent_assumed"]})]:
            row = ev(c, **params)
            check(row,c,params.get("exit_extra_cost",0))
            row.update(scenario=label,parameters=params,input_overrides={})
            row["scenario_monthly_rent_less_actual_instalment_and_fee"] = (
                c["rent_assumed"]*params.get("rent_factor",1)-row["actual_instalment"]-
                c["fee_assumed"]*params.get("fee_factor",1))
            row["scenario_boundary"] = "Standard balance retains original90/4/35 and baseline rent. Scenario cashflow and separate scenario monthly metric apply stress. No outcomes observed."
            local[label] = row
            stored = copy.deepcopy(row)
            if label not in ("base","combined12mo"):
                stored.pop("schedule"); stored.pop("cash_path")
            evaluations.append(stored)
        full[c["id"]] = local
        b = local["base"]
        for adverse in ("rate_5_5pct","rent_down20","fee_up20","zero_rent_first12","works30k_month24","unquoted_cost_buffer","combined5yr"):
            assert local[adverse]["terminal_nominal_breakeven"] > b["terminal_nominal_breakeven"]
        annual = 11*c["rent_assumed"]-12*(k*c["price"]+c["fee_assumed"]+c["other_assumed"])
        assert abs(annual-b["cashflow_by_year"][0])<.01
        thresholds.append({
            "id":c["id"],"standard_rent_required":k*c["price"]+c["fee_assumed"],
            "rent_for_6pct_gross":.005*c["price"],
            "annual_neutral_rent":12*(k*c["price"]+c["fee_assumed"]+c["other_assumed"])/11,
            "price_for_standard_coverage":max(0,(c["rent_assumed"]-c["fee_assumed"])/k),
            "price_for_6pct_gross":200*c["rent_assumed"],
            "price_for_annual_neutral":max(0,(11*c["rent_assumed"]/12-c["fee_assumed"]-c["other_assumed"])/k),
            "boundary":"Income constraints under fixed proxies, not executable bid, fair value or validated margin of safety."})
        noi = 11*c["rent_assumed"]-12*(c["fee_assumed"]+c["other_assumed"])
        be = b["terminal_nominal_breakeven"]
        exit_tests.append({
            "id":c["id"],"operating_income_before_finance":noi,
            "operating_yield_at_nominal_breakeven":noi/be,
            "standard_buyer_cash_at_breakeven":.15*be+c["refurb_assumed"],
            "stress_buyer_cash_at_breakeven":.35*be+c["refurb_assumed"],
            "standard_buyer_instalment":pay(.9*be,.04,35),
            "stress_buyer_instalment":pay(.7*be,.055,25),
            "investor_exit_values":[{"required_operating_yield":y,"income_only_value":noi/y,
                "equity_profit_at_that_exit":.97*noi/y-b["terminal_debt"]+b["cashflow_total"]-b["entry_cash"]}
                for y in (.05,.06,.07)],
            "boundary":"Illustrative5/6/7% operating yields are not observed cap rates or user6%gross.70%future LTV is stress, not law. No owner or investor depth validated."})
    byid = {c["id"]:c for c in cases}
    branches = []
    all_branches = working01["branches"] + working02["branches"] + supplement["branches"]
    for branch in all_branches:
        c = dict(byid[branch["parent"]],**branch["overrides"])
        params = branch["parameters"]
        row = ev(c,**params); check(row,c,params.get("exit_extra_cost",0))
        row.update(scenario=branch["label"],parameters=params,input_overrides=branch["overrides"],
                   boundary=branch.get("boundary",""))
        row.pop("schedule");row.pop("cash_path");branches.append(row)
    pairs = []
    for aid,bid in itertools.combinations(byid,2):
        a,b = full[aid]["combined12mo"],full[bid]["combined12mo"]
        path = [cfg["synthetic_cash"]-a["entry_cash"]-b["entry_cash"]]
        for ma,mb in zip(a["schedule"],b["schedule"]):
            path.append(path[-1]+ma["cashflow"]+mb["cashflow"])
        pairs.append({"ids":[aid,bid],"cash_path":path,"minimum_cash":min(path),
            "reserve_pass":min(path)>=cfg["synthetic_protected_reserve"]})
    selected_pairs = [("KV13","R338"),("KV13","R349"),("R230","R339"),
        ("R231","R341"),("R231","R350"),("R341","R350"),("R232","R342"),
        ("R233","R346"),("R234","R343"),("R234","R348"),("R343","R348"),
        ("R235","R347"),("R236","R345"),("R342","R350")]
    grids = []
    for aid,bid in selected_pairs:
        a,b = byid[aid],byid[bid]
        for ar,br in itertools.product((a["rent_low"],a["rent_assumed"],a["rent_high"]),
                                        (b["rent_low"],b["rent_assumed"],b["rent_high"])):
            am = ar-k*a["price"]-a["fee_assumed"];bm=br-k*b["price"]-b["fee_assumed"]
            aa=11*ar-12*(k*a["price"]+a["fee_assumed"]+a["other_assumed"])
            ba=11*br-12*(k*b["price"]+b["fee_assumed"]+b["other_assumed"])
            grids.append({"ids":[aid,bid],"rents":[ar,br],"standard_balances":[am,bm],
                "annual_cashflows":[aa,ba],"coverage_leader":aid if am>bm else bid if bm>am else "tie",
                "annual_cash_leader":aid if aa>ba else bid if ba>aa else "tie",
                "boundary":"Conditional arithmetic only; input quarantine and G0 holds override eligible ranking."})
    controls=[]
    for c in working01["threshold_controls"]+supplement["threshold_controls"]:
        payment=pay(.9*c["price"],.04,35)
        controls.append({"id":c["id"],"price_floor_sensitivity":c["price"],"fee_proxy":c["fee_assumed"],
            "standard_rent_required":payment+c["fee_assumed"],"rent_for_6pct_gross":.005*c["price"],
            "annual_neutral_rent":12*(payment+c["fee_assumed"]+c["other_assumed"])/11,
            "entry_allowance":.15*c["price"]+c["refurb_assumed"],
            "full_draw_no_income_carry12":12*(payment+c["fee_assumed"]+c["other_assumed"]),
            "boundary":c["boundary"]+" Full draw is a scenario, not progressive interest or worst-case bound."})
    # Working02T03 remains a distinct six-row sensitivity; include by exact formula.
    for fee,rate in itertools.product((250,350,450),(.04,.055)):
        p=377000; payment=pay(.9*p,rate,35)
        controls.append({"id":"B07-T03","price_floor_sensitivity":p,"fee_proxy":fee,"actual_rate":rate,
            "standard_rent_required":pay(.9*p,.04,35)+fee,"rent_for_6pct_gross":.005*p,
            "annual_neutral_rent":12*(payment+fee+200)/11,"entry_allowance":.15*p+20000,
            "full_draw_no_income_carry12":12*(payment+fee+200),
            "boundary":"Ambang377k price-only sensitivity; repeated brochureTypeA and restricted270k cohort are not a confirmed selected offer. No current rent assigned."})
    base=[x for x in evaluations if x["scenario"]=="base"]
    assert len(evaluations)==308 and len(branches)==18 and len(pairs)==231 and len(grids)==126
    return {"version":supplement["version"],"source_commit":supplement["source_commit"],"config":cfg,
        "cases":cases,"case_status_overlays":supplement["status_overlays"],"evaluations":evaluations,
        "branches":branches,"thresholds":thresholds,"investor_exit_diagnostics":exit_tests,
        "pair_paths":pairs,"rent_rank_grids":grids,"threshold_controls":controls,
        "summary":{"operating_cases":len(cases),"evaluations":len(evaluations)+len(branches),
            "pair_paths":len(pairs),"pairs_preserving_synthetic_reserve":sum(x["reserve_pass"] for x in pairs),
            "rank_grid_cells":len(grids),"standard_nonshortfall":[x["id"] for x in base if x["standard_monthly_balance"]>=0],
            "annual_nonnegative":[x["id"] for x in base if x["cashflow_by_year"][0]>=0],
            "gross_at_least6pct":[x["id"] for x in base if x["gross_yield"]>=.06]},
        "checks":"Historical20inputs unchanged; closed-form debt, principal conservation, independent economic basis, discounted exit and annual cash identities passed; adverse-shock direction checked.",
        "decision_boundary":"All22operating cases retain G0STOP/G9Defer. No Deploy, actual finance, lease, inspection or outcome validation. Threshold controls are not additional operating investments."}
