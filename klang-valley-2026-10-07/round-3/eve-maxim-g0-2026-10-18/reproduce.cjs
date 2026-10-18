const cp=require('node:child_process'),vm=require('node:vm'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const ref='05a2bcf78cdf993467824675ad8108368f07aa99',base='klang-valley-2026-10-07/round-3/sop-v2-all-base-replay-2026-10-16/';
function read(p){const r=JSON.parse(cp.execFileSync('gh',['api','repos/brandonkow/core/contents/'+p+'?ref='+ref],{encoding:'utf8',maxBuffer:3e6}));return Buffer.from(r.content,'base64').toString('utf8');}
const modelText=read(base+'financial_model.cjs'),box={module:{exports:{}}};vm.runInNewContext(modelText,box);const model=box.module.exports;
const I=JSON.parse(read(base+'Inputs.json')),summary=JSON.parse(read(base+'Summary.json'));
let checks=0; const near=(a,b)=>{assert(Math.abs(a-b)<1e-6);checks++;}; const results=[];
for(const id of ['R306','KV01']){
 const original=I.bases.find(c=>c.id===id),old=model.runCase(original,{},I);
 const sr=summary.rows.find(c=>c.id===id);near(old.annual_mean_cash,sr.annual);near(old.profit,sr.target_profit);
 const price=id==='R306'?370000:380000, refs=id==='R306'?[350000,375000,405000]:[350000,400000,440000],c={...original,price};
 for(const s of [{id:'TARGET20'},{id:'FLAT',exit:1},...refs.map(e=>({id:'FIXED_'+e,exit:e/price})),{id:'RENEWAL',renew:true}]){
  const r=model.runCase(c,s,I);
  near(r.profit,r.economic_profit_check);near(r.peak_funding,Object.values(r.peak_breakdown).reduce((a,b)=>a+b,0));
  if(!s.renew){near(r.paid_months,55);near(r.new_leases,5);near(r.annual_mean_cash,9.42*c.rent-12*c.fee-12*r.payment);}
  const {g0,g9,ledger,...financial}=r;results.push(financial);
 }
}
console.log(JSON.stringify({version:'EVE-MAXIM-G0-2026-10-18',source_commit:ref,financial_model_sha256:crypto.createHash('sha256').update(modelText).digest('hex'),scope:'12 conditional scenarios; current advertised Eve370k and Maxim380k; rents/fees and itemised cost references retained, not newly authenticated. Fixed exits are persistence sensitivities, not forecasts. Legacy model g0/g9 labels are excluded: evidence adjudication is separate.',checks,results}));
