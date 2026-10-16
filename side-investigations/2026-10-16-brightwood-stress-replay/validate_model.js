
function validate(api,cfg,full){
 const tests=[];const check=(name,ok)=>{tests.push({name,pass:!!ok});if(!ok)throw Error(name);};
 const near=(a,b)=>Math.abs(a-b)<.01;
 const get=(t,s,mode="self_paid_reference")=>full.results.find(r=>r.type===t&&r.scenario===s&&r.cost_mode===mode);
 for(const t of cfg.types){
  const r=get(t.id,"BASE"), L=t.gross*.9,R=t.rents.reduce((a,b)=>a+b,0), p=api.payment(L,.04,420);
  const closed=L*Math.pow(1+.04/12,60)-p*(Math.pow(1+.04/12,60)-1)/(.04/12);
  check(t.id+" independent closed-form debt",near(closed,r.exit_debt));
  check(t.id+" independent rent/cost identity",near(55*R-5*R*1.08-2.5*R-60*t.area*.35-60*p,r.operating_cash));
  check(t.id+" construction average",near(r.construction_interest,L*.04*4*.5));
  check(t.id+" rebate and nett identity",near(L,t.net)&&near(L+t.gross*.1,t.gross));
  check(t.id+" overrun loss exactly10k",near(r.profit_before_unpriced_costs-get(t.id,"S15_fitout10k").profit_before_unpriced_costs,10000));
  const crisis=get(t.id,"S8_crisis_once").annual[0];
  check(t.id+" S8 no double commission",near(crisis.collected,10*R)&&near(crisis.commission_incl_sst,1.08*R));
  check(t.id+" persistent S8 collections",near(get(t.id,"S8_crisis_persistent").rent_collected,50*R));
  const arrears=get(t.id,"S24_arrears_both");
  check(t.id+" arrears and existing void not duplicated",near(r.rent_collected-arrears.rent_collected,2*R)&&near(r.commission_total,arrears.commission_total));
  check(t.id+" one component arrears",near(r.profit_before_unpriced_costs-get(t.id,"S24_arrears_first").profit_before_unpriced_costs,2*t.rents[0]));
  const fees=get(t.id,"S12_fee5").annual;
  check(t.id+" AGM first2years and escalation",near(fees[0].fee,12*t.area*.35)&&near(fees[2].fee,12*t.area*.35*1.05)&&near(fees[4].fee,12*t.area*.35*Math.pow(1.05,3)));
  check(t.id+" legal coverage delta only",near(get(t.id,"BASE","advertised_legal_absorption").profit_before_unpriced_costs-r.profit_before_unpriced_costs,r.acquisition.legal_paid+r.acquisition.legal_sst));
  check(t.id+" future buyer haircut applied to resale only",near(r.future_buyer.loan_after10pct_valuation_haircut,.765*r.exit_price));
  const root=api.evaluate(t,{id:"TEST",exit_multiplier:r.break_even_exit_before_unpriced_costs/t.net},cfg,"self_paid_reference");
  check(t.id+" break-even root",near(root.profit_before_unpriced_costs,0));
  check(t.id+" renewal59months",near(get(t.id,"DIAG_renewal").rent_collected,59*R));
 }
 for(const r of full.results){
  check(r.type+"/"+r.scenario+"/"+r.cost_mode+" cash conservation",near(r.ledger.reduce((a,x)=>a+x.cash,0)+r.net_exit_cash,r.profit_before_unpriced_costs));
  check(r.type+"/"+r.scenario+"/"+r.cost_mode+" debt conservation",near(r.exit_debt+r.principal_repaid,cfg.types.find(t=>t.id===r.type).net));
  if(r.annual_irr_reference.annual!==null){
   const rate=Math.pow(1+r.annual_irr_reference.annual,1/12)-1;
   const npv=r.ledger.reduce((a,x)=>a+x.cash/Math.pow(1+rate,x.month),0)+r.net_exit_cash/Math.pow(1+rate,r.build_months+r.hold_months);
   check(r.type+"/"+r.scenario+"/"+r.cost_mode+" IRR residual",near(npv,0));
  }
 }
 check("zero-interest annuity",api.payment(12000,0,12)===1000);
 check("B fallback one contract",get("B","S23_B_whole").rent_streams.length===1&&get("B","S23_B_whole").monthly_rent===2500);
 check("no invented D whole fallback",!get("D","S23_B_whole"));
 check("104 evaluations",full.results.length===104);
 check("no removed stress reinstated",!cfg.scenarios.some(s=>/^S(5|6|9|10|11|13|14|22)(_|$)/.test(s.id)));
 return {checks:tests.length,passed:tests.filter(t=>t.pass).length,evaluations:full.results.length,tests,scope:"Arithmetic and selected boundary checks, not market validation"};
}
if(typeof module!=="undefined")module.exports={validate};

