"use strict";
function pmt(L,r,y){const m=r/12;return m===0?L/(12*y):L*m/(1-Math.pow(1+m,-12*y));}
function legal(x){if(x>7500000)throw Error("Unpriced negotiated legal band");return Math.max(500,Math.min(x,500000)*.0125+Math.max(0,x-500000)*.01);}
function duty(x){if(x>1000000)throw Error("This scoped stamp reference is limited to <=RM1m");return Math.ceil(Math.min(x,100000)/1000)*10+Math.ceil(Math.min(Math.max(0,x-100000),400000)/1000)*20+Math.ceil(Math.max(0,x-500000)/1000)*30;}
function sum(a){return a.reduce((x,y)=>x+y,0);}
function entryCost(P,L,tax){const f={transfer_duty:duty(P),loan_duty:Math.ceil((L-1e-8)/1000)*5,spa_legal:legal(P),loan_legal:legal(L)};f.invoice_tax=(f.spa_legal+f.loan_legal)*tax;f.total=sum(Object.values(f));return f;}
function exitCost(S,tax,ref){const f={agency:.03*S,legal:legal(S),discharge_reference:ref.discharge,ckht_reference:ref.ckht1a};f.invoice_tax=sum(Object.values(f))*tax;f.total=sum(Object.values(f));return f;}
function irr(cash){const n=cash.length;function pv(r){return sum(cash.map((x,i)=>x/Math.pow(1+r,i)));}const grid=[-.5,-.2,-.1,-.05,-.02,-.01,0,.005,.01,.02,.05,.1,.2,.5,1,2,5];let brackets=[];for(let i=1;i<grid.length;i++){if(pv(grid[i-1])*pv(grid[i])<=0)brackets.push([grid[i-1],grid[i]]);}if(brackets.length!==1)return null;let [a,b]=brackets[0];for(let i=0;i<90;i++){let m=(a+b)/2;if(pv(a)*pv(m)<=0)b=m;else a=m;}return Math.pow(1+(a+b)/2,12)-1;}
function runCase(c,s,I,includeLedger=false){
 const cfg=I.sop,ref=I.fee_reference,P=c.price,R=c.rent*(s.rent_factor??1),F=c.fee,H=s.hold??cfg.base.hold_months_from_handover,rate=s.rate??cfg.standard.annual_rate,term=s.term??cfg.standard.amortisation_years,tax=s.tax??ref.service_tax;
 const L=P*cfg.standard.ltv,acq=entryCost(P,L,tax),fit=(s.fitout??c.fitout_override??P*cfg.base.fitout_fraction_nett)+(s.fitout_extra??0),down=P-L,pay=pmt(L,rate,term);
 let debt=L,cumulative=-(down+acq.total+fit),peak=-cumulative,peakMonth=0,next=(s.initial_void??cfg.base.initial_void_months)+1,leaseEnd=0;
 const ledger=[],cash=[cumulative],years=Array(Math.ceil(H/12)).fill(0);let receipts=0,fees=0,repairs=0,commission=0,interest=0,payments=0,paid=0,starts=0,renewals=0;const S=P*(s.exit??cfg.targets.year5_nett_multiplier);
 for(let m=1;m<=H;m++){
   let commissionMonth=0;
   if(m===next){const renewal=!!s.renew&&starts>0;commissionMonth=renewal?cfg.base.renewal_commission_rent_months:cfg.base.new_tenant_commission_rent_months;if(renewal)renewals++;else starts++;leaseEnd=m+cfg.base.lease_months-1;next=leaseEnd+1+(s.renew?0:(s.turnover_void??cfg.base.turnover_void_months));}
   let rec=m<=leaseEnd&&m>=((s.initial_void??cfg.base.initial_void_months)+1)?R:0;
   // Near-expiry arrears example; month14 is already baseline void, replacement starts15.
   if(s.arrears&&[12,13].includes(m))rec=0;
   const charge=F*Math.pow(1+(s.fee_growth??0),Math.max(0,Math.floor((m-1)/12)-1));
   const repair=cfg.base.annual_repairs_rent_months*R/12,comm=commissionMonth*R*(1+tax),int=debt*rate/12;
   debt-=pay-int;const flow=rec-pay-charge-repair-comm;
   cumulative+=flow;if(-cumulative>peak){peak=-cumulative;peakMonth=m;}
   receipts+=rec;fees+=charge;repairs+=repair;commission+=comm;interest+=int;payments+=pay;if(rec>0)paid++;
   years[Math.floor((m-1)/12)]+=flow;cash.push(flow);
   ledger.push({month:m,receipt:rec,payment:pay,interest:int,principal:pay-int,fee:charge,repair_provision:repair,commission_with_tax:comm,net_cash:flow,cumulative_cash:cumulative,closing_debt:debt});
 }
 const selling=exitCost(S,tax,ref),netSale=S-selling.total-debt,op=sum(years),profit=cumulative+netSale;cash[cash.length-1]+=netSale;
 let lo=P*.1,hi=P*1.4;
 for(let i=0;i<70;i++){const mid=(lo+hi)/2;const v=cumulative+mid-exitCost(mid,tax,ref).total-debt;if(v>0)hi=mid;else lo=mid;}
 const economic=S-P-acq.total-fit+receipts-fees-repairs-commission-interest-selling.total;
 const ncf=ledger.slice(0,peakMonth);const peakBreakdown={downpayment:down,acquisition:acq.total,fitout:fit,loan_payments:sum(ncf.map(x=>x.payment)),fees:sum(ncf.map(x=>x.fee)),repairs:sum(ncf.map(x=>x.repair_provision)),commissions:sum(ncf.map(x=>x.commission_with_tax)),rent_offset:-sum(ncf.map(x=>x.receipt))};
 const futureLoan=S*cfg.stress.S19.future_buyer_ltv,futureHaircutLoan=S*(1-cfg.stress.S3.resale_valuation_haircut)*cfg.stress.S19.future_buyer_ltv;
 return {case_id:c.id,name:c.name,scenario:s.id??"BASE",price:P,rent:R,fee:F,fitout:fit,loan:L,payment:pay,standard_monthly_balance:R-pmt(L,cfg.standard.annual_rate,cfg.standard.amortisation_years)-F,gross_yield:12*R/P,net_operating_yield:(receipts-fees-repairs-commission)/(P*(H/12)),hold_months:H,paid_months:paid,new_leases:starts,renewals,annual_cash:years,annual_mean_cash:op/(H/12),operating_cash:op,acquisition:acq,downpayment:down,initial_cash:down+acq.total+fit,peak_funding:peak,peak_month:peakMonth,peak_breakdown:peakBreakdown,receipts,fees,repairs,commissions:commission,payments,interest,closing_debt:debt,exit_price:S,selling,net_sale_cash:netSale,profit,annual_irr:irr(cash),break_even_exit:(lo+hi)/2,economic_profit_check:economic,future_buyer:{loan:futureLoan,cash_equity:S-futureLoan,payment:pmt(futureLoan,.045,30),valuation_haircut_loan:futureHaircutLoan,valuation_haircut_equity:S-futureHaircutLoan,valuation_haircut_payment:pmt(futureHaircutLoan,.045,30),yield6_price:12*R/.06},g0:"STOP",g9:"Defer",...(includeLedger?{ledger}:{})};
}
function replay(I){
 const tests=[{id:"BASE"},{id:"S1_up",rate:.0425},{id:"S1_down",rate:.0375},{id:"S2_31",term:31},{id:"S2_25",term:25},{id:"S7",rent_factor:.8},{id:"S8_once",initial_void:2},{id:"S8_persistent",initial_void:2,turnover_void:2},{id:"S12",fee_growth:.05},{id:"S15",fitout_extra:10000},{id:"S16_minus",exit:.9},{id:"S16_plus",exit:1.1},{id:"S17",hold:66},{id:"S24",arrears:true},{id:"J1_completed",fitout_extra:10000,rate:.0425,fee_growth:.05},{id:"J2",rent_factor:.8,initial_void:2,exit:.9,hold:66},{id:"J3_completed",fitout_extra:10000,rate:.0425,fee_growth:.05,rent_factor:.8,initial_void:2,exit:.9,hold:66},{id:"FLAT",exit:1},{id:"YEAR3",hold:36,exit:1.1},{id:"RENEWAL",renew:true},{id:"NO_ADDITIONAL_INVOICE_TAX",tax:0}];
 const results=[];for(const c of I.bases){for(const s of tests)results.push(runCase(c,s,I,s.id==="BASE"));results.push(runCase(c,{id:"OLD_FITOUT_DIAGNOSTIC",fitout:c.old_fitout},I));}
 const alternatives=I.held_alternatives.map(c=>({...runCase(c,{id:c.label},I),held_status:c.status}));
 return {version:I.version,scenarios:tests,results,alternatives};
}
if(typeof module!=="undefined")module.exports={pmt,legal,duty,entryCost,exitCost,runCase,replay};
