"""Read-only, deterministic B07 scenario builder. No market validation or file writes."""
import ast
import itertools

def build(inputs, engine_source, cfg):
    tree = ast.parse(engine_source)
    ns = {"CFG": cfg}
    module = ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in ("payment", "evaluate", "check_financial_identities")], type_ignores=[])
    exec(compile(module, "<frozen-financial-functions>", "exec"), ns)
    ev, check, payment = ns["evaluate"], ns["check_financial_identities"], ns["payment"]
    cases = inputs["inherited_cases"] + inputs["working_01_cases"] + inputs["new_cases"]
    assert len(cases) == 19 and len({c["id"] for c in cases}) == 19
    scenarios = {
        "base": {},
        "rate_5_5pct": {"rate": .055},
        "rent_down20": {"rent_factor": .8},
        "fee_up20": {"fee_factor": 1.2},
        "zero_rent_first12": {"initial_vacancy": 12},
        "works30k_month24": {"levy_month": 24, "levy": 30000},
        "bank_value_down15": {"valuation_ratio": .85},
        "term25": {"term": 25},
        "exit_delay12": {"months": 72},
        "unquoted_cost_buffer": {"annual_extra_cost": 1200, "exit_extra_cost": 5000},
        "combined5yr": {"rate": .055, "rent_factor": .8, "fee_factor": 1.2, "first_year_paid": 6, "levy_month": 1, "levy": 30000},
        "combined12mo": {"months": 12, "rate": .055, "rent_factor": .8, "fee_factor": 1.2, "first_year_paid": 6, "levy_month": 1, "levy": 30000},
    }
    evaluations = []
    thresholds = []
    for c in cases:
        for label, params in list(scenarios.items()) + [("rent_low", {"rent_factor": c["rent_low"]/c["rent_assumed"]}), ("rent_high", {"rent_factor": c["rent_high"]/c["rent_assumed"]})]:
            r = ev(c, **params)
            check(r, c, params.get("exit_extra_cost", 0))
            r.update(scenario=label, parameters=params, input_overrides={})
            evaluations.append(r)
        instalment = payment(.9*c["price"], .04, 35)
        k = payment(.9, .04, 35)
        thresholds.append(dict(id=c["id"], standard_rent_required=instalment+c["fee_assumed"],
            rent_for_6pct=.005*c["price"],
            annual_neutral_rent=12*(instalment+c["fee_assumed"]+c["other_assumed"])/11,
            price_for_standard_coverage=max(0,(c["rent_assumed"]-c["fee_assumed"])/k),
            price_for_6pct=200*c["rent_assumed"],
            price_for_annual_neutral=max(0,(11*c["rent_assumed"]/12-c["fee_assumed"]-c["other_assumed"])/k)))
    byid = {c["id"]:c for c in cases}
    branches = []
    for branch in inputs["branches"]:
        c = dict(byid[branch["parent"]], **branch["overrides"])
        r = ev(c, **branch["parameters"])
        check(r, c, branch["parameters"].get("exit_extra_cost",0))
        r.update(scenario=branch["label"], parameters=branch["parameters"], input_overrides=branch["overrides"], boundary=branch.get("boundary",""))
        branches.append(r)
    stress = [x for x in evaluations if x["scenario"]=="combined12mo"]
    pairs = []
    for a,b in itertools.combinations(stress,2):
        path=[cfg["synthetic_cash"]-a["entry_cash"]-b["entry_cash"]]
        for ma,mb in zip(a["schedule"],b["schedule"]):
            path.append(path[-1]+ma["cashflow"]+mb["cashflow"])
        pairs.append(dict(ids=[a["id"],b["id"]],cash_path=path,minimum_cash=min(path),reserve_pass=min(path)>=cfg["synthetic_protected_reserve"]))
    grids=[]
    for aid,bid in [("KV13","R338"),("R230","R339"),("R231","R341"),("R232","R342"),("R234","R343"),("R235","R347"),("R236","R345")]:
        a,b=byid[aid],byid[bid]
        for ar,br in itertools.product((a["rent_low"],a["rent_assumed"],a["rent_high"]),(b["rent_low"],b["rent_assumed"],b["rent_high"])):
            am=ar-payment(.9*a["price"],.04,35)-a["fee_assumed"]
            bm=br-payment(.9*b["price"],.04,35)-b["fee_assumed"]
            grids.append(dict(ids=[aid,bid],rents=[ar,br],standard_balances=[am,bm],coverage_leader=aid if am>bm else bid if bm>am else "tie"))
    controls=[]
    for c in inputs["threshold_controls"]:
        pay=payment(.9*c["price"],.04,35)
        controls.append(dict(id=c["id"],price_floor_assumed=c["price"],fee_proxy=c["fee_assumed"],
            standard_rent_required=pay+c["fee_assumed"],rent_for_6pct=.005*c["price"],
            annual_neutral_rent=12*(pay+c["fee_assumed"]+c["other_assumed"])/11,
            entry_allowance=.15*c["price"]+c["refurb_assumed"],
            full_draw_no_income_carry12=12*(pay+c["fee_assumed"]+c["other_assumed"]),
            boundary=c["boundary"]+" Full-draw carry is illustrative only, not actual progressive interest or a worst-case bound."))
    return dict(version="B07-WORKING-01",config=cfg,source_commit=inputs["source_commit"],
        cases=cases,evaluations=evaluations,branches=branches,thresholds=thresholds,
        new_launch_controls=controls,pairs=pairs,rank_grids=grids,
        evaluation_count=len(evaluations)+len(branches),
        evidence_boundary="Conditional arithmetic, not observed investment returns. No unit passes G0; all G9 Defer. Scenarios rent_low/high retain base standard_balance by frozen-engine definition; actual cash flows use rent_factor. Recompute coverage at low/high separately in rank_grids.",
        checks="amortisation, principal conservation, independent cost basis and discounted exit identities passed")
