"""Read-only GitHub verification for the immutable B06 working packet 01."""
import ast, base64, hashlib, json, subprocess, sys

REPO = "repos/brandonkow/core"
ROOT = "klang-valley-2026-10-07/round-3/"
def api(path):
    return json.loads(subprocess.check_output(["gh", "api", REPO + path], text=True, encoding="utf-8"))
def main():
    ref = sys.argv[1] if len(sys.argv) > 1 else "main"
    head = api("/commits/" + ref)["sha"]
    tree = api("/git/trees/" + head + "?recursive=1")
    assert not tree.get("truncated")
    blobs = {r["path"]: r["sha"] for r in tree["tree"] if r["type"] == "blob"}
    def read(path):
        data = api("/git/blobs/" + blobs[path])
        return base64.b64decode(data["content"])
    manifest = json.loads(read(ROOT + "B06_Working_01_Manifest.json"))
    count = 0
    for f in manifest["files"]:
        b = read(ROOT + f["path"])
        assert len(b) == f["bytes"]
        assert hashlib.sha256(b).hexdigest() == f["sha256"]
        assert blobs[ROOT + f["path"]] == f["sha"]
        count += 1
    master = read("Residential_Investment_Framework.md")
    assert hashlib.sha256(master).hexdigest() == manifest["master_sha256"]
    fin = json.loads(read(ROOT + "B06_Working_Financials.json"))
    cfg = json.loads(read("execution-release-2026-10-07/financial_config.json"))
    assert cfg == fin["config"]
    eng = read("execution-release-2026-10-07/financial_engine.py")
    assert hashlib.sha256(eng).hexdigest() == fin["financial_engine_sha256"]
    mod = ast.parse(eng.decode("utf-8"))
    names = {"payment", "evaluate", "check_financial_identities"}
    ns = {"CFG": cfg}
    exec(compile(ast.Module(body=[n for n in mod.body if isinstance(n, ast.FunctionDef) and n.name in names], type_ignores=[]), "<frozen functions>", "exec"), ns)
    inputs = json.loads(read(ROOT + "B06_Working_Inputs.json"))
    assert len(inputs["new_cases"]) == 3
    assert len(inputs["inherited_cases"]) == 6
    for c in inputs["inherited_cases"]:
        original = next(x for x in json.loads(read(c["origin"]))["cases"] if x["id"] == c["id"])
        assert {k: c[k] for k in original} == original
    checks = 0
    for case in fin["cases"]:
        c = case["case"]
        assert c["g9"] == "Defer"
        for name, kw in case["scenario_parameters"].items():
            replay = ns["evaluate"](c, **kw)
            ns["check_financial_identities"](replay, c, kw.get("exit_extra_cost", 0))
            assert replay == case["scenarios"][name]
            checks += 1
    up = fin["ridge_furnished_upgrade"]
    replay = ns["evaluate"](up["case"])
    ns["check_financial_identities"](replay, up["case"])
    assert replay == up["result"]
    checks += 1
    assert checks == fin["checks"] == 120
    by = {x["case"]["id"]: x for x in fin["cases"]}
    for pair in fin["pairs"]:
        a, b = [by[i]["scenarios"]["combined12"] for i in pair["ids"]]
        path = [cfg["synthetic_cash"] - a["entry_cash"] - b["entry_cash"]]
        for x, y in zip(a["schedule"], b["schedule"]):
            path.append(path[-1] + x["cashflow"] + y["cashflow"])
        assert path == pair["cash_path"]
        assert min(path) == pair["minimum_cash"]
        assert pair["reserve_pass"] == (min(path) >= cfg["synthetic_protected_reserve"])
    assert len(fin["pairs"]) == 36
    report = read(ROOT + "B06_Working_01.md").decode("utf-8")
    for gate in range(10):
        assert report.count("| G" + str(gate) + " ") == 3
    assert "B06 remains in progress" in report
    print(json.dumps({"status": "PASS", "commit": head, "manifest_files": count, "financial_evaluations": checks, "pair_paths": len(fin["pairs"]), "inherited_input_rows_unchanged": 6, "master_unchanged": True, "research_status": "partial; no regional closeout or Deploy"}))
if __name__ == "__main__":
    main()
