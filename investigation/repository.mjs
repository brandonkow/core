
import { FORM } from './engine.mjs';
import { seedWorkspace } from './data.mjs';

const KEY='core-investigation-v1';
export function validateWorkspace(w){
 const fail=m=>{throw new Error('Invalid workspace: '+m);};
 if(!w||w.schemaVersion!==1||!['synthetic','imported'].includes(w.kind)||!Array.isArray(w.properties)||w.properties.length>200||!w.properties.length)fail('schema or property count');
 const str=(v,n=4000)=>typeof v==='string'&&v.length<=n;
 if(!str(w.name,160)||!Array.isArray(w.activity)||w.activity.length>500)fail('workspace metadata');
 const ids=new Set();
 for(const p of w.properties){
 if(!str(p.id,80)||!p.id||ids.has(p.id))fail('unique property id');ids.add(p.id);
 for(const k of ['name','district','type','question','notes'])if(!str(p[k]))fail(k);
 for(const k of ['floors','units','beds','area'])if(!Number.isFinite(p[k])||p[k]<=0||p[k]>100000)fail(k);
 if(!Number.isInteger(p.floors)||p.floors>200)fail('floors');
 if(!p.assessment||FORM.some(([k,,opts])=>!opts.some(([v])=>p.assessment[k]===v)))fail('assessment options');
 if(!p.finance||!['launch','resale'].includes(p.finance.kind))fail('finance kind');
 for(const k of ['gross','nett','rent','fee'])if(p.finance[k]!==null&&(!Number.isFinite(p.finance[k])||p.finance[k]<0||p.finance[k]>1e10))fail(k);
 if(!p.hypothesis||['family','claim','falsifier','note'].some(k=>!str(p.hypothesis[k])))fail('hypothesis');
 for(const [key,statuses] of [['evidence',['missing','received','reviewed','conflicting']],['tasks',['open','in-progress','done']]]){
 if(!Array.isArray(p[key])||p[key].length>200)fail(key);
 const childIds=new Set();
 for(const x of p[key]){
 if(!str(x.id,100)||!x.id||childIds.has(x.id)||!str(x.title,2000)||!/^G[0-8]$/.test(x.gate)||!statuses.includes(x.status)||!str(x.note))fail(key+' item');
 childIds.add(x.id);
 if(key==='evidence'&&(!str(x.source,2000)||!str(x.observedAt,40)))fail('provenance');
 if(key==='tasks'&&!str(x.owner,100))fail('owner');
 }
 }
 if(!Array.isArray(p.history)||p.history.length>100)fail('history');
 for(const x of p.history)if(!str(x.id,100)||!str(x.at,50)||!str(x.decision,40)||!str(x.version,100)||!str(x.note,4000)||!x.inputs||FORM.some(([k,,opts])=>!opts.some(([v])=>x.inputs[k]===v)))fail('decision snapshot');
 }
 for(const x of w.activity)if(!str(x.at,50)||!str(x.text,4000))fail('activity');
 return w;
}
export class LocalRepository{
 constructor(storage=globalThis.localStorage){this.storage=storage;this.label='Browser workspace';}
 async load(){const raw=this.storage.getItem(KEY);if(!raw)return seedWorkspace();return validateWorkspace(JSON.parse(raw));}
 async save(w){this.storage.setItem(KEY,JSON.stringify(validateWorkspace(w)));}
}
export class HttpRepository{
 constructor(base,token){const u=new URL(base,location.href);if(u.protocol!=='https:'&&!['localhost','127.0.0.1'].includes(u.hostname))throw new Error('Use HTTPS for a remote API.');if(u.username||u.password||u.search||u.hash)throw new Error('Use an API origin without credentials, query or fragment.');this.base=u.href.replace(/\/$/,'');this.token=token;this.etag=null;this.label='Connected workspace';}
 async request(method,w){
 const response=await fetch(this.base+'/v1/workspace',{method,headers:{Authorization:'Bearer '+this.token,...(w?{'Content-Type':'application/json','If-Match':this.etag||''}:{})},body:w?JSON.stringify(validateWorkspace(w)):undefined,signal:AbortSignal.timeout(12000)});
 if(response.status===412)throw new Error('Another session changed this workspace. Export your changes, then reconnect before saving.');
 if(!response.ok)throw new Error('Workspace API returned '+response.status+'.');
 const tag=response.headers.get('etag');if(!tag)throw new Error('API did not return an ETag.');
 const data=validateWorkspace(await response.json());this.etag=tag;return data;
 }
 load(){return this.request('GET');} save(w){return this.request('PUT',w);}
}
