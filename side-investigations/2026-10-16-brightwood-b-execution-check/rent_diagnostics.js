"use strict";
const api=require("../2026-10-16-brightwood-stress-replay/financial_model");
const cfg=require("../2026-10-16-brightwood-stress-replay/Inputs.json");
function replay(){
 const t=cfg.types.find(t=>t.id==="B"),cases=[];
 for(const rents of [[1200,2000],[1050,2000],[1200,1800],[1050,1800],[1000,1800],[1200,2200]])
 for(const mode of cfg.cost_modes){
  const r=api.evaluate({...t,rents},{id:"B_"+rents.join("_")},cfg,mode);
  cases.push({rents,mode,total:r.monthly_rent,annual_cash:r.annual[0].operating_cash,profit:r.profit_before_unpriced_costs,irr:r.annual_irr_reference.annual});
 }
 let checks=0;const assert=x=>{if(!x)throw Error("Diagnostic validation failed");checks++;};
 for(const row of cases){
  assert(Math.abs(row.annual_cash-(row.total*9.42-12*t.area*.35-12*api.payment(t.net,.04,420)))<.01);
  const base=cases.find(x=>x.total===3200&&x.mode===row.mode);
  assert(Math.abs(row.profit-base.profit-(row.total-3200)*47.1)<.01);
 }
 const d=api.evaluate(cfg.types.find(x=>x.id==="D"),{id:"BASE"},cfg,"self_paid_reference");
 const b=cases.find(x=>x.total===3200&&x.mode==="self_paid_reference");
 const rankRoot=3200-(b.profit-d.profit_before_unpriced_costs)/47.1;
 const check=api.evaluate({...t,rents:[1200,rankRoot-1200]},{id:"root"},cfg,"self_paid_reference");
 assert(Math.abs(check.profit_before_unpriced_costs-d.profit_before_unpriced_costs)<.01);
 const cashRoot=(12*api.payment(t.net,.04,420)+12*t.area*.35)/9.42;
 assert(Math.abs(cashRoot*9.42-12*t.area*.35-12*api.payment(t.net,.04,420))<.01);
 return {cases,B_total_rent_equal_D_profit:rankRoot,B_total_rent_zero_annual:cashRoot,checks,passed:checks};
}
if(require.main===module)console.log(JSON.stringify(replay(),null,2));
module.exports={replay};

