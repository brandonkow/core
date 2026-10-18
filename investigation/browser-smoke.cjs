
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
(async()=>{
const browser=await chromium.launch({headless:true,...(process.env.CORE_BROWSER_CHANNEL?{channel:process.env.CORE_BROWSER_CHANNEL}:{})});
const page=await browser.newPage({viewport:{width:1440,height:1000}});
const errors=[];page.on('pageerror',e=>errors.push(e.message));
const url=process.env.CORE_TEST_URL||'http://127.0.0.1:8788/investigation/';
try{
await page.goto(url);await page.getByRole('heading',{name:'See the whole picture.'}).waitFor();
assert.equal(await page.locator('.property-card').count(),6);
await page.locator('#search').fill('Meridian');assert.equal(await page.locator('.property-card').count(),1);
await page.locator('#search').fill('');
await page.locator('.property-card[data-property="p02"]').click();assert.match(await page.locator('.dossier h2').textContent(),/Courtyard/);
await page.getByRole('button',{name:'Toggle floor cutaway'}).click();
await page.getByRole('button',{name:'Rotate district'}).click();
await page.getByRole('button',{name:'Zoom in',exact:true}).click();
await page.getByRole('button',{name:'Toggle scene animation'}).click();
await page.locator('[data-layer="demand"]').click();assert.equal(await page.locator('.flow').count(),1);
await page.getByRole('button',{name:'Evidence',exact:true}).click();
await page.locator('[data-evidence]').first().selectOption('conflicting');
await page.locator('#hypothesis-form [name=note]').fill('Observed contradiction for review');
await page.getByRole('button',{name:'Save hypothesis',exact:true}).click();
await page.getByRole('button',{name:'Tasks',exact:true}).click();await page.getByRole('button',{name:'+ New task'}).click();
await page.locator('#item-form [name=title]').fill('Check unit-linked title');
await page.locator('#item-form [name=owner]').fill('Analyst');
await page.locator('#item-form button').click();await page.locator('[data-task]').last().selectOption('in-progress');
await page.getByRole('button',{name:'Scenarios',exact:true}).click();
await page.locator('#finance-form [name=kind]').selectOption('launch');
await page.locator('#finance-form [name=gross]').fill('620000');
await page.locator('#finance-form [name=nett]').fill('558000');
await page.locator('#finance-form [name=rent]').fill('3000');
await page.locator('#finance-form [name=fee]').fill('380');
await page.getByRole('button',{name:'Recalculate & save'}).click();assert.match(await page.locator('#coverage').textContent(),/RM/);
await page.locator('#finance-form [name=rent]').fill('');await page.getByRole('button',{name:'Recalculate & save'}).click();assert.equal(await page.locator('#coverage').textContent(),'Unknown');
await page.getByRole('button',{name:'Decision',exact:true}).click();
await page.locator('#gates-form [name=G4]').selectOption('fail');await page.getByRole('button',{name:'Apply assessments'}).click();assert.equal(await page.locator('.decision-title').textContent(),'Reject');
await page.getByRole('button',{name:'Save decision snapshot'}).click();await page.locator('#snapshot-form textarea').fill('UI verification snapshot');await page.locator('#snapshot-form button').click();await page.getByRole('heading',{name:'Keep the reasoning.'}).waitFor();
assert.match(await page.locator('.timeline').first().textContent(),/UI verification snapshot/);
await page.reload();await page.getByRole('button',{name:'Evidence',exact:true}).click();await page.locator('#property-picker').selectOption('p02');assert.equal(await page.locator('[data-evidence]').first().inputValue(),'conflicting');
await page.getByRole('button',{name:'Data & export'}).click();
const download=page.waitForEvent('download');await page.getByRole('button',{name:'Export workspace JSON'}).click();assert.match((await download).suggestedFilename(),/core-workspace/);
await page.getByRole('button',{name:'Close',exact:true}).click();

await page.getByRole('button',{name:'Data & export'}).click();
await page.locator('#import-file').setInputFiles({name:'bad.json',mimeType:'application/json',buffer:Buffer.from('{"schemaVersion":99}')});
await page.waitForFunction(()=>document.querySelector('#toast').textContent.includes('Invalid workspace'));
assert.equal(await page.locator('#dialog').isVisible(),true);
const imported=JSON.parse(await page.evaluate(()=>localStorage.getItem('core-investigation-v1')));
imported.properties[0].name='<img src=x onerror=alert(1)>';
await page.locator('#import-file').setInputFiles({name:'workspace.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(imported))});
await page.waitForFunction(()=>!document.querySelector('#dialog').open);
await page.getByRole('button',{name:'District',exact:true}).click();
assert.equal(await page.locator('.dossier h2').textContent(),'<img src=x onerror=alert(1)>');
assert.equal(await page.locator('.dossier h2 img').count(),0);
await page.getByRole('button',{name:'Data & export'}).click();await page.getByRole('button',{name:'Reset demo',exact:true}).click();await page.getByRole('button',{name:'Reset browser demo',exact:true}).click();
await page.getByRole('heading',{name:'See the whole picture.'}).waitFor();
for(const width of [1024,390,320]){
 await page.setViewportSize({width,height:844});
 for(const tab of ['District','Evidence','Tasks','Scenarios','Decision','Journal']){
  await page.getByRole('button',{name:tab,exact:true}).click();
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),tab+' overflow at '+width);
 }
}
await page.emulateMedia({reducedMotion:'reduce'});await page.reload();assert.equal(await page.locator('.shell.paused').count(),1);
assert.deepEqual(errors,[]);
console.log('Core browser checks passed: scene, search, evidence, tasks, scenarios, gates, snapshots, persistence, export and responsive navigation.');
}finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
