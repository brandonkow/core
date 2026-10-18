
export type Gate = 'G0'|'G1'|'G2'|'G3'|'G4'|'G5'|'G6'|'G7'|'G8';
export type CapitalDecision = 'deploy'|'defer'|'reject'|'preserve';
export interface Evidence {id:string;title:string;gate:Gate;status:'missing'|'received'|'reviewed'|'conflicting';source:string;observedAt:string;note:string}
export interface InvestigationTask {id:string;title:string;gate:Gate;status:'open'|'in-progress'|'done';owner:string;note:string}
export interface Finance {kind:'launch'|'resale';gross:number|null;nett:number|null;rent:number|null;fee:number|null}
export interface GateInputs {G0:'ok'|'stop';G1:'ok'|'inc';G2:'ok'|'stop';G3:'ok'|'unk'|'fail';G4:'ok'|'unk'|'fail';G5:'val'|'fair'|'unk';G6:'ok'|'single'|'unk'|'fail';G7:'ok'|'unk'|'fail';G8:'ok'|'unk'|'cap';div:'none'|'resolved'|'partial'|'unresolved';residual:'no'|'yes';cov:'pos'|'neg'|'unv';tr:'no'|'yes';role:'comp'|'defu'|'spec'|'inc'}
export interface DecisionSnapshot {id:string;at:string;version:string;decision:CapitalDecision;note:string;inputs:GateInputs;finance:Finance;reasons:[string,string][];evidence:Evidence[]}
export interface Property {id:string;name:string;district:string;type:string;floors:number;units:number;beds:number;area:number;question:string;notes:string;assessment:GateInputs;finance:Finance;evidence:Evidence[];tasks:InvestigationTask[];hypothesis:{family:string;claim:string;falsifier:string;note:string};history:DecisionSnapshot[]}
export interface Workspace {schemaVersion:1;kind:'synthetic'|'imported';name:string;properties:Property[];activity:{at:string;text:string}[]}
export interface WorkspaceRepository {label:string;load():Promise<Workspace>;save(workspace:Workspace):Promise<unknown>}
