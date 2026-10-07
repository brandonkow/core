"""Spacing-only editorial pass; preserve link destinations and long identifiers."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parent
def prose(s):
    parts=re.split(r'(\b[0-9a-f]{16,}\b)',s)
    for i,t in enumerate(parts):
        if re.fullmatch(r'[0-9a-f]{16,}',t):continue
        t=t.replace('existingReject','existing Reject').replace('retainDefer','retain Defer')
        t=t.replace('olderCheras','older Cheras').replace('A350','An RM350')
        t=t.replace('fragile.222','fragile. 222').replace('wrong.2/3','wrong. 2/3')
        t=re.sub(r'\b([A-Za-z]{3,})(\d)',lambda m:m[0] if m[1] in ('SHA','Univ') else m[1]+' '+m[2],t)
        t=re.sub(r'(\d)([A-Za-z]{2,})',r'\1 \2',t)
        t=re.sub(r'\b([A-Za-z]{3,})(\d)',lambda m:m[0] if m[1] in ('SHA','Univ') else m[1]+' '+m[2],t)
        t=re.sub(r'(?<=[a-z])(?=RM(?:\d|\b))',' ',t)
        t=re.sub(r'\bRM(?=[\d+-])','RM ',t)
        t=re.sub(r'%(?=[A-Za-z])','% ',t)
        t=re.sub(r'(?<=[a-z])(?=[+-]\d)',' ',t)
        t=re.sub(r'(\d)(?=R[12]\b)',r'\1 ',t)
        t=re.sub(r',(?=[A-Za-z])',', ',t)
        t=re.sub(r',(?=\d+[A-Za-z])',', ',t)
        parts[i]=t
    return ''.join(parts)
for p in ROOT.rglob('*.md'):
    if p.name in ('Research_Lock.md','Validation_Report.md'):continue
    parts=re.split(r'(\]\([^\n]*?\))',p.read_text(encoding='utf-8'))
    text=''.join(x if x.startswith('](') else prose(x) for x in parts)
    p.write_text(text,encoding='utf-8')
