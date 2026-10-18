// Extracted without changes from the 18 October 2026 decision map. Run tests to verify parity.
const FORM = [
  ['div','Divergence flag',[['none','None material'],['resolved','Resolved'],['partial','Partially resolved'],['unresolved','Unresolved']]],
  ['residual','Residual divergence test',[['no','Not demonstrated'],['yes','Gate-compatible; adverse explanation survived']]],
  ['G0','G0 · reference price',[['ok','Clearing price normalised'],['stop','Unresolved']]],
  ['G1','G1 · market mechanism',[['ok','Identified'],['inc','Incomplete']]],
  ['G2','G2 · future buyer',[['ok','Defined'],['stop','Vague']]],
  ['G3','G3 · project quality',[['ok','Supported'],['unk','Unknown'],['fail','Established hard-gate failure']]],
  ['G4','G4 · unit quality',[['ok','Supported'],['unk','Unknown'],['fail','Established structural failure']]],
  ['G5','G5 · price gap',[['val','Validated, recoverable'],['fair','Fair price, no discount claimed'],['unk','Gap unexplained']]],
  ['G6','G6 · exit',[['ok','Independent exits'],['single','Single-point exit'],['unk','Unknown'],['fail','Established exit failure']]],
  ['G7','G7 · financing & forced hold',[['ok','Survives stress'],['unk','Unknown'],['fail','Established structural failure']]],
  ['cov','Standard coverage 90·4·35',[['pos','Non-negative'],['neg','Shortfall'],['unv','Unverified']]],
  ['tr','Shortfall transition record',[['no','Not evidenced'],['yes','Fully evidenced']]],
  ['G8','G8 · portfolio',[['ok','Fits mandate'],['unk','Unknown'],['cap','Allocation constraint']]],
  ['role','Declared role',[['comp','Compounder'],['defu','Defensive utility'],['spec','Special situation'],['inc','Income engine']]]
];
const BASE = {div:'none',residual:'no',G0:'ok',G1:'ok',G2:'ok',G3:'ok',G4:'ok',G5:'fair',G6:'ok',G7:'ok',cov:'pos',tr:'no',G8:'ok',role:'comp'};
const PRESETS = [
  ['Aligned, but governance and title evidence missing','Integration audit · boundary scenario 1',{G3:'unk',G7:'unk'}],
  ['Unknown G0 with a deeper discount offered','Integration audit · boundary scenario 10',{div:'unresolved',G0:'stop',G5:'unk',role:'spec'}],
  ['Proven structural failure, optimistic judgment','Integration audit · boundary scenario 11',{div:'unresolved',G4:'fail'}],
  ['Asset unresolved, clear capital constraint','Integration audit · boundary scenario 12',{G3:'unk',G8:'cap'}],
  ['Current shortfall, no transition record','Execution standard §2',{cov:'neg',tr:'no',role:'inc'}],
  ['Special situation without a validated discount','Execution standard §2, item 9',{role:'spec',G5:'fair'}],
  ['Every gate supported (hypothetical)','Master G9 · Deploy',{}]
];
const ROLE_NODE = {comp:'COMP', defu:'DEFU', spec:'SPEC', inc:'INC'};
const ROLE_NAME = {comp:'Compounder', defu:'Defensive Utility Asset', spec:'Special Situation', inc:'Income Engine'};

