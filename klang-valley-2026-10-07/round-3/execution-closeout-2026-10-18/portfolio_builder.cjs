"use strict";
function build(I,design,api){
 const sum=a=>a.reduce((x,y)=>x+y,0),cache=new Map();let checks=0;
 const check=(v,msg)=>{checks++;if(!v)throw Error(msg);};
 const close=(a,b,msg)=>check(Number.isFinite(a)&&Math.abs(a-b)<1e-6,msg);
 const all=I.bases;
 check(all.length===138,"base universe");check(new Set(all.map(x=>x.metadata.project_id)).size===122,"project coverage");
 for(const s of design.scenarios)for(const c of all){
   const cfg=s.valuation_factor===undefined?I:{...I,sop:{...I.sop,standard:{...I.sop.standard,ltv:I.sop.standard.ltv*s.valuation_factor}}};
   const r=api.runCase(c,s,cfg,true);
   if(s.valuation_factor!==undefined)close(r.loan,.81*c.price,"S3 debt basis");
   close(r.profit,r.economic_profit_check,"cash/economic parity");
   close(r.ledger[r.ledger.length-1].cumulative_cash,-r.initial_cash+r.operating_cash,"cash chain");
   check(r.g0==="STOP"&&r.g9==="Defer","no financial admission");
   cache.set(c.id+"|"+s.id,r);
 }
 function aggregate(ids,s){
   const rr=ids.map(id=>cache.get(id+"|"+s.id));
   const H=s.hold??60,initial=sum(rr.map(r=>r.initial_cash));
   let cumulative=-initial,peak=initial,peakMonth=0;const monthly=[];
   for(let i=0;i<H;i++){
     const flow=sum(rr.map(r=>r.ledger[i].net_cash));cumulative+=flow;
     if(-cumulative>peak){peak=-cumulative;peakMonth=i+1;}
     monthly.push({month:i+1,net_cash:flow,cumulative_before_sale:cumulative});
   }
   const netSale=sum(rr.map(r=>r.net_sale_cash)),profit=cumulative+netSale;
   close(profit,sum(rr.map(r=>r.profit)),"portfolio profit additive");
   check(peak+1e-7>=initial,"entry funding floor");
   check(peak<=sum(rr.map(r=>r.peak_funding))+1e-6,"synchronous peak upper bound");
   const P=sum(rr.map(r=>r.price)),loan=sum(rr.map(r=>r.loan));
   return {ids,scenario:s.id,hold_months:H,entry_price_total:P,initial_debt:loan,initial_cash:initial,
     annual_mean_cash:sum(rr.map(r=>r.annual_mean_cash)),peak_funding_before_sale:peak,peak_month:peakMonth,
     cumulative_before_sale:cumulative,net_sale_cash:netSale,profit,monthly,
     price_concentration:rr.map(r=>({id:r.case_id,weight:P?r.price/P:0})),
     personal_liquidity:null,protected_reserve:null,capacity_pass:null,g0:ids.length?"STOP":null,g9:ids.length?"Defer":null};
 }
 const portfolios=[];
 for(const b of design.baskets)for(const s of design.scenarios)portfolios.push({id:b.id,label:b.label,...aggregate(b.ids,s)});
 const quantile=(arr,p)=>{const a=[...arr].sort((x,y)=>x-y);const k=(a.length-1)*p,l=Math.floor(k);return a[l]+(a[Math.ceil(k)]-a[l])*(k-l);};
 const stats=a=>({min:Math.min(...a),q25:quantile(a,.25),median:quantile(a,.5),q75:quantile(a,.75),max:Math.max(...a)});
 let excluded=0,pairs=0;const projectPairs=new Set();
 for(let i=0;i<all.length;i++)for(let j=i+1;j<all.length;j++){
   if(all[i].metadata.project_id===all[j].metadata.project_id){excluded++;continue;}
   pairs++;projectPairs.add([all[i].metadata.project_id,all[j].metadata.project_id].sort().join("|"));
 }
 check(pairs===9436&&excluded===17&&projectPairs.size===7381,"pair identity");
 const pair_summary=[];
 for(const s of design.scenarios){
   const peak=[],profit=[];const groups=new Map();
   for(let i=0;i<all.length;i++)for(let j=i+1;j<all.length;j++){
     const a=all[i],b=all[j];if(a.metadata.project_id===b.metadata.project_id)continue;
     const r=aggregate([a.id,b.id],s);peak.push(r.peak_funding_before_sale);profit.push(r.profit);
     const key=[a.metadata.project_id,b.metadata.project_id].sort().join("|");
     const g=groups.get(key)||{low:Infinity,high:-Infinity,variants:0};
     g.low=Math.min(g.low,r.peak_funding_before_sale);g.high=Math.max(g.high,r.peak_funding_before_sale);g.variants++;groups.set(key,g);
   }
   pair_summary.push({scenario:s.id,expression_pairs:pairs,project_pair_groups:groups.size,
     peak_funding_stats:stats(peak),profit_stats:stats(profit),
     profit_nonnegative_diagnostic:profit.filter(x=>x>=0).length,
     project_pair_funding_spread_stats:stats([...groups.values()].map(x=>x.high-x.low)),
     personal_capacity_pass_count:null,admitted_portfolios:0});
 }
 for(const b of design.baskets){
   const x=portfolios.find(r=>r.id===b.id&&r.scenario==="BASE"),f=portfolios.find(r=>r.id===b.id&&r.scenario==="FLAT");
   close(x.peak_funding_before_sale,f.peak_funding_before_sale,"sale proceeds cannot fund pre-sale period");
   const j=portfolios.find(r=>r.id===b.id&&r.scenario==="J3_completed");
   check(j.peak_funding_before_sale+1e-6>=x.peak_funding_before_sale,"joint funding direction");
 }
 const terminal=all.map(c=>{
   const r=cache.get(c.id+"|BASE"),be=r.break_even_exit,L=.85*be,H=.85*.9*be;
   return {id:c.id,name:c.name,project_id:c.metadata.project_id,break_even_exit:be,
     gross_yield_at_break_even:12*c.rent/be,gross6_income_reference:12*c.rent/.06,
     future_buyer_equity_before_costs:be-L,future_buyer_payment:api.pmt(L,.045,30),
     haircut_buyer_equity_before_costs:be-H,haircut_buyer_payment:api.pmt(H,.045,30),
     target_sale:r.exit_price,target_future_buyer:r.future_buyer,g0:"STOP",g9:"Defer"};
 });
 return {version:"KV-CLOSEOUT-2026-10-18",checks,asset_path_evaluations:all.length*design.scenarios.length,
   portfolio_path_evaluations:portfolios.length,pair_path_aggregations:pairs*design.scenarios.length,
   excluded_same_project_pairs:excluded,project_pair_groups:projectPairs.size,portfolios,pair_summary,terminal};
}
if(typeof module!=="undefined")module.exports={build};
