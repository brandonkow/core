'use strict';
const assert=require('node:assert/strict');
const {chromium}=require('playwright');
(async()=>{
 const browser=await chromium.launch({...(process.env.MAP_BROWSER_CHANNEL ? {channel:process.env.MAP_BROWSER_CHANNEL} : {}),headless:true});
 const context=await browser.newContext({viewport:{width:1440,height:900},colorScheme:'light',reducedMotion:'reduce'});
 const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
 const checks=[],layouts=[];
 try{
  await page.goto(process.env.MAP_TEST_URL||'http://127.0.0.1:8788/',{waitUntil:'domcontentloaded'});
  await page.locator('.node').first().waitFor();assert.equal(await page.locator('.node').count(),112);
  await page.getByRole('tab',{name:'Current SOP & progress',exact:true}).click();
  assert.match(await page.locator('#programme-status').innerText(),/138.*138/);
  assert.match(await page.locator('#programme-status').innerText(),/0 Deploy/);
  assert.match(await page.locator('#completion-guide').innerText(),/2027-10-06/);
  assert.match(await page.locator('#current-stress-rules').innerText(),/4.25%/);
  const link=page.getByRole('link',{name:'Financial SOP v2',exact:true});
  assert.match(await link.getAttribute('href'),/956aca7ae42578233d346c80fbbfe5b4be995c85\/sop\/Financial_Execution_SOP_v2.md$/);
  checks.push('Dated paused progress, 138/zero-Deploy counts, current SOP links and stress settings');
  await page.getByRole('tab',{name:'Run a path',exact:true}).click();
  await page.locator('[data-preset="1"]').click();
  assert.match(await page.locator('#funnel-prefix').innerText(),/None.*G0/s);
  assert.match(await page.locator('[data-id="G6"] .statebadge').textContent(),/CONDITIONAL/);
  assert(!(await page.locator('[data-id="G6"]').getAttribute('class')).includes('st-pass'));
  assert.equal(await page.locator('#r-G5-val').isDisabled(),true);
  const outcomes=['Defer','Defer','Reject','Preserve Capacity','Defer','Defer','Deploy'];
  for(let i=0;i<outcomes.length;i++){
   await page.locator('[data-preset="'+i+'"]').click();assert.equal(await page.locator('.verdict').innerText(),outcomes[i]);
  }
  assert.match(await page.locator('#funnel-prefix').innerText(),/G0 → G1 → G2 → G3 → G4 → G5 → G6 → G7 → G8/);
  checks.push('Seven presets; prefix stops; conditional later nodes; independent Reject/Preserve precedence');
  await page.getByRole('tab',{name:'Explore',exact:true}).click();
  await page.locator('[data-id="X1"]').press('Enter');
  await page.locator('#calc-rent').fill('2500');
  await page.locator('#calc-separate').check();
  await page.locator('#calc-price').fill('450000');
  await page.locator('#calc-basis').fill('500000');
  let out=await page.locator('#calc-out').innerText();assert(out.includes('450,000.00')&&out.includes('6.666666%'));
  await page.locator('#calc-basis').fill('0');assert(await page.locator('#calc-error').isVisible());assert.equal(await page.locator('#calc-out').innerText(),'');
  await page.locator('#calc-basis').fill('500000');await page.locator('#calc-separate').uncheck();
  assert(!(await page.locator('#calc-basis').isVisible()));assert((await page.locator('#calc-out').innerText()).includes('405,000.00'));
  await page.locator('#calc-price').fill('');assert(await page.locator('#calc-error').isVisible());
  await page.locator('#calc-price').fill('300022');await page.locator('#calc-rent').fill('1500.11');
  assert((await page.locator('#calc-out').innerText()).includes('6.000000%'));
  checks.push('Gross/net loan and yield separation, resale reset, invalid gross/blank price, exact-six boundary');
  await page.getByRole('tab',{name:'Walk the reasoning',exact:true}).click();
  assert.match(await page.locator('#drawerBody').innerText(),/STEP 1 OF 16/);
  await page.locator('[data-step="1"]').click();
  assert.match(await page.locator('#drawerBody').innerText(),/STEP 2 OF 16/);
  await page.locator('#zoomIn').click();await page.locator('#zoomFit').click();
  await page.locator('#togglePanel').click();assert((await page.locator('#stage').getAttribute('class')).includes('collapsed'));
  await page.locator('#togglePanel').click();
  checks.push('Reasoning navigation, map zoom controls and panel toggle');
  for(const [w,h,theme]of [[1440,900,'light'],[1440,900,'dark'],[1024,768,'light'],[861,600,'light'],[390,844,'dark'],[320,568,'light']]){
   await page.setViewportSize({width:w,height:h});await page.emulateMedia({colorScheme:theme});
   for(const name of ['Explore','Walk the reasoning','Run a path','Current SOP & progress']){
    await page.getByRole('tab',{name,exact:true}).click();
    const d=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,drawer:document.querySelector('#drawer').clientHeight,stage:document.querySelector('#stage').clientHeight}));
    assert(d.scroll<=w&&d.drawer>40&&d.stage>80,JSON.stringify({name,w,d}));
   }
   if(w<860){await page.locator('#sheetToggle').click();assert((await page.locator('#drawer').getAttribute('class')).includes('min'));await page.locator('#sheetToggle').click();}
   layouts.push([w,h,theme]);
  }
  assert.deepEqual(errors,[]);
  const result={status:'PASS',browser:browser.version(),checks,layouts,pageErrors:errors};
  if(process.env.MAP_SCREENSHOT==='1'){
   await page.setViewportSize({width:1440,height:900});await page.emulateMedia({colorScheme:'light'});
   await page.getByRole('tab',{name:'Current SOP & progress',exact:true}).click();
   result.screenshot=(await page.screenshot({type:'jpeg',quality:35})).toString('base64');
  }
  console.log(JSON.stringify(result));
 }finally{await context.close();await browser.close();}
})().catch(e=>{console.error(e.stack||e);process.exitCode=1;});
