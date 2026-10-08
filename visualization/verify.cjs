// Reproducible checks for the map only; not investment validation.
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const cp = require('node:child_process');
const assert = require('node:assert/strict');
const root = process.env.MAP_REMOTE_REF ? null : path.resolve(__dirname, '..');
function read(file) {
  if (!process.env.MAP_REMOTE_REF) return fs.readFileSync(path.join(root, file), 'utf8');
  const endpoint = file.endsWith('.html') && process.env.MAP_HTML_BLOB
    ? 'git/blobs/' + process.env.MAP_HTML_BLOB
    : 'contents/' + file + '?ref=' + process.env.MAP_REMOTE_REF;
  const r = JSON.parse(cp.execFileSync('gh', ['api', 'repos/brandonkow/core/' + endpoint], {encoding:'utf8', maxBuffer:5e6}));
  return Buffer.from(r.content, 'base64').toString('utf8');
}
const html = read('visualization/Decision_Engine_Neural_Map.html');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
new vm.Script(script); // The entire browser script must parse.
const prefix = script.slice(script.indexOf("(() => {") + "(() => {".length,
  script.indexOf('/* ------------------------------------------------------------------ svg build */'));
const app = vm.runInNewContext('(function(){' + prefix +
  ';return {N,ORDER,EDGES,STEPS,FORM,BASE,PRESETS,evaluate,ROUTES,CORE,GATES,calcStandard};})()', {
  window:{matchMedia:()=>({matches:true})}
});
const sha256 = s => crypto.createHash('sha256').update(s).digest('hex');
const expected = {
'Residential_Investment_Framework.md':'1fbf607a78111bc007736fe0cc8109ad3967939a2dcc7ff54f017b491172e86b',
'sop/Approved_Execution_Supplement.md':'2e62521e1b95eeaae3801020d762d9e76b4005ade30065b50a990ce1eb2f5b74',
'sop/Founder_QA_Approval_Register.md':'d60b617cc6568670df93d7a9d8269d6b1ae8ebcf707e1880c6528367152cce81',
'execution-release-2026-10-07/Decision_Execution_Standard.md':'ac13a9c14b7b30908e500ec75b0ad3edaf6f234730c40a3f3322312466c17327',
'execution-release-2026-10-07/Case_Workpaper_Template.md':'8cc826e2ddfa4194a77543342277c59c0aea6ecb05e487255745f5b18f39abc7',
'execution-release-2026-10-07/financial_config.json':'ddcbfca298e1ee33a55544f8c25750b17c60a531eccddd62ad6ddc124a4a367c',
'phase-7/Phase_7_SOP_Addendum.md':'7c637ea580058d526f55acc5be57a847dd14d6e00e5ab507e0e6a48fb9203620',
'Evidence_Judgment_Divergence_Integration_Audit.md':'3c4928fcfff065f450c1200108bdad83d19c53b7f6dd25c19dfeaae500996096'
};
const sources = {};
for (const [file,hash] of Object.entries(expected)) {
  sources[file] = read(file);
  assert.equal(sha256(sources[file]),hash,'Source changed: re-review the map against '+file);
}
const norm = s => s.replace(/^[ \t]*(?:[-*]|\d+\.)\s+/gm,'').replace(/[*_\x60>#;:.,]/g,'').replace(/\s+/g,' ').trim();
const strictNorm = s => s.replace(/[*_\x60>#]/g,'').replace(/\s+/g,' ').trim();
const sourceFor = label => label.startsWith('Master') ? 'Residential_Investment_Framework.md' :
 label.startsWith('Execution supplement') ? 'sop/Approved_Execution_Supplement.md' :
 label.startsWith('Execution standard') ? 'execution-release-2026-10-07/Decision_Execution_Standard.md' : null;
const quotes = [];
for(const n of Object.values(app.N)) {
  for(const key of ['q','stop','watch','packet','partial']) if(n[key]) quotes.push([n.id || n.code || n.label,key,n[key], key === 'packet' || key === 'partial' ? 'Execution standard' : n.src]);
}
for(const [i,s] of app.STEPS.entries()) for(const key of ['q','stop','cond'])
  if(s[key]) quotes.push(['step '+i,key,s[key],s.src]);
const misses = quotes.filter(([id,k,q,label]) => {
 const files = [sourceFor(label), ...(label.includes('Execution supplement') ? ['sop/Approved_Execution_Supplement.md'] : []),
 ...(label.includes('Execution standard') ? ['execution-release-2026-10-07/Decision_Execution_Standard.md'] : [])].filter(Boolean);
 assert(files.length, 'Unknown source label '+label);
 return !files.some(file => strictNorm(sources[file]).includes(strictNorm(q)) || norm(sources[file]).includes(norm(q)));
});
assert.equal(quotes.length,164);
assert.equal(misses.length,0,'Unmatched quotations: '+JSON.stringify(misses));
assert.equal(Object.values(app.N).filter(n=>n.L==='core').length,35);
assert.equal(Object.values(app.N).filter(n=>n.L==='gate').length,10);
assert(!app.N.G10);
for(const e of app.EDGES) {
  assert(app.N[e.f] && app.N[e.t], 'Dangling edge '+e.f+' > '+e.t);
  assert(['s','i'].includes(e.prov));
}
for(const step of app.STEPS) for(const id of step.nodes) assert(app.N[id], 'Dangling step node '+id);

// Independently parse the authoritative Markdown routing table, not the map's ROUTES array.
const table = sources['Residential_Investment_Framework.md'].split('| Finding / analytical destination |')[1].split('\n\n')[0];
const rows = table.split('\n').filter(l=>/^\|[^|]*\|[^|]*5\.\d/.test(l));
assert.equal(rows.length,13);
const routeCounts=new Map(), requiredPairs=new Set();
rows.forEach((line,i)=>{
 const cells=line.split('|');
 const cores=[...cells[2].matchAll(/\b5\.(\d+)/g)].map(m=>'c'+m[1]);
 let gates;
 if(i===1) gates=Array.from({length:10},(_,i)=>'G'+i);
 else gates=[...cells[3].matchAll(/\bG(\d)\b/g)].map(m=>'G'+m[1]);
 for(const c of cores)for(const g of gates){
   const key=c+'>'+g;routeCounts.set(key,(routeCounts.get(key)||0)+1);
   if(i!==1||g==='G0'||g==='G5')requiredPairs.add(key);
 }
});
const coreEdges=app.EDGES.filter(e=>app.N[e.f].L==='core'&&app.N[e.t].L==='gate');
for(const key of requiredPairs)assert(coreEdges.some(e=>e.f+'>'+e.t===key&&e.prov==='s'),'Missing stated route '+key);
for(const e of coreEdges.filter(e=>e.prov==='s'))
 assert.equal(e.rows,routeCounts.get(e.f+'>'+e.t),'Routing count '+e.f+'>'+e.t);

const presetExpected=['defer','defer','reject','preserve','defer','defer','deploy'];
app.PRESETS.forEach((p,i)=>assert.equal(app.evaluate({...app.BASE,...p[2]}).d,presetExpected[i],p[0]));
let total=0; const counts={deploy:0,defer:0,reject:0,preserve:0};
function check(s) {
  const r=app.evaluate(s); total++; counts[r.d]++;
  const failure=['G3','G4','G6','G7'].some(g=>s[g]==='fail');
  assert.equal(r.d==='reject',failure);
  if(!failure && s.G8==='cap') assert.equal(r.d,'preserve');
  if(r.d==='preserve') assert.equal(s.G8,'cap');
  const upstream=['G0','G1','G2','G3','G4'].every(g=>s[g]==='ok');
  if(!upstream) assert.equal(r.gs.G5,'blocked');
  if(s.cov==='neg') assert.match(r.prio,/lowest research/i);
  if(r.d==='deploy') {
    assert(upstream);
    assert(['val','fair'].includes(s.G5));
    assert.equal(s.G6,'ok'); assert.equal(s.G7,'ok'); assert.equal(s.G8,'ok');
    assert.notEqual(s.div,'unresolved');
    assert.notEqual(s.cov,'unv');
    assert(s.cov!=='neg'||s.tr==='yes');
    assert(s.role!=='spec'||s.G5==='val');
    if(s.div==='partial') assert.equal(s.residual,'yes');
  }
  if(!failure && s.G8!=='cap' && s.div==='partial' && s.residual!=='yes')
    assert.equal(r.d,'defer','Residual uncertainty cannot pass on a note alone');
}
function walk(i,s) {
  if(i===app.FORM.length){check(s);return;}
  const [id,,opts]=app.FORM[i];
  for(const [v] of opts)walk(i+1,{...s,[id]:v});
}
walk(0,{});
// Standard-coverage calculator arithmetic (integer sen), checked outside the browser.
const cs = app.calcStandard;
const payment = loan => { const r = 0.04 / 12; return loan * r / (1 - Math.pow(1 + r, -420)); }; // financial_engine.payment(loan, 0.04, 35)
let dflt = cs(500000, 2200, 350);
assert(Math.abs(dflt.inst - payment(450000)) < 1e-9 && dflt.cov < 0 && dflt.yieldMicro === 5280000n && !dflt.meets, 'default calculator case');
const exact = cs(300022, 1500.11, 350);
assert(exact.meets && exact.yieldMicro === 6000000n, 'exact 6% boundary must meet the preference');
assert.equal(cs(102414, 0, 0).sixSen, 51207, '6% rent must round up to the exact sen');
for (const bad of [[0, 1, 1], [-1, 1, 1], [1, -1, 1], [1, 1, -1], [0.004, 1, 1]]) assert.equal(cs(...bad), null, 'invalid calculator input ' + bad);
let calculatorCases = 0;
for (let P = 100000; P <= 1600000; P += 499) for (const fee of [0, 350, 1234.56]) {
  const c0 = cs(P, 0, fee); calculatorCases++;
  assert.equal(BigInt(c0.sixSen), (BigInt(Math.round(P * 100)) + 199n) / 200n, '6% rent at ' + P);
  assert(cs(P, c0.sixSen / 100, fee).meets && !cs(P, (c0.sixSen - 1) / 100, fee).meets, '6% boundary at ' + P);
  assert(cs(P, c0.zeroSen / 100, fee).cov >= 0 && cs(P, (c0.zeroSen - 1) / 100, fee).cov < 0, 'zero-coverage rent at ' + P);
}
console.log(JSON.stringify({status:'PASS',htmlSha256:sha256(html),sourceFiles:Object.keys(expected).length,
  quotations:quotes.length,nodes:app.ORDER.length,edges:app.EDGES.length,
  core:35,gates:10,steps:app.STEPS.length,presets:app.PRESETS.length,combinations:total,decisions:counts,calculatorCases},null,2));
