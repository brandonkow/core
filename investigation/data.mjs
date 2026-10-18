
import { BASE } from './engine.mjs';
export const ENGINE_VERSION = 'core-map-2026-10-18';
export const GATES = ['Reference price','Market mechanism','Future buyer','Project quality','Unit quality','Price gap','Exit resilience','Financing & hold','Portfolio fit','Capital decision'];
export function seedWorkspace(){
 const specs=[
 ['p01','Canopy Residences','Garden precinct','Completed condominium',24,520000,520000,2800,360,'G0', 'A defensible clearing-price range is still missing.'],
 ['p02','The Courtyard','Civic quarter','Low-rise residences',8,680000,680000,3400,430,'G3','Verify governance, sinking fund and the planned lift works.'],
 ['p03','Meridian House','Station quarter','Transit apartments',30,460000,460000,2600,310,'G6','Test buyer depth beyond the station-led investment thesis.'],
 ['p04','Parkline Terraces','Garden precinct','Family residences',5,820000,820000,3600,290,'G7','Current standard coverage is negative; funded hold is unproven.'],
 ['p05','Northbank Studios','Station quarter','Compact residences',18,340000,340000,1900,240,'G4','Layout adoption and privacy require an on-site check.'],
 ['p06','Arbor One','River quarter','New launch',32,620000,558000,3000,380,'G0','Gross contract and effective nett basis are separate assumptions.']
 ];
 return {schemaVersion:1,kind:'synthetic',name:'Core demonstration district',properties:specs.map((s,i)=>{
 const [id,name,district,type,floors,gross,nett,rent,fee,stop,question]=s;
 const assessment={...BASE,G0:'stop',G1:'inc',G2:'stop',G3:'unk',G4:'unk',G5:'unk',G6:'unk',G7:'unk',G8:'unk',cov:'unv'};
 if(i>0&&i<5){assessment.G0='ok';assessment.G1='ok';assessment.G2='ok';assessment.G3=i===1?'unk':'ok';assessment.G4=i===4?'unk':'ok';assessment.G5='fair';assessment.G6=i===2?'single':'ok';assessment.G7='unk';}
 return {id,name,district,type,floors,units:Math.max(30,floors*12),beds:i===4?1:3,area:i===4?550:1050+i*75,question,assessment,
 finance:{gross,nett,rent,fee,kind:i===5?'launch':'resale'},
 evidence:['Clearing-price comparables','Governance & capital works','Unit rights & approved layout','Achieved rent & tenant tasks','Buyer depth & financing'].map((title,j)=>({id:id+'-e'+j,title,gate:['G0','G3','G4','G7','G6'][j],status:j===0&&i>0&&i<5?'reviewed':'missing',source:'Synthetic example — no real document',observedAt:'2026-10-18',note:''})),
 tasks:[{id:id+'-t1',title:question,gate:stop,status:'open',owner:'Unassigned',note:''},{id:id+'-t2',title:'Test the strongest alternative explanation with unit-linked evidence.',gate:'G1',status:'open',owner:'Unassigned',note:''}],
 hypothesis:{family:'Omitted variable',claim:'The observed premium may reflect privacy, governance or unit rights.',falsifier:'Matched units with equivalent rights and condition do not sustain the premium.',note:''},
 notes:'',history:[]};
 }),activity:[]};
}
