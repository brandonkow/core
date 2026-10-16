"use strict";
// Read-only reproduction: node reproduce.cjs > results.json (redirection optional).
// No network and no filesystem writes from the script itself.
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto");
const A=require("./financial_model.cjs"),{validate}=require("./validate.cjs");
const I=JSON.parse(fs.readFileSync(path.join(__dirname,"Inputs.json"),"utf8"));
const root=path.resolve(__dirname,"../../..");
for(const [p,expected] of Object.entries(I.source_blobs)){
 const data=fs.readFileSync(path.join(root,p)),actual=crypto.createHash("sha1").update(Buffer.from("blob "+data.length+"\0")).update(data).digest("hex");
 if(actual!==expected)throw Error("Source drift: "+p);
}
const O=A.replay(I),validation=validate(I,O,A);
const files=fs.readdirSync(__dirname).filter(p=>/^B\d\d_Results\.json$/.test(p));
let savedCount=0,numeric=0;
function equal(a,b,p){
 if(typeof a==="number"){numeric++;if(Math.abs(a-b)>1e-6)throw Error("Mismatch "+p);}
 else if(Array.isArray(a)){if(a.length!==b.length)throw Error("Length "+p);a.forEach((x,i)=>equal(x,b[i],p+"/"+i));}
 else if(a&&typeof a==="object")Object.keys(a).forEach(k=>equal(a[k],b[k],p+"/"+k));
 else if(a!==b)throw Error("Mismatch "+p);
}
for(const f of files)for(const row of JSON.parse(fs.readFileSync(path.join(__dirname,f),"utf8")).results){
 equal(row,O.results.find(x=>x.case_id===row.case_id&&x.scenario===row.scenario),row.case_id+"/"+row.scenario);savedCount++;
}
const held=JSON.parse(fs.readFileSync(path.join(__dirname,"Held_Alternatives.json"),"utf8")).alternatives;
for(const row of held)equal(row,O.alternatives.find(x=>x.case_id===row.case_id&&x.scenario===row.scenario),row.case_id+"/"+row.scenario);
if(savedCount!==3312||held.length!==18)throw Error("Saved result coverage");
const summary=JSON.parse(fs.readFileSync(path.join(__dirname,"Summary.json"),"utf8"));
const bases=O.results.filter(x=>x.scenario==="BASE");
if(bases.filter(x=>x.annual_mean_cash>=0).length!==summary.counts.new_annual_nonnegative||
 bases.filter(x=>x.standard_monthly_balance>=0).length!==summary.counts.new_narrow_nonnegative||
 bases.filter(x=>x.profit>=0).length!==summary.counts.target_profit_nonnegative)throw Error("Summary counts");
process.stdout.write(JSON.stringify({validation,saved_results_compared:savedCount+held.length,numeric_comparisons:numeric,counts:summary.counts},null,2)+"\n");
