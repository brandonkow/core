"use strict";
const api=require("../2026-10-16-brightwood-stress-replay/financial_model");
const cfg=require("../2026-10-16-brightwood-stress-replay/Inputs.json");
function replay(){
 const base=cfg.types.find(x=>x.id==="B"),rows=[];let checks=0;
 function check(ok){if(!ok)throw Error("Execution-brief check failed");checks++;}
 for(const t of cfg.types)for(const mode of cfg.cost_modes){
  const a=api.evaluate(t,{id:"BASE"},cfg,mode);
  const b=api.evaluate({...t,parking_bays:1},{id:"BASE"},cfg,mode);
  check(JSON.stringify(a)===JSON.stringify(b));
 }
 for(const gross of [555000,560000,565000,575000,600000,661125]){
  const t={...base,gross,net:.9*gross,parking_bays:1};
  for(const mode of cfg.cost_modes)for(const exitBasis of ["user_20pct_net","fixed_original_sale"]){
   const r=api.evaluate(t,{id:"PRICE_"+gross+"_"+exitBasis,exit_multiplier:exitBasis==="user_20pct_net"?1.2:599400/t.net},cfg,mode);
   const row={gross,net:t.net,mode,exitBasis,payment:r.first_payment,annual_cash:r.annual[0].operating_cash,fitout:r.fitout,construction_interest:r.construction_interest,acquisition:r.acquisition.total,exit_price:r.exit_price,profit:r.profit_before_unpriced_costs,annual_irr:r.annual_irr_reference.annual,peak_funding:r.peak_funding_before_sale};
   rows.push(row);
   check(Math.abs(row.annual_cash-(3200*9.42-12*736*.35-12*api.payment(.9*gross,.04,420)))<.01);
   check(Math.abs(row.construction_interest-.9*gross*.04*4*.5)<.01);
   check(Math.abs(row.fitout-row.net*.05)<.01);
  }
 }
 const annualNeutralGross=(3200*9.42-12*736*.35)/(12*.9*api.payment(1,.04,420));
 const r=api.evaluate({...base,gross:annualNeutralGross,net:annualNeutralGross*.9},{id:"root"},cfg,"self_paid_reference");
 check(Math.abs(r.annual[0].operating_cash)<.01);
 return {rows,annualNeutralGross,priceHeadroom:annualNeutralGross-555000,checks,passed:checks};
}
if(require.main===module)console.log(JSON.stringify(replay(),null,2));
module.exports={replay};

