"use strict";
function validate(I,O,A){
 let count=0;function check(ok,msg){count++;if(!ok)throw Error(msg);}
 function near(a,b,msg,tol=1e-5){check(Math.abs(a-b)<=tol,msg);}
 check(I.bases.length===10&&new Set(I.bases.map(x=>x.id)).size===10,"base universe");
 check(I.held_alternatives.length===18&&new Set(I.held_alternatives.map(x=>x.label)).size===18,"held universe");
 for(const r of [...O.results,...O.alternatives]){
  const tag=r.case_id+"/"+r.scenario;
  near(r.profit,r.economic_profit_check,tag+" economic conservation");
  near(r.loan-r.payments+r.interest,r.closing_debt,tag+" loan conservation");
  near(r.profit,-r.initial_cash+r.operating_cash+r.net_sale_cash,tag+" owner cash");
  near(r.peak_funding,Object.values(r.peak_breakdown).reduce((a,b)=>a+b,0),tag+" peak");
  near(r.selling.total,Object.entries(r.selling).filter(([k])=>k!=="total").reduce((a,[k,v])=>a+v,0),tag+" seller costs");
  near(r.break_even_exit-A.exitCost(r.break_even_exit,r.scenario==="NO_ADDITIONAL_INVOICE_TAX"?0:.08,I.fee_reference).total-r.closing_debt-r.initial_cash+r.operating_cash,0,tag+" exit root");
  const rate=O.scenarios.find(x=>x.id===r.scenario)?.rate??.04,rr=rate/12;
  near(r.closing_debt,r.loan*Math.pow(1+rr,r.hold_months)-r.payment*(Math.pow(1+rr,r.hold_months)-1)/rr,tag+" independent amortisation");
  check(r.g0==="STOP"&&r.g9==="Defer",tag+" no admission");
 }
 for(const r of O.results.filter(x=>x.scenario==="BASE")){
  const src=I.bases.find(x=>x.id===r.case_id),get=id=>O.results.find(x=>x.case_id===r.case_id&&x.scenario===id);
  near(r.receipts,55*r.rent,"55 receipts");check(r.paid_months===55&&r.new_leases===5,"event counts");
  near(r.commissions,5*1.08*r.rent,"commission");near(r.repairs,2.5*r.rent,"repair");
  near(r.annual_mean_cash-src.old_annual_cash,12*src.old_other-1.58*r.rent,"old to new operating bridge");
  near(r.annual_mean_cash,9.42*r.rent-12*(r.payment+r.fee),"independent operating equation");
  near(get("S24").receipts,r.receipts-2*r.rent,"arrears overlap");
  near(get("S15").profit,r.profit-10000,"overrun conservation");
  near(get("RENEWAL").receipts,59*r.rent,"renewal no void");
  check(get("S8_persistent").paid_months===50,"persistent crisis calendar");
  check(get("S8_once").paid_months===54,"initial crisis calendar");
  near(get("S17").exit_price,r.exit_price,"delay no growth");
  near(get("OLD_FITOUT_DIAGNOSTIC").profit,r.profit-src.old_fitout+r.fitout,"fitout sensitivity");
  if(r.annual_irr!==null){const mr=Math.pow(1+r.annual_irr,1/12)-1;
   near(-r.initial_cash+r.ledger.reduce((a,x)=>a+x.net_cash/Math.pow(1+mr,x.month),0)+r.net_sale_cash/Math.pow(1+mr,r.hold_months),0,"IRR independent discount",1e-4);
  }
 }
 near(A.duty(350000),6000,"reference duty fixture");near(A.legal(700000),8250,"legal scale fixture");
 return {passed:count,evaluations:O.results.length+O.alternatives.length,boundary:"Arithmetic, source bridge and event checks; not empirical market validation."};
}
if(typeof module!=="undefined")module.exports={validate};
