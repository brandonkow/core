"use strict";
const fs=require("fs"),path=require("path"),assert=require("assert");
const base=path.resolve(__dirname,"../sop-v2-all-base-replay-2026-10-16");
const I=JSON.parse(fs.readFileSync(path.join(base,"Inputs.json"),"utf8"));
const D=JSON.parse(fs.readFileSync(path.join(__dirname,"Diagnostics.json"),"utf8"));
const E=JSON.parse(fs.readFileSync(path.join(__dirname,"Evidence.json"),"utf8"));
const {runCase}=require(path.join(base,"financial_model.cjs"));
const b=I.bases.find(x=>x.id==="R219");
let checks=0;
function test(ok){checks++;assert(ok);}
function close(a,b){test(Number.isFinite(a)&&Math.abs(a-b)<1e-7);}
for(const e of D.results){
 const r=runCase({...b,price:e.price,rent:e.rent},{id:e.scenario,exit:e.exit_price/e.price},I);
 close(r.profit,e.profit);close(r.annual_mean_cash,e.annual);
 close(r.standard_monthly_balance,e.narrow);close(r.peak_funding,e.peak);
 close(r.payment,e.monthly_payment);close(r.profit,r.economic_profit_check);
 close(e.annual,9.42*e.rent-12*210-12*e.monthly_payment);
 close(r.loan,.9*e.price);close(r.fitout,.05*e.price);
 close(r.paid_months,55);close(r.new_leases,5);
}
const lo=D.results.find(x=>x.price===265000&&x.scenario==="fixed_318k");
const hi=D.results.find(x=>x.price===280000&&x.scenario==="fixed_318k");
close(lo.profit,38013.69515891868);
close(lo.annual,1763.7869116266563);
close(lo.annual-hi.annual,717.2950804739648);
close(lo.profit-hi.profit,19106.685179683467);
test(E.disposition.first_unresolved_gate==="G0");
test(E.disposition.contiguous_passed_prefix.length===0);
test(E.disposition.g9==="Defer"&&!E.disposition.cleared);
test(D.accepted_market_input_updates.length===0);
test(E.sources.find(x=>x.id==="ND01").observed.bay_count_in_document===1);
test(E.sources.find(x=>x.id==="ND02").observed.bays_claimed===2);
console.log({checks,passed:true,evaluations:D.results.length,meaning:"Arithmetic, source-scope and admission-boundary checks; not market validation"});
