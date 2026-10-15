"""Brightwood case-only lifecycle model. Run: python financial_model.py < Financial_Inputs.json
Pure standard library; stdout JSON; no file writes. Gross-based debt is the user's case instruction.
Unquoted scenarios, not valuation, loan approval or an investment recommendation.
"""
import json, sys, math
def payment(loan, rate, years):
    if not 0 <= rate or years <= 0 or loan < 0:
        raise ValueError('Invalid loan inputs')
    r = rate / 12
    return loan / (years * 12) if r == 0 else loan * r / (1 - (1 + r) ** (-years * 12))

def evaluate(t, rent, cfg, name="base", rate=.04, term=35, build=48, op=60,
             paid=None, fee_psf=.35, other=200, works=0, credit_ratio=1,
             initial_paid=None, draw_avg=.5, fitout_delta=0, extra_exit=0, acq_fraction=.05):
    p=t["net"]; gross=t["gross"]; loan=.9*gross*credit_ratio
    assert p is not None and 0 <= credit_ratio <= 1 and build >= 0
    streams=rent if isinstance(rent,list) else [rent]
    months=paid if paid is not None else [11]*len(streams)
    assert len(streams)==len(months) and all(0<=n<=12 for n in months)
    total=sum(streams); fee=t["bua"]*fee_psf; pay=payment(loan,rate,term)
    std=payment(.9*gross,.04,35)
    costbase=acq_fraction*gross
    fitout=t["fitout"]+fitout_delta
    equity=max(0,p-loan)
    excess=max(0,loan-p) # Not assumed to become spendable or recoverable cash.
    entry=equity+costbase+fitout
    debt=loan; path=[-equity-costbase]; schedule=[]
    ci=0
    for m in range(1,build+1):
        # midpoint linear draw averages 50%; 25/75% paths are shaped alternatives.
        frac=((m-.5)/build)**(1/draw_avg-1)
        interest=loan*frac*rate/12
        ci+=interest; path.append(path[-1]-interest)
    path[-1]-=fitout
    interest_sum=0; principal_sum=0; cash=0; operations_net=0
    for m in range(1,op+1):
        ns=initial_paid if initial_paid is not None and m<=12 else months
        collected=sum(v for v,n in zip(streams,ns) if (m-1)%12+1>12-n)
        repair=.05*collected
        letting=.5*total/12 # 0.5 month per component per year, summed once.
        operating=fee+other+repair+letting
        capital=works if m==12 else 0
        interest=debt*rate/12; principal=pay-interest; debt-=principal
        cf=collected-operating-pay-capital
        cash+=cf; interest_sum+=interest; principal_sum+=principal
        operations_net+=collected-operating-capital
        path.append(path[-1]+cf)
        schedule.append(dict(month=m,collection=collected,interest=interest,principal=principal,debt=debt,cashflow=cf))
    terminal=(entry+ci-cash+debt+extra_exit)/.97
    flat=.97*p-extra_exit-debt+cash-entry-ci
    econ=p+costbase+fitout+excess+ci+interest_sum-operations_net+extra_exit
    r=rate/12
    closed=loan*(1+r)**op-pay*((1+r)**op-1)/r if r else loan-pay*op
    assert abs(closed-debt)<.01
    assert abs(principal_sum+debt-loan)<.01
    assert abs(econ/.97-terminal)<.01
    assert abs(.97*terminal-extra_exit-debt+cash-entry-ci)<.01
    annual=sum(v*n*.95 for v,n in zip(streams,months))-.5*total-12*(fee+other+pay)
    neutral=(12*(fee+other+pay))/9.95
    return dict(id=t["id"],scenario=name,net=p,gross=gross,loan=loan,rate=rate,term=term,
        rent=total,rent_streams=streams,paid_months=months,fee=fee,payment=pay,
        standard_payment=std,standard_coverage=total-std-fee,gross_yield_on_net=12*total/p,
        rent_for_6pct=.005*p,annual_cash_stabilised=annual,annual_neutral_rent_11months=neutral,
        acquisition_allowance=costbase,fitout=fitout,net_equity=equity,uncredited_excess_loan=excess,
        entry_cash_excluding_construction_interest=entry,build_months=build,operating_months=op,
        construction_interest=ci,cashflow_operating=cash,first_year_cash=sum(x["cashflow"] for x in schedule[:12]),
        terminal_debt=debt,nominal_break_even_exit=terminal,flat_net_price_profit=flat,
        break_even_appreciation_from_net=terminal/p-1,
        annualised_price_growth_burden=(terminal/p)**(12/(build+op))-1,
        maximum_cumulative_cash_required=-min(path),funding_path=path,
        exit_scenarios={str(k):.97*p*k-extra_exit-debt+cash-entry-ci for k in [.8,1,1.15]},
        investor_exit_6pct_rent_required=terminal*.005,
        future_buyer_payment_standard=payment(.9*terminal,.04,35),
        future_buyer_payment_credit_stress=payment(.8*terminal,.055,25),
        gross_deposit_bridge=.1*gross,
        bridge_peak_upper=max(0,-min(path))+.1*gross,
        checks="amortisation; principal conservation; equity and independent economic break-even")
