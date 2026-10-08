"""Verify a GitHub-downloaded archive against its exact commit and preserved sources."""
import argparse,hashlib,json,subprocess,zipfile
from pathlib import Path
P=Path(__file__).resolve().parent
def run(args):return subprocess.check_output(args,cwd=P).decode('utf-8').strip()
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
# Current navigation/status registers that AGENTS.md lets advance after the transfer. They must still exist;
# their bytes may differ from MIGRATION_MANIFEST.json. Every other manifest file stays byte-checked.
NAVIGATION_REGISTERS={'README.md','klang-valley-2026-10-07/round-3/README.md','klang-valley-2026-10-07/round-3/Coverage_Audit.md'}
def verify(archive,commit):
 local=run(['git','rev-parse','HEAD']);assert local==commit
 remote=run(['git','ls-remote','origin','refs/heads/main']).split()[0];assert remote==commit
 tree=subprocess.check_output(['git','ls-tree','-rz',commit],cwd=P).decode('utf-8')
 expected={}
 for row in tree.split('\0'):
  if not row:continue
  meta,name=row.split('\t',1);mode,kind,oid=meta.split()
  assert kind=='blob' and mode in ['100644','100755'],name
  expected[name]=oid
 with zipfile.ZipFile(archive) as z:
  files={};roots=set()
  for item in z.infolist():
   if item.is_dir():continue
   root,rel=item.filename.split('/',1);roots.add(root)
   assert '..' not in Path(rel).parts and not Path(rel).is_absolute()
   assert rel not in files
   files[rel]=z.read(item)
  assert len(roots)==1
  assert set(files)==set(expected),(set(files)-set(expected),set(expected)-set(files))
  assert all(blob(b)==expected[name] for name,b in files.items())
  manifest=json.loads(files['MIGRATION_MANIFEST.json'])
  assert NAVIGATION_REGISTERS<={item['path'] for item in manifest['files']},NAVIGATION_REGISTERS
  checked=0;advanced=[]
  for item in manifest['files']:
   assert item['path'] in files,'Missing preserved file '+item['path']
   b=files[item['path']]
   if item['path'] in NAVIGATION_REGISTERS:
    if len(b)!=item['bytes'] or sha(b)!=item['sha256']:advanced.append(item['path'])
    continue
   assert len(b)==item['bytes'] and sha(b)==item['sha256'],item['path'];checked+=1
  master='1fbf607a78111bc007736fe0cc8109ad3967939a2dcc7ff54f017b491172e86b'
  assert sha(files['Residential_Investment_Framework.md'])==master
  base='klang-valley-2026-10-07/round-3/'
  preserved=json.loads(files[base+'Preservation_Audit.json'])
  frozen=0
  for item in preserved['checks']:
   assert sha(files[item['path'].replace('\\','/')])==item['expected'],item['path'];frozen+=1
  for release in ['B03','B04','B05']:
   m=json.loads(files[base+release+'_Release_Manifest.json'])
   for name,digest in m['files'].items():
    assert sha(files[base+name])==digest,name;frozen+=1
  return dict(version='CORE-REMOTE-VERIFICATION-2026-10-08',status='PASS',repository='https://github.com/brandonkow/core',
   verified_commit=commit,remote_main_matches=True,verification_source='GitHub exact-commit zipball downloaded through authenticated gh API; complete archive compared to Git tree blobs',
   tracked_archive_files=len(files),tracked_markdown_files=sum(k.endswith('.md') for k in files),preserved_source_files=len(manifest['files']),generated_source_files=manifest['generated_source_files'],
   additional_user_source_files=manifest['additional_user_source_files'],source_sha256_checks=checked,
   navigation_registers_exempt=sorted(NAVIGATION_REGISTERS),navigation_registers_advanced=sorted(advanced),frozen_file_comparisons=frozen,master_sha256=master,
   all_archive_blobs_match=True,all_frozen_source_bytes_match=True,local_deletion_authorized=False,
   boundary='File transfer and preservation verification only; no investment approval. Local cleanup is suspended by AGENTS.md, so a pass does not authorise deletion.')
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--archive',required=True);a.add_argument('--commit',required=True);a.add_argument('--receipt')
 args=a.parse_args();result=verify(args.archive,args.commit)
 if args.receipt:
  q=(P/args.receipt).resolve();assert q.parent==P
  q.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(result,indent=2))

