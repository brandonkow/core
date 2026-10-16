"use strict";
function payment(p,r,n){if(p<0||r<0||n<=0)throw Error("Invalid debt");const m=r/12;return m===0?p/n:p*m/(1-Math.pow(1+m,-n));}
function scale(p){return Math.max(500,.0125*Math.min(p,500000)+.01*Math.max(0,p-500000));}
function hda(p){return p<=50000?500:scale(p)*(p<=250000?.75:p<=500000?.7:p<=1000000?.65:.5);}
function transferDuty(p){return Math.ceil(Math.min(p,100000)/100)*1+Math.ceil(Math.max(0,Math.min(p-100000,400000))/100)*2+Math.ceil(Math.max(0,Math.min(p-500000,500000))/100)*3+Math.ceil(Math.max(0,p-1000000)/100)*4;}
function loanDuty(p){return Math.ceil(p/1000)*5;}
function acqCosts(t,loan,mode,sst){
 const legal=hda(t.gross)+hda(loan);
 return {mot:transferDuty(t.gross),loan_stamp:loanDuty(loan),purchase_legal:hda(t.gross),loan_legal:hda(loan),legal_paid:mode==="self_paid_reference"?legal:0,legal_sst:mode==="self_paid_reference"?legal*sst:0,total:transferDuty(t.gross)+loanDuty(loan)+(mode==="self_paid_reference"?legal*(1+sst):0)};
}
function exitCosts(price,f,sst){const agency=price*f.agent_sale_fraction,legal=scale(price),fixed=f.discharge_reference+f.ckht1a_reference;return {agency,legal,discharge:f.discharge_reference,ckht1a:f.ckht1a_reference,sst:(agency+legal+fixed)*sst,total:(agency+legal+fixed)*(1+sst)};}
function leaseEvents(hold,b,s){
 const arr=Array.from({length:hold},(_,i)=>({month:i+1,paid:false,newLease:false,renewal:false}));
 let start=(s.initial_void_months??b.initial_void_months)+1; let first=true;
 while(start<=hold){
  arr[start-1].newLease=first||!s.renew;arr[start-1].renewal=!first&&!!s.renew;
  for(let m=start;m<start+b.lease_months&&m<=hold;m++)arr[m-1].paid=true;
  start+=b.lease_months+(s.renew?0:(s.turnover_void_months??b.turnover_void_months));first=false;
 }
 return arr;
}
function irrMonthly(flows){
 const npv=r=>flows.reduce((sum,x,i)=>sum+x/Math.pow(1+r,i),0);
 const grid=[-.5,-.25,-.1,-.05,-.02,-.01,-.005,0,.002,.005,.01,.02,.05,.1,.25,.5,1];
 const intervals=[];for(let i=0;i<grid.length-1;i++){let fa=npv(grid[i]),fb=npv(grid[i+1]);if(fa===0)return {annual:Math.pow(1+grid[i],12)-1,root_count:1};if(fa*fb<0)intervals.push([grid[i],grid[i+1]]);}
 if(intervals.length!==1)return {annual:null,root_count:intervals.length};
 let [a,z]=intervals[0];for(let i=0;i<100;i++){let m=(a+z)/2;if(npv(a)*npv(m)<=0)z=m;else a=m;}
 return {annual:Math.pow(1+(a+z)/2,12)-1,root_count:1};
}
function evaluate(t,s,cfg,mode){
 const b=cfg.base,f=cfg.fees,sst=s.service_tax??f.service_tax;
 const build=s.build_months??b.build_months,hold=s.hold_months??b.hold_months,term=s.term_years??b.term_years;
 const loan=b.ltv_gross*t.gross, equity=Math.max(0,t.net-loan), acq=acqCosts(t,loan,mode,sst);
 const fitout=t.net*b.fitout_fraction_net+(s.fitout_extra??0);
 const rent=(s.whole_unit?[t.fallback]:t.rents).map(r=>r*(s.rent_multiplier??1));
 if(rent.some(x=>x==null))throw Error("No fallback");
 const monthlyRent=rent.reduce((a,b)=>a+b,0),fee0=t.area*b.fee_psf,feeGrowth=s.fee_growth??b.fee_growth;
 const constructionRate=s.construction_rate??b.rate;
 const ledger=[{month:0,phase:"entry",cash:-equity-acq.total}];const flows=[ledger[0].cash];
 let ci=0;for(let m=1;m<=build;m++){const drawFraction=(m-.5)/build;const interest=loan*drawFraction*constructionRate/12;ci+=interest;ledger.push({month:m,phase:"construction",interest,drawn_balance:loan*drawFraction,cash:-interest});flows.push(-interest);}
 let debt=loan,opCash=0,opInterest=0,principalPaid=0,noi=0,rentCollected=0,commissionTotal=0,feeTotal=0,repairsTotal=0,arrearsTotal=0;
 const leases=leaseEvents(hold,b,s),annual=[],ops=[];
 let lastRate=null,pay=0;
 for(let m=1;m<=hold;m++){
  const ev=leases[m-1],year=Math.floor((m-1)/12)+1;
  const rate=s.rate_after!==undefined&&m>=(s.rate_change_op_month??1)?s.rate_after:b.rate;
  if(rate!==lastRate){pay=payment(debt,rate,term*12-m+1);lastRate=rate;}
  let collected=0,arrears=0;
  rent.forEach((r,j)=>{if(ev.paid){if((s.arrears_stream===j||s.arrears_stream==="all")&&(m===12||m===13))arrears+=r;else collected+=r;}});
  const commMonths=ev.newLease?b.new_lease_commission_months:ev.renewal?b.renewal_commission_months:0;
  const commission=monthlyRent*commMonths,commissionTax=commission*sst;
  const fee=fee0*Math.pow(1+feeGrowth,Math.max(0,year-2));
  const repair=monthlyRent*b.repair_rent_months_year/12;
  const interest=debt*rate/12,principal=pay-interest;debt-=principal;
  const netOp=collected-fee-repair-commission-commissionTax;
  const cash=netOp-pay;const fitoutCash=m===1?fitout:0;
  const row={month:build+m,operating_month:m,phase:"operation",scheduled_paid:ev.paid,new_lease:ev.newLease,renewal:ev.renewal,collected,arrears,commission,commission_tax:commissionTax,fee,repair,interest,principal,debt,payment:pay,operating_cash:cash,fitout:fitoutCash,cash:cash-fitoutCash};
  ledger.push(row);flows.push(row.cash);ops.push(row);
  opCash+=cash;opInterest+=interest;principalPaid+=principal;noi+=netOp;rentCollected+=collected;commissionTotal+=commission+commissionTax;feeTotal+=fee;repairsTotal+=repair;arrearsTotal+=arrears;
  if(!annual[year-1])annual[year-1]={year,months:0,collected:0,commission_incl_sst:0,fee:0,repairs:0,debt_service:0,operating_cash:0};
  const y=annual[year-1];y.months++;y.collected+=collected;y.commission_incl_sst+=commission+commissionTax;y.fee+=fee;y.repairs+=repair;y.debt_service+=pay;y.operating_cash+=cash;
 }
 const exitMultiple=s.exit_multiplier??b.exit_multiplier,price=t.net*exitMultiple,cost=exitCosts(price,f,sst),netExit=price-cost.total-debt;
 let cumulative=0,min=0;for(const cf of flows){cumulative+=cf;min=Math.min(min,cumulative);}
 const totalBeforeExit=cumulative;
 flows[flows.length-1]+=netExit;ledger[ledger.length-1].sale_price=price;ledger[ledger.length-1].sale_cost=cost.total;ledger[ledger.length-1].debt_redemption=debt;ledger[ledger.length-1].exit_cash=netExit;
 const profit=flows.reduce((a,b)=>a+b,0);
 const economic=price-t.net-cost.total-acq.total-fitout-ci-opInterest+noi;
 if(Math.abs(profit-economic)>.001||Math.abs(principalPaid+debt-loan)>.001)throw Error("Conservation "+s.id);
 const proceedsNeeded=debt-totalBeforeExit;
 let lo=0,hi=t.net*4;for(let n=0;n<90;n++){const mid=(lo+hi)/2;if(mid-exitCosts(mid,f,sst).total<proceedsNeeded)lo=mid;else hi=mid;}
 const breakeven=(lo+hi)/2;
 const stdPay=payment(loan,b.rate,b.term_years*12);
 const futureLoan=.85*price,futureHaircutLoan=.85*.9*price;
 return {type:t.id,scenario:s.id,label:s.label,cost_mode:mode,build_months:build,hold_months:hold,term_years:term,monthly_rent:monthlyRent,rent_streams:rent,first_payment:ops[0].payment,normal_month_cover_before_full_costs:monthlyRent-ops[0].payment-fee0,gross_yield:12*monthlyRent/t.net,acquisition:acq,fitout,construction_interest:ci,rent_collected:rentCollected,commission_total:commissionTotal,fee_total:feeTotal,repairs_total:repairsTotal,arrears_gross_loss:arrearsTotal,operating_cash:opCash,annual,operating_interest:opInterest,principal_repaid:principalPaid,exit_debt:debt,exit_price:price,exit_cost:cost,net_exit_cash:netExit,profit_before_unpriced_costs:profit,additional_unpriced_total_cost_room:profit,peak_funding_before_sale:-min,peak_funding_including_exit:Math.max(-min,-profit),additional_cash_to_close_sale:Math.max(0,-netExit),break_even_exit_before_unpriced_costs:breakeven,annual_irr_reference:irrMonthly(flows),total_cash_injected:flows.filter(x=>x<0).reduce((a,b)=>a-b,0),future_buyer:{loan:futureLoan,equity:price-futureLoan,payment:payment(futureLoan,.045,360),loan_after10pct_valuation_haircut:futureHaircutLoan,equity_after_haircut:price-futureHaircutLoan,payment_after_haircut:payment(futureHaircutLoan,.045,360)},exit_gross_yield:12*monthlyRent/price,price_at6pct_gross:12*monthlyRent/.06,ledger};
}
function run(cfg){
 const rows=[];for(const t of cfg.types)for(const s of cfg.scenarios){if(s.only&&s.only!==t.id)continue;for(const mode of cfg.cost_modes)rows.push(evaluate(t,s,cfg,mode));}
 return {release:cfg.release,results:rows};
}
if(typeof module!=="undefined")module.exports={run,evaluate,payment,leaseEvents,scale,hda,transferDuty,loanDuty};

