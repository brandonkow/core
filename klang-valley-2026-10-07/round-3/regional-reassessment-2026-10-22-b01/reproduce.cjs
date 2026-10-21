"use strict";
// RAM-only reproduction. Requires Node.js and authenticated gh; writes no files.
// node reproduce.cjs <packet commit or main>
const {execFileSync}=require("node:child_process");
const ref=process.argv[2]||"main";
function read(path,sha){const j=JSON.parse(execFileSync("gh",["api","repos/brandonkow/core/contents/"+path+"?ref="+sha],{encoding:"utf8",maxBuffer:30*1024*1024}));return Buffer.from(j.content,"base64").toString("utf8");}
const I=JSON.parse(read("klang-valley-2026-10-07/round-3/regional-reassessment-2026-10-22-b01/Financial_Inputs.json",ref));
const model=read(I.model_path,I.source_commit);
const expected=JSON.parse(read("klang-valley-2026-10-07/round-3/regional-reassessment-2026-10-22-b01/Financial_Diagnostics.json",ref));
function calculate(I,model){
const mod={exports:{}};new Function("module",model)(mod); const {runCase,pmt}=mod.exports;const results=[],checks=[];
function assert(c,label){if(!c)throw Error(label);checks.push(label);}
function add(c,s,label){const r=runCase(c,s,I,true);delete r.g0;delete r.g9;r.profile=label;
assert(Math.abs(r.profit-r.economic_profit_check)<1e-6,label+":"+s.id+":cash-economic");
assert(Math.abs(Object.values(r.peak_breakdown).reduce((a,b)=>a+b,0)-r.peak_funding)<1e-6,label+":"+s.id+":peak");
assert(Math.abs(r.loan-r.payments+r.interest-r.closing_debt)<1e-6,label+":"+s.id+":debt");
assert(Math.abs(r.net_sale_cash-r.exit_price+r.selling.total+r.closing_debt)<1e-6,label+":"+s.id+":sale");
assert(!("g0" in r)&&!("g9" in r),label+":"+s.id+":no-financial-gate");
if(s.id==="BASE"){assert(r.paid_months===55&&r.new_leases===5,label+":lease-timing");}
if(s.id==="RENEWAL_FLAT"){assert(r.paid_months===59&&r.new_leases===1&&r.renewals===4,label+":renewal-timing");}
if(s.id!=="BASE")delete r.ledger;results.push(r);}
for(const c of I.bases)for(const s of I.scenarios)add(c,s,c.id);
for(const v of I.variants){const c={...I.bases.find(c=>c.id===v.case_id),...v.changes};for(const s of [{id:"BASE"},{id:"FLAT",exit:1}])add(c,s,v.id);}
const rows=I.bases.map(c=>{const b=results.find(r=>r.profile===c.id&&r.scenario==="BASE"),f=results.find(r=>r.profile===c.id&&r.scenario==="FLAT"),n=results.find(r=>r.profile===c.id&&r.scenario==="RENEWAL_FLAT"),j=results.find(r=>r.profile===c.id&&r.scenario==="J3_COMPLETED");const zero=runCase({...c,rent:0},{},I),one=runCase({...c,rent:1},{},I);const rentNeutral=-zero.annual_mean_cash/(one.annual_mean_cash-zero.annual_mean_cash);
assert(Math.abs(runCase({...c,rent:rentNeutral},{},I).annual_mean_cash)<1e-5,c.id+":neutral-rent-root");
return{id:c.id,name:c.name,price:c.price,rent:c.rent,fee:c.fee,monthly_payment:b.payment,narrow_monthly:b.standard_monthly_balance,annual_cash:b.annual_mean_cash,annual_neutral_rent:rentNeutral,gross_yield:b.gross_yield,flat_profit:f.profit,target_profit:b.profit,target_exit:b.exit_price,flat_exit_break_even:f.break_even_exit,peak_funding:b.peak_funding,renewal_flat_profit:n.profit,joint_stress_profit:j.profit,future_buyer:b.future_buyer};});
assert(results.length===I.bases.length*I.scenarios.length+I.variants.length*2,"scenario-count");
return{version:I.version,rows,results,validation:{checks:checks.length,all_passed:true,scope:"Arithmetic and accounting consistency only; no market fact validated."}};
}
const result=calculate(I,model);
if(JSON.stringify(result)!==JSON.stringify(expected))throw Error("Remote diagnostics differ");
process.stdout.write(JSON.stringify({reproduced:true,scenarios:result.results.length,checks:result.validation.checks,model_source:I.source_commit})+"\n");
