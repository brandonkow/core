const cp=require('node:child_process'),vm=require('node:vm'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const ref='8854a90564a9ff6d677c99c2ea3e4d777c590626',base='klang-valley-2026-10-07/round-3/sop-v2-all-base-replay-2026-10-16/';
function read(p){const r=JSON.parse(cp.execFileSync('gh',['api','repos/brandonkow/core/contents/'+p+'?ref='+ref],{encoding:'utf8',maxBuffer:3e6}));return Buffer.from(r.content,'base64').toString('utf8');}
const modelText=read(base+'financial_model.cjs'),box={module:{exports:{}}};vm.runInNewContext(modelText,box);const model=box.module.exports;
const I=JSON.parse(read(base+'Inputs.json')),summary=JSON.parse(read(base+'Summary.json')),c=I.bases.find(x=>x.id==='R315');
let checks=0;function near(a,b){assert(Math.abs(a-b)<1e-6);checks++;}
const old=model.runCase(c,{},I),sr=summary.rows.find(x=>x.id==='R315');near(old.annual_mean_cash,sr.annual);near(old.profit,sr.target_profit);
const results=[];
for(const price of [700000,780000])for(const rent of [3500,3800]){
 for(const spec of [{id:'BASE_TARGET20'},{id:'FLAT',exit:1},{id:'RENEWAL_TARGET20',renew:true},{id:'S15_PLUS_10K',fitout_extra:10000},{id:'S12_FEE_GROWTH',fee_growth:.05},...(price===780000&&rent===3800?[{id:'TURNKEY_ZERO_ADDITIONAL_FITOUT_TARGET20',fitout:0},{id:'TURNKEY_ZERO_ADDITIONAL_FITOUT_FLAT',fitout:0,exit:1}]:[])]){
  const r=model.runCase({...c,price,rent},spec,I);near(r.profit,r.economic_profit_check);near(r.peak_funding,Object.values(r.peak_breakdown).reduce((a,b)=>a+b,0));
  if(!spec.renew&&!spec.fee_growth)near(r.annual_mean_cash,9.42*rent-12*c.fee-12*r.payment);
  const {g0,g9,ledger,...financial}=r;results.push(financial);
 }
}
const unitPmt=model.pmt(.9,.04,35),thresholds=[3500,3800].map(rent=>({rent,annual_neutral_entry:(9.42*rent-12*c.fee)/(12*unitPmt),gross6_entry:12*rent/.06}));
const result={version:'PINES-COHORT-2026-10-18',source_commit:ref,financial_model_sha256:crypto.createHash('sha256').update(modelText).digest('hex'),scope:'22 conditional diagnostics, not gate admission or a full fresh stress release. Price/rent advertisements are not matched executable unit packages. Fee450 and 5 percent fitout remain assumptions. No cost or rent calibration.',checks,thresholds,results};
console.log(JSON.stringify(result));