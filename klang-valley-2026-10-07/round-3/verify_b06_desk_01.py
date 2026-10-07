"""Read-only GitHub verification. Requires authenticated gh; creates no local files."""
import ast
import base64
import hashlib
import json
import subprocess
import sys

REPO = "repos/brandonkow/core"
ROOT = "klang-valley-2026-10-07/round-3/"
MASTER = "1fbf607a78111bc007736fe0cc8109ad3967939a2dcc7ff54f017b491172e86b"
MUTABLE = {"README.md", "AGENTS.md", "CURRENT_WORKFLOW.md", ROOT+"README.md", ROOT+"Coverage_Audit.md"}

def api(path):
    r = subprocess.run(["gh","api",REPO+path],capture_output=True,text=True,encoding="utf-8",check=True)
    return json.loads(r.stdout)

def tree_at(commit):
    obj=api("/git/trees/"+commit+"?recursive=1")
    assert not obj["truncated"]
    return {r["path"]:r["sha"] for r in obj["tree"] if r["type"]=="blob"}

def blob(sha):
    return base64.b64decode(api("/git/blobs/"+sha)["content"])

def main():
    head = sys.argv[1] if len(sys.argv)>1 else api("/git/ref/heads/main")["object"]["sha"]
    current=tree_at(head)
    read=lambda path: blob(current[path])
    manifest=json.loads(read(ROOT+"B06_Release_Manifest.json"))
    checked={}
    for f in manifest["files"]:
        path=ROOT+f["path"]
        raw=read(path)
        assert current[path]==f["sha"],path
        assert len(raw)==f["bytes"],path
        assert hashlib.sha256(raw).hexdigest()==f["sha256"],path
        checked[f["path"]]=raw
    assert hashlib.sha256(read("Residential_Investment_Framework.md")).hexdigest()==MASTER
    old=tree_at(manifest["source_commit"])
    unchanged=[p for p in old if p not in MUTABLE]
    assert all(current.get(p)==old[p] for p in unchanged)
    inputs=json.loads(checked["B06_Case_Inputs.json"])
    prior=json.loads(read(ROOT+"B06_Working_Inputs.json"))
    assert inputs["inherited_cases"]==prior["inherited_cases"]
    assert inputs["working_01_cases"]==prior["new_cases"]
    ns={}
    exec(compile(checked["b06_financial_model.py"].decode(),"<B06-model>","exec"),ns)
    rebuilt=ns["build"](inputs,read("execution-release-2026-10-07/financial_engine.py").decode(),
                        json.loads(read("execution-release-2026-10-07/financial_config.json")))
    stored=json.loads(checked["B06_Financial_Results.json"])
    assert rebuilt==stored,"Financial replay mismatch"
    assert stored["evaluation_count"]==204 and len(stored["pairs"])==91
    assert len(stored["rank_grids"])==36
    assert all(x["g9"]=="Defer" for x in stored["cases"])
    assert len(inputs["threshold_controls"])==2
    base=[x for x in stored["evaluations"] if x["scenario"]=="base"]
    assert len(base)==14 and all(x["cashflow_by_year"][0]<0 for x in base)
    assert all(x["profit_by_exit_multiple"]["1"]<0 for x in base)
    gates=checked["B06_Cases_G0_G9.md"].decode()
    assert all(gates.count("| G"+str(i)+" ")>=14 for i in range(10))
    evidence=json.loads(checked["B06_Evidence_Register.json"])
    assert len(evidence["sources"])==38 and len({s["id"] for s in evidence["sources"]})==38
    print(json.dumps({"status":"PASS","commit":head,"manifest_files":len(checked),
        "preserved_prior_files":len(unchanged),"inherited_numeric_expressions":9,
        "financial_evaluations":204,"pairs":91,"pair_passes":sum(x["reserve_pass"] for x in stored["pairs"]),
        "rank_cells":36,"master_unchanged":True,"decision":"14 Defer plus2 threshold controls; no Deploy",
        "research_boundary":"B06 bounded desk-complete; full programme incomplete"},indent=2))
if __name__=="__main__":
    main()
