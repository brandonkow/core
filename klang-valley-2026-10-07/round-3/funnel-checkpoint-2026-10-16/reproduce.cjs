"use strict";
const fs=require("fs"),path=require("path"),assert=require("assert");
const base=path.resolve(__dirname,"../sop-v2-all-base-replay-2026-10-16");
const I=JSON.parse(fs.readFileSync(path.join(base,"Inputs.json"),"utf8"));
const {runCase}=require(path.join(base,"financial_model.cjs"));
const c=I.bases.find(x=>x.id==="R208");
const saved=JSON.parse(fs.readFileSync(path.join(__dirname,"Centrestage_Sensitivity.json"),"utf8"));
for(const e of saved.rows){const r=runCase({...c,rent:e.rent},{id:e.scenario,exit:1,fitout:e.fitout},I);assert(Math.abs(r.annual_mean_cash-e.annual)<1e-7);assert(Math.abs(r.profit-e.flat_profit)<1e-7);assert(Math.abs(r.peak_funding-e.peak)<1e-7);assert(Math.abs(r.profit-r.economic_profit_check)<1e-7);}
const F=JSON.parse(fs.readFileSync(path.join(__dirname,"Funnel_Register.json"),"utf8"));
assert.equal(F.cases.length,138);assert.equal(new Set(F.cases.map(x=>x.id)).size,138);
for(const c of F.cases){assert.equal(c.first_unpassed_gate,"G0");assert.equal(c.passed_gate_prefix.length,0);assert.equal(c.G0.status,"STOP");assert.equal(c.G9,"Defer");}
console.log("PASS: 138 funnel dispositions and six conditional sensitivity branches; no evidence admission implied.");
