'use strict';
const assert=require('node:assert/strict');
const pay=(l,r,y)=>r?l*r/12/(1-(1+r/12)**(-y*12)):l/(y*12);
function costs(p,t){const agent=p*.03,legal=Math.max(500,p*.0125),discharge=400,filing=500;return{agent,legal,discharge,filing,tax:(agent+legal+discharge+filing)*t,total:(agent+legal+discharge+filing)*(1+t)};}
function leases(h,initial,gap,renew){let a=[],s=initial+1,k=0;while(s<=h){a.push({start:s,end:Math.min(h,s+11),commission:k===0||!renew?1:.5});s+=12+(renew?0:gap);k++;}return a;}
function irr(cf){
 const first=cf.findIndex(x=>x!==0);if(first<0||!cf.some(x=>x>0)||!cf.some(x=>x<0))return [];
 const c=cf.slice(first),npv=x=>c.reduce((a,v,t)=>a+v*Math.exp(-x*t/12),0),roots=[];
 let lastX=Math.log(.001),lastV=npv(lastX);
 for(let k=1;k<=800;k++){const x=Math.log(.001)+(Math.log(1001)-Math.log(.001))*k/800,v=npv(x);
 if(v*lastV<0){let lo=lastX,hi=x,vl=lastV;for(let j=0;j<80;j++){const m=(lo+hi)/2,vm=npv(m);if(vm*vl>0){lo=m;vl=vm;}else hi=m;}roots.push(Math.exp((lo+hi)/2)-1);}
 lastX=x;lastV=v;}return roots;
}
function evaluate(i,spec={}){
 const s={id:'base',rent:i.rent,fee:i.fee,rate:i.rate,years:i.years,build:i.build,hold:i.hold,fitout:i.fitout,exit:i.nett*1.2,initial:1,gap:1,renew:false,feeGrowth:0,carry:false,firstDraw:false,arrears:false,...spec};
 assert.equal(i.loan,i.nett,'Case-specific net consideration/debt reconciliation');
 const p=pay(i.loan,s.rate,s.years),cal=leases(s.hold,s.initial,s.gap,s.renew);
 const proxy=i.loan*.5*(s.firstDraw?s.rate:i.rate)*s.build/12,construction=s.carry?proxy:0;
 // Uniform cash timing is an explicit proxy only; total equals 50%-average-draw construction estimate.
 const cf=[0,...Array(s.build).fill(-construction/s.build)];
 let bal=i.loan,cum=-construction,peak=construction,peakMonth=-s.build,interest=0,principal=0,rents=0,fees=0,repairs=0,commissions=0,op=0;
 const ledger=[];
 for(let m=1;m<=s.hold;m++){
 const l=cal.find(x=>m>=x.start&&m<=x.end),defaulted=s.arrears&&(m===cal[0].end-1||m===cal[0].end);
 const rent=l&&!defaulted?s.rent:0,commission=l&&m===l.start?l.commission*s.rent*(1+i.tax):0;
 const fee=s.fee*(1+s.feeGrowth)**Math.max(0,Math.ceil(m/12)-2),repair=s.rent/24;
 const intr=bal*s.rate/12,princ=p-intr;bal-=princ;
 const operating=rent-commission-fee-repair-p,fit=m===1?s.fitout:0;
 cum+=operating-fit;cf.push(operating-fit);if(-cum>peak){peak=-cum;peakMonth=m;}
 interest+=intr;principal+=princ;rents+=rent;commissions+=commission;fees+=fee;repairs+=repair;op+=operating;
 ledger.push({month:m,rent,commission,fee,repair,instalment:p,interest:intr,principal:princ,balance:bal,fitout:fit,cumulativeCash:cum});
 }
 const selling=costs(s.exit,i.tax),exitCash=s.exit-selling.total-bal,profit=cum+exitCash;
 cf[cf.length-1]+=exitCash;
 const economic=s.exit-i.nett-selling.total-s.fitout-construction+rents-commissions-fees-repairs-interest;
 assert.ok(Math.abs(profit-economic)<1e-6,'profit conservation');
 assert.ok(Math.abs(principal+bal-i.loan)<1e-6,'debt conservation');
 const breakEvenExit=(bal-cum+900*(1+i.tax))/(1-.0425*(1+i.tax));
 return{id:s.id,scenario:s,payment:p,grossYield:s.rent*12/i.nett,netOperatingYield:(rents-commissions-fees-repairs)/(s.hold/12)/i.nett,
 narrowMonthly:s.rent-p-s.fee,paidMonths:s.rent?rents/s.rent:null,leaseStarts:cal.map(x=>x.start),commissionRentMonths:cal.reduce((a,x)=>a+x.commission,0),
 constructionInterestProxy:proxy,buyerConstructionCash:construction,totalCalendarMonths:s.build+s.hold,
 receipts:rents,commissions,fees,repairs,debtService:p*s.hold,interest,principal,closingDebt:bal,operatingCash:op,annualOperatingCash:op/(s.hold/12),
 cumulativePreSale:cum,peakPreSale:peak,peakOperatingMonth:peakMonth,peakIncludingClosing:Math.max(peak,-profit),
 sale:s.exit,sellingCosts:selling,netExitCash:exitCash,closingTopUp:Math.max(0,-exitCash),profitBeforeUAndPersonalTaxes:profit,breakEvenExit,
 conditionalAnnualMoneyWeightedRoots:irr(cf),ledger};
}
function run(i){
 const results=[],add=x=>results.push(evaluate(i,x));
 for(const rent of[1400,1600,1800])for(const fee of[100,150,200])for(const mult of[1,1.2])add({id:'grid-'+rent+'-'+fee+'-'+mult,rent,fee,exit:i.nett*mult});
 const defs=[{id:'S1-up',rate:.0425},{id:'S1-down',rate:.0375},{id:'S2-31',years:31},{id:'S2-25',years:25},{id:'S4-delay',build:72},{id:'S7-rent',rent:i.rent*.8},{id:'S8-once',initial:2},{id:'S8-persistent',initial:2,gap:2},{id:'S12-fee',feeGrowth:.05},{id:'S15-fitout',fitout:i.fitout+10000},{id:'S16-minus10',exit:i.nett*.9},{id:'S16-plus10',exit:i.nett*1.1},{id:'S17-delay',hold:66},{id:'S24-arrears',arrears:true},{id:'J1',build:72,fitout:i.fitout+10000,rate:.0425,feeGrowth:.05},{id:'J2',rent:i.rent*.8,initial:2,exit:i.nett*.9,hold:66},{id:'J3',build:72,fitout:i.fitout+10000,rate:.0425,feeGrowth:.05,rent:i.rent*.8,initial:2,exit:i.nett*.9,hold:66},{id:'renewal-flat',renew:true,exit:i.nett},{id:'year3-target',hold:36,exit:i.nett*1.1}];
 defs.forEach(add);
 for(const x of[{id:'carry-flat',exit:i.nett},{id:'carry-target'},...defs.filter(x=>['S1-up','S4-delay','J1','J2','J3'].includes(x.id)).map(x=>({...x,id:'carry-'+x.id})),{id:'carry-S1-firstdraw',rate:.0425,firstDraw:true}])add({...x,carry:true});
 const buyer=[.9,1,1.1,1.2].map(mult=>{const price=i.nett*mult;return{price,loan:price*.85,equity:price*.15,payment:pay(price*.85,.045,30),rentAtSixPercent:price*.06/12,equityWithTenPercentValuationShortfall:price*(1-.85*.9)};});
 return{case:i.case,scenarioCount:results.length,buyer,results};
}
function verify(i,o){
 let count=0;const near=(a,b,m)=>{assert.ok(Math.abs(a-b)<1e-6,m);count++;},yes=(a,m)=>{assert.ok(a,m);count++;};
 const get=id=>o.results.find(x=>x.id===id),b=get('grid-1600-150-1.2');
 near(b.payment,1133.5033370452747,'instalment');
 near(b.closingDebt,i.loan*(1+i.rate/12)**60-b.payment*((1+i.rate/12)**60-1)/(i.rate/12),'closed form debt');
 near(b.paidMonths,55,'base receipts');near(b.commissionRentMonths,5,'base commission');
 yes(JSON.stringify(b.leaseStarts)==='[2,15,28,41,54]','lease events');
 near(b.operatingCash,47.1*1600-60*150-60*b.payment,'independent cash formula');
 near(get('renewal-flat').paidMonths,59,'renewal receipts');near(get('renewal-flat').commissionRentMonths,3,'renewals');
 near(get('S8-once').ledger.slice(0,12).filter(x=>x.rent>0).length,10,'crisis receipt definition');
 near(get('S24-arrears').receipts,b.receipts-3200,'arrears not duplicate void');near(get('S17-delay').paidMonths,60,'extended hold');
 near(get('carry-flat').buyerConstructionCash,25600,'construction carry');near(get('carry-S4-delay').buyerConstructionCash,30720,'delay carry');
 near(get('carry-S1-firstdraw').buyerConstructionCash,27200,'firstdraw rate');
 near(get('carry-flat').profitBeforeUAndPersonalTaxes,get('grid-1600-150-1').profitBeforeUAndPersonalTaxes-25600,'carry bridge');
 near(get('J3').peakIncludingClosing,-get('J3').profitBeforeUAndPersonalTaxes,'closing funding');yes(!get('J3').scenario.arrears,'no extra joint stress');
 for(const x of o.results){yes(Number.isFinite(x.profitBeforeUAndPersonalTaxes),'finite result');near(x.principal+x.closingDebt,i.loan,'debt balance');
 const breakdown=x.buyerConstructionCash+x.ledger.slice(0,Math.max(0,x.peakOperatingMonth)).reduce((a,r)=>a+r.instalment+r.fee+r.repair+r.commission+r.fitout-r.rent,0);near(x.peakPreSale,breakdown,'peak funding breakdown');
 yes(x.conditionalAnnualMoneyWeightedRoots.every(Number.isFinite),'finite reported IRR roots; absent root explicitly retained');
 const flows=[0,...Array(x.scenario.build).fill(-x.buyerConstructionCash/x.scenario.build),...x.ledger.map(r=>r.rent-r.commission-r.fee-r.repair-r.instalment-r.fitout)];flows[flows.length-1]+=x.netExitCash;
 for(const root of x.conditionalAnnualMoneyWeightedRoots){const value=flows.reduce((a,c,t)=>a+c/((1+root)**(t/12)),0);yes(Math.abs(value)<.01,'IRR residual');}}
 return{status:'PASS',checks:count,scenarioCount:o.scenarioCount,scope:'Arithmetic and cash conservation, not market/lender/rights/subsidy validation'};
}
module.exports={pay,costs,leases,evaluate,run,verify};
