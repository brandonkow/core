
export function sceneMarkup(properties,selected,{layer='evidence',slice=false,zoom=1,rotate=false,motion=true,floor=12}={}){
 const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const iso=(x,y,z=0)=>{if(rotate)[x,y]=[600-y,x];return [450+(x-y)*.76,98+(x+y)*.37-z];};
 const pts=a=>a.map(p=>iso(...p).join(',')).join(' ');
 const poly=(a,fill,extra='')=>'<polygon points="'+pts(a)+'" fill="'+fill+'" '+extra+'/>';
 const box=(x,y,w,d,h,color,selected=false,z0=0)=>{
 let s=poly([[x,y,h],[x+w,y,h],[x+w,y+d,h],[x,y+d,h]],color[0]);
 s+=poly([[x,y+d,z0],[x+w,y+d,z0],[x+w,y+d,h],[x,y+d,h]],color[1]);
 s+=poly([[x+w,y,z0],[x+w,y+d,z0],[x+w,y+d,h],[x+w,y,h]],color[2]);
 if(selected)s+=poly([[x-4,y-4,0],[x+w+4,y-4,0],[x+w+4,y+d+4,0],[x-4,y+d+4,0]],'none','stroke="#e29555" stroke-width="2.5"');
 return s;
 };
 let s='<svg id="district-svg" viewBox="'+(450-450/zoom)+' '+(310-310/zoom)+' '+900/zoom+' '+620/zoom+'" role="img" aria-label="Interactive schematic district. Select a property from the scene or property list."><defs><pattern id="dotgrid" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".8" fill="#c5d0c6"/></pattern><filter id="shadow"><feDropShadow dx="0" dy="12" stdDeviation="10" flood-color="#243f32" flood-opacity=".12"/></filter></defs><rect width="900" height="620" fill="url(#dotgrid)"/><g filter="url(#shadow)">';
 s+=box(-30,-30,660,570,16,['#dfe6d8','#b7c5b4','#c7d1bf']);
 s+=poly([[-30,240,17],[630,240,17],[630,290,17],[-30,290,17]],'#f2f1e7');
 s+=poly([[270,-30,17],[310,-30,17],[310,540,17],[270,540,17]],'#f2f1e7');
 s+=poly([[-30,475,18],[630,475,18],[630,510,18],[-30,510,18]],'#8eb6ae');
 s+='</g>';
 // Context buildings sit behind the interactive parcels.
 for(let i=0;i<7;i++)s+=box(10+i*80,-12,40,25,35+(i%3)*15,['#e5e7dd','#c7d1c7','#d7ddd2']);
 const positions=[[65,85],[350,65],[465,175],[55,345],[200,335],[405,345],[85,170],[345,180],[500,360],[170,70],[75,410],[490,65]];
 const parcels=properties.slice(0,12).map((p,i)=>({p,x:positions[i][0],y:positions[i][1]})).sort((a,b)=>a.x+a.y-b.x-b.y);
 if(layer!=='evidence'){
 const route=layer==='demand'?[[20,265,20],[290,265,20],[290,80,20],[505,80,20]]:[[60,360,20],[290,360,20],[290,265,20],[560,265,20]];
 const d=route.map((p,i)=>(i?'L':'M')+iso(...p).join(' ')).join(' ');
 s+='<path d="'+d+'" fill="none" stroke="'+(layer==='demand'?'#4e9681':'#d49250')+'" stroke-width="5" stroke-linecap="round" stroke-dasharray="8 8" class="flow"/>';
 if(motion)s+='<circle r="5" fill="#254f43"><animateMotion dur="12s" repeatCount="indefinite" path="'+d+'"/></circle>';
 }
 for(let i=0;i<30;i++){
 const x=20+(i*61)%570,y=i<15?305+(i*29)%135:35+(i*37)%185;
 if((x>260&&x<320))continue;const [cx,cy]=iso(x,y,25);
 s+='<path d="M'+cx+' '+cy+'v10" stroke="#758675" stroke-width="2"/><ellipse cx="'+cx+'" cy="'+(cy-5)+'" rx="7" ry="11" fill="'+(i%2?'#8aa68c':'#72957d')+'"/>';
 }
 for(const {p,x,y} of parcels){
 const active=p.id===selected,h=active&&slice?Math.min(160,20+floor*3.3):Math.min(160,35+p.floors*3.3),w=p.floors<10?95:62,d=65;
 s+='<g class="parcel '+(active?'selected':'')+'" role="button" tabindex="0" aria-label="Inspect '+esc(p.name)+'" data-property="'+esc(p.id)+'">';
 s+=poly([[x-12,y-12,18],[x+w+12,y-12,18],[x+w+12,y+d+12,18],[x-12,y+d+12,18]],active?'#f5d8b6':'#c9d9c3','class="parcel-pad"');
 s+=box(x,y,w,d,h+18,active?['#f5f0df','#d9c4a6','#eee1c6']:['#e8ece1','#b8c7b8','#d2ddcc'],active);
 for(let z=30;z<h+8;z+=14){
 s+=poly([[x+5,y+d+.2,z],[x+w-5,y+d+.2,z],[x+w-5,y+d+.2,z+5],[x+5,y+d+.2,z+5]],active?'#8c9f8c':'#849d90');
 s+=poly([[x+w+.2,y+5,z],[x+w+.2,y+d-5,z],[x+w+.2,y+d-5,z+5],[x+w+.2,y+5,z+5]],active?'#748f84':'#9aafa0');
 }
 s+=box(x+10,y+10,w-20,d-20, h+20,active?['#d3ddc4','#bccdb4','#c8d6bf']:['#d6dfd0','#b8c7b8','#c4d0bf'],false,h+18);
 if(slice&&active){
 s+=poly([[x+8,y+8,h+21],[x+w-8,y+8,h+21],[x+w-8,y+d-8,h+21],[x+8,y+d-8,h+21]],'#fff6e3');
 s+='<path d="M'+iso(x+w/2,y+8,h+22).join(' ')+'L'+iso(x+w/2,y+d-8,h+22).join(' ')+'" stroke="#bc9972" stroke-width="2"/>';
 }
 const [cx,cy]=iso(x+w/2,y+d/2,h+44);
 s+='<g class="scene-label"><rect x="'+(cx-18)+'" y="'+(cy-17)+'" width="36" height="25" rx="7" fill="'+(active?'#213e35':'#fafbf5')+'" stroke="#c9d1c5"/><text x="'+cx+'" y="'+cy+'" text-anchor="middle" fill="'+(active?'#fff':'#52675b')+'" font-size="11" font-weight="700">'+esc(p.id.replace('p','').slice(0,4))+'</text></g>';
 if(active)s+='<ellipse class="beacon" cx="'+cx+'" cy="'+(cy-29)+'" rx="5" ry="5" fill="#d28d4f"/>';
 s+='</g>';
 }
 const [tx,ty]=iso(330,282,19);
 s+='<text x="'+tx+'" y="'+ty+'" transform="rotate(26 '+tx+' '+ty+')" font-size="10" letter-spacing="3" fill="#7c8e7b">CORE AVENUE</text>';
 s+='<g transform="translate(785,500)"><circle r="27" fill="#f3f5ed" stroke="#c7d0c3"/><path d="M0,-19 L-5,9 L0,5 L5,9Z" fill="#294f41"/><text y="42" text-anchor="middle" font-size="10" fill="#738275">N · SCHEMATIC</text></g></svg>';
 return s;
}
