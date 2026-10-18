"use strict";
const fs=require("fs"),path=require("path"),assert=require("assert");
const base=path.resolve(__dirname,"../sop-v2-all-base-replay-2026-10-16");
const I=JSON.parse(fs.readFileSync(path.join(base,"Inputs.json"),"utf8"));
const D=JSON.parse(fs.readFileSync(path.join(__dirname,"Diagnostics.json"),"utf8"));
const {runCase}=require(path.join(base,"financial_model.cjs"));
let checks=0;
const close=(a,b)=>{checks++;assert(Number.isFinite(a)&&Math.abs(a-b)<1e-7);};
for(const e of D.results){
 const b=I.bases.find(x=>x.id===e.case_id);
 const r=runCase({...b,price:e.price,rent:e.rent},{id:e.scenario,exit:e.exit_price/e.price},I);
 close(r.profit,e.profit);close(r.annual_mean_cash,e.annual);close(r.peak_funding,e.peak);
 close(e.annual,9.42*e.rent-12*e.fee-12*e.payment);
 close(e.narrow,e.rent-e.fee-e.payment);close(e.profit,e.economic);
 close(e.receipts,55*e.rent);close(e.commissions,5*1.08*e.rent);
 close(e.paid,55);close(e.new_leases,5);close(e.fitout,.05*e.price);
 const m=.04/12,L=.9*e.price;
 close(e.closing_debt,L*Math.pow(1+m,60)-e.payment*(Math.pow(1+m,60)-1)/m);
}
for(const id of ["R309","R219"]){const b=I.bases.find(x=>x.id===id);close(runCase({...b,rent:D.roots[id].annual_neutral_rent},{id:"root"},I).annual_mean_cash,0);}
close(D.results.find(x=>x.label==="A_old"&&x.scenario==="target").annual,1312.5737928905558);
close(D.results.find(x=>x.label==="N_old"&&x.scenario==="target").annual,138.25215304854436);
console.log({checks,passed:true,meaning:"Conditional model verification, not market or gate validation"});
