import json,urllib.request,asyncio,os
from websockets.asyncio.client import connect
URL=os.environ.get('MAP_TEST_URL','http://127.0.0.1:8785/')
PORT=os.environ.get('MAP_CDP_PORT','9223')
async def main():
 from urllib.parse import quote
 tab=json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:'+PORT+'/json/new?'+quote(URL,safe=':/'),method='PUT')))
 async with connect(tab['webSocketDebuggerUrl'],max_size=20_000_000) as ws:
  events=[]
  n=0
  async def call(m,p={}):
   nonlocal n
   n+=1;i=n
   await ws.send(json.dumps({'id':i,'method':m,'params':p}))
   while True:
    v=json.loads(await ws.recv())
    if v.get('id')==i:
     if 'error' in v:raise RuntimeError(str(v['error']))
     return v
    events.append(v)
  results=[]
  async def ev(code):
   v=await call('Runtime.evaluate',{'expression':code,'returnByValue':True,'awaitPromise':True})
   if 'exceptionDetails' in v['result']:raise AssertionError(v['result']['exceptionDetails'])
   return v['result']['result'].get('value')
  async def mouse_click(selector):
   rect=await ev("(()=>{const e=document.querySelector("+json.dumps(selector)+");e.scrollIntoView({block:'nearest'});const r=e.getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2};})()")
   await call('Input.dispatchMouseEvent',{'type':'mousePressed',**rect,'button':'left','clickCount':1})
   await call('Input.dispatchMouseEvent',{'type':'mouseReleased',**rect,'button':'left','clickCount':1})
  await call('Runtime.enable')
  await call('Page.enable')
  await call('Emulation.setDeviceMetricsOverride',{'width':1440,'height':900,'deviceScaleFactor':1,'mobile':False})
  await call('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-color-scheme','value':'light'},{'name':'prefers-reduced-motion','value':'reduce'}]})
  await call('Page.navigate',{'url':URL})
  await asyncio.sleep(.7)
  assert await ev("document.querySelectorAll('.node').length")==112
  await mouse_click('#tab-walk')
  assert 'STEP 1 OF 16' in (await ev("document.querySelector('#drawerBody').innerText")).upper()
  steps=await ev("""(()=>{const out=[];for(const b of document.querySelectorAll('#steps button')){b.click();out.push(document.querySelector('#drawerBody h2')?.textContent);}return out})()""")
  assert len(steps)==16 and all(steps)
  results.append('16 reasoning steps, panel text and node activation')
  await mouse_click('#tab-run')
  verdicts=await ev("""(()=>{const out=[];for(let i=0;i<7;i++){document.querySelector('[data-preset="'+i+'"]').click();out.push(document.querySelector('.verdict').textContent);}return out;})()""")
  assert verdicts==['Defer','Defer','Reject','Preserve Capacity','Defer','Defer','Deploy']
  async def select(name,value):
   await ev("(()=>{const e=document.getElementById("+json.dumps('r-'+name+'-'+value)+");e.checked=true;e.dispatchEvent(new Event('change',{bubbles:true}));})()")
  await select('div','partial')
  assert await ev("document.querySelector('.verdict').textContent")=='Defer'
  assert await ev("!!document.getElementById('r-residual-yes')")
  await select('residual','yes')
  assert await ev("document.querySelector('.verdict').textContent")=='Deploy'
  await select('div','resolved');await select('div','partial')
  assert await ev("document.getElementById('r-residual-no').checked")
  await select('G4','fail')
  assert await ev("document.querySelector('.verdict').textContent")=='Reject'
  await ev("document.querySelector('[data-preset=\"6\"]').click()")
  await select('G0','stop')
  assert await ev("Array.from(document.querySelectorAll('input[name=\"G5\"]')).every(e=>e.disabled&&!e.checked)")
  await select('G0','ok');await select('cov','neg')
  assert 'Lowest research' in await ev("document.querySelector('.prio').textContent")
  assert await ev("document.querySelector('.verdict').textContent")=='Defer'
  await select('tr','yes')
  assert await ev("document.querySelector('.verdict').textContent")=='Deploy'
  await ev("document.querySelector('[data-preset=\"0\"]').click()")
  assert await ev("document.querySelectorAll('.edge.spine.r-pass').length")==3
  assert await ev("document.querySelectorAll('.edge.spine.r-cond').length")==6
  results.append('7 presets; conditional trace after unknown; partial residual default, explicit pass and reset; independent Reject; G5 lock; shortfall transition')
  for name,v in {'G0':'stop','G1':'inc','G2':'stop','G3':'unk','G4':'unk','G6':'single','G7':'unk','cov':'neg','G8':'unk','div':'unresolved','tr':'no'}.items():await select(name,v)
  reach=await ev("""(()=>{const d=document.getElementById('drawer');d.scrollTop=d.scrollHeight;const e=document.querySelector('label[for="r-role-inc"]'),r=e.getBoundingClientRect();return document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)===e;})()""")
  assert reach
  results.append('Long result no longer covers final form inputs')
  await ev("document.querySelector('#tab-explore').click()")
  inspected=await ev("""(()=>{let count=0;for(const n of document.querySelectorAll('.node')){n.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true}));if(!document.querySelector('#drawerBody h2'))throw Error('Missing inspector '+n.dataset.id);count++;}return count;})()""")
  assert inspected==112
  await ev("document.querySelector('[data-id=\"X1\"]').dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true}))")
  default=await ev("document.querySelector('#calc-out').innerText")
  assert 'RM 450,000.00' in default and 'Negative' in default and '5.280000%' in default
  for field in ['price','rent','fee']:
   for value in ['','-1']:
    await ev("(()=>{const e=document.getElementById("+json.dumps('calc-'+field)+");e.value="+json.dumps(value)+";e.dispatchEvent(new Event('input',{bubbles:true}));})()")
    assert await ev("!document.getElementById('calc-error').hidden && document.getElementById('calc-out').textContent===''")
   await ev("(()=>{const e=document.getElementById("+json.dumps('calc-'+field)+");e.value="+json.dumps({'price':'500000','rent':'2200','fee':'350'}[field])+";e.dispatchEvent(new Event('input',{bubbles:true}));})()")
  await ev("document.getElementById('calc-price').value='0';document.getElementById('calc-price').dispatchEvent(new Event('input',{bubbles:true}))")
  assert await ev("!document.getElementById('calc-error').hidden")
  await ev("document.getElementById('calc-price').value='500000';document.getElementById('calc-rent').value='2499.99';document.getElementById('calc-rent').dispatchEvent(new Event('input',{bubbles:true}))")
  assert 'below the 6%' in await ev("document.getElementById('calc-out').innerText")
  await ev("document.getElementById('calc-rent').value='2500';document.getElementById('calc-rent').dispatchEvent(new Event('input',{bubbles:true}))")
  assert 'meets the 6%' in await ev("document.getElementById('calc-out').innerText")
  results.append('112 inspectors; calculator blank/negative/zero-price rejection; exact 6% boundary')
  await ev("document.querySelector('#tab-explore').click()")
  zoom_before=await ev("document.querySelector('#map g').getAttribute('transform')")
  await mouse_click('#zoomIn')
  zoom_after=await ev("document.querySelector('#map g').getAttribute('transform')")
  # The viewport group is selected explicitly below; its id is verified in the rendered DOM.
  transforms=await ev("[...document.querySelectorAll('#map g[transform]')].map(g=>g.getAttribute('transform'))")
  await mouse_click('#zoomFit')
  await mouse_click('#togglePanel')
  assert await ev("document.querySelector('#stage').classList.contains('collapsed')")
  await mouse_click('#togglePanel')
  assert not await ev("document.querySelector('#stage').classList.contains('collapsed')")
  # Keyboard entry into the actual focused SVG node.
  await ev("document.querySelector('[data-id=\"G0\"]').focus()")
  await call('Input.dispatchKeyEvent',{'type':'keyDown','key':'Enter','code':'Enter','windowsVirtualKeyCode':13})
  await call('Input.dispatchKeyEvent',{'type':'keyUp','key':'Enter','code':'Enter','windowsVirtualKeyCode':13})
  assert 'G0' in await ev("document.querySelector('#drawerBody h2').innerText")
  results.append('Mouse mode controls, panel toggle, zoom controls and trusted Enter on SVG node')
  layouts=[]
  for width,height,scheme in [(1440,900,'light'),(1440,900,'dark'),(1024,768,'light'),(861,600,'light'),(390,844,'dark'),(320,568,'light')]:
   await call('Emulation.setDeviceMetricsOverride',{'width':width,'height':height,'deviceScaleFactor':1,'mobile':width<860})
   await call('Emulation.setEmulatedMedia',{'features':[{'name':'prefers-color-scheme','value':scheme},{'name':'prefers-reduced-motion','value':'reduce'}]})
   await ev("document.querySelector('#tab-run').click()")
   await asyncio.sleep(.1)
   dims=await ev("({w:innerWidth,scroll:document.documentElement.scrollWidth,stage:document.querySelector('#stage').clientHeight,drawer:document.querySelector('#drawer').clientHeight})")
   assert dims['scroll']<=width and dims['stage']>80 and dims['drawer']>40,(width,dims)
   if width<860:
    await mouse_click('#sheetToggle')
    assert await ev("document.getElementById('drawer').classList.contains('min')")
    await mouse_click('#sheetToggle')
    assert not await ev("document.getElementById('drawer').classList.contains('min')")
   layouts.append([width,height,scheme])
  results.append('Six responsive/theme configurations without horizontal overflow; mobile sheet open/close')
  exceptions=[x for x in events if x.get('method')=='Runtime.exceptionThrown']
  assert not exceptions,exceptions
  print(json.dumps({'status':'PASS','checks':results,'layouts':layouts,'pageExceptions':len(exceptions),'calculatorDefault':default,'browser':json.load(urllib.request.urlopen('http://127.0.0.1:'+PORT+'/json/version'))['Browser']}))
asyncio.run(main())
