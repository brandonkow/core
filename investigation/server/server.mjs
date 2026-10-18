
import http from 'node:http';
import { DatabaseSync } from 'node:sqlite';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { timingSafeEqual } from 'node:crypto';
import { validateWorkspace } from '../repository.mjs';
import { seedWorkspace } from '../data.mjs';
export function createCoreServer({dbPath='core.sqlite',token,allowedOrigin='',initial=seedWorkspace()}={}){
 if(typeof token!=='string'||token.length<32)throw new Error('CORE_API_TOKEN must contain at least 32 characters.');
 const db=new DatabaseSync(dbPath);
 db.exec(readFileSync(new URL('./schema.sql',import.meta.url),'utf8'));
 db.prepare('INSERT OR IGNORE INTO workspaces VALUES (?, 1, 1, ?, ?)').run('default',JSON.stringify(validateWorkspace(initial)),new Date().toISOString());
 const get=db.prepare('SELECT revision, document FROM workspaces WHERE id = ?');
 const srv=http.createServer(async(req,res)=>{
  res.setHeader('X-Content-Type-Options','nosniff');res.setHeader('Cache-Control','no-store');
  const origin=req.headers.origin;
  if(origin&&origin!==allowedOrigin&&origin!=='http://'+req.headers.host&&origin!=='https://'+req.headers.host){res.writeHead(403);return res.end('Origin not allowed');}
  if(origin){res.setHeader('Access-Control-Allow-Origin',origin);res.setHeader('Vary','Origin');res.setHeader('Access-Control-Expose-Headers','ETag');}
  const path=new URL(req.url,'http://localhost').pathname;
  if(req.method==='OPTIONS'){res.setHeader('Access-Control-Allow-Methods','GET, PUT, OPTIONS');res.setHeader('Access-Control-Allow-Headers','Authorization, Content-Type, If-Match');res.writeHead(204);return res.end();}
  if(path==='/health'&&req.method==='GET'){res.setHeader('Content-Type','application/json');return res.end('{"status":"ok","schemaVersion":1}');}
  if(path!=='/v1/workspace'){res.writeHead(404);return res.end('Not found');}
  const supplied=Buffer.from(req.headers.authorization||''),expected=Buffer.from('Bearer '+token);
  if(supplied.length!==expected.length||!timingSafeEqual(supplied,expected)){res.writeHead(401);return res.end('Unauthorised');}
  const send=(status,row)=>{res.setHeader('Content-Type','application/json');res.setHeader('ETag','"'+row.revision+'"');res.writeHead(status);res.end(row.document);};
  if(req.method==='GET')return send(200,get.get('default'));
  if(req.method!=='PUT'){res.setHeader('Allow','GET, PUT');res.writeHead(405);return res.end('Method not allowed');}
  if(!req.headers['if-match']){res.writeHead(428);return res.end('If-Match required');}
  if(!req.headers['content-type']?.startsWith('application/json')){res.writeHead(415);return res.end('JSON required');}
  try{
   const chunks=[];let bytes=0;
   for await(const chunk of req){bytes+=chunk.length;if(bytes>2e6){res.writeHead(413);res.end('Workspace too large');return;}chunks.push(chunk);}
   const payload=validateWorkspace(JSON.parse(Buffer.concat(chunks).toString('utf8')));
   const document=JSON.stringify(payload),now=new Date().toISOString();
   db.exec('BEGIN IMMEDIATE');
   try{
    const row=get.get('default');
    if(req.headers['if-match']!=='"'+row.revision+'"'){db.exec('ROLLBACK');res.writeHead(412);return res.end('Revision conflict');}
    db.prepare('INSERT INTO workspace_revisions VALUES (?, ?, ?, ?)').run('default',row.revision,row.document,now);
    db.prepare('UPDATE workspaces SET revision=revision+1, document=?, updated_at=? WHERE id=?').run(document,now,'default');
    db.exec('COMMIT');return send(200,get.get('default'));
   }catch(error){if(db.isTransaction)db.exec('ROLLBACK');throw error;}
  }catch(error){res.writeHead(error instanceof SyntaxError||error.message.startsWith('Invalid workspace:')?400:500);res.end(error.message.startsWith('Invalid workspace:')?error.message:'Request failed');}
 });
 srv.requestTimeout=15000;srv.on('close',()=>db.close());return srv;
}
if(process.argv[1]&&fileURLToPath(import.meta.url)===process.argv[1]){
 const srv=createCoreServer({dbPath:process.env.CORE_DB_PATH||'core.sqlite',token:process.env.CORE_API_TOKEN,allowedOrigin:process.env.CORE_ALLOWED_ORIGIN||''});
 srv.listen(Number(process.env.PORT||8792),process.env.HOST||'127.0.0.1',()=>console.log('Core API listening on '+JSON.stringify(srv.address())));
}
