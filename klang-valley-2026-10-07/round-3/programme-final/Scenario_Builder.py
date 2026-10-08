"""Whole-programme scenario integration. Pure calculation; no file or network operations."""
import ast
import copy
import itertools

def build(inputs, engine_source, cfg):
    body=[n for n in ast.parse(engine_source).body if isinstance(n,ast.FunctionDef)
          and n.name in ("payment","evaluate","check_financial_identities")]
    ns={"CFG":cfg};exec(compile(ast.Module(body=body,type_ignores=[]),"<frozen-functions>","exec"),ns)
    ev,check,pay=ns["evaluate"],ns["check_financial_identities"],ns["payment"]
    cases=copy.deepcopy(inputs["source_cases"])
    assert len(cases)==138 and len({c["id"] for c in cases})==138
    byid={c["id"]:c for c in cases};meta=inputs["case_metadata"]
    assert set(meta)==set(byid) and {m["area_id"] for m in meta.values()}=={"A%02d"%i for i in range(1,62)}
    k=pay(.9,.04,35)
    combined={"rate":.055,"rent_factor":.8,"fee_factor":1.2,"first_year_paid":6,"levy_month":1,"levy":30000}
    scenarios={
        "base":{},"rate5_5":{"rate":.055},"rent_down20":{"rent_factor":.8},
        "fee_up20":{"fee_factor":1.2},"zero_rent12":{"initial_vacancy":12},
        "works30k_m24":{"levy_month":24,"levy":30000},"bank_value_down15":{"valuation_ratio":.85},
        "term25":{"term":25},"exit_delay12":{"months":72},
        "unquoted_cost_buffer":{"annual_extra_cost":1200,"exit_extra_cost":5000},
        "combined5yr":dict(combined),"combined12mo":dict(combined,months=12),
        "combined_no_sale24mo":dict(combined,months=24),
        "combined_credit12mo":dict(combined,months=12,valuation_ratio=.85,term=25),
        "combined_credit24mo":dict(combined,months=24,valuation_ratio=.85,term=25),
        "combined_credit60mo":dict(combined,months=60,valuation_ratio=.85,term=25)}
    full={};evaluations=[];thresholds=[];exits=[]
    for c in cases:
        lo,hi=inputs["rent_bounds"][c["id"]]
        params=dict(scenarios,
          rent_low={"rent_factor":lo/c["rent_assumed"]},
          rent_high={"rent_factor":hi/c["rent_assumed"]},
          rent_low_feeup20={"rent_factor":lo/c["rent_assumed"],"fee_factor":1.2})
        local={}
        for label,p in params.items():
            r=ev(c,**p);check(r,c,p.get("exit_extra_cost",0))
            r.update(scenario=label,parameters=p,
                scenario_monthly_coverage=c["rent_assumed"]*p.get("rent_factor",1)-r["actual_instalment"]-c["fee_assumed"]*p.get("fee_factor",1))
            local[label]=r
            saved=copy.deepcopy(r);saved.pop("schedule");saved.pop("cash_path")
            if label in ("base","combined12mo","combined_no_sale24mo","combined_credit12mo","combined_credit24mo"):
                saved["monthly_cashflows"]=[x["cashflow"] for x in r["schedule"]]
            evaluations.append(saved)
        full[c["id"]]=local;b=local["base"]
        assert abs(b["entry_cash"]-(.15*c["price"]+c["refurb_assumed"]))<.01
        assert abs(b["cashflow_by_year"][0]-(11*c["rent_assumed"]-12*(k*c["price"]+c["fee_assumed"]+c["other_assumed"])))<.01
        for adverse in ("rate5_5","rent_down20","fee_up20","zero_rent12","works30k_m24","unquoted_cost_buffer","combined5yr"):
            assert local[adverse]["terminal_nominal_breakeven"]>b["terminal_nominal_breakeven"]
        thresholds.append({"id":c["id"],"standard_rent_required":k*c["price"]+c["fee_assumed"],
            "annual_neutral_rent":12*(k*c["price"]+c["fee_assumed"]+c["other_assumed"])/11,
            "rent_for_6pct_gross":.005*c["price"],
            "price_for_annual_neutral":max(0,(11*c["rent_assumed"]/12-c["fee_assumed"]-c["other_assumed"])/k),
            "price_for_standard":max(0,(c["rent_assumed"]-c["fee_assumed"])/k),
            "price_for_6pct":200*c["rent_assumed"]})
        noi=11*c["rent_assumed"]-12*(c["fee_assumed"]+c["other_assumed"]);be=b["terminal_nominal_breakeven"]
        exits.append({"id":c["id"],"net_operating_income":noi,"operating_yield_at_recovery":noi/be,
            "buyer_standard_entry_at_recovery":.15*be+c["refurb_assumed"],
            "buyer_stress_entry_at_recovery":.35*be+c["refurb_assumed"],
            "buyer_standard_payment":pay(.9*be,.04,35),"buyer_stress_payment":pay(.7*be,.055,25),
            "required_yield_exits":[{"operating_yield":y,"income_only_value":noi/y,
                "investor_profit":.97*noi/y-b["terminal_debt"]+b["cashflow_total"]-b["entry_cash"]}
                for y in (.05,.06,.07)]})
    def portfolio(ids,label,months):
        rs=[full[i][label] for i in ids]
        entry=sum(r["entry_cash"] for r in rs)
        path=[cfg["synthetic_cash"]-entry]
        for n in range(months):
            path.append(path[-1]+sum(r["schedule"][n]["cashflow"] for r in rs))
        assert len(path)==months+1
        return {"entry_cash":entry,"minimum_cash":min(path),"minimum_month":path.index(min(path)),
            "ending_cash":path[-1],"reserve_pass":min(path)>=cfg["synthetic_protected_reserve"],
            "initial_reserve_pass":path[0]>=cfg["synthetic_protected_reserve"],
            "required_starting_cash_for_protected_reserve":cfg["synthetic_protected_reserve"]+cfg["synthetic_cash"]-min(path),
            "cash_path":path}
    pairs=[]
    for a,b in itertools.combinations(byid,2):
        same=meta[a]["project_id"]==meta[b]["project_id"]
        x={"ids":[a,b],"same_project_alternatives":same,
           "special_verification_hold":bool(meta[a]["special_holds"] or meta[b]["special_holds"])}
        for label,months in (("combined12mo",12),("combined_credit24mo",24)):
            p=portfolio([a,b],label,months);p.pop("cash_path");x[label]=p
        pairs.append(x)
    project_pairs={}
    for p in pairs:
        if p["same_project_alternatives"]: continue
        key=tuple(sorted(meta[i]["project_id"] for i in p["ids"]))
        project_pairs.setdefault(key,[]).append(p)
    project_ranges=[]
    for key,variants in sorted(project_pairs.items()):
        row={"project_ids":list(key),"expression_variants":len(variants)}
        for label in ("combined12mo","combined_credit24mo"):
            row[label]={"all_variants_pass":all(v[label]["reserve_pass"] for v in variants),
                "any_variant_pass":any(v[label]["reserve_pass"] for v in variants),
                "worst_minimum_cash":min(v[label]["minimum_cash"] for v in variants),
                "best_minimum_cash":max(v[label]["minimum_cash"] for v in variants)}
        project_ranges.append(row)
    assert len(project_ranges)==7381 and sum(r["expression_variants"] for r in project_ranges)==9436
    studies=[]
    for study in inputs["study_portfolios"]:
        assert len({meta[i]["project_id"] for i in study["ids"]})==len(study["ids"])
        r=copy.deepcopy(study);r["project_ids"]=[meta[i]["project_id"] for i in study["ids"]]
        r["special_holds"]={i:meta[i]["special_holds"] for i in study["ids"] if meta[i]["special_holds"]}
        r["paths"]={label:portfolio(study["ids"],label,months) for label,months in (
           ("base",60),("combined12mo",12),("combined_no_sale24mo",24),
           ("combined_credit12mo",12),("combined_credit24mo",24))}
        r["base_annual_cashflow"]=sum(full[i]["base"]["cashflow_by_year"][0] for i in study["ids"])
        r["base_flat_price_profit"]=sum(full[i]["base"]["profit_by_exit_multiple"]["1"] for i in study["ids"])
        studies.append(r)
    grids=[]
    for aid,bid in inputs["cross_task_pairs"]:
        a,b=byid[aid],byid[bid]
        for ar,br in itertools.product((inputs["rent_bounds"][aid][0],a["rent_assumed"],inputs["rent_bounds"][aid][1]),
                                        (inputs["rent_bounds"][bid][0],b["rent_assumed"],inputs["rent_bounds"][bid][1])):
            aa=11*ar-12*(k*a["price"]+a["fee_assumed"]+a["other_assumed"])
            ba=11*br-12*(k*b["price"]+b["fee_assumed"]+b["other_assumed"])
            grids.append({"ids":[aid,bid],"rents":[ar,br],"annual_cashflows":[aa,ba],
                          "annual_cash_leader":aid if aa>ba else bid if ba>aa else "tie"})
    base=[r for r in evaluations if r["scenario"]=="base"]
    distinct=[p for p in pairs if not p["same_project_alternatives"]]
    assert len(evaluations)==2622 and len(pairs)==9453 and len(distinct)==9436 and len(grids)==180
    summary={"operating_expressions":len(cases),"project_groups":len({m["project_id"] for m in meta.values()}),
        "areas":len({m["area_id"] for m in meta.values()}),"evaluations":len(evaluations),
        "all_pairs":len(pairs),"same_project_pairs":len(pairs)-len(distinct),"distinct_project_pairs":len(distinct),
        "distinct_pair_reserve_pass12":sum(p["combined12mo"]["reserve_pass"] for p in distinct),
        "distinct_pair_reserve_pass_credit24":sum(p["combined_credit24mo"]["reserve_pass"] for p in distinct),
        "monthly_nonshortfall":[r["id"] for r in base if r["standard_monthly_balance"]>=0],
        "gross_at_least6":[r["id"] for r in base if r["gross_yield"]>=.06],
        "annual_nonnegative":[r["id"] for r in base if r["cashflow_by_year"][0]>=0],
        "flat_price_profit_nonnegative":[r["id"] for r in base if r["profit_by_exit_multiple"]["1"]>=0],
        "low_rent_fee20_annual_nonnegative":[r["id"] for r in evaluations if r["scenario"]=="rent_low_feeup20" and r["cashflow_by_year"][0]>=0],
        "study_portfolios":len(studies),"rank_grid_cells":len(grids),
        "unique_project_pair_groups":len(project_ranges),
        "project_pairs_all_variants_pass12":sum(r["combined12mo"]["all_variants_pass"] for r in project_ranges),
        "project_pairs_any_variant_pass12":sum(r["combined12mo"]["any_variant_pass"] for r in project_ranges),
        "project_pairs_all_variants_pass_credit24":sum(r["combined_credit24mo"]["all_variants_pass"] for r in project_ranges),
        "project_pairs_any_variant_pass_credit24":sum(r["combined_credit24mo"]["any_variant_pass"] for r in project_ranges)}
    return {"version":inputs["version"],"source_commit":inputs["source_commit"],"config":cfg,
        "case_metadata":meta,"evaluations":evaluations,"thresholds":thresholds,"terminal_tests":exits,
        "pair_results":pairs,"project_pair_ranges":project_ranges,"study_portfolios":studies,"cross_task_rank_grids":grids,"summary":summary,
        "boundary":"All138G0STOP/G9Defer. Source objects/overlays are in Inputs.json. Historical branches remain separate. No source inference, forecast validation, investment admission or user capital allocation is created. Alternative projects are not independent risk factors.",
        "checks":"Frozen-function financial identities; principal conservation; annual/entry identities; adverse direction;138unique cases/61areas/122projectgroups; same-project exclusion; deterministic cash paths."}