function evaluate(s){
  const gs = {};
  gs.G0 = s.G0 === 'ok' ? 'pass' : 'stop';
  gs.G1 = s.G1 === 'ok' ? 'pass' : 'unk';
  gs.G2 = s.G2 === 'ok' ? 'pass' : 'stop';
  gs.G3 = {ok:'pass', unk:'unk', fail:'fail'}[s.G3];
  gs.G4 = {ok:'pass', unk:'unk', fail:'fail'}[s.G4];
  const pre = ['G0','G1','G2','G3','G4'].every(g => gs[g] === 'pass');
  gs.G5 = !pre ? 'blocked' : (s.G5 === 'unk' ? 'unk' : 'pass');
  gs.G6 = {ok:'pass', single:'unk', unk:'unk', fail:'fail'}[s.G6];
  gs.G7 = {ok:'pass', unk:'unk', fail:'fail'}[s.G7];
  gs.G8 = {ok:'pass', unk:'unk', cap:'cap'}[s.G8];
  const shortfall = s.cov === 'neg', trOK = shortfall && s.tr === 'yes';
  const fails = ['G3','G4','G6','G7'].filter(g => gs[g] === 'fail');
  const reasons = [], notes = [];
  let d;
  if (fails.length) {
    d = 'reject';
    reasons.push([`Structural failure independently established at ${fails.join(', ')}. A confirmed structural failure can produce Reject independently of other unknowns.`, 'Execution standard §6 · Master G9']);
    reasons.push(['A flag, a lower price or a smaller position cannot waive it.', 'Master §5 · decision precedence']);
  } else if (gs.G8 === 'cap') {
    d = 'preserve';
    reasons.push(['An independently established allocation constraint supports Preserve Capacity.', 'Master §5 · decision precedence']);
    if (['G0','G1','G2','G3','G4','G5','G6','G7'].some(g => gs[g] !== 'pass') || s.div === 'unresolved' || s.cov !== 'pos') reasons.push(['Other gates, flags or coverage are not all clear; Preserve Capacity makes no claim that they are.', 'Integration audit · scenario 12']);
  } else {
    if (gs.G0 === 'stop') reasons.push(['G0 clearing price unresolved: STOP. No discount claim allowed.', 'Master G0']);
    if (gs.G1 === 'unk') reasons.push(['G1 mechanism incomplete: MRT, mall, brand, prime location or launch take-up alone does not explain ownership.', 'Master G1']);
    if (gs.G2 === 'stop') reasons.push(['G2 future buyer vague: STOP.', 'Master G2']);
    ['G3','G4','G7'].forEach(g => { if (gs[g] === 'unk') reasons.push([`${g} evidence unknown: insufficient evidence ordinarily yields Defer.`, 'Master §5 · decision precedence']); });
    if (s.G6 === 'single') reasons.push(['G6 Single-Point Exit Failure flagged: the exit depends on one catalyst or one buyer.', 'Master G6']);
    if (s.G6 === 'unk') reasons.push(['G6 exit unknown: future buyer, alternatives and weak-exit cases are not yet defined.', 'Execution standard §4']);
    if (pre && s.G5 === 'unk') reasons.push(['G5 gap unexplained: why is it there, is it reversible, how much is recoverable?', 'Master G5']);
    if (gs.G8 === 'unk') reasons.push(['G8 capital constraints unknown: only a labelled synthetic allocation experiment is possible.', 'Execution standard §4']);
    if (s.div === 'unresolved') reasons.push(['Divergence flag unresolved: preserve the affected gate stop. Waiting or a favourable price move does not resolve it.', 'Master §5 · unresolved divergence']);
    if (s.div === 'partial' && s.residual !== 'yes') reasons.push(['Residual divergence needs an explicit, evidenced gate-compatibility assessment and a thesis that survives the plausible adverse explanation.', 'Master §5 · decision precedence']);
    if (s.cov === 'unv') reasons.push(['Standard coverage unverified: reliable rent, loan basis or fee is missing.', 'Execution supplement §1']);
    if (shortfall && !trOK) reasons.push(['Current standard shortfall with no evidenced transition record: an unverified forecast remains Defer at lowest research priority.', 'Execution standard §2']);
    if (s.role === 'spec' && !(pre && s.G5 === 'val')) reasons.push(['Special Situation needs a validated, recoverable discount at G5. Do not disguise one role as another.', 'Master §10 · Execution standard §2']);
    if (reasons.length) d = 'defer';
    else {
      d = 'deploy';
      reasons.push([`Evidence sufficient; asset and portfolio gates pass. Declared role: ${ROLE_NAME[s.role]}.`, 'Master G9 · §10']);
      if (s.role === 'inc' && s.cov === 'pos') reasons.push(['Income Engine default met: non-negative standard coverage at entry.', 'Execution standard §2']);
    }
  }
  if (d !== 'defer') {
    if (shortfall) reasons.push([trOK && d === 'deploy' ? 'Current standard shortfall stays visible: Deploy rests on the evidenced transition record as a reasoned exception; forecast rent does not replace the negative number.' : 'Current standard shortfall stays visible in G7/G8 and in this rationale; by itself it is not a structural Reject.', 'Execution supplement §1 · Execution standard §2']);
    if (s.cov === 'unv') reasons.push(['Standard coverage is still unverified.', 'Execution supplement §1']);
    if (s.div === 'unresolved') reasons.push(['Divergence flag still unresolved; it is carried into G9 with its higher protection.', 'Master §9 · G9 watchpoint']);
  }
  if (!pre) notes.push('G5 not assessable: G0–G4 have not all survived. Downstream gates can run as conditional diagnostics but do not clear upstream unknowns.');
  if (s.div === 'partial') notes.push('Partially resolved flag: the residual components keep a higher proof and safety burden. Deploy is possible only if that residual is compatible with the gate standards and the thesis survives its plausible adverse explanation.');
  if (s.div === 'unresolved' || s.div === 'partial') notes.push(gs.G0 === 'stop' ? 'Required margin of safety rises, but with clearing price unknown it cannot be responsibly quantified.' : 'Required margin of safety rises and position conviction falls.');
  if (trOK) notes.push('Shortfall exception: the evidenced transition record allows a reasoned G9 proposal. The current negative coverage stays visible and is not replaced by forecast rent.');
  if (d === 'deploy') notes.push('This is the logical outcome of the inputs you set, not a purchase instruction. Purchase execution is a separate authorised action.');
  let prio;
  if (d === 'reject') prio = 'Stop active research; reopen only on identified evidence about the failure.' + (shortfall ? ' The shortfall also keeps it in the lowest research tier.' : '');
  else if (shortfall) prio = 'Lowest research-priority tier while the shortfall remains.';
  else if (d === 'defer') prio = 'Rank by the decision value of the next unknown; at most three immediate decision-changing unknowns.';
  else if (d === 'preserve') prio = 'Event-watch; unused capacity is kept as optionality.';
  else if (s.div === 'partial') prio = 'Residual flag components stay under review; reopen on the specified evidence or material new evidence.';
  else prio = 'Not a research question at this point.';
  return {d, gs, pre, reasons, notes, prio, shortfall, trOK};
}