def main(cfg):
    assert cfg["standard"] == {"ltv_on_gross":.9,"rate":.04,"years":35,"preferred_gross_yield":.06}
    assert cfg["costs"] == {"fee_psf_month":.35,"paid_months":11,"repairs_fraction_collected":.05,"letting_months_per_year":.5,"other_monthly":200,"acquisition_allowance_fraction_gross":.05,"disposal_fraction":.03}
    types=cfg["types"]; rows=[]; base={}
    for t in types:
        if t["net"] is None: continue
        for rent in t["rents"]:
            streams=[rent/2,rent/2] if t["id"]=="D" else [rent]
            x=evaluate(t,streams,cfg,name="rent_"+str(rent)); rows.append(x)
            if rent==t["rents"][1]: base[t["id"]]=x
    sens=[]
    for t in types:
        if t["id"] not in ["D","B"]: continue
        total=t["rents"][1]; rent=[total/2]*2 if t["id"]=="D" else [total]
        options=[
        ("rate_5.5",dict(rate=.055)),("fee_.50",dict(fee_psf=.5)),("term_31",dict(term=31)),
        ("term_25",dict(term=25)),("valuation_down15",dict(credit_ratio=.85)),
        ("build_36",dict(build=36)),("build_60",dict(build=60)),
        ("draw_frontloaded",dict(draw_avg=.75)),("draw_backloaded",dict(draw_avg=.25)),
        ("extra_operating100",dict(other=300)),("works30k",dict(works=30000)),
        ("fitout_extra20k",dict(fitout_delta=20000)),("extra_exit10k",dict(extra_exit=10000)),("acquisition_allowance_zero_diagnostic",dict(acq_fraction=0)),
        ("exit_delay12",dict(op=72)),("no_rent_first12",dict(initial_paid=[0]*len(rent))),
        ("correlated_shock",dict(rate=.055,build=60,op=72,initial_paid=[6]*len(rent),
            fee_psf=.5,other=300,works=30000,credit_ratio=.85,term=31))
        ]
        for name,kw in options:
            shockrent=[r*.8 for r in rent] if name=="correlated_shock" else rent
            sens.append(evaluate(t,shockrent,cfg,name=name,**kw))
        if t["id"]=="D":
            sens.append(evaluate(t,[1300,1300],cfg,name="asymmetric_10_8_months",paid=[10,8]))
            sens.append(evaluate(t,[1300,0],cfg,name="one_side_zero_entire_hold",paid=[11,0]))
        grosscase=dict(t,net=t["gross"])
        sens.append(evaluate(grosscase,rent,cfg,name="gross_paid_no_rebate_counterfactual"))
        exactnet=dict(t,net=.9*t["gross"])
        sens.append(evaluate(exactnet,rent,cfg,name="rounded_net_plus_delta"))
    screen=[]
    for t in types:
        for gp in [t["gross"],t["gross_max"]]:
            fee=t["bua"]*.35; pay=payment(.9*gp,.04,35)
            screen.append(dict(id=t["id"],gross=gp,net=t["net"] if gp==t["gross"] else None,
                fee=fee,payment=pay,coverage_rent=pay+fee,annual_neutral_rent=(12*(pay+fee+200))/9.95,
                net_6pct_rent=.005*t["net"] if t["net"] is not None and gp==t["gross"] else None))
    roots=[]
    for id in ["D","B"]:
        t=next(t for t in types if t["id"]==id); ratio=t["net"]/t["gross"]; fee=t["bua"]*.35
        for rent in [2200,2300,2600,2800,3000,3200]:
            maxgross=(9.95*rent-12*(fee+200))/(12*payment(.9,.04,35))
            maxnet=maxgross*ratio
            assert abs(9.95*rent-12*(payment(.9*maxgross,.04,35)+fee+200))<.01
            roots.append(dict(id=id,rent=rent,annual_neutral_max_gross=maxgross,
                annual_neutral_max_net_if_same_package_ratio=maxnet,
                six_pct_max_net=200*rent,
                warning="cashflow threshold only; changes gross and debt with net; net-only rebate does not reduce loan"))
    shock=[x for x in sens if x["scenario"]=="correlated_shock"]
    pair=[500000+sum(x["funding_path"][i] for x in shock) for i in range(len(shock[0]["funding_path"]))]
    # The two synchronized scenarios have equal durations.
    assert len(shock)==2 and len(shock[0]["funding_path"])==len(shock[1]["funding_path"])
    return dict(base=base,rent_scenarios=rows,sensitivities=sens,type_screen=screen,thresholds=roots,
        portfolio=dict(synthetic_start=500000,protected_reserve=150000,minimum_cash=min(pair),
          reserve_pass=min(pair)>=150000,minimum_if_deposit_bridge_reserved=min(pair)-sum(x["gross_deposit_bridge"] for x in shock),
          required_start_to_preserve_reserve=150000+500000-min(pair),
          note="not user finances; same-project pair is correlated; bridge upper reservation is conservative, not a timed settlement"),
        tests=dict(evaluations=len(rows)+len(sens),threshold_roots=len(roots),type_price_screens=len(screen),passed=True))
if __name__=="__main__":
    print(json.dumps(main(json.load(sys.stdin)),indent=2))
