"use strict";
// Run with Node: node reproduce.cjs. Reads saved inputs; writes JSON to stdout only.
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto");
const A=require("./financial_model.cjs"),{validate}=require("./validate.cjs");
const I=JSON.parse(fs.readFileSync(path.join(__dirname,"Inputs.json"),"utf8"));
const repo=path.resolve(__dirname,"../../..");
for(const [p,expected] of Object.entries(I.source_blobs)){
 const data=fs.readFileSync(path.join(repo,p));const actual=crypto.createHash("sha1").update(Buffer.from("blob "+data.length+"\0")).update(data).digest("hex");
 if(actual!==expected)throw Error("Source drift: "+p);
}
const O=A.replay(I);const validation=validate(I,O,A);
process.stdout.write(JSON.stringify({validation,...O},null,2)+"\n");
