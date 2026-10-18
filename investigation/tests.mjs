
import assert from 'node:assert/strict';
import { readFileSync, mkdtempSync, unlinkSync, rmdirSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { once } from 'node:events';
import { FORM, BASE, PRESETS, evaluate, calcStandard, gateTrace } from './engine.mjs';
import { seedWorkspace } from './data.mjs';
import { validateWorkspace, LocalRepository } from './repository.mjs';
import { createCoreServer } from './server/server.mjs';
const map=readFileSync(new URL('../visualization/Decision_Engine_Neural_Map.html',import.meta.url),'utf8');
const engine=readFileSync(new URL('./engine.mjs',import.meta.url),'utf8');
const extracted=map.slice(map.indexOf('const FORM'),map.indexOf('/* ------------------------------------------------------------------ svg build'));
assert.ok(engine.includes(extracted),'Bundled engine must match latest map exactly');
assert.equal(evaluate({...BASE,G0:'stop',G5:'val'}).d,'defer');
assert.equal(evaluate({...BASE,G0:'stop',G4:'fail'}).d,'reject');
assert.equal(evaluate({...BASE,G0:'stop',G8:'cap'}).d,'preserve');
assert.equal(evaluate({...BASE,G4:'fail',G8:'cap'}).d,'reject');
assert.equal(evaluate({...BASE,cov:'neg',tr:'no'}).d,'defer');
assert.equal(evaluate({...BASE,cov:'neg',tr:'yes'}).d,'deploy');
assert.equal(evaluate({...BASE,div:'partial',residual:'no'}).d,'defer');
assert.equal(evaluate({...BASE,role:'spec',G5:'fair'}).d,'defer');
assert.equal(evaluate({...BASE,role:'spec',G5:'val'}).d,'deploy');
assert.equal(gateTrace(evaluate({...BASE,G0:'stop'}).gs).prefix.length,0);
assert.equal(gateTrace(evaluate({...BASE,G3:'unk'}).gs).firstStop,'G3');
const a=calcStandard(558000,3000,380,620000),b=calcStandard(558000,3000,380);
assert.ok(a.inst>b.inst);assert.equal(a.yieldMicro,b.yieldMicro);
assert.equal(calcStandard(0,3000,380),null);
assert.equal(calcStandard(558000,3000,-1),null);
const w=seedWorkspace();validateWorkspace(w);
for(const p of w.properties)assert.equal(evaluate(p.assessment).d,'defer');
const bad=structuredClone(w);bad.properties[0].assessment.G0='pass';assert.throws(()=>validateWorkspace(bad));
const duplicate=structuredClone(w);duplicate.properties[1].id=duplicate.properties[0].id;assert.throws(()=>validateWorkspace(duplicate));
const no=structuredClone(w);no.properties[0].finance.rent=null;validateWorkspace(no);
const nan=structuredClone(w);nan.properties[0].finance.rent=NaN;assert.throws(()=>validateWorkspace(nan));
const mem=new Map(),storage={getItem:k=>mem.get(k)||null,setItem:(k,v)=>mem.set(k,v)};
const local=new LocalRepository(storage);await local.save(w);assert.deepEqual(await local.load(),w);
storage.getItem=()=>'{invalid';await assert.rejects(()=>local.load());
const token='test-only-secret-01234567890123456789';
const server=createCoreServer({dbPath:':memory:',token,allowedOrigin:'https://ui.example'});
server.listen(0,'127.0.0.1');await once(server,'listening');
const base='http://127.0.0.1:'+server.address().port;
try{
 const auth={Authorization:'Bearer '+token};
 assert.equal((await fetch(base+'/v1/workspace')).status,401);
 assert.equal((await fetch(base+'/v1/workspace',{headers:{...auth,Origin:'https://evil.example'}})).status,403);
 let r=await fetch(base+'/v1/workspace',{headers:{...auth,Origin:'https://ui.example'}});assert.equal(r.status,200);assert.equal(r.headers.get('access-control-expose-headers'),'ETag');
 const etag=r.headers.get('etag'),doc=await r.json();doc.properties[0].notes='saved through API';
 const write=(tag,body)=>fetch(base+'/v1/workspace',{method:'PUT',headers:{...auth,'Content-Type':'application/json',...(tag?{'If-Match':tag}:{})},body:JSON.stringify(body)});
 assert.equal((await write(null,doc)).status,428);
 assert.equal((await write(etag,{schemaVersion:2})).status,400);
 r=await write(etag,doc);assert.equal(r.status,200);assert.notEqual(r.headers.get('etag'),etag);
 assert.equal((await write(etag,w)).status,412);
 const latest=await (await fetch(base+'/v1/workspace',{headers:auth})).json();assert.equal(latest.properties[0].notes,'saved through API');
}finally{await new Promise(resolve=>server.close(resolve));}
console.log('Core: engine parity, precedence, financial separation, validation, storage and authenticated API/revision checks passed.');

const temp=mkdtempSync(join(tmpdir(),'core-db-test-')),dbPath=join(temp,'workspace.sqlite');
let durable;
try{
 durable=createCoreServer({dbPath,token});durable.listen(0,'127.0.0.1');await once(durable,'listening');
 let endpoint='http://127.0.0.1:'+durable.address().port+'/v1/workspace';
 let res=await fetch(endpoint,{headers:{Authorization:'Bearer '+token}});
 const originalTag=res.headers.get('etag'),doc=await res.json();doc.properties[0].notes='Survives a server restart';
 assert.equal((await fetch(endpoint,{method:'PUT',headers:{Authorization:'Bearer '+token,'Content-Type':'application/json','If-Match':originalTag},body:JSON.stringify(doc)})).status,200);
 await new Promise(r=>durable.close(r));durable=null;
 durable=createCoreServer({dbPath,token});durable.listen(0,'127.0.0.1');await once(durable,'listening');
 endpoint='http://127.0.0.1:'+durable.address().port+'/v1/workspace';
 res=await fetch(endpoint,{headers:{Authorization:'Bearer '+token}});
 assert.equal((await res.json()).properties[0].notes,'Survives a server restart');
 assert.notEqual(res.headers.get('etag'),originalTag);
 console.log('Core SQLite durable restart check passed.');
}finally{
 if(durable)await new Promise(r=>durable.close(r));
 for(const suffix of ['','-wal','-shm'])if(existsSync(dbPath+suffix))unlinkSync(dbPath+suffix);
 rmdirSync(temp);
}