/* Standard-coverage arithmetic in integer sen. Pure, so verify.cjs can test it outside the browser. */
function calcStandard(P, R, M, B = P){
  const Ps = Math.round(P * 100), Rs = Math.round(R * 100), Ms = Math.round(M * 100), Bs = Math.round(B * 100);
  if (![Ps, Rs, Ms, Bs].every(Number.isSafeInteger) || Ps <= 0 || Bs <= 0 || Rs < 0 || Ms < 0) return null;
  const L = 0.9 * Bs / 100, r = 0.04 / 12, inst = L * r / (1 - Math.pow(1 + r, -420));
  const cov = Rs / 100 - inst - Ms / 100;
  if (![L, inst, cov].every(Number.isFinite)) return null;
  let zeroSen = Math.ceil(inst * 100 + Ms);
  if (!Number.isSafeInteger(zeroSen)) return null;
  while (zeroSen / 100 - inst - Ms / 100 < 0) zeroSen++;
  return {L, inst, cov, zeroSen, sixSen: Math.ceil(Ps / 200),
    yieldMicro: 1200n * BigInt(Rs) * 1000000n / BigInt(Ps),   // gross yield % x 10^6, truncated
    meets: 200n * BigInt(Rs) >= BigInt(Ps)};                  // 12 R / P >= 6%  <=>  200 R >= P
}

function gateTrace(gs){
  const prefix = [];
  let firstStop = null;
  const conditional = [];
  for(let i=0;i<9;i++){
    const g = 'G'+i;
    if(firstStop === null && gs[g] === 'pass') prefix.push(g);
    else { if(firstStop === null) firstStop = g; if(gs[g] === 'pass') conditional.push(g); }
  }
  return {prefix,firstStop,conditional};
}


export { FORM, BASE, PRESETS, ROLE_NAME, evaluate, calcStandard, gateTrace };
