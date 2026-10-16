"use strict";
const fs=require("node:fs");
const path=require("node:path");
const api=require("./financial_model");
const {validate}=require("./validate_model");
const cfg=JSON.parse(fs.readFileSync(path.join(__dirname,"Inputs.json"),"utf8"));
const full=api.run(cfg);
const validation=validate(api,cfg,full);
console.log(JSON.stringify({validation,results:full.results.map(({ledger,...r})=>r)},null,2));
